# CRB Strategy — Python Backtest & Tuning Contract (SPEC)

Single source of truth for every agent working on this backtest. Strategy under test:
`../Combined Role-Based Strategy.pine` (Pine v6). Read it alongside this spec.

Interpreter: `backtest/.venv/Scripts/python.exe` (Python 3.13; numpy, pandas, numba, scipy, backtesting, pyarrow, pytest).
All paths below are relative to `C:/Course-Work/CIP-Project/backtest/`.

---------------------------------------------------------------------------------------------------
## 0. Periods and data-isolation rules (NON-NEGOTIABLE)

| Name | Bar open time (UTC), inclusive | Use |
|---|---|---|
| Warm-up | 2022-01-01 00:00 → 2022-12-31 23:00 | Indicator warm-up. Engine smoke tests may run here (DEV window 2022-04-01 → 2022-12-31). |
| In-Sample (IS) | 2023-01-01 00:00 → 2025-06-30 23:00 | The ONLY period used for tuning. |
| Out-of-Sample (OOS) | 2025-07-01 00:00 → last fully closed bar in data file | Run EXACTLY ONCE with frozen params. |

- IS runs must physically truncate the data frame to bars `<= 2025-06-30 23:00 UTC` BEFORE any indicator is computed.
- Nobody runs the strategy on IS or OOS dates except through `run_backtest.py is` (which logs every run) or `run_backtest.py oos` (once-only).
- Engine development/tests use synthetic data or the DEV window only, and must not print performance metrics
  (return/Sharpe/PF) for the DEV window — only "runs, N trades, runtime".
- Every IS invocation is a "parameter set tried" and counts against the hard cap of **25**.

Data file: `data/BTCUSDT_1h.csv` columns `time,open,high,low,close,volume` (time = bar OPEN time, UTC ISO8601),
source Binance spot `GET /api/v3/klines symbol=BTCUSDT interval=1h`, from 2022-01-01 00:00 UTC to the last fully
closed bar. Gaps are NOT filled (TradingView has no bars for missing hours either). `data/BTCUSDT_1h.meta.json`
records fetch time, rows, first/last bar, gap list, sha256.

---------------------------------------------------------------------------------------------------
## 1. Code layout

```
backtest/
  SPEC.md
  data/                    BTCUSDT_1h.csv, BTCUSDT_1h.meta.json, fetch_data.py
  engine/__init__.py
  engine/params.py         DEFAULTS dict (= Pine input defaults), BOUNDS, FIXED, validate(), config_hash()
  engine/pine_ta.py        Pine-faithful ta.* functions (numpy/numba)
  engine/mlext.py          jdehorty/MLExtensions/2 ports (n_rsi, n_wt, n_cci, n_adx, filters, normalize, rescale)
  engine/signals.py        compute_signals(df, params) -> DataFrame (Section 3)
  engine/broker.py         Pine broker emulator simulate(df, sig, params, window, costs) (Section 4)
  engine/metrics.py        compute_metrics(...) (Section 5)
  run_backtest.py          CLI (Section 6)
  log_tools.py             render / leaderboard / verify / best / freeze (Section 7)
  tests/                   pytest: ta parity, causality, broker, backtesting.py cross-check
  configs/run_NN.json      parameter sets (tuner writes)
  results/run_NN/          metrics.json, trades.csv, equity_daily.csv
  critic/run_NN.md         critic verdict (verbatim)
  logs/tuning_log.jsonl    machine log, one line per IS run (append-only)
  logs/tuning_log.md       human log (rendered from jsonl + critic files)
  logs/leaderboard.md      rendered
  FROZEN_PARAMS.json       written once by `log_tools.py freeze`
  results/OOS_FINAL/       written once by `run_backtest.py oos`
```

---------------------------------------------------------------------------------------------------
## 2. Parameters

