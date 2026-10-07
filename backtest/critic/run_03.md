RUN: 03
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -0.798 (down from run02's -0.666, Δ-0.132 — regression, not improvement); PSR0 0.098 (down from 0.143); best-so-far in leaderboard is still run02 (DSR 0.033 at N=3, falling as trials accumulate). FAIL, and worse than run02.
- Drawdown: max_dd 2.87% (up from 2.21%), skew -1.35 (worse than run02's -0.90, deeper left tail), kurtosis 21.93 (marginally better than 25.29), max consecutive losses unchanged at 6.
- Significance: trades unchanged 117; trade t-stat -1.26 (still statistically ambiguous, slightly more negative than run02's -1.09); win rate improved 44.4%→47.0%, CI95 [38.2%, 56.0%], but payoff ratio fell 0.984→0.843 — win rate gain didn't translate to edge.
- Robustness: G4 still 1/3 — 2024 profit collapsed +1.11%→+0.36% (PF 1.35→1.09), 2025H1 improved slightly (-1.50%→-1.31%), 2023 flat (-1.44%→-1.40%). Net effect: no sub-period crossed into "fixed." Stress net worsened -3.40%→-3.89% (still fails G3).
- Costs: unchanged mechanism; not the driver of the regression.

WEAKNESSES:
- Demand #2 (widen `riskSlMult` 2.0→3.0) backfired: SL exit count fell 43→21 (fewer stop-outs) but avg loss per losing trade grew (-1.34%→-1.51%, avg_loss_usd -13.30→-14.95) — trades.csv shows the wider stop lets losers run further before LC-flip/timer catches them (e.g. -3.50%, -3.76%, -4.26%, -3.08% losses now appear where run02 would have stopped near -2%). This is a whipsaw-prone entry set, not a "give it room" setup — widening risk amplified variance without adding edge.
- Net pnl worse on both sides: long -$75→-$122 (PF 0.798→0.707), short -$109→-$112 (roughly flat) — the wider stop actively hurt longs, which had been stable.
- profit_factor fell 0.787→0.747, net_return -1.84%→-2.34%, Sharpe -0.666→-0.798 — a clean single-lever test that moved every headline metric in the wrong direction. Useful negative result, not noise-mining (single param, large N, consistent direction across sub-metrics).

DEMANDS FOR NEXT CONFIG:
1. Revert `riskSlMult` to 2.0 (run02's value) — this lever is disproven in the "wider" direction; do not re-test above 2.0. If stop-tightening is wanted, test 1.5 instead in a future isolated run, but it's not the priority now.
2. Return to run02's base (`exitHoldBars=12, riskUseTp=true, riskSlMult=2.0`) and address 2023/2025H1 weakness via trend/regime, single-lever: `nwSlopeLen` 3-5 + `nwRequirePriceSide=true`, or `sqzRegimeMode='Released Within Window'`.
3. Diagnose the long side (PF still <0.80 across all 3 runs) via LC entry params (`lcNeighbors`, `lcDistQuantile`) — untouched since run01.
4. Run deferred `allowShorts=false` diagnostic once the base config is back at the run02 level.

PLATEAU ASSESSMENT: Best (fallback) still run02, sharpe -0.666, unchanged for 1 run since improvement (run03 regressed). Untested: trend NW, LC entry, WT timing, WWV, SQZ regime, long/short isolation. Only 3/25 runs used, one gate-passing dimension still open (G1 only) — not remotely plateau; the negative result on riskSlMult is informative, not a sign of exhausted search space.
