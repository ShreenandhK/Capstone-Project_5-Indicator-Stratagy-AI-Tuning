#!/usr/bin/env python
"""Multi-market 1D backtest of `Combined Role-Based Strategy.pine` AS IT IS NOW (current input defaults).

  run_multimarket.py [KEY ...]      KEY in BTCUSD_1D, NIFTY_1D, HDFCBANK_1D, RELIANCE_1D (default: all)

This is an evaluation, not a tuning study: parameters are read from the .pine file, checked against
engine bounds and FROZEN_PARAMS.json, and never changed. Nothing is written to ../logs, ../results or
../results/OOS_FINAL. Engine = the tested BTC 1H study engine (TradingView broker semantics, deviation D1:
causal rolling LC window), so the first tradable bar is bar index lcMaxBarsBack.

Outputs: multimarket/results/<KEY>/{metrics.json, trades.csv, trades_long_only.csv, equity_daily.csv}
         multimarket/results/summary.json
"""
from __future__ import annotations

import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BT = HERE.parent
if str(BT) not in sys.path:
    sys.path.insert(0, str(BT))

from engine import metrics as MX  # noqa: E402
from engine import params as PRM  # noqa: E402
from engine.broker import STRESS_COSTS, simulate  # noqa: E402
from engine.signals import compute_signals  # noqa: E402

PINE = BT.parent / "Combined Role-Based Strategy.pine"
FROZEN = BT / "FROZEN_PARAMS.json"
DATA = HERE / "data"
RESULTS = HERE / "results"

# mintick = TradingView symbol tick (only used for the 2-tick slippage; immaterial at these price levels)
MARKETS = {
    "BTCUSD_1D": {"label": "Bitcoin — BITSTAMP:BTCUSD 1D", "ann": 365, "mintick": 1.0,
                  "periods": {"Before BTC 1H study (window start → 2022-12-31)": (None, "2022-12-31"),
                              "Same dates as BTC 1H tuning IS (2023-01-01 → 2025-06-30)": ("2023-01-01", "2025-06-30"),
                              "Same dates as BTC 1H OOS (2025-07-01 → end)": ("2025-07-01", None)}},
    "NIFTY_1D": {"label": "NSE:NIFTY 1D", "ann": 252, "mintick": 0.05, "periods": {}},
    "HDFCBANK_1D": {"label": "NSE:HDFCBANK 1D", "ann": 252, "mintick": 0.05, "periods": {}},
    "RELIANCE_1D": {"label": "NSE:RELIANCE 1D", "ann": 252, "mintick": 0.05, "periods": {}},
}

_INPUT_RE = re.compile(r"^(\w+)\s*=\s*input\.(bool|int|float|string|source)\(\s*('[^']*'|[^,]+?)\s*,", re.M)


# ---------------------------------------------------------------------------------------------------
# parameters straight from the .pine file
# ---------------------------------------------------------------------------------------------------
def pine_params(pretuning: bool = False) -> tuple[dict, dict]:
    """Current .pine input defaults, or (pretuning) the original pre-study defaults = engine DEFAULTS = run 01."""
    text = PINE.read_text(encoding="utf-8")
    raw = {}
    for name, kind, lit in _INPUT_RE.findall(text):
        raw[name] = {"bool": lambda s: s == "true", "int": int, "float": float,
                     "string": lambda s: s.strip("'"), "source": str}[kind](lit.strip())
    missing = sorted(set(PRM.DEFAULTS) - set(raw))
    extra = sorted(set(raw) - set(PRM.DEFAULTS))
    if missing or extra:
        raise ValueError(f".pine inputs do not match engine parameters: missing {missing}, extra {extra}")
    current = PRM.validate(raw)
    full = PRM.validate({}) if pretuning else current
    hdr = re.search(r"strategy\((.*?)\)\s*\n\s*\nimport", text, re.S).group(1)
    props = {k: float(re.search(rf"{k}\s*=\s*([\d.]+)", hdr).group(1))
             for k in ("initial_capital", "default_qty_value", "commission_value", "slippage", "pyramiding")}
    expect = {"initial_capital": 10000.0, "default_qty_value": 10.0, "commission_value": 0.075, "slippage": 2.0,
              "pyramiding": 0.0}
    if props != expect or "process_orders_on_close = false" not in hdr:
        raise ValueError(f"strategy() properties changed: {props}; engine emulates {expect}")
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    diff = {k: (frozen["params_full"].get(k), v) for k, v in full.items() if frozen["params_full"].get(k) != v}
    return full, {"config_hash": PRM.config_hash(full), "strategy_props": props,
                  "matches_frozen_run": frozen["run_id"] if not diff else None, "diff_vs_frozen": diff,
                  "diff_vs_engine_defaults": PRM.diff_vs_defaults(full),
                  "variant": "pretuning" if pretuning else "current_pine",
                  "diff_vs_current_pine": {k: (v, current[k]) for k, v in full.items() if current[k] != v}}


