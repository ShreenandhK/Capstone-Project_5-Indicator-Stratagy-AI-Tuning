#!/usr/bin/env python
"""Render results/summary.json + equity_daily.csv into a single self-contained HTML report.

  build_report.py OUT.html
"""
from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
ORDER = ["BTCUSD_1D", "NIFTY_1D", "HDFCBANK_1D", "RELIANCE_1D"]
SHORT = {"BTCUSD_1D": "Bitcoin", "NIFTY_1D": "NIFTY 50", "HDFCBANK_1D": "HDFCBANK", "RELIANCE_1D": "RELIANCE"}
TV = {"BTCUSD_1D": "BITSTAMP:BTCUSD", "NIFTY_1D": "NSE:NIFTY", "HDFCBANK_1D": "NSE:HDFCBANK", "RELIANCE_1D": "NSE:RELIANCE"}
CCY = {"BTCUSD_1D": "USD", "NIFTY_1D": "INR", "HDFCBANK_1D": "INR", "RELIANCE_1D": "INR"}


def ok(x):
    return x is not None and not (isinstance(x, float) and not math.isfinite(x))


def num(x, nd=2, sign=False, suffix=""):
    if not ok(x):
        return '<span class="na">—</span>'
    s = f"{x:+,.{nd}f}" if sign else f"{x:,.{nd}f}"
    return s.replace("-", "−") + suffix


def row(label, cells, cls=""):
    return f'<tr class="{cls}"><th scope="row">{label}</th>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


def summary_table(S):
    ks = ORDER
    head = "".join(f'<th scope="col">{SHORT[k]}<small>{TV[k]}</small></th>' for k in ks)
    g = lambda f: [f(S[k]) for k in ks]  # noqa: E731
    rows = [
        row("Backtest window", g(lambda r: f"{r['window_start']} → {r['window_end']}<small>{r['window_bars']:,} bars</small>")),
        row("Closed trades", g(lambda r: f"{r['base']['trades']}<small>{r['base']['long']['trades']} long · {r['base']['short']['trades']} short</small>")),
        row("Net profit", g(lambda r: f"{num(r['base']['net_profit'], 0, True)}<small>{num(r['base']['net_return_pct'], 2, True, ' %')}</small>"), "key"),
        row("Profit factor", g(lambda r: num(r["base"]["all"]["profit_factor"])), "key"),
        row("Percent profitable", g(lambda r: num(r["base"]["all"]["percent_profitable"], 1, suffix=" %"))),
        row("Avg trade", g(lambda r: f"{num(r['base']['all']['avg_trade'], 2, True)}<small>{num(r['base']['all']['avg_trade_pct'], 2, True, ' %')}</small>")),
        row("Avg win / avg loss", g(lambda r: num(r["base"]["all"]["ratio_avg_win_avg_loss"]))),
        row("Max equity drawdown", g(lambda r: f"{num(r['base']['max_drawdown'], 0)}<small>{num(r['base']['max_drawdown_pct'], 2, suffix=' %')}</small>")),
        row("CAGR", g(lambda r: num(r["base"]["cagr_pct"], 2, True, " %"))),
        row("Sharpe (annualised)", g(lambda r: num(r["base"]["sharpe"]))),
        row("Trade t-stat", g(lambda r: num(r["base"]["trade_tstat"]))),
        row("Avg bars in trade", g(lambda r: num(r["base"]["all"]["avg_bars_in_trade"], 1))),
        row("Time in market", g(lambda r: num(r["base"]["exposure_pct"], 1, suffix=" %"))),
        row("Commission paid", g(lambda r: num(r["base"]["all"]["commission_paid"], 0))),
        row("Stress costs · net", g(lambda r: f"{num(r['stress']['net_return_pct'], 2, True, ' %')}<small>PF {num(r['stress']['all']['profit_factor'])}</small>"), "sep"),
        row("Long-only · net", g(lambda r: f"{num(r['long_only']['net_return_pct'], 2, True, ' %')}<small>PF {num(r['long_only']['all']['profit_factor'])} · {r['long_only']['trades']} trades</small>")),
        row("Buy &amp; hold · net", g(lambda r: f"{num(r['buy_and_hold']['net_return_pct'], 0, True, ' %')}<small>max DD {num(r['buy_and_hold']['max_drawdown_pct'], 1, suffix=' %')}</small>")),
    ]
    return f'<div class="scroll"><table class="summary"><thead><tr><th></th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def side_table(r):
    b = r["base"]
    sides = [("All", b["all"]), ("Long", b["long"]), ("Short", b["short"])]
    spec = [("Net profit", "net_profit", 2, True, ""), ("Gross profit", "gross_profit", 2, False, ""),
            ("Gross loss", "gross_loss", 2, False, ""), ("Profit factor", "profit_factor", 2, False, ""),
            ("Trades", "trades", 0, False, ""), ("Percent profitable", "percent_profitable", 1, False, " %"),
            ("Avg trade", "avg_trade_pct", 2, True, " %"), ("Median trade", "median_trade_pct", 2, True, " %"),
            ("Avg winning trade", "avg_win", 2, False, ""), ("Avg losing trade", "avg_loss", 2, False, ""),
            ("Largest winning trade", "largest_win", 2, False, ""), ("Largest losing trade", "largest_loss", 2, False, ""),
            ("Avg bars in trade", "avg_bars_in_trade", 1, False, "")]
    head = "".join(f'<th scope="col">{n}</th>' for n, _ in sides)
    body = "".join(row(lbl, [num(s[key], nd, sg, sf) for _, s in sides]) for lbl, key, nd, sg, sf in spec)
    return f'<table class="perf"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table>'


