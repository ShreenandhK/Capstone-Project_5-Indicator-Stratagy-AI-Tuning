RUN: 05
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -0.0551 vs run04 -0.1113, Δ=+0.0562 — clears the ≥0.05 bar, but by only 0.006; PSR0 0.465 (up from 0.430); DSR of current best 0.089 at N=5 (down from 0.101 — deflation growing faster than raw PSR). Marginal, not decisive.
- Drawdown: max_dd 2.30% (WORSE than run04's 1.88%), duration 392d (better than 448d), skew +0.21 (less positive than +0.52), kurtosis 13.53 (much improved from 21.60, more trades dilutes any single tail event). Mixed, not a clean win.
- Significance: trades 108→191 (+77%); trade t-stat -0.082 (best yet, but largely a sample-size effect — avg_trade_return_pct barely moved, -0.026%→-0.0087%, n did most of the work); win rate 44.4%→47.1% but payoff ratio WORSE (1.199→1.104, avg win 1.44%→1.28%).
- Robustness: net pnl genuinely improved (-$29.51→-$18.64, +$10.87) but decomposes as: long -$28.91→+$15.08 (Δ+$43.99, PF 0.910→1.024, long alone now clears G2); short -$0.61→-$33.72 (Δ-$33.11, PF 0.998→0.939). 100% of this run's gain is long-side; loosening WT timing diluted short quality — expected in a BTC uptrend (more badly-timed counter-trend shorts admitted). 2025H1 net worse (-1.29%→-1.56%), G4 still 1/3. Stress worse (-1.75%→-2.74%, more trades = more cost drag).
- Costs: stress degradation scaled with trade count — a real, quantifiable price for "widening."

WEAKNESSES: The improvement is real in dollars but thin and one-sided, not broad-based (short PF regressed under looser timing). Max_dd and stress both moved the wrong way even as Sharpe improved — not free. G2 (0.984), G3, G4 all still fail; PF barely moved from run04's 0.959.

TUNER REASONING CHECK: (a) SQZ 'Released Within Window' collapsing trades<100 — plausible but unverified; still an untested lever, defer only, don't drop. (b) lcDistQuantile 0.80 no-op at lcNeighbors=8: CONFIRMED — floor(8×0.75+0.5)=floor(8×0.80+0.5)=6; correctly skipped, but a bigger move (≥0.90, floor=7) would not be a no-op — don't treat the lever as dead. (c) allowShorts=false ≈48 trades fails G1 (matches run04's long_trades=48): CONFIRMED, using long_profit_factor as proxy is budget-sound. All three deferrals are sound reasoning, correctly executed.

DEMANDS FOR NEXT CONFIG:
1. Use this widened 191-trade universe for the tightening it was built for: test `lcNeighbors` up (10-12) or `lcDistQuantile` ≥0.85-0.90 (a real, non-no-op move) to recover quality, especially on shorts, while staying ≥100 trades.
2. Repair the short-side regression directly — e.g. narrow `wtCrossWindow` instead of a full mode swap, or tighten `wtOsLevel1/2`, rather than accepting a long-only edge.
3. Still owed: `sqzRegimeMode='Released Within Window'` test to address 2025H1, which just got worse (-1.56%).

PLATEAU ASSESSMENT: Best (fallback) = run05, sharpe -0.0551, 0 runs since ≥0.05 improvement (this run cleared it, barely). Untested: SQZ regime mode, LC neighbor/quantile tightening, WWV volume threshold. 5/25 used — not plateau; gains are real but thin and long-only-driven, with clear next probes remaining.
