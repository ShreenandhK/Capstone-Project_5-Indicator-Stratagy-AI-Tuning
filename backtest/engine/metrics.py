"""Pre-registered performance metrics (SPEC Section 5) and gates (SPEC Section 8).

compute_metrics(trades, equity, info, df, window_start, window_end, period="IS", stress=None) -> dict

Resolved definitions (documented so that every run is computed identically):
  * Daily equity = last bar-close equity of each UTC calendar day present in the window.
    Daily simple returns include the first day, measured against the equity at the start of the
    window (= initial capital, the strategy is flat before the window), so T = number of days.
  * Percent quantities carry a `_pct` suffix and are in percent units. max_dd_pct is a POSITIVE
    magnitude (12.5 means a -12.5 % peak-to-trough decline on bar-close equity).
  * Zero denominators (std = 0, no losing trades, ...) give NaN except profit_factor, which is +inf
    when there are winning trades and no losing trades (NaN with no trades at all).
  * Loss = pnl < 0, win = pnl > 0 (net of both commissions).
  * skew / kurtosis are the population (biased) moments; kurtosis is NON-excess (normal = 3).
  * CAGR uses the window's calendar span (first bar open -> last bar close) over 365.25-day years.
  * Buy & hold: 100 % BTC bought at the OPEN of the first window bar, no costs, marked at each close.
  * Sub-period net return = equity at the sub-period's last bar close / equity just before its first
    bar (previous bar close, or initial capital) - 1. Sub-period sharpe uses the daily returns whose
    day falls inside the sub-period; trades are assigned by entry_time.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats as _st

EULER_GAMMA = 0.5772156649

IS_SUBPERIODS = {
    "2023": ("2023-01-01 00:00", "2023-12-31 23:59:59"),
    "2024": ("2024-01-01 00:00", "2024-12-31 23:59:59"),
    "2025H1": ("2025-01-01 00:00", "2025-06-30 23:59:59"),
}
OOS_SUBPERIODS = {
    "2025H2": ("2025-07-01 00:00", "2025-12-31 23:59:59"),
    "2026YTD": ("2026-01-01 00:00", None),   # None -> end of window
}

GATE_RULES = {
    "G1": "trades >= 100",
    "G2": "profit_factor > 1.0",
    "G3": "stress.net_return_pct > 0",
    "G4": ">= 2 of 3 IS sub-periods (2023, 2024, 2025H1) with net_return_pct > 0",
}


def _utc(ts) -> pd.Timestamp:
    ts = pd.Timestamp(ts)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def _f(x) -> float:
    """Plain python float (NaN preserved)."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return math.nan


# ---------------------------------------------------------------------------------------------------
# primitive statistics
# ---------------------------------------------------------------------------------------------------
def daily_equity(equity: pd.Series) -> pd.Series:
    idx = equity.index
    if idx.tz is None:
        idx = idx.tz_localize("UTC")
    e = pd.Series(equity.to_numpy(dtype=float), index=idx.tz_convert("UTC"))
    return e.groupby(e.index.floor("D")).last()


def daily_returns(equity: pd.Series, start_equity: float) -> pd.Series:
    d = daily_equity(equity)
    prev = np.concatenate([[float(start_equity)], d.to_numpy()[:-1]])
    return pd.Series(d.to_numpy() / prev - 1.0, index=d.index, name="ret")


def sharpe(r, periods: float = 365.0) -> float:
    r = np.asarray(r, dtype=float)
    if r.size < 2:
        return math.nan
    sd = r.std(ddof=1)
    if not sd > 0:
        return math.nan
    return float(r.mean() / sd * math.sqrt(periods))


def sortino(r, periods: float = 365.0) -> float:
    r = np.asarray(r, dtype=float)
    if r.size < 1:
        return math.nan
    dd = math.sqrt(float(np.mean(np.minimum(r, 0.0) ** 2)))
    if not dd > 0:
        return math.nan
    return float(r.mean() / dd * math.sqrt(periods))


def max_drawdown(equity: pd.Series):
    """(max_dd_pct as positive magnitude, max_dd_duration_days). Duration = longest time spent below a
    prior equity peak (peak -> recovery to that peak, or -> end of series if never recovered)."""
    v = np.asarray(equity, dtype=float)
    if v.size == 0:
        return math.nan, math.nan
    peak = np.maximum.accumulate(v)
    dd = v / peak - 1.0
    max_dd = float(-dd.min() * 100.0)
    if max_dd <= 0:
        max_dd = 0.0
    is_dt = isinstance(equity.index, pd.DatetimeIndex)
    tns = equity.index.as_unit("ns").asi8 if is_dt else np.arange(v.size, dtype=np.int64)
    at_peak = v >= peak
    below = ~at_peak
    if not below.any():
        return max_dd, 0.0
    i64 = np.iinfo(np.int64)
    last_peak_t = np.maximum.accumulate(np.where(at_peak, tns, i64.min))
    # time of the next bar that regains the peak (recovery), or the final bar if never recovered
    next_peak_t = np.minimum.accumulate(np.where(at_peak, tns, i64.max)[::-1])[::-1]
    end_t = np.where(next_peak_t == i64.max, tns[-1], next_peak_t)
    dur_ns = int(np.where(below, end_t - last_peak_t, 0).max())
    per_day = 86400e9 if is_dt else 1.0
    return max_dd, float(dur_ns / per_day)