Config JSON keys use the **exact Pine input variable names** (so the final Pine update maps 1:1).
`engine/params.py` holds `DEFAULTS` = every input default in the .pine file. A config file contains a
full or partial dict; it is merged over DEFAULTS; unknown keys or out-of-bounds values raise.
`config_hash` = sha256 of the canonical JSON (sorted keys) of the FULL merged dict, first 12 hex chars.

FIXED (not tunable; validate() rejects changes): `nwSrc=close, lcSource=close, lcRegimeSrc=ohlc4, wtSrc=hlc3,
sqzSrc=close, wtCciConst=0.015, lcIncludeFullHistory=false, wwvUseTrueRange='Auto'`, and strategy properties
initial_capital=10000, percent_of_equity=10, pyramiding=0, commission 0.075 %/side, slippage 2 ticks, mintick 0.01.

TUNABLE bounds (inclusive):
- Strategy: allowLongs, allowShorts: bool
- NW: nwKernelType ∈ {Gaussian, Epanechnikov, Triangular, Quartic, Cosine, Rational Quadratic}; nwLookback 10–300;
  nwBandwidth 1–50; nwHMult 0.5–5.0; nwRelWeight 0.25–25; nwSlopeLen 1–20; nwRequirePriceSide bool
- LC: lcNeighbors 4–30; lcMaxBarsBack 500–5000; lcHorizon 1–20; lcSpacing 2–10; lcDistQuantile 0.5–1.0;
  lcEntryWindow 0–10; lcFeatureCount 2–5; lcF{1..5}String ∈ {RSI, WT, CCI, ADX}; lcF{k}ParamA 2–50; lcF{k}ParamB 1–20;
  lcUseVolFilter bool; lcVolMinLen 1–10; lcVolMaxLen 2–50; lcUseRegimeFilter bool; lcRegimeThreshold −1.0–1.0;
  lcUseAdxFilter bool; lcAdxThreshold 5–50; lcAdxLen 5–50
- WT: wtN1 3–40; wtN2 5–60; wtSigLen 2–10; wtObLevel1 30–100; wtObLevel2 20–100; wtOsLevel1 −100–−30; wtOsLevel2 −100–−20;
  wtExtLevelSel ∈ {Level 1, Level 2}; wtTimingMode ∈ {Recent Cross + Not Overextended, Not Overextended Only}; wtCrossWindow 0–20
- WWV: wwvMethod ∈ {ATR, Traditional, Part of Price}; wwvMethodValue 1–2000; wwvPriceSource ∈ {Close, Open / Close, High / Low};
  wwvNormalize bool; wwvUseVolThreshold bool; wwvAvgLen 2–100; wwvAvgMult 0.1–3.0
- SQZ: sqzBbLen 5–60; sqzBbMult 0.5–4.0; sqzKcLen 5–60; sqzKcMult 0.5–4.0; sqzUseTrueRange bool; sqzReplicateQuirk bool;
  sqzRegimeMode ∈ {Squeeze Off, Not In Squeeze, Released Within Window}; sqzReleaseWindow 1–50; sqzRequireMomExpansion bool
- Exit: exitMode ∈ {LC Signal Flip, LC Fixed Hold, Either (LC Default)}; exitHoldBars 1–96; riskUseSl bool; riskUseTp bool;
  riskAtrLen 2–50; riskSlMult 0.5–8.0; riskTpMult 0.5–12.0
Integer inputs must be ints; float inputs floats.

---------------------------------------------------------------------------------------------------
## 3. Signals (engine/signals.py) — faithful Pine port, position-independent

`compute_signals(df, p) -> pd.DataFrame` (same index as df) with REQUIRED columns:
`long_cond, short_cond, lc_new_buy, lc_new_sell` (bool) and `risk_atr` (float),
plus audit columns `regime_gate, trend_long, trend_short, entry_long, entry_short, timing_long, timing_short,
confirm_long, confirm_short, lc_prediction, lc_signal, nw_trend, wt1, wt2, wwv_direction, sqz_val`.

