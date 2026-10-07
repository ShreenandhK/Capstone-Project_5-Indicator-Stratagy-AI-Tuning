// ================================================================== CONTENT (20-page version)
for (const k of ["jdehorty", "lbsqz", "lbwt"]) REFS[k] = REFS[k].replace(" [Online]. Available: https://www.tradingview.com/scripts/", "");
REFS.sebi = "SEBI, “Updated SEBI study reveals 93% of individual traders incurred losses in equity F&O between FY22 and FY24,” press release, Mumbai, Sept. 2024.";
const CH_BREAK = process.env.CH_BREAK === "1";
const H1c = (t) => H1(t, { noBreak: !CH_BREAK });
const TITLE = "Quantum Enhanced AI Momentum Trading in Financial Markets and Strategies";
const TEAM = [
  ["B. Rohith", "25WV0105005"],
  ["C. Srinish", "25WU0102056"],
  ["K. Chinmai Datha", "25WU0102126"],
  ["K. Shreenandh", "25WU0102119"],
  ["M. Satvik Kumar", "25WU0102341"],
];
const MENTOR = "Dr. Ram Soorat";
const DEGREE = "Bachelor of Technology in Artificial Intelligence and Machine Learning";

// ---------- title page
const logo = fs.readFileSync(path.join(SCR, "img_p1_13.jpeg"));
const titlePage = [
  C("Woxsen University", { run: { size: 52, bold: true }, para: { spacing: { before: 120, after: 60 } } }),
  C("School of Technology", { run: { size: 32, bold: true }, para: { spacing: { after: 160 } } }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new ImageRun({ type: "jpg", data: logo, transformation: { width: 144, height: 71 }, altText: { title: "Woxsen University logo", description: "Woxsen University logo", name: "logo" } })] }),
  C("A", { run: { size: 24 } }),
  C("PROJECT REPORT", { run: { size: 26, bold: true } }),
  C("on", { run: { size: 24 }, para: { spacing: { after: 200 } } }),
  C("QUANTUM ENHANCED AI MOMENTUM TRADING IN", { run: { size: 32, bold: true } }),
  C("FINANCIAL MARKETS AND STRATEGIES", { run: { size: 32, bold: true }, para: { spacing: { after: 200 } } }),
  C("Submitted in partial fulfillment of the requirements for the degree of", { run: { size: 22 } }),
  C("B. Tech. in Artificial Intelligence and Machine Learning", { run: { size: 24, bold: true }, para: { spacing: { before: 60, after: 200 } } }),
  C("Submitted by:", { run: { size: 24, bold: true } }),
  ...TEAM.map(([n, r]) => C(`${n}  (${r})`, { run: { size: 23 }, para: { spacing: { after: 0, line: 300 } } })),
  C("Under the guidance of:", { run: { size: 24, bold: true }, para: { spacing: { before: 200, after: 60 } } }),
  C(`${MENTOR}`, { run: { size: 24 }, para: { spacing: { after: 240 } } }),
  C("Department of Artificial Intelligence and Machine Learning", { run: { size: 22 }, para: { spacing: { after: 0 } } }),
  C("Woxsen University, Hyderabad · October 2026", { run: { size: 22 }, para: { spacing: { after: 0 } } }),
];

// ---------- certificate
const names = TEAM.map(([n, r]) => `${n} (${r})`);
const nameList = names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
const certificate = [
  FrontTitle("CERTIFICATE"),
  P(`This is to certify that the project report entitled “${TITLE}” submitted by ${nameList} in partial fulfillment of the requirements for the award of the degree of ${DEGREE} from Woxsen University is a bonafide record of work carried out by the students under my supervision and guidance.`),
  P("The work embodied in this project report has been carried out by the candidates and has not been submitted elsewhere for a degree."),
  ...blank(4),
  P("Signature of Mentor", { align: AlignmentType.LEFT, run: { bold: true } }),
  P(`Name: ${MENTOR}`, { align: AlignmentType.LEFT }),
  P("Date:", { align: AlignmentType.LEFT }),
];