def profit_factor(pnl) -> float:
    pnl = np.asarray(pnl, dtype=float)
    if pnl.size == 0:
        return math.nan
    gw = float(pnl[pnl > 0].sum())
    gl = float(-pnl[pnl < 0].sum())
    if gl == 0:
        return math.inf if gw > 0 else math.nan
    return gw / gl


def max_consecutive_losses(pnl) -> int:
    best = cur = 0
    for x in np.asarray(pnl, dtype=float):
        cur = cur + 1 if x < 0 else 0
        best = max(best, cur)
    return int(best)


def moments(r):
    """(skew, non-excess kurtosis) population moments."""
    r = np.asarray(r, dtype=float)
    if r.size < 3 or not r.std() > 0:
        return math.nan, math.nan
    return float(_st.skew(r, bias=True)), float(_st.kurtosis(r, fisher=False, bias=True))


def psr(sr: float, T: int, skew: float, kurt: float, sr_benchmark: float = 0.0) -> float:
    """Probabilistic Sharpe ratio  Phi((SR - SR*)*sqrt(T-1) / sqrt(1 - skew*SR + (kurt-1)/4*SR^2)).
    SR and SR* are per-period (daily) Sharpe ratios; kurt is non-excess."""
    if any(isinstance(x, float) and math.isnan(x) for x in (sr, skew, kurt)) or T is None or T < 2:
        return math.nan
    den = 1.0 - skew * sr + (kurt - 1.0) / 4.0 * sr * sr
    if not den > 0:
        return math.nan
    return float(_st.norm.cdf((sr - sr_benchmark) * math.sqrt(T - 1) / math.sqrt(den)))


def expected_max_sharpe(var_trials: float, n_trials: int) -> float:
    """SR0 = sqrt(V) * ((1-g)*PhiInv(1-1/N) + g*PhiInv(1-1/(N e))). N < 2 -> 0 (no multiple testing)."""
    if n_trials is None or n_trials < 2 or var_trials is None or not np.isfinite(var_trials):
        return 0.0
    g = EULER_GAMMA
    return float(math.sqrt(var_trials) * ((1 - g) * _st.norm.ppf(1 - 1.0 / n_trials)
                                          + g * _st.norm.ppf(1 - 1.0 / (n_trials * math.e))))


def deflated_sharpe(sr_best: float, T: int, skew: float, kurt: float, trial_sharpes, n_trials=None):
    """Bailey & Lopez de Prado (2014) DSR. trial_sharpes = daily (non-annualised) Sharpe of every trial.
    Returns (dsr, sr0, n_trials, var_trials). V uses the finite trial Sharpes (ddof=1)."""
    ts = np.asarray([x for x in trial_sharpes if x is not None], dtype=float)
    N = int(n_trials if n_trials is not None else ts.size)
    fin = ts[np.isfinite(ts)]
    V = float(fin.var(ddof=1)) if fin.size >= 2 else math.nan
    sr0 = expected_max_sharpe(V, N)
    return psr(sr_best, T, skew, kurt, sr_benchmark=sr0), sr0, N, V


