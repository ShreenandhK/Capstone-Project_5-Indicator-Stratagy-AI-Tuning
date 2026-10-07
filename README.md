# Combined Role-Based (CRB) Strategy — Backtest, Tuning & Out-of-Sample Study

**Authors:** B. Rohith, C. Srinish, K. Chinmai Datha, K. Shreenandh, M. Satvik Kumar  
**Mentor:** Dr. Ram Soorat

A five-indicator Pine Script v6 strategy for BTC/USDT on the 1-hour chart was ported to Python, tuned in-sample
under a pre-registered protocol (hard cap 25 parameter sets), frozen, and evaluated **once** out-of-sample.

**Result in one line:** the best in-sample configuration (Sharpe 0.355) failed out-of-sample (Sharpe −1.93,
net −3.12 %, profit factor 0.60, trade t-stat −2.43). The in-sample optimum is best described as an overfit,
tail-concentrated local spike, not a demonstrated edge.

## 1. Headline results

| Metric | In-sample (run 17) | Out-of-sample |
|---|---|---|
| Window (bar open time, UTC) | 2023-01-01 00:00 → 2025-06-30 23:00 | 2025-07-01 00:00 → 2026-09-13 15:00 |
| Sharpe / Sortino (annualised, daily returns, rf = 0) | 0.355 / 0.554 | **−1.927** / −2.332 |
| Net return / CAGR | +1.12 % / +0.45 % | **−3.12 %** / −2.60 % |
| Max drawdown / duration | 1.49 % / 326 d | 3.72 % / 387 d |
| Trades / win rate / profit factor | 188 / 47.9 % / 1.098 | 125 / 35.2 % / **0.596** |
| Trade t-stat / PSR(0) | 0.54 / 0.715 | −2.43 / 0.013 |
| Stress costs (0.10 % + 5 bps per side) | −1.42 % (Sharpe −0.43) | −4.81 % (Sharpe −2.86) |
| Buy-and-hold BTC, same window | +547.7 % (Sharpe 1.79) | −28.0 % (Sharpe −0.44) |
| Deflated Sharpe ratio (19 trials) | 0.187 | — |

Position sizing is fixed at 10 % of equity per trade, so absolute returns are small by construction; compare
scale-free metrics (Sharpe, profit factor, t-stat).

## 2. What is in this bundle

```
./
├── Combined Role-Based Strategy.pine     FINAL strategy, inputs set to the frozen configuration (run 17)
├── README.md                             this file
├── LICENSE                               licensing: CC BY-NC-SA 4.0, with MPL 2.0 portions and third-party exceptions
├── paper/                                publication materials (regenerable)
│   ├── figures/                          fig1_tuning_trajectory, fig2_equity_is_oos, fig3_subperiod_returns (.png 300 dpi + .pdf)
│   ├── tables/                           table1..table5 (.csv) + tables.md
│   ├── Combined Role-Based Strategy.baseline.pine   pre-tuning strategy (Pine defaults = run 01), for comparison
│   ├── make_figures.py                   regenerates figures/
│   └── make_tables.py                    regenerates tables/ and the baseline .pine (verified against engine defaults)
├── backtest/
│   ├── SPEC.md                           the pre-registered contract: periods, costs, Pine semantics, metrics, selection rule
│   ├── LOOP_PROTOCOL.md                  role briefs for the tuning loop (tuner, executor, critic, tracker)
│   ├── FROZEN_PARAMS.json                frozen parameters, selection rule/status, DSR, full in-sample metrics
│   ├── results/OOS_FINAL/                the single out-of-sample run: metrics.json, trades.csv, equity_daily.csv, LOCK
│   ├── results/run_01 … run_19/          every in-sample run: metrics.json, trades.csv, equity_daily.csv
│   ├── logs/tuning_log.md                COMPLETE tuning log (params, exact metrics, gates, critic verdict per run)
│   ├── logs/tuning_log.jsonl             machine-readable log (one JSON object per run)
│   ├── logs/leaderboard.md               runs ranked by Sharpe, with DSR
│   ├── critic/run_01 … run_19.md         the adversarial critic's full verdict after every run
│   ├── configs/run_01 … run_19.json      exact parameter overrides for every run
│   ├── engine/                           Python port: pine_ta, mlext, signals, broker (TradingView fill emulator), metrics, params
│   ├── tests/                            88 tests (ta parity, causality/lookahead, broker, cross-check vs backtesting.py, guards)
│   ├── run_backtest.py, log_tools.py     CLI runner (guards: run cap, IS truncation, one-shot OOS lock) and log tooling
│   ├── diagnostics.py, nesting.py        trade-concentration and filter-nesting diagnostics used in the critic reviews
│   ├── data/BTCUSDT_1h.csv (+ .meta.json, fetch_data.py)   dataset, checksum/gap report, downloader
│   ├── multimarket/                      post-study 1D check on BTCUSD, NIFTY, HDFCBANK, RELIANCE (fetch, run, results)
│   └── requirements.txt                  pinned Python package versions
├── Project_Report/                       course project report (PDF), its figures and the scripts that build it
├── source_indicators/                    the five third-party indicator sources, unmodified, with citation headers
└── .claude/agents/                       sub-agent definitions (adversary = critic/reviewer, builder)
```

