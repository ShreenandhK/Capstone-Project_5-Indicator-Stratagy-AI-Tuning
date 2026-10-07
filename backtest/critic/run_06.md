RUN: 06
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -0.055→+0.226 (Δ+0.281, clears bar easily) — first positive Sharpe. PF crosses 1.0 for the first time (0.984→1.060, G2 PASSES). But trade_tstat only 0.344 (not remotely significant, need ~±1.97 at n≈190); PSR0 0.640 (64% confidence true SR>0 — barely more than a coin flip); DSR of this new "best" is only 0.139 at N=6 (vs PSR0 0.640) — the multiple-testing correction erases most of the raw confidence. Treat "positive Sharpe" as unproven, not confirmed.
- Drawdown: max_dd 2.30%→1.50% (real improvement), duration 392→402d (flat), skew 0.21→0.57 (better), kurtosis flat (13.5→14.0).
- Significance: still only 191 trades, still G1-only-adequate; t-stat and DSR both say "not yet distinguishable from noise."
- Robustness: G4 still 1/3 — 2023 got WORSE (-0.72%→-0.84%), 2024 slightly better (+2.14%→+2.28%), 2025H1 improved (-1.56%→-0.71%) but stays negative. Long PF 1.024→1.032 (net +$15.1→+$20.0), short PF 0.939→1.093 (net -$33.7→+$49.5, +$83 swing) — both sides now nominally >1, but see entry-set audit below for why this is fragile. Stress net -2.74%→-1.87%, still fails G3.
- Costs: unaffected mechanically; G3 failure is the binding constraint now that G1/G2 pass.

ENTRY-SET AUDIT (run05 vs run06 trades.csv, by entry_time+direction): NOT identical, despite both having 191 trades — the match is coincidental, not exit-only. At least 7 entries appear only in run06, ≥6 only in run05, and 3 shift to an adjacent bar (same underlying signal, different fill) — ~16 trades (~8%) differ; the remaining ~92% are byte-identical entries. lcNeighbors moved entries, not just exits. Critically, two trades explain most of the $88.09 net-pnl swing: one shifted trade (long, 2025-01-14→01-13) flips from a -$18.45 SL to a +$30.15 TP (Δ+$48.60), and one brand-new trade (short, 2025-03-03, TP) contributes +$42.88 — together ≈$91, i.e. essentially the entire improvement, concentrated in 2 of 191 trades, both landing in the already-thin 2025H1 window (49→51 trades). This is a textbook fragile-peak signature (small param change, discontinuous single-trade outcome flip driving the headline result), not a broad distributional improvement.

WEAKNESSES: First positive Sharpe is real in dollars but statistically unproven (t=0.34, DSR=0.14) and mechanically fragile (2 trades ≈ 100% of the gain). G3 still fails. 2023 regressed.

DEMANDS FOR NEXT CONFIG: (1) Do not treat run06 as a stable baseline — run a robustness neighbor probe (lcNeighbors 10 or 14) to see if the gain survives a small perturbation, given how bar-shift-sensitive it proved. (2) Target G3/stress directly next. (3) Still owed: SQZ 'Released Within Window' for 2023/2025H1.

PLATEAU ASSESSMENT: Best (fallback) = run06, sharpe 0.226, 0 runs since improvement. Untested: SQZ regime mode, WWV threshold, further LC tightening, allowShorts diagnostic. 6/25 used — not plateau; first gate-pass is encouraging but needs a robustness re-test before trusting it.
