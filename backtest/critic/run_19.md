RUN: 19
VERDICT: PLATEAU
SCORECARD:
- Risk-adjusted: Sharpe -0.119 (vs run17 0.355) — triggers the tuner's own REFUTE threshold (<0.355) with room to spare, and is negative outright. PF 0.964 (<1.0, fails G2 — first endgame probe to fail G2 outright since run14/15). PSR0 0.425, trade_tstat -0.187 (both negative-leaning, weak).
- Drawdown: max_dd 2.11% (worse than run17's 1.49%), duration 414.5d. Kurtosis 24.5 — fattest tail of any run in the 06+ family.
- Significance: trades 169 (near predicted 170-215, only 1 below range).
- Sub-period: 2023 -1.002% (tuner's third criterion — "2023 stays positive" — explicitly REFUTED, and by a wide margin: run17's +0.037% collapses to -1.002%); 2024 +2.448% (best 2024 print of the study, but isolated); 2025H1 -1.796% (worse than run17's -0.734%). G4 fails (1/3). Long PF 1.118 (best long print yet, net +$61.6) vs short PF 0.829 (net -$101.5, worst short print in the 06+ family) — the WWV brick resize helped longs and badly hurt shorts. Stress -2.66% (worse than run17's -1.42%), G3 fails by more than ever.

RULING ON TUNER'S PRE-STATED CRITERIA: REFUTED on all three stated conditions simultaneously — Sharpe (-0.119 ≪ 0.355), PF-ex-top-2 (headline PF itself is already <1.0, so ex-top-2 is certainly <1.0, ≪ the 1.0 bar), and "2023 stays positive" (it flips hard negative). This is the cleanest, most decisive refutation of any endgame probe.

WEAKNESSES: None new to diagnose — this result closes out the endgame plan with a clear negative.

DEMANDS FOR NEXT CONFIG: None. Per the tuner's own wrap-up plan and my pre-committed rule, freeze is recommended.

PLATEAU ASSESSMENT — final ruling: All three endgame probes are now resolved: (a) LC feature type (run16) — REFUTED. (b) WT overextension cap (run17) — passed its own initial bar, but the mandatory ±45 neighborhood check (run18) showed a non-monotonic dip-then-spike (0.213→0.196→0.355), the signature of a fragile, narrow local peak rather than a broad regime effect. (c) WWV brick resize (run19) — REFUTED decisively on all three stated criteria. Per my own pre-committed rule ("PLATEAU is warranted if (b) and (c) fail to deliver a robust lift"), that condition is now met. Additional support: DSR of the current best is ~0.18-0.19 and has been essentially flat since run17 despite Sharpe more than doubling from run06 — the multiple-testing penalty is now the dominant constraint, and each further trial raises that bar further while remaining untested levers (lcSpacing, lcRegimeThreshold, riskAtrLen, wtN1/N2, nwKernelType/Lookback) are progressively marginal, second-order parameters within already-probed roles, not new mechanisms. One role (SQZ regime) has had only a single probe (run08) — a genuine gap — but given 6 slots remain and the accumulated fragility evidence across the whole study (PF-ex-top-2 has cleared 1.0 in exactly one, now-discredited run), I judge the expected value of further search below its DSR cost. RULING: PLATEAU.

Mechanically selected frozen configuration: per SPEC §8, no run has ever passed all four gates (best eligible sharpe = NaN throughout); the fallback rule applies — highest Sharpe among runs with trades≥30, flagged FAILED PRE-REGISTERED GATES. That is run17 (config = run06 base + nwBandwidth=5 + wtObLevel2/wtOsLevel2=±40; sharpe 0.355, PF 1.098, trades 188; fails G3 only, passes G1/G2/G4).

Caveats the write-up MUST carry: (1) Fails G3 — not robust to realistic stress costs (+1.12% base → -1.42% stress). (2) Tail-concentrated: PF-ex-top-2=1.019, net-ex-top-2=+$21.99 of $112.32 total (~80% from 2 trades); ex-top-3 net is NEGATIVE (-$11.35). (3) The ±40 WT threshold is a non-monotonic, likely fragile local spike (run18 evidence), not a validated broad effect. (4) G4's pass rests on a near-zero 2023 (+0.037%, essentially coin-flip). (5) 2025H1 has never been made robustly positive across all 19 runs. (6) DSR ≈0.18-0.19 at N=19-25 — treat the IS result as statistically unconfirmed after correcting for search. OOS results should be interpreted with wide skepticism, not as edge confirmation.

---

ORCHESTRATOR NOTE (not critic text): exact diagnostics for run 19 vs run 17 — 165/169 entries shared with identical exits; 23 run-17 trades removed (+$122.09, median +0.493 %); 4 new trades (−$29.80); PF-ex-top-2 = 0.890; net ex-top-2 = −$122.72. Loop stopped on this PLATEAU verdict with 19 of 25 parameter sets used.
