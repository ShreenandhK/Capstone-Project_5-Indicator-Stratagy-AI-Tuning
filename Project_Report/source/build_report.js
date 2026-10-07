// Builds the CIP project report (.docx) following the Woxsen sample report structure and formatting guidelines.
const fs = require("fs");
const path = require("path");
const d = require("docx");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, HeadingLevel, BorderStyle, PageBreak, Footer, PageNumber, NumberFormat, LevelFormat,
  TableOfContents, StyleLevel, PageBorderDisplay, PageBorderOffsetFrom, VerticalAlign, HighlightColor,
  TabStopType,
} = d;

const SCR = __dirname;
const FIG = path.join(SCR, "figs");
const PROJ = "C:/Course-Work/CIP-Project";
const OUT = process.argv[2] || path.join(PROJ, "CIP_Project_Report.docx");
const DATA = JSON.parse(fs.readFileSync(path.join(SCR, "data.json"), "utf8"));

const FONT = "Times New Roman";
const MONO = "Consolas";
const TEXT_W = 9026; // A4 width 11906 - 2 x 1440 margins

// ------------------------------------------------------------------ citations
const REFS = {
  sebi: "Securities and Exchange Board of India (SEBI), \u201cUpdated SEBI study reveals 93% of individual traders incurred losses in equity F&O between FY22 and FY24,\u201d press release and accompanying study, Mumbai, 23 Sept. 2024.",
  jt93: "N. Jegadeesh and S. Titman, \u201cReturns to buying winners and selling losers: Implications for stock market efficiency,\u201d The Journal of Finance, vol. 48, no. 1, pp. 65\u201391, 1993.",
  mop12: "T. J. Moskowitz, Y. H. Ooi, and L. H. Pedersen, \u201cTime series momentum,\u201d Journal of Financial Economics, vol. 104, no. 2, pp. 228\u2013250, 2012.",
  bblz14: "D. H. Bailey, J. M. Borwein, M. L\u00f3pez de Prado, and Q. J. Zhu, \u201cPseudo-mathematics and financial charlatanism: The effects of backtest overfitting on out-of-sample performance,\u201d Notices of the American Mathematical Society, vol. 61, no. 5, pp. 458\u2013471, 2014.",
  pine: "TradingView, \u201cPine Script\u00ae v6 User Manual,\u201d 2025. [Online]. Available: https://www.tradingview.com/pine-script-docs/",
  hop17: "B. Hurst, Y. H. Ooi, and L. H. Pedersen, \u201cA century of evidence on trend-following investing,\u201d The Journal of Portfolio Management, vol. 44, no. 1, pp. 15\u201329, 2017.",
  nadaraya: "E. A. Nadaraya, \u201cOn estimating regression,\u201d Theory of Probability and Its Applications, vol. 9, no. 1, pp. 141\u2013142, 1964.",
  watson: "G. S. Watson, \u201cSmooth regression analysis,\u201d Sankhy\u0101: The Indian Journal of Statistics, Series A, vol. 26, no. 4, pp. 359\u2013372, 1964.",
  quantalgo: "QuantAlgo, \u201cNadaraya-Watson Trend,\u201d open-source indicator script, TradingView. [Online]. Available: https://www.tradingview.com/scripts/",
  coverhart: "T. Cover and P. Hart, \u201cNearest neighbor pattern classification,\u201d IEEE Transactions on Information Theory, vol. 13, no. 1, pp. 21\u201327, 1967.",
  jdehorty: "jdehorty, \u201cMachine Learning: Lorentzian Classification,\u201d open-source indicator script, TradingView, 2022. [Online]. Available: https://www.tradingview.com/scripts/",
  wilder: "J. W. Wilder, New Concepts in Technical Trading Systems. Greensboro, NC, USA: Trend Research, 1978.",
  lambert: "D. R. Lambert, \u201cCommodity channel index: Tools for trading cyclic trends,\u201d Commodities, vol. 9, no. 10, pp. 40\u201341, 1980.",
  carter: "J. F. Carter, Mastering the Trade: Proven Techniques for Profiting from Intraday and Swing Trading Setups. New York, NY, USA: McGraw-Hill, 2005.",
  bollinger: "J. Bollinger, Bollinger on Bollinger Bands. New York, NY, USA: McGraw-Hill, 2001.",
  lbsqz: "LazyBear, \u201cSqueeze Momentum Indicator [LazyBear],\u201d open-source indicator script, TradingView, 2014. [Online]. Available: https://www.tradingview.com/scripts/",
  lbwt: "LazyBear, \u201cWaveTrend Oscillator [WT],\u201d open-source indicator script, TradingView, 2014. [Online]. Available: https://www.tradingview.com/scripts/",
  weis: "D. H. Weis, Trades About to Happen: A Modern Adaptation of the Wyckoff Method. Hoboken, NJ, USA: Wiley, 2013.",
  psr: "D. H. Bailey and M. L\u00f3pez de Prado, \u201cThe Sharpe ratio efficient frontier,\u201d Journal of Risk, vol. 15, no. 2, pp. 3\u201344, 2012.",
  dsr: "D. H. Bailey and M. L\u00f3pez de Prado, \u201cThe deflated Sharpe ratio: Correcting for selection bias, backtest overfitting, and non-normality,\u201d The Journal of Portfolio Management, vol. 40, no. 5, pp. 94\u2013107, 2014.",
  hlz16: "C. R. Harvey, Y. Liu, and H. Zhu, \u201c\u2026and the cross-section of expected returns,\u201d The Review of Financial Studies, vol. 29, no. 1, pp. 5\u201368, 2016.",
  lopez18: "M. L\u00f3pez de Prado, Advances in Financial Machine Learning. Hoboken, NJ, USA: Wiley, 2018.",
  irving18: "G. Irving, P. Christiano, and D. Amodei, \u201cAI safety via debate,\u201d arXiv preprint arXiv:1805.00899, 2018.",
  du23: "Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch, \u201cImproving factuality and reasoning in language models through multiagent debate,\u201d arXiv preprint arXiv:2305.14325, 2023.",
  madaan23: "A. Madaan et al., \u201cSelf-Refine: Iterative refinement with self-feedback,\u201d in Advances in Neural Information Processing Systems, vol. 36, 2023.",
  sharpe94: "W. F. Sharpe, \u201cThe Sharpe ratio,\u201d The Journal of Portfolio Management, vol. 21, no. 1, pp. 49\u201358, 1994.",
  sortino94: "F. A. Sortino and L. N. Price, \u201cPerformance measurement in a downside risk framework,\u201d The Journal of Investing, vol. 3, no. 3, pp. 59\u201364, 1994.",
  binance: "Binance, \u201cSpot API documentation: Kline/candlestick data (GET /api/v3/klines),\u201d 2025. [Online]. Available: https://developers.binance.com/docs/binance-spot-api-docs",
  numba: "S. K. Lam, A. Pitrou, and S. Seibert, \u201cNumba: A LLVM-based Python JIT compiler,\u201d in Proc. 2nd Workshop on the LLVM Compiler Infrastructure in HPC, 2015, pp. 1\u20136.",
  btpy: "K. Kernc, \u201cBacktesting.py: Backtest trading strategies in Python,\u201d version 0.6.6, open-source software. [Online]. Available: https://github.com/kernc/backtesting.py",
  claudecode: "Anthropic, \u201cClaude Code documentation: Subagents,\u201d 2025. [Online]. Available: https://docs.anthropic.com/en/docs/claude-code",
  farhi14: "E. Farhi, J. Goldstone, and S. Gutmann, \u201cA quantum approximate optimization algorithm,\u201d arXiv preprint arXiv:1411.4028, 2014.",
  goto19: "H. Goto, K. Tatsumura, and A. R. Dixon, \u201cCombinatorial optimization by simulating adiabatic bifurcations in nonlinear Hamiltonian systems,\u201d Science Advances, vol. 5, no. 4, eaav2372, 2019.",
};
const citeOrder = [];
function citeNum(key) {
  if (!REFS[key]) throw new Error("unknown ref " + key);
  let i = citeOrder.indexOf(key);
  if (i < 0) { citeOrder.push(key); i = citeOrder.length - 1; }
  return i + 1;
}

// ------------------------------------------------------------------ inline markup
// **bold**, *italic*, `mono`, [[placeholder]] (yellow highlight), {key} or {key,key2} citations
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[\[[^\]]+\]\]|\{[a-z0-9_,]+\})/g;
  let last = 0, m;
  const push = (t, o = {}) => { if (t) out.push(new TextRun({ text: t, font: FONT, ...base, ...o })); };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith("**")) push(tok.slice(2, -2), { bold: true });
    else if (tok.startsWith("`")) push(tok.slice(1, -1), { font: MONO, size: (base.size || 24) - 3 });
    else if (tok.startsWith("[[")) push(tok.slice(2, -2), { highlight: HighlightColor.YELLOW });
    else if (tok.startsWith("{")) {
      const nums = tok.slice(1, -1).split(",").map(citeNum);
      push(nums.map((n) => `[${n}]`).join(", "));
    } else push(tok.slice(1, -1), { italics: true });
    last = m.index + tok.length;
  }
  push(text.slice(last));
  return out;
}

const P = (text, opts = {}) => new Paragraph({ children: runs(text, opts.run || {}), alignment: opts.align || AlignmentType.JUSTIFIED, ...(opts.para || {}) });
const C = (text, opts = {}) => P(text, { ...opts, align: AlignmentType.CENTER });
const H1 = (t, opts = {}) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: FONT })], pageBreakBefore: opts.noBreak ? false : true });
const H2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, font: FONT })], keepNext: true });
const H3 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: t, font: FONT })], keepNext: true });
const FrontTitle = (t) => new Paragraph({ style: "FrontTitle", pageBreakBefore: true, children: [new TextRun({ text: t, font: FONT })] });
const blank = (n = 1) => Array.from({ length: n }, () => new Paragraph({ children: [] }));
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

let listInstance = 0;
const bullets = (items) => items.map((t) => new Paragraph({ children: runs(t), numbering: { reference: "bullets", level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 60 } }));
const numbered = (items) => {
  listInstance += 1;
  return items.map((t) => new Paragraph({ children: runs(t), numbering: { reference: "numbers", level: 0, instance: listInstance }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 60 } }));
};