The three core deliverables: **final strategy** → `Combined Role-Based Strategy.pine`;
**backtest results** → `backtest/results/` + `backtest/FROZEN_PARAMS.json`;
**tuning logs** → `backtest/logs/` + `backtest/critic/` + `backtest/configs/`.

## 3. Study design

- **Instrument / data:** Binance spot BTCUSDT, 1-hour klines, 2022-01-01 → 2026-09-13 15:00 UTC (41,199 bars; one missing
  bar 2023-03-24 13:00, not filled). SHA-256 `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`.
  2022 is indicator warm-up only.
- **Periods:** in-sample 2023-01-01 → 2025-06-30; out-of-sample 2025-07-01 → last closed bar. In-sample runs truncate the
  data *before* any indicator is computed; the out-of-sample run is guarded by an exclusive lock file.
- **Execution model:** TradingView semantics — signals on bar close, market fills at next open, intrabar stop/limit with
  TradingView's O-H-L-C path rule, commission 0.075 %/side, 2-tick slippage, 10 % of equity per trade, no pyramiding.
- **Strategy roles:** Nadaraya-Watson = trend filter; Lorentzian Classification = sole entry signal; WaveTrend = timing;
  Weis Wave Volume = confirmation; Squeeze Momentum = regime gate; exits = LC flip / fixed hold / ATR stop & target.
- **Pre-registered selection rule (SPEC §8, fixed before run 01):** eligible if G1 trades ≥ 100, G2 profit factor > 1,
  G3 stress-cost net return > 0, G4 ≥ 2 of 3 in-sample sub-periods profitable; best = highest in-sample Sharpe among
  eligible runs; fallback if none eligible = highest Sharpe with ≥ 30 trades, flagged "FAILED PRE-REGISTERED GATES".
  **No run passed all four gates; run 17 was selected by the fallback** (it fails G3 only).
- **Tuning loop:** each iteration a tuner agent proposed one parameter set, an executor ran it, an adversarial critic
  reviewed the metrics (and trade-level diagnostics) and demanded changes, and a tracker logged the verdict. The loop
  stopped when the critic declared a plateau (after run 19 of 25).

## 4. Reproducing

