RUN: 02
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -0.666 (up from -1.708 in run01, Δ+1.042, well past the 0.05 bar) vs B&H +1.787 — gap still ~2.45; PSR0 0.143 (up from 0.003, still <50% confidence true Sharpe>0); DSR of current best 0.047 at N=2 trials — most of the raw improvement is already eaten by the multiple-testing penalty. Real progress, still FAIL.
- Drawdown: max_dd 2.21% (down from 4.20%; ≈22% full-size-equivalent at 10x for 10%-of-equity sizing), duration 887 days (still ~2.4y, unrecovered in-window), skew -0.90 / kurtosis 25.29 (still fat left tail, kurtosis marginally worse), max consecutive losses 6 (down from 9). Improved but still structurally long/unrecovered.
- Significance: trades unchanged at 117; trade t-stat -1.09 (no longer statistically distinguishable from zero, vs -2.69 in run01 — can't confirm a real fix, only that "proven negative" is no longer provable); win rate 44.4%, CI95 [35.8%, 53.5%] now straddles the ~50.4% breakeven win rate implied by payoff 0.984 — genuinely ambiguous rather than clearly negative.
- Robustness: G4 still 1/3 — 2024 flipped positive (+1.11%, PF 1.35) but 2023 stayed negative (-1.44%) and 2025H1 got WORSE (-1.50% vs -1.16% in run01); short PF jumped 0.355→0.779 (net -\→-\, 66 trades) while long PF/net barely moved (0.752→0.798, -\→-\, 51 trades) — confirms the run01 short-side bleed was largely an exit-design artifact, validating the tuner's deferral of allowShorts=false, but the 2025H1 regression is a new flag. Stress still fails G3 (-3.40% net, stress Sharpe -1.21; degradation ≈1.56pp, similar proportionally to run01's ≈1.68pp — cost sensitivity essentially unchanged).
- Costs: unaffected by this config change and still not the binding constraint — G2 (PF 0.787<1) and G3 (stress net <0) both still fail; the strategy remains a net loser independent of statistical noise.

WEAKNESSES:
- Still 0/2 eligible runs; G2, G3, G4 all fail again this run.
- 2025H1 sub-period got worse (-1.50% vs -1.16%), and SL count rose from 27→43 (23%→36.8% of trades, avg loss also grew -1.00%→-1.34%) — the longer 12-bar hold is exposing positions to more adverse stop-outs; the 2×ATR stop is now the dominant loss driver, not the old timer.
- Trade t-stat moved from -2.69 (significant negative) to -1.09 (ambiguous) — good direction, but at 117 trades this is not yet strong evidence the exit fix produced a real edge; needs more runs/robustness before trusting it.
- DSR 0.047 vs PSR0 0.143 at just N=2 trials — the deflation penalty is already large; it will keep growing as more of the 25-run budget is spent, so future "improvements" need to be structurally justified, not incremental noise-chasing.
- Long side essentially untouched by this fix (PF 0.798, net -\, unchanged from run01) — all of this run's gain came from the short side and the payoff-ratio repair; long entries/exits remain undiagnosed.

DEMANDS FOR NEXT CONFIG:
1. Target 2023/2025H1 weakness directly (G4 needs 2/3, currently 1/3): probe regime/trend timing — test `nwSlopeLen` 3-5 with `nwRequirePriceSide=true`, or `sqzRegimeMode='Released Within Window'`, to see if better regime timing turns 2023 and/or 2025H1 positive without breaking 2024.
2. Address the now-dominant SL bleed (43 stop-outs, avg loss -1.34%): test `riskSlMult` in 2.5-3.0 (bounds 0.5-8.0) now that holds are longer, to check if fewer premature stop-outs improve PF without collapsing trade count.
3. Diagnose the long side specifically (flat at PF 0.798 since run01): probe LC entry parameters (`lcNeighbors`, `lcDistQuantile`, `lcEntryWindow`) or `wtTimingMode` to see whether long entries can be improved independently of the exit fix that mostly rescued shorts.
4. Run the deferred `allowShorts=false` diagnostic within the next few runs — now that the exit model is materially different, this comparison will cleanly isolate genuine long edge vs short edge instead of being conflated with the old broken exit.
5. Return to single-lever changes per the tuner's own protocol — this run's 2-parameter jump was justified as answering explicit demands, but the next step should isolate cause and effect again.

PLATEAU ASSESSMENT: No eligible run yet (0/2); best-by-fallback = run 02, sharpe -0.666 (FAILED PRE-REGISTERED GATES). Runs since last ≥0.05 improvement: 0 (this run is itself the improvement, Δ+1.042 vs run01). Untested levers: trend NW (slope length, price-side requirement), LC entry (neighbors, distance quantile, entry window, regime/ADX filters), WT timing mode, WWV volume threshold, SQZ regime mode, and long/short isolation — all remain untested. Far from plateau: 2/25 runs used, gates still failing on G2/G3/G4, and a concrete hypothesis-driven change just validated real progress with clear next levers identified.
