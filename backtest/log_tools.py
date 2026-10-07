#!/usr/bin/env python
"""Tuning-log tooling (SPEC Section 7).

  log_tools.py render   regenerate logs/tuning_log.md and logs/leaderboard.md
  log_tools.py verify   integrity check of the machine log, configs and results (prints OK / errors)
  log_tools.py best     apply the pre-registered selection rule (SPEC Section 8)
  log_tools.py freeze   write FROZEN_PARAMS.json once (refuses if it exists or verify fails)
  log_tools.py dsr      print the Deflated Sharpe Ratio of the current best

Paths honour CRB_BACKTEST_ROOT (configs/results/logs/critic/FROZEN_PARAMS) and CRB_DATA_FILE.
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

MAX_RUNS = 25
SELECTION_RULE = ("Eligible = G1 trades>=100, G2 profit_factor>1.0, G3 stress.net_return_pct>0, "
                  "G4 >=2 of 3 IS sub-periods (2023, 2024, 2025H1) net_return_pct>0. "
                  "Best = eligible run with highest IS sharpe (ties -> more trades). "
                  "Fallback if none eligible: highest sharpe among runs with trades>=30, flagged "
                  "'FAILED PRE-REGISTERED GATES'.")


# ---------------------------------------------------------------------------------------------------
def get_paths() -> SimpleNamespace:
    root = Path(os.environ.get("CRB_BACKTEST_ROOT") or CODE_DIR)
    data = os.environ.get("CRB_DATA_FILE")
    logs = root / "logs"
    results = root / "results"
    return SimpleNamespace(
        root=root, configs=root / "configs", results=results, logs=logs, critic=root / "critic",
        jsonl=logs / "tuning_log.jsonl", md=logs / "tuning_log.md", leaderboard=logs / "leaderboard.md",
        frozen=root / "FROZEN_PARAMS.json", oos=results / "OOS_FINAL",
        data=Path(data) if data else root / "data" / "BTCUSDT_1h.csv",
    )


def run_name(nn: int) -> str:
    return f"run_{int(nn):02d}"


def read_jsonl(path: Path) -> list:
    path = Path(path)
    if not path.exists():
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(f"{path}: line {ln} is not valid JSON: {e}") from e
    return out


def count_lines(path: Path) -> int:
    path = Path(path)
    if not path.exists():
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def _num(x) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return -math.inf
    return v if not math.isnan(v) else -math.inf


def fmt(v) -> str:
    """Exact value rendering: floats use Python's shortest round-trip repr (no rounding)."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        if math.isnan(v):
            return "NaN"
        if math.isinf(v):
            return "inf" if v > 0 else "-inf"
        return repr(v)
    if v is None:
        return "null"
    return str(v)


def flatten(d: dict, prefix: str = ""):
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            yield from flatten(v, key + ".")
        else:
            yield key, v


# ---------------------------------------------------------------------------------------------------
# selection rule & DSR
# ---------------------------------------------------------------------------------------------------
def select_best(records: list):
    """Returns (record | None, status) per SPEC Section 8."""
    key = lambda r: (_num(r["metrics"].get("sharpe")), int(r["metrics"].get("trades", 0)))  # noqa: E731
    elig = [r for r in records if r.get("eligible")]
    if elig:
        return max(elig, key=key), "ELIGIBLE"
    fb = [r for r in records if int(r["metrics"].get("trades", 0)) >= 30]
    if fb:
        return max(fb, key=key), "FAILED PRE-REGISTERED GATES"
    return None, "NO QUALIFYING RUN"


def dsr_of_best(records: list):
    from engine.metrics import deflated_sharpe
    best, status = select_best(records)
    if best is None:
        return None
    m = best["metrics"]
    trials = [r["metrics"].get("sharpe_daily") for r in records]
    dsr, sr0, n, v = deflated_sharpe(m.get("sharpe_daily", math.nan), int(m.get("n_days", 0)),
                                     m.get("skew", math.nan), m.get("kurtosis", math.nan), trials,
                                     n_trials=len(records))
    return {"run_id": best["run_id"], "status": status, "dsr": dsr, "sr0_daily": sr0, "n_trials": n,
            "var_trial_sharpe_daily": v, "sharpe_daily": m.get("sharpe_daily"), "sharpe": m.get("sharpe"),
            "n_days": m.get("n_days")}