function code(lines) {
  const border = { style: BorderStyle.SINGLE, size: 8, color: "808080", space: 4 };
  return lines.map((l, i) => new Paragraph({
    children: [new TextRun({ text: l.length ? l : " ", font: MONO, size: 20 })],
    shading: { type: ShadingType.CLEAR, fill: "F2F2F2", color: "auto" },
    border: { left: border, right: border, top: i === 0 ? border : undefined, bottom: i === lines.length - 1 ? border : undefined },
    spacing: { line: 240, before: 0, after: i === lines.length - 1 ? 200 : 0 },
    alignment: AlignmentType.LEFT,
    indent: { left: 120, right: 120 },
  }));
}

// ------------------------------------------------------------------ tables and figures
const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: "8C8C8C" };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
function table(header, rows, widths, caption, opts = {}) {
  const size = opts.size || 22;
  const sum = widths.reduce((a, b) => a + b, 0);
  if (sum !== TEXT_W && !opts.allowNarrow) throw new Error(`table widths ${sum} != ${TEXT_W} for ${caption}`);
  const mk = (t, w, head, ci) => new TableCell({
    borders, width: { size: w, type: WidthType.DXA },
    shading: head ? { fill: "D5E8F0", type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 110, right: 110 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      children: runs(String(t), { size, bold: head || undefined }),
      alignment: (opts.align && opts.align[ci]) || AlignmentType.LEFT,
      spacing: { line: 240, before: 0, after: 0 },
      keepNext: opts.keep !== false,
    })],
  });
  const t = new Table({
    width: { size: sum, type: WidthType.DXA },
    columnWidths: widths,
    alignment: AlignmentType.CENTER,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: header.map((h, i) => mk(h, widths[i], true, i)) }),
      ...rows.map((r) => new TableRow({ cantSplit: true, children: r.map((c, i) => mk(c, widths[i], false, i)) })),
    ],
  });
  return [t, new Paragraph({ style: "TableCaption", children: [new TextRun({ text: caption, font: FONT })] })];
}

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20), data: b };
}
function figure(file, caption, widthIn = 6.2) {
  const { w, h, data } = pngSize(file);
  const W = Math.round(widthIn * 96);
  const H = Math.round((W * h) / w);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60, line: 240 },
      children: [new ImageRun({ type: "png", data, transformation: { width: W, height: H }, altText: { title: caption, description: caption, name: path.basename(file) } })] }),
    new Paragraph({ style: "FigureCaption", children: [new TextRun({ text: caption, font: FONT })] }),
  ];
}

// ------------------------------------------------------------------ number helpers
const f = (x, nd = 2) => {
  const s = Math.abs(x).toFixed(nd);
  return (x < 0 && Number(s) !== 0 ? "\u2212" : "") + s;
};
const fs_ = (x, nd = 2) => (x > 0 ? "+" : "") + f(x, nd);

// ================================================================== CONTENT
const TITLE = "Quantum Enhanced AI Momentum Trading in Financial Markets and Strategies";
const TEAM = [
  ["B. Rohith", "[[Roll Number]]"],
  ["C. Srinish", "[[Roll Number]]"],
  ["K. Chinmai Datha", "[[Roll Number]]"],
  ["K. Shreenandh", "[[Roll Number]]"],
  ["M. Satvik Kumar", "[[Roll Number]]"],
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
  C(`${MENTOR}`, { run: { size: 24 }, para: { spacing: { after: 0 } } }),
  C("[[Designation]], School of Technology", { run: { size: 22 }, para: { spacing: { after: 200 } } }),
  C("Department of Artificial Intelligence and Machine Learning", { run: { size: 22 }, para: { spacing: { after: 0 } } }),
  C("Woxsen University, Hyderabad \u00b7 October 2026", { run: { size: 22 }, para: { spacing: { after: 0 } } }),
];

// ---------- certificate
const names = TEAM.map(([n, r]) => `${n} (${r})`);
const nameList = names.slice(0, -1).join(", ") + " and " + names[names.length - 1];
const certificate = [
  FrontTitle("CERTIFICATE"),
  P(`This is to certify that the project report entitled \u201c${TITLE}\u201d submitted by ${nameList} in partial fulfillment of the requirements for the award of the degree of ${DEGREE} from Woxsen University is a bonafide record of work carried out by the students under my supervision and guidance.`),
  P("The work embodied in this project report has been carried out by the candidates and has not been submitted elsewhere for a degree."),
  ...blank(4),
  P("Signature of Mentor", { align: AlignmentType.LEFT, run: { bold: true } }),
  P(`Name: ${MENTOR}`, { align: AlignmentType.LEFT }),
  P("Designation: [[Designation]]", { align: AlignmentType.LEFT }),
  P("Date:", { align: AlignmentType.LEFT }),
  ...blank(3),
  P("Signature of the Head of the Department", { align: AlignmentType.LEFT, run: { bold: true } }),
  P("Name: [[Head of Department Name]]", { align: AlignmentType.LEFT }),
  P("Department of Artificial Intelligence and Machine Learning", { align: AlignmentType.LEFT }),
  P("Date:", { align: AlignmentType.LEFT }),
];

// ---------- declaration
const declaration = [
  FrontTitle("DECLARATION OF THE CANDIDATES"),
  P(`We hereby declare that the project work entitled \u201c${TITLE}\u201d submitted to the School of Technology, Woxsen University, in partial fulfillment of the requirements for the award of the degree of ${DEGREE} is our original work and has been carried out under the guidance of ${MENTOR}.`),
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
  P(`We thank our project guide, ${MENTOR}, [[Designation]], for guidance through every review of this project. A question raised at those reviews, how we would know whether a backtest result was real rather than how good it looked, shaped the testing protocol that became the core of this work.`),
  P("We are grateful to [[Head of Department Name]], Head of the Department of Artificial Intelligence and Machine Learning, and to the School of Technology, Woxsen University, for the facilities and support provided during the project."),
  P("This project builds on open-source work. We thank the TradingView community authors whose indicator scripts we ported and combined: jdehorty (Machine Learning: Lorentzian Classification), LazyBear (WaveTrend Oscillator and Squeeze Momentum), QuantAlgo (Nadaraya-Watson Trend), and the author of the Weis Wave Volume script. We also thank Binance, Bitstamp and Yahoo Finance for the public market data used in the study, and the maintainers of NumPy, pandas, Numba, SciPy, pytest and backtesting.py."),
  P("We used Anthropic\u2019s Claude Code to run the tuning agents described in Chapter 3. The protocol, the rules the agents worked under and the checks on their output were designed by the team."),
  P("Finally, we thank our families and friends for their patience and support throughout the semester."),
  ...blank(1),
  P(TEAM.map(([n]) => n).join(", "), { align: AlignmentType.RIGHT, run: { italics: true } }),
];

// ---------- abstract
const abstract = [
  FrontTitle("ABSTRACT"),
  P("Most individual traders lose money, and most trading strategies that look profitable on historical data stop working on new data. This project tackles both problems with a rule-based momentum strategy for Bitcoin and a testing protocol designed to prevent overfitting."),
  P("The strategy, written in Pine Script v6 for TradingView, assigns five open-source indicators one role each. A Lorentzian-distance k-nearest-neighbour classifier proposes entries, Squeeze Momentum acts as a volatility regime gate, a Nadaraya-Watson kernel regression sets the trend direction, the WaveTrend oscillator blocks late entries and Weis Wave Volume confirms that volume supports the move. A trade is taken only when all five agree on a closed candle, with ATR-based stop-loss and take-profit orders."),
  P("To run controlled experiments we rebuilt the strategy and TradingView\u2019s order-fill rules in Python, checked by 88 automated tests that include causality proofs and a cross-check against an independent library. Using 41,199 hourly BTC/USDT candles, a team of AI agents tuned the strategy: a tuner that proposed one change per run without access to price data, an executor, an adversarial critic instructed to assume every result was overfitted, and a tracker that kept a hash-verified log. The budget was capped at 25 parameter sets, and the selection gates were fixed before the first run."),
  P("Over 19 runs, in-sample performance (January 2023 to June 2025) improved from a Sharpe ratio of \u22121.71 and profit factor 0.52 to a Sharpe ratio of 0.36 and profit factor 1.10, with maximum drawdown falling from 4.20% to 1.49%. The selected configuration failed one of the four pre-registered gates (profitability under stress costs), and its Deflated Sharpe Ratio was only 0.19. On 14 months of locked out-of-sample data, opened once, the strategy lost 3.12% (Sharpe \u22121.93, 125 trades) while Bitcoin fell 28.0%. Applied without re-tuning to four daily markets, it was profitable on Reliance Industries (+6.05%, profit factor 1.47) but not on Bitcoin, NIFTY 50 or HDFC Bank."),
  P("The in-sample improvement did not carry over to unseen data. The main contribution is the testing framework, which recorded this honestly, and the evidence that the adversarial critic flagged the selected configuration as fragile before the out-of-sample test."),
  P("**Keywords:** Algorithmic Trading, Momentum, k-Nearest Neighbours, Kernel Regression, Backtesting, Overfitting, Deflated Sharpe Ratio, Multi-Agent Systems, Large Language Model Agents, Pine Script"),
];

// ---------- TOC, LoT, LoF
const tocPages = [
  FrontTitle("TABLE OF CONTENTS"),
  new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),
  FrontTitle("LIST OF TABLES"),
  new TableOfContents("List of Tables", { hyperlink: true, stylesWithLevels: [new StyleLevel("TableCaption", 1)] }),
  FrontTitle("LIST OF FIGURES"),
  new TableOfContents("List of Figures", { hyperlink: true, stylesWithLevels: [new StyleLevel("FigureCaption", 1)] }),
];

