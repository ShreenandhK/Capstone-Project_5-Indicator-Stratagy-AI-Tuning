#!/usr/bin/env python
"""CRB backtest CLI (SPEC Section 6).

  run_backtest.py is  --config configs/run_NN.json   logged In-Sample run (counts against the 25-run cap)
  run_backtest.py oos --frozen FROZEN_PARAMS.json    one-shot Out-of-Sample run (LOCKED afterwards)
  run_backtest.py smoke                              defaults on the DEV window; prints trade count + runtime only

Environment (for tests): CRB_BACKTEST_ROOT redirects configs/results/logs/critic/FROZEN_PARAMS (and the
default data path to <root>/data/BTCUSDT_1h.csv); CRB_DATA_FILE overrides the data file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import log_tools  # noqa: E402
from engine import params as PRM  # noqa: E402
from engine.broker import BASE_COSTS, STRESS_COSTS, simulate  # noqa: E402
from engine.metrics import buy_and_hold, compute_metrics, daily_equity  # noqa: E402

IS_START = pd.Timestamp("2023-01-01 00:00", tz="UTC")
IS_END = pd.Timestamp("2025-06-30 23:00", tz="UTC")
OOS_START = pd.Timestamp("2025-07-01 00:00", tz="UTC")
DEV_START = pd.Timestamp("2022-04-01 00:00", tz="UTC")
DEV_END = pd.Timestamp("2022-12-31 23:00", tz="UTC")
MAX_RUNS = log_tools.MAX_RUNS


class GuardError(RuntimeError):
    """A guard refused the command. Nothing is logged."""


def compute_signals(df: pd.DataFrame, p: dict) -> pd.DataFrame:
    """Indirection so tests can spy on exactly what reaches the signal engine."""
    from engine.signals import compute_signals as _cs
    return _cs(df, p)


# ---------------------------------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------------------------------
def load_data(end_inclusive=None, path=None) -> pd.DataFrame:
    """Load OHLCV (DatetimeIndex = bar open time, UTC). Rows with time > end_inclusive are dropped HERE,
    before anything else sees the frame."""
    path = Path(path) if path is not None else log_tools.get_paths().data
    raw = pd.read_csv(path)
    need = ["time", "open", "high", "low", "close", "volume"]
    missing = [c for c in need if c not in raw.columns]
    if missing:
        raise ValueError(f"{path}: missing columns {missing}")
    idx = pd.DatetimeIndex(pd.to_datetime(raw["time"], utc=True), name="time")
    df = pd.DataFrame({c: raw[c].to_numpy(dtype=float) for c in need[1:]}, index=idx)
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError(f"{path}: bar times must be strictly increasing")
    if end_inclusive is not None:
        end = pd.Timestamp(end_inclusive)
        end = end.tz_localize("UTC") if end.tzinfo is None else end.tz_convert("UTC")
        df = df.loc[df.index <= end].copy()
    return df


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_data_file(path: Path) -> str:
    if not path.exists():
        raise GuardError(f"data file not found: {path}")
    sha = file_sha256(path)
    meta = path.with_name(path.name.replace(".csv", ".meta.json"))
    if meta.exists():
        try:
            m = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            m = {}
        if m.get("sha256") and m["sha256"] != sha:
            raise GuardError(f"data sha256 {sha} does not match {meta.name} ({m['sha256']})")
    return sha


# ---------------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------------
def _resolve(arg: str, root: Path) -> Path:
    p = Path(arg)
    if p.is_absolute():
        return p
    if (Path.cwd() / p).exists():
        return Path.cwd() / p
    return root / p


def _jsonable(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, datetime)):
        return o.isoformat()
    raise TypeError(f"not JSON serialisable: {type(o).__name__}")


def _dumps(o, **kw) -> str:
    return json.dumps(o, default=_jsonable, **kw)


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_signals(sig: pd.DataFrame, df: pd.DataFrame) -> None:
    if len(sig) != len(df) or not sig.index.equals(df.index):
        raise ValueError("compute_signals returned a frame not aligned with the data")


def _write_results(out_dir: Path, metrics: dict, base, stress, df: pd.DataFrame) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tr, eq, info = base
    _, seq, _ = stress
    (out_dir / "metrics.json").write_text(_dumps(metrics, indent=2), encoding="utf-8")
    trades = tr.copy()
    for c in ("entry_time", "exit_time"):
        trades[c] = trades[c].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    trades.to_csv(out_dir / "trades.csv", index=False, float_format="%.10g")
    _, bh = buy_and_hold(df, eq.index, float(info["initial_capital"]))
    daily = pd.DataFrame({"equity": daily_equity(eq), "equity_stress": daily_equity(seq),
                          "buy_and_hold": daily_equity(bh)})
    daily.index = daily.index.strftime("%Y-%m-%d")
    daily.index.name = "date"
    daily.to_csv(out_dir / "equity_daily.csv", float_format="%.10g")


def _summary(prefix: str, m: dict) -> str:
    f = log_tools.fmt
    st = m.get("stress") or {}
    lines = [
        f"{prefix}",
        f"  sharpe {f(m['sharpe'])} | sortino {f(m['sortino'])} | net_return_pct {f(m['net_return_pct'])} | "
        f"max_dd_pct {f(m['max_dd_pct'])} | calmar {f(m['calmar'])}",
        f"  trades {m['trades']} | profit_factor {f(m['profit_factor'])} | win_rate_pct {f(m['win_rate_pct'])} | "
        f"exposure_pct {f(m['exposure_pct'])} | psr0 {f(m['psr0'])}",
        f"  stress: net_return_pct {f(st.get('net_return_pct'))} | sharpe {f(st.get('sharpe'))} | "
        f"PF {f(st.get('profit_factor'))} | trades {st.get('trades')}",
        f"  buy&hold: net_return_pct {f(m['buy_and_hold']['net_return_pct'])} | sharpe {f(m['buy_and_hold']['sharpe'])}",
        "  subperiods: " + " | ".join(f"{k}: net {f(v['net_return_pct'])} sharpe {f(v['sharpe'])} trades {v['trades']}"
                                      for k, v in m["subperiods"].items()),
    ]
    if "gates" in m:
        lines.append("  gates: " + " ".join(f"{k}={'PASS' if g['pass'] else 'FAIL'}" for k, g in m["gates"].items())
                     + f" | eligible {m['eligible']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------------------------------
def cmd_is(config_arg: str) -> int:
    P = log_tools.get_paths()
    cfg_path = _resolve(config_arg, P.root)
    m = re.fullmatch(r"run_(\d+)\.json", cfg_path.name)
    if not m:
        raise GuardError(f"config file must be named run_NN.json, got {cfg_path.name}")
    nn = int(m.group(1))
    canonical = P.configs / f"{log_tools.run_name(nn)}.json"
    if not cfg_path.exists() or cfg_path.resolve() != canonical.resolve():
        raise GuardError(f"config must be the existing file {canonical}")
    n_logged = log_tools.count_lines(P.jsonl)
    if nn > MAX_RUNS or n_logged >= MAX_RUNS:
        raise GuardError(f"run cap reached: {n_logged} runs logged, cap {MAX_RUNS} (requested run {nn})")
    if nn != n_logged + 1:
        raise GuardError(f"run id {nn} != logged runs + 1 = {n_logged + 1}")
    records = log_tools.read_jsonl(P.jsonl)
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        full = PRM.validate(cfg)
    except (ValueError, json.JSONDecodeError) as e:
        raise GuardError(f"invalid config: {e}") from e
    h = PRM.config_hash(full)
    dup = [r["run_id"] for r in records if r.get("config_hash") == h]
    if dup:
        raise GuardError(f"config hash {h} already logged as run {dup[0]:02d}")
    data_sha = check_data_file(P.data)

    t0 = time.perf_counter()
    df = load_data(end_inclusive=IS_END, path=P.data)          # truncation BEFORE any computation
    if len(df) == 0 or df.index.max() > IS_END:
        raise GuardError("IS truncation failed")
    if df.index.min() > IS_START or df.index.max() < IS_START:
        raise GuardError("data does not cover the IS window")
    sig = compute_signals(df, full)
    _check_signals(sig, df)
    t_sig = time.perf_counter() - t0
    base = simulate(df, sig, full, IS_START, IS_END, BASE_COSTS)
    stress = simulate(df, sig, full, IS_START, IS_END, STRESS_COSTS)
    metrics = compute_metrics(*base, df, IS_START, IS_END, period="IS", stress=stress)
    runtime = time.perf_counter() - t0
    metrics["runtime_s"] = runtime
    metrics["signals_runtime_s"] = t_sig

    # re-check the slot right before committing (concurrent invocations)
    if log_tools.count_lines(P.jsonl) != nn - 1:
        raise GuardError("tuning_log.jsonl changed during the run; not logging")
    run_dir = P.results / log_tools.run_name(nn)
    if run_dir.exists():                      # stale output of a crashed, unlogged attempt
        shutil.rmtree(run_dir)
    _write_results(run_dir, metrics, base, stress, df)
    record = {
        "run_id": nn,
        "utc_timestamp": _utc_now(),
        "config_hash": h,
        "config_file": f"configs/{canonical.name}",
        "params_full": full,
        "params_diff_vs_defaults": PRM.diff_vs_defaults(full),
        "metrics": metrics,
        "gates": metrics["gates"],
        "eligible": metrics["eligible"],
        "runtime_s": runtime,
        "data_sha256": data_sha,
        "data_last_bar_used": str(df.index.max()),
        "costs": {"base": BASE_COSTS, "stress": STRESS_COSTS},
    }
    P.logs.mkdir(parents=True, exist_ok=True)
    with open(P.jsonl, "a", encoding="utf-8") as f:
        f.write(_dumps(record, sort_keys=False) + "\n")
        f.flush()
    log_tools.render(P)
    print(_summary(f"IS run {nn:02d} hash {h} runtime {runtime:.2f}s (logged {nn}/{MAX_RUNS})", metrics))
    return 0


def cmd_oos(frozen_arg: str) -> int:
    P = log_tools.get_paths()
    lock = P.oos / "LOCK"
    if lock.exists():
        raise GuardError(f"OOS already run ({lock} exists); never re-runnable")
    fpath = _resolve(frozen_arg, P.root)
    if not fpath.exists() or fpath.resolve() != P.frozen.resolve():
        raise GuardError(f"frozen params must be the existing file {P.frozen}")
    try:
        frozen = json.loads(fpath.read_text(encoding="utf-8"))
        full = PRM.validate(frozen["params_full"])
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        raise GuardError(f"invalid FROZEN_PARAMS.json: {e}") from e
    h = PRM.config_hash(full)
    if h != frozen.get("config_hash"):
        raise GuardError(f"FROZEN_PARAMS hash mismatch: params hash {h} != embedded {frozen.get('config_hash')}")
    errors, _ = log_tools.verify(P)
    if errors:
        raise GuardError("log verify failed:\n  " + "\n  ".join(errors))
    data_sha = check_data_file(P.data)

    P.oos.mkdir(parents=True, exist_ok=True)
    with open(lock, "x", encoding="utf-8") as f:                 # LOCK first (exclusive create)
        f.write(_dumps({"locked_utc": _utc_now(), "run_id": frozen.get("run_id"), "config_hash": h,
                        "data_sha256": data_sha}, indent=2))
    t0 = time.perf_counter()
    df = load_data(end_inclusive=None, path=P.data)               # continuous series, warm from 2022
    window_end = df.index.max()
    if window_end < OOS_START:
        raise GuardError("data has no OOS bars")
    sig = compute_signals(df, full)
    _check_signals(sig, df)
    base = simulate(df, sig, full, OOS_START, window_end, BASE_COSTS)
    stress = simulate(df, sig, full, OOS_START, window_end, STRESS_COSTS)
    metrics = compute_metrics(*base, df, OOS_START, window_end, period="OOS", stress=stress)
    metrics["runtime_s"] = time.perf_counter() - t0
    metrics["frozen_run_id"] = frozen.get("run_id")
    metrics["config_hash"] = h
    metrics["data_sha256"] = data_sha
    _write_results(P.oos, metrics, base, stress, df)
    print(_summary(f"OOS FINAL (frozen run {frozen.get('run_id')}, hash {h}) window {OOS_START} -> {window_end}",
                   metrics))
    return 0


def cmd_smoke() -> int:
    P = log_tools.get_paths()
    full = PRM.validate({})
    t0 = time.perf_counter()
    df = load_data(end_inclusive=DEV_END, path=P.data)           # nothing at/after 2023-01-01 is loaded
    if df.index.max() > DEV_END:
        raise GuardError("DEV truncation failed")
    sig = compute_signals(df, full)
    _check_signals(sig, df)
    t1 = time.perf_counter()
    tr, eq, info = simulate(df, sig, full, DEV_START, DEV_END, BASE_COSTS)
    t2 = time.perf_counter()
    print(f"smoke: runs, {len(tr)} trades, runtime {t2 - t0:.2f}s (signals {t1 - t0:.2f}s, broker {t2 - t1:.3f}s)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_is = sub.add_parser("is")
    a_is.add_argument("--config", required=True)
    a_oos = sub.add_parser("oos")
    a_oos.add_argument("--frozen", required=True)
    sub.add_parser("smoke")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "is":
            return cmd_is(a.config)
        if a.cmd == "oos":
            return cmd_oos(a.frozen)
        return cmd_smoke()
    except GuardError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