// ---------- declaration
const declaration = [
  FrontTitle("DECLARATION OF THE CANDIDATES"),
  P(`We hereby declare that the project work entitled “${TITLE}” submitted to the School of Technology, Woxsen University, in partial fulfillment of the requirements for the award of the degree of ${DEGREE} is our original work and has been carried out under the guidance of ${MENTOR}.`),
  P("We further declare that the work reported in this project has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university."),
];
{
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const nb = { top: none, bottom: none, left: none, right: none };
  const L = (t, bold) => P(t, { align: AlignmentType.LEFT, run: bold ? { bold: true } : {}, para: { spacing: { after: 0, line: 300 } } });
  const block = (m) => new TableCell({ borders: nb, width: { size: 4513, type: WidthType.DXA }, margins: { top: 0, bottom: 360, left: 0, right: 120 },
    children: m ? [new Paragraph({ children: [], spacing: { after: 360 } }), L("Signature of Student", true), L(`Name: ${m[0]}`), L(`Roll Number: ${m[1]}`), L("Date:")] : [new Paragraph({ children: [] })] });
  const rows = [];
  for (let i = 0; i < TEAM.length; i += 2) rows.push(new TableRow({ cantSplit: true, children: [block(TEAM[i]), block(TEAM[i + 1])] }));
  declaration.push(new Paragraph({ children: [], spacing: { after: 120 } }),
    new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [4513, 4513], borders: { top: none, bottom: none, left: none, right: none, insideHorizontal: none, insideVertical: none }, rows }));
}

// ---------- acknowledgment
const acknowledgment = [
  FrontTitle("ACKNOWLEDGMENT"),
  P(`We thank our project guide, ${MENTOR}, for guidance through every review of this project. A question raised at those reviews, how we would know whether a backtest result was real rather than how good it looked, shaped the testing protocol that became the core of this work.`),
  P("We are grateful to the Department of Artificial Intelligence and Machine Learning and the School of Technology, Woxsen University, for the facilities and support provided."),
  P("The strategy is built on open-source TradingView indicators by jdehorty, LazyBear, QuantAlgo and the author of the Weis Wave Volume script. Market data came from Binance, Bitstamp and Yahoo Finance. We used Anthropic’s Claude Code to run the tuning agents; the protocol they worked under and the checks on their output were designed by the team."),
  P("Finally, we thank our families and friends for their patience and support throughout the semester."),
  ...blank(1),
  P(TEAM.map(([n]) => n).join(", "), { align: AlignmentType.RIGHT, run: { italics: true } }),
];

// ---------- abstract
const abstract = [
  FrontTitle("ABSTRACT"),
  P("Most trading strategies that look profitable on historical data stop working on new data. This project builds a rule-based momentum strategy for Bitcoin together with a testing protocol designed to catch that failure."),
  P("The strategy, written in Pine Script v6 for TradingView, gives five open-source indicators one role each. A Lorentzian k-nearest-neighbour classifier proposes entries, Squeeze Momentum gates the volatility regime, a Nadaraya-Watson kernel regression sets the trend, WaveTrend blocks late entries and Weis Wave Volume confirms the move. A trade is taken only when all five agree on a closed candle."),
  P("We rebuilt the strategy and TradingView’s order-fill rules in Python, verified by 88 automated tests, and tuned it on 41,199 hourly BTC/USDT candles with a team of AI agents: a tuner with no access to price data, an executor, an adversarial critic and a tracker, working under a 25-run budget and selection gates fixed in advance."),
  P("Over 19 runs the in-sample Sharpe ratio rose from −1.71 to 0.36 and the profit factor from 0.52 to 1.10. The critic flagged the selected configuration as fragile. On 14 months of locked out-of-sample data, opened once, it lost 3.12% (Sharpe −1.93) while Bitcoin fell 28.0%. Applied unchanged to four daily markets, it was profitable only on Reliance Industries (+6.05%). The in-sample gain did not carry over; the contribution of the project is a testing framework that exposed this before any money was risked."),
  P("**Keywords:** Algorithmic Trading, Momentum, k-Nearest Neighbours, Kernel Regression, Backtest Overfitting, Deflated Sharpe Ratio, Multi-Agent Systems, Pine Script"),
];