// ================================================================== CHAPTER 1
const R = DATA.runs;
const r1 = R[0], r17 = R[16];
const ch1 = [
  H1("1. INTRODUCTION"),
  P("This project builds a rule-based trading strategy for Bitcoin that combines five technical indicators, two of which are statistical learning models, and then tests it as strictly as we could. Most of the effort went into the testing: a Python copy of TradingView\u2019s backtest engine, a tuning loop run by AI agents that includes an adversarial critic, and a block of recent data that was locked away during tuning and opened exactly once at the end."),
  P("A note on the title. \u201cQuantum Enhanced\u201d describes the long-term direction of the project. The phase reported here builds and validates the classical AI layer. No quantum hardware or quantum algorithm was used, and quantum-inspired optimisation of the parameter search is listed as future work in Section 5.3."),
  H2("1.1 Background"),
  P("Momentum is one of the most studied effects in finance: assets that have risen recently tend to keep rising for a while, and assets that have fallen tend to keep falling {jt93}. The effect also appears in an asset\u2019s own past returns, across futures, currencies and equity indices, which is the basis of trend-following funds {mop12}. A momentum strategy has to answer three practical questions: when has a move started, which way is it going, and is it too late to join."),
  P("Retail traders usually answer these questions with technical indicators drawn on a chart. TradingView is the most widely used charting platform for this, and its Pine Script language lets users write indicators and strategies and backtest them in the built-in Strategy Tester {pine}. Thousands of indicators are shared openly on the platform. Each one is tuned for a particular job and fires many false signals when used alone."),
  P("Bitcoin is a convenient market for this kind of study. It trades around the clock, so hourly data is plentiful (more than 41,000 hourly candles between January 2022 and September 2026), and it has had both strong rallies and deep crashes within a few years, which tests whether a strategy only works in one kind of market."),
  H2("1.2 Motivation"),
  P(`In September 2024 the Securities and Exchange Board of India reported that 93% of more than one crore individual traders in the equity futures and options segment lost money between FY22 and FY24, with aggregate losses above \u20b91.8 lakh crore {sebi}. The same study found that 97% of the trading profits of foreign portfolio investors and 96% of those of proprietary traders in FY24 came from algorithmic trading. Systematic, rule-based trading is not a guarantee of profit, but it removes two common causes of loss: decisions driven by fear and greed, and rules that change from one trade to the next.`),
  P("The second motivation is that building a rule-based strategy is the easy part. Testing it honestly is harder. A strategy with many settings can be adjusted until it fits past prices almost perfectly, and that fit usually disappears on new data. Bailey et al. show that, after enough trials, a high backtest Sharpe ratio is expected even when the strategy has no real edge {bblz14}. AI coding agents make this worse, because they can try hundreds of settings in an afternoon. We wanted to find out whether the same agents, given strict rules and an adversarial reviewer, could be used to tune a strategy without fooling ourselves."),
  H2("1.3 Problem Statement"),
  P("The problem addressed in this project is to design an AI-assisted momentum strategy for Bitcoin that only trades when several independent indicators agree, to tune it on historical data without overfitting, and to measure honestly how well it performs on data it has never seen. The main difficulties are:"),
  ...bullets([
    "Hourly price changes are dominated by noise, so any single indicator produces many false signals.",
    "Market regimes change. Bitcoin rose more than sixfold between January 2023 and June 2025 and then fell 28% over the following 14 months, so a strategy tuned on one period may meet a very different market next.",
    "Trading costs (commission and slippage) are large relative to the typical gain on a short-horizon trade.",
    "The strategy has 72 tunable settings. Even with only three candidate values per setting there are about 2.3 \u00d7 10\u00b3\u2074 combinations, far too many to search, and searching a large space makes overfitting more likely.",
    "TradingView\u2019s Strategy Tester cannot run hundreds of logged, controlled experiments, so a separate, faithful testing environment is needed.",
  ]),
  H2("1.4 Objectives"),
  P("The specific objectives of this project are:"),
  ...numbered([
    "To build a Pine Script v6 strategy in which each of five open-source indicators has exactly one role (entry, regime, trend, timing, confirmation), entries are taken only when all five agree, and all signals are computed on closed candles.",
    "To build a Python backtest engine that reproduces the strategy and TradingView\u2019s order-fill rules, and to verify it with automated tests for correctness and for the absence of look-ahead bias.",
    "To tune the strategy on January 2023 to June 2025 data with a multi-agent loop (tuner, executor, adversarial critic, tracker) under a hard budget of 25 parameter sets and selection rules fixed in advance.",
    "To evaluate the frozen configuration exactly once on 14 months of unseen Bitcoin data, and without re-tuning on four daily markets, and to report the results whether or not they are favourable.",
  ]),
  H2("1.5 Dataset Overview"),
  P("The primary dataset is the hourly BTC/USDT candle series from Binance spot, downloaded through the public klines endpoint {binance}. Table 1.1 summarises it. The single missing hour is left as a gap, as TradingView also has no candle for it. The file\u2019s SHA-256 hash is stored and checked before every run, so any change to the data would be detected."),
  ...table(["Attribute", "Value"], [
    ["Source", "Binance spot API, GET /api/v3/klines"],
    ["Symbol and timeframe", "BTCUSDT, 1 hour"],
    ["Fields", "time (bar open, UTC), open, high, low, close, volume"],
    ["Total candles", "41,199"],
    ["First and last candle", "2022-01-01 00:00 UTC to 2026-09-13 15:00 UTC"],
    ["Missing candles", "1 (2023-03-24 13:00 UTC), not filled"],
    ["Integrity hash (SHA-256)", "82423f2f\u2026c44a64f"],
  ], [3000, 6026], "Table 1.1: Primary Dataset (BTC/USDT, 1 Hour)"),
  P("The series is split into three periods (Table 1.2 and Figure 1.1). The warm-up year lets every indicator settle before any trade is counted. The in-sample period is the only data the tuning loop could use. The out-of-sample period was physically locked until the final configuration had been frozen."),
  ...table(["Period", "Dates (UTC)", "Candles", "Use"], [
    ["Warm-up", "2022-01-01 to 2022-12-31", "8,760", "Indicator warm-up only"],
    ["In-sample (IS)", "2023-01-01 to 2025-06-30", "21,887", "Tuning (19 runs)"],
    ["Out-of-sample (OOS)", "2025-07-01 to 2026-09-13", "10,552", "Run once with frozen parameters"],
  ], [2100, 3100, 1300, 2526], "Table 1.2: Study Periods", { align: [null, null, AlignmentType.RIGHT, null] }),
  ...figure(path.join(FIG, "fig_1_1_btc_periods.png"), "Figure 1.1: BTC/USDT Hourly Close and the Three Study Periods"),
  P("For the transfer test in Section 4.6 we also used four daily series that the strategy was never tuned on (Table 1.3). In each case the first 2,000 daily candles serve as warm-up, matching the 2,000-bar memory of the nearest-neighbour model."),
  ...table(["Market", "Source", "Daily candles", "Evaluation window"], [
    ["Bitcoin (BTCUSD)", "Bitstamp API", "5,505", "2017-02-07 to 2026-09-12"],
    ["NIFTY 50 index", "Yahoo Finance", "4,659", "2015-11-30 to 2026-09-11"],
    ["HDFC Bank (NSE)", "Yahoo Finance", "7,586", "2004-01-20 to 2026-09-11"],
    ["Reliance Industries (NSE)", "Yahoo Finance", "7,586", "2004-01-20 to 2026-09-11"],
  ], [2700, 1900, 1500, 2926], "Table 1.3: Daily Datasets Used for the Transfer Test", { align: [null, null, AlignmentType.RIGHT, null] }),
  H2("1.6 Scope and Limitations"),
  P("The study covers one strategy design, tuned on one market (Bitcoin) at one timeframe (one hour), and evaluated on one locked period plus four daily markets. Its limits are:"),
  ...bullets([
    "Position size is fixed at 10% of equity per trade, so absolute returns are small by design. Scale-free measures such as the Sharpe ratio and profit factor are the main yardsticks.",
    "Backtests model commission and slippage but not funding rates, exchange outages or the price impact of large orders.",
    "With a budget of 25 parameter sets, most of the 72 settings were never changed. The study is a disciplined local search, not a global optimisation.",
    "The in-app TradingView results depend on how much history TradingView loads, so they cover a shorter window than the Python study (Section 3.4.2).",
    "No live or paper trading was carried out.",
  ]),
  H2("1.7 Organization of the Report"),
  P("Chapter 2 reviews the literature behind each indicator, research on momentum, the statistics of backtest overfitting and work on multi-agent AI systems. Chapter 3 describes the strategy, the Python engine and its tests, and the agent-based tuning protocol. Chapter 4 presents the tuning results, the out-of-sample test, the multi-market transfer test and the TradingView run. Chapter 5 summarises the contributions and limitations and sets out the next phase of work."),
];