def year_table(r):
    head = "<th scope='col'>Year</th><th scope='col'>Strategy</th><th scope='col'>Trades</th><th scope='col'>PF</th><th scope='col'>Buy &amp; hold</th>"
    body = ""
    for y, v in r["years"].items():
        if not v:
            continue
        body += (f"<tr><th scope='row'>{y}</th><td>{num(v['net_return_pct'], 2, True, ' %')}</td><td>{v['trades']}</td>"
                 f"<td>{num(v['profit_factor']) if v['trades'] else '<span class=na>—</span>'}</td>"
                 f"<td>{num(v['buy_and_hold_pct'], 1, True, ' %')}</td></tr>")
    return f'<div class="scroll short"><table class="years"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def funnel_table(r):
    f = r["funnel"]
    steps = list(f["long"].keys())[:-1]
    body = "".join(row(html.escape(s), [f["long"][s], f["short"][s]]) for s in steps)
    return (f'<table class="funnel"><thead><tr><th scope="col">Bars passing</th><th scope="col">Long</th><th scope="col">Short</th></tr></thead>'
            f'<tbody>{body}</tbody></table><p class="note">LC flips in window: {f["lc_flips_long"]} long, {f["lc_flips_short"]} short.</p>')


def exits(r):
    e = r["base"]["exit_reasons"]
    names = {"LC Exit": "hold timer / LC flip", "SL": "ATR stop", "TP": "ATR target", "Reverse": "Reversal", "WindowEnd": "End of data"}
    return " · ".join(f"{names.get(k, k)} {v}" for k, v in e.items())


def join(names):
    names = list(names)
    if not names:
        return "none"
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def verdict(S):
    b = {k: S[k]["base"] for k in ORDER}
    fmt = lambda k: f"{SHORT[k]} {num(b[k]['net_return_pct'], 2, True, ' %')}"  # noqa: E731
    pos = [fmt(k) for k in ORDER if b[k]["net_return_pct"] > 0]
    neg = [fmt(k) for k in ORDER if b[k]["net_return_pct"] <= 0]
    best = max(ORDER, key=lambda k: b[k]["trade_tstat"] if ok(b[k]["trade_tstat"]) else -1e9)
    tmax = b[best]["trade_tstat"]
    exp = [b[k]["exposure_pct"] for k in ORDER]
    short_neg = [SHORT[k] for k in ORDER if b[k]["short"]["net_profit"] < 0]
    long_pos = [SHORT[k] for k in ORDER if b[k]["long"]["net_profit"] > 0]
    sig = (f"No market reaches a trade t-stat of 2 (highest: {SHORT[best]} {num(tmax)}), so none of these results is "
           f"statistically distinguishable from zero." if tmax < 2 else
           f"{SHORT[best]} reaches a trade t-stat of {num(tmax)}.")
    return (f"<p>Across the four markets the strategy took <b>{sum(x['trades'] for x in b.values())}</b> trades in total. "
            f"Positive: {join(pos)}. Zero or negative: {join(neg)}.</p>"
            f"<p>{sig} With 10 % of equity per trade and {min(exp):.0f}–{math.ceil(max(exp))} % time in market, returns are "
            f"small in every case and far below buy-and-hold. Short trades lost money on {join(short_neg)}; the long side "
            f"was positive on {join(long_pos)}.</p>")


