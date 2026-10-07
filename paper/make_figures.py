"""Regenerate the paper figures (PNG at 300 dpi + vector PDF) from the logged study.

Run from the bundle root:   python paper/make_figures.py
Inputs are read-only: backtest/logs, backtest/results.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BT = ROOT / "backtest"
OUT = ROOT / "paper" / "figures"

# Reference palette (light mode): surface, ink, chrome, categorical slots 1-2.
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE = "#2a78d6", "#eb6834"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"], "font.size": 9,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK2, "axes.titlecolor": INK,
    "axes.titlesize": 10, "axes.titleweight": "semibold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "legend.frameon": False, "legend.labelcolor": INK2,
    "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
})
LINE = dict(lw=1.6, marker="o", ms=5, mec=SURFACE, mew=1.2, zorder=3)
NOTE = dict(color=INK2, fontsize=8.5, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7))


def signed_pct(v: float) -> str:
    """Signed percentage with a true minus sign, matching matplotlib's axis tick labels."""
    return f"{v:+.2f} %".replace("-", "−")


def save(fig, name: str) -> None:
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def pf_ex_top2(run_dir: Path) -> float:
    pnl = sorted(pd.read_csv(run_dir / "trades.csv")["pnl"].tolist(), reverse=True)[2:]
    return sum(v for v in pnl if v > 0) / -sum(v for v in pnl if v < 0)


def cumulative_return_pct(run_dir: Path) -> pd.Series:
    d = pd.read_csv(run_dir / "equity_daily.csv")
    t = pd.to_datetime(d.iloc[:, 0], utc=True)
    col = "equity" if "equity" in d.columns else d.columns[1]
    start = json.loads((run_dir / "metrics.json").read_text(encoding="utf-8"))["start_equity"]
    return pd.Series((d[col].to_numpy() / start - 1.0) * 100.0, index=t)


def fig1_tuning_trajectory() -> None:
    runs = [json.loads(line) for line in open(BT / "logs" / "tuning_log.jsonl", encoding="utf-8")]
    ids = [r["run_id"] for r in runs]
    sharpe = [r["metrics"]["sharpe"] for r in runs]
    pfx = [pf_ex_top2(BT / "results" / f"run_{i:02d}") for i in ids]
    sel = ids.index(17)

    fig, (a, b) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True, gridspec_kw={"hspace": 0.38})
    a.axhline(0, color=AXIS, lw=0.8, zorder=1)
    a.plot(ids, sharpe, color=BLUE, **LINE)
    a.plot([17], [sharpe[sel]], "o", ms=8, color=ORANGE, mec=SURFACE, mew=1.5, zorder=4)
    a.annotate(f"Run 17, frozen (Sharpe {sharpe[sel]:.3f})", xy=(17, sharpe[sel]), xytext=(11.2, 0.62), **NOTE)
    a.annotate("Critic declares plateau", xy=(19, sharpe[-1]), xytext=(15.6, -0.95), **NOTE)
    a.set_ylim(-1.95, 0.85)
    a.set_title("a   In-sample Sharpe ratio by parameter set")
    a.set_ylabel("Sharpe ratio (annualised)")

    b.axhline(1.0, color=AXIS, lw=0.8, zorder=1)
    b.text(19.4, 1.0, "break-even", color=MUTED, fontsize=8, va="center")
    b.plot(ids, pfx, color=BLUE, **LINE)
    b.plot([17], [pfx[sel]], "o", ms=8, color=ORANGE, mec=SURFACE, mew=1.5, zorder=4)
    b.annotate(f"Run 17 ({pfx[sel]:.3f})", xy=(17, pfx[sel]), xytext=(13.2, 1.08), **NOTE)
    b.set_ylim(0.35, 1.15)
    b.set_title("b   Profit factor excluding the two largest winning trades")
    b.set_ylabel("Profit factor")
    b.set_xlabel("Parameter set (run number)")
    b.set_xticks(ids)
    b.set_xlim(0.5, 20.3)
    save(fig, "fig1_tuning_trajectory")