// ================================================================== CHAPTER 2
const ch2 = [
  H1("2. LITERATURE REVIEW / TECHNOLOGY REVIEW"),
  P("This chapter reviews the research each part of the project draws on: momentum and trend following, the two statistical models inside the strategy, the volatility and volume indicators, the statistics of backtest overfitting, and recent work on systems in which AI agents critique one another."),
  H2("2.1 Momentum and Trend Following"),
  P("Jegadeesh and Titman found that US stocks that performed best over the previous three to twelve months kept outperforming over the following months {jt93}. Moskowitz, Ooi and Pedersen later showed a related effect in each asset\u2019s own history, which they called time-series momentum: across 58 futures and forward contracts, the sign of the past year\u2019s return predicted the next month\u2019s return {mop12}. Hurst, Ooi and Pedersen extended the evidence back more than a century and found trend following profitable in every decade they studied {hop17}."),
  P("These studies work at monthly horizons on diversified portfolios. Our strategy trades a single asset on hourly candles, where the effect is weaker and costs matter more. The literature supports the premise that trends persist, but it does not show that a short-horizon version will survive trading costs. That had to be tested."),
  H2("2.2 Kernel Regression for Trend Estimation"),
  P("Nadaraya and Watson independently proposed estimating a regression function as a weighted average of nearby observations, with weights given by a kernel function {nadaraya,watson}. Applied to a price series, the estimate at time t is"),
  C("NW(t) = \u03a3 w(i) \u00b7 price(t \u2212 i) / \u03a3 w(i),   i = 0, 1, \u2026, L", { run: { italics: true } }),
  P("where w(i) falls as the lag i grows. With a Gaussian kernel, w(i) = exp(\u2212i\u00b2 / 2h\u00b2), where h is the bandwidth. A small bandwidth tracks price closely; a large one gives a smoother line that reacts more slowly."),
  P("Many Nadaraya-Watson indicators on TradingView use a centred window that includes future bars. These redraw past values as new data arrives (\u201crepainting\u201d) and make backtests look far better than live trading would be. The QuantAlgo script we used {quantalgo} computes only the causal endpoint estimate shown above, which uses current and past bars and never changes a value once a bar has closed. We use the slope of this line as the trend filter."),
  H2("2.3 Nearest-Neighbour Classification"),
  P("Cover and Hart showed that the nearest-neighbour rule, which labels a new point with the label of the closest training example, has an error rate at most twice the Bayes optimal rate as the training set grows {coverhart}. The k-nearest-neighbour (KNN) version takes a vote among the k closest examples. KNN needs no training step and makes few assumptions about the data, which suits financial series whose patterns drift over time."),
  P("The Machine Learning: Lorentzian Classification script by jdehorty applies KNN to price data {jdehorty}. Each candle is described by up to five normalised features chosen from RSI, WaveTrend, CCI and ADX {wilder,lambert}. Distance between two candles is measured with the Lorentzian metric, the sum over features of log(1 + |a\u2096 \u2212 b\u2096|). The logarithm reduces the influence of a single extreme feature difference, which matters in markets where large moves distort Euclidean distance. The script searches the last 2,000 candles, takes every fourth one to reduce correlation between neighbours, and keeps the closest k. Their labels are summed into a prediction whose sign gives the direction."),
  H2("2.4 Volatility and Volume Indicators"),
  P("John Carter\u2019s TTM Squeeze compares Bollinger Bands, which measure volatility through the standard deviation of price {bollinger}, with Keltner Channels, which use the average true range {carter}. When the Bollinger Bands sit inside the Keltner Channels, volatility is compressed (\u201csqueeze on\u201d). When they move outside, the squeeze has \u201cfired\u201d and a larger move often follows. LazyBear\u2019s Squeeze Momentum script implements this idea {lbsqz}, and we use it only as a regime gate: no new trade is allowed while volatility is compressed."),
  P("LazyBear\u2019s WaveTrend oscillator smooths the distance between price and its exponential moving average, scaled by average deviation, into two lines, WT1 and WT2 {lbwt}. Values far above zero mean the market is overbought and values far below mean it is oversold. We use WaveTrend for timing: a long entry is refused if WT1 is already above an overbought cap, because the move is likely to be exhausted."),
  P("David Weis adapted Richard Wyckoff\u2019s method by grouping price into up-waves and down-waves and adding up the volume traded in each wave {weis}. A rising wave with growing volume suggests buyers are committed. The Weis Wave Volume indicator gives the direction of the current wave, which we use to confirm that the direction of a proposed trade matches the direction of the current volume wave."),
  H2("2.5 Backtest Overfitting and Multiple Testing"),
  P("A backtest is a single draw from a noisy process. If many strategy variants are tried and the best is reported, its measured performance is biased upwards. Bailey, Borwein, L\u00f3pez de Prado and Zhu show how quickly this happens: with only a few years of daily data, trying a few dozen configurations is enough to find one with an impressive in-sample Sharpe ratio that has no out-of-sample value {bblz14}. Harvey, Liu and Zhu make the same point about academic factor research and argue that a t-statistic above 3.0, not 2.0, should be required once many tests have been run {hlz16}."),
  P("Two statistics from this literature are used directly in the project. The Probabilistic Sharpe Ratio (PSR) gives the probability that the true Sharpe ratio is above a benchmark, allowing for track-record length, skewness and fat tails in the returns {psr}. The Deflated Sharpe Ratio (DSR) raises that benchmark to the Sharpe ratio expected from the best of N unskilled trials, so that every additional trial makes the test harder to pass {dsr}. L\u00f3pez de Prado also recommends recording every trial, fixing selection rules before testing and keeping a true hold-out set untouched until the end {lopez18}. Our protocol in Section 3.6 follows these recommendations."),
  H2("2.6 Multi-Agent AI Systems and Adversarial Review"),
  P("Large language model agents can write code, run experiments and read results, which makes them useful for repetitive research loops. They also tend to accept their own conclusions too readily. Irving, Christiano and Amodei proposed AI safety via debate, in which two agents argue opposite sides so that a judge can spot flaws neither would admit alone {irving18}. Du et al. found that letting several language model instances critique each other\u2019s answers over several rounds improved factual accuracy and reasoning {du23}, and Madaan et al. showed gains from having a model critique and revise its own output {madaan23}."),
  P("We applied these ideas to strategy tuning. Instead of one agent that both proposes and judges changes, the tuning loop separates the roles and gives the judging role to an agent instructed to act as a hostile risk committee. The agents were run with Claude Code subagents {claudecode}."),
  H2("2.7 Evaluation Metrics"),
  P("The Sharpe ratio, the mean excess return divided by the standard deviation of returns, is the standard measure of return per unit of risk {sharpe94}. The Sortino ratio penalises only downside deviation {sortino94}. Trading studies also report the profit factor (gross profit divided by gross loss), the win rate, the maximum drawdown (the largest fall from a previous equity peak) and the t-statistic of mean trade return. A strategy that earns less than buy-and-hold in absolute terms can still be useful if it earns more per unit of risk or carries much less drawdown, so all of these are reported against buy-and-hold on the same window."),
  H2("2.8 Research Gap"),
  P("Open-source indicator scripts are usually shared with in-app backtests that do not show how many settings were tried, use repainting calculations or leave out costs. Academic momentum research, on the other hand, rarely deals with the practical details of short-horizon execution. We found little work that combines published community indicators into a role-based strategy and then tests it with multiple-testing corrections, a pre-registered hold-out and an AI tuning loop whose every trial is logged. This project aims to fill that gap at the scale of a student capstone."),
];

