"""TradingView-faithful broker emulator for the CRB strategy (SPEC Section 4).

simulate(df, sig, p, window_start, window_end, costs) -> (trades_df, equity_series, info)

Semantics reproduced (strategy() header: process_orders_on_close=false, pyramiding=0,
default_qty_type=percent_of_equity 10, commission 0.075 %/side, slippage 2 ticks):

Per bar t, in order:
  1. Open      : market orders queued at close[t-1] fill at open[t] +/- slippage.
                 Entry against an opposite position is ONE fill of |pos| + q (close + open).
                 strategy.close closes the whole position if it still exists. New position entry_bar = t.
  2. Intrabar  : the risk exit (stop / limit) that was active for bar t is checked against the
                 CURRENT position. Path: (high-open) <= (open-low) -> O-H-L-C, else O-L-H-C; the first
                 level touched fills. Gap rule: open already beyond a level -> fill at open.
                 Stop fills get adverse slippage, limit fills none.
  3. Close     : mark-to-market E = cash + pos*close; exit / entry logic of the Pine "EXITS & RISK" and
                 "Orders" blocks; entries only when window_start <= time[t] <= window_end;
                 q = percent_of_equity/100 * E / close[t]; levels fixed at the signal bar;
                 risk order for bar t+1 active iff (inPos or entry queued) and stop level not na.
  4. Last bar of the window (or data): force-close at close[t] (slippage + commission), reason
     'WindowEnd'; queued orders are discarded.

Implementation notes / resolved ambiguities:
  * The loop starts at the first window bar: before it no entry is possible, so the position is
    flat, no order is queued and all levels are na (identical to simulating from bar 0).
  * The equity value recorded at the final bar is the equity AFTER the WindowEnd force close
    (= realised cash), so net return equals the sum of trade pnl including exit costs. All other
    bars carry the mark-to-market close equity.
  * bars_held = exit_bar - entry_bar (TradingView "# bars" convention): a 4-bar fixed hold that
    enters at open of bar e and exits at open of e+4 has bars_held = 4.
  * Quantities are not rounded (SPEC: q = 0.10 * E / close).
  * long_cond and short_cond true on the same bar is impossible by construction of the LC state
    (sig == 1 vs sig == -1) and is rejected with ValueError instead of guessing TV's order of fills.
"""
from __future__ import annotations

import math
import time as _time

import numpy as np
import pandas as pd

BASE_COSTS = {"commission_pct": 0.075, "slip_mode": "ticks", "slip_value": 2, "mintick": 0.01}
STRESS_COSTS = {"commission_pct": 0.10, "slip_mode": "bps", "slip_value": 5}

INITIAL_CAPITAL = 10000.0
PERCENT_OF_EQUITY = 10.0

EXIT_MODES = {"LC Signal Flip": 0, "LC Fixed Hold": 1, "Either (LC Default)": 2}

TRADE_COLUMNS = [
    "direction", "entry_time", "entry_price", "exit_time", "exit_price", "qty", "pnl", "return_pct",
    "bars_held", "exit_reason", "entry_bar", "exit_bar", "entry_commission", "exit_commission",
]

# pending market order codes
_NONE, _ENTRY_LONG, _ENTRY_SHORT, _CLOSE_LONG, _CLOSE_SHORT = 0, 1, 2, 3, 4


def bar_times(df: pd.DataFrame) -> pd.DatetimeIndex:
    """Bar OPEN times as a tz-aware UTC DatetimeIndex (from a 'time' column or the index)."""
    if "time" in df.columns:
        t = pd.DatetimeIndex(pd.to_datetime(df["time"], utc=True))
    elif isinstance(df.index, pd.DatetimeIndex):
        t = df.index
    else:
        raise ValueError("df needs a 'time' column or a DatetimeIndex")
    if t.tz is None:
        t = t.tz_localize("UTC")
    else:
        t = t.tz_convert("UTC")
    return t


def to_utc(ts) -> pd.Timestamp:
    ts = pd.Timestamp(ts)
    return ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")


