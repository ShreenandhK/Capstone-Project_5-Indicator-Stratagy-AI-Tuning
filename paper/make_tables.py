"""Regenerate the paper tables (CSV + Markdown) and the pre-tuning baseline .pine from the logged study.

Run from the bundle root:   python paper/make_tables.py
Inputs are read-only: backtest/logs, backtest/results, backtest/critic, backtest/FROZEN_PARAMS.json.
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BT = ROOT / "backtest"
OUT = ROOT / "paper" / "tables"
sys.path.insert(0, str(BT))
from engine import params as P  # noqa: E402

ROLES = [("allow", "Strategy controls"), ("nw", "Trend - Nadaraya-Watson"),
         ("lc", "Entry - Lorentzian Classification"), ("wt", "Timing - WaveTrend"),
         ("wwv", "Confirmation - Weis Wave Volume"), ("sqz", "Regime gate - Squeeze Momentum"),
         ("exit", "Exits & risk"), ("risk", "Exits & risk")]
INPUT_RE = re.compile(r"^(\s*(\w+)\s*=\s*input\.(bool|int|float|string|source)\(\s*)('[^']*'|[^,\s)]+)", re.M)


def role(key: str) -> str:
    return next(r for p, r in ROLES if key.startswith(p))


def r4(x):
    if isinstance(x, float):
        return "inf" if math.isinf(x) else round(x, 4)
    return x


def profit_factor(pnl) -> float:
    gw = sum(v for v in pnl if v > 0)
    gl = -sum(v for v in pnl if v < 0)
    return math.inf if gl == 0 else gw / gl


def concentration(run_dir: Path) -> dict:
    t = pd.read_csv(run_dir / "trades.csv")
    pnl = sorted(t["pnl"].tolist(), reverse=True)
    ex = pnl[2:]
    return {"pf_ex_top2": profit_factor(ex), "net_ex_top2_usd": sum(ex),
            "median_trade_return_pct": float(t["return_pct"].median())}


def write_csv(name: str, rows: list[dict]) -> None:
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow({k: r4(v) for k, v in row.items()})


def md_table(rows: list[dict], cols: list[str]) -> str:
    def cell(v):
        v = r4(v)
        return f"{v:.4f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return head + "".join("| " + " | ".join(cell(r[c]) for c in cols) + " |\n" for r in rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    frozen_doc = json.loads((BT / "FROZEN_PARAMS.json").read_text(encoding="utf-8"))
    frozen = frozen_doc["params_full"]
    runs = [json.loads(line) for line in open(BT / "logs" / "tuning_log.jsonl", encoding="utf-8")]

    # Table 1 - every in-sample parameter set
    t1 = []
    for r in runs:
        m, g = r["metrics"], r["gates"]
        rid = r["run_id"]
        verdicts = re.findall(r"VERDICT:\s*(\w+)", (BT / "critic" / f"run_{rid:02d}.md").read_text(encoding="utf-8"))
        conc = concentration(BT / "results" / f"run_{rid:02d}")
        t1.append({
            "run": rid, "config_hash": r["config_hash"],
            "changed_vs_pine_defaults": "; ".join(f"{k}={v}" for k, v in r["params_diff_vs_defaults"].items()) or "(Pine defaults)",
            "sharpe": m["sharpe"], "sortino": m["sortino"], "net_return_pct": m["net_return_pct"], "cagr_pct": m["cagr_pct"],
            "max_dd_pct": m["max_dd_pct"], "max_dd_duration_days": m["max_dd_duration_days"], "calmar": m["calmar"],
            "trades": m["trades"], "win_rate_pct": m["win_rate_pct"], "profit_factor": m["profit_factor"],
            "payoff_ratio": m["payoff_ratio"], "trade_tstat": m["trade_tstat"], "psr0": m["psr0"],
            "pf_ex_top2": conc["pf_ex_top2"], "net_ex_top2_usd": conc["net_ex_top2_usd"],
            "median_trade_return_pct": conc["median_trade_return_pct"],
            "stress_net_return_pct": m["stress"]["net_return_pct"], "stress_sharpe": m["stress"]["sharpe"],
            **{k: ("pass" if g[k]["pass"] else "fail") for k in ("G1", "G2", "G3", "G4")},
            "eligible": r["eligible"], "critic_verdict": verdicts[-1] if verdicts else "",
        })
    write_csv("table1_tuning_runs", t1)

    # Table 2 - frozen configuration, in-sample vs out-of-sample
    is_m = json.loads((BT / "results" / "run_17" / "metrics.json").read_text(encoding="utf-8"))
    oos_m = json.loads((BT / "results" / "OOS_FINAL" / "metrics.json").read_text(encoding="utf-8"))
    is_c, oos_c = concentration(BT / "results" / "run_17"), concentration(BT / "results" / "OOS_FINAL")
    metric_keys = ["sharpe", "sortino", "net_return_pct", "cagr_pct", "ann_vol_pct", "max_dd_pct", "max_dd_duration_days",
                   "calmar", "trades", "win_rate_pct", "profit_factor", "payoff_ratio", "avg_trade_return_pct",
                   "median_trade_return_pct", "trade_tstat", "psr0", "exposure_pct", "long_trades", "long_profit_factor",
                   "short_trades", "short_profit_factor", "max_consecutive_losses", "skew", "kurtosis"]
    t2 = [{"metric": k, "in_sample_run17": is_m[k], "out_of_sample": oos_m[k]} for k in metric_keys]
    t2 += [{"metric": "pf_ex_top2", "in_sample_run17": is_c["pf_ex_top2"], "out_of_sample": oos_c["pf_ex_top2"]},
           {"metric": "net_ex_top2_usd", "in_sample_run17": is_c["net_ex_top2_usd"], "out_of_sample": oos_c["net_ex_top2_usd"]}]
    for block, keys in (("stress", ["net_return_pct", "sharpe", "profit_factor", "max_dd_pct"]),
                        ("buy_and_hold", ["net_return_pct", "sharpe", "max_dd_pct"])):
        t2 += [{"metric": f"{block}.{k}", "in_sample_run17": is_m[block][k], "out_of_sample": oos_m[block][k]} for k in keys]
    t2 += [{"metric": "window", "in_sample_run17": f"{is_m['window_start']} -> {is_m['window_end']}",
            "out_of_sample": f"{oos_m['window_start']} -> {oos_m['window_end']}"},
           {"metric": "window_bars", "in_sample_run17": is_m["window_bars"], "out_of_sample": oos_m["window_bars"]}]
    write_csv("table2_is_vs_oos", t2)

    # Table 3 - sub-periods
    t3 = [{"period": k, "sample": "in-sample", **v} for k, v in is_m["subperiods"].items()]
    t3 += [{"period": k, "sample": "out-of-sample", **v} for k, v in oos_m["subperiods"].items()]
    write_csv("table3_subperiods", t3)

    # Table 4 - parameters: Pine baseline vs frozen
    t4 = [{"parameter": k, "role": role(k), "pine_baseline_default": P.DEFAULTS[k], "frozen_run17": frozen[k],
           "changed": P.DEFAULTS[k] != frozen[k], "tunable": k in P.BOUNDS} for k in P.DEFAULTS]
    write_csv("table4_parameters_baseline_vs_frozen", t4)

    # Table 5 - selection and multiple-testing
    d = frozen_doc["dsr"]
    t5 = [{"item": "selected_run", "value": frozen_doc["run_id"]}, {"item": "config_hash", "value": frozen_doc["config_hash"]},
          {"item": "selection_status", "value": frozen_doc["selection_status"]}, {"item": "selection_rule", "value": frozen_doc["selection_rule"]},
          {"item": "n_trials", "value": d["n_trials"]}, {"item": "is_sharpe_annualised", "value": d["sharpe"]},
          {"item": "is_sharpe_daily", "value": d["sharpe_daily"]}, {"item": "var_trial_sharpe_daily", "value": d["var_trial_sharpe_daily"]},
          {"item": "expected_max_sharpe_daily_sr0", "value": d["sr0_daily"]}, {"item": "deflated_sharpe_ratio", "value": d["dsr"]},
          {"item": "n_days", "value": d["n_days"]}, {"item": "frozen_utc", "value": frozen_doc["frozen_utc"]}]
    write_csv("table5_selection_and_dsr", t5)

    changed = [r for r in t4 if r["changed"]]
    md = ["# Paper tables (generated by paper/make_tables.py)\n",
          "## Table 1 - In-sample parameter sets (2023-01-01 to 2025-06-30)\n",
          md_table(t1, ["run", "changed_vs_pine_defaults", "sharpe", "net_return_pct", "max_dd_pct", "trades", "profit_factor",
                        "pf_ex_top2", "stress_net_return_pct", "G1", "G2", "G3", "G4", "critic_verdict"]),
          "\n## Table 2 - Frozen configuration (run 17): in-sample vs out-of-sample\n",
          md_table(t2, ["metric", "in_sample_run17", "out_of_sample"]),
          "\n## Table 3 - Sub-periods\n", md_table(t3, ["period", "sample", "net_return_pct", "sharpe", "trades", "profit_factor"]),
          "\n## Table 4 - Parameters changed from the Pine baseline\n",
          md_table(changed, ["parameter", "role", "pine_baseline_default", "frozen_run17"]),
          "\n## Table 5 - Selection and deflated Sharpe ratio\n", md_table(t5, ["item", "value"])]
    (OUT / "tables.md").write_text("\n".join(md), encoding="utf-8")


def write_baseline_pine() -> Path:
    """Rebuild the pre-tuning strategy (Pine input defaults = engine DEFAULTS) from the frozen .pine, and verify it."""
    frozen = json.loads((BT / "FROZEN_PARAMS.json").read_text(encoding="utf-8"))["params_full"]
    src = (ROOT / "Combined Role-Based Strategy.pine").read_text(encoding="utf-8")

    def literal(kind, v):
        return {"bool": lambda: "true" if v else "false", "string": lambda: f"'{v}'",
                "int": lambda: str(int(v)), "float": lambda: repr(float(v))}.get(kind, lambda: str(v))()

    def swap(m):
        name, kind = m.group(2), m.group(3)
        if name in P.DEFAULTS and P.DEFAULTS[name] != frozen[name]:
            return m.group(1) + literal(kind, P.DEFAULTS[name])
        return m.group(0)

    out = INPUT_RE.sub(swap, src)
    parsed = {}
    for _, name, kind, raw in INPUT_RE.findall(out):
        parsed[name] = {"bool": lambda: raw == "true", "int": lambda: int(raw), "float": lambda: float(raw),
                        "string": lambda: raw.strip("'")}.get(kind, lambda: raw)()
    bad = {k: (parsed.get(k), v) for k, v in P.DEFAULTS.items() if parsed.get(k) != v}
    if bad or set(parsed) != set(P.DEFAULTS):
        raise SystemExit(f"baseline reconstruction mismatch: {bad}")
    path = ROOT / "paper" / "Combined Role-Based Strategy.baseline.pine"
    path.write_text(out, encoding="utf-8")
    return path


if __name__ == "__main__":
    main()
    p = write_baseline_pine()
    print(f"tables -> {OUT}")
    print(f"baseline pine -> {p} (all {len(P.DEFAULTS)} inputs verified equal to engine DEFAULTS)")