// ================================================================== CHAPTER 3
const ch3 = [
  H1("3. METHODOLOGY"),
  P("This chapter describes the data handling, the design of the strategy, the Python engine used to test it, the checks that the engine is correct, and the protocol under which the AI agents tuned it."),
  H2("3.1 System Overview"),
  P("The system has two halves (Figure 3.1). The first is the strategy itself, written in Pine Script v6 so that it runs on TradingView. The second is a Python research environment that loads the hourly data, recomputes every indicator exactly as Pine does, simulates TradingView\u2019s broker, computes performance metrics and records every experiment in an append-only log. The multi-agent tuning loop works only through this environment. When tuning finished, the chosen parameters were copied back into the Pine script as its default inputs."),
  ...figure(path.join(FIG, "fig_3_1_architecture.png"), "Figure 3.1: System Architecture and Methodology Flow"),
  H2("3.2 Data Preparation"),
  H3("3.2.1 Collection and Integrity"),
  P("The script `data/fetch_data.py` downloads hourly candles from the Binance klines endpoint in pages, stores the bar open time in UTC and keeps only fully closed candles. It writes a metadata file with the fetch time, row count, first and last candle, the list of gaps and the SHA-256 hash of the CSV file. Gaps are not filled, because filling them would create candles that TradingView does not have. The one missing hour was the only gap found."),
  H3("3.2.2 Data Isolation"),
  P("Look-ahead and data leakage were treated as the most serious risks. Three rules were enforced in code, not left to discipline:"),
  ...numbered([
    "For any in-sample run, the data frame is cut at 2025-06-30 23:00 UTC before any indicator is computed, so no in-sample calculation can see later prices.",
    "Every in-sample run goes through one command, `run_backtest.py is`, which refuses to run if the run number is not the next in sequence, if the 25-run cap is reached, if the same configuration was already tried or if the data hash has changed.",
    "The out-of-sample command, `run_backtest.py oos`, writes a LOCK file before it computes anything and refuses to run if that file exists. It can therefore be run only once.",
  ]),
  H3("3.2.3 Daily Market Data"),
  P("For the transfer test, daily candles were downloaded from Bitstamp for Bitcoin (matching TradingView\u2019s BITSTAMP:BTCUSD symbol) and from Yahoo Finance for NIFTY 50, HDFC Bank and Reliance Industries. Each series was checked for missing values, impossible OHLC combinations and calendar gaps, and hashed in the same way as the hourly data."),
  H2("3.3 Strategy Design"),
  P("The strategy is called the Combined Role-Based (CRB) strategy. Its main design rule is that each indicator does one job only. Table 3.1 lists the roles and Figure 3.2 shows how they combine."),
  ...table(["Role", "Indicator (author)", "Condition for a long entry (short is mirrored)"], [
    ["Entry", "Lorentzian Classification (jdehorty)", "KNN signal flipped to long within the last 2 bars, is still long, and that flip has not yet produced a trade"],
    ["Regime gate", "Squeeze Momentum (LazyBear)", "Squeeze is off: Bollinger Bands are outside the Keltner Channels"],
    ["Trend", "Nadaraya-Watson Trend (QuantAlgo)", "NW line higher than 3 bars ago and close above the line"],
    ["Timing", "WaveTrend (LazyBear)", "WT1 below the overbought cap (40 after tuning)"],
    ["Confirmation", "Weis Wave Volume", "Current Weis wave direction is up"],
  ], [1500, 2900, 4626], "Table 3.1: Indicator Roles in the CRB Strategy"),
  ...figure(path.join(FIG, "fig_3_2_pipeline.png"), "Figure 3.2: The Five-Role Entry Decision"),
  P("The final entry rule is a logical AND of the five role conditions, evaluated only when the candle has closed. The code below is taken directly from the strategy script."),
  ...code([
    "bool barConfirmed = barstate.isconfirmed",
    "bool longCondition  = barConfirmed and allowLongs and regimeGate",
    "     and trendLong and entryLong and timingLong and confirmLong",
    "bool shortCondition = barConfirmed and allowShorts and regimeGate",
    "     and trendShort and entryShort and timingShort and confirmShort",
  ]),
  H3("3.3.1 Entry: Lorentzian Classification"),
  P("The KNN model uses five features: RSI(14), WaveTrend(10, 11), CCI(20), ADX(20) and RSI(9), each normalised to the range 0 to 1. The training label for each historical candle compares its close with the close four candles earlier. The model searches the previous 2,000 candles and keeps 12 neighbours after tuning (8 by default). The original script also filters predictions with its own kernel-regression and moving-average filters. We removed those, because trend direction belongs to the Nadaraya-Watson role alone, and kept only the script\u2019s volatility and regime filters. To stop one signal from producing several trades, an entry is allowed only within two candles of the flip and only once per flip."),
  H3("3.3.2 Regime: Squeeze Momentum"),
  P("Bollinger Bands and Keltner Channels are both computed over 20 candles. The gate opens when the squeeze is off, that is, when volatility has expanded. The script supports two other modes (\u201cnot in squeeze\u201d and \u201creleased within N bars\u201d). One of these was tested during tuning (run 8) and rejected."),
  H3("3.3.3 Trend: Nadaraya-Watson Kernel Regression"),
  P("The trend line uses a Gaussian kernel over the last 50 candles with an effective bandwidth of 5 \u00d7 2.0 = 10 after tuning. A long trade needs the line to be higher than it was three candles earlier and the close to be above it. Requiring price to be on the correct side of the line was one of the earliest useful changes (run 4)."),
  H3("3.3.4 Timing: WaveTrend"),
  P("By default the timing role required a recent WT1/WT2 crossover and WT1 below a cap of 53. Tuning changed this to the cap alone (run 5) and lowered the cap to 40 (run 17), so the strategy refuses to buy when WT1 is above 40 and refuses to sell short when it is below \u221240."),
  H3("3.3.5 Confirmation: Weis Wave Volume"),
  P("Waves are formed with an ATR(14)-based reversal size, and the current wave direction must match the trade direction. An optional rule requiring the wave\u2019s volume to exceed its average was tested in run 9 and rejected."),
  H3("3.3.6 Exits, Risk Control and Position Sizing"),
  P("Each entry places a stop-loss two ATR(14) below the entry price and a take-profit three ATR(14) above it for a long trade, and the reverse for a short. Because both levels are set in units of ATR, they widen in volatile markets and tighten in quiet ones. A position is also closed if the KNN signal flips against it or once it has been held for 12 candles. Table 3.2 lists the fixed trading properties, which match the Pine script\u2019s strategy() settings."),
  ...table(["Property", "Base case", "Stress case"], [
    ["Initial capital", "$10,000", "$10,000"],
    ["Position size", "10% of equity per trade", "10% of equity per trade"],
    ["Pyramiding", "None (one position at a time)", "None"],
    ["Commission", "0.075% per side", "0.10% per side"],
    ["Slippage", "2 ticks ($0.02) on market and stop fills", "5 basis points on market and stop fills"],
    ["Stop-loss / take-profit", "2 \u00d7 ATR / 3 \u00d7 ATR", "Same"],
    ["Maximum holding period", "12 candles", "Same"],
  ], [2600, 3300, 3126], "Table 3.2: Trading Properties and Cost Scenarios"),
  P("The stress case is deliberately harsher than Binance\u2019s retail fees. A strategy whose profit disappears under it has too little margin over its trading costs."),
  H2("3.4 Python Backtest Engine"),
  P("TradingView cannot run large numbers of logged experiments, so we rebuilt the strategy and TradingView\u2019s order handling in Python. The engine has four modules."),
  H3("3.4.1 Signal Engine"),
  P("`engine/pine_ta.py` re-implements every Pine built-in the strategy uses (sma, ema, rma, rsi, cci, atr, linreg, crossover, barssince and others), matching Pine\u2019s handling of missing values and its seeding rules. For example, Pine seeds an EMA with the simple average of its first n values. `engine/mlext.py` ports the feature and filter functions from the MLExtensions library used by the Lorentzian script. The nearest-neighbour search runs once per candle over up to 2,000 previous candles, so it is compiled with Numba {numba}. One full in-sample backtest of 21,887 candles takes about 2.4 seconds."),
  H3("3.4.2 A Documented Deviation (D1)"),
  P("The original Lorentzian script anchors its search window to the last bar of the chart. On TradingView this means it produces predictions only for the most recent 2,000 candles on the chart, and earlier candles get none. That behaviour cannot be reproduced fairly in a backtest that walks forward through time. The Python engine therefore applies the script\u2019s stated intent, a search over the most recent 2,000 candles, at every candle in a strictly causal way. This difference, recorded in the specification as deviation D1, is the main reason why TradingView\u2019s own Strategy Tester covers a shorter window than our study (Section 4.7)."),
  H3("3.4.3 Broker Emulator"),
  P("`engine/broker.py` follows TradingView\u2019s strategy semantics candle by candle. Orders created at the close of a candle are filled at the next candle\u2019s open, plus adverse slippage. Stop and take-profit levels are checked within each candle along the price path TradingView assumes: if the open is closer to the high, the path is open, high, low, close, and otherwise open, low, high, close. If a candle opens beyond a stop or target level, the order fills at the open. Commission is charged on every fill. An opposite entry closes and reverses the position in one order, as in Pine. Any open position is closed at the end of the test window."),
  H3("3.4.4 Metrics"),
  P("`engine/metrics.py` converts the hourly equity curve to daily returns and computes the measures fixed in the specification before tuning began. The main ones are:"),
  ...bullets([
    "Annualised Sharpe ratio = mean(r) / std(r) \u00d7 \u221a365, using daily simple returns r with a zero risk-free rate; Sortino ratio uses downside deviation only.",
    "Maximum drawdown and its duration, Calmar ratio, profit factor, win rate with a 95% confidence interval, average and median trade return, longest losing streak and the t-statistic of trade returns.",
    "PSR(0), the probability that the true Sharpe ratio is above zero, adjusted for skewness and kurtosis {psr}.",
    "DSR across all logged trials, using the variance of Sharpe ratios across trials and the expected maximum of N unskilled Sharpe ratios {dsr}.",
    "Results by sub-period (2023, 2024 and the first half of 2025), long and short trades separately, the same run under stress costs, and buy-and-hold over the same window.",
  ]),
  H2("3.5 Verification of the Engine"),
  P("A tuning study is only as good as the engine that scores it, so the engine was tested before the first tuning run. The suite has 66 test functions, which expand to 88 test cases through parametrisation. All 88 passed when the study was run and again when this report was prepared. Table 3.3 lists the suites."),
  ...table(["Test file", "Tests", "What it checks"], [
    ["test_ta.py", "7", "Each Pine built-in against a slow, independent pure-Python loop"],
    ["test_lc_ann.py", "1", "Numba nearest-neighbour search against a literal translation of the specification"],
    ["test_lc_state.py", "8", "KNN signal state, entry window and one-trade-per-flip rule against a bar-by-bar reference"],
    ["test_causality.py", "2", "Signals on a prefix of the data equal signals on the full data; changing a future candle never changes a past signal"],
    ["test_broker.py", "17", "Hand-computed fills: next-open entries, intrabar stops, gaps through levels, same-candle stop and target, reversals, window end"],
    ["test_crosscheck_backtestingpy.py", "1", "Equity and trades match the independent backtesting.py library on synthetic data"],
    ["test_metrics.py", "11", "Sharpe, Sortino, drawdown, PSR, DSR and gates against hand calculations"],
    ["test_params.py", "5", "Every Pine input default is present, within bounds and hashed consistently"],
    ["test_guards.py", "14", "Run sequencing, 25-run cap, duplicate refusal, in-sample truncation, data-hash check, one-shot OOS lock, tamper detection"],
  ], [2700, 800, 5526], "Table 3.3: Automated Test Suites", { size: 21, align: [null, AlignmentType.CENTER, null] }),
  P("The causality tests matter most. They run the signal engine on the first part of a series and then on the whole series, and check that every signal in the overlap is identical. They also perturb a future candle and confirm that no earlier signal changes. Together these rule out look-ahead bias in the signal engine. The cross-check against backtesting.py {btpy} confirms that the broker\u2019s fills, costs and position sizing agree with an implementation we did not write."),
  H2("3.6 Multi-Agent Tuning Protocol"),
  H3("3.6.1 Code Review Before Tuning"),
  P("Two Claude Code agents were defined for the strategy script itself. The builder agent wrote and edited the Pine code under the role rules in Table 3.1 and a fixed list of requirements (Pine v6, commission and slippage set, all thresholds exposed as inputs, signals on confirmed bars only, no repainting estimators). The adversary agent, which could read but not edit files, reviewed each version for repainting, look-ahead bias, unrealistic fills, small samples and signs of overfitting, and reported each issue with its severity and a fix."),
  H3("3.6.2 Agent Roles in the Tuning Loop"),
  P("Each tuning iteration passed through four agents in a fixed order (Figure 3.3 and Table 3.4)."),
  ...table(["Agent", "Responsibility", "Restrictions"], [
    ["Tuner", "Reads the log, leaderboard and all critic verdicts; writes exactly one new parameter set and states its hypothesis and expected effect", "May not run backtests or look at price data in any form; must keep values round and change few parameters at a time"],
    ["Executor", "Runs the logged in-sample backtest and reports the metrics", "May not edit engine code or configurations"],
    ["Adversarial critic", "Acts as a hostile risk committee: scores risk-adjusted return, drawdown, significance, robustness and costs; lists weaknesses with numbers; demands the next experiment; returns CONTINUE or PLATEAU", "Read-only; must assume the result is overfitted; may not praise without numbers"],
    ["Tracker", "Saves the critic\u2019s verdict verbatim, re-renders the log and leaderboard, and verifies the log\u2019s integrity", "Must report a failed integrity check"],
  ], [1700, 4200, 3126], "Table 3.4: Agent Roles in the Tuning Loop", { size: 21 }),
  ...figure(path.join(FIG, "fig_3_3_tuning_loop.png"), "Figure 3.3: The Tuning Loop", 5.2),
  P("The separation is deliberate. The agent that proposes a change never judges it, and the agent that judges it is rewarded for finding faults. Keeping the tuner away from price data stops it from designing a change around patterns it has seen in the chart, so every idea has to be tested through the logged executor and counts against the budget."),
  H3("3.6.3 Budget and Pre-registered Selection Rule"),
  P("Before run 1, the following rules were written into the specification and could not be changed afterwards. The budget was 25 in-sample parameter sets, counted by the run command itself. A run was eligible for selection only if it passed all four gates in Table 3.5. The best run was the eligible run with the highest in-sample Sharpe ratio. If no run passed all four gates, the fallback was the highest Sharpe among runs with at least 30 trades, flagged as \u201cFAILED PRE-REGISTERED GATES\u201d."),
  ...table(["Gate", "Rule", "Purpose"], [
    ["G1", "At least 100 trades", "Enough trades for the statistics to mean something"],
    ["G2", "Profit factor above 1.0", "Profitable after base costs"],
    ["G3", "Net return above zero under stress costs", "Profit margin large enough to survive harsher costs"],
    ["G4", "Net return above zero in at least 2 of the 3 sub-periods (2023, 2024, 2025 H1)", "Not dependent on one lucky period"],
  ], [900, 4400, 3726], "Table 3.5: Pre-registered Selection Gates"),
  H3("3.6.4 Stopping Rule, Freeze and Out-of-Sample Test"),
  P("The loop stopped when the critic declared a plateau or when run 25 was logged. The critic could declare a plateau only if at least five consecutive runs had failed to raise the best eligible Sharpe by 0.05, every role had been probed, and it judged that further search would be mining noise. After the plateau, a freeze command applied the selection rule and wrote the chosen parameters, with their hash, to `FROZEN_PARAMS.json`. The out-of-sample command was then run once on the full continuous series, with indicators warmed up from 2022 and entries allowed only in the locked window."),
  H2("3.7 Multi-Market Transfer Test"),
  P("After the out-of-sample test, the frozen parameters were applied unchanged to the four daily series in Table 1.3 using the same engine. For each market we recorded the signal funnel (how many candidate signals survived each role), base and stress results, long-only results and buy-and-hold. The same markets were also run with the original Pine defaults, so that the effect of tuning on each market could be seen."),
  H2("3.8 Implementation Details"),
  ...table(["Component", "Tools and versions"], [
    ["Strategy", "Pine Script v6 on TradingView; 518 lines, 72 tunable inputs grouped by role"],
    ["Backtest engine", "Python 3.13 with NumPy, pandas, Numba, SciPy and PyArrow; 5,356 lines including tests and the multi-market scripts"],
    ["Testing", "pytest (88 test cases); backtesting.py 0.6.6 for the independent cross-check"],
    ["AI agents", "Claude Code subagents (builder, adversary, tuner, executor, critic, tracker) with written role briefs"],
    ["Logging", "Append-only JSONL log, Markdown log and leaderboard rendered from it, per-run result folders, critic verdict files"],
    ["Hardware", "Windows 11 desktop; about 2.4 seconds per 2.5-year hourly backtest after compilation"],
  ], [2400, 6626], "Table 3.6: Implementation Environment"),
];