def _bool_col(sig: pd.DataFrame, name: str) -> list:
    if name not in sig.columns:
        raise ValueError(f"signals missing required column {name!r}")
    s = sig[name]
    if s.dtype != bool:
        s = s.astype("boolean").fillna(False).astype(bool)
    return s.to_numpy(dtype=bool).tolist()


def _slippage(costs: dict):
    """Return (rel, abs) so that buy fill = px*(1+rel)+abs, sell fill = px*(1-rel)-abs."""
    mode = costs.get("slip_mode", "ticks")
    val = float(costs.get("slip_value", 0.0))
    if mode == "ticks":
        return 0.0, val * float(costs.get("mintick", 0.01))
    if mode == "bps":
        return val / 1e4, 0.0
    raise ValueError(f"unknown slip_mode {mode!r}")


def simulate(df: pd.DataFrame, sig: pd.DataFrame, p: dict, window_start, window_end, costs: dict):
    t_start = _time.perf_counter()
    n = len(df)
    if len(sig) != n:
        raise ValueError(f"signals length {len(sig)} != data length {n}")
    times = bar_times(df)
    if n > 1 and not times.is_monotonic_increasing:
        raise ValueError("bar times must be increasing")
    ws, we = to_utc(window_start), to_utc(window_end)
    in_win = np.asarray((times >= ws) & (times <= we), dtype=bool)
    widx = np.flatnonzero(in_win)
    if widx.size == 0:
        raise ValueError(f"no bars inside window [{ws}, {we}]")
    first_w, last_w = int(widx[0]), int(widx[-1])

    # ---- parameters
    try:
        exit_mode = EXIT_MODES[p["exitMode"]]
    except KeyError as e:
        raise ValueError(f"invalid exitMode {p.get('exitMode')!r}") from e
    hold = int(p["exitHoldBars"])
    use_sl, use_tp = bool(p["riskUseSl"]), bool(p["riskUseTp"])
    use_risk = use_sl or use_tp
    sl_mult, tp_mult = float(p["riskSlMult"]), float(p["riskTpMult"])
    capital = float(p.get("initial_capital", INITIAL_CAPITAL))
    pct = float(p.get("percent_of_equity", PERCENT_OF_EQUITY)) / 100.0
    comm = float(costs["commission_pct"]) / 100.0
    rel, sab = _slippage(costs)

    # ---- arrays as python lists (fast scalar access)
    o_ = df["open"].to_numpy(dtype=float).tolist()
    h_ = df["high"].to_numpy(dtype=float).tolist()
    l_ = df["low"].to_numpy(dtype=float).tolist()
    c_ = df["close"].to_numpy(dtype=float).tolist()
    lc_ = _bool_col(sig, "long_cond")
    sc_ = _bool_col(sig, "short_cond")
    nb_ = _bool_col(sig, "lc_new_buy")
    ns_ = _bool_col(sig, "lc_new_sell")
    if "risk_atr" not in sig.columns:
        raise ValueError("signals missing required column 'risk_atr'")
    atr_ = sig["risk_atr"].to_numpy(dtype=float).tolist()
    both = np.flatnonzero(np.asarray(lc_[first_w:last_w + 1]) & np.asarray(sc_[first_w:last_w + 1]))
    if both.size:
        raise ValueError(f"long_cond and short_cond both true at bar {first_w + int(both[0])}")

    nan = math.nan
    isnan = math.isnan

    # ---- state
    cash = capital
    pos = 0.0
    entry_bar = -1
    entry_px = nan
    entry_comm = 0.0
    long_stop = long_tp = short_stop = short_tp = nan
    long_risk = short_risk = False          # active for the current bar
    pend, pend_q = _NONE, 0.0

    tr_dir, tr_eb, tr_xb, tr_ep, tr_xp, tr_q, tr_pnl, tr_ec, tr_xc, tr_reason = ([] for _ in range(10))

    n_win = last_w - first_w + 1
    equity = np.empty(n_win, dtype=float)
    in_pos = np.zeros(n_win, dtype=bool)

    def close_position(px, t, reason):
        nonlocal cash, pos, entry_bar, entry_px, entry_comm
        qty = abs(pos)
        xc = comm * px * qty
        if pos > 0:
            cash += qty * px - xc
            pnl = (px - entry_px) * qty - entry_comm - xc
            tr_dir.append("long")
        else:
            cash -= qty * px + xc
            pnl = (entry_px - px) * qty - entry_comm - xc
            tr_dir.append("short")
        tr_eb.append(entry_bar); tr_xb.append(t); tr_ep.append(entry_px); tr_xp.append(px)
        tr_q.append(qty); tr_pnl.append(pnl); tr_ec.append(entry_comm); tr_xc.append(xc); tr_reason.append(reason)
        pos = 0.0
        entry_bar = -1
        entry_px = nan
        entry_comm = 0.0

    def open_position(px, qty, direction, t):
        nonlocal cash, pos, entry_bar, entry_px, entry_comm
        ec = comm * px * qty
        if direction > 0:
            cash -= qty * px + ec
            pos = qty
        else:
            cash += qty * px - ec
            pos = -qty
        entry_bar = t
        entry_px = px
        entry_comm = ec

    for t in range(first_w, last_w + 1):
        o, h, l, c = o_[t], h_[t], l_[t], c_[t]

        # ---------------- 1. open: market orders
        if pend != _NONE:
            if pend == _ENTRY_LONG:
                px = o * (1.0 + rel) + sab
                if pos < 0:
                    close_position(px, t, "Reverse")
                if pos == 0:
                    open_position(px, pend_q, 1, t)
            elif pend == _ENTRY_SHORT:
                px = o * (1.0 - rel) - sab
                if pos > 0:
                    close_position(px, t, "Reverse")
                if pos == 0:
                    open_position(px, pend_q, -1, t)
            elif pend == _CLOSE_LONG:
                if pos > 0:
                    close_position(o * (1.0 - rel) - sab, t, "LC Exit")
            elif pend == _CLOSE_SHORT:
                if pos < 0:
                    close_position(o * (1.0 + rel) + sab, t, "LC Exit")
            pend, pend_q = _NONE, 0.0

        # ---------------- 2. intrabar: risk exit order
        if pos > 0 and long_risk:
            S = long_stop if use_sl else nan
            L = long_tp if use_tp else nan
            has_s, has_l = not isnan(S), not isnan(L)
            if has_s and o <= S:
                close_position(o * (1.0 - rel) - sab, t, "SL")
            elif has_l and o >= L:
                close_position(o, t, "TP")
            else:
                s_hit = has_s and l <= S
                l_hit = has_l and h >= L
                if s_hit and l_hit:
                    if (h - o) <= (o - l):      # O-H-L-C: the high (limit) is reached first
                        close_position(L, t, "TP")
                    else:                        # O-L-H-C: the low (stop) is reached first
                        close_position(S * (1.0 - rel) - sab, t, "SL")
                elif s_hit:
                    close_position(S * (1.0 - rel) - sab, t, "SL")
                elif l_hit:
                    close_position(L, t, "TP")
        elif pos < 0 and short_risk:
            S = short_stop if use_sl else nan
            L = short_tp if use_tp else nan
            has_s, has_l = not isnan(S), not isnan(L)
            if has_s and o >= S:
                close_position(o * (1.0 + rel) + sab, t, "SL")
            elif has_l and o <= L:
                close_position(o, t, "TP")
            else:
                s_hit = has_s and h >= S
                l_hit = has_l and l <= L
                if s_hit and l_hit:
                    if (h - o) <= (o - l):      # O-H-L-C: the high (stop) is reached first
                        close_position(S * (1.0 + rel) + sab, t, "SL")
                    else:                        # O-L-H-C: the low (limit) is reached first
                        close_position(L, t, "TP")
                elif s_hit:
                    close_position(S * (1.0 + rel) + sab, t, "SL")
                elif l_hit:
                    close_position(L, t, "TP")

        # ---------------- 3. close: strategy logic
        E = cash + pos * c
        k = t - first_w
        in_long, in_short = pos > 0, pos < 0
        in_pos[k] = pos != 0
        bars_from = (t - entry_bar + 1) if pos != 0 else 0
        hold_exp = bars_from >= hold
        lc, sc = lc_[t], sc_[t]
        if exit_mode == 0:
            xl_raw, xs_raw = ns_[t], nb_[t]
        elif exit_mode == 1:
            xl_raw = xs_raw = hold_exp
        else:
            xl_raw, xs_raw = ns_[t] or hold_exp, nb_[t] or hold_exp
        long_exit = in_long and xl_raw and not sc
        short_exit = in_short and xs_raw and not lc

        long_q = short_q = False
        atr = atr_[t]
        if in_win[t] and not isnan(atr):
            if lc and not in_long:
                long_stop = c - atr * sl_mult
                long_tp = c + atr * tp_mult
                pend, pend_q = _ENTRY_LONG, pct * E / c
                long_q = True
            if sc and not in_short:
                short_stop = c + atr * sl_mult
                short_tp = c - atr * tp_mult
                pend, pend_q = _ENTRY_SHORT, pct * E / c
                short_q = True
        if long_exit:
            pend, pend_q = _CLOSE_LONG, 0.0
        if short_exit:
            pend, pend_q = _CLOSE_SHORT, 0.0
        if (long_q + short_q + long_exit + short_exit) > 1:   # impossible by construction
            raise AssertionError(f"conflicting orders at bar {t}")

        if use_risk:
            long_risk = (in_long or long_q) and not isnan(long_stop)
            short_risk = (in_short or short_q) and not isnan(short_stop)
        else:
            long_risk = short_risk = False

        # ---------------- 4. window end
        if t == last_w:
            if pos > 0:
                close_position(c * (1.0 - rel) - sab, t, "WindowEnd")
            elif pos < 0:
                close_position(c * (1.0 + rel) + sab, t, "WindowEnd")
            pend, pend_q = _NONE, 0.0
            E = cash
        equity[k] = E

    # ---- outputs
    tarr = times
    eb = np.asarray(tr_eb, dtype=np.int64)
    xb = np.asarray(tr_xb, dtype=np.int64)
    ep = np.asarray(tr_ep, dtype=float)
    qty = np.asarray(tr_q, dtype=float)
    pnl = np.asarray(tr_pnl, dtype=float)
    trades = pd.DataFrame({
        "direction": pd.Series(tr_dir, dtype=object),
        "entry_time": tarr[eb] if len(eb) else pd.DatetimeIndex([], tz="UTC"),
        "entry_price": ep,
        "exit_time": tarr[xb] if len(xb) else pd.DatetimeIndex([], tz="UTC"),
        "exit_price": np.asarray(tr_xp, dtype=float),
        "qty": qty,
        "pnl": pnl,
        "return_pct": pnl / (ep * qty) * 100.0 if len(eb) else np.asarray([], dtype=float),
        "bars_held": xb - eb,
        "exit_reason": pd.Series(tr_reason, dtype=object),
        "entry_bar": eb,
        "exit_bar": xb,
        "entry_commission": np.asarray(tr_ec, dtype=float),
        "exit_commission": np.asarray(tr_xc, dtype=float),
    }, columns=TRADE_COLUMNS)

    eq = pd.Series(equity, index=tarr[first_w:last_w + 1], name="equity")
    info = {
        "initial_capital": capital,
        "final_equity": float(equity[-1]),
        "first_bar": int(first_w),
        "last_bar": int(last_w),
        "window_bars": int(n_win),
        "bars_in_position": int(in_pos.sum()),
        "exposure_pct": float(in_pos.sum() / n_win * 100.0),
        "in_position": pd.Series(in_pos, index=eq.index, name="in_position"),
        "costs": dict(costs),
        "runtime_s": _time.perf_counter() - t_start,
    }
    return trades, eq, info