# ---------------------------------------------------------------------------------------------------
# trade statistics
# ---------------------------------------------------------------------------------------------------
def trade_stats(trades: pd.DataFrame) -> dict:
    pnl = trades["pnl"].to_numpy(dtype=float) if len(trades) else np.asarray([], dtype=float)
    ret = trades["return_pct"].to_numpy(dtype=float) if len(trades) else np.asarray([], dtype=float)
    n = int(pnl.size)
    wins, losses = pnl > 0, pnl < 0
    out = {
        "trades": n,
        "win_rate_pct": float(wins.mean() * 100.0) if n else math.nan,
        "profit_factor": profit_factor(pnl),
        "gross_profit_usd": float(pnl[wins].sum()),
        "gross_loss_usd": float(-pnl[losses].sum()),
        "net_pnl_usd": float(pnl.sum()),
        "avg_trade_return_pct": float(ret.mean()) if n else math.nan,
        "median_trade_return_pct": float(np.median(ret)) if n else math.nan,
        "avg_win_pct": float(ret[wins].mean()) if wins.any() else math.nan,
        "avg_loss_pct": float(ret[losses].mean()) if losses.any() else math.nan,
        "avg_win_usd": float(pnl[wins].mean()) if wins.any() else math.nan,
        "avg_loss_usd": float(pnl[losses].mean()) if losses.any() else math.nan,
        "expectancy_usd": float(pnl.mean()) if n else math.nan,
        "avg_bars_held": float(trades["bars_held"].mean()) if n else math.nan,
        "max_consecutive_losses": max_consecutive_losses(pnl),
    }
    aw, al = out["avg_win_usd"], out["avg_loss_usd"]
    out["payoff_ratio"] = float(aw / abs(al)) if (np.isfinite(aw) and np.isfinite(al) and al != 0) else math.nan
    if n >= 2 and ret.std(ddof=1) > 0:
        out["trade_tstat"] = float(ret.mean() / ret.std(ddof=1) * math.sqrt(n))
    else:
        out["trade_tstat"] = math.nan
    if n:  # Wilson 95 % interval of the win rate
        z, ph = 1.959963984540054, wins.mean()
        centre = (ph + z * z / (2 * n)) / (1 + z * z / n)
        half = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        out["win_rate_ci95_low_pct"] = float((centre - half) * 100.0)
        out["win_rate_ci95_high_pct"] = float((centre + half) * 100.0)
    else:
        out["win_rate_ci95_low_pct"] = out["win_rate_ci95_high_pct"] = math.nan
    for d in ("long", "short"):
        sub = pnl[(trades["direction"] == d).to_numpy()] if n else pnl
        out[f"{d}_trades"] = int(sub.size)
        out[f"{d}_profit_factor"] = profit_factor(sub)
        out[f"{d}_net_pnl_usd"] = float(sub.sum())
    reasons = ["LC Exit", "SL", "TP", "Reverse", "WindowEnd"]
    counts = trades["exit_reason"].value_counts().to_dict() if n else {}
    out["exit_reasons"] = {r: int(counts.get(r, 0)) for r in reasons}
    return out


# ---------------------------------------------------------------------------------------------------
# equity statistics
# ---------------------------------------------------------------------------------------------------
def equity_stats(equity: pd.Series, start_equity: float, bar_seconds: float = 3600.0) -> dict:
    r = daily_returns(equity, start_equity)
    rv = r.to_numpy()
    final = float(equity.iloc[-1])
    span_days = (equity.index[-1] - equity.index[0]).total_seconds() / 86400.0 + bar_seconds / 86400.0
    growth = final / start_equity
    cagr = (growth ** (365.25 / span_days) - 1.0) * 100.0 if growth > 0 and span_days > 0 else math.nan
    mdd, mdd_dur = max_drawdown(equity)
    sk, ku = moments(rv)
    srd = sharpe(rv, periods=1.0)
    return {
        "start_equity": float(start_equity),
        "final_equity": final,
        "net_return_pct": (growth - 1.0) * 100.0,
        "cagr_pct": float(cagr),
        "ann_vol_pct": float(rv.std(ddof=1) * math.sqrt(365.0) * 100.0) if rv.size >= 2 else math.nan,
        "sharpe": sharpe(rv),
        "sortino": sortino(rv),
        "max_dd_pct": mdd,
        "max_dd_duration_days": mdd_dur,
        "calmar": float(cagr / mdd) if (mdd and mdd > 0 and np.isfinite(cagr)) else math.nan,
        "sharpe_daily": srd,
        "skew": sk,
        "kurtosis": ku,
        "n_days": int(rv.size),
        "psr0": psr(srd, int(rv.size), sk, ku),
    }


def _window_slice(equity: pd.Series, start, end):
    s = _utc(start)
    m = equity.index >= s
    if end is not None:
        m &= equity.index <= _utc(end)
    return m


def subperiod_stats(trades, equity: pd.Series, start_equity: float, period: str) -> dict:
    defs = IS_SUBPERIODS if period.upper() == "IS" else OOS_SUBPERIODS
    r_all = daily_returns(equity, start_equity)
    out = {}
    eq_vals = equity.to_numpy(dtype=float)
    for name, (s, e) in defs.items():
        m = np.asarray(_window_slice(equity, s, e))
        idx = np.flatnonzero(m)
        if idx.size == 0:
            out[name] = {"net_return_pct": math.nan, "sharpe": math.nan, "trades": 0,
                         "profit_factor": math.nan, "bars": 0}
            continue
        before = eq_vals[idx[0] - 1] if idx[0] > 0 else float(start_equity)
        net = (eq_vals[idx[-1]] / before - 1.0) * 100.0
        rm = np.asarray(_window_slice(r_all, s, e))
        if len(trades):
            et = trades["entry_time"]
            tm = (et >= _utc(s)) & ((et <= _utc(e)) if e is not None else True)
            pnl = trades.loc[tm, "pnl"].to_numpy(dtype=float)
        else:
            pnl = np.asarray([], dtype=float)
        out[name] = {
            "net_return_pct": float(net),
            "sharpe": sharpe(r_all.to_numpy()[rm]),
            "trades": int(pnl.size),
            "profit_factor": profit_factor(pnl),
            "bars": int(idx.size),
        }
    return out


