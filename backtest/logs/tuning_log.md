# CRB Strategy - IS tuning log

Rendered 2026-09-13T20:01:50Z from `logs/tuning_log.jsonl` (19 / 25 runs) and `critic/run_NN.md`.
Do not edit by hand; run `python log_tools.py render`.

Pre-registered selection rule: Eligible = G1 trades>=100, G2 profit_factor>1.0, G3 stress.net_return_pct>0, G4 >=2 of 3 IS sub-periods (2023, 2024, 2025H1) net_return_pct>0. Best = eligible run with highest IS sharpe (ties -> more trades). Fallback if none eligible: highest sharpe among runs with trades>=30, flagged 'FAILED PRE-REGISTERED GATES'.

## Run 01

- run id: `run_01`
- timestamp (UTC): `2026-09-13T16:54:43Z`
- config hash: `ee67637fc13d`
- eligible: **NO**
- runtime_s: `2.2307731000037165`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

_none (Pine defaults)_

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 4,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 8,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": false,
 "nwSlopeLen": 1,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": false,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Recent Cross + Not Overextended",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `117` | PASS |
| G2 | profit_factor > 1.0 | `0.5192712846329246` | FAIL |
| G3 | stress.net_return_pct > 0 | `-5.1871695817496954` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `0` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9649.252115755207` |
| `net_return_pct` | `-3.507478842447931` |
| `cagr_pct` | `-1.419773795364243` |
| `ann_vol_pct` | `0.8346084807281866` |
| `sharpe` | `-1.7079410143786595` |
| `sortino` | `-2.102856702841333` |
| `max_dd_pct` | `4.199679826767843` |
| `max_dd_duration_days` | `900.9583333333334` |
| `calmar` | `-0.33806715128970416` |
| `sharpe_daily` | `-0.08939771852987866` |
| `skew` | `-1.0402950868544738` |
| `kurtosis` | `23.648353303515538` |
| `n_days` | `912` |
| `psr0` | `0.002845321093327074` |
| `trades` | `117` |
| `win_rate_pct` | `36.75213675213676` |
| `profit_factor` | `0.5192712846329246` |
| `gross_profit_usd` | `378.8692013020248` |
| `gross_loss_usd` | `729.6170855468145` |
| `net_pnl_usd` | `-350.7478842447897` |
| `avg_trade_return_pct` | `-0.3043815212037567` |
| `median_trade_return_pct` | `-0.35232166795220726` |
| `avg_win_pct` | `0.8967979448716241` |
| `avg_loss_pct` | `-1.0023641839232347` |
| `avg_win_usd` | `8.810911658186624` |
| `avg_loss_usd` | `-9.859690345227222` |
| `expectancy_usd` | `-2.997845164485382` |
| `avg_bars_held` | `3.4615384615384617` |
| `max_consecutive_losses` | `9` |
| `payoff_ratio` | `0.893629652624103` |
| `trade_tstat` | `-2.6937458930933564` |
| `win_rate_ci95_low_pct` | `28.566809393867317` |
| `win_rate_ci95_high_pct` | `45.77974326899144` |
| `long_trades` | `51` |
| `long_profit_factor` | `0.7522733038241952` |
| `long_net_pnl_usd` | `-74.62632783216009` |
| `short_trades` | `66` |
| `short_profit_factor` | `0.3554171628843663` |
| `short_net_pnl_usd` | `-276.1215564126296` |
| `exit_reasons.LC Exit` | `90` |
| `exit_reasons.SL` | `27` |
| `exit_reasons.TP` | `0` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `405` |
| `exposure_pct` | `1.8504134874583085` |
| `subperiods.2023.net_return_pct` | `-1.4775379384048049` |
| `subperiods.2023.sharpe` | `-1.7341628506978937` |
| `subperiods.2023.trades` | `38` |
| `subperiods.2023.profit_factor` | `0.47572655289604543` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `-0.9125064086922929` |
| `subperiods.2024.sharpe` | `-1.0964872459879205` |
| `subperiods.2024.trades` | `49` |
| `subperiods.2024.profit_factor` | `0.6631415541670174` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.1584483640815102` |
| `subperiods.2025H1.sharpe` | `-2.9330245494095633` |
| `subperiods.2025H1.trades` | `30` |
| `subperiods.2025H1.profit_factor` | `0.37486107602379665` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-5.1871695817496954` |
| `stress.sharpe` | `-2.4536048475348493` |
| `stress.profit_factor` | `0.38066762657813574` |
| `stress.trades` | `117` |
| `stress.max_dd_pct` | `5.789764945999409` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2307731000037165` |
| `signals_runtime_s` | `2.1594246000022395` |

### Critic verdict

﻿RUN: 01
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -1.71 / Sortino -2.10 / Calmar -0.34 vs buy-and-hold Sharpe +1.79 on the identical window; PSR0 = 0.0028 (~0.3% probability the true Sharpe is even positive). FAIL.
- Drawdown: max_dd 4.20% at 10%-of-equity sizing (≈42% scaled to full exposure), duration 901 days (near the entire 2.5y IS window), skew -1.04, kurtosis 23.65, 9 max consecutive losses — fat-tailed, unrecovered. FAIL.
- Significance: 117 trades clears G1 (>=100) but trade t-stat = -2.69 (statistically significant negative edge, not noise); win rate 36.75%, 95% CI [28.6%, 45.8%] — entire CI sits below the ~52.9% breakeven win rate implied by payoff ratio 0.89. FAIL, and this is a real signal, not a sampling artifact.
- Robustness: all 3 sub-periods negative (2023 -1.48%, 2024 -0.91%, 2025H1 -1.16%, G4 = 0/3); short trades (66, PF 0.36, -\ net) are the dominant bleed vs longs (51, PF 0.75, -\ net) while B&H returned +548% — shorting into the strongest leg of a bull market. Stress costs push it further negative (net -5.19%, Sharpe -2.45). FAIL.
- Costs: round-trip commission ~0.15% + 2-tick slippage is immaterial in $ terms at $17k- BTC prices (fixed, not tunable) — costs are not the cause of the loss; avg trade -0.30% is explained by the win-rate/payoff gap, not fee drag. TP never fires (riskUseTp=false, 0 TP exits in exit_reasons).

WEAKNESSES:
- Exit mix is timer-dominated, not signal-dominated: of 90 "LC Exit" trades essentially all show bars_held=4 (avg_bars_held=3.46 overall), meaning `exitHoldBars`=4 is doing almost all the work and LC's own signal-flip logic rarely fires first inside the window — the "Either (LC Default)" mode is functionally a fixed 4-bar exit with an SL overlay.
- Payoff ratio 0.89 (avg win 0.897% vs avg loss -1.002%) is inverted relative to the 36.75% win rate (expectancy -$3.00/trade, -0.304% avg) — both entry selection and exit/risk design contribute to negative expectancy.
- Short side is the structural problem: 66 short trades, PF 0.36, -$276 net vs 51 longs, PF 0.75, -$75 net, against a +548% B&H bull run — this looks like fighting trend/beta, not a fine-tuning issue.
- Exposure only 1.85% (405/21887 bars) — equity curve is flat >98% of the time punctuated by sharp SL losses; annualized Sharpe/Sortino are being set by a handful of tail days (skew -1.04, kurtosis 23.65).
- TP disabled and never used (riskUseTp=false, TP:0 exits) — winners are only ever capped by the 4-bar timer while the 2×ATR stop (SL: 27 trades) realizes losses (~-1.0% to -2.9%) larger than average wins, an asymmetric-risk/no-asymmetric-reward design.
- All 3 IS sub-periods negative — G4 fails 0/3 (needed 2/3), so this is a persistent negative edge across the whole IS window, not one bad year.

DEMANDS FOR NEXT CONFIG (priority order):
1. Isolate the short-side drag: run `allowShorts=false` (long-only) as a structured Strategy-Controls probe to quantify how much of -3.51% net / -1.71 Sharpe is short-side beta-fighting vs a genuine long-side entry problem.
2. Fix the payoff asymmetry: set `riskUseTp=true` (riskTpMult already 3.0, in-bounds 0.5-12.0) so winners get a defined target instead of only the 4-bar timer; and/or raise `exitHoldBars` from 4 toward 8-12 (bounds 1-96) to let winners develop, since the timer currently pre-empts the LC flip almost every trade.
3. Re-tune the stop: `riskSlMult` (currently 2.0, bounds 0.5-8.0) is producing SL losses bigger than average wins — test 2.5-3.0 paired with the TP change so risk stays bounded but stops aren't firing on normal 1H BTC noise.
4. Strengthen trend/regime quality rather than just quantity: `nwSlopeLen=1` is a single-bar (very noisy) slope — test 3-5 (bounds 1-20) with `nwRequirePriceSide=true`; test `sqzRegimeMode='Released Within Window'` vs current 'Squeeze Off' to time entries nearer volatility expansion.
5. Lower priority: test `wtTimingMode='Not Overextended Only'` — with only 1.85% exposure, the 5-filter AND funnel may be over-pruning rather than adding orthogonal edge.
Do not spend budget on costs/sizing — they are fixed and not the loss driver here.

PLATEAU ASSESSMENT: No eligible run yet (0/1; run 01 fails G2, G3, G4). Best-by-fallback sharpe = -1.7079 (run 01, FAILED PRE-REGISTERED GATES). Runs since improvement: N/A (first run). Untested levers: every role (trend NW, entry LC, timing WT, confirmation WWV, regime SQZ, exits/risk) and long/short permission remain unprobed beyond Pine defaults. Far too early for PLATEAU — only 1/25 runs used, and the failure mode is clearly diagnosable (timer-dominated exits, inverted payoff ratio, short-side beta drag) with concrete untested levers remaining.

---

## Run 02

- run id: `run_02`
- timestamp (UTC): `2026-09-13T17:01:33Z`
- config hash: `b1b9e101a273`
- eligible: **NO**
- runtime_s: `6.096796199999517`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `riskUseTp` | `true` | `false` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 8,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": false,
 "nwSlopeLen": 1,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Recent Cross + Not Overextended",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `117` | PASS |
| G2 | profit_factor > 1.0 | `0.7869231511367754` | FAIL |
| G3 | stress.net_return_pct > 0 | `-3.399938237383171` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9815.839832048574` |
| `net_return_pct` | `-1.8416016795142598` |
| `cagr_pct` | `-0.7416612842275017` |
| `ann_vol_pct` | `1.1074389069397812` |
| `sharpe` | `-0.6662042395423485` |
| `sortino` | `-0.8772959077534216` |
| `max_dd_pct` | `2.212460468579591` |
| `max_dd_duration_days` | `887.0833333333334` |
| `calmar` | `-0.3352201292453606` |
| `sharpe_daily` | `-0.03487072363074865` |
| `skew` | `-0.8998687208635417` |
| `kurtosis` | `25.290853440138022` |
| `n_days` | `912` |
| `psr0` | `0.1433577972773833` |
| `trades` | `117` |
| `win_rate_pct` | `44.44444444444444` |
| `profit_factor` | `0.7869231511367754` |
| `gross_profit_usd` | `680.1297299606679` |
| `gross_loss_usd` | `864.2898979120953` |
| `net_pnl_usd` | `-184.1601679514274` |
| `avg_trade_return_pct` | `-0.15765020516599457` |
| `median_trade_return_pct` | `-0.4059088517887931` |
| `avg_win_pct` | `1.322997793104707` |
| `avg_loss_pct` | `-1.342168603782556` |
| `avg_win_usd` | `13.079417883858998` |
| `avg_loss_usd` | `-13.296767660186081` |
| `expectancy_usd` | `-1.5740185294993796` |
| `avg_bars_held` | `6.948717948717949` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `0.9836539389209692` |
| `trade_tstat` | `-1.0921445220696666` |
| `win_rate_ci95_low_pct` | `35.75972219792095` |
| `win_rate_ci95_high_pct` | `53.48238053166497` |
| `long_trades` | `51` |
| `long_profit_factor` | `0.7976445736751149` |
| `long_net_pnl_usd` | `-75.00439099958425` |
| `short_trades` | `66` |
| `short_profit_factor` | `0.7788727064241076` |
| `short_net_pnl_usd` | `-109.1557769518432` |
| `exit_reasons.LC Exit` | `42` |
| `exit_reasons.SL` | `43` |
| `exit_reasons.TP` | `31` |
| `exit_reasons.Reverse` | `1` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `813` |
| `exposure_pct` | `3.7145337414903827` |
| `subperiods.2023.net_return_pct` | `-1.4352537179632363` |
| `subperiods.2023.sharpe` | `-1.5523196162865238` |
| `subperiods.2023.trades` | `38` |
| `subperiods.2023.profit_factor` | `0.5359428457776861` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.1090879728826275` |
| `subperiods.2024.sharpe` | `0.9173354738236682` |
| `subperiods.2024.trades` | `49` |
| `subperiods.2024.profit_factor` | `1.352766593748107` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.5046649256018285` |
| `subperiods.2025H1.sharpe` | `-2.5129543857623835` |
| `subperiods.2025H1.trades` | `30` |
| `subperiods.2025H1.profit_factor` | `0.3882549811055944` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-3.399938237383171` |
| `stress.sharpe` | `-1.2115745387054955` |
| `stress.profit_factor` | `0.6441242525597978` |
| `stress.trades` | `117` |
| `stress.max_dd_pct` | `3.6807414725215315` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `6.096796199999517` |
| `signals_runtime_s` | `5.972248200007016` |

### Critic verdict

﻿RUN: 02
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

---

## Run 03

- run id: `run_03`
- timestamp (UTC): `2026-09-13T17:04:44Z`
- config hash: `a123711fe7f1`
- eligible: **NO**
- runtime_s: `2.190488099993672`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `riskSlMult` | `3.0` | `2.0` |
| `riskUseTp` | `true` | `false` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 8,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": false,
 "nwSlopeLen": 1,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 3.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Recent Cross + Not Overextended",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `117` | PASS |