def improvement_tracker(records: list, min_step: float = 0.05):
    """(best eligible sharpe, run id that last raised it by >= min_step, runs since that run)."""
    best = -math.inf
    last = None
    for r in records:
        if not r.get("eligible"):
            continue
        s = _num(r["metrics"].get("sharpe"))
        if s == -math.inf:
            continue
        if best == -math.inf or s >= best + min_step:
            last = r["run_id"]
        best = max(best, s)
    since = (len(records) - last) if last is not None else len(records)
    return (best if best > -math.inf else math.nan), last, since


# ---------------------------------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------------------------------
def _params_diff_table(rec: dict) -> list:
    from engine.params import DEFAULTS
    diff = rec.get("params_diff_vs_defaults") or {}
    if not diff:
        return ["_none (Pine defaults)_", ""]
    lines = ["| parameter | value | Pine default |", "|---|---|---|"]
    for k in sorted(diff):
        lines.append(f"| `{k}` | `{fmt(diff[k])}` | `{fmt(DEFAULTS.get(k))}` |")
    lines.append("")
    return lines


def render(paths: SimpleNamespace | None = None) -> None:
    P = paths or get_paths()
    records = read_jsonl(P.jsonl)
    P.logs.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # ------------------------------------------------------------------ tuning_log.md
    L = ["# CRB Strategy - IS tuning log", "",
         f"Rendered {now} from `logs/tuning_log.jsonl` ({len(records)} / {MAX_RUNS} runs) and `critic/run_NN.md`.",
         "Do not edit by hand; run `python log_tools.py render`.", "",
         f"Pre-registered selection rule: {SELECTION_RULE}", ""]
    for rec in records:
        nn = rec["run_id"]
        m = rec.get("metrics", {})
        L += [f"## Run {nn:02d}", "",
              f"- run id: `{run_name(nn)}`",
              f"- timestamp (UTC): `{rec.get('utc_timestamp')}`",
              f"- config hash: `{rec.get('config_hash')}`",
              f"- eligible: **{'YES' if rec.get('eligible') else 'NO'}**",
              f"- runtime_s: `{fmt(rec.get('runtime_s'))}`",
              f"- data sha256: `{rec.get('data_sha256')}`", "",
              "### Params diff vs defaults", ""]
        L += _params_diff_table(rec)
        full = rec.get("params_full") or {}
        L += [f"<details><summary>Full parameter set ({len(full)} keys)</summary>", "", "```json",
              json.dumps(full, indent=1, sort_keys=True), "```", "", "</details>", "",
              "### Gates", "", "| gate | rule | value | pass |", "|---|---|---|---|"]
        for g, gd in (rec.get("gates") or {}).items():
            L.append(f"| {g} | {gd.get('rule')} | `{fmt(gd.get('value'))}` | {'PASS' if gd.get('pass') else 'FAIL'} |")
        L += ["", "### Metrics (exact)", "", "| metric | value |", "|---|---|"]
        for k, v in flatten({k: v for k, v in m.items() if k not in ("gates", "eligible")}):
            L.append(f"| `{k}` | `{fmt(v)}` |")
        L += ["", "### Critic verdict", ""]
        cf = P.critic / f"{run_name(nn)}.md"
        if cf.exists():
            L += [cf.read_text(encoding="utf-8").rstrip(), ""]
        else:
            L += ["_(no critic/%s.md yet)_" % run_name(nn), ""]
        L += ["---", ""]
    P.md.write_text("\n".join(L), encoding="utf-8")

    # ------------------------------------------------------------------ leaderboard.md
    best, status = select_best(records)
    B = ["# CRB Strategy - IS leaderboard", "",
         f"Rendered {now}. Runs used: {len(records)} / {MAX_RUNS}. Sorted by IS sharpe (daily, annualised sqrt(365)).",
         "", f"Pre-registered selection rule: {SELECTION_RULE}", ""]
    if best is None:
        B.append("**Current best (pre-registered rule):** none (no run qualifies yet)")
    else:
        d = dsr_of_best(records)
        bm = best["metrics"]
        flag = "" if status == "ELIGIBLE" else f" - **{status}**"
        B.append(f"**Current best (pre-registered rule):** Run {best['run_id']:02d} (`{best['config_hash']}`){flag} - "
                 f"sharpe {fmt(bm.get('sharpe'))}, trades {bm.get('trades')}, PF {fmt(bm.get('profit_factor'))}, "
                 f"net {fmt(bm.get('net_return_pct'))} %, max DD {fmt(bm.get('max_dd_pct'))} % ; "
                 f"PSR(0) {fmt(bm.get('psr0'))} ; DSR {fmt(d['dsr'])} "
                 f"(N={d['n_trials']} trials, V[SR_daily]={fmt(d['var_trial_sharpe_daily'])}, "
                 f"SR0_daily={fmt(d['sr0_daily'])}, SR*_daily={fmt(d['sharpe_daily'])}, T={d['n_days']})")
    be, last, since = improvement_tracker(records)
    B += ["", f"Best eligible sharpe: {fmt(be)} ; last run raising it by >= 0.05: "
              f"{('Run %02d' % last) if last else 'none'} ; runs since: {since}", ""]
    # best-so-far markers (who was the rule's best right after each run)
    best_so_far = set()
    for i in range(1, len(records) + 1):
        b, _ = select_best(records[:i])
        if b is not None and b["run_id"] == records[i - 1]["run_id"]:
            best_so_far.add(b["run_id"])
    B += ["| rank | run | hash | sharpe | sortino | net % | max DD % | trades | PF | win % | stress net % | B&H sharpe "
          "| G1 | G2 | G3 | G4 | eligible | best-so-far | current best |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    ranked = sorted(records, key=lambda r: (_num(r["metrics"].get("sharpe")), r["metrics"].get("trades", 0)),
                    reverse=True)
    for rank, r in enumerate(ranked, 1):
        m, g = r["metrics"], r.get("gates") or {}
        st = m.get("stress") or {}
        pf = lambda k: "PASS" if (g.get(k) or {}).get("pass") else "FAIL"  # noqa: E731
        B.append(
            f"| {rank} | {r['run_id']:02d} | `{r['config_hash']}` | {fmt(m.get('sharpe'))} | {fmt(m.get('sortino'))} "
            f"| {fmt(m.get('net_return_pct'))} | {fmt(m.get('max_dd_pct'))} | {m.get('trades')} "
            f"| {fmt(m.get('profit_factor'))} | {fmt(m.get('win_rate_pct'))} | {fmt(st.get('net_return_pct'))} "
            f"| {fmt((m.get('buy_and_hold') or {}).get('sharpe'))} | {pf('G1')} | {pf('G2')} | {pf('G3')} | {pf('G4')} "
            f"| {'YES' if r.get('eligible') else 'no'} | {'*' if r['run_id'] in best_so_far else ''} "
            f"| {'BEST' if best is not None and r['run_id'] == best['run_id'] else ''} |")
    B.append("")
    P.leaderboard.write_text("\n".join(B), encoding="utf-8")