// ================================================================== CHAPTER 4
const runDesc = {
  1: "Pine defaults (baseline)", 2: "Hold 12 bars, take-profit on", 3: "Run 2 + stop-loss 3.0 ATR", 4: "Run 2 + NW slope 3, price on trend side",
  5: "Run 4 + WT cap only (no cross)", 6: "Run 5 + KNN neighbours 12", 7: "Run 6 with neighbours 14", 8: "Run 6 + SQZ released-within-window",
  9: "Run 6 + WWV volume threshold", 10: "Run 6 + KNN horizon 8", 11: "Run 6 + NW bandwidth 5", 12: "Run 11 + 4 KNN features",
  13: "Run 11 + fixed-hold exit mode", 14: "Run 11 + take-profit 2.0 ATR", 15: "Run 11, no take-profit, hold 20", 16: "Run 11 + KNN feature 1 = ADX(50)",
  17: "Run 11 + WT caps \u00b140", 18: "Run 11 + WT caps \u00b145", 19: "Run 17 + WWV part-of-price 400",
};
const runRows = R.map((r) => [
  r.id === 17 ? "**17**" : String(r.id), r.id === 17 ? "**" + runDesc[r.id] + "**" : runDesc[r.id],
  f(r.sharpe, 3), f(r.pf, 3), String(r.trades), fs_(r.net), fs_(r.stress), r.gates.split("").join(" "),
]);