| G2 | profit_factor > 1.0 | `0.7474716805696617` | FAIL |
| G3 | stress.net_return_pct > 0 | `-3.886770390506167` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9765.860876888612` |
| `net_return_pct` | `-2.3413912311138874` |
| `cagr_pct` | `-0.9443764468251237` |
| `ann_vol_pct` | `1.1789928881744276` |
| `sharpe` | `-0.7983556468300298` |
| `sortino` | `-1.0115620886472962` |
| `max_dd_pct` | `2.8673186128454042` |
| `max_dd_duration_days` | `887.0833333333334` |
| `calmar` | `-0.3293587404602954` |
| `sharpe_daily` | `-0.041787844428582153` |
| `skew` | `-1.3451480394992896` |
| `kurtosis` | `21.933098763322302` |
| `n_days` | `912` |
| `psr0` | `0.09816997820570506` |
| `trades` | `117` |
| `win_rate_pct` | `47.008547008547005` |
| `profit_factor` | `0.7474716805696617` |
| `gross_profit_usd` | `693.0405438644647` |
| `gross_loss_usd` | `927.179666975859` |
| `net_pnl_usd` | `-234.1391231113945` |
| `avg_trade_return_pct` | `-0.20100891735851484` |
| `median_trade_return_pct` | `-0.3080788627101905` |
| `avg_win_pct` | `1.2785770605183553` |
| `avg_loss_pct` | `-1.5135448654750934` |
| `avg_win_usd` | `12.600737161172084` |
| `avg_loss_usd` | `-14.954510757675147` |
| `expectancy_usd` | `-2.0011890864221753` |
| `avg_bars_held` | `8.316239316239317` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `0.8426044399148913` |
| `trade_tstat` | `-1.2630594274887295` |
| `win_rate_ci95_low_pct` | `38.20433508650713` |
| `win_rate_ci95_high_pct` | `56.00295099865453` |
| `long_trades` | `51` |
| `long_profit_factor` | `0.7067513206582587` |
| `long_net_pnl_usd` | `-122.24680555136672` |
| `short_trades` | `66` |
| `short_profit_factor` | `0.7807360986429468` |
| `short_net_pnl_usd` | `-111.89231756002785` |
| `exit_reasons.LC Exit` | `62` |
| `exit_reasons.SL` | `21` |
| `exit_reasons.TP` | `32` |
| `exit_reasons.Reverse` | `2` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `973` |
| `exposure_pct` | `4.445561292091195` |
| `subperiods.2023.net_return_pct` | `-1.4035337371610668` |
| `subperiods.2023.sharpe` | `-1.4891801411513683` |
| `subperiods.2023.trades` | `38` |
| `subperiods.2023.profit_factor` | `0.5448394119974601` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `0.3593233531554274` |
| `subperiods.2024.sharpe` | `0.265724404317703` |
| `subperiods.2024.trades` | `49` |
| `subperiods.2024.profit_factor` | `1.0915262510096138` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.3058391874162911` |
| `subperiods.2025H1.sharpe` | `-2.2897718657175803` |
| `subperiods.2025H1.trades` | `30` |
| `subperiods.2025H1.profit_factor` | `0.4424173308493719` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-3.886770390506167` |
| `stress.sharpe` | `-1.3116232216304882` |
| `stress.profit_factor` | `0.6163711877914059` |
| `stress.trades` | `117` |
| `stress.max_dd_pct` | `4.282465438677951` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.190488099993672` |
| `signals_runtime_s` | `2.122908199991798` |

### Critic verdict

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

---

## Run 04

- run id: `run_04`
- timestamp (UTC): `2026-09-13T17:06:47Z`
- config hash: `cc0394cf905e`
- eligible: **NO**
- runtime_s: `2.1956702999887057`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 8,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Recent Cross + Not Overextended",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `108` | PASS |
| G2 | profit_factor > 1.0 | `0.9589547935292594` | FAIL |
| G3 | stress.net_return_pct > 0 | `-1.7452271798894303` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9970.485875006205` |
| `net_return_pct` | `-0.2951412499379469` |
| `cagr_pct` | `-0.11830686665770251` |
| `ann_vol_pct` | `1.0168726186490835` |
| `sharpe` | `-0.1112549622537207` |
| `sortino` | `-0.1608035823585615` |
| `max_dd_pct` | `1.8838346745177814` |
| `max_dd_duration_days` | `447.625` |
| `calmar` | `-0.06280108772707794` |
| `sharpe_daily` | `-0.005823350875046865` |
| `skew` | `0.517920307739309` |
| `kurtosis` | `21.59641875859833` |
| `n_days` | `912` |
| `psr0` | `0.43034921297895423` |
| `trades` | `108` |
| `win_rate_pct` | `44.44444444444444` |
| `profit_factor` | `0.9589547935292594` |
| `gross_profit_usd` | `689.5497446162587` |
| `gross_loss_usd` | `719.0638696100531` |
| `net_pnl_usd` | `-29.514124993794486` |
| `avg_trade_return_pct` | `-0.02615556078854393` |
| `median_trade_return_pct` | `-0.3044337317353165` |
| `avg_win_pct` | `1.4401552453853201` |
| `avg_loss_pct` | `-1.1992042057276353` |
| `avg_win_usd` | `14.365619679505391` |
| `avg_loss_usd` | `-11.984397826834218` |
| `expectancy_usd` | `-0.2732789351277267` |
| `avg_bars_held` | `7.0092592592592595` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `1.1986934919115741` |
| `trade_tstat` | `-0.17376456832919054` |
| `win_rate_ci95_low_pct` | `35.424144424466085` |
| `win_rate_ci95_high_pct` | `53.84638179494009` |
| `long_trades` | `48` |
| `long_profit_factor` | `0.9101931155574774` |
| `long_net_pnl_usd` | `-28.908713540799923` |
| `short_trades` | `60` |
| `short_profit_factor` | `0.9984756685614345` |
| `short_net_pnl_usd` | `-0.6054114529945411` |
| `exit_reasons.LC Exit` | `40` |
| `exit_reasons.SL` | `37` |
| `exit_reasons.TP` | `31` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `757` |
| `exposure_pct` | `3.4586740987800977` |
| `subperiods.2023.net_return_pct` | `-0.9546859768427396` |
| `subperiods.2023.sharpe` | `-1.2089330234690452` |
| `subperiods.2023.trades` | `35` |
| `subperiods.2023.profit_factor` | `0.5990437836775513` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.985342086022568` |
| `subperiods.2024.sharpe` | `1.6240426078689931` |
| `subperiods.2024.trades` | `44` |
| `subperiods.2024.profit_factor` | `1.76817692971504` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.2937546309273795` |
| `subperiods.2025H1.sharpe` | `-2.6954035061498702` |
| `subperiods.2025H1.trades` | `29` |
| `subperiods.2025H1.profit_factor` | `0.41913002517809206` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-1.7452271798894303` |
| `stress.sharpe` | `-0.6734127110491492` |
| `stress.profit_factor` | `0.7833534333890259` |
| `stress.trades` | `108` |
| `stress.max_dd_pct` | `2.2663533316829354` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.1956702999887057` |
| `signals_runtime_s` | `2.1275859999877866` |

### Critic verdict

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

---

## Run 05

- run id: `run_05`
- timestamp (UTC): `2026-09-13T17:10:14Z`
- config hash: `fb53615c781d`
- eligible: **NO**
- runtime_s: `2.2281172000075458`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 8,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `191` | PASS |
| G2 | profit_factor > 1.0 | `0.9841489927035095` | FAIL |
| G3 | stress.net_return_pct > 0 | `-2.7378821916518192` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9981.355808213213` |
| `net_return_pct` | `-0.18644191786787445` |
| `cagr_pct` | `-0.07471053286215446` |
| `ann_vol_pct` | `1.2205035706090142` |
| `sharpe` | `-0.05509846185610812` |
| `sortino` | `-0.07919964850003426` |
| `max_dd_pct` | `2.2965946706517415` |
| `max_dd_duration_days` | `392.4166666666667` |
| `calmar` | `-0.03253100506453437` |
| `sharpe_daily` | `-0.002883985303341138` |
| `skew` | `0.20774253290475167` |
| `kurtosis` | `13.530618669899914` |
| `n_days` | `912` |
| `psr0` | `0.465328011350058` |
| `trades` | `191` |
| `win_rate_pct` | `47.12041884816754` |
| `profit_factor` | `0.9841489927035095` |
| `gross_profit_usd` | `1157.5707602376708` |
| `gross_loss_usd` | `1176.2149520244516` |
| `net_pnl_usd` | `-18.644191786781008` |
| `avg_trade_return_pct` | `-0.008699056867468963` |
| `median_trade_return_pct` | `-0.20392501051142187` |
| `avg_win_pct` | `1.2841380907694913` |
| `avg_loss_pct` | `-1.160732158722186` |
| `avg_win_usd` | `12.86189733597412` |
| `avg_loss_usd` | `-11.6456925943015` |
| `expectancy_usd` | `-0.09761356956429847` |
| `avg_bars_held` | `7.366492146596858` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.104433869589494` |
| `trade_tstat` | `-0.08193999231595187` |
| `win_rate_ci95_low_pct` | `40.16796352289213` |
| `win_rate_ci95_high_pct` | `54.186420771611154` |
| `long_trades` | `99` |
| `long_profit_factor` | `1.0243280202499623` |
| `long_net_pnl_usd` | `15.078992332583699` |
| `short_trades` | `92` |
| `short_profit_factor` | `0.9393898505729369` |
| `short_net_pnl_usd` | `-33.72318411936469` |
| `exit_reasons.LC Exit` | `78` |
| `exit_reasons.SL` | `58` |
| `exit_reasons.TP` | `55` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1407` |
| `exposure_pct` | `6.428473523095901` |
| `subperiods.2023.net_return_pct` | `-0.7233891289174066` |
| `subperiods.2023.sharpe` | `-0.7484089088794317` |
| `subperiods.2023.trades` | `57` |
| `subperiods.2023.profit_factor` | `0.7844141126391321` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `2.1368197347763296` |
| `subperiods.2024.sharpe` | `1.5254715402133967` |
| `subperiods.2024.trades` | `85` |
| `subperiods.2024.profit_factor` | `1.4352249094426826` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.5625706844704657` |
| `subperiods.2025H1.sharpe` | `-2.432684562714926` |
| `subperiods.2025H1.trades` | `49` |
| `subperiods.2025H1.profit_factor` | `0.55147717380895` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.7378821916518192` |
| `stress.sharpe` | `-0.8864025699895192` |
| `stress.profit_factor` | `0.7921861222310251` |
| `stress.trades` | `191` |
| `stress.max_dd_pct` | `3.194300018416507` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2281172000075458` |
| `signals_runtime_s` | `2.1558446000126423` |

### Critic verdict

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

---

## Run 06

- run id: `run_06`
- timestamp (UTC): `2026-09-13T17:13:16Z`
- config hash: `6e8b70e48aa9`
- eligible: **NO**
- runtime_s: `2.232236700001522`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `191` | PASS |
| G2 | profit_factor > 1.0 | `1.0600917137611088` | PASS |
| G3 | stress.net_return_pct > 0 | `-1.8740945619427851` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10069.443188293333` |
| `net_return_pct` | `0.6944318829333218` |
| `cagr_pct` | `0.2775386141812053` |
| `ann_vol_pct` | `1.2609897681449846` |
| `sharpe` | `0.22593780653043638` |
| `sortino` | `0.33792753131581404` |
| `max_dd_pct` | `1.4971170591172367` |
| `max_dd_duration_days` | `401.875` |
| `calmar` | `0.18538203976170958` |
| `sharpe_daily` | `0.011826125295558982` |
| `skew` | `0.5707632241208686` |
| `kurtosis` | `14.018095993106137` |
| `n_days` | `912` |
| `psr0` | `0.6398560581107225` |
| `trades` | `191` |
| `win_rate_pct` | `48.167539267015705` |
| `profit_factor` | `1.0600917137611088` |
| `gross_profit_usd` | `1225.0632221867806` |
| `gross_loss_usd` | `1155.6200338934525` |
| `net_pnl_usd` | `69.44318829332802` |
| `avg_trade_return_pct` | `0.037355496435860926` |
| `median_trade_return_pct` | `-0.08826181753759114` |
| `avg_win_pct` | `1.3279394772423125` |
| `avg_loss_pct` | `-1.1619750715862962` |
| `avg_win_usd` | `13.315904588986745` |
| `avg_loss_usd` | `-11.6729296352874` |
| `expectancy_usd` | `0.363576902059309` |
| `avg_bars_held` | `7.4136125654450264` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.140750865895106` |
| `trade_tstat` | `0.34368932539901265` |
| `win_rate_ci95_low_pct` | `41.18763984393767` |
| `win_rate_ci95_high_pct` | `55.2196956162008` |
| `long_trades` | `98` |
| `long_profit_factor` | `1.0319895766627802` |
| `long_net_pnl_usd` | `19.97753927726282` |
| `short_trades` | `93` |
| `short_profit_factor` | `1.0931348612433767` |
| `short_net_pnl_usd` | `49.46564901606519` |
| `exit_reasons.LC Exit` | `79` |
| `exit_reasons.SL` | `56` |
| `exit_reasons.TP` | `56` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1416` |
| `exposure_pct` | `6.469593822817197` |
| `subperiods.2023.net_return_pct` | `-0.8444361616368079` |
| `subperiods.2023.sharpe` | `-0.8571969400035117` |
| `subperiods.2023.trades` | `56` |
| `subperiods.2023.profit_factor` | `0.7568718317582268` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `2.2787297821800667` |
| `subperiods.2024.sharpe` | `1.6229477434207182` |
| `subperiods.2024.trades` | `84` |
| `subperiods.2024.profit_factor` | `1.4839715797712028` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.7105644682525503` |
| `subperiods.2025H1.sharpe` | `-0.9772249399068706` |
| `subperiods.2025H1.trades` | `51` |
| `subperiods.2025H1.profit_factor` | `0.7889439135826681` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-1.8740945619427851` |
| `stress.sharpe` | `-0.5838688781790445` |
| `stress.profit_factor` | `0.8551170167420028` |
| `stress.trades` | `191` |
| `stress.max_dd_pct` | `2.2146848200111924` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.232236700001522` |
| `signals_runtime_s` | `2.1646329000068363` |

### Critic verdict

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

---

## Run 07

- run id: `run_07`
- timestamp (UTC): `2026-09-13T17:17:50Z`
- config hash: `6031a3b45820`
- eligible: **NO**
- runtime_s: `2.2470716000098037`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `14` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 14,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `193` | PASS |
| G2 | profit_factor > 1.0 | `1.0476459154161921` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.0241318465394786` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10056.623902255218` |
| `net_return_pct` | `0.566239022552173` |
| `cagr_pct` | `0.22639125129269022` |
| `ann_vol_pct` | `1.288602944054683` |
| `sharpe` | `0.18180409029783332` |
| `sortino` | `0.26759273299789116` |
| `max_dd_pct` | `1.3913205738109502` |
| `max_dd_duration_days` | `406.6666666666667` |
| `calmar` | `0.16271681419371564` |
| `sharpe_daily` | `0.009516061008663734` |
| `skew` | `0.36518772796758037` |
| `kurtosis` | `14.008367240921201` |
| `n_days` | `912` |
| `psr0` | `0.6132037710738447` |
| `trades` | `193` |
| `win_rate_pct` | `48.704663212435236` |
| `profit_factor` | `1.0476459154161921` |
| `gross_profit_usd` | `1245.0553084023607` |
| `gross_loss_usd` | `1188.4314061471284` |
| `net_pnl_usd` | `56.62390225523234` |
| `avg_trade_return_pct` | `0.030436866779937212` |
| `median_trade_return_pct` | `-0.07365267232305385` |
| `avg_win_pct` | `1.321878633920064` |
| `avg_loss_pct` | `-1.1957805686864458` |
| `avg_win_usd` | `13.245269238322985` |
| `avg_loss_usd` | `-12.004357637849782` |
| `expectancy_usd` | `0.29338809458669607` |
| `avg_bars_held` | `7.487046632124352` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.103371761980883` |
| `trade_tstat` | `0.27457380555584027` |
| `win_rate_ci95_low_pct` | `41.747347166621005` |
| `win_rate_ci95_high_pct` | `55.712537539601094` |
| `long_trades` | `99` |
| `long_profit_factor` | `1.0810950582519951` |
| `long_net_pnl_usd` | `49.08774998499184` |
| `short_trades` | `94` |
| `short_profit_factor` | `1.012923840852342` |
| `short_net_pnl_usd` | `7.536152270240503` |
| `exit_reasons.LC Exit` | `80` |
| `exit_reasons.SL` | `56` |
| `exit_reasons.TP` | `57` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1445` |
| `exposure_pct` | `6.602092566363595` |
| `subperiods.2023.net_return_pct` | `-0.5733400364043906` |
| `subperiods.2023.sharpe` | `-0.5886106751870245` |
| `subperiods.2023.trades` | `56` |
| `subperiods.2023.profit_factor` | `0.8255886771996289` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.8700024392072967` |
| `subperiods.2024.sharpe` | `1.26939529519923` |
| `subperiods.2024.trades` | `86` |
| `subperiods.2024.profit_factor` | `1.3584484861765782` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.7105644682527501` |
| `subperiods.2025H1.sharpe` | `-0.9772249399070432` |
| `subperiods.2025H1.trades` | `51` |
| `subperiods.2025H1.profit_factor` | `0.7889439135826679` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.0241318465394786` |
| `stress.sharpe` | `-0.6182802867291932` |
| `stress.profit_factor` | `0.8473182579804082` |
| `stress.trades` | `193` |
| `stress.max_dd_pct` | `2.3642013324707944` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2470716000098037` |
| `signals_runtime_s` | `2.17959189999965` |

### Critic verdict

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

---

## Run 08

- run id: `run_08`
- timestamp (UTC): `2026-09-13T17:20:46Z`
- config hash: `9fa51c472368`
- eligible: **NO**
- runtime_s: `2.2612057000078494`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `sqzRegimeMode` | `Released Within Window` | `Squeeze Off` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Released Within Window",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `137` | PASS |
| G2 | profit_factor > 1.0 | `1.0389429900174267` | PASS |
| G3 | stress.net_return_pct > 0 | `-1.4926187612478659` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10033.11335810883` |
| `net_return_pct` | `0.3311335810883165` |
| `cagr_pct` | `0.13248541930719338` |
| `ann_vol_pct` | `1.099030424403704` |
| `sharpe` | `0.12587362250620956` |
| `sortino` | `0.1857147336305037` |
| `max_dd_pct` | `1.328563768513491` |
| `max_dd_duration_days` | `406.6666666666667` |
| `calmar` | `0.09972078303432075` |
| `sharpe_daily` | `0.006588526524284002` |
| `skew` | `0.4850288734252948` |
| `kurtosis` | `15.12603760626985` |
| `n_days` | `912` |
| `psr0` | `0.5789324632302382` |
| `trades` | `137` |
| `win_rate_pct` | `48.9051094890511` |
| `profit_factor` | `1.0389429900174267` |
| `gross_profit_usd` | `883.4167912555554` |
| `gross_loss_usd` | `850.3034331467383` |
| `net_pnl_usd` | `33.11335810881738` |
| `avg_trade_return_pct` | `0.02524299608853875` |
| `median_trade_return_pct` | `-0.07365267232305385` |
| `avg_win_pct` | `1.3177986341655206` |
| `avg_loss_pct` | `-1.2119174003565725` |
| `avg_win_usd` | `13.18532524262023` |
| `avg_loss_usd` | `-12.14719190209626` |
| `expectancy_usd` | `0.24170334385998088` |
| `avg_bars_held` | `7.0510948905109485` |
| `max_consecutive_losses` | `4` |
| `payoff_ratio` | `1.0854628253913414` |
| `trade_tstat` | `0.19746089091310945` |
| `win_rate_ci95_low_pct` | `40.6793178139353` |
| `win_rate_ci95_high_pct` | `57.19062756640947` |
| `long_trades` | `72` |
| `long_profit_factor` | `1.079627125324118` |
| `long_net_pnl_usd` | `36.26235677271886` |
| `short_trades` | `65` |
| `short_profit_factor` | `0.9920258604683652` |
| `short_net_pnl_usd` | `-3.1489986639014678` |
| `exit_reasons.LC Exit` | `51` |
| `exit_reasons.SL` | `42` |
| `exit_reasons.TP` | `44` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `966` |
| `exposure_pct` | `4.413578836752411` |
| `subperiods.2023.net_return_pct` | `-0.7446602488835219` |
| `subperiods.2023.sharpe` | `-0.842550782469524` |
| `subperiods.2023.trades` | `40` |
| `subperiods.2023.profit_factor` | `0.7261935052398417` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.7176708938657637` |
| `subperiods.2024.sharpe` | `1.4535547993016318` |
| `subperiods.2024.trades` | `61` |
| `subperiods.2024.profit_factor` | `1.518563181228867` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.6231030920728631` |
| `subperiods.2025H1.sharpe` | `-0.9534958567433016` |
| `subperiods.2025H1.trades` | `36` |
| `subperiods.2025H1.profit_factor` | `0.747929486190075` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-1.4926187612478659` |
| `stress.sharpe` | `-0.5340009040929634` |
| `stress.profit_factor` | `0.8428243946782538` |
| `stress.trades` | `137` |
| `stress.max_dd_pct` | `1.8180063579970485` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2612057000078494` |
| `signals_runtime_s` | `2.1922451999998884` |