def fig2_equity_is_oos() -> None:
    is_r = cumulative_return_pct(BT / "results" / "run_17")
    oos_r = cumulative_return_pct(BT / "results" / "OOS_FINAL")
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.axhline(0, color=AXIS, lw=0.8, zorder=1)
    ax.plot(is_r.index, is_r.values, color=BLUE, lw=1.6, label="In-sample (2023-01 to 2025-06)", zorder=3)
    ax.plot(oos_r.index, oos_r.values, color=ORANGE, lw=1.6, label="Out-of-sample (2025-07 to 2026-09)", zorder=3)
    for s, color in ((is_r, BLUE), (oos_r, ORANGE)):
        ax.plot([s.index[-1]], [s.values[-1]], "o", ms=5, color=color, mec=SURFACE, mew=1.2, zorder=4)
        ax.annotate(signed_pct(s.values[-1]), xy=(s.index[-1], s.values[-1]), xytext=(5, 0),
                    textcoords="offset points", color=INK2, fontsize=8.5, va="center")
    ax.set_xlim(is_r.index[0] - pd.Timedelta(days=20), oos_r.index[-1] + pd.Timedelta(days=95))
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.35)
    split = pd.Timestamp("2025-07-01", tz="UTC")
    ax.axvline(split, color=AXIS, lw=0.8, zorder=1)
    ax.text(split + pd.Timedelta(days=10), hi + 0.3, "Out-of-sample begins", color=MUTED, fontsize=8, va="top", ha="left")
    ax.set_title("Frozen configuration (run 17): cumulative return, 10 % of equity per trade")
    ax.set_ylabel("Return on starting equity (%)")
    ax.legend(loc="lower left", fontsize=8.5)
    save(fig, "fig2_equity_is_oos")


def fig3_subperiod_returns() -> None:
    is_m = json.loads((BT / "results" / "run_17" / "metrics.json").read_text(encoding="utf-8"))["subperiods"]
    oos_m = json.loads((BT / "results" / "OOS_FINAL" / "metrics.json").read_text(encoding="utf-8"))["subperiods"]
    labels = {"2023": "2023", "2024": "2024", "2025H1": "2025 H1", "2025H2": "2025 H2", "2026YTD": "2026 YTD"}
    rows = [(labels[k], v["net_return_pct"], BLUE) for k, v in is_m.items()] + \
           [(labels[k], v["net_return_pct"], ORANGE) for k, v in oos_m.items()]
    x = list(range(len(rows)))
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.axhline(0, color=AXIS, lw=0.8, zorder=1)
    ax.bar(x, [r[1] for r in rows], width=0.5, color=[r[2] for r in rows], linewidth=0, zorder=3)
    ax.axvline(len(is_m) - 0.5, color=AXIS, lw=0.8, zorder=1)
    for xi, (_, val, _) in zip(x, rows):
        ax.annotate(signed_pct(val), xy=(xi, val), xytext=(0, 4 if val >= 0 else -4), textcoords="offset points",
                    ha="center", va="bottom" if val >= 0 else "top", color=INK2, fontsize=8.5)
    ax.set_xticks(x, [r[0] for r in rows])
    ax.grid(axis="x", visible=False)
    lo = min(r[1] for r in rows)
    hi = max(r[1] for r in rows)
    ax.set_ylim(lo - 0.6, hi + 0.6)
    ax.set_title("Net return by sub-period, frozen configuration (run 17)")
    ax.set_ylabel("Net return (%)")
    ax.legend(handles=[Patch(color=BLUE, label="In-sample"), Patch(color=ORANGE, label="Out-of-sample")],
              loc="upper right", fontsize=8.5)
    save(fig, "fig3_subperiod_returns")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fig1_tuning_trajectory()
    fig2_equity_is_oos()
    fig3_subperiod_returns()
    print(f"figures -> {OUT}")