const ch4 = [
  H1("4. RESULTS AND DISCUSSION"),
  P("This chapter reports the tuning results, the selected configuration and the critic\u2019s objections to it, the one-time out-of-sample test, the transfer test on four daily markets and the strategy running on TradingView. All figures come from the result files written by the engine. Unless stated otherwise, returns are for a $10,000 account trading 10% of equity per position, after base costs."),
  H2("4.1 Baseline: The Untuned Strategy"),
  P(`Run 1 used the default inputs of every indicator. Over the in-sample period it lost 3.51% with a Sharpe ratio of \u22121.71 and a profit factor of 0.52 across 117 trades. Its trade t-statistic was \u22122.69, so the losses were not bad luck. The short side was the main problem: 66 short trades returned a profit factor of 0.36. Trades were closed after an average of 3.5 candles, mostly by the default 4-candle timer, before any target could be reached, and the take-profit order was switched off. In its first verdict the critic pointed to the short trades fighting a strong bull market, to the 4-candle timer doing almost all of the exit work, and to a payoff ratio below 1 (average loss larger than average win). It demanded probes of the short side, the exits, the stop distance and the trend filter.`),
  H2("4.2 The Tuning Trajectory"),
  P("Table 4.1 lists all 19 runs and Figure 4.1 shows their in-sample Sharpe ratios. Only five of the 18 changes beat the best result so far (runs 2, 4, 5, 6 and 17). The rest were refuted and recorded, which is what the critic was meant to make happen."),
  ...table(["Run", "Change", "Sharpe", "PF", "Trades", "Net %", "Stress %", "Gates G1\u2013G4"],
    runRows, [520, 2880, 820, 740, 760, 800, 920, 1586],
    "Table 4.1: In-sample Results of All 19 Tuning Runs (P = pass, F = fail)",
    { size: 19, align: [AlignmentType.CENTER, null, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.CENTER] }),
  ...figure(path.join(FIG, "fig_4_1_sharpe_runs.png"), "Figure 4.1: In-sample Sharpe Ratio of Each Tuning Run"),
  P("The runs fall into five phases."),
  ...numbered([
    "**Exits (runs 2\u20133).** Holding for 12 candles and enabling the 3 ATR take-profit lifted the Sharpe ratio from \u22121.71 to \u22120.67. Widening the stop to 3 ATR made it worse.",
    "**Trend and timing (runs 4\u20135).** Requiring a three-candle slope with price on the correct side of the Nadaraya-Watson line, then dropping the WaveTrend crossover requirement, brought the strategy close to break-even.",
    "**Entry model (runs 6\u20137).** Raising the KNN neighbour count from 8 to 12 gave the first positive Sharpe ratio (0.23). A neighbourhood probe at 14 gave 0.18, so the gain was not a single-value spike.",
    "**Filters and structure (runs 8\u201316).** Stricter regime and volume filters, a longer label horizon, fewer features, a different exit mode, tighter and looser targets and a different first feature were all tried. None beat run 6. Several of these runs showed a pattern the critic kept pointing out: filters that only cut the number of trades did not improve the typical trade.",
    "**WaveTrend cap (runs 17\u201319).** Lowering the overextension cap from \u00b153 to \u00b140 produced the best Sharpe of the study (0.355). The demanded neighbourhood check at \u00b145 gave 0.196, lower than both neighbours, and a final volume-wave change gave \u22120.12. After run 19 the critic declared a plateau, with 6 of the 25 slots unused.",
  ]),
  H2("4.3 The Selected Configuration"),
  P("No run passed all four gates. Every run with a positive Sharpe ratio failed G3, profitability under stress costs, so the pre-registered fallback rule applied. It selected run 17, the highest Sharpe among runs with at least 30 trades, and flagged it \u201cFAILED PRE-REGISTERED GATES\u201d. Run 17 passes G1, G2 and G4 and fails G3 with \u22121.42% under stress costs. Table 4.2 lists the nine inputs that differ from the indicator defaults. The other 63 inputs were never changed."),
  ...table(["Input", "Role", "Default", "Run 17"], [
    ["exitHoldBars", "Exit", "4", "12"],
    ["riskUseTp", "Exit", "false", "true (3 \u00d7 ATR)"],
    ["nwSlopeLen", "Trend", "1", "3"],
    ["nwRequirePriceSide", "Trend", "false", "true"],
    ["nwBandwidth", "Trend", "8", "5"],
    ["lcNeighbors", "Entry", "8", "12"],
    ["wtTimingMode", "Timing", "Recent Cross + Not Overextended", "Not Overextended Only"],
    ["wtObLevel2", "Timing", "53", "40"],
    ["wtOsLevel2", "Timing", "\u221253", "\u221240"],
  ], [2500, 1300, 2900, 2326], "Table 4.2: Inputs Changed by Tuning (Configuration Hash b8376d7d48f5)"),
  P("Table 4.3 compares run 17 with the baseline on the in-sample period, and Figure 4.2 shows the two equity curves."),
  ...table(["Metric", "Run 1 (defaults)", "Run 17 (selected)"], [
    ["Net return", "\u22123.51%", "+1.12%"],
    ["Sharpe ratio (annualised)", "\u22121.71", "0.36"],
    ["Sortino ratio", "\u22122.10", "0.55"],
    ["Profit factor", "0.52", "1.10"],
    ["Win rate (95% CI)", "36.8% (28.6\u201345.8%)", "47.9% (40.8\u201355.0%)"],
    ["Average win / average loss", "0.90% / \u22121.00%", "1.39% / \u22121.16%"],
    ["Maximum drawdown", "4.20%", "1.49%"],
    ["Trades (long / short)", "117 (51 / 66)", "188 (95 / 93)"],
    ["Profit factor long / short", "0.75 / 0.36", "1.11 / 1.09"],
    ["Longest losing streak", "9", "6"],
    ["Average holding period", "3.5 candles", "7.7 candles"],
    ["Time in market", "1.9%", "6.6%"],
    ["Trade t-statistic", "\u22122.69", "0.54"],
    ["PSR (Sharpe > 0)", "0.003", "0.715"],
    ["Net return under stress costs", "\u22125.19%", "\u22121.42%"],
    ["Buy-and-hold BTC, same window", "+547.7%, Sharpe 1.79, max drawdown 32.3%", "same"],
  ], [3200, 2913, 2913], "Table 4.3: Baseline versus Selected Configuration (In-sample, Jan 2023 to Jun 2025)", { size: 21 }),
  ...figure(path.join(FIG, "fig_4_2_is_equity.png"), "Figure 4.2: In-sample Account Value, Baseline versus Run 17"),
  P("By every risk measure in the table, tuning turned a strategy that was clearly losing into one that was slightly profitable, with long and short trades both profitable and a lower drawdown. Two numbers in the same table keep this in proportion. A trade t-statistic of 0.54 is far from statistical significance, and buy-and-hold Bitcoin earned a Sharpe ratio of 1.79 over the same window, about five times the strategy\u2019s."),
  H2("4.4 The Critic\u2019s Objections to Run 17"),
  P("The critic did not accept run 17 at face value. Its verdicts on runs 17 and 19 recorded the following problems, each backed by the result files."),
  ...table(["Check", "Finding"], [
    ["Concentration", "The two largest winners ($90.32) made up 80% of the $112.32 net profit. Without the top three trades the net result was \u2212$11.35."],
    ["Sub-periods", "2023: +0.04% (profit factor 1.01, effectively break-even); 2024: +1.83% (Sharpe 1.27); 2025 H1: \u22120.73%. The G4 pass rested on a near-zero 2023."],
    ["Costs", "+1.12% under base costs became \u22121.42% under stress costs (G3 fail). The average net trade (+0.06%) was smaller than the extra round-trip cost of the stress case (about 0.15 percentage points)."],
    ["Neighbourhood", "The WaveTrend cap went \u00b153 \u2192 \u00b145 \u2192 \u00b140 with Sharpe 0.21 \u2192 0.20 \u2192 0.36: a dip followed by a spike, the signature of a narrow peak, not a broad effect."],
    ["Multiple testing", "PSR was 0.715, but the Deflated Sharpe Ratio over 19 trials was only 0.187: about 19% confidence that the Sharpe ratio beats what the best of 19 unskilled trials would be expected to produce."],
  ], [2000, 7026], "Table 4.4: Robustness Checks on the Selected Configuration", { size: 21 }),
  P("The critic\u2019s final verdict listed these points as caveats that the write-up must carry and said that out-of-sample results should be read \u201cwith wide skepticism, not as edge confirmation\u201d. That verdict was saved before the out-of-sample data was opened."),
  H2("4.5 Out-of-Sample Test"),
  P("The frozen run 17 configuration was run once on the locked period from 1 July 2025 to 13 September 2026. Over this period Bitcoin fell 28.0%, and at its worst point it was 53.7% below its previous peak. Table 4.5 sets the result beside the in-sample figures, and Figures 4.3 and 4.4 show the equity curves."),
  ...table(["Metric", "In-sample (run 17)", "Out-of-sample (run 17, frozen)"], [
    ["Net return", "+1.12%", "\u22123.12%"],
    ["Final account value", "$10,112", "$9,688"],
    ["Sharpe ratio", "0.36", "\u22121.93"],
    ["Profit factor", "1.10", "0.60"],
    ["Win rate (95% CI)", "47.9% (40.8\u201355.0%)", "35.2% (27.4\u201343.9%)"],
    ["Trades (long / short)", "188 (95 / 93)", "125 (64 / 61)"],
    ["Profit factor long / short", "1.11 / 1.09", "0.53 / 0.67"],
    ["Maximum drawdown", "1.49%", "3.72%"],
    ["Longest losing streak", "6", "16"],
    ["Trade t-statistic", "0.54", "\u22122.43"],
    ["Net return under stress costs", "\u22121.42%", "\u22124.81%"],
    ["Sub-periods", "2023 +0.04%, 2024 +1.83%, 2025 H1 \u22120.73%", "2025 H2 \u22121.03%, 2026 YTD \u22122.11%"],
    ["Buy-and-hold BTC", "+547.7% (max drawdown 32.3%)", "\u221228.0% (max drawdown 53.7%)"],
  ], [2900, 3063, 3063], "Table 4.5: In-sample versus Out-of-sample Performance", { size: 21 }),
  ...figure(path.join(FIG, "fig_4_3_oos_equity.png"), "Figure 4.3: Out-of-sample Value of $10,000, Strategy versus Bitcoin Buy-and-Hold"),
  ...figure(path.join(FIG, "fig_4_4_oos_zoom.png"), "Figure 4.4: Out-of-sample Strategy Equity under Base and Stress Costs"),
  P("The in-sample edge did not survive. The strategy lost money in both halves of the period, on both long and short trades, and its trade t-statistic of \u22122.43 means the losses are unlikely to be chance alone. The win rate fell by about 13 points while the ratio of average win to average loss stayed close to its in-sample value (1.10 against 1.20), which suggests that the entries, not the exits, stopped working in the new market."),
  P("The comparison with buy-and-hold needs care. The strategy kept 96.9% of its capital while buy-and-hold kept 72.0%, but most of that difference comes from position sizing, not skill. The strategy held a position only 9.7% of the time, each at 10% of equity, so on average less than 1% of the account was exposed to Bitcoin. A passive position of that average size would have lost roughly 0.3% over the period, less than the strategy lost. The risk controls did limit damage (the worst drawdown was 3.7%), but the strategy did not protect capital better than an equally small passive position would have."),
  H2("4.6 Transfer to Daily Markets"),
  P("Table 4.6 shows the frozen parameters applied without change to four daily markets, alongside the result with the original defaults. Figure 4.5 shows the same comparison."),
  ...table(["Market", "Trades", "Net % (defaults)", "Net % (run 17)", "Profit factor", "Win rate", "Stress net %"], [
    ["Bitcoin 1D (2017\u20132026)", "39", "+3.67", "\u22120.43", "0.97", "51.3%", "\u22120.83"],
    ["NIFTY 50 1D (2015\u20132026)", "52", "\u22121.32", "\u22121.19", "0.81", "44.2%", "\u22121.91"],
    ["HDFC Bank 1D (2004\u20132026)", "58", "\u22120.83", "\u22125.60", "0.61", "36.2%", "\u22125.83"],
    ["Reliance 1D (2004\u20132026)", "75", "+0.63", "+6.05", "1.47", "58.7%", "+5.49"],
  ], [2700, 900, 1250, 1200, 1150, 1000, 826], "Table 4.6: Frozen Parameters Applied to Four Daily Markets", { size: 21, align: [null, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT, AlignmentType.RIGHT] }),
  ...figure(path.join(FIG, "fig_4_6_multimarket.png"), "Figure 4.5: Net Return by Market, Default versus Tuned Parameters"),
  P("Reliance Industries was the one clear success. The tuned settings lifted its 22-year result from +0.63% to +6.05%, with a profit factor of 1.47, a 58.7% win rate and a profit that held under stress costs (+5.49%). On the other three markets the result was flat or negative, and on Bitcoin daily and HDFC Bank the tuned settings did worse than the defaults. One positive market out of four, with a trade t-statistic of 1.28 on that market, is consistent with chance. We report Reliance as an encouraging case, not as evidence that the tuning transfers."),
  P("Figure 4.6 shows the signal funnel on Reliance. Of 502 candidate signals from the KNN model, 75 survived all five roles, so 85% were filtered out. The regime gate removed the most (502 to 150), and the trend filter removed most of what remained (150 to 93). The volume confirmation removed only one signal at this stage, which suggests it adds little once the trend filter is in place."),
  ...figure(path.join(FIG, "fig_4_5_funnel.png"), "Figure 4.6: Signal Funnel on Reliance Industries (Daily, 2004\u20132026)", 5.6),
  H2("4.7 The Strategy on TradingView"),
  P("The frozen parameters were written into the Pine script as its default inputs and the strategy was loaded on TradingView. Figure 4.7 shows it on the BTCUSD daily chart with TradingView\u2019s own Strategy Tester. The green and red line is the Nadaraya-Watson trend filter, and the line at the top of the chart lists the full parameter set."),
  ...figure(path.join(PROJ, "Final_Review_PPT/screenshots/tv_chart_main.png"), "Figure 4.7: CRB Strategy on TradingView (BTCUSD Daily) with Key Stats"),
  ...table(["Strategy Tester statistic", "Value"], [
    ["Total P&L", "+$211.71 (+2.12%)"],
    ["Profitable trades", "56.52% (13 of 23)"],
    ["Profit factor", "1.298"],
    ["Maximum drawdown", "$369.75 (3.60%)"],
  ], [4513, 4513], "Table 4.7: TradingView Strategy Tester Results, BTCUSD Daily (6 Oct 2026)"),
  P("These numbers differ from the Python daily Bitcoin result in Table 4.6 (39 trades, \u22120.43%) for the reason given in Section 3.4.2. On TradingView the KNN model produces predictions only over the most recent 2,000 candles of the chart, so the Strategy Tester covers roughly the last five and a half years, not the full history. For the same reason the figures move as new candles arrive. With 23 trades the result is too small a sample to draw conclusions from. What it does show is that the script compiles, runs and trades on TradingView with the tuned settings, and that every entry can be audited: the chart\u2019s data window shows each of the five role conditions as 1 or 0 on every candle (Appendix I, Figure A.1)."),
  H2("4.8 Discussion"),
  P("Three findings stand out."),
  P("**The process worked even though the strategy did not.** Every trial was logged, the selection rule was fixed in advance, and the critic identified the weaknesses of run 17 (concentration in two trades, a near-zero year, a narrow parameter peak, no margin for higher costs and a Deflated Sharpe Ratio of 0.19) before the out-of-sample data was opened. The out-of-sample loss is what those warnings predicted. Without the locked hold-out we would have reported a profitable strategy with a positive Sharpe ratio and a drawdown of 1.5%, and it would have been wrong."),
  P("**The largest single improvement came from the exits, not from the machine learning model.** Letting trades run for 12 candles with a 3 ATR target took the Sharpe ratio from \u22121.71 to \u22120.67. Changing the KNN model itself (neighbours, horizon, feature count, feature type) gave smaller gains or none. This matches the momentum literature, which finds that trends are worth riding but not easy to time."),
  P("**Costs are the binding constraint at this horizon.** The selected configuration earned an average of 0.06% per trade after base costs, while a round trip cost about 0.15% in commission alone. Every run with a positive Sharpe ratio failed the stress-cost gate. A short-horizon strategy on Bitcoin needs either a larger edge per trade or fewer, longer trades before it can be trusted."),
  P("On the agents themselves: the tuner followed the critic\u2019s demands closely, and twice (runs 7 and 18) it spent a slot checking the neighbourhood of its own best result instead of chasing a new high. The critic\u2019s stance had to be enforced by its brief. Its default position was that the result was overfitted and that it could not praise without numbers. The team\u2019s role was to design these briefs and rules, to check the engine, and to verify the agents\u2019 claims against the result files. For run 17, for example, the critic\u2019s estimate of the profit concentration was later confirmed by a separate diagnostic script."),
];