// ---------- TOC + combined lists
const tocPages = [
  FrontTitle("TABLE OF CONTENTS"),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }),
  FrontTitle("LIST OF TABLES"),
  new TableOfContents("List of Tables", { hyperlink: true, stylesWithLevels: [new StyleLevel("TableCaption", 1)] }),
  new Paragraph({ style: "FrontTitle", children: [new TextRun({ text: "LIST OF FIGURES", font: FONT })], spacing: { before: 480, after: 240 } }),
  new TableOfContents("List of Figures", { hyperlink: true, stylesWithLevels: [new StyleLevel("FigureCaption", 1)] }),
];

// ================================================================== CHAPTER 1
const ch1 = [
  H1("1. INTRODUCTION", { noBreak: true }),
  P("This project builds a rule-based trading strategy for Bitcoin from five technical indicators, two of them statistical learning models, and then tests it as strictly as we could. “Quantum Enhanced” in the title describes the project’s long-term direction. This phase builds and validates the classical AI layer; no quantum method was used, and quantum-inspired search is planned as the next phase (Section 5.3)."),
  H2("1.1 Background"),
  P("Assets that have risen recently tend to keep rising for a while, an effect documented in stock returns {jt93} and in each asset’s own price history across futures markets {mop12}. Retail traders try to capture it with technical indicators on charting platforms such as TradingView, whose Pine Script language lets users write and backtest strategies {pine}. Each indicator is tuned for one job and fires many false signals when used alone. Bitcoin suits this study because it trades around the clock, giving plenty of hourly data, and because it has had both strong rallies and deep crashes within a few years."),
  H2("1.2 Motivation"),
  P("In September 2024 SEBI reported that 93% of more than one crore individual traders in equity futures and options lost money between FY22 and FY24, with aggregate losses above ₹1.8 lakh crore, while 96–97% of the FY24 trading profits of proprietary traders and foreign portfolio investors came from algorithms {sebi}. Rule-based trading removes emotional decisions, but it brings a different risk. A strategy with many settings can be adjusted until it fits past prices, and the fit usually disappears on new data {bblz14}. AI coding agents make this easier, since they can try hundreds of settings in an afternoon. We wanted to find out whether such agents, given strict rules and an adversarial reviewer, could tune a strategy without fooling us."),
  H2("1.3 Problem Statement"),
  P("The problem is to design an AI-assisted momentum strategy that trades only when several independent indicators agree, tune it without overfitting, and measure honestly how it performs on data it has never seen. Hourly prices are noisy, the market regime can change completely (Bitcoin rose more than sixfold from January 2023 to June 2025, then fell 28%), trading costs are large relative to short-horizon gains, and the strategy has 72 settings, about 2.3 × 10³⁴ combinations even at three values each. TradingView alone also cannot run hundreds of logged, controlled experiments."),
  H2("1.4 Objectives"),
  ...numbered([
    "Build a Pine Script v6 strategy in which each of five open-source indicators has one role, with entries only when all five agree on a closed candle.",
    "Rebuild the strategy and TradingView’s fill rules in Python and verify the engine with automated tests, including tests for look-ahead bias.",
    "Tune it on January 2023 to June 2025 data with a multi-agent loop under a 25-run budget and selection rules fixed in advance.",
    "Test the frozen configuration once on 14 months of unseen data and on four daily markets, and report the results whether favourable or not.",
  ]),
  H2("1.5 Dataset Overview"),
  P("The primary dataset is the hourly BTC/USDT series from the Binance spot API (Table 1.1). The one missing hour is left as a gap, as on TradingView, and the file’s SHA-256 hash is checked before every run. For the transfer test we also used daily data for Bitcoin (Bitstamp), NIFTY 50, HDFC Bank and Reliance Industries (Yahoo Finance)."),
  ...table(["Attribute", "Value"], [
    ["Source, symbol, timeframe", "Binance spot API, BTCUSDT, 1 hour"],
    ["Candles and range", "41,199 candles, 2022-01-01 to 2026-09-13 (UTC), 1 missing hour"],
    ["Warm-up period", "2022 (8,760 candles): indicator warm-up only"],
    ["In-sample period (IS)", "Jan 2023 to Jun 2025 (21,887 candles): the only data used for tuning"],
    ["Out-of-sample period (OOS)", "Jul 2025 to Sep 2026 (10,552 candles): locked, run once"],
  ], [2900, 6126], "Table 1.1: Primary Dataset and Study Periods"),
  H2("1.6 Scope and Limitations"),
  P("The study covers one strategy, tuned on one market at one timeframe. Position size is fixed at 10% of equity, so absolute returns are small and scale-free measures (Sharpe ratio, profit factor) are the main yardsticks. Commission and slippage are modelled, but funding rates and market impact are not, and no live or paper trading was done."),
  H2("1.7 Organization of the Report"),
  P("Chapter 2 reviews the relevant literature, Chapter 3 describes the strategy, the Python engine and the tuning protocol, Chapter 4 presents the results, and Chapter 5 concludes."),
];