### Critic verdict

RUN: 08
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.126 (vs run06 incumbent 0.226, Δ-0.100 — a clear regression, not an improvement); PF 1.039 (down from 1.060, still >1, G2 holds); PSR0 0.579 (down from 0.640); trade_tstat 0.197 (down from 0.344, further from significance). Run06 remains the high-water mark on every risk-adjusted metric across runs 06→08.
- Drawdown: max_dd 1.33% (best yet, down from 1.50%), duration flat ~407d, skew 0.485, kurtosis 15.1 — the one clear improvement in this run.
- Significance: trades collapsed 191→137 (-28.3%), still clears G1 but with a much smaller sample; win rate 48.9% (flat).
- Robustness (incl. pf_ex_top2 diagnostic): SQZ 'Released Within Window' did NOT flip either weak sub-period — 2023 stays negative (-0.84%→-0.75%, still no flip), 2025H1 stays negative (-0.71%→-0.62%, still no flip); only 2024 is positive. G4 still 1/3, unresolved by this probe. Short side got WORSE: PF 1.093→0.992 (flips below 1.0), short net +$49.5→-$3.1 — the SQZ filter preferentially removed profitable shorts. Long side improved (PF 1.032→1.080, net +$20.0→+$36.3). Diagnostic trend pf_ex_top2 was 0.98(run06)→0.97(run07); run08 ≈0.955 by the same top-2-removal method (42.71+28.66 removed from $883.42 gross profit → $812.05/$850.30) — continuing the same fragility, not resolving it, and now on a smaller base. Stress improved -1.87%→-1.49% but still fails G3.
- Carrier-trade check: of the two trades that drove run06's result, the short 2025-03-03 TP survives intact (+$42.71 vs run06's +$42.88); but the long 2025-01-13 TP is GONE entirely (its whole setup — including the preceding short 2025-01-12 signal — no longer appears in trades.csv), removing roughly $30 of run06's edge. This confirms the earlier fragility warning: the SQZ regime change further destabilizes an already thin, trade-dependent result.

WEAKNESSES: This run trades quantity and short-side quality for a smaller, cleaner-looking sample, but does not solve G3/G4 and makes Sharpe/PF/significance worse than the incumbent. It is a net regression, not progress.

DEMANDS FOR NEXT CONFIG: (1) Revert to run06 base (sqzRegimeMode='Squeeze Off') — this probe is answered: REFUTED as an improvement (Sharpe/PF/short-PF all fell). (2) Since SQZ mode-swap didn't fix G4, try a milder regime lever instead: `sqzReleaseWindow` or leave regime as-is and probe WWV (`wwvUseVolThreshold=true`) or the still-owed `allowShorts=false` diagnostic, now informed by run08's short-side fragility. (3) Keep reporting pf_ex_top2 and carrier-trade survival every run — both are now core robustness evidence, not just G1-G4.

PLATEAU ASSESSMENT: Best (fallback) = run06, sharpe 0.226, 2 runs since last ≥0.05 improvement (07, 08 both regressed). Untested: WWV volume threshold, allowShorts isolation, further SQZ release-window tuning. 8/25 used — not plateau; two consecutive regressions is a signal to return to the incumbent, not evidence search is exhausted.

---

## Run 09

- run id: `run_09`
- timestamp (UTC): `2026-09-13T17:23:52Z`
- config hash: `0c2c80e164aa`
- eligible: **NO**
- runtime_s: `2.235330499999691`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |
| `wwvUseVolThreshold` | `true` | `false` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": true
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `130` | PASS |
| G2 | profit_factor > 1.0 | `1.0440832532868927` | PASS |
| G3 | stress.net_return_pct > 0 | `-1.4210096295670716` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10032.81200808219` |
| `net_return_pct` | `0.32812008082190314` |
| `cagr_pct` | `0.1312809109779156` |
| `ann_vol_pct` | `1.0018337513521978` |
| `sharpe` | `0.13586928160095002` |
| `sortino` | `0.1926797918841852` |
| `max_dd_pct` | `1.5685227506697208` |
| `max_dd_duration_days` | `356.2083333333333` |
| `calmar` | `0.08369716723704637` |
| `sharpe_daily` | `0.0071117232335083614` |
| `skew` | `-0.1926557262332702` |
| `kurtosis` | `16.703422736188916` |
| `n_days` | `912` |
| `psr0` | `0.5849149416466475` |
| `trades` | `130` |
| `win_rate_pct` | `47.69230769230769` |
| `profit_factor` | `1.0440832532868927` |
| `gross_profit_usd` | `777.1311232945369` |
| `gross_loss_usd` | `744.3191152123547` |
| `net_pnl_usd` | `32.8120080821821` |
| `avg_trade_return_pct` | `0.026172429429147128` |
| `median_trade_return_pct` | `-0.0809572449303225` |
| `avg_win_pct` | `1.2502560737080908` |
| `avg_loss_pct` | `-1.089903834472243` |
| `avg_win_usd` | `12.534372956363498` |
| `avg_loss_usd` | `-10.945869341358158` |
| `expectancy_usd` | `0.25240006217063155` |
| `avg_bars_held` | `7.346153846153846` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.1451235681211083` |
| `trade_tstat` | `0.2131172425430293` |
| `win_rate_ci95_low_pct` | `39.29654221630551` |
| `win_rate_ci95_high_pct` | `56.22054191228418` |
| `long_trades` | `67` |
| `long_profit_factor` | `0.9961477768126592` |
| `long_net_pnl_usd` | `-1.63833648537857` |
| `short_trades` | `63` |
| `short_profit_factor` | `1.107987106277826` |
| `short_net_pnl_usd` | `34.45034456756067` |
| `exit_reasons.LC Exit` | `53` |
| `exit_reasons.SL` | `39` |
| `exit_reasons.TP` | `38` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `955` |
| `exposure_pct` | `4.363320692648604` |
| `subperiods.2023.net_return_pct` | `-0.19220179500168966` |
| `subperiods.2023.sharpe` | `-0.22823925795062047` |
| `subperiods.2023.trades` | `39` |
| `subperiods.2023.profit_factor` | `0.9117411605542756` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.1915808831818087` |
| `subperiods.2024.sharpe` | `1.0682702582262702` |
| `subperiods.2024.trades` | `58` |
| `subperiods.2024.profit_factor` | `1.3884884885616997` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.6623644058854183` |
| `subperiods.2025H1.sharpe` | `-1.2308199360189622` |
| `subperiods.2025H1.trades` | `33` |
| `subperiods.2025H1.profit_factor` | `0.696496821689958` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-1.4210096295670716` |
| `stress.sharpe` | `-0.5570256672632788` |
| `stress.profit_factor` | `0.8312503718712217` |
| `stress.trades` | `130` |
| `stress.max_dd_pct` | `2.1209784064868065` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.235330499999691` |
| `signals_runtime_s` | `2.165313799996511` |

### Critic verdict