def load(key: str) -> pd.DataFrame:
    raw = pd.read_csv(DATA / f"{key}.csv")
    idx = pd.DatetimeIndex(pd.to_datetime(raw["time"], utc=True), name="time")
    df = pd.DataFrame({c: raw[c].to_numpy(dtype=float) for c in ["open", "high", "low", "close", "volume"]}, index=idx)
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError(f"{key}: bar times must be strictly increasing")
    return df


# ---------------------------------------------------------------------------------------------------
# statistics
# ---------------------------------------------------------------------------------------------------
def _num(x):
    x = float(x)
    return None if math.isnan(x) else x


def side_stats(tr: pd.DataFrame) -> dict:
    """TradingView 'Performance Summary' style numbers for one trade subset."""
    pnl = tr["pnl"].to_numpy(dtype=float)
    ret = tr["return_pct"].to_numpy(dtype=float)
    win, loss = pnl > 0, pnl < 0
    n = len(tr)
    aw = pnl[win].mean() if win.any() else math.nan
    al = pnl[loss].mean() if loss.any() else math.nan
    return {
        "trades": n,
        "net_profit": float(pnl.sum()),
        "gross_profit": float(pnl[win].sum()),
        "gross_loss": float(-pnl[loss].sum()),
        "profit_factor": MX.profit_factor(pnl),
        "percent_profitable": float(win.mean() * 100) if n else math.nan,
        "winning_trades": int(win.sum()),
        "losing_trades": int(loss.sum()),
        "avg_trade": float(pnl.mean()) if n else math.nan,
        "avg_trade_pct": float(ret.mean()) if n else math.nan,
        "median_trade_pct": float(np.median(ret)) if n else math.nan,
        "avg_win": float(aw),
        "avg_loss": float(al),
        "ratio_avg_win_avg_loss": float(aw / abs(al)) if n and win.any() and loss.any() else math.nan,
        "largest_win": float(pnl.max()) if win.any() else math.nan,
        "largest_loss": float(pnl.min()) if loss.any() else math.nan,
        "avg_bars_in_trade": float(tr["bars_held"].mean()) if n else math.nan,
        "commission_paid": float((tr["entry_commission"] + tr["exit_commission"]).sum()),
    }


def equity_block(eq: pd.Series, start: float, ann: int) -> dict:
    r = MX.daily_returns(eq, start).to_numpy()
    v = eq.to_numpy(dtype=float)
    peak = np.maximum.accumulate(np.concatenate([[start], v]))[1:]
    mdd_pct, mdd_days = MX.max_drawdown(pd.concat([pd.Series([start], index=[eq.index[0] - pd.Timedelta(days=1)]), eq]))
    span = (eq.index[-1] - eq.index[0]).total_seconds() / 86400.0 + 1.0
    g = v[-1] / start
    sk, ku = MX.moments(r)
    srd = MX.sharpe(r, 1.0)
    return {
        "final_equity": float(v[-1]),
        "net_profit": float(v[-1] - start),
        "net_return_pct": float((g - 1) * 100),
        "cagr_pct": float((g ** (365.25 / span) - 1) * 100) if g > 0 else math.nan,
        "ann_vol_pct": float(r.std(ddof=1) * math.sqrt(ann) * 100),
        "sharpe": MX.sharpe(r, ann),
        "sortino": MX.sortino(r, ann),
        "max_drawdown": float((peak - v).max()),
        "max_drawdown_pct": float(mdd_pct),
        "max_drawdown_duration_days": float(mdd_days),
        "psr_sharpe_gt_0": MX.psr(srd, len(r), sk, ku),
        "n_days": int(len(r)),
        "annualisation_periods": ann,
    }