# ---------------------------------------------------------------------------------------------------
# verify
# ---------------------------------------------------------------------------------------------------
def verify(paths: SimpleNamespace | None = None):
    """Returns (errors, warnings)."""
    from engine.params import config_hash, validate
    P = paths or get_paths()
    errors, warns = [], []
    try:
        records = read_jsonl(P.jsonl)
    except ValueError as e:
        return [str(e)], warns
    if len(records) > MAX_RUNS:
        errors.append(f"{len(records)} runs logged > cap {MAX_RUNS}")
    seen = {}
    for i, rec in enumerate(records, 1):
        nn = rec.get("run_id")
        tag = f"line {i} (run_id={nn})"
        if nn != i:
            errors.append(f"{tag}: run ids not contiguous (expected {i})")
        h = rec.get("config_hash")
        if h in seen:
            errors.append(f"{tag}: duplicate config hash {h} (also run {seen[h]})")
        seen[h] = nn
        try:
            if config_hash(validate(rec.get("params_full"))) != h:
                errors.append(f"{tag}: params_full does not hash to logged {h}")
        except ValueError as e:
            errors.append(f"{tag}: params_full invalid: {e}")
        if not isinstance(nn, int):
            continue
        cfg = P.configs / f"{run_name(nn)}.json"
        if not cfg.exists():
            errors.append(f"{tag}: missing config {cfg}")
        else:
            try:
                ch = config_hash(validate(json.loads(cfg.read_text(encoding="utf-8"))))
                if ch != h:
                    errors.append(f"{tag}: config file {cfg.name} merged hash {ch} != logged {h} (tampered?)")
            except (ValueError, json.JSONDecodeError) as e:
                errors.append(f"{tag}: config {cfg.name} invalid: {e}")
        rd = P.results / run_name(nn)
        for fn in ("metrics.json", "trades.csv", "equity_daily.csv"):
            if not (rd / fn).exists():
                errors.append(f"{tag}: missing results/{run_name(nn)}/{fn}")
        mf = rd / "metrics.json"
        if mf.exists():
            try:
                mj = json.loads(mf.read_text(encoding="utf-8"))
                for k in ("sharpe", "trades", "net_return_pct"):
                    a, b = mj.get(k), rec.get("metrics", {}).get(k)
                    if not (a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))):
                        errors.append(f"{tag}: metrics.json {k}={a} != log {b}")
            except json.JSONDecodeError as e:
                errors.append(f"{tag}: metrics.json unreadable: {e}")
    logged = {run_name(r.get("run_id", -1)) for r in records}
    if P.results.exists():
        for d in sorted(P.results.glob("run_*")):
            if d.is_dir() and d.name not in logged:
                warns.append(f"results/{d.name} exists but is not logged (crashed run?)")
    if P.frozen.exists():
        try:
            fz = json.loads(P.frozen.read_text(encoding="utf-8"))
            fh = config_hash(validate(fz.get("params_full")))
            if fh != fz.get("config_hash"):
                errors.append("FROZEN_PARAMS.json: params_full does not match embedded config_hash")
            if seen.get(fz.get("config_hash")) != fz.get("run_id"):
                errors.append("FROZEN_PARAMS.json: run_id/config_hash not found in the log")
        except (ValueError, json.JSONDecodeError) as e:
            errors.append(f"FROZEN_PARAMS.json invalid: {e}")
    return errors, warns