RUN: 09
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.136 (vs incumbent run06 0.226, Δ-0.090 — 3rd consecutive run below the 0.276 improvement bar, following run07 0.182 and run08 0.126). PF 1.044 (still >1, G2 holds but weaker than run06's 1.060). PSR0 0.585 (down from 0.640), trade_tstat 0.213 (down from 0.344) — every confidence metric keeps drifting away from run06, not toward it.
- Drawdown: max_dd 1.57% (slightly worse than run06's 1.50%), duration 356d (better). Skew flipped 0.571→-0.193 (now negative-tailed again), kurtosis worsened 14.0→16.7 — tail risk got worse under this filter, not better.
- Significance: trades 191→130 (-32%), still clears G1 comfortably (130≥100).
- Robustness (concentration diagnostics, run06→run09): overlap 113/130 entries (87%) match run06, 17 new — not a clean subset (unlike run08). The 78 trades removed were net +$52.64 under run06's own pricing (median -0.151%, but dollar-positive in aggregate) — this filter discarded a net-profitable trade group to get a "cleaner-looking" median. Top-2 winners shrank $88.84→$58.92, but net-ex-top-2 got WORSE, not better: -$19.40→-$26.10. PF-ex-top-2 fell 0.983→0.965. Median trade -0.088%→-0.081% (flat). This is the key finding: headline PF/Sharpe still stand only because of 2 outlier trades, and the "typical" trade population's edge is deteriorating across runs 06→08→09, not improving — the filters are trading volume for cosmetics, not for real quality.
- Carrier trades: long 2025-01-13 TP present (+$30.03, consistent with run06). Short 2025-03-03 TP ABSENT — this is the third run in a row (06✓✓, 07✓✓, 08✗✓, 09✓✗) where a new filter swaps which one of the two carrier trades survives, never keeping both, never adding a third. One especially telling swap: 2024-03-15 short — a +$46.01 TP winner in run06 — becomes a -$0.52 LC-Exit under a 1-hour-later entry in run09 (a ~$46.5 single-trade swing from a volume-threshold gate).
- Sub-periods: 2023 improved sharply (-0.844%→-0.192%, closest yet to flipping, still negative); 2024 fell (2.279%→1.192%); 2025H1 flat (-0.711%→-0.662%). G4 still 1/3. Stress -1.874%→-1.421%, still fails G3. Long PF fell below 1.0 for the first time since run06 (1.032→0.996, net +$20.0→-$1.6); short PF held up (1.093→1.108).

WEAKNESSES: Every post-run06 filter (SQZ-08, WWV-09) shrinks trades and superficially cleans headline metrics while the ex-top-2 core edge keeps eroding (-$19.40→-$26.10) — this is a fragility trend, not noise. Neither filter has produced a genuine 2-sub-period G4 pass.

DEMANDS FOR NEXT CONFIG: (1) Revert to run06 base; the last 3 runs (07/08/09) are all inferior on Sharpe, PF-ex-top-2, and tail risk. (2) Stop pursuing filters that only cut trade count — target the entry/exit mechanics that make the "ex-top-2" population profitable (e.g., LC feature/window tuning) instead of confirmation-role gating. (3) Given 2023 nearly flipped under WWV, consider combining a mild WWV threshold with something targeting 2025H1 specifically, but require it to raise (not merely hold) net-ex-top-2.

PLATEAU ASSESSMENT: Best (fallback) = run06, sharpe 0.226; 3 consecutive runs (07, 08, 09) without a ≥0.05 improvement — below the plateau threshold of 5, and not all roles (WWV alternates, allowShorts, LC re-tightening) are exhausted. CONTINUE, but the trend is a warning sign to stop filter-only probes.

---

## Run 10

- run id: `run_10`
- timestamp (UTC): `2026-09-13T17:26:46Z`
- config hash: `ea72d91a556f`
- eligible: **NO**
- runtime_s: `2.2721512999996776`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcHorizon` | `8` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 8,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 8,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `192` | PASS |
| G2 | profit_factor > 1.0 | `1.0184345614233612` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.3496219420014675` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10022.204292436358` |
| `net_return_pct` | `0.22204292436358575` |
| `cagr_pct` | `0.08886761242894448` |
| `ann_vol_pct` | `1.2883209500925457` |
| `sharpe` | `0.07533520887616502` |
| `sortino` | `0.11005444101209222` |
| `max_dd_pct` | `1.4971170591172367` |
| `max_dd_duration_days` | `425.5` |
| `calmar` | `0.05935916092048578` |
| `sharpe_daily` | `0.003943225053911538` |
| `skew` | `0.3456069135485255` |
| `kurtosis` | `14.066290191612682` |
| `n_days` | `912` |
| `psr0` | `0.5474002051049414` |
| `trades` | `192` |
| `win_rate_pct` | `47.91666666666667` |
| `profit_factor` | `1.0184345614233612` |
| `gross_profit_usd` | `1226.6968716968804` |
| `gross_loss_usd` | `1204.4925792605197` |
| `net_pnl_usd` | `22.204292436360447` |
| `avg_trade_return_pct` | `0.012743077598798598` |
| `median_trade_return_pct` | `-0.09312186685296386` |
| `avg_win_pct` | `1.3340199479302044` |
| `avg_loss_pct` | `-1.2028316431060946` |
| `avg_win_usd` | `13.333661648879135` |
| `avg_loss_usd` | `-12.044925792605197` |
| `expectancy_usd` | `0.11564735643937733` |
| `avg_bars_held` | `7.416666666666667` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.1069940885036533` |
| `trade_tstat` | `0.11413992773785361` |
| `win_rate_ci95_low_pct` | `40.96078946077781` |
| `win_rate_ci95_high_pct` | `54.95427364783367` |
| `long_trades` | `99` |
| `long_profit_factor` | `1.0451939390324976` |
| `long_net_pnl_usd` | `28.143388974022585` |
| `short_trades` | `93` |
| `short_profit_factor` | `0.989791292547594` |
| `short_net_pnl_usd` | `-5.939096537662086` |
| `exit_reasons.LC Exit` | `79` |
| `exit_reasons.SL` | `57` |
| `exit_reasons.TP` | `56` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1424` |
| `exposure_pct` | `6.506145200347238` |
| `subperiods.2023.net_return_pct` | `-0.7623391637769927` |
| `subperiods.2023.sharpe` | `-0.7703555160080345` |
| `subperiods.2023.trades` | `57` |
| `subperiods.2023.profit_factor` | `0.7805117245578671` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.7146925303533456` |
| `subperiods.2024.sharpe` | `1.1754578243372922` |
| `subperiods.2024.trades` | `84` |
| `subperiods.2024.profit_factor` | `1.3289213161271962` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.7105644682525947` |
| `subperiods.2025H1.sharpe` | `-0.9772249399068818` |
| `subperiods.2025H1.trades` | `51` |
| `subperiods.2025H1.profit_factor` | `0.7889439135826681` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.3496219420014675` |
| `stress.sharpe` | `-0.7195356224200632` |
| `stress.profit_factor` | `0.8250304855338161` |
| `stress.trades` | `192` |
| `stress.max_dd_pct` | `2.688561667599676` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2721512999996776` |
| `signals_runtime_s` | `2.200630999999703` |

### Critic verdict

RUN: 10
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.226→0.075 (Δ-0.150 — the largest regression yet, worse than runs 07/08/09); PF 1.060→1.018 (barely clears G2, weakest PF since run06); PSR0 0.640→0.547; trade_tstat 0.344→0.114. This is the 4th consecutive run below the 0.276 bar, and the worst of the four on every headline metric.
- Drawdown: max_dd identical to run06 at 1.497% (same worst-loss trade sequence), duration worse 402→425.5d. Skew 0.571→0.346, kurtosis flat (~14.0-14.1).
- Significance: trades 191→192 (flat); the first 29 rows of trades.csv are BYTE-IDENTICAL to run06 (same entry/exit/pnl) — the label-horizon change only starts biting later in the sample.
- Robustness: 2025H1 is EXACTLY unchanged (net -0.71056% both runs, 51 trades, PF 0.78894 matching to 10 decimals) — lcHorizon=8 had zero effect there; 2023 marginally better (-0.844%→-0.762%, still negative); 2024 worse (2.279%→1.715%). G4 still 1/3. Short PF fell below 1.0 again (1.093→0.990, net +$49.5→-$5.9); long PF flat (~1.03-1.05). Stress worse (-1.874%→-2.350%), still fails G3.

MECHANISM CHECK (per orchestrator correction): lcHorizon is not a forward prediction window. The ported label is y[t] = (src[t-H]<src[t]) ? SHORT : (src[t-H]>src[t]) ? LONG : NEUTRAL — a backward mean-reversion label comparing price H bars ago to now, attached to the CURRENT feature vector. The tuner's rationale ("align labels with the 12-bar hold") conflated this with a forward-return horizon; there's no mechanical reason a longer H should track hold length. Empirically, doubling H (4→8) lengthens the realized-move window used to call "reversion" and made results materially worse (Sharpe -0.150, PF -0.042, stress -0.48pp) — consistent with staler/less-relevant labels, not a hold-alignment benefit. Treat this lever as refuted with a correct mechanistic explanation, not just "didn't help."

WEAKNESSES: Worst post-run06 result across Sharpe, PF, and t-stat; no G4 progress; the tuner's stated hypothesis for this change was mechanistically wrong, and the result confirms the wrong direction rather than being neutral.

DEMANDS FOR NEXT CONFIG: (1) Revert to run06 base (lcHorizon=4). (2) Do not re-probe lcHorizon upward again — refuted with a clear mechanism. (3) If horizon is revisited, only test shorter values (e.g., 2-3) under an explicit reversion-window hypothesis, not a hold-alignment one. (4) Move to a genuinely unexplored lever targeting 2025H1/G4: `lcSpacing`, `nwBandwidth`/`nwLookback` (trend role untouched beyond slope), or `wtObLevel2`/`wtOsLevel2` (timing thresholds untouched).

PLATEAU ASSESSMENT: Best (fallback) = run06, sharpe 0.226. 4 consecutive runs (07, 08, 09, 10) without a ≥0.05 improvement — below the required ≥5, so PLATEAU cannot be invoked yet regardless of role coverage. All 6 roles have been touched at least once (trend-04, entry-06/10, timing-05, confirmation-09, regime-08, exits-02/03/04), but this run's regression is the worst yet, which argues against conviction that search is exhausted — unexplored parameters remain within nearly every role. VERDICT: CONTINUE.

---

## Run 11

- run id: `run_11`
- timestamp (UTC): `2026-09-13T17:29:47Z`
- config hash: `ca9d74aee942`
- eligible: **NO**
- runtime_s: `2.19005130000005`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `219` | PASS |
| G2 | profit_factor > 1.0 | `1.0531903507906095` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.2515008154103455` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10070.422332774373` |
| `net_return_pct` | `0.704223327743736` |
| `cagr_pct` | `0.2814436742414994` |
| `ann_vol_pct` | `1.364857733027254` |
| `sharpe` | `0.21259166018293962` |
| `sortino` | `0.3183320745792339` |
| `max_dd_pct` | `1.5332647253111564` |
| `max_dd_duration_days` | `392.2083333333333` |
| `calmar` | `0.18355843553655357` |
| `sharpe_daily` | `0.011127556068292` |
| `skew` | `0.8212329915763272` |
| `kurtosis` | `15.523922484603583` |
| `n_days` | `912` |
| `psr0` | `0.6320656306481305` |
| `trades` | `219` |
| `win_rate_pct` | `48.401826484018265` |
| `profit_factor` | `1.0531903507906095` |
| `gross_profit_usd` | `1394.390528652553` |
| `gross_loss_usd` | `1323.968195878182` |
| `net_pnl_usd` | `70.42233277437123` |
| `avg_trade_return_pct` | `0.03314795930017288` |
| `median_trade_return_pct` | `-0.07914069157976798` |
| `avg_win_pct` | `1.311321815448786` |
| `avg_loss_pct` | `-1.165846985405606` |
| `avg_win_usd` | `13.15462762879767` |
| `avg_loss_usd` | `-11.716532706886568` |
| `expectancy_usd` | `0.32156316335329327` |
| `avg_bars_held` | `7.602739726027397` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.122740656974895` |
| `trade_tstat` | `0.32947715270369826` |
| `win_rate_ci95_low_pct` | `41.86789433224716` |
| `win_rate_ci95_high_pct` | `54.99085895493515` |
| `long_trades` | `111` |
| `long_profit_factor` | `1.035087948267707` |
| `long_net_pnl_usd` | `24.02649039025571` |
| `short_trades` | `108` |
| `short_profit_factor` | `1.0725822254949129` |
| `short_net_pnl_usd` | `46.395842384115504` |
| `exit_reasons.LC Exit` | `94` |
| `exit_reasons.SL` | `64` |
| `exit_reasons.TP` | `61` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1665` |
| `exposure_pct` | `7.607255448439713` |
| `subperiods.2023.net_return_pct` | `-0.6234821086940623` |
| `subperiods.2023.sharpe` | `-0.5962055472873198` |
| `subperiods.2023.trades` | `65` |
| `subperiods.2023.profit_factor` | `0.8372056507479363` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `2.0640921294277748` |
| `subperiods.2024.sharpe` | `1.3262426687254845` |
| `subperiods.2024.trades` | `94` |
| `subperiods.2024.profit_factor` | `1.372040619758239` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.7133329031322577` |
| `subperiods.2025H1.sharpe` | `-0.9303494631033651` |
| `subperiods.2025H1.trades` | `60` |
| `subperiods.2025H1.profit_factor` | `0.8143097928176263` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.2515008154103455` |
| `stress.sharpe` | `-0.6503658566529251` |
| `stress.profit_factor` | `0.8474078821729057` |
| `stress.trades` | `219` |
| `stress.max_dd_pct` | `2.7357761387957313` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.19005130000005` |
| `signals_runtime_s` | `2.1209835999907227` |

### Critic verdict

RUN: 11
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.213 (vs incumbent run06 0.226, Δ-0.013 — the closest any run has come to the incumbent since run06 itself, and still the 2nd-best Sharpe across all 11 runs); PF 1.053 (vs 1.060, both PF>1 held); PSR0 0.632 (2nd-highest); trade_tstat 0.329 (2nd-highest). This is the 5th consecutive run below the 0.276 raise-bar, but qualitatively the strongest of the five.
- Drawdown: max_dd 1.53% (vs 1.50%, marginally worse), duration 392d (better than 402d); skew 0.821 (best of any run so far, vs 0.571), kurtosis 15.5 (worse than 14.0).
- Significance: trades 191→219 (+28, the largest trade count yet), both long PF (1.035) and short PF (1.073) hold above 1.0 simultaneously — cleanest long/short split seen since run06.
- Robustness: 2023 net -0.844%→-0.623% (best 2023 result across all 11 runs, closest yet to flipping G4); 2024 2.279%→2.064% (slightly weaker); 2025H1 -0.711%→-0.713% (essentially unchanged). G4 still 1/3. Stress -1.874%→-2.252% (worse), still fails G3. First 9 trades are identical to run06; trade #10 (short, 2023-03-14, new) is a plausible confirmation of the tuner's stated mechanism (faster NW + price-side requirement admits a dip-reversion entry run06 rejected). Full overlap/carrier diagnostics pending.

WEAKNESSES: Still not eligible (G3, G4 fail). Stress degraded further. No sub-period actually flipped positive despite 2023 getting much closer.

DEMANDS FOR NEXT CONFIG: (1) Push the 2023 near-miss further — test `nwBandwidth` slightly below 5 or `nwLookback` (still untouched) to see if 2023 crosses zero. (2) Open LC feature engineering (`lcF{1-5}String/ParamA/ParamB`) — completely untested since run01, the single highest-leverage untested lever given LC is the sole entry signal. (3) Vary `riskTpMult` (fixed at default 3.0 through all 11 runs) now that TP is load-bearing (44-61 TP exits/run).

PLATEAU ASSESSMENT — rigorous application: Numeric precondition (≥5 consecutive runs without raising best by ≥0.05) is now MET: 07(0.182), 08(0.126), 09(0.136), 10(0.075), 11(0.213) are all <0.276. However the rule is a conjunction, and the other two legs FAIL: (a) "every role probed" — trend/entry/timing/confirmation/regime/exits have each had ONE lever touched, but each still has untested, mechanistically-credible parameters (LC feature set entirely untouched; NW lookback/kernel/H-mult untouched; WT ob/os thresholds untouched; WWV method/avg-length untouched; SQZ release-window/BB-KC mults untouched; exit risk-TP multiplier never varied). This is shallow coverage, not exhaustion. (b) "conviction further search is noise-mining" — NOT met: run11 is the 2nd-best Sharpe ever, has the best skew and closest 2023 near-flip of any run, directly contradicting the idea that the neighborhood is exhausted; DSR (0.115 at N=11) is declining as expected with N but doesn't itself signal exhaustion. Budget: 14/25 slots remain, well over half. Best (fallback) = run06, sharpe 0.226, 5 runs since last ≥0.05 improvement. Ruling: PLATEAU REJECTED — continue, prioritizing LC feature engineering and trend-role refinement around the run11 direction.

---

## Run 12

- run id: `run_12`
- timestamp (UTC): `2026-09-13T17:32:46Z`
- config hash: `63c46035c8d0`
- eligible: **NO**
- runtime_s: `1.8878224000072805`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcFeatureCount` | `4` | `5` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 4,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `222` | PASS |
| G2 | profit_factor > 1.0 | `1.016224385992762` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.754530566906832` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10022.649909380843` |
| `net_return_pct` | `0.22649909380842992` |
| `cagr_pct` | `0.0906498837514258` |
| `ann_vol_pct` | `1.4055279355958417` |
| `sharpe` | `0.0714403497348508` |
| `sortino` | `0.1040735419964677` |
| `max_dd_pct` | `1.9437463045933079` |
| `max_dd_duration_days` | `392.2083333333333` |
| `calmar` | `0.046636684806658744` |
| `sharpe_daily` | `0.0037393588089432344` |
| `skew` | `0.46223046395611106` |
| `kurtosis` | `15.986943345548667` |
| `n_days` | `912` |
| `psr0` | `0.5449684435694577` |
| `trades` | `222` |
| `win_rate_pct` | `47.2972972972973` |
| `profit_factor` | `1.016224385992762` |
| `gross_profit_usd` | `1418.6909916705708` |
| `gross_loss_usd` | `1396.0410822897486` |
| `net_pnl_usd` | `22.64990938082235` |
| `avg_trade_return_pct` | `0.011336499325003127` |
| `median_trade_return_pct` | `-0.21734406654148217` |
| `avg_win_pct` | `1.3483573200815815` |
| `avg_loss_pct` | `-1.188553980841157` |
| `avg_win_usd` | `13.51134277781496` |
| `avg_loss_usd` | `-11.931975062305543` |
| `expectancy_usd` | `0.10202661883253311` |
| `avg_bars_held` | `7.4774774774774775` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `1.1323643158205063` |
| `trade_tstat` | `0.11137852786763072` |
| `win_rate_ci95_low_pct` | `40.83160948688594` |
| `win_rate_ci95_high_pct` | `53.8549285550387` |
| `long_trades` | `115` |
| `long_profit_factor` | `1.0381915866150004` |
| `long_net_pnl_usd` | `27.514728683326236` |
| `short_trades` | `107` |
| `short_profit_factor` | `0.9927992775019187` |
| `short_net_pnl_usd` | `-4.864819302503835` |
| `exit_reasons.LC Exit` | `91` |
| `exit_reasons.SL` | `69` |
| `exit_reasons.TP` | `62` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1660` |
| `exposure_pct` | `7.584410837483438` |
| `subperiods.2023.net_return_pct` | `-0.7958307595890446` |
| `subperiods.2023.sharpe` | `-0.7650350936440218` |
| `subperiods.2023.trades` | `65` |
| `subperiods.2023.profit_factor` | `0.7975826055928166` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `2.196981033047818` |
| `subperiods.2024.sharpe` | `1.398544276588711` |
| `subperiods.2024.trades` | `96` |
| `subperiods.2024.profit_factor` | `1.381759964081407` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.141374122877814` |
| `subperiods.2025H1.sharpe` | `-1.3620071160230207` |
| `subperiods.2025H1.trades` | `61` |
| `subperiods.2025H1.profit_factor` | `0.7321188188401829` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.754530566906832` |
| `stress.sharpe` | `-0.7743039396147156` |
| `stress.profit_factor` | `0.822470390080962` |
| `stress.trades` | `222` |
| `stress.max_dd_pct` | `3.2363137303346057` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `1.8878224000072805` |
| `signals_runtime_s` | `1.8101917000021785` |

### Critic verdict

RUN: 12
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.071 (vs run11 base 0.213, Δ-0.141; vs incumbent run06 0.226, Δ-0.155) — one of the two worst post-run06 results, tied with run10 (0.075). PF 1.016 (down from 1.053, barely clears G2). PSR0 0.545 (down from 0.632), trade_tstat 0.111 (down from 0.329). 6th consecutive run below the 0.276 raise-bar.
- Drawdown: max_dd 1.94% (worst since run05's 2.30%, up from run11's 1.53%), duration flat 392d. Skew 0.821→0.462 (weaker), kurtosis 15.5→16.0 (worse).
- Significance: trades 219→222 (flat count, but composition shifted materially — short PF collapsed).
- Robustness: BOTH sub-periods that had improved under run11 reversed: 2023 -0.623%→-0.796% (moved away from the G4 near-miss), 2025H1 -0.713%→-1.141% (notably worse); 2024 marginally better (2.064%→2.197%). G4 still 1/3, and now further from closing than run11 was. Short PF collapsed 1.073→0.993 (net +$46.4→-$4.9); long PF flat (1.035→1.038). Stress worse (-2.252%→-2.755%), still fails G3.

MECHANISM RULING: The tuner's hypothesis (dropping redundant RSI-feature-5 raises ADX's relative weight, sharpening trend-regime matching) is REFUTED by the data — it degraded Sharpe, PF, both weak sub-periods, and stress simultaneously. This is feature-COUNT-specific evidence, not a verdict on LC feature engineering broadly; feature TYPE/ParamA/ParamB swaps remain untested.

WEAKNESSES: Regression across nearly every axis relative to its own base (run11). Trade-quality composition (short side) is now fragile again.

DEMANDS FOR NEXT CONFIG: (1) Revert to run11 base (lcFeatureCount=5). (2) If probing LC features again, change feature TYPE or ParamA/B (e.g., swap feature 5 from RSI to WT or CCI) rather than count — count-reduction is refuted. (3) Continue the run11 trend-role direction (nwBandwidth neighborhood) since it's the only lever that has moved 2023 meaningfully toward positive.

PLATEAU ASSESSMENT — weighing the invariance evidence explicitly: The run11-vs-run06 supplement (26% entries swapped, both carrier trades replaced, yet net $70.42 vs $69.44, PF-ex-top2 0.985 vs 0.983) shows the run06/11 "12-bar hold + TP + refined NW trend" neighborhood produces a REPRODUCIBLE aggregate economic profile independent of which specific trades populate it — that argues against "two magic rows" overfitting and for a real, if weak, structural pattern in that neighborhood, i.e., NOT pure noise-mining there. But run12 shows that invariance does not extend to every lever: this feature-count change broke the pattern in the wrong direction, proving the space is not flat/saturated — different levers still produce materially different (here, worse) outcomes. That is evidence FOR continued search, not against it. Numeric precondition (≥5 consecutive without +0.05) is met at 6, but role coverage remains shallow (LC feature type/params, WT ob/os thresholds, WWV method/length, SQZ release-window magnitude, exit riskTpMult all untested), and the reproducible-but-weak core (PF-ex-top2 ≈0.98, still <1) means the ceiling hasn't been tested. Best (fallback) = run06, sharpe 0.226. Ruling: PLATEAU REJECTED — continue. Budget: 13/25 remain.

---

## Run 13

- run id: `run_13`
- timestamp (UTC): `2026-09-13T17:35:33Z`
- config hash: `70c0837222ea`
- eligible: **NO**
- runtime_s: `2.2333443999959854`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `exitMode` | `LC Fixed Hold` | `Either (LC Default)` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "LC Fixed Hold",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `219` | PASS |
| G2 | profit_factor > 1.0 | `1.0280722315631754` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.565542778760155` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10038.053608785396` |
| `net_return_pct` | `0.38053608785395543` |
| `cagr_pct` | `0.15222871096189916` |
| `ann_vol_pct` | `1.3942264451720172` |
| `sharpe` | `0.11598944977911084` |
| `sortino` | `0.16937495686488824` |
| `max_dd_pct` | `1.8497601483312698` |
| `max_dd_duration_days` | `392.2083333333333` |
| `calmar` | `0.08229645940811826` |
| `sharpe_daily` | `0.006071165278246279` |
| `skew` | `0.48312400129009153` |
| `kurtosis` | `16.337072379222842` |
| `n_days` | `912` |
| `psr0` | `0.5727975143821643` |
| `trades` | `219` |
| `win_rate_pct` | `48.401826484018265` |
| `profit_factor` | `1.0280722315631754` |
| `gross_profit_usd` | `1393.6141277191152` |
| `gross_loss_usd` | `1355.56051893371` |
| `net_pnl_usd` | `38.05360878540503` |
| `avg_trade_return_pct` | `0.018476656082540937` |
| `median_trade_return_pct` | `-0.07914069157976795` |
| `avg_win_pct` | `1.311321815448786` |
| `avg_loss_pct` | `-1.194280750048627` |
| `avg_win_usd` | `13.147303091689766` |
| `avg_loss_usd` | `-11.996110787023982` |
| `expectancy_usd` | `0.17376077070961202` |
| `avg_bars_held` | `7.602739726027397` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.0959637940248945` |
| `trade_tstat` | `0.18124133157343833` |
| `win_rate_ci95_low_pct` | `41.86789433224716` |
| `win_rate_ci95_high_pct` | `54.99085895493515` |
| `long_trades` | `111` |
| `long_profit_factor` | `0.9924563338241464` |
| `long_net_pnl_usd` | `-5.384612248153623` |
| `short_trades` | `108` |
| `short_profit_factor` | `1.067685236625158` |
| `short_net_pnl_usd` | `43.43822103355857` |
| `exit_reasons.LC Exit` | `92` |
| `exit_reasons.SL` | `66` |
| `exit_reasons.TP` | `61` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1665` |
| `exposure_pct` | `7.607255448439713` |
| `subperiods.2023.net_return_pct` | `-0.6234821086940623` |
| `subperiods.2023.sharpe` | `-0.5962055472873198` |
| `subperiods.2023.trades` | `65` |
| `subperiods.2023.profit_factor` | `0.8372056507479363` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `2.0640921294277748` |
| `subperiods.2024.sharpe` | `1.3262426687254845` |
| `subperiods.2024.trades` | `94` |
| `subperiods.2024.profit_factor` | `1.372040619758239` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.0324637813462378` |
| `subperiods.2025H1.sharpe` | `-1.2487838671741414` |
| `subperiods.2025H1.trades` | `60` |
| `subperiods.2025H1.profit_factor` | `0.7513931157275694` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.565542778760155` |
| `stress.sharpe` | `-0.726230798512324` |
| `stress.profit_factor` | `0.8296708322937868` |
| `stress.trades` | `219` |
| `stress.max_dd_pct` | `3.0482622442590035` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2333443999959854` |
| `signals_runtime_s` | `2.1679368000040995` |

### Critic verdict

RUN: 13
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.116 (vs run11 base 0.213, Δ-0.097; vs incumbent run06 0.226, Δ-0.110). PF 1.028 (down from 1.053, still clears G2). PSR0 0.573 (down from 0.632), trade_tstat 0.181 (down from 0.329). 7th consecutive run below the 0.276 bar.
- Drawdown: max_dd 1.85% (worse than run11's 1.53%), duration flat 392d. Skew 0.483 (weaker than 0.821), kurtosis 16.3 (worse).
- Significance: trades 219→219 — identical count, and the entry set is essentially untouched (see below), so this is a clean, well-isolated single-lever test.
- Robustness: 2023 and 2024 are BYTE-IDENTICAL to run11 to 10+ decimal places (net_return_pct, sharpe, trades, PF all match exactly) — meaning no LC-flip exit ever fired before the 12-bar timer in those two years under run11's config; removing the flip channel had zero effect there. The ENTIRE regression is concentrated in 2025H1: -0.713%→-1.032% (worse), PF 0.814→0.751 (worse), trade count unchanged at 60. Long PF fell below 1.0 (1.035→0.992, net +$24.0→-$5.4); short PF flat (1.073→1.068). Stress worse (-2.252%→-2.566%), still fails G3.

MECHANISM RULING: REFUTED, and cleanly so. The tuner's hypothesis was that LC-flip exits are a noisy channel cutting good trades early. The evidence shows the opposite in the only period they mattered: in 2025H1, forcing full 12-bar holds (removing flips) made results WORSE, not better — flip exits were doing useful early-loss-cutting there, not noise-cutting winners. Exit role has now had three structural probes (hold+TP in 02 = confirmed helpful; SL widening in 03 = refuted; flip removal in 13 = refuted) — the exit *mode* is settled; only magnitude calibration remains untested.

WEAKNESSES: Regression fully attributable to one sub-period, cleanly isolated — useful negative result, but still a regression from the best-so-far neighborhood.

DEMANDS FOR NEXT CONFIG: (1) Revert exitMode to 'Either (LC Default)' (run11 base). (2) Do not re-test flip-removal or SL-widening — both refuted. (3) Try `riskTpMult`/`riskSlMult` magnitude recalibration (e.g., TP 2.0-2.5 to lock in the already-favorable ~1.3% avg win faster) instead of structural exit changes.

PLATEAU ASSESSMENT — untested levers judged mechanistically credible AND likely to move PF-ex-top-2 above 1.0 (not just reshape the book): (1) LC feature TYPE/ParamA-B changes (distinct from the refuted count-reduction in run12) — untouched since run01, directly determines KNN signal discrimination, the most upstream lever in the whole model. (2) `wtObLevel2`/`wtOsLevel2` tightening — could filter marginal "not overextended" entries let in by run05's mode loosening, raising typical-trade quality without collapsing count. (3) `riskTpMult` recalibration (above) — untested magnitude space on a structurally-confirmed exit mode. (4) `wwvMethod`/`wwvAvgLen` (distinct from the tested on/off threshold) — could sharpen confirmation specifically in choppy 2025H1. None of these are guaranteed, but each has a distinct, testable mechanism for raising the sub-1.0 core edge, not just redistributing trades — so conviction that further search is noise-mining is NOT yet warranted. Best (fallback) = run06, sharpe 0.226; 7 consecutive non-improving runs. Budget: 12/25 remain. PLATEAU REJECTED — continue.

---

RUN: 13 (REVISED — incorporating orchestrator's per-trade join diagnostics)
VERDICT: CONTINUE
SCORECARD (updated): Sharpe 0.116 vs run11 0.213 (Δ-0.097) is now understood to come from exactly 2 trades, not a distributional shift — 217/219 entries, exit times, and bars_held are byte-identical to run11. This is materially different from what the metrics.json comparison alone suggested (a 2025H1-wide effect); it is narrower and more mechanically precise than my prior verdict characterized it.

CORRECTED MECHANISM RULING: exitMode is effectively INERT on this base, not a genuine structural exit-mechanism test. In run11 ('Either'), of 94 "LC Exit"-labeled closes, 92 were timer-expiry (bars_held=12) and only 2 were genuine LC-flip closes (9, 10 bars) — the flip channel almost never fires before the 12-bar timer here. Run13 ('LC Fixed Hold') simply let those 2 trades run into their stops: long 2025-01-20 -$5.77→-$35.30 (SL), short 2025-05-19 -$14.48→-$17.43 (SL), summing to -$32.47 ≈ the entire net change ($70.42→$38.05). Both genuine flips were protective (cut a loss before it got worse); removing them made both trades worse, not better. The tuner's premise ("flip exits are the noisy channel") is refuted directly by run11's own exit distribution — there was barely a flip channel to be noisy. My prior "3rd exit-mechanism probed, mode is settled" framing overstated what this run tested; correct framing: run13 is a 2-trade perturbation confirming flip-exits (rare as they are) are protective, and that the *real* exit-role structure is the 12-bar timer + SL + TP, not exit mode.

REVISED CONCENTRATION EVIDENCE: net ex-top-2 got markedly worse: -$19.32 (run11) → -$51.56 (run13); PF-ex-top-2 0.985→0.962 — a real degradation in the "typical trade" core, driven entirely by those same 2 trades moving from small losses to larger ones. Median trade unchanged (-0.079% both runs), confirming the bulk of the book is untouched.

WEAKNESSES: My original run13 verdict was directionally correct (regression, mechanism refuted) but attributed it to a sub-period-wide effect when it was in fact a 2-trade perturbation — a useful correction for future concentration-sensitivity given how much a couple of trades move every headline number in this study.

DEMANDS FOR NEXT CONFIG (unchanged, sharpened): (1) Revert exitMode to 'Either (LC Default)' (run11 base) — confirmed inert/refuted as a lever here, don't re-test. (2) The only remaining exit-role levers with real mechanism are `exitHoldBars` (magnitude) and `riskTpMult`/`riskSlMult` (magnitude) — not mode, since the flip channel barely exists at 12-bar hold. (3) Treat any future exit-role proposal skeptically unless it changes the 92/64/61 timer/SL/TP split materially.

PLATEAU ASSESSMENT (unchanged from prior verdict, reinforced): Best (fallback) = run06, sharpe 0.226; 7 consecutive non-improving runs; budget 12/25 remain. The sharper diagnostic strengthens rather than weakens the case that search isn't exhausted — this was a near-null test, not a real probe of the exit role's remaining potential. PLATEAU REJECTED — continue, prioritizing LC feature type/param, WT threshold, and riskTpMult/exitHoldBars magnitude levers as listed previously.

---

## Run 14

- run id: `run_14`
- timestamp (UTC): `2026-09-13T17:39:22Z`
- config hash: `a68d8fa86cd2`
- eligible: **NO**
- runtime_s: `2.2613861999998335`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskTpMult` | `2.0` | `3.0` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 2.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `219` | PASS |
| G2 | profit_factor > 1.0 | `0.959748415406435` | FAIL |
| G3 | stress.net_return_pct > 0 | `-3.2953205670823493` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9949.483925669301` |
| `net_return_pct` | `-0.5051607433069871` |
| `cagr_pct` | `-0.2026207325552365` |
| `ann_vol_pct` | `1.1690364266927626` |
| `sharpe` | `-0.16753922166636226` |
| `sortino` | `-0.2236171898180049` |
| `max_dd_pct` | `1.4266614554319323` |
| `max_dd_duration_days` | `406.6666666666667` |
| `calmar` | `-0.14202439673670975` |
| `sharpe_daily` | `-0.008769403659231866` |
| `skew` | `-0.5940100697116731` |
| `kurtosis` | `12.450327984014606` |
| `n_days` | `912` |
| `psr0` | `0.39537081659265993` |
| `trades` | `219` |
| `win_rate_pct` | `52.054794520547944` |
| `profit_factor` | `0.959748415406435` |
| `gross_profit_usd` | `1204.4922648630295` |
| `gross_loss_usd` | `1255.0083391937148` |
| `net_pnl_usd` | `-50.516074330685406` |
| `avg_trade_return_pct` | `-0.022253294317867902` |
| `median_trade_return_pct` | `0.12244880386725386` |
| `avg_win_pct` | `1.0630947116306766` |
| `avg_loss_pct` | `-1.2006311293477163` |
| `avg_win_usd` | `10.565721621605523` |
| `avg_loss_usd` | `-11.952460373273475` |
| `expectancy_usd` | `-0.23066700607618906` |
| `avg_bars_held` | `6.287671232876712` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `0.8839788036638218` |
| `trade_tstat` | `-0.2490104306205782` |
| `win_rate_ci95_low_pct` | `45.46004429621583` |
| `win_rate_ci95_high_pct` | `58.57870147740688` |
| `long_trades` | `111` |
| `long_profit_factor` | `0.9778068315160443` |
| `long_net_pnl_usd` | `-14.15419570836405` |
| `short_trades` | `108` |
| `short_profit_factor` | `0.9410891514956315` |
| `short_net_pnl_usd` | `-36.36187862232135` |
| `exit_reasons.LC Exit` | `70` |
| `exit_reasons.SL` | `61` |
| `exit_reasons.TP` | `88` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1377` |
| `exposure_pct` | `6.291405857358249` |
| `subperiods.2023.net_return_pct` | `-0.862229335019915` |
| `subperiods.2023.sharpe` | `-0.9435934654620325` |
| `subperiods.2023.trades` | `65` |
| `subperiods.2023.profit_factor` | `0.7667019203198945` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `0.6749019676510315` |
| `subperiods.2024.sharpe` | `0.5172851579137774` |
| `subperiods.2024.trades` | `94` |
| `subperiods.2024.profit_factor` | `1.1245999107335745` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.31261798410426866` |
| `subperiods.2025H1.sharpe` | `-0.47425024212311717` |
| `subperiods.2025H1.trades` | `60` |
| `subperiods.2025H1.profit_factor` | `0.9104541525327513` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-3.2953205670823493` |
| `stress.sharpe` | `-1.1144413016396875` |
| `stress.profit_factor` | `0.7636908946950602` |
| `stress.trades` | `219` |
| `stress.max_dd_pct` | `3.567729257320318` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.2613861999998335` |
| `signals_runtime_s` | `2.193601300008595` |

### Critic verdict

RUN: 14
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.213(run11)→-0.168 (Δ-0.380 — the single worst regression of any probe since run06, flips the whole family negative); PF 1.053→0.960 (drops BELOW 1 for the first time since run06 — G2 now FAILS, in addition to G3/G4). PSR0 0.632→0.395 (worst since run04), trade_tstat 0.329→-0.249 (flips negative). 8th consecutive run below the 0.276 bar, and by far the worst of the eight.
- Drawdown: max_dd 1.53%→1.43% (slightly better — tighter TP does reduce variance), duration worse 392→407d. Skew flips 0.821→-0.594 (fat left tail is back), kurtosis 15.5→12.5 (better).
- Significance: trades 219→219 (same count/entries), win rate UP 48.4%→52.1%, but payoff ratio collapsed 1.123→0.884 (avg win 1.31%→1.06%, avg loss flat ~-1.17%→-1.20%).
- Robustness: 2024 gutted (2.064%→0.675%, PF 1.372→1.125); 2023 worse (-0.623%→-0.862%); 2025H1 actually the best of any run yet (-0.713%→-0.313%, closest sub-period near-flip so far) but still negative — net effect: G4 stays 1/3. Long PF 1.035→0.978, short PF 1.073→0.941 — both now below 1.0. Stress much worse (-2.252%→-3.295%), fails G3 by a wider margin.

MECHANISM RULING — nuanced, not a clean refutation: exit mix moved exactly as predicted (TP 61→88, +27, within the tuner's 85-100 forecast; SL only 64→61, modest pre-emption; LC/timer 94→70). And the median trade DID improve as hypothesized: -0.079%→+0.122% (run11→run14), confirming tighter TP raises the *typical* trade. But the aggregate collapsed because avg win shrank far more than avg loss did, destroying the tail-driven profitability this entire parameter neighborhood has depended on since run06. This is the clearest confirmation yet of the concentration diagnosis built over runs 06-13: the edge here lives almost entirely in a handful of large winners, and capping them (rather than filtering entries) directly destroys it. REFUTED as a net-positive change, but mechanistically informative — it proves the "core" edge (PF-ex-top-2, persistently <1 across 06/07/09/11/13) is real and the strategy has no cushion once tail wins are capped.

DEMANDS FOR NEXT CONFIG: (1) Revert riskTpMult to 3.0 (run11 base). (2) Given tight TP hurts, test the OPPOSITE direction — riskTpMult 4.0-5.0 or riskUseTp=false with a longer `exitHoldBars` (16-20), to see if giving tail winners MORE room (rather than less) raises the core edge instead of just relying on luck. (3) LC feature TYPE/ParamA-B and WT ob/os cap tightening remain the top untested, mechanistically distinct levers.

PLATEAU ASSESSMENT — updated: riskTpMult downward is now tested and clearly refuted. Remaining credible, untested levers likely to move PF-ex-top-2 above 1.0: (1) LC feature TYPE/params (untouched), (2) `wtObLevel2`/`wtOsLevel2` tightening (untouched), (3) `wwvMethod`/`wwvAvgLen` (untouched), (4) riskTpMult WIDENING / TP-off with longer hold (new hypothesis from this run's own evidence). Best (fallback) = run06, sharpe 0.226; 8 consecutive non-improving runs; 11/25 slots remain. PLATEAU REJECTED — continue, but budget discipline matters: if the next 2-3 targeted tests also fail to lift PF-ex-top-2 above 1.0, plateau becomes the correct call.

---

## Run 15

- run id: `run_15`
- timestamp (UTC): `2026-09-13T17:42:16Z`
- config hash: `35ecea2963da`
- eligible: **NO**
- runtime_s: `2.247132500007865`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `20` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 20,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": false,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `219` | PASS |
| G2 | profit_factor > 1.0 | `0.9224940497622983` | FAIL |
| G3 | stress.net_return_pct > 0 | `-4.423482736141448` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9876.80176020421` |
| `net_return_pct` | `-1.2319823979579092` |
| `cagr_pct` | `-0.49523499417067907` |
| `ann_vol_pct` | `1.6622762079819693` |
| `sharpe` | `-0.29016302866292415` |
| `sortino` | `-0.44152449614981304` |
| `max_dd_pct` | `2.246960005695531` |
| `max_dd_duration_days` | `872.8333333333334` |
| `calmar` | `-0.22040222919650165` |
| `sharpe_daily` | `-0.015187827065340437` |
| `skew` | `1.2315992502406843` |
| `kurtosis` | `14.55626855723739` |
| `n_days` | `912` |
| `psr0` | `0.3249113595568728` |
| `trades` | `219` |
| `win_rate_pct` | `42.465753424657535` |
| `profit_factor` | `0.9224940497622983` |
| `gross_profit_usd` | `1466.3344272825177` |
| `gross_loss_usd` | `1589.5326670782888` |
| `net_pnl_usd` | `-123.19823979577124` |
| `avg_trade_return_pct` | `-0.05489415593353307` |
| `median_trade_return_pct` | `-0.3641015799214294` |
| `avg_win_pct` | `1.5830933870632153` |
| `avg_loss_pct` | `-1.263884961478752` |
| `avg_win_usd` | `15.76703685250019` |
| `avg_loss_usd` | `-12.615338627605466` |
| `expectancy_usd` | `-0.5625490401633391` |
| `avg_bars_held` | `14.442922374429223` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `1.2498306480650494` |
| `trade_tstat` | `-0.4379957826158535` |
| `win_rate_ci95_low_pct` | `36.10451213361835` |
| `win_rate_ci95_high_pct` | `49.08675336309833` |
| `long_trades` | `111` |
| `long_profit_factor` | `1.0013381665623518` |
| `long_net_pnl_usd` | `1.0842399006482903` |
| `short_trades` | `108` |
| `short_profit_factor` | `0.840518279168251` |
| `short_net_pnl_usd` | `-124.28247969641941` |
| `exit_reasons.LC Exit` | `131` |
| `exit_reasons.SL` | `83` |
| `exit_reasons.TP` | `0` |
| `exit_reasons.Reverse` | `4` |
| `exit_reasons.WindowEnd` | `1` |
| `bars_in_position` | `3164` |
| `exposure_pct` | `14.456069813131082` |
| `subperiods.2023.net_return_pct` | `-0.6634311987437136` |
| `subperiods.2023.sharpe` | `-0.4603497490799095` |
| `subperiods.2023.trades` | `65` |
| `subperiods.2023.profit_factor` | `0.8502642545870122` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `0.46068186962546775` |
| `subperiods.2024.sharpe` | `0.2586805219632695` |
| `subperiods.2024.trades` | `94` |
| `subperiods.2024.profit_factor` | `1.0641414005336207` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.0282930466379736` |
| `subperiods.2025H1.sharpe` | `-1.1888434576244087` |
| `subperiods.2025H1.trades` | `60` |
| `subperiods.2025H1.profit_factor` | `0.7630082362096084` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-4.423482736141448` |
| `stress.sharpe` | `-1.0651873806675831` |
| `stress.profit_factor` | `0.7485517908711617` |
| `stress.trades` | `219` |
| `stress.max_dd_pct` | `5.280478961825463` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.247132500007865` |
| `signals_runtime_s` | `2.1799311000067974` |

### Critic verdict

RUN: 15
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe -0.290 (vs run11 base 0.213, Δ-0.503; vs run14's tight-TP -0.168, Δ-0.122 further down; vs incumbent run06 0.226, Δ-0.516) — the worst result in the entire run06+ family, and among the worst of all 15 runs. PF 0.922 (<1, G2 fails). PSR0 0.325 (worst since run02/03), trade_tstat -0.438 (clearly negative point estimate). 9th consecutive run below the 0.276 bar, and this is the low point of the sequence.
- Drawdown: max_dd 2.25% (worse than run11's 1.53%), duration EXPLODED 392d→873d (worst since the pre-run06 era). Skew 1.232 (highest positive skew of any run — tail winners got enormous, e.g. one trade +7.12%/+$71.19 that TP would have capped at +$9.55), kurtosis 14.6.
- Significance: trades 219→219 (same entry book as run11/run13/run14, cleanly isolated). Win rate cratered 48.4%→42.5%; payoff ratio actually IMPROVED 1.123→1.250 (avg win 1.31%→1.58%, avg loss -1.17%→-1.26%) — but the win-rate collapse (-5.9pp) outweighs the payoff gain, exactly the arithmetic PF=payoff×wr/(1-wr) predicts (1.25×0.425/0.575≈0.92, matches).
- Robustness: exit mix matched the tuner's forecast closely (TP 0, LC/timer 131 vs ~125 predicted, SL 83 vs 80-90 predicted) — good mechanical prediction, decisively bad financial outcome. 2024 gutted again (2.064%→0.461%); 2023 flat (-0.623%→-0.663%); 2025H1 worse (-0.713%→-1.028%). G4 still 1/3. Short side collapsed hardest (PF 1.073→0.841, net +$46.4→-$124.3) — longer holds expose mean-reversion shorts to more adverse continuation in this bull market. Stress much worse (-2.252%→-4.423%), exposure nearly doubled (7.6%→14.5%).

RULING ON THE EXIT ROLE: Both exit-magnitude directions have now been tested on the identical 219-trade book: tighter TP (run14, riskTpMult 2.0, Sharpe -0.168) and no-TP/longer-hold (run15, riskUseTp=false + exitHoldBars=20, Sharpe -0.290) both underperform run11's middle setting (exitHoldBars=12, riskTpMult=3.0, riskSlMult=2.0, Sharpe 0.213) by a wide margin. Combined with run03's SL-widening (refuted) and run13's flip-removal (near-null), this is five convergent exit-magnitude/mode probes all pointing to the SAME conclusion: run06/11's exit settings sit at a local optimum for this entry book. The exit role should be considered SETTLED — revert to it, and stop spending budget on further exit-magnitude tuning; no in-bounds exit lever remains with a credible untested mechanism.

RULING ON PLATEAU: NOT yet warranted. My run-14 "2-3 targeted tests" commitment concerned exit-role variants specifically (both now tested and refuted) — it did not cover the other three still-fully-untested, mechanistically distinct hypotheses: LC feature TYPE/params (entry role), `wtObLevel2`/`wtOsLevel2` tightening (timing role), and `wwvMethod`/`wwvAvgLen` (confirmation role). None of these have been tried even once. Given 6 roles require probing and 3 remain genuinely untested with credible mechanisms, PLATEAU is REJECTED. Best (fallback) = run06, sharpe 0.226; 9 consecutive non-improving runs; 10/25 slots remain.

DEMANDS FOR NEXT CONFIG: (1) Revert to run11 base (exitHoldBars=12, riskUseTp=true, riskTpMult=3.0). (2) Test LC feature TYPE swap (e.g., feature 5 RSI→WT) next — highest-leverage untested mechanism. (3) Reserve 1-2 of the remaining 10 slots for WT/WWV probes; if all three also fail to clear PF-ex-top-2 above 1.0, plateau at run06 becomes the correct call with ~5-6 slots to spare for OOS prep.

---

## Run 16

- run id: `run_16`
- timestamp (UTC): `2026-09-13T17:45:52Z`
- config hash: `c09b8bfadd29`
- eligible: **NO**
- runtime_s: `2.168855600000825`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcF1ParamA` | `50` | `14` |
| `lcF1String` | `ADX` | `RSI` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 50,
 "lcF1ParamB": 1,
 "lcF1String": "ADX",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 53,
 "wtOsLevel1": -60,
 "wtOsLevel2": -53,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `221` | PASS |
| G2 | profit_factor > 1.0 | `1.0071536339901737` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.8626664217112907` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10010.051290168907` |
| `net_return_pct` | `0.1005129016890649` |
| `cagr_pct` | `0.04024263396804617` |
| `ann_vol_pct` | `1.3991573091176084` |
| `sharpe` | `0.03572282821154277` |
| `sortino` | `0.052111544666024544` |
| `max_dd_pct` | `1.5324805464312141` |
| `max_dd_duration_days` | `401.7916666666667` |
| `calmar` | `0.026259800858002263` |
| `sharpe_daily` | `0.0018698182868502067` |
| `skew` | `0.5581093710307644` |
| `kurtosis` | `14.7535673400222` |
| `n_days` | `912` |
| `psr0` | `0.5225144860799149` |
| `trades` | `221` |
| `win_rate_pct` | `47.05882352941176` |
| `profit_factor` | `1.0071536339901737` |
| `gross_profit_usd` | `1415.1120163285805` |
| `gross_loss_usd` | `1405.0607261596665` |
| `net_pnl_usd` | `10.051290168913962` |
| `avg_trade_return_pct` | `0.00574271514888744` |
| `median_trade_return_pct` | `-0.20392501051142187` |
| `avg_win_pct` | `1.3612106469828675` |
| `avg_loss_pct` | `-1.1991176687035392` |
| `avg_win_usd` | `13.606846310851735` |
| `avg_loss_usd` | `-12.009066035552705` |
| `expectancy_usd` | `0.04548095099056091` |
| `avg_bars_held` | `7.479638009049774` |
| `max_consecutive_losses` | `5` |
| `payoff_ratio` | `1.1330478382389455` |
| `trade_tstat` | `0.055068492394803555` |
| `win_rate_ci95_low_pct` | `40.58468124883838` |
| `win_rate_ci95_high_pct` | `53.6334669217945` |
| `long_trades` | `115` |
| `long_profit_factor` | `1.0704873190603585` |
| `long_net_pnl_usd` | `49.07195356742163` |
| `short_trades` | `106` |
| `short_profit_factor` | `0.9449544420728863` |
| `short_net_pnl_usd` | `-39.020663398507615` |
| `exit_reasons.LC Exit` | `90` |
| `exit_reasons.SL` | `69` |
| `exit_reasons.TP` | `62` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1653` |
| `exposure_pct` | `7.552428382144652` |
| `subperiods.2023.net_return_pct` | `-0.61300204104906` |
| `subperiods.2023.sharpe` | `-0.5754645476205683` |
| `subperiods.2023.trades` | `65` |
| `subperiods.2023.profit_factor` | `0.838686002368265` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.4552346681160122` |
| `subperiods.2024.sharpe` | `0.9096052934062854` |
| `subperiods.2024.trades` | `96` |
| `subperiods.2024.profit_factor` | `1.2290579831036266` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.7267430698854493` |
| `subperiods.2025H1.sharpe` | `-0.9332608542514325` |
| `subperiods.2025H1.trades` | `60` |
| `subperiods.2025H1.profit_factor` | `0.8138388309792568` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.8626664217112907` |
| `stress.sharpe` | `-0.8092178788429012` |
| `stress.profit_factor` | `0.8165672963771031` |
| `stress.trades` | `221` |
| `stress.max_dd_pct` | `3.3439138477468378` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.168855600000825` |
| `signals_runtime_s` | `2.1004237000015564` |

### Critic verdict

RUN: 16
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.213(run11)→0.036 (Δ-0.178 — a clear regression, though the mildest of the last three probes; run14 was -0.168, run15 was -0.290). PF 1.053→1.007 (still >1, but barely — the weakest PF pass in the 06+ family). PSR0 0.632→0.523, trade_tstat 0.329→0.055 (essentially indistinguishable from zero). 10th consecutive run below the 0.276 bar.
- Drawdown: max_dd flat ~1.53%, duration flat ~402d. Skew 0.821→0.558 (weaker), kurtosis 15.5→14.75 (slightly better).
- Significance: trades 219→221 (close to the tuner's 85-95% overlap prediction — a well-isolated single-lever test), win rate 48.4%→47.1%.
- Robustness: Long PF IMPROVED (1.035→1.070, net +$24.0→+$49.1) — some support for the "trend-context" mechanism on the long side. But short PF collapsed below 1.0 (1.073→0.945, net +$46.4→-$39.0), erasing the long-side gain and then some. 2023 flat (-0.623%→-0.613%), 2024 worse (2.064%→1.455%), 2025H1 flat (-0.713%→-0.727%). G4 still 1/3. Stress worse (-2.252%→-2.863%), still fails G3.

RULING ON ENDGAME HYPOTHESIS (a) — LC feature type swap: FAILS the criterion. Headline PF (1.007) is now barely above 1.0 at all — given the consistent ~0.07 gap between headline PF and PF-ex-top-2 observed across every prior run in this family (run06: 1.060→0.983; run11: 1.053→0.985), PF-ex-top-2 for run16 is very likely still below 1.0 (≈0.93-0.94 by extrapolation; awaiting exact diagnostic). Sharpe, trade_tstat, PSR0, 2024, and stress all moved the wrong way vs run11. The mechanism (ADX-50 regime context sharpens neighbor matching) shows a plausible partial effect (long PF up) but is dominated by short-side damage — net, this is a refutation, not a confirmation. Hypothesis (a): REFUTED.

DEMANDS FOR NEXT CONFIG: (1) Revert to run11 base. (2) Proceed to endgame hypothesis (b): `wtObLevel2`/`wtOsLevel2` tightening — untested, distinct mechanism (timing role, not entry role), worth its own clean test given (a) is now closed. (3) Reserve the final slot for (c) WWV method/length only if (b) also fails to move PF-ex-top-2 above 1.0.

PLATEAU ASSESSMENT: Best (fallback) = run06, sharpe 0.226; 10 consecutive non-improving runs; 9/25 slots remain. Endgame status: (a) LC feature type — TESTED, REFUTED. (b) WT ob/os caps — untested. (c) WWV method/length — untested. Per the pre-committed endgame plan, PLATEAU is warranted only if (b) and (c) also fail to lift PF-ex-top-2 above 1.0. Two credible, mechanistically distinct, entirely untested hypotheses remain, so PLATEAU is REJECTED this run. Recommend testing (b) next with 8-9 slots still available, leaving adequate buffer (5-6 slots) after (b)/(c) for freeze + OOS regardless of outcome.

---

## Run 17

- run id: `run_17`
- timestamp (UTC): `2026-09-13T17:48:11Z`
- config hash: `b8376d7d48f5`
- eligible: **NO**
- runtime_s: `2.414003700003377`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtObLevel2` | `40` | `53` |
| `wtOsLevel2` | `-40` | `-53` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 40,
 "wtOsLevel1": -60,
 "wtOsLevel2": -40,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `188` | PASS |
| G2 | profit_factor > 1.0 | `1.0978413868104693` | PASS |
| G3 | stress.net_return_pct > 0 | `-1.422280889998273` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `2` | PASS |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10112.31560543362` |
| `net_return_pct` | `1.123156054336194` |
| `cagr_pct` | `0.44831121726971457` |
| `ann_vol_pct` | `1.2813062110424176` |
| `sharpe` | `0.3552631577661067` |
| `sortino` | `0.5537202380398549` |
| `max_dd_pct` | `1.492872202317197` |
| `max_dd_duration_days` | `325.7916666666667` |
| `calmar` | `0.30030113533754443` |
| `sharpe_daily` | `0.01859532355897215` |
| `skew` | `1.2645961607786051` |
| `kurtosis` | `18.284242352012676` |
| `n_days` | `912` |
| `psr0` | `0.7148271103257331` |
| `trades` | `188` |
| `win_rate_pct` | `47.87234042553192` |
| `profit_factor` | `1.0978413868104693` |
| `gross_profit_usd` | `1260.2511477945707` |
| `gross_loss_usd` | `1147.9355423609475` |
| `net_pnl_usd` | `112.31560543362315` |
| `avg_trade_return_pct` | `0.06056976849108794` |
| `median_trade_return_pct` | `-0.08370125455867955` |
| `avg_win_pct` | `1.3902283682967047` |
| `avg_loss_pct` | `-1.1605452721467233` |
| `avg_win_usd` | `14.002790531050785` |
| `avg_loss_usd` | `-11.713627983274975` |
| `expectancy_usd` | `0.59742343315757` |
| `avg_bars_held` | `7.680851063829787` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `1.1954272878602885` |
| `trade_tstat` | `0.5442438167208665` |
| `win_rate_ci95_low_pct` | `40.84589277494525` |
| `win_rate_ci95_high_pct` | `54.98399715125824` |
| `long_trades` | `95` |
| `long_profit_factor` | `1.1099950715003535` |
| `long_net_pnl_usd` | `63.23191551461955` |
| `short_trades` | `93` |
| `short_profit_factor` | `1.0856498002239299` |
| `short_net_pnl_usd` | `49.083689919003604` |
| `exit_reasons.LC Exit` | `80` |
| `exit_reasons.SL` | `54` |
| `exit_reasons.TP` | `54` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1444` |
| `exposure_pct` | `6.59752364417234` |
| `subperiods.2023.net_return_pct` | `0.03723546115321774` |
| `subperiods.2023.sharpe` | `0.04155451381014257` |
| `subperiods.2023.trades` | `58` |
| `subperiods.2023.profit_factor` | `1.0117628867608317` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.8326949157739802` |
| `subperiods.2024.sharpe` | `1.26737207975342` |
| `subperiods.2024.trades` | `78` |
| `subperiods.2024.profit_factor` | `1.3778145411397082` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-0.7337314604557887` |
| `subperiods.2025H1.sharpe` | `-1.045470089204105` |
| `subperiods.2025H1.trades` | `52` |
| `subperiods.2025H1.profit_factor` | `0.7840510788036048` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-1.422280889998273` |
| `stress.sharpe` | `-0.4346422677740231` |
| `stress.profit_factor` | `0.8891196238685607` |
| `stress.trades` | `188` |
| `stress.max_dd_pct` | `2.1378448445630416` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.414003700003377` |
| `signals_runtime_s` | `2.348676500012516` |

### Critic verdict

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

---

## Run 18

- run id: `run_18`
- timestamp (UTC): `2026-09-13T19:55:26Z`
- config hash: `6dc9b42cba6b`
- eligible: **NO**
- runtime_s: `5.963834299996961`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtObLevel2` | `45` | `53` |
| `wtOsLevel2` | `-45` | `-53` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 45,
 "wtOsLevel1": -60,
 "wtOsLevel2": -45,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "ATR",
 "wwvMethodValue": 14.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `203` | PASS |
| G2 | profit_factor > 1.0 | `1.0505665089055023` | PASS |
| G3 | stress.net_return_pct > 0 | `-2.103124326120287` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `10063.537076745339` |
| `net_return_pct` | `0.6353707674533915` |
| `cagr_pct` | `0.2539788133762766` |
| `ann_vol_pct` | `1.340943439466784` |
| `sharpe` | `0.1957286855928386` |
| `sortino` | `0.2943190456671208` |
| `max_dd_pct` | `1.6681681123559056` |
| `max_dd_duration_days` | `388.625` |
| `calmar` | `0.1522501308441807` |
| `sharpe_daily` | `0.010244907637643023` |
| `skew` | `0.8943463954472619` |
| `kurtosis` | `16.58161054731534` |
| `n_days` | `912` |
| `psr0` | `0.6219408347157237` |
| `trades` | `203` |
| `win_rate_pct` | `47.29064039408867` |
| `profit_factor` | `1.0505665089055023` |
| `gross_profit_usd` | `1320.042184979563` |
| `gross_loss_usd` | `1256.5051082342277` |
| `net_pnl_usd` | `63.53707674533535` |
| `avg_trade_return_pct` | `0.03234535434282933` |
| `median_trade_return_pct` | `-0.0979819161683366` |
| `avg_win_pct` | `1.365966255975107` |
| `avg_loss_pct` | `-1.1641743331029526` |
| `avg_win_usd` | `13.750439426870448` |
| `avg_loss_usd` | `-11.743038394712409` |
| `expectancy_usd` | `0.31299052583909037` |
| `avg_bars_held` | `7.635467980295567` |
| `max_consecutive_losses` | `6` |
| `payoff_ratio` | `1.1709439213842578` |
| `trade_tstat` | `0.3038863101711339` |
| `win_rate_ci95_low_pct` | `40.536828050383924` |
| `win_rate_ci95_high_pct` | `54.14508917128118` |
| `long_trades` | `103` |
| `long_profit_factor` | `1.01419173363998` |
| `long_net_pnl_usd` | `9.307984169698454` |
| `short_trades` | `100` |
| `short_profit_factor` | `1.0902868006772246` |
| `short_net_pnl_usd` | `54.22909257563695` |
| `exit_reasons.LC Exit` | `86` |
| `exit_reasons.SL` | `60` |
| `exit_reasons.TP` | `57` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1550` |
| `exposure_pct` | `7.081829396445379` |
| `subperiods.2023.net_return_pct` | `-0.006252015171737124` |
| `subperiods.2023.sharpe` | `-0.0010218977815257932` |
| `subperiods.2023.trades` | `59` |
| `subperiods.2023.profit_factor` | `0.9980513414623801` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `1.7815134358225793` |
| `subperiods.2024.sharpe` | `1.1600041718460081` |
| `subperiods.2024.trades` | `87` |
| `subperiods.2024.profit_factor` | `1.3269402317034809` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.1198993784410138` |
| `subperiods.2025H1.sharpe` | `-1.515927353720773` |
| `subperiods.2025H1.trades` | `57` |
| `subperiods.2025H1.profit_factor` | `0.7083452049898673` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.103124326120287` |
| `stress.sharpe` | `-0.6172701511028081` |
| `stress.profit_factor` | `0.8499419573823807` |
| `stress.trades` | `203` |
| `stress.max_dd_pct` | `2.720185436715594` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `5.963834299996961` |
| `signals_runtime_s` | `5.875195100001292` |

### Critic verdict

RUN: 18
VERDICT: CONTINUE
SCORECARD:
- Risk-adjusted: Sharpe 0.196 — BELOW run11's own baseline (0.213) despite ±45 being the midpoint between run11's ±53 and run17's ±40. PF 1.051 (down from run17's 1.098). trade_tstat 0.304, PSR0 0.622 — both between run11 and run17 as expected, but Sharpe itself is not. DSR of current best (still run17) ticks to 0.181 at N=18 (flat vs N=17's 0.179).
- Drawdown/tail: max_dd 1.67% (worse than both run11 1.53% and run17 1.49%), duration 389d. Skew 0.894, kurtosis 16.58 — between the two endpoints.
- Significance: trades 203 — within the tuner's predicted 195-210 range.
- Sub-period/long-short: 2023 -0.006% (nearly zero but still negative, doesn't flip), 2024 +1.782% (WORSE than both endpoints: run11 2.064%, run17 1.833%), 2025H1 -1.120% (WORSE than both endpoints: run11 -0.713%, run17 -0.734%). G4 REVERTS to 1/3 (fails) — the midpoint is not "between" run11 and run17 on two of three sub-periods, it's worse than both. Long PF 1.014 (weakest of the three settings, vs run11 1.035 and run17 1.110); short PF 1.090 (essentially matches run17's 1.086, both above run11's 1.073). Stress -2.10% (worse than run17 -1.42%, better than run11 -2.25%), G3 fails.

RULING ON TUNER'S PRE-STATED CRITERIA: REFUTED, decisively, on BOTH stated conditions simultaneously. (1) Sharpe 0.196 ≤ 0.213 — triggers the REFUTE threshold outright. (2) PF-ex-top-2 (self-derived: top-2 wins $46.32+$43.77=$90.09; (1320.04-90.09)/1256.51 ≈ 0.979) is BELOW 0.985 — also triggers REFUTE. The CONFIRM bar (sharpe≥0.28, PF-ex-top-2≥1.0) is missed by a wide margin on both counts. Worse: the sharpe path across the cap is NON-MONOTONIC — 0.213 (±53) → 0.196 (±45) → 0.355 (±40) — a dip at the midpoint followed by a sharp spike at the endpoint, not a smooth ramp. A genuine "filter overextended reversion entries" mechanism should produce roughly monotonic improvement as the cap tightens; a dip-then-spike shape is the classic signature of a narrow, coincidental sweet spot rather than a broad regime effect.

IMPLICATIONS FOR RUN 17'S CREDIBILITY: This materially weakens confidence in run17 as a genuine discovery. The mechanical selection rule still names run17 current best (0.355 > every other run, none eligible), and that stays unchanged — but my robustness judgment is that run17 should be treated as a likely fragile, narrowly-tuned local spike at exactly ±40, not a validated broad improvement. If FROZEN_PARAMS ultimately selects run17, the OOS result should be expected with real skepticism, and the writeup should flag this non-monotonicity explicitly as an overfitting risk rather than presenting run17 uncritically.

DEMANDS FOR NEXT CONFIG: (1) Do not fine-tune further around ±40 (e.g., ±38/±42) — a non-monotonic response there is noise-chasing, not signal-following. (2) Spend one of the remaining slots on the final endgame item (c): WWV method/length — the last genuinely untested, distinct mechanism. (3) Begin reserving slots for wrap-up (freeze + OOS) — after WWV, further search should be judged against a rising bar given DSR is flat at ~0.18 and this run just supplied direct evidence of fragility in the neighborhood of the current best.

PLATEAU ASSESSMENT: Best (fallback, mechanical) = run17, sharpe 0.355, but now flagged fragile. 7/25 slots remain. PLATEAU still REJECTED — one credible untested lever (WWV) remains — but this is very likely the second-to-last substantive test before plateau becomes appropriate.

---

ORCHESTRATOR NOTE (not critic text): per-trade nesting confirms the critic's reading — run 17 (±40) ⊆ run 18 (±45) ⊆ run 11 (±53), identical exits on all shared trades; band ±53→±45 removed 16 net-winning trades (+$7.63), band ±45→±40 removed 15 net-losing trades (−$48.54, median −0.435 %). Run 18 PF-ex-top-2 = 0.979 (exact), net ex-top-2 −$26.55.

---

## Run 19

- run id: `run_19`
- timestamp (UTC): `2026-09-13T19:59:21Z`
- config hash: `18fd840634a9`
- eligible: **NO**
- runtime_s: `2.309410799993202`
- data sha256: `82423f2f69930d69d7149055a6b08c77c33a973e4e0fa631401fef25bc44a64f`

### Params diff vs defaults

| parameter | value | Pine default |
|---|---|---|
| `exitHoldBars` | `12` | `4` |
| `lcNeighbors` | `12` | `8` |
| `nwBandwidth` | `5` | `8` |
| `nwRequirePriceSide` | `true` | `false` |
| `nwSlopeLen` | `3` | `1` |
| `riskUseTp` | `true` | `false` |
| `wtObLevel2` | `40` | `53` |
| `wtOsLevel2` | `-40` | `-53` |
| `wtTimingMode` | `Not Overextended Only` | `Recent Cross + Not Overextended` |
| `wwvMethod` | `Part of Price` | `ATR` |
| `wwvMethodValue` | `400.0` | `14.0` |

<details><summary>Full parameter set (80 keys)</summary>

```json
{
 "allowLongs": true,
 "allowShorts": true,
 "exitHoldBars": 12,
 "exitMode": "Either (LC Default)",
 "lcAdxLen": 14,
 "lcAdxThreshold": 20,
 "lcDistQuantile": 0.75,
 "lcEntryWindow": 2,
 "lcF1ParamA": 14,
 "lcF1ParamB": 1,
 "lcF1String": "RSI",
 "lcF2ParamA": 10,
 "lcF2ParamB": 11,
 "lcF2String": "WT",
 "lcF3ParamA": 20,
 "lcF3ParamB": 1,
 "lcF3String": "CCI",
 "lcF4ParamA": 20,
 "lcF4ParamB": 2,
 "lcF4String": "ADX",
 "lcF5ParamA": 9,
 "lcF5ParamB": 1,
 "lcF5String": "RSI",
 "lcFeatureCount": 5,
 "lcHorizon": 4,
 "lcIncludeFullHistory": false,
 "lcMaxBarsBack": 2000,
 "lcNeighbors": 12,
 "lcRegimeSrc": "ohlc4",
 "lcRegimeThreshold": -0.1,
 "lcSource": "close",
 "lcSpacing": 4,
 "lcUseAdxFilter": false,
 "lcUseRegimeFilter": true,
 "lcUseVolFilter": true,
 "lcVolMaxLen": 10,
 "lcVolMinLen": 1,
 "nwBandwidth": 5,
 "nwHMult": 2.0,
 "nwKernelType": "Gaussian",
 "nwLookback": 50,
 "nwRelWeight": 8.0,
 "nwRequirePriceSide": true,
 "nwSlopeLen": 3,
 "nwSrc": "close",
 "riskAtrLen": 14,
 "riskSlMult": 2.0,
 "riskTpMult": 3.0,
 "riskUseSl": true,
 "riskUseTp": true,
 "sqzBbLen": 20,
 "sqzBbMult": 2.0,
 "sqzKcLen": 20,
 "sqzKcMult": 1.5,
 "sqzRegimeMode": "Squeeze Off",
 "sqzReleaseWindow": 5,
 "sqzReplicateQuirk": true,
 "sqzRequireMomExpansion": false,
 "sqzSrc": "close",
 "sqzUseTrueRange": true,
 "wtCciConst": 0.015,
 "wtCrossWindow": 5,
 "wtExtLevelSel": "Level 2",
 "wtN1": 10,
 "wtN2": 21,
 "wtObLevel1": 60,
 "wtObLevel2": 40,
 "wtOsLevel1": -60,
 "wtOsLevel2": -40,
 "wtSigLen": 4,
 "wtSrc": "hlc3",
 "wtTimingMode": "Not Overextended Only",
 "wwvAvgLen": 20,
 "wwvAvgMult": 1.0,
 "wwvMethod": "Part of Price",
 "wwvMethodValue": 400.0,
 "wwvNormalize": false,
 "wwvPriceSource": "Close",
 "wwvUseTrueRange": "Auto",
 "wwvUseVolThreshold": false
}
```

</details>

### Gates

| gate | rule | value | pass |
|---|---|---|---|
| G1 | trades >= 100 | `169` | PASS |
| G2 | profit_factor > 1.0 | `0.9641801007806049` | FAIL |
| G3 | stress.net_return_pct > 0 | `-2.6600076399791006` | FAIL |
| G4 | >= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0 | `1` | FAIL |

### Metrics (exact)

| metric | value |
|---|---|
| `period` | `IS` |
| `window_start` | `2023-01-01 00:00:00+00:00` |
| `window_end` | `2025-06-30 23:00:00+00:00` |
| `first_bar_time` | `2023-01-01 00:00:00+00:00` |
| `last_bar_time` | `2025-06-30 23:00:00+00:00` |
| `window_bars` | `21887` |
| `start_equity` | `10000.0` |
| `final_equity` | `9960.049814249303` |
| `net_return_pct` | `-0.39950185750696754` |
| `cagr_pct` | `-0.16018987544311747` |
| `ann_vol_pct` | `1.2752749013205484` |
| `sharpe` | `-0.11925760583958442` |
| `sortino` | `-0.17184413768991758` |
| `max_dd_pct` | `2.1137024387927084` |
| `max_dd_duration_days` | `414.5` |
| `calmar` | `-0.07578638908824543` |
| `sharpe_daily` | `-0.0062422283847272855` |
| `skew` | `0.2186102168970936` |
| `kurtosis` | `24.507669487907574` |
| `n_days` | `912` |
| `psr0` | `0.42533726687895973` |
| `trades` | `169` |
| `win_rate_pct` | `46.74556213017752` |
| `profit_factor` | `0.9641801007806049` |
| `gross_profit_usd` | `1075.3568536691428` |
| `gross_loss_usd` | `1115.3070394198435` |
| `net_pnl_usd` | `-39.9501857507009` |
| `avg_trade_return_pct` | `-0.02247864051355137` |
| `median_trade_return_pct` | `-0.20392501051142187` |
| `avg_win_pct` | `1.3609206541902512` |
| `avg_loss_pct` | `-1.236795799198` |
| `avg_win_usd` | `13.6121120717613` |
| `avg_loss_usd` | `-12.39230043799826` |
| `expectancy_usd` | `-0.2363916316609521` |
| `avg_bars_held` | `7.491124260355029` |
| `max_consecutive_losses` | `8` |
| `payoff_ratio` | `1.0984330262057524` |
| `trade_tstat` | `-0.1874941035295319` |
| `win_rate_ci95_low_pct` | `39.379266514893665` |
| `win_rate_ci95_high_pct` | `54.25651967028811` |
| `long_trades` | `87` |
| `long_profit_factor` | `1.11789380774113` |
| `long_net_pnl_usd` | `61.56177716919852` |
| `short_trades` | `82` |
| `short_profit_factor` | `0.8288529443336772` |
| `short_net_pnl_usd` | `-101.51196291989943` |
| `exit_reasons.LC Exit` | `68` |
| `exit_reasons.SL` | `53` |
| `exit_reasons.TP` | `48` |
| `exit_reasons.Reverse` | `0` |
| `exit_reasons.WindowEnd` | `0` |
| `bars_in_position` | `1266` |
| `exposure_pct` | `5.784255494128935` |
| `subperiods.2023.net_return_pct` | `-1.0019820359614462` |
| `subperiods.2023.sharpe` | `-0.9937939270559377` |
| `subperiods.2023.trades` | `52` |
| `subperiods.2023.profit_factor` | `0.7098817636967978` |
| `subperiods.2023.bars` | `8759` |
| `subperiods.2024.net_return_pct` | `2.4483378676161793` |
| `subperiods.2024.sharpe` | `1.749730530845185` |
| `subperiods.2024.trades` | `71` |
| `subperiods.2024.profit_factor` | `1.5946060044862234` |
| `subperiods.2024.bars` | `8784` |
| `subperiods.2025H1.net_return_pct` | `-1.7957927722505596` |
| `subperiods.2025H1.sharpe` | `-2.4471985722972676` |
| `subperiods.2025H1.trades` | `46` |
| `subperiods.2025H1.profit_factor` | `0.4972942317522977` |
| `subperiods.2025H1.bars` | `4344` |
| `buy_and_hold.net_return_pct` | `547.7329814161362` |
| `buy_and_hold.sharpe` | `1.7868532260277095` |
| `buy_and_hold.max_dd_pct` | `32.31069072207684` |
| `buy_and_hold.sortino` | `2.9197571846708037` |
| `buy_and_hold.cagr_pct` | `111.32883764210595` |
| `stress.costs.commission_pct` | `0.1` |
| `stress.costs.slip_mode` | `bps` |
| `stress.costs.slip_value` | `5` |
| `stress.net_return_pct` | `-2.6600076399791006` |
| `stress.sharpe` | `-0.8261928575831242` |
| `stress.profit_factor` | `0.785417375278694` |
| `stress.trades` | `169` |
| `stress.max_dd_pct` | `2.804779217095632` |
| `costs.commission_pct` | `0.075` |
| `costs.slip_mode` | `ticks` |
| `costs.slip_value` | `2` |
| `costs.mintick` | `0.01` |
| `runtime_s` | `2.309410799993202` |
| `signals_runtime_s` | `2.237415700001293` |

### Critic verdict

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

---