def period_stats(eq: pd.Series, bh: pd.Series, tr: pd.DataFrame, start: float, s, e, ann: int) -> dict:
    m = np.ones(len(eq), dtype=bool)
    if s is not None:
        m &= eq.index >= pd.Timestamp(s, tz="UTC")
    if e is not None:
        m &= eq.index <= pd.Timestamp(e, tz="UTC") + pd.Timedelta(hours=23, minutes=59)
    idx = np.flatnonzero(m)
    if idx.size == 0:
        return {}
    v, b = eq.to_numpy(float), bh.to_numpy(float)
    before = v[idx[0] - 1] if idx[0] > 0 else start
    bbefore = b[idx[0] - 1] if idx[0] > 0 else start
    r = MX.daily_returns(eq, start)
    rm = r.to_numpy()[np.asarray((r.index >= eq.index[idx[0]].floor("D")) & (r.index <= eq.index[idx[-1]].floor("D")))]
    et = tr["entry_time"]
    sel = (et >= eq.index[idx[0]]) & (et <= eq.index[idx[-1]])
    pnl = tr.loc[sel, "pnl"].to_numpy(float)
    return {
        "from": str(eq.index[idx[0]].date()), "to": str(eq.index[idx[-1]].date()),
        "net_return_pct": float((v[idx[-1]] / before - 1) * 100),
        "buy_and_hold_pct": float((b[idx[-1]] / bbefore - 1) * 100),
        "sharpe": MX.sharpe(rm, ann),
        "trades": int(sel.sum()),
        "profit_factor": MX.profit_factor(pnl),
        "percent_profitable": float((pnl > 0).mean() * 100) if pnl.size else math.nan,
    }


def funnel(sig: pd.DataFrame, win: np.ndarray) -> dict:
    """How many LC entry-window bars survive each additional role gate (window bars only)."""
    out = {}
    for side in ("long", "short"):
        cur = sig[f"entry_{side}"].to_numpy(bool) & win
        steps = {"LC entry window (fresh flip)": int(cur.sum())}
        for label, col in (("+ SQZ regime gate", "regime_gate"), (f"+ NW trend", f"trend_{side}"),
                           ("+ WT timing", f"timing_{side}"), ("+ WWV confirmation", f"confirm_{side}")):
            cur = cur & sig[col].to_numpy(bool)
            steps[label] = int(cur.sum())
        steps["= entry condition bars"] = int((sig[f"{side}_cond"].to_numpy(bool) & win).sum())
        out[side] = steps
    out["lc_flips_long"] = int((sig["lc_new_buy"].to_numpy(bool) & win).sum())
    out["lc_flips_short"] = int((sig["lc_new_sell"].to_numpy(bool) & win).sum())
    return out


def run_market(key: str, full: dict, pinfo: dict) -> dict:
    cfg = MARKETS[key]
    ann = cfg["ann"]
    t0 = time.perf_counter()
    df = load(key)
    M = full["lcMaxBarsBack"]
    if len(df) <= M + 250:
        raise ValueError(f"{key}: {len(df)} bars, need > {M + 250} (LC warm-up {M})")
    ws, we = df.index[M], df.index[-1]
    base_costs = {"commission_pct": 0.075, "slip_mode": "ticks", "slip_value": 2, "mintick": cfg["mintick"]}

    sig = compute_signals(df, full)
    base = simulate(df, sig, full, ws, we, base_costs)
    stress = simulate(df, sig, full, ws, we, STRESS_COSTS)
    lo_params = PRM.validate({**full, "allowShorts": False})
    sig_lo = compute_signals(df, lo_params)
    long_only = simulate(df, sig_lo, lo_params, ws, we, base_costs)

    tr, eq, info = base
    start = float(info["initial_capital"])
    bh_meta, bh = MX.buy_and_hold(df, eq.index, start)
    win = np.asarray((df.index >= ws) & (df.index <= we))

    def block(sim):
        t, e, i = sim
        return {**equity_block(e, start, ann), "trades": len(t), "exposure_pct": i["exposure_pct"],
                "all": side_stats(t), "long": side_stats(t[t["direction"] == "long"]),
                "short": side_stats(t[t["direction"] == "short"]),
                "exit_reasons": {k: int(v) for k, v in t["exit_reason"].value_counts().items()},
                "trade_tstat": MX.trade_stats(t)["trade_tstat"] if len(t) else math.nan,
                "win_rate_ci95_pct": [MX.trade_stats(t)["win_rate_ci95_low_pct"],
                                      MX.trade_stats(t)["win_rate_ci95_high_pct"]] if len(t) else None,
                "costs": i["costs"]}

    years = {str(y): (f"{y}-01-01", f"{y}-12-31") for y in range(ws.year, we.year + 1)}
    res = {
        "market": key, "label": cfg["label"], "timeframe": "1D",
        "data": json.loads((DATA / f"{key}.meta.json").read_text(encoding="utf-8")),
        "bars_total": len(df), "warmup_bars": M, "window_start": str(ws.date()), "window_end": str(we.date()),
        "window_bars": int(win.sum()),
        "params": pinfo,
        "base": block(base), "stress": block(stress), "long_only": block(long_only),
        "buy_and_hold": {**equity_block(bh, start, ann)},
        "years": {y: period_stats(eq, bh, tr, start, s, e, ann) for y, (s, e) in years.items()},
        "periods": {name: period_stats(eq, bh, tr, start, s, e, ann) for name, (s, e) in cfg["periods"].items()},
        "funnel": funnel(sig, win),
        "runtime_s": time.perf_counter() - t0,
    }

    out = RESULTS / key
    out.mkdir(parents=True, exist_ok=True)
    for name, t in (("trades.csv", tr), ("trades_long_only.csv", long_only[0])):
        t = t.copy()
        for c in ("entry_time", "exit_time"):
            t[c] = t[c].dt.strftime("%Y-%m-%d")
        t.to_csv(out / name, index=False, float_format="%.10g")
    daily = pd.DataFrame({"equity": MX.daily_equity(eq), "equity_stress": MX.daily_equity(stress[1]),
                          "equity_long_only": MX.daily_equity(long_only[1]), "buy_and_hold": MX.daily_equity(bh)})
    daily.index = daily.index.strftime("%Y-%m-%d")
    daily.index.name = "date"
    daily.to_csv(out / "equity_daily.csv", float_format="%.10g")
    (out / "metrics.json").write_text(json.dumps(res, indent=2, default=_json), encoding="utf-8")
    return res