Historical bars are confirmed, so `barConfirmed` = True. All signals are pure functions of bars `<= t`.

### 3.1 Pine semantics to replicate
- Comparisons with na are false; bool results are never na. `nz(x)` = 0 when na.
- `ta.sma` na until `len` values. `ta.ema` α=2/(len+1), `ta.rma` α=1/len; both seeded with the SMA of the first
  `len` non-na values, na before. `ta.stdev` = population std (ddof=0). `ta.dev` = mean |x − sma|.
- `ta.rsi(x,n)`: u=max(x−x[1],0), d=max(x[1]−x,0), rs=rma(u)/rma(d), rsi=100−100/(1+rs); rma(d)==0 → 100; rma(u)==0 → 0.
- `ta.cci(x,n) = (x − sma(x,n)) / (0.015 · dev(x,n))`.
- `ta.tr` (variable, handle_na=false): na on bar 0, else max(h−l, |h−c[1]|, |l−c[1]|). `ta.atr(n) = rma(tr(true), n)`
  where tr(true) on bar 0 = h−l.
- `ta.linreg(x,n,0)`: OLS fit over last n values with x-coordinates 0..n−1 (current bar = n−1); value = intercept + slope·(n−1).
- `ta.highest/lowest(x,n)` rolling over n bars incl. current. `ta.crossover(a,b)`: a>b and a[1]<=b[1].
  `ta.barssince(c)`: bars since last true (0 if true now), na if never. `ta.valuewhen(c, bar_index, 0)`: last bar_index where c, na if never.
- `math.round` = floor(x+0.5). `bar_index` = row position from data start (2022-01-01 00:00).

### 3.2 MLExtensions v2 (engine/mlext.py)
```
normalize(src, min, max): var hMin=10e10, hMax=-10e10 (persistent from data start)
    hMin := min(nz(src,hMin),hMin); hMax := max(nz(src,hMax),hMax)
    return min + (max-min)*(src-hMin)/max(hMax-hMin, 10e-10)          # na if src na
rescale(src,oMin,oMax,nMin,nMax) = nMin + (nMax-nMin)*(src-oMin)/max(oMax-oMin,10e-10)
n_rsi(src,n1,n2) = rescale(ema(rsi(src,n1),n2), 0,100, 0,1)
n_cci(src,n1,n2) = normalize(ema(cci(src,n1),n2), 0,1)
n_wt(src,n1,n2):  e1=ema(src,n1); e2=ema(|src-e1|,n1); ci=(src-e1)/(0.015*e2); w1=ema(ci,n2); w2=sma(w1,4); normalize(w1-w2,0,1)
n_adx(h,l,c,n):   tr=max(h-l, |h-nz(c[1])|, |l-nz(c[1])|)
                  dmp = (h-nz(h[1]) > nz(l[1])-l) ? max(h-nz(h[1]),0) : 0
                  dmm = (nz(l[1])-l > h-nz(h[1])) ? max(nz(l[1])-l,0) : 0
                  trS := nz(trS[1]) - nz(trS[1])/n + tr ; same Wilder-sum for dmpS, dmmS
                  diP=dmpS/trS*100; diM=dmmS/trS*100; dx=|diP-diM|/(diP+diM)*100; adx=rma(dx,n); rescale(adx,0,100,0,1)
filter_volatility(minLen,maxLen,use) = use ? atr(minLen) > atr(maxLen) : true
regime_filter(src=ohlc4, thr, use):
    v1 := 0.2*(src-src[1]) + 0.8*nz(v1[1]);  v2 := 0.1*(high-low) + 0.8*nz(v2[1])
    omega=|v1/v2|; alpha=(-omega^2 + sqrt(omega^4 + 16*omega^2))/8; klmf := alpha*src + (1-alpha)*nz(klmf[1])
    s=|klmf-klmf[1]|; e=ema(s,200); nsd=(s-e)/e; use ? nsd >= thr : true
filter_adx(src,len,thr,use): same ADX construction as n_adx (on high/low/close, unscaled 0..100); use ? adx > thr : true
```
Features: `lcF{k}String` → RSI: n_rsi(close,A,B); WT: n_wt(hlc3,A,B); CCI: n_cci(close,A,B); ADX: n_adx(high,low,close,A).