def buy_and_hold(df: pd.DataFrame, equity_index: pd.DatetimeIndex, start_equity: float) -> dict:
    from engine.broker import bar_times
    times = bar_times(df)
    pos = times.get_indexer(equity_index)
    if (pos < 0).any():
        raise ValueError("equity index not aligned with df bars")
    o0 = float(df["open"].to_numpy(dtype=float)[pos[0]])
    closes = df["close"].to_numpy(dtype=float)[pos]
    eq = pd.Series(start_equity * closes / o0, index=equity_index)
    es = equity_stats(eq, start_equity)
    return {"net_return_pct": es["net_return_pct"], "sharpe": es["sharpe"], "max_dd_pct": es["max_dd_pct"],
            "sortino": es["sortino"], "cagr_pct": es["cagr_pct"]}, eq


def gates(m: dict) -> dict:
    subs = m.get("subperiods", {})
    pos_subs = sum(1 for k in IS_SUBPERIODS if np.isfinite(subs.get(k, {}).get("net_return_pct", math.nan))
                   and subs[k]["net_return_pct"] > 0)
    stress_net = (m.get("stress") or {}).get("net_return_pct", math.nan)
    pf = m.get("profit_factor", math.nan)
    g = {
        "G1": {"rule": GATE_RULES["G1"], "value": m.get("trades", 0), "pass": bool(m.get("trades", 0) >= 100)},
        "G2": {"rule": GATE_RULES["G2"], "value": pf, "pass": bool(not math.isnan(pf) and pf > 1.0)},
        "G3": {"rule": GATE_RULES["G3"], "value": stress_net,
               "pass": bool(not math.isnan(stress_net) and stress_net > 0)},
        "G4": {"rule": GATE_RULES["G4"], "value": pos_subs, "pass": bool(pos_subs >= 2)},
    }
    return g


# ---------------------------------------------------------------------------------------------------
# main entry
# ---------------------------------------------------------------------------------------------------
def compute_metrics(trades: pd.DataFrame, equity: pd.Series, info: dict, df: pd.DataFrame,
                    window_start, window_end, period: str = "IS", stress=None) -> dict:
    """stress: (trades, equity, info) tuple of the stress-cost simulation (required for IS gates)."""
    period = period.upper()
    if period not in ("IS", "OOS"):
        raise ValueError("period must be 'IS' or 'OOS'")
    start_eq = float(info.get("initial_capital", 10000.0))
    m = {
        "period": period,
        "window_start": str(_utc(window_start)),
        "window_end": str(_utc(window_end)),
        "first_bar_time": str(equity.index[0]),
        "last_bar_time": str(equity.index[-1]),
        "window_bars": int(len(equity)),
    }
    m.update(equity_stats(equity, start_eq))
    m.update(trade_stats(trades))
    m["bars_in_position"] = int(info.get("bars_in_position", 0))
    m["exposure_pct"] = float(info.get("bars_in_position", 0) / len(equity) * 100.0)
    m["subperiods"] = subperiod_stats(trades, equity, start_eq, period)
    m["buy_and_hold"], _ = buy_and_hold(df, equity.index, start_eq)
    if stress is not None:
        st_tr, st_eq, st_info = stress
        ses = equity_stats(st_eq, float(st_info.get("initial_capital", start_eq)))
        m["stress"] = {
            "costs": st_info.get("costs"),
            "net_return_pct": ses["net_return_pct"],
            "sharpe": ses["sharpe"],
            "profit_factor": profit_factor(st_tr["pnl"].to_numpy(dtype=float)) if len(st_tr) else math.nan,
            "trades": int(len(st_tr)),
            "max_dd_pct": ses["max_dd_pct"],
        }
    else:
        m["stress"] = None
    m["costs"] = info.get("costs")
    if period == "IS":
        m["gates"] = gates(m)
        m["eligible"] = bool(all(g["pass"] for g in m["gates"].values()))
    return m


SUMMARY_KEYS = ["sharpe", "sortino", "net_return_pct", "cagr_pct", "max_dd_pct", "max_dd_duration_days", "calmar",
                "trades", "win_rate_pct", "profit_factor", "trade_tstat", "exposure_pct", "psr0", "sharpe_daily",
                "skew", "kurtosis", "n_days"]