// ================================================================== CHAPTER 2
const ch2 = [
  H1c("2. LITERATURE REVIEW / TECHNOLOGY REVIEW"),
  H2("2.1 Indicator Foundations"),
  P("Nadaraya and Watson proposed estimating a regression function as a kernel-weighted average of nearby observations {nadaraya,watson}. Applied to prices, NW(t) = Σ w(i)·price(t−i) / Σ w(i), with a Gaussian weight w(i) = exp(−i²/2h²). Many TradingView versions use a centred window that includes future bars and redraws past values (“repainting”). We use only the causal estimate, which never changes after a bar closes."),
  P("Cover and Hart showed that the nearest-neighbour rule has an error rate at most twice the Bayes rate as data grows {coverhart}. jdehorty’s Lorentzian Classification script applies k-nearest neighbours to price data {jdehorty}: each candle is described by normalised RSI, WaveTrend, CCI and ADX features, and distance is measured as Σ log(1 + |aₖ − bₖ|), which limits the influence of one extreme feature. The other three roles use Carter’s TTM Squeeze, which flags compressed volatility when Bollinger Bands sit inside Keltner Channels {carter,lbsqz}; LazyBear’s WaveTrend oscillator for overbought and oversold levels {lbwt}; and Weis’s wave volume, which sums volume over up-waves and down-waves {weis}."),
  H2("2.2 Backtest Overfitting"),
  P("If many strategy variants are tried and the best is reported, its backtest is biased upwards. Bailey et al. show that a few dozen trials on a few years of data are enough to produce an impressive Sharpe ratio with no out-of-sample value {bblz14}. The Probabilistic Sharpe Ratio (PSR) corrects for track length, skew and fat tails {psr}, and the Deflated Sharpe Ratio (DSR) also raises the bar for every trial run {dsr}. López de Prado recommends logging every trial, fixing selection rules in advance and keeping a hold-out set untouched until the end {lopez18}. Our protocol follows all three."),
  H2("2.3 Multi-Agent AI and Adversarial Review"),
  P("Language model agents tend to accept their own conclusions too readily. Irving et al. proposed debate between AI agents as a way to expose flaws {irving18}, and Du et al. found that agents critiquing each other’s answers improved reasoning {du23}. We apply this to strategy tuning by separating the agent that proposes changes from an agent whose job is to attack them."),
  H2("2.4 Research Gap"),
  P("Community indicator scripts are usually shared with in-app backtests that hide how many settings were tried, use repainting calculations or leave out costs. We found little work that combines such indicators into one strategy and tests it with multiple-testing corrections, a pre-registered hold-out and a fully logged AI tuning loop."),
];