### 3.3 Components (see .pine for exact expressions)
- NW: h = nwBandwidth·nwHMult; w(i) kernel of distance i for i=0..nwLookback (inclusive); NW = Σw·src[t−i]/Σw (na if any
  src[t−i] na). Kernels exactly as `nwKernelWeight`. trendLong = NW>NW[k] and (not requireSide or src>NW); short mirrored.
- LC training label (as-is): `y[t] = src[t−H] < src[t] ? −1 : src[t−H] > src[t] ? +1 : 0` (0 when src[t−H] na).
- **LC nearest-neighbour search — DEVIATION D1 (causal rolling window).** The Pine anchors the window on `last_bar_index`
  (non-causal; on TradingView it only produces predictions on the final maxBarsBack bars of the chart). The backtest uses
  the source's stated intent — search the most recent maxBarsBack bars — evaluated causally at every bar:
  ```
  predictions=[], distances=[]  # persistent across bars (Pine `var`), never cleared
  prediction=0.0
  for t in 0..n-1:
      lastD = -1.0
      if t >= M:                                   # M = lcMaxBarsBack
          for i in (t-M) .. (t-1) ascending:       # excludes current bar
              d = Σ_{k<featureCount} log(1+|f_k[t]-f_k[i]|)      # NaN -> comparison false
              if d >= lastD and i % lcSpacing != 0:
                  lastD = d; distances.append(d); predictions.append(y[i])
                  if len(predictions) > K:
                      lastD = distances[floor(K*lcDistQuantile + 0.5)]
                      distances.pop(0); predictions.pop(0)
          prediction = sum(predictions)
      lc_prediction[t] = prediction
  ```
  Implement with numba (@njit(cache=True)); use a ring buffer or index arithmetic, not Python lists.
