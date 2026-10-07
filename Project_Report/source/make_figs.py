import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd

BT = Path(r"C:/Course-Work/CIP-Project/backtest")
OUT = Path(__file__).parent / "figs"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#dddddd",
    "grid.linewidth": 0.6,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})
BLUE, GREEN, RED, GREY, AMBER = "#2962FF", "#089981", "#D93A3A", "#8a8f99", "#E69500"


def save(fig, name):
    fig.savefig(OUT / name)
    plt.close(fig)


# ---------------- Figure 1.1: BTC price with periods ----------------
df = pd.read_csv(BT / "data/BTCUSDT_1h.csv", parse_dates=["time"])
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.plot(df["time"], df["close"], color="#333333", lw=0.6)
spans = [("2022-01-01", "2023-01-01", "#eeeeee", "Warm-up (2022)"),
         ("2023-01-01", "2025-07-01", "#dbe7ff", "In-sample: tuning (Jan 2023 - Jun 2025)"),
         ("2025-07-01", "2026-09-14", "#ffe1dc", "Out-of-sample: locked (Jul 2025 - Sep 2026)")]
for a, b, c, lab in spans:
    ax.axvspan(pd.Timestamp(a, tz="UTC"), pd.Timestamp(b, tz="UTC"), color=c, label=lab, zorder=0)
ax.set_ylabel("BTC/USDT close (USD)")
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
ax.legend(loc="upper left", fontsize=9, frameon=False)
ax.grid(axis="x", visible=False)
save(fig, "fig_1_1_btc_periods.png")


# ---------------- helpers for box diagrams ----------------
def box(ax, x, y, w, h, title, body, edge=BLUE, fill="#f3f6ff", tsize=10, bsize=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                ec=edge, fc=fill, lw=1.3))
    ax.text(x + w / 2, y + h - 0.16, title, ha="center", va="top", fontsize=tsize, weight="bold")
    ax.text(x + w / 2, y + h - 0.48, body, ha="center", va="top", fontsize=bsize, linespacing=1.25)


def arrow(ax, p, q, color="#444444", style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=14, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}"))


# ---------------- Figure 3.1: system architecture ----------------
fig, ax = plt.subplots(figsize=(8, 3.0))
ax.set_xlim(0, 10.2); ax.set_ylim(0, 3.5); ax.axis("off")
w, h, y = 1.85, 1.35, 2.05
items = [("Data", "Binance BTC/USDT\n41,199 hourly bars\nSHA-256 hashed"),
         ("Signal engine", "5 indicators ported\nfrom Pine Script\nKNN in Numba"),
         ("Broker emulator", "TradingView fill rules\nnext-bar open fills\nfees + slippage"),
         ("Metrics", "Sharpe, Sortino, DD\nPSR, DSR, gates\nstress costs"),
         ("Audit log", "append-only JSONL\nconfig hashes\nverify command")]
xs = [0.1 + i * 2.05 for i in range(5)]
for x, (t, b) in zip(xs, items):
    box(ax, x, y, w, h, t, b, bsize=8.3)
for i in range(4):
    arrow(ax, (xs[i] + w, y + h / 2), (xs[i + 1], y + h / 2))
box(ax, 0.1, 0.1, 3.85, 1.15, "Pine Script v6 strategy (TradingView)",
    "518 lines, 72 inputs, signals on closed bars\nfrozen parameters copied back after the study",
    edge=GREEN, fill="#eefaf6")
box(ax, 4.2, 0.1, 5.85, 1.15, "Multi-agent tuning loop (Claude Code)",
    "Tuner -> Executor -> Adversarial critic -> Tracker\n25-run budget, pre-registered gates, OOS opened once",
    edge=RED, fill="#fff1ef")
arrow(ax, (2.0, 1.25), (2.0, y), style="<|-|>")
arrow(ax, (7.1, 1.25), (7.1, y), style="<|-|>")
save(fig, "fig_3_1_architecture.png")


# ---------------- Figure 3.2: five-role decision pipeline ----------------
fig, ax = plt.subplots(figsize=(8, 2.2))
ax.set_xlim(0, 12.3); ax.set_ylim(0, 2.5); ax.axis("off")
roles = [("1. Entry", "Lorentzian\nClassification\n(KNN)"),
         ("2. Regime", "Squeeze\nMomentum"),
         ("3. Trend", "Nadaraya-\nWatson kernel\nregression"),
         ("4. Timing", "WaveTrend\noscillator"),
         ("5. Confirm", "Weis Wave\nVolume")]