// ================================================================== CHAPTER 5
const ch5 = [
  H1("5. CONCLUSION AND FUTURE WORK"),
  H2("5.1 Summary of Contributions"),
  P("This project built, tuned and tested an AI-assisted momentum strategy under rules designed to prevent self-deception. Its main contributions are:"),
  ...numbered([
    "A role-based Pine Script v6 strategy that combines five open-source indicators, including a Lorentzian KNN classifier and a causal Nadaraya-Watson kernel regression, with every role condition visible on the chart for auditing.",
    "A Python backtest engine that reproduces the strategy and TradingView\u2019s fill rules, with 88 passing tests including proofs of causality and a cross-check against an independent library, and about 2.4 seconds per 2.5-year hourly backtest.",
    "A multi-agent tuning protocol (tuner without data access, executor, adversarial critic, tracker) with a 25-run budget, pre-registered gates, an integrity-checked log and a one-shot out-of-sample lock.",
    "An honest record of the outcome: tuning improved the in-sample Sharpe ratio from \u22121.71 to 0.36, the critic flagged the result as fragile, and the strategy lost 3.12% on unseen data (Sharpe \u22121.93) while Bitcoin fell 28.0%. Applied to four daily markets without re-tuning, it was profitable only on Reliance Industries (+6.05%).",
  ]),
  H2("5.2 Limitations"),
  ...bullets([
    "The study tuned one market at one timeframe. The out-of-sample period was a single, mostly falling market regime, so it is one test, not a distribution of tests.",
    "Only 19 parameter sets were tried and 63 of the 72 inputs were never changed. A different search could find a better configuration, but it would also face a higher Deflated Sharpe Ratio hurdle.",
    "Fixed 10% position sizing keeps absolute returns small and makes drawdown comparisons with buy-and-hold misleading unless exposure is taken into account (Section 4.5).",
    "Deviation D1 means TradingView\u2019s in-app results and the Python study cover different windows, so the two cannot be compared trade for trade.",
    "The agents\u2019 judgments, although checked against the result files, depend on the quality of their briefs. A different critic brief might have stopped the search earlier or later.",
  ]),
  H2("5.3 Future Work"),
  H3("5.3.1 Quantum-Inspired Parameter Search"),
  P("The parameter space has roughly 10\u00b3\u2074 combinations even at three values per input. The next phase of the project is the \u201cquantum enhanced\u201d part of the title: framing the choice of discrete settings as a combinatorial optimisation problem and testing quantum-inspired solvers, such as simulated bifurcation {goto19} or classical simulations of the Quantum Approximate Optimization Algorithm {farhi14}, as search methods. Any such search must keep the same rules as this study, because a more powerful optimiser overfits faster. Every evaluated configuration has to count towards the Deflated Sharpe Ratio, and a fresh, untouched hold-out period is needed, because the current one has already been used."),
  H3("5.3.2 Walk-Forward and Regime-Aware Evaluation"),
  P("A single hold-out period gives one data point. Walk-forward testing, which re-tunes on a rolling window and tests on the next block, and combinatorial purged cross-validation {lopez18} would give a distribution of out-of-sample results and show whether the strategy fails only in falling markets."),
  H3("5.3.3 Cost-Aware Design"),
  P("Since every positive configuration failed the stress-cost gate, the next designs should target fewer and longer trades, for example on four-hour or daily candles, or use limit orders where fees are lower. Expected cost per trade should become an explicit part of the selection rule."),
  H3("5.3.4 Aligning TradingView and Python"),
  P("Rewriting the Lorentzian search in the Pine script so that it is causal at every bar, as in the Python engine, would remove deviation D1 and allow trade-by-trade comparison between TradingView\u2019s Strategy Tester and the Python results."),
  H3("5.3.5 Paper Trading and Portfolio Extension"),
  P("A forward paper-trading period on live data is the only test that cannot be contaminated by the research process. Running the strategy across a basket of markets with volatility-based position sizing, instead of one market at a fixed 10%, would also show whether the occasional successes, such as Reliance, add up to a useful portfolio."),
  H2("5.4 Societal Relevance"),
  P("The project connects to three of the United Nations Sustainable Development Goals. For SDG 4 (Quality Education), the full research record, including specification, code, tests, every tuning run and every critic verdict, can be re-run and used to teach disciplined, evidence-based investing. For SDG 8 (Decent Work and Economic Growth), the strategy design limits each trade to 10% of capital with an automatic stop-loss, and the study shows retail traders why an attractive backtest is not enough evidence to risk money on. For SDG 9 (Industry, Innovation and Infrastructure), it shows a practical way to use AI agents in financial research without letting them overfit."),
  H2("5.5 Concluding Remarks"),
  P("We set out to build a strategy that would trade only when five indicators agreed, and to tune it with AI agents without fooling ourselves. The first goal was met. The second was met in the sense that matters: the protocol caught the problem. The tuned strategy looked profitable on the data it was tuned on and lost money on data it had not seen, and the adversarial critic had said in advance that this was likely. A positive in-sample result alone would have been easy to report and difficult to believe. What this project offers instead is a framework that makes it hard to overstate a result. The quantum-inspired search planned for the next phase will have to work under the same rules."),
];

// ================================================================== REFERENCES (built after content so citation order is known)
function referencesSection() {
  return [
    H1("REFERENCES"),
    ...citeOrder.map((k, i) => new Paragraph({
      children: [new TextRun({ text: `[${i + 1}]`, font: FONT }), new TextRun({ text: "\t", font: FONT }), ...runs(REFS[k])],
      alignment: AlignmentType.JUSTIFIED,
      tabStops: [{ type: TabStopType.LEFT, position: 600 }],
      indent: { left: 600, hanging: 600 },
      spacing: { after: 120, line: 300 },
    })),
  ];
}

// ================================================================== APPENDICES
const fz = DATA.frozen;
const tuned = new Set(["exitHoldBars", "riskUseTp", "nwSlopeLen", "nwRequirePriceSide", "nwBandwidth", "lcNeighbors", "wtTimingMode", "wtObLevel2", "wtOsLevel2"]);
const keys = Object.keys(fz);
const fmtv = (v) => (typeof v === "number" && v < 0 ? "\u2212" + Math.abs(v) : String(v));
const half = Math.ceil(keys.length / 2);
const fzRows = [];
for (let i = 0; i < half; i++) {
  const a = keys[i], b = keys[i + half];
  const cellK = (k) => (k ? (tuned.has(k) ? `**${k}**` : k) : "");
  const cellV = (k) => (k ? (tuned.has(k) ? `**${fmtv(fz[k])}**` : fmtv(fz[k])) : "");
  fzRows.push([cellK(a), cellV(a), cellK(b), cellV(b)]);
}

const critic19 = fs.readFileSync(path.join(PROJ, "backtest/critic/run_19.md"), "utf8");
const caveatStart = critic19.indexOf("Caveats the write-up MUST carry");
const caveatEnd = critic19.indexOf("---", caveatStart);
const caveatText = critic19.slice(caveatStart, caveatEnd).trim();

const appendices = [
  H1("APPENDIX I: SCREENSHOTS OF WORK DONE"),
  P("Figure A.1 shows the strategy on the BTCUSD one-hour chart with TradingView\u2019s data window open. Each role condition is plotted as a separate value (C1 to C5), so any entry can be checked by eye: at the highlighted long entry all five long conditions equal 1."),
  ...figure(path.join(PROJ, "Final_Review_PPT/tv_data_window.png"), "Figure A.1: TradingView Data Window Showing the Five Role Conditions"),
  P("The project folder is organised as follows."),
  ...code([
    "CIP-Project/",
    "  Combined Role-Based Strategy.pine   Pine v6 strategy, frozen defaults",
    "  5 source indicator .pine files      LC, NW, WT, WWV, SQZ",
    "  .claude/agents/                     builder.md, adversary.md",
    "  backtest/",
    "    SPEC.md, LOOP_PROTOCOL.md         contract, agent role briefs",
    "    data/                             BTCUSDT_1h.csv, meta, fetch",
    "    engine/                           ta, mlext, signals, broker,",
    "                                      metrics, params",
    "    run_backtest.py, log_tools.py     logged CLI, verify, freeze",
    "    tests/                            9 suites, 88 test cases",
    "    configs/run_01..19.json           one parameter set per run",
    "    results/run_01..19/, OOS_FINAL/   metrics, trades, equity",
    "    critic/run_01..19.md              critic verdicts, verbatim",
    "    logs/                             tuning log, leaderboard",
    "    FROZEN_PARAMS.json                selected config and hash",
    "    multimarket/                      daily-market transfer test",
  ]),
  P("[[Insert screenshots of the GitHub repository, and any HackerRank or LeetCode profiles required by the department, here.]]"),
  H1("APPENDIX II: FROZEN PARAMETER SET"),
  P(`The complete configuration frozen after run 19 (run 17, hash ${DATA.frozen_hash}, frozen ${DATA.frozen_utc.replace("T", " ").replace("Z", " UTC")}). Inputs changed by tuning are shown in bold. Eight inputs (sources, the CCI constant, the full-history switch and the WWV true-range mode) were fixed by the specification and are not tunable.`),
  ...table(["Input", "Value", "Input", "Value"], fzRows, [2700, 1813, 2700, 1813], "Table A.1: Frozen Parameter Set (Run 17)", { size: 18, keep: false }),
  H1("APPENDIX III: EXTRACT FROM THE FINAL CRITIC VERDICT"),
  P("The following caveats are quoted verbatim from the adversarial critic\u2019s final verdict (`critic/run_19.md`), written after run 19 and before the out-of-sample test."),
  ...numbered(caveatText.replace(/^Caveats the write-up MUST carry:\s*/, "").split(/\s*\(\d\)\s*/).filter((x) => x.trim()).map((x) => "\u201c" + x.trim() + "\u201d")),
];

function wrap(text, width) {
  const out = [];
  for (const para of text.split(/\n/)) {
    let line = "";
    for (const w of para.split(/\s+/)) {
      if ((line + " " + w).trim().length > width) { out.push(line); line = w; } else line = (line + " " + w).trim();
    }
    out.push(line);
  }
  return out;
}

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

// build body first so citation numbers are assigned in reading order
const bodyChildren = [...ch1, ...ch2, ...ch3, ...ch4, ...ch5];
const refs = referencesSection();
// the first chapter starts on the first page of its section: no page break before it
bodyChildren[0] = H1("1. INTRODUCTION", { noBreak: true });

const doc = new Document({
  creator: "B. Rohith, C. Srinish, K. Chinmai Datha, K. Shreenandh, M. Satvik Kumar",
  title: TITLE,
  description: "CIP project report, Woxsen University",
  features: { updateFields: true },
  styles: {
    default: {
      document: { run: { font: FONT, size: 24 }, paragraph: { spacing: { line: 360, after: 120 } } },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 32, bold: true, color: "000000" }, paragraph: { spacing: { before: 360, after: 240, line: 276 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 28, bold: true, color: "000000" }, paragraph: { spacing: { before: 240, after: 120, line: 276 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 26, bold: true, color: "000000" }, paragraph: { spacing: { before: 200, after: 120, line: 276 }, outlineLevel: 2 } },
      { id: "FrontTitle", name: "FrontTitle", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 32, bold: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 240, after: 360 } } },
      { id: "TableCaption", name: "TableCaption", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 22, italics: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 100, after: 240, line: 240 } } },
      { id: "FigureCaption", name: "FigureCaption", basedOn: "Normal", next: "Normal",
        run: { font: FONT, size: 22, italics: true }, paragraph: { alignment: AlignmentType.CENTER, spacing: { before: 60, after: 240, line: 240 } } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [
    { properties: pageProps({ start: 1, formatType: NumberFormat.LOWER_ROMAN }), children: titlePage },
    { properties: { ...pageProps({ start: 2, formatType: NumberFormat.LOWER_ROMAN }) }, footers: footer(),
      children: [...certificate, ...declaration, ...acknowledgment, ...abstract, ...tocPages] },
    { properties: pageProps({ start: 1, formatType: NumberFormat.DECIMAL }), footers: footer(),
      children: [...bodyChildren, ...refs, ...appendices] },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote", OUT, buf.length, "bytes;", citeOrder.length, "references");
});