# ---------------------------------------------------------------------------------------------------
# freeze
# ---------------------------------------------------------------------------------------------------
def freeze(paths: SimpleNamespace | None = None) -> dict:
    from engine.params import config_hash, validate
    P = paths or get_paths()
    if P.frozen.exists():
        raise FileExistsError(f"{P.frozen} already exists; freeze is write-once")
    errors, _ = verify(P)
    if errors:
        raise RuntimeError("verify failed; refusing to freeze:\n  " + "\n  ".join(errors))
    records = read_jsonl(P.jsonl)
    best, status = select_best(records)
    if best is None:
        raise RuntimeError("no run qualifies under the pre-registered rule (incl. fallback)")
    full = validate(best["params_full"])
    h = config_hash(full)
    if h != best["config_hash"]:
        raise RuntimeError("best run params do not hash to its logged config_hash")
    doc = {
        "run_id": best["run_id"],
        "config_hash": h,
        "params_full": full,
        "frozen_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "selection_rule": SELECTION_RULE,
        "selection_status": status,
        "n_trials": len(records),
        "dsr": dsr_of_best(records),
        "is_metrics": best["metrics"],
    }
    with open(P.frozen, "x", encoding="utf-8") as f:     # exclusive create: never overwrites
        f.write(json.dumps(doc, indent=2, sort_keys=False))
    return doc


# ---------------------------------------------------------------------------------------------------
def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["render", "verify", "best", "freeze", "dsr"])
    a = ap.parse_args(argv)
    P = get_paths()
    if a.cmd == "render":
        render(P)
        print(f"rendered {P.md} and {P.leaderboard}")
        return 0
    if a.cmd == "verify":
        errors, warns = verify(P)
        for w in warns:
            print(f"WARNING: {w}")
        if errors:
            print("ERRORS:")
            for e in errors:
                print(f"  - {e}")
            return 1
        print(f"OK ({len(read_jsonl(P.jsonl))} runs logged, cap {MAX_RUNS})")
        return 0
    if a.cmd == "best":
        records = read_jsonl(P.jsonl)
        best, status = select_best(records)
        if best is None:
            print(status)
            return 1
        print(f"best: run {best['run_id']:02d} hash {best['config_hash']} status {status} "
              f"sharpe {fmt(best['metrics'].get('sharpe'))} trades {best['metrics'].get('trades')}")
        print("params_diff_vs_defaults:", json.dumps(best.get("params_diff_vs_defaults"), sort_keys=True))
        print("params_full:", json.dumps(best.get("params_full"), sort_keys=True))
        return 0
    if a.cmd == "dsr":
        d = dsr_of_best(read_jsonl(P.jsonl))
        print(json.dumps(d, indent=2) if d else "no qualifying run")
        return 0 if d else 1
    if a.cmd == "freeze":
        try:
            doc = freeze(P)
        except (FileExistsError, RuntimeError) as e:
            print(f"REFUSED: {e}", file=sys.stderr)
            return 2
        print(f"frozen run {doc['run_id']:02d} hash {doc['config_hash']} ({doc['selection_status']}) -> {P.frozen}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