w, h, y = 1.5, 1.45, 0.8
xs = [0.05 + i * 2.05 for i in range(5)]
for x, (t, b) in zip(xs, roles):
    box(ax, x, y, w, h, t, b, bsize=8.8)
for i in range(4):
    ax.text(xs[i] + w + 0.275, y + h / 2, "AND", ha="center", va="center", fontsize=7.5, weight="bold", color=BLUE)
xt = xs[-1] + w + 0.45
arrow(ax, (xs[-1] + w, y + h / 2), (xt, y + h / 2))
box(ax, xt, y, 1.5, h, "Trade", "SL 2 x ATR\nTP 3 x ATR\n12-bar hold", edge=GREEN, fill="#eefaf6", bsize=8.8)
ax.text(5.95, 0.3, "A long (short) order is queued only when all five long (short) conditions are true on a closed candle.",
        ha="center", fontsize=9, style="italic")
save(fig, "fig_3_2_pipeline.png")


# ---------------- Figure 3.3: tuning loop ----------------
fig, ax = plt.subplots(figsize=(6.6, 3.6))
ax.set_xlim(0, 8); ax.set_ylim(0, 4.9); ax.axis("off")
nodes = {
    "Tuner": (0.3, 3.3, "proposes ONE config per run\nnever sees price data"),
    "Executor": (4.4, 3.3, "runs run_backtest.py is\nslot counted, results hashed"),
    "Adversarial critic": (4.4, 0.4, "assumes overfitting\nscorecard + demands\nCONTINUE / PLATEAU"),
    "Tracker": (0.3, 0.4, "saves verdict verbatim\nrenders + verifies logs"),
}
for k, (x, y, b) in nodes.items():
    red = k.startswith("Adversarial")
    box(ax, x, y, 3.3, 1.35, k, b, edge=RED if red else BLUE, fill="#fff1ef" if red else "#f3f6ff", bsize=9)
arrow(ax, (3.6, 3.97), (4.4, 3.97))
arrow(ax, (6.05, 3.3), (6.05, 1.75))
arrow(ax, (4.4, 1.07), (3.6, 1.07))
arrow(ax, (1.95, 1.75), (1.95, 3.3))
ax.text(4.0, 2.52, "hard cap: 25 runs\nstop on PLATEAU\nthen freeze -> OOS once", ha="center", va="center",
        fontsize=9, style="italic", color="#444444")
save(fig, "fig_3_3_tuning_loop.png")


# ---------------- Figure 4.1: Sharpe per run ----------------
runs = [json.loads(l) for l in open(BT / "logs/tuning_log.jsonl")]
ids = [r["run_id"] for r in runs]
sh = [r["metrics"]["sharpe"] for r in runs]
fig, ax = plt.subplots(figsize=(7.5, 3.2))
cols = [AMBER if i == 17 else (RED if s < 0 else "#7d8aa6") for i, s in zip(ids, sh)]
ax.bar(ids, sh, color=cols, width=0.7)
ax.axhline(0, color="#333333", lw=0.8)
ax.set_xticks(ids)
ax.set_xlabel("Tuning run")
ax.set_ylabel("In-sample Sharpe ratio")
ax.annotate("Run 17 (selected)\nSharpe 0.355", xy=(17, sh[16]), xytext=(13.2, 0.75), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#333333"))
ax.annotate("Run 1 (Pine defaults)\nSharpe -1.708", xy=(1, sh[0]), xytext=(2.3, -1.55), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="#333333"))
ax.set_ylim(-1.95, 1.1)
ax.grid(axis="x", visible=False)
save(fig, "fig_4_1_sharpe_runs.png")


# ---------------- Figure 4.2: IS equity before/after ----------------
e1 = pd.read_csv(BT / "results/run_01/equity_daily.csv", parse_dates=["date"])
e17 = pd.read_csv(BT / "results/run_17/equity_daily.csv", parse_dates=["date"])
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.plot(e1["date"], e1["equity"], color=RED, lw=1.3, label="Run 1: Pine defaults (ends $9,649)")
ax.plot(e17["date"], e17["equity"], color=GREEN, lw=1.3, label="Run 17: tuned (ends $10,112)")
ax.axhline(10000, color="#999999", lw=0.8, ls="--")
ax.set_ylabel("Account value (USD)")
ax.legend(loc="lower left", fontsize=9, frameon=False)
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
save(fig, "fig_4_2_is_equity.png")


