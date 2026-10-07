RUN: 17
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.213(run11)/0.226(run06)→0.355 (Δ+0.129/+0.142 — first run to clear the 0.276 bar since run06, largest single-run jump in the whole study). PF 1.098 (best since run06). trade_tstat 0.544 (highest of any run, but still far from conventional significance, |t|~0.54 vs a ~1.96 bar). PSR0 0.715 (first time >50%) — BUT DSR at N=17 is only 0.179. That 0.715-vs-0.179 gap is the central fact: after correcting for 17 searched configurations, there is only ~18% confidence this Sharpe exceeds noise. Encouraging, not proven.
- Drawdown: max_dd 1.49% (best-in-class, tied with run06), duration 326d (best yet). Skew 1.265 / kurtosis 18.28 — highest positive skew AND fattest tail of any run: gains are even more tail-concentrated than before.
- Significance: trades 219→188 (-31, -14%, within tuner's 175-205 prediction) — smaller sample, cutting both ways for power.
- Concentration (self-derived from trades.csv, pending official diagnostic): top-2 winners (2024-03-15 short TP +$46.44, 2025-03-03 short TP +$43.89) sum to $90.32 — 80.4% of the entire $112.32 net profit. PF-ex-top-2 ≈ (1260.25-90.32)/1147.94 ≈ 1.019; net-ex-top-2 ≈ $22.00. If confirmed, this is the FIRST run where PF-ex-top-2 clears 1.0 — genuine progress on the core-edge question — but the margin is razor-thin (≈$22 net, ≈0.019 PF) built entirely on losing BOTH of two specific trades; losing either alone still leaves PF>1 (≈1.06), so it isn't a single-trade cliff, but it is a two-trade cliff.
- Sub-period/long-short: G4 PASSES (2/3) — but 2023 is +0.037% on 58 trades (PF 1.012, essentially a coin-flip result, not a robust positive) and 2025H1 is still -0.734% (PF 0.784), unresolved. Only 2024 is a clear win. Long PF 1.110 / short PF 1.086 — genuinely balanced, no directional crutch, a real improvement over prior runs.
- Stress/G3: -1.42% is the best stress result of any run, but still fails G3. Base-to-stress degradation (~2.55pp) has been structurally ~1.5-2.7pp in every run regardless of lever — it hasn't shrunk with tuning. Closing G3 realistically requires roughly doubling the current base edge (~1.1%→~3%+), not a marginal push.

RULING ON TUNER'S 3 PRE-STATED CRITERIA: (1) PF-ex-top-2>1.0 — PASSES by my estimate (~1.019), pending confirmation. (2) net-ex-top-2>$0 — PASSES (~$22), pending confirmation. (3) removed trades net-negative in aggregate — UNCONFIRMED, awaiting diagnostic; cannot rule yet.

WEAKNESSES: G4's pass hinges on a near-zero 2023 result. DSR (0.179) says treat this as unproven. WT threshold moved 13 points in one jump — untested whether this is a broad improvement or a narrow peak.

DEMANDS: (1) MANDATORY neighborhood probe before trusting this run: test wtObLevel2/wtOsLevel2 at ±45 or ±47 (between run11's ±53 and run17's ±40) to check if the gain is monotonic/broad or a fragile spike. (2) Await the removed-trades diagnostic to close criterion (3). (3) Do not spend more than 1-2 more slots chasing G3 directly — the required base-edge doubling is a high bar.

PLATEAU ASSESSMENT: Best (fallback) = run17, sharpe 0.355; streak of non-improvement BROKEN. 8/25 slots remain. PLATEAU REJECTED — this is exactly the kind of result that argues search is not exhausted; but the very next run must be the fragility/neighborhood check before further exploitation.

---

ORCHESTRATOR NOTE (not critic text; added at pause, 2026-09-13): the critic finalized the verdict above before reading the queued diagnostics. The diagnostics (RESUME.md §3; reproducible with `python diagnostics.py 06 11 17`) confirm all three pre-stated criteria: (1) PF-ex-top-2 = 1.019 > 1.0; (2) net-ex-top-2 = +$21.99 > $0; (3) the 31 removed trades = −$40.74 aggregate (net-negative). Also: run 17 is a pure subset of run 11 (0 new entries, identical exits); net ex-top-3 = −$11.35.