Python 3.13 on Windows was used.

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r backtest/requirements.txt
cd backtest
../.venv/Scripts/python -m pytest tests -q          # expect 88 passed
../.venv/Scripts/python log_tools.py verify          # expect OK (19 runs logged, cap 25)
../.venv/Scripts/python log_tools.py best            # expect run 17
cd ..
.venv/Scripts/python paper/make_tables.py
.venv/Scripts/python paper/make_figures.py
```

`run_backtest.py is` refuses to overwrite logged runs and `oos` refuses to run a second time (by design). To recompute a
run independently, point the tooling at a scratch copy with the `CRB_BACKTEST_ROOT` environment variable (see
`run_backtest.py` / `tests/test_guards.py`).

## 5. Limitations and caveats (state these in any write-up)

1. **TradingView will not reproduce these numbers.** The Pine script's Lorentzian kNN window is anchored on
   `last_bar_index`, so on a chart it only produces predictions on the final `lcMaxBarsBack` bars. The Python engine uses a
   causal rolling window of the most recent `lcMaxBarsBack` bars (SPEC §3.3, "Deviation D1"). This is the only intentional
   logic deviation; reproducing the backtest in TradingView requires porting that window into the Pine code.
2. **Fragile in-sample optimum.** Run 17's gain comes from a WaveTrend cap of ±40; ±45 (run 18) gave Sharpe 0.196 and
   ±53 (run 11) 0.213 — a non-monotonic spike. The whole gain is 15 trades with WaveTrend between 40 and 45 at entry.
3. **Tail concentration.** ~80 % of run 17's in-sample profit came from two trades; net profit excluding the top three trades
   is negative. G4 passed only because 2023 returned +0.037 %.
4. **Multiple testing.** 19 configurations were evaluated; the deflated Sharpe ratio of the selected run is 0.19.
5. **Not cost-robust.** The selected run fails G3 (negative under 0.10 % + 5 bps costs) in-sample.
6. **Scope.** One asset, one timeframe, one exchange feed, long/short spot-like PnL without funding or borrow costs.
7. **Pine-faithful quirks are kept on purpose:** the LC training label is backward-looking (as in the original script),
   MLExtensions normalisation uses running min/max from the data start (2022-01-01).
8. **Engine validation.** The Python port was checked by 88 automated tests (reference implementations, prefix-causality
   proof, broker scenarios, a backtesting.py cross-check agreeing to 3e-9 relative) and an independent adversarial code
   review. It has not been cross-checked against TradingView's own Strategy Tester (not possible because of item 1).

## 6. AI assistance disclosure

The Python engine, tests, tuning loop, diagnostics and this bundle were produced with **Claude Code** (Anthropic) in an
orchestrator + sub-agent setup: an orchestrator model (Claude Opus 5) coordinated build agents (data fetch, signal port,
broker/metrics), an independent adversarial reviewer, and the loop agents — tuner, executor, tracker, and the critic
defined in `.claude/agents/adversary.md`. The human authors defined the strategy, the periods, the 25-run cap, the one-shot
out-of-sample rule and the review requirements. Many venues require disclosure of AI tool use; the authors remain
responsible for verifying the code and claims.

## 7. Data, third-party code and licensing

- **Market data:**
  - `backtest/data/BTCUSDT_1h.csv` (Binance spot public API, `/api/v3/klines`) and
    `backtest/multimarket/data/BTCUSD_1D.csv` (Bitstamp public API) are **included**, because the fetch scripts
    always download up to the current time and so cannot rebuild the exact files the study used. Check the SHA-256
    against the matching `.meta.json`. The same Binance klines are also published at https://data.binance.vision.
  - The NSE series (`NIFTY_1D`, `HDFCBANK_1D`, `RELIANCE_1D`) come from Yahoo Finance, whose terms do not allow
    redistribution, so they are **not included**. Rebuild them with
    `python backtest/multimarket/fetch_multimarket.py NIFTY_1D HDFCBANK_1D RELIANCE_1D`. The new files will run past
    the study's end date and Yahoo may revise adjusted prices, so results can differ slightly from
    `backtest/multimarket/results/`. Running the script also overwrites the committed `.meta.json`, which holds the
    original checksums (`git checkout` restores it).
- **Indicator sources** (`source_indicators/`, included for provenance). Each file holds the author's published
  code unmodified (verified line by line against TradingView on 2026-10-07), with the author's own licence and
  credit lines, under a citation header. The strategy file credits all five at the top.

  | Indicator | Author (TradingView account) | Published | Licence |
  |---|---|---|---|
  | [Machine Learning: Lorentzian Classification](https://www.tradingview.com/script/WhBzgfDu-Machine-Learning-Lorentzian-Classification/) | [jdehorty](https://www.tradingview.com/u/jdehorty/) | 2023-01-23 (upd. 2024-06-29) | MPL 2.0 |
  | [Nadaraya-Watson Trend [QuantAlgo]](https://www.tradingview.com/script/DyPTog1C-Nadaraya-Watson-Trend-QuantAlgo/) | [QuantAlgo](https://www.tradingview.com/u/QuantAlgo/) | 2026-07-09 | CC BY-NC-SA 4.0 |
  | [Indicator: WaveTrend Oscillator [WT]](https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/) | [LazyBear](https://www.tradingview.com/u/LazyBear/) | 2014-05-27 | none stated (TradingView House Rules) |
  | [Weis Wave Volume](https://www.tradingview.com/script/QrCFs0K2-Weis-Wave-Volume/) | [modhelius](https://www.tradingview.com/u/modhelius/) | 2018-06-13 (upd. 2024-02-09) | none stated (TradingView House Rules) |
  | [Squeeze Momentum Indicator [LazyBear]](https://www.tradingview.com/script/nqQ1DT5a-Squeeze-Momentum-Indicator-LazyBear/) | [LazyBear](https://www.tradingview.com/u/LazyBear/) | 2014-07-04 | none stated (TradingView House Rules) |

  Lorentzian Classification also imports jdehorty's `MLExtensions/2` and `KernelFunctions/2` libraries. Underlying
  concepts credited by the authors: John Carter's TTM Squeeze (*Mastering the Trade*, ch. 11) for Squeeze Momentum;
  David H. Weis, *Trades About to Happen* (Wiley, 2013), after R. D. Wyckoff, for Weis Wave Volume; the
  Nadaraya–Watson kernel regression estimator (Nadaraya 1964; Watson 1964).
- **Python libraries:** numpy, pandas, numba, scipy, backtesting.py (cross-check only), matplotlib — versions in
  `backtest/requirements.txt`.

- **Licence of this repository:** CC BY-NC-SA 4.0, as the Nadaraya-Watson adaptation requires. Portions derived
  from jdehorty's code stay under MPL 2.0, and third-party indicator code and market data keep their own terms.
  See `LICENSE`.

## 8. Integrity references

| Item | Value |
|---|---|
| Frozen config hash | `b8376d7d48f5` (run 17) |
| `FROZEN_PARAMS.json` SHA-256 | `B817CF9ACE0B46E9C6AE98CBA414FF557E552F0AD5357B0B76D474D461DCD5C1` |
| Data SHA-256 | `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f` |
| In-sample trials logged | 19 of 25 (plateau declared by critic after run 19) |
| Out-of-sample runs | exactly 1 (`backtest/results/OOS_FINAL/LOCK`) |
