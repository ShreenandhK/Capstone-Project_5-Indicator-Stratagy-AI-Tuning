RUN: 04
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -0.111 (run02 -0.666, Δ+0.555 — largest jump yet); PSR0 0.430 (highest so far, was 0.143); DSR of current best only 0.101 at N=4 — deflation still large vs PSR0. Still FAIL vs B&H +1.787.
- Drawdown: max_dd 1.88% (down from 2.21%), duration 448 days (down from 887 — halved), skew flipped -0.90→+0.52 (first positive skew), kurtosis 25.29→21.60. Real tail-risk improvement.
- Significance: trades 108 (still ≥100, G1 pass) vs 117 in run02 — trade t-stat -0.174 (near-zero, best yet, essentially indistinguishable from breakeven); win rate flat at 44.44% (identical ratio to run02) but payoff ratio rose 0.984→1.199 (avg win 1.32%→1.44%, avg loss -1.34%→-1.20%) — the gain is on payoff, not win-rate/count manipulation.
- Robustness: long PF 0.798→0.910 (-3 trades) and short PF 0.779→0.998 (-6 trades, net -$109→-$0.60) improved together — broad-based, not one bucket. 2024 PF 1.35→1.77 (44 trades, materially better quality, not just fewer); 2023 improved (-1.44%→-0.95%) but still negative; 2025H1 net improved slightly (-1.50%→-1.29%) but Sharpe worsened (-2.51→-2.70, more variance on 29 vs 30 trades) — G4 still 1/3. Stress net -3.40%→-1.75%, still fails G3.
- Costs: unaffected, not binding. G2 now close: PF 0.959 vs 1.0 — first run within reach of a gate pass.

WEAKNESSES:
- Trade count fell 117→108 (-7.7%): win rate held and payoff improved on both sides, so this reads as a genuine quality filter, not pure count-collapse — but 108 is now closer to the G1=100 floor; further tightening risks crossing under 100 or manufacturing PF gains via attrition alone.
- 2025H1 Sharpe got WORSE (-2.51→-2.70) despite better net return — remains the weakest link; risk, not just return, hasn't improved there. G4 still fails.
- Still 0/4 eligible; PF 0.959 <1.0, stress still net-negative (-1.75%).
- Only 4 trials — DSR 0.101 well below PSR0 0.430; "best so far" is still fragile against the multiple-testing correction.

DEMANDS FOR NEXT CONFIG:
1. Keep this base fixed and do one single-lever probe targeting 2025H1 specifically (e.g. `sqzRegimeMode='Released Within Window'` or a small `lcRegimeThreshold` tightening) to try to flip a second sub-period positive and close G4.
2. Separately test a small LC entry tightening (`lcNeighbors` up, or `lcDistQuantile`→0.80) to push PF over 1.0 — watch trade count doesn't fall below ~100.
3. Run the deferred `allowShorts=false` diagnostic now that short PF (0.998) is near breakeven — confirm how much residual gap is long- vs short-side.
4. Do not stack multiple new levers next run — isolate cause given proximity to gates.

PLATEAU ASSESSMENT: Best (fallback) = run04, sharpe -0.111, 0 runs since improvement (this run is the improvement, Δ+0.555). Untested: LC entry params, WT timing, WWV threshold, SQZ regime mode, long/short isolation. 4/25 runs used — not plateau; broad-based, non-artifactual progress with a concrete remaining gap (2025H1 risk, PF<1).
