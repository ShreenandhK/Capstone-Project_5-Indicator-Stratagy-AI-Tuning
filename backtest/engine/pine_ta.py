"""Pine-faithful ta.* functions on float64 numpy arrays (SPEC 3.1).

Conventions
-----------
* na is represented by NaN. Boolean outputs are never na (comparisons with na are False).
* Window functions (sma, stdev, dev, linreg, highest, lowest) return na unless all `n` values of the
  window [t-n+1, t] are non-na (Pine reference implementations `for i = 0 to n-1 ... x[i]`).
* ema / rma follow the Pine reference form with an SMA seed:
      s[t] = na(s[t-1]) ? sma(x, n)[t] : alpha*x[t] + (1-alpha)*s[t-1]
  i.e. seeded with the SMA of the first `n` consecutive non-na values, na before. A mid-series na
  input makes the output na and the series reseeds from the SMA once a clean window is available.
* Division by zero yields na (see `pdiv`).
"""
from __future__ import annotations

import math

import numpy as np
from numba import njit

NaN = np.nan


def _f(x) -> np.ndarray:
    return np.ascontiguousarray(np.asarray(x, dtype=np.float64))


def _b(x) -> np.ndarray:
    return np.ascontiguousarray(np.asarray(x, dtype=np.bool_))


# ---------------------------------------------------------------------------------------------------
# numba kernels
# ---------------------------------------------------------------------------------------------------
@njit(cache=True)
def _sma_k(x, n):
    m = x.shape[0]
    out = np.full(m, np.nan)
    for t in range(n - 1, m):
        s = 0.0
        ok = True
        for i in range(t - n + 1, t + 1):
            v = x[i]
            if np.isnan(v):
                ok = False
                break
            s += v
        if ok:
            out[t] = s / n
    return out


@njit(cache=True)
def _smooth_k(x, n, alpha):
    m = x.shape[0]
    out = np.full(m, np.nan)
    prev = np.nan
    for t in range(m):
        if np.isnan(prev):
            val = np.nan
            if t >= n - 1:
                s = 0.0
                ok = True
                for i in range(t - n + 1, t + 1):
                    v = x[i]
                    if np.isnan(v):
                        ok = False
                        break
                    s += v
                if ok:
                    val = s / n
        else:
            val = alpha * x[t] + (1.0 - alpha) * prev
        out[t] = val
        prev = val
    return out


@njit(cache=True)
def _stdev_dev_k(x, n, mode):
    # mode 0: population stdev, mode 1: mean absolute deviation from the window mean
    m = x.shape[0]
    out = np.full(m, np.nan)
    for t in range(n - 1, m):
        s = 0.0
        ok = True
        for i in range(t - n + 1, t + 1):
            v = x[i]
            if np.isnan(v):
                ok = False
                break
            s += v
        if not ok:
            continue
        mean = s / n
        acc = 0.0
        if mode == 0:
            for i in range(t - n + 1, t + 1):
                d = x[i] - mean
                acc += d * d
            out[t] = math.sqrt(acc / n)
        else:
            for i in range(t - n + 1, t + 1):
                acc += abs(x[i] - mean)
            out[t] = acc / n
    return out


@njit(cache=True)
def _linreg_k(x, n, offset):
    m = x.shape[0]
    out = np.full(m, np.nan)
    xbar = (n - 1) / 2.0
    sxx = 0.0
    for j in range(n):
        sxx += (j - xbar) * (j - xbar)
    for t in range(n - 1, m):
        sy = 0.0
        ok = True
        for i in range(t - n + 1, t + 1):
            v = x[i]
            if np.isnan(v):
                ok = False
                break
            sy += v
        if not ok:
            continue
        ybar = sy / n
        sxy = 0.0
        for j in range(n):
            sxy += (j - xbar) * (x[t - n + 1 + j] - ybar)
        slope = sxy / sxx if sxx != 0.0 else 0.0
        intercept = ybar - slope * xbar
        out[t] = intercept + slope * (n - 1 - offset)
    return out


@njit(cache=True)
def _extreme_k(x, n, is_max):
    m = x.shape[0]
    out = np.full(m, np.nan)
    for t in range(n - 1, m):
        best = x[t]
        ok = not np.isnan(best)
        if ok:
            for i in range(t - n + 1, t):
                v = x[i]
                if np.isnan(v):
                    ok = False
                    break
                if is_max:
                    if v > best:
                        best = v
                else:
                    if v < best:
                        best = v
        if ok:
            out[t] = best
    return out