// ================================================================== CHAPTER 3
const ch3 = [
  H1c("3. METHODOLOGY"),
  H2("3.1 System Overview"),
  P("The system has two halves (Figure 3.1). The strategy is written in Pine Script so it runs on TradingView. A Python environment recomputes every indicator as Pine does, simulates TradingView’s broker, computes metrics and logs every experiment. The tuning agents work only through this environment, and the chosen parameters were copied back into the Pine script at the end."),
  ...figure(path.join(FIG, "fig_3_1_architecture.png"), "Figure 3.1: System Architecture", 5.6),
  H2("3.2 Data Preparation and Isolation"),
  P("Hourly candles are downloaded from Binance with bar open times in UTC; only closed candles are kept and gaps are not filled. Three rules are enforced in code. Every in-sample run cuts the data at 30 June 2025 before any indicator is computed. Every run goes through one logged command that refuses out-of-sequence runs, repeated configurations, a changed data hash or a 26th run. The out-of-sample command writes a LOCK file before computing anything and refuses to run again."),
  H2("3.3 Strategy Design"),
  P("In the Combined Role-Based (CRB) strategy each indicator does one job (Table 3.1). A long or short order is placed only when all five conditions hold on a closed candle (Figure 3.2)."),
  ...table(["Role", "Indicator (author)", "Condition for a long entry (short is mirrored)"], [
    ["Entry", "Lorentzian Classification (jdehorty)", "KNN signal flipped to long within the last 2 bars and that flip has not yet been traded"],
    ["Regime", "Squeeze Momentum (LazyBear)", "Squeeze off: Bollinger Bands outside the Keltner Channels"],
    ["Trend", "Nadaraya-Watson Trend (QuantAlgo)", "NW line higher than 3 bars ago, close above the line"],
    ["Timing", "WaveTrend (LazyBear)", "WT1 below the overbought cap (40 after tuning)"],
    ["Confirmation", "Weis Wave Volume", "Current Weis wave direction is up"],
  ], [1400, 3000, 4626], "Table 3.1: Indicator Roles in the CRB Strategy", { size: 21 }),
  ...figure(path.join(FIG, "fig_3_2_pipeline.png"), "Figure 3.2: The Five-Role Entry Decision", 6.0),
  P("Each trade carries a stop-loss at 2 × ATR(14) and a take-profit at 3 × ATR(14), so both adapt to volatility, and is closed after 12 candles or if the KNN signal flips. Each position uses 10% of equity on a $10,000 account. Base costs are 0.075% commission per side plus 2 ticks of slippage; a stress case uses 0.10% plus 5 basis points."),
  H2("3.4 Python Engine and Verification"),
  P("The engine re-implements every Pine built-in the strategy uses, with Pine’s rules for missing values and moving-average seeding, and compiles the nearest-neighbour search with Numba; a 2.5-year hourly backtest takes about 2.4 seconds. The broker fills orders at the next candle’s open, checks stops and targets along TradingView’s assumed intrabar price path, fills gaps at the open and charges costs on every fill. One deviation is documented: the original Lorentzian script anchors its search to the last bar of the chart, so on TradingView it predicts only over the most recent 2,000 candles. The engine applies the same 2,000-candle search causally at every bar."),
  P("The engine is covered by 88 automated tests, all passing. The most important prove causality: signals computed on part of a series must equal those computed on the full series, and changing a future candle must never change a past signal. Hand-computed broker cases and a cross-check against the independent backtesting.py library {btpy} confirm the fills and costs."),
  H2("3.5 Multi-Agent Tuning Protocol"),
  P("Before tuning, a builder agent wrote the Pine script under the role rules and a read-only adversary agent reviewed it for repainting, look-ahead, unrealistic fills and overfitting. Tuning then ran in a loop of four Claude Code agents {claudecode}. The **tuner** read the log and every critic verdict and proposed one new parameter set, but could not run backtests or see price data. The **executor** ran the logged backtest. The **adversarial critic**, briefed to act as a hostile risk committee that assumes every result is overfitted, scored each run, demanded the next experiment and returned CONTINUE or PLATEAU. The **tracker** saved the verdict verbatim and verified the log."),
  P("The rules in Table 3.2 were fixed before run 1. The best run would be the eligible run with the highest in-sample Sharpe ratio; if none passed all four gates, the fallback was the highest Sharpe among runs with at least 30 trades, flagged as failing the gates. The critic could declare a plateau only after five runs without a 0.05 Sharpe gain and once every role had been probed. The chosen parameters were then frozen and run once on the out-of-sample period, and afterwards applied unchanged to the four daily markets."),
  ...table(["Gate", "Rule", "Purpose"], [
    ["G1", "At least 100 trades", "Enough trades for meaningful statistics"],
    ["G2", "Profit factor above 1.0", "Profitable after base costs"],
    ["G3", "Net return above zero under stress costs", "Margin to survive higher costs"],
    ["G4", "Profit in at least 2 of 3 sub-periods (2023, 2024, 2025 H1)", "Not reliant on one lucky period"],
    ["Budget", "At most 25 parameter sets, all logged", "Limits the multiple-testing penalty"],
  ], [1100, 4500, 3426], "Table 3.2: Pre-registered Selection Rules", { size: 21 }),
];

