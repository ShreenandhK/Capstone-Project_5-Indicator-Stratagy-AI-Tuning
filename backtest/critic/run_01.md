RUN: 01
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -1.71 / Sortino -2.10 / Calmar -0.34 vs buy-and-hold Sharpe +1.79 on the identical window; PSR0 = 0.0028 (~0.3% probability the true Sharpe is even positive). FAIL.
- Drawdown: max_dd 4.20% at 10%-of-equity sizing (≈42% scaled to full exposure), duration 901 days (near the entire 2.5y IS window), skew -1.04, kurtosis 23.65, 9 max consecutive losses — fat-tailed, unrecovered. FAIL.
- Significance: 117 trades clears G1 (>=100) but trade t-stat = -2.69 (statistically significant negative edge, not noise); win rate 36.75%, 95% CI [28.6%, 45.8%] — entire CI sits below the ~52.9% breakeven win rate implied by payoff ratio 0.89. FAIL, and this is a real signal, not a sampling artifact.
- Robustness: all 3 sub-periods negative (2023 -1.48%, 2024 -0.91%, 2025H1 -1.16%, G4 = 0/3); short trades (66, PF 0.36, -\ net) are the dominant bleed vs longs (51, PF 0.75, -\ net) while B&H returned +548% — shorting into the strongest leg of a bull market. Stress costs push it further negative (net -5.19%, Sharpe -2.45). FAIL.
- Costs: round-trip commission ~0.15% + 2-tick slippage is immaterial in $ terms at $17k- BTC prices (fixed, not tunable) — costs are not the cause of the loss; avg trade -0.30% is explained by the win-rate/payoff gap, not fee drag. TP never fires (riskUseTp=false, 0 TP exits in exit_reasons).

WEAKNESSES:
- Exit mix is timer-dominated, not signal-dominated: of 90 "LC Exit" trades essentially all show bars_held=4 (avg_bars_held=3.46 overall), meaning `exitHoldBars`=4 is doing almost all the work and LC's own signal-flip logic rarely fires first inside the window — the "Either (LC Default)" mode is functionally a fixed 4-bar exit with an SL overlay.
- Payoff ratio 0.89 (avg win 0.897% vs avg loss -1.002%) is inverted relative to the 36.75% win rate (expectancy -$3.00/trade, -0.304% avg) — both entry selection and exit/risk design contribute to negative expectancy.
- Short side is the structural problem: 66 short trades, PF 0.36, -$276 net vs 51 longs, PF 0.75, -$75 net, against a +548% B&H bull run — this looks like fighting trend/beta, not a fine-tuning issue.
- Exposure only 1.85% (405/21887 bars) — equity curve is flat >98% of the time punctuated by sharp SL losses; annualized Sharpe/Sortino are being set by a handful of tail days (skew -1.04, kurtosis 23.65).
- TP disabled and never used (riskUseTp=false, TP:0 exits) — winners are only ever capped by the 4-bar timer while the 2×ATR stop (SL: 27 trades) realizes losses (~-1.0% to -2.9%) larger than average wins, an asymmetric-risk/no-asymmetric-reward design.
- All 3 IS sub-periods negative — G4 fails 0/3 (needed 2/3), so this is a persistent negative edge across the whole IS window, not one bad year.

DEMANDS FOR NEXT CONFIG (priority order):
1. Isolate the short-side drag: run `allowShorts=false` (long-only) as a structured Strategy-Controls probe to quantify how much of -3.51% net / -1.71 Sharpe is short-side beta-fighting vs a genuine long-side entry problem.
2. Fix the payoff asymmetry: set `riskUseTp=true` (riskTpMult already 3.0, in-bounds 0.5-12.0) so winners get a defined target instead of only the 4-bar timer; and/or raise `exitHoldBars` from 4 toward 8-12 (bounds 1-96) to let winners develop, since the timer currently pre-empts the LC flip almost every trade.
3. Re-tune the stop: `riskSlMult` (currently 2.0, bounds 0.5-8.0) is producing SL losses bigger than average wins — test 2.5-3.0 paired with the TP change so risk stays bounded but stops aren't firing on normal 1H BTC noise.
4. Strengthen trend/regime quality rather than just quantity: `nwSlopeLen=1` is a single-bar (very noisy) slope — test 3-5 (bounds 1-20) with `nwRequirePriceSide=true`; test `sqzRegimeMode='Released Within Window'` vs current 'Squeeze Off' to time entries nearer volatility expansion.
5. Lower priority: test `wtTimingMode='Not Overextended Only'` — with only 1.85% exposure, the 5-filter AND funnel may be over-pruning rather than adding orthogonal edge.
Do not spend budget on costs/sizing — they are fixed and not the loss driver here.

PLATEAU ASSESSMENT: No eligible run yet (0/1; run 01 fails G2, G3, G4). Best-by-fallback sharpe = -1.7079 (run 01, FAILED PRE-REGISTERED GATES). Runs since improvement: N/A (first run). Untested levers: every role (trend NW, entry LC, timing WT, confirmation WWV, regime SQZ, exits/risk) and long/short permission remain unprobed beyond Pine defaults. Far too early for PLATEAU — only 1/25 runs used, and the failure mode is clearly diagnosable (timer-dominated exits, inverted payoff ratio, short-side beta drag) with concrete untested levers remaining.