# ---------------- Figure 4.3: OOS equity vs buy and hold ----------------
eo = pd.read_csv(BT / "results/OOS_FINAL/equity_daily.csv", parse_dates=["date"])
fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.plot(eo["date"], eo["buy_and_hold"], color=RED, lw=1.3, label="BTC buy-and-hold (ends $7,199, -28.0%)")
ax.plot(eo["date"], eo["equity"], color=GREEN, lw=1.5, label="CRB strategy, run 17 frozen (ends $9,688, -3.1%)")
ax.plot(eo["date"], eo["equity_stress"], color=GREEN, lw=1.0, ls=":", label="CRB strategy, stress costs (-4.8%)")
ax.axhline(10000, color="#999999", lw=0.8, ls="--")
ax.set_ylabel("Value of $10,000 (USD)")
ax.legend(loc="upper right", fontsize=9, frameon=False)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
save(fig, "fig_4_3_oos_equity.png")

# OOS zoom on strategy only
fig, ax = plt.subplots(figsize=(7.5, 2.6))
ax.plot(eo["date"], eo["equity"], color=GREEN, lw=1.3, label="Base costs")
ax.plot(eo["date"], eo["equity_stress"], color="#555555", lw=1.0, ls=":", label="Stress costs")
ax.axhline(10000, color="#999999", lw=0.8, ls="--")
ax.set_ylabel("Account value (USD)")
ax.legend(loc="lower left", fontsize=9, frameon=False)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
save(fig, "fig_4_4_oos_zoom.png")


# ---------------- Figure 4.5: Reliance funnel ----------------
mm = json.load(open(BT / "multimarket/results/summary.json"))
fn = mm["RELIANCE_1D"]["funnel"]
stages = ["LC entry window (fresh flip)", "+ SQZ regime gate", "+ NW trend", "+ WT timing", "+ WWV confirmation"]
labels = ["ML entry candidates (LC)", "+ Regime gate (SQZ)", "+ Trend filter (NW)", "+ Timing (WT)",
          "+ Volume confirmation (WWV)"]
vals = [fn["long"][s] + fn["short"][s] for s in stages]
fig, ax = plt.subplots(figsize=(7.0, 2.8))
yy = list(range(len(vals)))[::-1]
ax.barh(yy, vals, color=[BLUE] * 4 + [GREEN], height=0.6)
for y_, v in zip(yy, vals):
    ax.text(v + 6, y_, str(v), va="center", fontsize=10)
ax.set_yticks(yy); ax.set_yticklabels(labels)
ax.set_xlabel("Candidate bars (long + short), Reliance daily, 2004-2026")
ax.set_xlim(0, 560)
ax.grid(axis="y", visible=False)
save(fig, "fig_4_5_funnel.png")


# ---------------- Figure 4.6: multi-market before/after ----------------
pre = json.load(open(BT / "multimarket/results_pretuning/summary.json"))
order = ["BTCUSD_1D", "NIFTY_1D", "HDFCBANK_1D", "RELIANCE_1D"]
names = ["Bitcoin 1D", "NIFTY 50 1D", "HDFC Bank 1D", "Reliance 1D"]
a = [pre[k]["base"]["net_return_pct"] for k in order]
b = [mm[k]["base"]["net_return_pct"] for k in order]
fig, ax = plt.subplots(figsize=(7.0, 3.0))
x = range(len(order))
ax.bar([i - 0.18 for i in x], a, 0.36, color="#9aa3b5", label="Pine defaults")
ax.bar([i + 0.18 for i in x], b, 0.36, color=BLUE, label="Run 17 parameters (tuned on BTC 1h)")
for i, (u, v) in enumerate(zip(a, b)):
    ax.text(i - 0.18, u + (0.2 if u >= 0 else -0.6), f"{u:+.1f}", ha="center", fontsize=9)
    ax.text(i + 0.18, v + (0.2 if v >= 0 else -0.6), f"{v:+.1f}", ha="center", fontsize=9)
ax.axhline(0, color="#333333", lw=0.8)
ax.set_xticks(list(x)); ax.set_xticklabels(names)
ax.set_ylabel("Net return (%)")
ax.set_ylim(-7, 8)
ax.legend(fontsize=9, frameon=False, loc="upper left")
ax.grid(axis="x", visible=False)
save(fig, "fig_4_6_multimarket.png")

print("figures:", sorted(p.name for p in OUT.iterdir()))
print("funnel", vals)