- LC state: `sig[t] = (pred>0 and filterAll) ? 1 : (pred<0 and filterAll) ? −1 : sig[t−1]` (sig[−1]=0);
  changed = sig[t]≠sig[t−1] (False on bar 0); newBuy = sig==1 and changed; newSell = sig==−1 and changed.
  longFlipBar = valuewhen(newBuy, t); inWindow = flipBar not na and t−flipBar <= lcEntryWindow;
  fresh = usedLongFlipBar is na or longFlipBar ≠ usedLongFlipBar (evaluated BEFORE this bar's update);
  entryLong = sig==1 and inWindow and fresh. After computing longCondition at t: if longCondition → usedLongFlipBar = longFlipBar.
  Short mirrored with its own used-bar state. (This bookkeeping does not depend on position, so it lives here.)
- WT timing, WWV confirmation (recursive series: wwvCurrClose, wwvDirection, wwvBarCount, wwvVol use their own
  previous-bar FINAL values), SQZ regime gate: port the Pine expressions literally.
- `long_cond = allowLongs and regimeGate and trendLong and entryLong and timingLong and confirmLong`; short mirrored.
- `risk_atr = ta.atr(riskAtrLen)`.

Performance target: one full compute on 2022-01-01→2025-06-30 (~30.6k bars) in < 10 s after numba compile.

---------------------------------------------------------------------------------------------------
## 4. Broker emulator (engine/broker.py) — TradingView strategy semantics

`simulate(df, sig, p, window_start, window_end, costs) -> (trades_df, equity_series, info)`
`costs = {"commission_pct": 0.075, "slip_mode": "ticks", "slip_value": 2, "mintick": 0.01}` (base) or
`{"commission_pct": 0.10, "slip_mode": "bps", "slip_value": 5}` (stress). Slippage is adverse on market and stop fills,
none on limit fills. Commission = pct/100 · fill_price · qty on every fill.

Per bar t, in this order:
1. **Open**: fill market orders queued at close of t−1 at `open[t]` ± slippage.
   - Entry Long from flat: buy q. Entry Long while short: one buy of |pos|+q (closes short, opens long). Short mirrored.
   - Close order (strategy.close): close the whole position if it still exists.
   - A new position's `entry_bar = t`.
2. **Intrabar**: if a position exists and its risk exit order is active (placed at a prior close, see step 3),
   check stop (long: low<=S; short: high>=S) and limit (long: high>=L; short: low<=L).
   Price path: if (high−open) <= (open−low) → O→H→L→C, else O→L→H→C. First level touched on that path fills.
   Gap rule: if open already beyond the level, fill at open (stop: open±slippage; limit: open).
3. **Close** (strategy logic at bar t, using position state after steps 1–2):
   - mark-to-market equity E = cash + pos·close[t]
   - inLong = pos>0, inShort = pos<0; barsFromEntry = t − entry_bar + 1 if position else 0; holdExpired = barsFromEntry >= exitHoldBars
   - exitLongRaw: 'LC Signal Flip' → lc_new_sell; 'LC Fixed Hold' → holdExpired; 'Either (LC Default)' → lc_new_sell or holdExpired (short mirrored with lc_new_buy)
   - longExit = inLong and exitLongRaw and not short_cond; shortExit mirrored with long_cond
   - entries allowed only if window_start <= time[t] <= window_end:
     if long_cond and not inLong and risk_atr not na: longStop = close−atr·slMult; longTp = close+atr·tpMult;
        queue Entry Long with q = 0.10·E/close[t]
     if short_cond and not inShort and risk_atr not na: mirrored
   - if longExit: queue Close Long; if shortExit: queue Close Short
   - risk orders (only if riskUseSl or riskUseTp): the long risk order is active for bar t+1 iff (inLong or long_cond-entry-queued)
     and longStop not na; otherwise cancelled. Stop uses longStop if riskUseSl; limit uses longTp if riskUseTp. Short mirrored.
     Levels persist until the next fresh entry sets them.
4. At the LAST bar of the window (or of the data), after step 3's mark-to-market, force-close any open position at close[t]
   (with slippage + commission), exit reason 'WindowEnd'; discard queued orders.
Exit reasons: 'LC Exit', 'SL', 'TP', 'Reverse', 'WindowEnd'.
Trade record: direction, entry_time, entry_price, exit_time, exit_price, qty, pnl (net of both commissions), return_pct
(pnl / entry notional), bars_held, exit_reason. Equity series = mark-to-market at every bar close within the window.

---------------------------------------------------------------------------------------------------
## 5. Metrics (engine/metrics.py) — pre-registered definitions

On the window's equity: daily equity = last bar-close equity per UTC day; daily simple returns r.
- net_return_pct, CAGR (365.25-day year), ann_vol = std(r,ddof=1)·√365
- **sharpe = mean(r)/std(r,ddof=1)·√365** (rf=0), sortino = mean(r)/sqrt(mean(min(r,0)²))·√365
- max_dd_pct (on bar-close equity), max_dd_duration_days, calmar = CAGR/|max_dd|
- trades, win_rate, profit_factor (gross win / gross loss, net pnl), avg_trade_return_pct, median, avg_win/avg_loss,
  payoff_ratio, expectancy_usd, avg_bars_held, max_consecutive_losses, exposure_pct (bars in position / window bars),
  long/short trade counts and PF, exit_reason counts, trade_tstat = mean(ret)/std(ret)·√n
- psr0 = Φ( SR_d·√(T−1) / √(1 − skew·SR_d + (kurt−1)/4·SR_d²) ) with daily SR_d, T days, kurt = non-excess
- skew, kurtosis of daily returns; sharpe_daily (non-annualised), n_days
- subperiods {2023, 2024, 2025H1 (IS) | OOS: 2025H2, 2026YTD}: net_return_pct, sharpe, trades (by entry), profit_factor
- buy_and_hold over the window (100 % BTC, no costs): net_return_pct, sharpe, max_dd_pct
- stress (costs = stress set): net_return_pct, sharpe, profit_factor, trades
- gates (IS only), see Section 8.

---------------------------------------------------------------------------------------------------
## 6. run_backtest.py CLI

- `run_backtest.py is --config configs/run_NN.json`
  guards: NN must equal (#lines in logs/tuning_log.jsonl)+1; NN <= 25; config_hash not already logged;
  params validate; data truncated to <= 2025-06-30 23:00 before computing. Computes base + stress simulations,
  metrics, gates; writes results/run_NN/{metrics.json,trades.csv,equity_daily.csv}; appends one JSON line to
  logs/tuning_log.jsonl {run_id, utc_timestamp, config_hash, params_full, params_diff_vs_defaults, metrics(summary),
  gates, eligible, runtime_s, data_sha256}; runs `log_tools.py render`; prints a compact summary.
  A run that crashes before metrics does not consume a slot (nothing is logged); fix the engine and rerun the same NN.
- `run_backtest.py oos --frozen FROZEN_PARAMS.json`
  guards: results/OOS_FINAL/LOCK must not exist; FROZEN_PARAMS.json hash must match its embedded hash. Writes LOCK
  first, computes on the full continuous series (indicators warm from 2022), entries only in the OOS window, writes
  results/OOS_FINAL/{metrics.json,trades.csv,equity_daily.csv}; never re-runnable.
- `run_backtest.py smoke` — defaults on DEV window; prints only trade count and runtime. Not logged.

---------------------------------------------------------------------------------------------------
## 7. log_tools.py

- `render`: regenerate logs/tuning_log.md (per-run: params diff vs defaults, full exact metrics table, gates, critic verdict
  from critic/run_NN.md if present) and logs/leaderboard.md (all runs sorted by sharpe, eligible flag, best-so-far marker,
  DSR of the current best).
- `verify`: integrity — every jsonl line has results dir + config file whose merged hash matches; run ids 1..N contiguous;
  N <= 25; no duplicate hashes; prints OK/errors.
- `best`: apply Section 8 rule, print run id + params.
- `freeze`: write FROZEN_PARAMS.json {run_id, config_hash, params_full, frozen_utc, selection_rule, is_metrics} once; refuse if exists.
- DSR (Bailey & López de Prado 2014): N = #trials logged, V = var of sharpe_daily across trials (ddof=1),
  SR0 = √V · ((1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e))), γ = 0.5772156649;
  DSR = Φ( (SR*−SR0)·√(T−1) / √(1 − skew·SR* + (kurt−1)/4·SR*²) ) using the best trial's daily stats.

---------------------------------------------------------------------------------------------------
## 8. Pre-registered selection rule (fixed before run 01; do not change)

Eligible run = all gates pass:
- G1 trades >= 100
- G2 profit_factor > 1.0
- G3 stress.net_return_pct > 0
- G4 at least 2 of the 3 IS sub-periods (2023, 2024, 2025H1) have net_return_pct > 0
**Best = eligible run with the highest IS `sharpe`** (ties → higher trades).
Fallback (only if no run is eligible): highest sharpe among runs with trades >= 30, flagged "FAILED PRE-REGISTERED GATES".

## 9. Loop protocol
Run 01 = Pine defaults (baseline). Each iteration: tuner proposes configs/run_NN.json → executor runs `is` →
critic (adversary) reviews metrics + full log and returns VERDICT: CONTINUE | PLATEAU → tracker saves critic/run_NN.md,
renders and verifies logs. Stop when critic says PLATEAU or run 25 is logged. Then `freeze`, then `oos` exactly once.
