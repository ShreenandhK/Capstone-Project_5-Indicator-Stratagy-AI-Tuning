"""Post-hoc concentration diagnostics for logged IS runs (read-only; NOT part of the pre-registered selection rule).

usage: python diagnostics.py            -> table for every results/run_NN
       python diagnostics.py 06 07      -> only those runs
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def pf(pnl):
    gw, gl = pnl[pnl > 0].sum(), -pnl[pnl < 0].sum()
    return float("inf") if gl == 0 else gw / gl


def row(run_id):
    t = pd.read_csv(ROOT / "results" / f"run_{run_id}" / "trades.csv")
    p = t["pnl"].to_numpy(float)
    order = np.argsort(p)[::-1]
    ex2 = np.delete(p, order[:2])
    return {
        "run": run_id, "trades": len(p), "net_usd": p.sum(), "top2_usd": p[order[:2]].sum(),
        "net_ex_top2_usd": ex2.sum(), "pf": pf(p), "pf_ex_top2": pf(ex2),
        "median_ret_pct": float(np.median(t["return_pct"])), "pct_winners": float((p > 0).mean() * 100),
    }


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(d.name.split("_")[1] for d in (ROOT / "results").glob("run_*") if (d / "trades.csv").exists())
    df = pd.DataFrame([row(i) for i in ids])
    print(df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