def compare_section(S, O, pretuning, pinfo):
    if O is None:
        return ""
    cur, oth = ("Pre-tuning", "Tuned") if pretuning else ("Tuned", "Pre-tuning")
    spec = [("Trades", lambda r: str(r["base"]["trades"])),
            ("Net return", lambda r: num(r["base"]["net_return_pct"], 2, True, " %")),
            ("Profit factor", lambda r: num(r["base"]["all"]["profit_factor"])),
            ("Max drawdown", lambda r: num(r["base"]["max_drawdown_pct"], 2, suffix=" %")),
            ("Trade t-stat", lambda r: num(r["base"]["trade_tstat"])),
            ("Long-only net", lambda r: num(r["long_only"]["net_return_pct"], 2, True, " %"))]
    head = "".join(f'<th scope="col">{SHORT[k]}</th>' for k in ORDER)
    body = ""
    for i, (lbl, f) in enumerate(spec):
        body += row(f"{lbl} · {cur}", [f(S[k]) for k in ORDER], "key" + (" sep" if i else ""))
        body += row(f"{lbl} · {oth}", [f(O[k]) for k in ORDER])
    diffs = pinfo["diff_vs_current_pine"] if pretuning else {}
    if not pretuning:
        diffs = O[ORDER[0]]["params"]["diff_vs_current_pine"]  # already (pre-tuning, tuned)
    dl = "; ".join(f"<code>{k}</code> {v[0]} → {v[1]}" for k, v in diffs.items())
    return (f'<section><h2>Pre-tuning vs tuned inputs</h2><p class="note" style="margin-bottom:10px">Same script logic, same data, '
            f'same costs. The inputs that differ (pre-tuning → tuned): {dl}.</p><div class="scroll"><table class="summary">'
            f'<thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div></section>')


def variant_text(S, pretuning, full):
    p = S[ORDER[0]]["params"]
    tp = f" / target {full['riskTpMult']:g}×" if full["riskUseTp"] else ", no take-profit"
    v = {"exec_fact": f"signal on bar close → fill next open; ATR stop {full['riskSlMult']:g}×{tp}; "
                      f"{full['exitHoldBars']}-bar hold or LC flip"}
    if pretuning:
        v.update(
            title="Pre-Tuning CRB Daily Backtests",
            h1="Combined Role-Based Strategy on daily bars, pre-tuning inputs",
            lede="Backtest of <code>Combined Role-Based Strategy.pine</code> with the input defaults it had before the "
                 "BTC 1H tuning study, run unchanged over the full available daily history of Bitcoin, NIFTY 50, "
                 "HDFC Bank and Reliance.",
            params_fact=f"original .pine input defaults · hash {p['config_hash']}<br>= BTC 1H study run 01 (baseline)",
            cav_title="Untuned original inputs",
            cav="These are the script's defaults before any tuning (BTC 1H run 01). The script logic is identical to "
                "the current file; only 9 input defaults differ (listed in the comparison above).",
            flag=" --pretuning")
    else:
        v.update(
            title="CRB Strategy Daily Backtests",
            h1="Combined Role-Based Strategy on daily bars",
            lede="Backtest of <code>Combined Role-Based Strategy.pine</code> with its current inputs, run unchanged over "
                 "the full available daily history of Bitcoin, NIFTY 50, HDFC Bank and Reliance. No parameter was "
                 "fitted to these markets.",
            params_fact=f".pine input defaults · hash {p['config_hash']}<br>= frozen BTC 1H run {p['matches_frozen_run']}",
            cav_title="Parameters come from BTC 1H",
            cav="The inputs were tuned on Bitcoin hourly bars (2023–2025, frozen run 17). The daily runs are an "
                "out-of-market transfer test, not a re-optimisation.",
            flag="")
    return v