def _json(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if math.isnan(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o).__name__)


def _f(x, nd=2):
    return "n/a" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x:,.{nd}f}"


def main(argv: list[str]) -> int:
    global RESULTS
    pretuning = "--pretuning" in argv
    keys = [a for a in argv if not a.startswith("--")] or list(MARKETS)
    if pretuning:
        RESULTS = HERE / "results_pretuning"
    full, pinfo = pine_params(pretuning)
    print(f"variant {pinfo['variant']} | params hash {pinfo['config_hash']} | matches frozen run "
          f"{pinfo['matches_frozen_run']} | diff vs current .pine {pinfo['diff_vs_current_pine']}")
    summary = {}
    for key in keys:
        r = run_market(key, full, pinfo)
        b, s, lo, bh = r["base"], r["stress"], r["long_only"], r["buy_and_hold"]
        print(f"\n{r['label']}: window {r['window_start']} -> {r['window_end']} ({r['window_bars']} bars, "
              f"{r['bars_total']} total) runtime {r['runtime_s']:.1f}s")
        print(f"  base   : net {_f(b['net_return_pct'])}% | CAGR {_f(b['cagr_pct'])}% | maxDD {_f(b['max_drawdown_pct'])}% "
              f"| sharpe {_f(b['sharpe'])} | PF {_f(b['all']['profit_factor'])} | trades {b['trades']} "
              f"(L {b['long']['trades']} / S {b['short']['trades']}) | win {_f(b['all']['percent_profitable'])}% "
              f"| t {_f(b['trade_tstat'])} | exposure {_f(b['exposure_pct'])}%")
        print(f"  stress : net {_f(s['net_return_pct'])}% | sharpe {_f(s['sharpe'])} | PF {_f(s['all']['profit_factor'])}")
        print(f"  longonly: net {_f(lo['net_return_pct'])}% | sharpe {_f(lo['sharpe'])} | PF {_f(lo['all']['profit_factor'])} "
              f"| trades {lo['trades']}")
        print(f"  B&H    : net {_f(bh['net_return_pct'])}% | CAGR {_f(bh['cagr_pct'])}% | maxDD {_f(bh['max_drawdown_pct'])}% "
              f"| sharpe {_f(bh['sharpe'])}")
        print(f"  long  PF {_f(b['long']['profit_factor'])} net {_f(b['long']['net_profit'])} | short PF "
              f"{_f(b['short']['profit_factor'])} net {_f(b['short']['net_profit'])} | exits {b['exit_reasons']}")
        print("  years  : " + " | ".join(f"{y} {_f(v.get('net_return_pct'))}%/{v.get('trades')}t"
                                         for y, v in r["years"].items()))
        for name, v in r["periods"].items():
            print(f"  period : {name}: net {_f(v.get('net_return_pct'))}% PF {_f(v.get('profit_factor'))} "
                  f"trades {v.get('trades')} sharpe {_f(v.get('sharpe'))}")
        print(f"  funnel : {r['funnel']}")
        summary[key] = r
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, default=_json), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
