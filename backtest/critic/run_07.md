RUN: 07
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.182 (vs run06 0.226, Δ-0.044 — moved the wrong way); PF 1.048 (vs 1.060); PSR0 0.613 (vs 0.640); DSR of the still-standing best (run06) ticks down to 0.123 at N=7. Neither run eligible (G3, G4 fail); still far below B&H 1.787.
- Drawdown: max_dd 1.39% (better than run06's 1.50%), duration ~407d (flat), skew 0.365 (down from 0.571), kurtosis flat (~14.0).
- Significance: 193 trades, trade t-stat 0.275 (still nowhere near significant), win rate 48.7%.
- Robustness: long PF 1.081, short PF 1.013 (both hold ≥1.0); 2023 improved (-0.84%→-0.57%), 2024 fell (2.28%→1.87%), 2025H1 numerically identical (-0.71%, 51 trades — same as run06). G4 still 1/3. Stress -1.87%→-2.02% (slightly worse), still fails G3.

PRE-REGISTERED CONFIRM/REFUTE RULING: Sharpe 0.182≥0.10 ✓, PF 1.048≥1.03 ✓, long PF 1.081≥1.0 ✓, short PF 1.013≥1.0 ✓ — all four numeric bars met → CONFIRMS by the letter of the pre-registration. Both flagged trades (long 2025-01-13 TP, short 2025-03-03 TP) are present, same direction/outcome, near-identical size to run06 (+$30.11 vs +$30.15; +$42.82 vs +$42.88) — not neighbor=12-specific flukes. BUT a new -$52.27 SL (short, 2024-03-05, -5.25%, the largest single-trade loss across all 7 runs) appears, replacing a small run06 loser — same fragility pattern, now cutting the other way. Hard test: removing just the top-2 gross winners (2024-03-15, 2025-03-03) drops PF below 1.0 in BOTH runs (run06→0.983, run07→0.973). The "not concentrated in 1-2 trades" clause is therefore NOT satisfied in either run — pre-existing, unresolved, not something run07 fixed or worsened. Net ruling: CONFIRM on the four numeric thresholds; FAIL on the concentration clause. PF>1 should be treated as thin, not structural.

INCUMBENT: Run06 remains incumbent under the mechanical pre-registered rule — neither run is eligible, so fallback applies (highest Sharpe among trades≥30 runs): run06 0.226 > run07 0.182. Run07 was a diagnostic robustness probe, not a replacement candidate; it confirms run06 isn't a zero-neighbor-count fluke while also showing real sensitivity (-0.044 Sharpe from a 2-neighbor move, plus a new $52 loss trade) — a mild caution, not a refutation.

WEAKNESSES: PF fragile in both runs (flips <1.0 losing just 2 trades). G3/G4 still unresolved. The robustness probe moved Sharpe down, not up.

DEMANDS FOR NEXT CONFIG: (1) Keep lcNeighbors=12 (run06) as incumbent, not 14. (2) Attack G3/G4 next — SQZ 'Released Within Window' probe still owed for 2023/2025H1. (3) Adopt a leave-top-2-trades-out PF check as a standing robustness gate going forward, given how easily PF flips.

PLATEAU ASSESSMENT: Best (fallback) = run06, sharpe 0.226, 1 run since last ≥0.05 improvement (this run regressed slightly). Untested: SQZ regime mode, WWV threshold, allowShorts diagnostic. 7/25 used — not plateau.