def main(out: Path, pretuning: bool) -> None:
    from run_multimarket import pine_params
    res = HERE / ("results_pretuning" if pretuning else "results")
    S = json.loads((res / "summary.json").read_text(encoding="utf-8"))
    other = HERE / ("results" if pretuning else "results_pretuning") / "summary.json"
    O = json.loads(other.read_text(encoding="utf-8")) if other.exists() else None
    full, pinfo = pine_params(pretuning)
    V = variant_text(S, pretuning, full)
    series = {}
    for k in ORDER:
        d = pd.read_csv(res / k / "equity_daily.csv")
        series[k] = {"d": d["date"].tolist(), "s": [round(x, 2) for x in d["equity"]],
                     "l": [round(x, 2) for x in d["equity_long_only"]]}
    p = S[ORDER[0]]["params"]
    markets = ""
    for k in ORDER:
        r = S[k]
        dq = r["data"]["quality"]
        dnotes = []
        if dq.get("manual_fixes"):
            dnotes.append("7 bars 1997-10-27→11-04 halved (Yahoo applied the 2:1 split a week late)")
        if dq.get("rows_dropped_zero_volume_flat"):
            dnotes.append(f"{dq['rows_dropped_zero_volume_flat']} zero-volume flat filler rows removed")
        if dq.get("rows_ohlc_repaired"):
            dnotes.append(f"{dq['rows_ohlc_repaired']} bars with inconsistent high/low widened")
        markets += f"""
<section class="market" id="{k}">
  <header><h3>{SHORT[k]} <span>{TV[k]} · 1D · {CCY[k]}</span></h3>
  <p class="meta">{r['bars_total']:,} daily bars from {r['data']['first_bar'][:10]} ({html.escape(r['data']['source'].split(' GET')[0])}). The first {r['warmup_bars']:,} are classifier warm-up; trading from {r['window_start']}. Exits: {exits(r)}.{(' Data: ' + '; '.join(dnotes) + '.') if dnotes else ''}</p></header>
  <div class="grid3">
    <div><h4>Performance summary</h4>{side_table(r)}</div>
    <div><h4>By calendar year</h4>{year_table(r)}</div>
    <div><h4>Entry funnel</h4>{funnel_table(r)}</div>
  </div>
</section>"""

    doc = f"""<title>{V['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap">
<style>
:root{{--ground:#f6f7f5;--surface:#fcfcfb;--ink:#16181a;--ink2:#54575b;--ink3:#80837f;--rule:#dde0dc;--rule2:#eceeea;--hi:#eef3fb;
--s1:#2a78d6;--s2:#eb6834;--grid:#e6e8e4;
--serif:"Source Serif 4",Georgia,serif;--sans:"IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--ground:#111312;--surface:#1a1a19;--ink:#f2f2ef;--ink2:#c3c2b7;--ink3:#8f8f88;--rule:#343532;--rule2:#262725;--hi:#1b2433;--s1:#3987e5;--s2:#d95926;--grid:#2c2d2a}}}}
:root[data-theme="dark"]{{--ground:#111312;--surface:#1a1a19;--ink:#f2f2ef;--ink2:#c3c2b7;--ink3:#8f8f88;--rule:#343532;--rule2:#262725;--hi:#1b2433;--s1:#3987e5;--s2:#d95926;--grid:#2c2d2a}}
body{{background:var(--ground);color:var(--ink);font:15px/1.55 var(--sans)}}
main{{max-width:1120px;margin:0 auto;padding:40px 24px 64px;display:flex;flex-direction:column;gap:44px}}
h1,h2,h3{{font-family:var(--serif);font-weight:600;text-wrap:balance;margin:0}}
h1{{font-size:34px;line-height:1.15}} h2{{font-size:23px;margin-bottom:12px}} h3{{font-size:20px}}
h3 span{{font:500 13px var(--mono);color:var(--ink2);margin-left:8px}}
h4{{font:600 12px var(--sans);text-transform:uppercase;letter-spacing:.06em;color:var(--ink2);margin:0 0 8px}}
p{{margin:0;max-width:72ch}} .lede{{color:var(--ink2);font-size:16px;margin-top:10px}}
.note,.meta{{color:var(--ink2);font-size:13px}} .meta{{margin-top:6px;max-width:none}}
.facts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);margin-top:22px}}
.facts div{{background:var(--surface);padding:10px 14px}} .facts dt{{font-size:12px;color:var(--ink2)}} .facts dd{{margin:2px 0 0;font:500 13px var(--mono)}}
.verdict{{background:var(--surface);border:1px solid var(--rule);padding:18px 22px;display:grid;gap:8px}}
.verdict p{{max-width:90ch}}
.scroll{{overflow-x:auto}} .scroll.short{{max-height:420px;overflow-y:auto}}
table{{border-collapse:collapse;font-variant-numeric:tabular-nums;width:100%}}
th,td{{padding:6px 10px;text-align:right;border-bottom:1px solid var(--rule2);vertical-align:top;white-space:nowrap}}
th[scope=row]{{text-align:left;font-weight:400;color:var(--ink2)}} thead th{{font-weight:600;border-bottom:1px solid var(--rule);position:sticky;top:0;background:var(--surface)}}
td{{font-family:var(--mono);font-size:13px}} small{{display:block;font:12px var(--mono);color:var(--ink3)}}
thead small{{font-family:var(--mono);font-weight:400}}
.summary{{background:var(--surface);border:1px solid var(--rule);min-width:760px}} .summary td,.summary thead th{{min-width:150px}}
.summary tr.key td{{background:var(--hi);font-weight:500}} .summary tr.sep th,.summary tr.sep td{{border-top:1px solid var(--rule)}}
.na{{color:var(--ink3)}}
.charts{{display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:16px}}
.chart{{background:var(--surface);border:1px solid var(--rule);padding:14px 16px 8px;position:relative}}
.chart h4{{display:flex;justify-content:space-between;gap:8px}} .chart h4 b{{font:500 12px var(--mono);text-transform:none;letter-spacing:0;color:var(--ink)}}
.chart svg{{width:100%;height:auto;display:block;overflow:visible}}
.legend{{display:flex;gap:18px;font-size:13px;color:var(--ink2);margin-bottom:12px}} .legend i{{display:inline-block;width:14px;height:2px;vertical-align:middle;margin-right:6px;border-radius:1px}}
.tip{{position:absolute;pointer-events:none;background:var(--surface);border:1px solid var(--rule);padding:6px 9px;font:12px/1.45 var(--mono);color:var(--ink);box-shadow:0 2px 8px rgba(0,0,0,.08);white-space:nowrap}}
.market{{display:flex;flex-direction:column;gap:16px;border-top:1px solid var(--rule);padding-top:22px}}
.grid3{{display:grid;grid-template-columns:1.25fr 1fr .95fr;gap:22px;align-items:start}}
@media (max-width:980px){{.grid3{{grid-template-columns:1fr}}}}
.grid3 table{{background:var(--surface);border:1px solid var(--rule)}}
.caveats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px 28px;padding:0;margin:0;list-style:none}}
.caveats li{{border-top:1px solid var(--rule);padding-top:10px;font-size:14px}} .caveats b{{display:block;font-weight:600;margin-bottom:2px}}
code,pre{{font:13px var(--mono)}} pre{{background:var(--surface);border:1px solid var(--rule);padding:12px 14px;overflow-x:auto;margin:0}}
</style>
<main>
<header>
  <h1>{V['h1']}</h1>
  <p class="lede">{V['lede']}</p>
  <dl class="facts">
    <div><dt>Parameters</dt><dd>{V['params_fact']}</dd></div>
    <div><dt>Capital &amp; sizing</dt><dd>10,000 · 10 % of equity per trade · no pyramiding</dd></div>
    <div><dt>Costs (Pine header)</dt><dd>0.075 %/side commission · 2 ticks slippage</dd></div>
    <div><dt>Stress costs</dt><dd>0.10 %/side commission · 5 bps slippage</dd></div>
    <div><dt>Execution</dt><dd>{V['exec_fact']}</dd></div>
    <div><dt>Engine</dt><dd>Python port of the Pine logic + TradingView broker emulator (88 tests)</dd></div>
  </dl>
</header>

<section class="verdict">
  <h2>Result</h2>
  {verdict(S)}
</section>

<section>
  <h2>Summary</h2>
  {summary_table(S)}
  <p class="note" style="margin-top:8px">Net profit, drawdown and commission are in the instrument's currency on 10,000 starting capital. Sharpe uses daily returns annualised with √365 for Bitcoin and √252 for NSE. Max drawdown is peak-to-trough on bar-close equity. Buy &amp; hold covers the same window with no costs.</p>
</section>

{compare_section(S, O, pretuning, pinfo)}

<section>
  <h2>Equity curves</h2>
  <div class="legend"><span><i style="background:var(--s1)"></i>Strategy (as written)</span><span><i style="background:var(--s2)"></i>Long-only variant (allowShorts = false)</span></div>
  <div class="charts" id="charts"></div>
</section>

<section>
  <h2>Per market</h2>
  <p class="note">Laid out like TradingView's Strategy Tester. The entry funnel counts bars where the Lorentzian classifier had a fresh flip, then how many survive each extra role gate. The WWV confirmation almost never removes a bar that the other gates passed.</p>
  {markets}
</section>

<section>
  <h2>Read before quoting these numbers</h2>
  <ul class="caveats">
    <li><b>Classifier window differs from TradingView</b>The Pine anchors the Lorentzian search on <code>last_bar_index</code>, so TradingView's Strategy Tester trains on one fixed block of history. This engine searches the previous 2,000 bars at every bar (causal). Trade lists on TradingView will not match one-for-one.</li>
    <li><b>2,000-bar warm-up</b><code>lcMaxBarsBack = 2000</code> means no signal is possible before bar 2,000: about 5.5 years of Bitcoin and 8 years of NSE history are consumed before the first trade.</li>
    <li><b>Small samples</b>39–75 trades over roughly 10–23 years. Yearly figures often rest on 0–5 trades; treat them as anecdotes.</li>
    <li><b>{V['cav_title']}</b>{V['cav']}</li>
    <li><b>Shorting on NSE</b>Cash equities cannot be held short overnight, and the NIFTY index cannot be traded directly. Short trades there assume futures or a CFD. The long-only line is the realistic cash-market case.</li>
    <li><b>Data sources</b>Bitcoin: Bitstamp daily (TradingView BITSTAMP:BTCUSD). NSE: Yahoo Finance, split-adjusted and not dividend-adjusted (TradingView default). Real NSE delivery costs are above the Pine's 0.075 %. The stress-cost line is closer to them.</li>
  </ul>
</section>

<section>
  <h2>Reproduce</h2>
  <pre>cd backtest
.venv\\Scripts\\python.exe multimarket\\fetch_multimarket.py
.venv\\Scripts\\python.exe multimarket\\run_multimarket.py{V['flag']}
.venv\\Scripts\\python.exe multimarket\\build_report.py report.html{V['flag']}</pre>
  <p class="note" style="margin-top:8px">Per-market metrics.json, trades.csv, trades_long_only.csv and equity_daily.csv are in <code>backtest/multimarket/{res.name}/</code>.</p>
</section>
</main>
<script>
const DATA={json.dumps(series, separators=(",", ":"))};
const NAMES={json.dumps({k: SHORT[k] + " · " + TV[k] for k in ORDER})};
const CCY={json.dumps(CCY)};
const W=520,H=230,M={{l:52,r:14,t:8,b:26}};
function ticks(lo,hi,n){{const span=hi-lo||1,step0=span/n,mag=Math.pow(10,Math.floor(Math.log10(step0)));const step=[1,2,2.5,5,10].map(m=>m*mag).find(s=>s>=step0);const out=[];for(let v=Math.ceil(lo/step)*step;v<=hi+1e-9;v+=step)out.push(+v.toFixed(6));return out;}}
function fmt(v){{return (v<0?"−":"")+Math.abs(v).toLocaleString("en-US",{{maximumFractionDigits:0}});}}
const root=document.getElementById("charts");
for(const [k,d] of Object.entries(DATA)){{
  const n=d.d.length, all=d.s.concat(d.l), lo0=Math.min(...all), hi0=Math.max(...all);
  const pad=(hi0-lo0)*0.08||50, lo=lo0-pad, hi=hi0+pad;
  const x=i=>M.l+(W-M.l-M.r)*i/(n-1), y=v=>M.t+(H-M.t-M.b)*(1-(v-lo)/(hi-lo));
  const path=a=>a.map((v,i)=>(i?"L":"M")+x(i).toFixed(1)+" "+y(v).toFixed(1)).join("");
  let g="";
  for(const t of ticks(lo,hi,4)){{g+=`<line x1="${{M.l}}" x2="${{W-M.r}}" y1="${{y(t)}}" y2="${{y(t)}}" stroke="var(--grid)" stroke-width="1"/><text x="${{M.l-6}}" y="${{y(t)+4}}" text-anchor="end" font-size="11" fill="var(--ink3)" font-family="var(--mono)">${{fmt(t)}}</text>`;}}
  g+=`<line x1="${{M.l}}" x2="${{W-M.r}}" y1="${{y(10000)}}" y2="${{y(10000)}}" stroke="var(--ink3)" stroke-width="1" stroke-dasharray="3 3"/>`;
  let lastYear="";const y0=+d.d[0].slice(0,4),y1=+d.d[n-1].slice(0,4),every=Math.max(1,Math.ceil((y1-y0)/6));
  d.d.forEach((s,i)=>{{const yr=s.slice(0,4);if(yr!==lastYear){{lastYear=yr;if(i>0&&(+yr-y0)%every===0)g+=`<text x="${{x(i)}}" y="${{H-6}}" text-anchor="middle" font-size="11" fill="var(--ink3)" font-family="var(--mono)">${{yr}}</text>`;}}}});
  const fs=d.s[n-1],fl=d.l[n-1];
  const card=document.createElement("figure");card.className="chart";card.style.margin="0";
  card.innerHTML=`<h4>${{NAMES[k]}}<b>${{fmt(fs)}} ${{CCY[k]}}</b></h4><svg viewBox="0 0 ${{W}} ${{H}}" role="img" aria-label="Equity curve ${{NAMES[k]}}: strategy ends at ${{fmt(fs)}}, long-only at ${{fmt(fl)}} from 10,000">${{g}}
  <path d="${{path(d.l)}}" fill="none" stroke="var(--s2)" stroke-width="2" stroke-linejoin="round"/>
  <path d="${{path(d.s)}}" fill="none" stroke="var(--s1)" stroke-width="2" stroke-linejoin="round"/>
  <line class="cx" y1="${{M.t}}" y2="${{H-M.b}}" stroke="var(--ink3)" stroke-width="1" visibility="hidden"/>
  <circle class="ps" r="4" fill="var(--s1)" stroke="var(--surface)" stroke-width="2" visibility="hidden"/>
  <circle class="pl" r="4" fill="var(--s2)" stroke="var(--surface)" stroke-width="2" visibility="hidden"/>
  <rect x="${{M.l}}" y="0" width="${{W-M.l-M.r}}" height="${{H}}" fill="transparent"/></svg><div class="tip" hidden></div>`;
  root.appendChild(card);
  const svg=card.querySelector("svg"),tip=card.querySelector(".tip"),cx=svg.querySelector(".cx"),ps=svg.querySelector(".ps"),pl=svg.querySelector(".pl");
  svg.addEventListener("pointermove",e=>{{const r=svg.getBoundingClientRect(),sx=(e.clientX-r.left)*W/r.width;const i=Math.max(0,Math.min(n-1,Math.round((sx-M.l)/(W-M.l-M.r)*(n-1))));
    for(const el of [cx,ps,pl])el.setAttribute("visibility","visible");cx.setAttribute("x1",x(i));cx.setAttribute("x2",x(i));
    ps.setAttribute("cx",x(i));ps.setAttribute("cy",y(d.s[i]));pl.setAttribute("cx",x(i));pl.setAttribute("cy",y(d.l[i]));
    tip.hidden=false;tip.innerHTML=`${{d.d[i]}}<br><span style="color:var(--s1)">━</span> Strategy ${{fmt(d.s[i])}}<br><span style="color:var(--s2)">━</span> Long-only ${{fmt(d.l[i])}}`;
    const px=(x(i)/W)*r.width+16, left=px+tip.offsetWidth>r.width?px-tip.offsetWidth-32:px;tip.style.left=(left+16)+"px";tip.style.top="44px";}});
  svg.addEventListener("pointerleave",()=>{{tip.hidden=true;for(const el of [cx,ps,pl])el.setAttribute("visibility","hidden");}});
}}
</script>
"""
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main(Path(sys.argv[1]), "--pretuning" in sys.argv[2:])