// ================================================================== CHAPTER 4
const ch4 = [
  H1c("4. RESULTS AND DISCUSSION"),
  H2("4.1 Tuning Trajectory"),
  P("With default settings (run 1) the strategy lost 3.51% in-sample with a Sharpe ratio of −1.71, mostly on short trades, which were closed by a 4-candle timer before any target could be reached. Figure 4.1 shows all 19 runs. Holding trades for 12 candles with a take-profit (run 2) gave the largest single gain. Trend and timing changes (runs 4–5) and 12 KNN neighbours (run 6) produced the first positive Sharpe ratio. Nine structural probes (runs 7–16) failed to beat run 6, and lowering the WaveTrend cap to ±40 (run 17) gave the best result, 0.355. Only 5 of the 18 changes improved on the best run so far. After a neighbourhood check (run 18) and a final probe (run 19), the critic declared a plateau with 6 of 25 slots unused."),
  ...figure(path.join(FIG, "fig_4_1_sharpe_runs.png"), "Figure 4.1: In-sample Sharpe Ratio of Each Tuning Run", 5.8),
  P("Nine inputs ended up changed from their defaults: holding period 4 → 12 candles, take-profit enabled, trend slope 1 → 3 bars with price on the trend side, NW bandwidth 8 → 5, KNN neighbours 8 → 12, WaveTrend timing set to the overextension cap only, and the cap lowered from ±53 to ±40."),
  H2("4.2 The Selected Configuration and the Critic’s Objections"),
  P("No run passed all four gates: every run with a positive Sharpe ratio lost money under stress costs (G3). The fallback rule therefore selected run 17, flagged as failing the gates. Before the out-of-sample test, the critic recorded these objections:"),
  ...bullets([
    "The two largest winners made up 80% of the $112.32 net profit; without the top three trades the result was negative.",
    "2023 was essentially break-even (+0.04%) and 2025 H1 was negative, so the G4 pass rested on 2024 alone.",
    "The average net trade (+0.06%) was smaller than the extra cost of the stress scenario, which turned +1.12% into −1.42%.",
    "The WaveTrend cap at ±45 scored lower than both ±53 and ±40, a sign of a narrow, fragile peak.",
    "The Deflated Sharpe Ratio over 19 trials was only 0.187.",
  ]),
  H2("4.3 Out-of-Sample Test"),
  P("Table 4.1 compares the baseline and run 17 in-sample with run 17 on the locked period (July 2025 to September 2026), when Bitcoin fell 28.0% and was at one point 53.7% below its peak. Figure 4.2 shows the out-of-sample equity."),
  ...table(["Metric", "Run 1, IS", "Run 17, IS", "Run 17, OOS", "BTC buy-and-hold, OOS"], [
    ["Net return", "−3.51%", "+1.12%", "−3.12%", "−28.0%"],
    ["Sharpe ratio", "−1.71", "0.36", "−1.93", "−0.44"],
    ["Profit factor", "0.52", "1.10", "0.60", "–"],
    ["Win rate", "36.8%", "47.9%", "35.2%", "–"],
    ["Trades", "117", "188", "125", "–"],
    ["Maximum drawdown", "4.20%", "1.49%", "3.72%", "53.7%"],
    ["Trade t-statistic", "−2.69", "0.54", "−2.43", "–"],
    ["Net return, stress costs", "−5.19%", "−1.42%", "−4.81%", "–"],
  ], [2526, 1500, 1500, 1600, 1900], "Table 4.1: Baseline, Selected Configuration and Out-of-Sample Results", { size: 21, align: [null, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT] }),
  ...figure(path.join(FIG, "fig_4_3_oos_equity.png"), "Figure 4.2: Out-of-sample Value of $10,000, Strategy versus Bitcoin", 5.8),
  P("The in-sample edge did not survive. The strategy lost money in both halves of the period and on both long and short trades, and a t-statistic of −2.43 makes chance an unlikely explanation. It kept 96.9% of its capital against 72.0% for buy-and-hold, but that gap comes mostly from position sizing: it held a position only 9.7% of the time at 10% of equity, so under 1% of the account was exposed on average. A passive position of that size would have lost only about 0.3%."),
  H2("4.4 Transfer to Daily Markets"),
  ...table(["Market (daily)", "Trades", "Net %, defaults", "Net %, run 17", "Profit factor", "Stress net %"], [
    ["Bitcoin (2017–2026)", "39", "+3.67", "−0.43", "0.97", "−0.83"],
    ["NIFTY 50 (2015–2026)", "52", "−1.32", "−1.19", "0.81", "−1.91"],
    ["HDFC Bank (2004–2026)", "58", "−0.83", "−5.60", "0.61", "−5.83"],
    ["Reliance (2004–2026)", "75", "+0.63", "+6.05", "1.47", "+5.49"],
  ], [2826, 1000, 1350, 1350, 1250, 1250], "Table 4.2: Frozen Parameters Applied to Four Daily Markets", { size: 21, align: [null, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT] }),
  P("Reliance was the one clear success: the tuned settings lifted its 22-year result from +0.63% to +6.05% with a 58.7% win rate, and it stayed profitable under stress costs. On Reliance, 502 candidate KNN signals were cut to 75 trades by the other four roles, so 85% of the model’s signals were filtered out. On the other three markets the tuned settings were flat or worse than the defaults. One success in four, with a t-statistic of 1.28, is consistent with chance."),
  H2("4.5 The Strategy on TradingView"),
  P("With the frozen parameters as its defaults, the script runs on TradingView (Appendix I). On the BTCUSD daily chart, TradingView’s Strategy Tester reported a profit factor of 1.298, 13 of 23 trades profitable, +2.12% and a 3.60% maximum drawdown on 6 October 2026. Because the Lorentzian search covers only the latest 2,000 candles on TradingView, this window is shorter than the Python study, and 23 trades are too few to draw conclusions. It does show that every entry can be audited, as the data window displays all five role conditions."),
  H2("4.6 Discussion"),
  P("The process worked even though the strategy did not. Every trial was logged, the selection rule was fixed in advance, and the critic identified the weaknesses of run 17 before the hold-out was opened; the out-of-sample loss is what those warnings predicted. Without the locked period we would have reported a profitable strategy with a 1.5% drawdown, and it would have been wrong. The biggest improvement came from the exits, not from the machine learning model, and trading costs were the binding constraint: a round trip cost about 0.15% in commission against an average net gain of 0.06% per trade. The team’s role was to design the rules, verify the engine and check the agents’ claims against the result files."),
];