@njit(cache=True)
def _barssince_k(c):
    m = c.shape[0]
    out = np.full(m, np.nan)
    last = -1
    for t in range(m):
        if c[t]:
            last = t
        if last >= 0:
            out[t] = t - last
    return out


@njit(cache=True)
def _valuewhen_k(c, src, occurrence):
    m = c.shape[0]
    out = np.full(m, np.nan)
    hist = np.empty(occurrence + 1)
    cnt = 0
    for t in range(m):
        if c[t]:
            # shift history: hist[0] is most recent
            for j in range(occurrence, 0, -1):
                hist[j] = hist[j - 1]
            hist[0] = src[t]
            cnt += 1
        if cnt > occurrence:
            out[t] = hist[occurrence]
    return out


# ---------------------------------------------------------------------------------------------------
# public API
# ---------------------------------------------------------------------------------------------------
def pdiv(a, b):
    """Pine-style division: na when the denominator is 0 (or either operand na)."""
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = a / b
    return np.where(b == 0.0, np.nan, r)


def nz(x, repl=0.0):
    x = _f(x)
    return np.where(np.isnan(x), repl, x)


def shift(x, k=1):
    """x[k] (history reference): na for the first k bars."""
    x = _f(x)
    out = np.full(x.shape[0], np.nan)
    if k == 0:
        return x.copy()
    if k < x.shape[0]:
        out[k:] = x[:-k]
    return out


def sma(x, n):
    return _sma_k(_f(x), int(n))


def ema(x, n):
    n = int(n)
    return _smooth_k(_f(x), n, 2.0 / (n + 1))


def rma(x, n):
    n = int(n)
    return _smooth_k(_f(x), n, 1.0 / n)


def stdev(x, n):
    return _stdev_dev_k(_f(x), int(n), 0)


def dev(x, n):
    return _stdev_dev_k(_f(x), int(n), 1)


def change(x, length=1):
    x = _f(x)
    return x - shift(x, length)


def rsi(x, n):
    x = _f(x)
    x1 = shift(x, 1)
    # math.max(na, 0) is na in Pine; np.maximum propagates NaN the same way
    u = np.maximum(x - x1, 0.0)
    d = np.maximum(x1 - x, 0.0)
    up = rma(u, n)
    dn = rma(d, n)
    with np.errstate(divide="ignore", invalid="ignore"):
        res = 100.0 - 100.0 / (1.0 + up / dn)
    res = np.where(dn == 0.0, 100.0, np.where(up == 0.0, 0.0, res))
    res = np.where(np.isnan(up) | np.isnan(dn), np.nan, res)
    return res


def cci(x, n):
    x = _f(x)
    return pdiv(x - sma(x, n), 0.015 * dev(x, n))


def tr(high, low, close, handle_na=False):
    h, l, c = _f(high), _f(low), _f(close)
    c1 = shift(c, 1)
    hl = h - l
    r = np.maximum(np.maximum(hl, np.abs(h - c1)), np.abs(l - c1))
    if handle_na:
        r = np.where(np.isnan(c1), hl, r)
    return r


def atr(high, low, close, n):
    return rma(tr(high, low, close, True), n)


def linreg(x, n, offset=0):
    return _linreg_k(_f(x), int(n), int(offset))


def highest(x, n):
    return _extreme_k(_f(x), int(n), True)


def lowest(x, n):
    return _extreme_k(_f(x), int(n), False)


def crossover(a, b):
    a, b = _f(a), _f(b)
    a1, b1 = shift(a, 1), shift(b, 1)
    with np.errstate(invalid="ignore"):
        return (a > b) & (a1 <= b1)


def crossunder(a, b):
    a, b = _f(a), _f(b)
    a1, b1 = shift(a, 1), shift(b, 1)
    with np.errstate(invalid="ignore"):
        return (a < b) & (a1 >= b1)


def barssince(cond):
    return _barssince_k(_b(cond))


def valuewhen(cond, src, occurrence=0):
    return _valuewhen_k(_b(cond), _f(src), int(occurrence))


def math_round(x):
    """Pine math.round as specified: floor(x + 0.5)."""
    return math.floor(x + 0.5)
