"""pine_ta parity vs slow, independent pure-Python loop references (random walk with leading-NaN segment)."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import pine_ta as ta  # noqa: E402

NA = float("nan")
LEAD = 17
N = 700


def isna(v):
    return v is None or (isinstance(v, float) and math.isnan(v))


@pytest.fixture(scope="module")
def data():
    rng = np.random.default_rng(12345)
    x = 100.0 + np.cumsum(rng.normal(0, 1, N))
    x[:LEAD] = np.nan
    c = 20000.0 * np.exp(np.cumsum(rng.normal(0, 0.01, N)))
    o = np.r_[c[0], c[:-1]]
    h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.003, N)))
    l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.003, N)))
    return x, o, h, l, c


# ----------------------------- references --------------------------------------------------------
def r_hist(x, t, i):
    return x[t - i] if t - i >= 0 else NA


def r_sma(x, n):
    out = []
    for t in range(len(x)):
        vals = [r_hist(x, t, i) for i in range(n)]
        out.append(NA if any(isna(v) for v in vals) else sum(vals) / n)
    return out


def r_smooth(x, n, alpha):
    sm = r_sma(x, n)
    out = []
    prev = NA
    for t in range(len(x)):
        cur = sm[t] if isna(prev) else alpha * x[t] + (1 - alpha) * prev
        out.append(cur)
        prev = cur
    return out


def r_ema(x, n):
    return r_smooth(x, n, 2.0 / (n + 1))


def r_rma(x, n):
    return r_smooth(x, n, 1.0 / n)


def r_stdev(x, n):
    out = []
    for t in range(len(x)):
        vals = [r_hist(x, t, i) for i in range(n)]
        if any(isna(v) for v in vals):
            out.append(NA)
            continue
        m = sum(vals) / n
        out.append(math.sqrt(sum((v - m) ** 2 for v in vals) / n))
    return out


def r_dev(x, n):
    out = []
    for t in range(len(x)):
        vals = [r_hist(x, t, i) for i in range(n)]
        if any(isna(v) for v in vals):
            out.append(NA)
            continue
        m = sum(vals) / n
        out.append(sum(abs(v - m) for v in vals) / n)
    return out


def r_rsi(x, n):
    u, d = [], []
    for t in range(len(x)):
        a, b = x[t], r_hist(x, t, 1)
        if isna(a) or isna(b):
            u.append(NA)
            d.append(NA)
        else:
            u.append(max(a - b, 0.0))
            d.append(max(b - a, 0.0))
    up, dn = r_rma(u, n), r_rma(d, n)
    out = []
    for t in range(len(x)):
        if isna(up[t]) or isna(dn[t]):
            out.append(NA)
        elif dn[t] == 0:
            out.append(100.0)
        elif up[t] == 0:
            out.append(0.0)
        else:
            out.append(100.0 - 100.0 / (1.0 + up[t] / dn[t]))
    return out


def r_cci(x, n):
    s, dv = r_sma(x, n), r_dev(x, n)
    out = []
    for t in range(len(x)):
        if isna(x[t]) or isna(s[t]) or isna(dv[t]) or dv[t] == 0:
            out.append(NA)
        else:
            out.append((x[t] - s[t]) / (0.015 * dv[t]))
    return out


def r_tr(h, l, c, handle_na):
    out = []
    for t in range(len(c)):
        if t == 0:
            out.append(h[t] - l[t] if handle_na else NA)
        else:
            out.append(max(h[t] - l[t], abs(h[t] - c[t - 1]), abs(l[t] - c[t - 1])))
    return out


def r_linreg(x, n):
    out = []
    for t in range(len(x)):
        vals = [r_hist(x, t, n - 1 - j) for j in range(n)]  # x-coord j, current bar j = n-1
        if any(isna(v) for v in vals):
            out.append(NA)
            continue
        xs = list(range(n))
        mx = sum(xs) / n
        my = sum(vals) / n
        slope = sum((a - mx) * (b - my) for a, b in zip(xs, vals)) / sum((a - mx) ** 2 for a in xs)
        out.append(my - slope * mx + slope * (n - 1))
    return out


def r_extreme(x, n, fn):
    out = []
    for t in range(len(x)):
        vals = [r_hist(x, t, i) for i in range(n)]
        out.append(NA if any(isna(v) for v in vals) else fn(vals))
    return out


def r_cross(a, b, over):
    out = []
    for t in range(len(a)):
        a0, b0 = a[t], b[t]
        a1, b1 = r_hist(a, t, 1), r_hist(b, t, 1)
        if any(isna(v) for v in (a0, b0, a1, b1)):
            out.append(False)
        elif over:
            out.append(a0 > b0 and a1 <= b1)
        else:
            out.append(a0 < b0 and a1 >= b1)
    return out


def r_barssince(c):
    out, last = [], None
    for t, v in enumerate(c):
        if v:
            last = t
        out.append(NA if last is None else float(t - last))
    return out


def r_valuewhen(c, src):
    out, last = [], NA
    for t, v in enumerate(c):
        if v:
            last = src[t]
        out.append(last)
    return out


def close(a, b):
    np.testing.assert_allclose(np.asarray(a, float), np.asarray(b, float), rtol=1e-9, atol=1e-9, equal_nan=True)


# ----------------------------- tests --------------------------------------------------------------
@pytest.mark.parametrize("n", [1, 2, 5, 14, 20])
def test_sma_ema_rma(data, n):
    x = data[0]
    close(ta.sma(x, n), r_sma(list(x), n))
    close(ta.ema(x, n), r_ema(list(x), n))
    close(ta.rma(x, n), r_rma(list(x), n))


def test_ema_seed_is_sma_of_first_len_non_na(data):
    x = data[0]
    n = 10
    e = ta.ema(x, n)
    first = LEAD + n - 1
    assert np.all(np.isnan(e[:first]))
    assert e[first] == pytest.approx(np.mean(x[LEAD:LEAD + n]), rel=1e-12)
    r = ta.rma(x, n)
    assert np.all(np.isnan(r[:first])) and r[first] == pytest.approx(np.mean(x[LEAD:LEAD + n]), rel=1e-12)


@pytest.mark.parametrize("n", [2, 7, 20])
def test_stdev_dev_cci(data, n):
    x = data[0]
    close(ta.stdev(x, n), r_stdev(list(x), n))
    close(ta.dev(x, n), r_dev(list(x), n))
    close(ta.cci(x, n), r_cci(list(x), n))


@pytest.mark.parametrize("n", [2, 9, 14])
def test_rsi(data, n):
    x = data[0]
    close(ta.rsi(x, n), r_rsi(list(x), n))


def test_tr_atr(data):
    _, o, h, l, c = data
    close(ta.tr(h, l, c, False), r_tr(h, l, c, False))
    close(ta.tr(h, l, c, True), r_tr(h, l, c, True))
    for n in (1, 10, 14):
        close(ta.atr(h, l, c, n), r_rma(r_tr(h, l, c, True), n))


@pytest.mark.parametrize("n", [2, 5, 20])
def test_linreg_highest_lowest(data, n):
    x = data[0]
    close(ta.linreg(x, n, 0), r_linreg(list(x), n))
    close(ta.highest(x, n), r_extreme(list(x), n, max))
    close(ta.lowest(x, n), r_extreme(list(x), n, min))


def test_cross_barssince_valuewhen_change(data):
    x = data[0]
    a = ta.ema(x, 5)
    b = ta.sma(x, 12)
    co = ta.crossover(a, b)
    cu = ta.crossunder(a, b)
    assert co.tolist() == r_cross(list(a), list(b), True)
    assert cu.tolist() == r_cross(list(a), list(b), False)
    assert co.any() and cu.any()
    close(ta.barssince(co), r_barssince(co.tolist()))
    idx = np.arange(len(x), dtype=float)
    close(ta.valuewhen(co, idx, 0), r_valuewhen(co.tolist(), idx.tolist()))
    ref_change = [NA] + [x[t] - x[t - 1] for t in range(1, len(x))]
    close(ta.change(x), ref_change)