// ================================================================== CHAPTER 5
const ch5 = [
  H1c("5. CONCLUSION AND FUTURE WORK"),
  H2("5.1 Summary of Contributions"),
  ...numbered([
    "A role-based Pine Script v6 strategy combining five open-source indicators, including a Lorentzian KNN classifier and a causal kernel regression, with every condition visible on the chart.",
    "A Python twin of the strategy and TradingView’s broker, verified by 88 tests including causality proofs and an independent cross-check.",
    "A multi-agent tuning protocol with a data-blind tuner, an adversarial critic, a 25-run budget, pre-registered gates and a one-shot hold-out.",
    "An honest record: in-sample Sharpe rose from −1.71 to 0.36, the critic flagged the result as fragile, and the strategy lost 3.12% on unseen data.",
  ]),
  H2("5.2 Limitations"),
  P("The study used one market, one timeframe and one out-of-sample period, which was mostly a falling market. Only 9 of 72 inputs were changed in 19 runs. Fixed 10% sizing makes drawdown comparisons with buy-and-hold misleading unless exposure is taken into account, and TradingView’s results cover a different window from the Python study."),
  H2("5.3 Future Work"),
  P("The next phase is the quantum part of the title: treating the discrete parameter choice as a combinatorial optimisation problem and testing quantum-inspired solvers such as classical simulations of the Quantum Approximate Optimization Algorithm {farhi14}. A stronger optimiser overfits faster, so every evaluated configuration must count towards the Deflated Sharpe Ratio and a fresh hold-out period will be needed. Other steps are walk-forward testing {lopez18}, fewer and longer trades to reduce cost drag, a causal Lorentzian search inside the Pine script so that TradingView and Python agree trade for trade, and a period of paper trading on live data."),
  H2("5.4 Concluding Remarks"),
  P("We set out to build a strategy that trades only when five indicators agree and to tune it with AI agents without fooling ourselves. The strategy works as designed but has no reliable edge, and the protocol caught this before any money was risked. The fully logged record also supports SDG 4, 8 and 9 as a teaching resource on disciplined, capped-risk investing and a practical use of AI agents in financial research."),
];

