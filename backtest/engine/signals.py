# The Lorentzian Classification sections of this file are ported from jdehorty's "Machine Learning: Lorentzian
# Classification" (https://www.tradingview.com/script/WhBzgfDu-Machine-Learning-Lorentzian-Classification/) and
# remain subject to the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/, (c) jdehorty. The Nadaraya-Watson
# sections are adapted from QuantAlgo's CC BY-NC-SA 4.0 indicator. See LICENSE.
"""compute_signals(df, p): faithful, position-independent port of the CRB strategy signal logic (SPEC 3.3).

All outputs at bar t are pure functions of bars <= t (causal). bar_index = row position in `df`.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from numba import njit

from . import mlext as ml
from . import pine_ta as ta


# ---------------------------------------------------------------------------------------------------
# Nadaraya-Watson (causal endpoint)
# ---------------------------------------------------------------------------------------------------
def nw_kernel_weight(dist: float, h: float, ktype: str, rq: float) -> float:
    """Literal port of nwKernelWeight."""
    w = 0.0
    if h > 0.0:
        u = dist / h
        if ktype == "Gaussian":
            w = math.exp(-(dist * dist) / (2.0 * h * h))
        elif ktype == "Rational Quadratic":
            w = math.pow(1.0 + (dist * dist) / (2.0 * rq * h * h), -rq)
        elif abs(u) <= 1.0:
            if ktype == "Epanechnikov":
                w = 0.75 * (1.0 - u * u)
            elif ktype == "Triangular":
                w = 1.0 - abs(u)
            elif ktype == "Quartic":
                w = (15.0 / 16.0) * math.pow(1.0 - u * u, 2.0)
            elif ktype == "Cosine":
                w = (math.pi / 4.0) * math.cos(math.pi * u / 2.0)
    return w


@njit(cache=True)
def _nw_k(src, w):
    m = src.shape[0]
    L = w.shape[0] - 1
    out = np.full(m, np.nan)
    sum_w = 0.0
    for i in range(L + 1):
        sum_w += w[i]
    if sum_w == 0.0:
        return out
    for t in range(L, m):  # t < L: src[t-i] is na for some i -> nwSumP na -> na
        sp = 0.0
        for i in range(L + 1):
            sp += src[t - i] * w[i]
        out[t] = sp / sum_w
    return out


# ---------------------------------------------------------------------------------------------------
# Lorentzian Classification ANN (DEVIATION D1: causal rolling window)
# ---------------------------------------------------------------------------------------------------
@njit(cache=True)
def lc_ann_predictions(feat, y, feature_count, max_bars_back, neighbors, spacing, quantile):
    """feat: (n, 5) float64 C-contiguous; y: (n,) int64 labels. Returns lc_prediction (n,) float64."""
    n = feat.shape[0]
    M = max_bars_back
    K = neighbors
    out = np.empty(n)
    cap = K + 1
    dist_buf = np.empty(cap)
    pred_buf = np.empty(cap)
    start = 0
    cnt = 0
    qidx = int(math.floor(K * quantile + 0.5))
    prediction = 0.0
    for t in range(n):
        last_d = -1.0
        if t >= M:
            i0 = t - M
            r = i0 % spacing
            for i in range(i0, t):
                if r != 0:
                    d = 0.0
                    for k in range(feature_count):
                        d += math.log(1.0 + abs(feat[t, k] - feat[i, k]))
                    if d >= last_d:  # NaN -> False
                        last_d = d
                        pos = start + cnt
                        if pos >= cap:
                            pos -= cap
                        dist_buf[pos] = d
                        pred_buf[pos] = y[i]
                        cnt += 1
                        if cnt > K:
                            qpos = start + qidx
                            if qpos >= cap:
                                qpos -= cap
                            last_d = dist_buf[qpos]
                            start += 1
                            if start >= cap:
                                start = 0
                            cnt -= 1
                r += 1
                if r == spacing:
                    r = 0
            s = 0.0
            for j in range(cnt):
                pos = start + j
                if pos >= cap:
                    pos -= cap
                s += pred_buf[pos]
            prediction = s
        out[t] = prediction
    return out


@njit(cache=True)
def _lc_state_k(pred, filt, entry_window, allow_l, allow_s, gate, tr_l, tr_s, ti_l, ti_s, co_l, co_s):
    m = pred.shape[0]
    sig = np.zeros(m, dtype=np.int64)
    new_buy = np.zeros(m, dtype=np.bool_)
    new_sell = np.zeros(m, dtype=np.bool_)
    entry_l = np.zeros(m, dtype=np.bool_)
    entry_s = np.zeros(m, dtype=np.bool_)
    long_c = np.zeros(m, dtype=np.bool_)
    short_c = np.zeros(m, dtype=np.bool_)
    prev = 0
    long_flip = -1  # -1 == na
    short_flip = -1
    used_l = -1
    used_s = -1
    for t in range(m):
        if pred[t] > 0 and filt[t]:
            s = 1
        elif pred[t] < 0 and filt[t]:
            s = -1
        else:
            s = prev
        changed = t > 0 and s != prev
        nb = s == 1 and changed
        ns = s == -1 and changed
        if nb:
            long_flip = t
        if ns:
            short_flip = t
        in_wl = long_flip >= 0 and t - long_flip <= entry_window
        in_ws = short_flip >= 0 and t - short_flip <= entry_window
        fresh_l = used_l < 0 or long_flip != used_l
        fresh_s = used_s < 0 or short_flip != used_s
        el = s == 1 and in_wl and fresh_l
        es = s == -1 and in_ws and fresh_s
        lc = allow_l and gate[t] and tr_l[t] and el and ti_l[t] and co_l[t]
        sc = allow_s and gate[t] and tr_s[t] and es and ti_s[t] and co_s[t]
        if lc:
            used_l = long_flip
        if sc:
            used_s = short_flip
        sig[t] = s
        new_buy[t] = nb
        new_sell[t] = ns
        entry_l[t] = el
        entry_s[t] = es
        long_c[t] = lc
        short_c[t] = sc
        prev = s
    return sig, new_buy, new_sell, entry_l, entry_s, long_c, short_c


# ---------------------------------------------------------------------------------------------------
# Weis Wave Volume (recursive series)
# ---------------------------------------------------------------------------------------------------
@njit(cache=True)
def _wwv_k(hi, lo, brick, vol, normalize):
    m = hi.shape[0]
    direction = np.zeros(m, dtype=np.int64)
    res = np.full(m, np.nan)
    cc_prev = np.nan
    dir_prev = 0
    bc_prev = 0
    vol_prev = np.nan
    for t in range(m):
        prev_close = 0.0 if np.isnan(cc_prev) else cc_prev
        prev_high = prev_close + brick[t]
        prev_low = prev_close - brick[t]
        if hi[t] > prev_high:
            cc = hi[t]
        elif lo[t] < prev_low:
            cc = lo[t]
        else:
            cc = prev_close
        if cc > prev_close:
            d = 1
        elif cc < prev_close:
            d = -1
        else:
            d = dir_prev  # nz(direction[1]); 0 on bar 0
        changed = t > 0 and d != dir_prev
        if (not changed) and normalize:
            bc = bc_prev + 1  # nz(barCount[1]) + 1
        else:
            bc = 1
        if not changed:
            v = (0.0 if np.isnan(vol_prev) else vol_prev) + vol[t]
        else:
            v = vol[t]
        r = v / bc if bc > 1 else v
        direction[t] = d
        res[t] = r
        cc_prev = cc
        dir_prev = d
        bc_prev = bc
        vol_prev = v
    return direction, res


# ---------------------------------------------------------------------------------------------------
def _source(name, o, h, l, c):
    if name == "close":
        return c
    if name == "open":
        return o
    if name == "high":
        return h
    if name == "low":
        return l
    if name == "hl2":
        return (h + l) / 2.0
    if name == "hlc3":
        return (h + l + c) / 3.0
    if name == "ohlc4":
        return (o + h + l + c) / 4.0
    raise ValueError(f"unknown source {name!r}")


def _gt(a, b):
    with np.errstate(invalid="ignore"):
        return np.asarray(a > b, dtype=np.bool_)


def _lt(a, b):
    with np.errstate(invalid="ignore"):
        return np.asarray(a < b, dtype=np.bool_)


def compute_signals(df: pd.DataFrame, p: dict) -> pd.DataFrame:
    o = np.ascontiguousarray(df["open"].to_numpy(dtype=np.float64))
    h = np.ascontiguousarray(df["high"].to_numpy(dtype=np.float64))
    l = np.ascontiguousarray(df["low"].to_numpy(dtype=np.float64))
    c = np.ascontiguousarray(df["close"].to_numpy(dtype=np.float64))
    vol = np.ascontiguousarray(df["volume"].to_numpy(dtype=np.float64))
    n = c.shape[0]
    hlc3 = (h + l + c) / 3.0

    # ---------------- TREND | Nadaraya-Watson
    nw_src = _source(p["nwSrc"], o, h, l, c)
    nw_h = p["nwBandwidth"] * p["nwHMult"]
    w = np.array([nw_kernel_weight(float(i), nw_h, p["nwKernelType"], p["nwRelWeight"])
                  for i in range(p["nwLookback"] + 1)], dtype=np.float64)
    nw = _nw_k(np.ascontiguousarray(nw_src), w)
    nw_k = ta.shift(nw, p["nwSlopeLen"])
    nw_valid = ~np.isnan(nw) & ~np.isnan(nw_k)
    nw_up = nw_valid & _gt(nw, nw_k)
    nw_dn = nw_valid & _lt(nw, nw_k)
    req = p["nwRequirePriceSide"]
    trend_long = nw_up & ((not req) | _gt(nw_src, nw))
    trend_short = nw_dn & ((not req) | _lt(nw_src, nw))

    # ---------------- ENTRY | Lorentzian Classification
    lc_src = _source(p["lcSource"], o, h, l, c)
    f_vol = ml.filter_volatility(h, l, c, p["lcVolMinLen"], p["lcVolMaxLen"], p["lcUseVolFilter"])
    f_reg = ml.regime_filter(_source(p["lcRegimeSrc"], o, h, l, c), h, l, p["lcRegimeThreshold"],
                             p["lcUseRegimeFilter"])
    f_adx = ml.filter_adx(h, l, lc_src, p["lcAdxLen"], p["lcAdxThreshold"], p["lcUseAdxFilter"])  # Pine: ml.filter_adx(lcSource, ...)
    f_all = f_vol & f_reg & f_adx

    fc = p["lcFeatureCount"]
    feat = np.full((n, 5), np.nan)
    for k in range(fc):  # features beyond featureCount never enter the distance
        j = k + 1
        feat[:, k] = ml.series_from(p[f"lcF{j}String"], c, h, l, hlc3, p[f"lcF{j}ParamA"], p[f"lcF{j}ParamB"])
    feat = np.ascontiguousarray(feat)

    H = p["lcHorizon"]
    src_h = ta.shift(lc_src, H)
    y = np.where(_lt(src_h, lc_src), -1, np.where(_gt(src_h, lc_src), 1, 0)).astype(np.int64)

    lc_pred = lc_ann_predictions(feat, y, fc, p["lcMaxBarsBack"], p["lcNeighbors"], p["lcSpacing"],
                                 float(p["lcDistQuantile"]))

    # ---------------- TIMING | WaveTrend
    wt_src = _source(p["wtSrc"], o, h, l, c)
    wt_esa = ta.ema(wt_src, p["wtN1"])
    wt_d = ta.ema(np.abs(wt_src - wt_esa), p["wtN1"])
    wt_ci = ta.pdiv(wt_src - wt_esa, p["wtCciConst"] * wt_d)
    wt1 = ta.ema(wt_ci, p["wtN2"])
    wt2 = ta.sma(wt1, p["wtSigLen"])
    wt_cross_up = ta.crossover(wt1, wt2)
    wt_cross_dn = ta.crossunder(wt1, wt2)
    bs_up = ta.barssince(wt_cross_up)
    bs_dn = ta.barssince(wt_cross_dn)
    lvl1 = p["wtExtLevelSel"] == "Level 1"
    ob_cap = float(p["wtObLevel1"] if lvl1 else p["wtObLevel2"])
    os_cap = float(p["wtOsLevel1"] if lvl1 else p["wtOsLevel2"])
    wt_valid = ~np.isnan(wt1)
    long_not_ext = wt_valid & _lt(wt1, ob_cap)
    short_not_ext = wt_valid & _gt(wt1, os_cap)
    win = p["wtCrossWindow"]
    long_recent = ~np.isnan(bs_up) & (np.nan_to_num(bs_up, nan=1e18) <= win) & _gt(wt1, wt2)
    short_recent = ~np.isnan(bs_dn) & (np.nan_to_num(bs_dn, nan=1e18) <= win) & _lt(wt1, wt2)
    use_cross = p["wtTimingMode"] == "Recent Cross + Not Overextended"
    timing_long = long_not_ext & ((not use_cross) | long_recent)
    timing_short = short_not_ext & ((not use_cross) | short_recent)

    # ---------------- CONFIRMATION | Weis Wave Volume
    use_close = p["wwvPriceSource"] == "Close"
    use_oc = p["wwvPriceSource"] == "Open / Close" or use_close
    utr = p["wwvUseTrueRange"]
    tr_var = ta.tr(h, l, c, False)
    if utr == "Always":
        wwv_vol = tr_var
    elif utr == "Auto":
        wwv_vol = np.where(np.isnan(vol), tr_var, vol)
    else:
        wwv_vol = vol
    wwv_op = c if use_close else o
    if use_oc:
        wwv_hi = np.where(c >= wwv_op, c, wwv_op)
        wwv_lo = np.where(c <= wwv_op, c, wwv_op)
    else:
        wwv_hi = h
        wwv_lo = l
    mv = p["wwvMethodValue"]
    if p["wwvMethod"] == "ATR":
        brick = ta.atr(h, l, c, max(1, ta.math_round(mv)))
    elif p["wwvMethod"] == "Part of Price":
        brick = ta.pdiv(c, np.full(n, mv))
    else:
        brick = np.full(n, float(mv))
    wwv_dir, wwv_res = _wwv_k(np.ascontiguousarray(wwv_hi, dtype=np.float64),
                              np.ascontiguousarray(wwv_lo, dtype=np.float64),
                              np.ascontiguousarray(brick, dtype=np.float64),
                              np.ascontiguousarray(wwv_vol, dtype=np.float64),
                              bool(p["wwvNormalize"]))
    wwv_avg = ta.sma(wwv_res, p["wwvAvgLen"])
    if p["wwvUseVolThreshold"]:
        with np.errstate(invalid="ignore"):
            wwv_ok = ~np.isnan(wwv_avg) & (wwv_res >= wwv_avg * p["wwvAvgMult"])
    else:
        wwv_ok = np.ones(n, dtype=np.bool_)
    confirm_long = (wwv_dir > 0) & wwv_ok
    confirm_short = (wwv_dir < 0) & wwv_ok

    # ---------------- REGIME GATE | Squeeze Momentum
    sq_src = _source(p["sqzSrc"], o, h, l, c)
    bb_len, kc_len = p["sqzBbLen"], p["sqzKcLen"]
    basis = ta.sma(sq_src, bb_len)
    sdev = (p["sqzKcMult"] if p["sqzReplicateQuirk"] else p["sqzBbMult"]) * ta.stdev(sq_src, bb_len)
    upper_bb = basis + sdev
    lower_bb = basis - sdev
    ma = ta.sma(sq_src, kc_len)
    rng = tr_var if p["sqzUseTrueRange"] else (h - l)
    range_ma = ta.sma(rng, kc_len)
    upper_kc = ma + range_ma * p["sqzKcMult"]
    lower_kc = ma - range_ma * p["sqzKcMult"]
    sqz_on = _gt(lower_bb, lower_kc) & _lt(upper_bb, upper_kc)
    sqz_off = _lt(lower_bb, lower_kc) & _gt(upper_bb, upper_kc)
    mid = ((ta.highest(h, kc_len) + ta.lowest(l, kc_len)) / 2.0 + ta.sma(sq_src, kc_len)) / 2.0
    sqz_val = ta.linreg(sq_src - mid, kc_len, 0)
    bs_on = ta.barssince(sqz_on)
    fired_recently = ~sqz_on & ~np.isnan(bs_on) & (np.nan_to_num(bs_on, nan=1e18) <= p["sqzReleaseWindow"])
    sqz_val1 = ta.shift(sqz_val, 1)
    mom_expanding = ~np.isnan(sqz_val) & ~np.isnan(sqz_val1) & _gt(np.abs(sqz_val), np.abs(sqz_val1))
    mode = p["sqzRegimeMode"]
    if mode == "Squeeze Off":
        base = sqz_off
    elif mode == "Not In Squeeze":
        base = ~sqz_on
    elif mode == "Released Within Window":
        base = fired_recently
    else:
        base = np.zeros(n, dtype=np.bool_)
    regime_gate = base & ((not p["sqzRequireMomExpansion"]) | mom_expanding)

    # ---------------- LC signal state, entry window, one-trade-per-flip, final conditions
    sig, new_buy, new_sell, entry_long, entry_short, long_cond, short_cond = _lc_state_k(
        lc_pred, np.ascontiguousarray(f_all), int(p["lcEntryWindow"]),
        bool(p["allowLongs"]), bool(p["allowShorts"]),
        np.ascontiguousarray(regime_gate), np.ascontiguousarray(trend_long), np.ascontiguousarray(trend_short),
        np.ascontiguousarray(timing_long), np.ascontiguousarray(timing_short),
        np.ascontiguousarray(confirm_long), np.ascontiguousarray(confirm_short))

    risk_atr = ta.atr(h, l, c, p["riskAtrLen"])

    out = pd.DataFrame({
        "long_cond": long_cond,
        "short_cond": short_cond,
        "lc_new_buy": new_buy,
        "lc_new_sell": new_sell,
        "risk_atr": risk_atr,
        "regime_gate": np.asarray(regime_gate, dtype=bool),
        "trend_long": np.asarray(trend_long, dtype=bool),
        "trend_short": np.asarray(trend_short, dtype=bool),
        "entry_long": entry_long,
        "entry_short": entry_short,
        "timing_long": np.asarray(timing_long, dtype=bool),
        "timing_short": np.asarray(timing_short, dtype=bool),
        "confirm_long": np.asarray(confirm_long, dtype=bool),
        "confirm_short": np.asarray(confirm_short, dtype=bool),
        "lc_prediction": lc_pred,
        "lc_signal": sig,
        "nw_trend": nw,
        "wt1": wt1,
        "wt2": wt2,
        "wwv_direction": wwv_dir,
        "sqz_val": sqz_val,
        # extra audit columns
        "lc_filter_all": np.asarray(f_all, dtype=bool),
        "wwv_res": wwv_res,
        "sqz_on": np.asarray(sqz_on, dtype=bool),
        "sqz_off": np.asarray(sqz_off, dtype=bool),
    }, index=df.index)
    return out
