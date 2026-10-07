# Port of jdehorty/MLExtensions/2 (https://www.tradingview.com/script/ia5ozyMF-MLExtensions/).
# This file is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
# Original (c) jdehorty. See LICENSE.
"""Ports of jdehorty/MLExtensions/2 functions used by the strategy (SPEC 3.2)."""
from __future__ import annotations

import math

import numpy as np
from numba import njit

from . import pine_ta as ta


def _f(x):
    return np.ascontiguousarray(np.asarray(x, dtype=np.float64))


@njit(cache=True)
def _normalize_k(src, lo, hi):
    m = src.shape[0]
    out = np.full(m, np.nan)
    hmin = 10e10
    hmax = -10e10
    for t in range(m):
        v = src[t]
        vmin = hmin if np.isnan(v) else v
        vmax = hmax if np.isnan(v) else v
        hmin = min(vmin, hmin)
        hmax = max(vmax, hmax)
        if not np.isnan(v):
            out[t] = lo + (hi - lo) * (v - hmin) / max(hmax - hmin, 10e-10)
    return out


@njit(cache=True)
def _wilder_sum_k(x, n):
    # s := nz(s[1]) - nz(s[1]) / n + x
    m = x.shape[0]
    out = np.empty(m)
    prev = np.nan
    for t in range(m):
        p = 0.0 if np.isnan(prev) else prev
        s = p - p / n + x[t]
        out[t] = s
        prev = s
    return out


@njit(cache=True)
def _klmf_k(src, high, low):
    m = src.shape[0]
    out = np.empty(m)
    v1p = np.nan
    v2p = np.nan
    kp = np.nan
    srcp = np.nan
    for t in range(m):
        v1 = 0.2 * (src[t] - srcp) + 0.8 * (0.0 if np.isnan(v1p) else v1p)
        v2 = 0.1 * (high[t] - low[t]) + 0.8 * (0.0 if np.isnan(v2p) else v2p)
        if v2 == 0.0 or np.isnan(v1) or np.isnan(v2):
            omega = np.nan
        else:
            omega = abs(v1 / v2)
        alpha = (-(omega ** 2) + math.sqrt(omega ** 4 + 16.0 * omega ** 2)) / 8.0
        k = alpha * src[t] + (1.0 - alpha) * (0.0 if np.isnan(kp) else kp)
        out[t] = k
        v1p = v1
        v2p = v2
        kp = k
        srcp = src[t]
    return out


def normalize(src, lo, hi):
    return _normalize_k(_f(src), float(lo), float(hi))


def rescale(src, old_min, old_max, new_min, new_max):
    src = _f(src)
    return new_min + (new_max - new_min) * (src - old_min) / max(old_max - old_min, 10e-10)


def n_rsi(src, n1, n2):
    return rescale(ta.ema(ta.rsi(src, n1), n2), 0.0, 100.0, 0.0, 1.0)


def n_cci(src, n1, n2):
    return normalize(ta.ema(ta.cci(src, n1), n2), 0.0, 1.0)


def n_wt(src, n1=10, n2=11):
    src = _f(src)
    ema1 = ta.ema(src, n1)
    ema2 = ta.ema(np.abs(src - ema1), n1)
    ci = ta.pdiv(src - ema1, 0.015 * ema2)
    wt1 = ta.ema(ci, n2)
    wt2 = ta.sma(wt1, 4)
    return normalize(wt1 - wt2, 0.0, 1.0)


def _adx_unscaled(high, low, close, n):
    h, l, c = _f(high), _f(low), _f(close)
    h1 = ta.nz(ta.shift(h, 1))
    l1 = ta.nz(ta.shift(l, 1))
    c1 = ta.nz(ta.shift(c, 1))
    tr = np.maximum(np.maximum(h - l, np.abs(h - c1)), np.abs(l - c1))
    up = h - h1
    dn = l1 - l
    dmp = np.where(up > dn, np.maximum(up, 0.0), 0.0)
    dmm = np.where(dn > up, np.maximum(dn, 0.0), 0.0)
    tr_s = _wilder_sum_k(tr, float(n))
    dmp_s = _wilder_sum_k(dmp, float(n))
    dmm_s = _wilder_sum_k(dmm, float(n))
    di_p = ta.pdiv(dmp_s, tr_s) * 100.0
    di_m = ta.pdiv(dmm_s, tr_s) * 100.0
    dx = ta.pdiv(np.abs(di_p - di_m), di_p + di_m) * 100.0
    return ta.rma(dx, n)


def n_adx(high, low, close, n1):
    return rescale(_adx_unscaled(high, low, close, n1), 0.0, 100.0, 0.0, 1.0)


def filter_volatility(high, low, close, min_len, max_len, use):
    if not use:
        return np.ones(len(close), dtype=np.bool_)
    recent = ta.atr(high, low, close, min_len)
    hist = ta.atr(high, low, close, max_len)
    with np.errstate(invalid="ignore"):
        return recent > hist


def regime_filter(src, high, low, threshold, use):
    src = _f(src)
    if not use:
        return np.ones(len(src), dtype=np.bool_)
    klmf = _klmf_k(src, _f(high), _f(low))
    slope = np.abs(klmf - ta.shift(klmf, 1))
    e = 1.0 * ta.ema(slope, 200)
    nsd = ta.pdiv(slope - e, e)
    with np.errstate(invalid="ignore"):
        return nsd >= threshold


def filter_adx(high, low, close, length, threshold, use):
    if not use:
        return np.ones(len(close), dtype=np.bool_)
    adx = _adx_unscaled(high, low, close, length)
    with np.errstate(invalid="ignore"):
        return adx > threshold


def series_from(feature, close, high, low, hlc3, param_a, param_b):
    if feature == "RSI":
        return n_rsi(close, param_a, param_b)
    if feature == "WT":
        return n_wt(hlc3, param_a, param_b)
    if feature == "CCI":
        return n_cci(close, param_a, param_b)
    if feature == "ADX":
        return n_adx(high, low, close, param_a)
    raise ValueError(f"unknown feature {feature!r}")