// ================================================================== REFERENCES
function referencesSection() {
  return [
    H1("REFERENCES"),
    ...citeOrder.map((k, i) => new Paragraph({
      children: [new TextRun({ text: `[${i + 1}]`, font: FONT }), new TextRun({ text: "\t", font: FONT }), ...runs(REFS[k])],
      alignment: AlignmentType.JUSTIFIED,
      tabStops: [{ type: TabStopType.LEFT, position: 600 }],
      indent: { left: 600, hanging: 600 },
      spacing: { after: 20, line: 240 },
    })),
  ];
}

// ================================================================== APPENDIX
const appendices = [
  H1("APPENDIX I: SCREENSHOTS OF WORK DONE"),
  ...figure(path.join(PROJ, "Final_Review_PPT/screenshots/tv_chart_main.png"), "Figure A.1: CRB Strategy on TradingView (BTCUSD Daily) with Key Stats", 5.3),
  ...figure(path.join(PROJ, "Final_Review_PPT/tv_data_window.png"), "Figure A.2: TradingView Data Window Showing the Five Role Conditions (C1–C5)", 5.3),
];

// ================================================================== DOCUMENT
const pageBorder = { style: BorderStyle.SINGLE, size: 6, color: "7F7F7F", space: 24 };
const pageProps = (pn) => ({
  page: {
    size: { width: 11906, height: 16838 },
    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440, footer: 600 },
    pageNumbers: pn,
    borders: {
      pageBorderTop: pageBorder, pageBorderBottom: pageBorder, pageBorderLeft: pageBorder, pageBorderRight: pageBorder,
      pageBorders: { display: PageBorderDisplay.ALL_PAGES, offsetFrom: PageBorderOffsetFrom.PAGE, zOrder: "front" },
    },
  },
});
const footer = () => ({ default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 22 })] })] }) });

const bodyChildren = [...ch1, ...ch2, ...ch3, ...ch4, ...ch5];
const refs = referencesSection();

const doc = new Document({
  creator: "B. Rohith, C. Srinish, K. Chinmai Datha, K. Shreenandh, M. Satvik Kumar",
  title: TITLE,
  description: "CIP project report, Woxsen University",
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 360, after: 120 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 32, bold: true, color: "000000" }, paragraph: { spacing: { before: 360, after: 240, line: 276 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 28, bold: true, color: "000000" }, paragraph: { spacing: { before: 240, after: 120, line: 276 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 200, after: 120, line: 276 }, outlineLevel: 2 } },
      { id: "TOC1", name: "toc 1", basedOn: "Normal", next: "Normal", paragraph: { spacing: { line: 276, before: 60, after: 20 } } },
      { id: "TOC2", name: "toc 2", basedOn: "Normal", next: "Normal", paragraph: { spacing: { line: 276, before: 0, after: 20 }, indent: { left: 240 } } },
      { id: "FrontTitle", name: "FrontTitle", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 32, bold: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 240, after: 360 } } },
      { id: "TableCaption", name: "TableCaption", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 22, italics: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 100, after: 200, line: 240 } } },
      { id: "FigureCaption", name: "FigureCaption", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 22, italics: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 60, after: 200, line: 240 } } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [
    { properties: pageProps({ start: 1, formatType: NumberFormat.LOWER_ROMAN }), children: titlePage },
    { properties: pageProps({ start: 2, formatType: NumberFormat.LOWER_ROMAN }), footers: footer(),
      children: [...certificate, ...declaration, ...acknowledgment, ...abstract, ...tocPages] },
    { properties: pageProps({ start: 1, formatType: NumberFormat.DECIMAL }), footers: footer(),
      children: [...bodyChildren, ...refs, ...appendices] },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT, buf.length, "bytes;", citeOrder.length, "references");
});
