"""Independent reference for the LC signal state / entry window / one-trade-per-flip logic (_lc_state_k),
transcribed bar-by-bar from the Pine source (lines 267-285 and 418-419, 460-468), plus hand-built
adversarial scenarios and a real-data (DEV window only) check that no mid-series NaN reaches the
EMA/RMA reseed branch after warm-up."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import params as P  # noqa: E402
from engine.signals import _lc_state_k, compute_signals  # noqa: E402


def ref_lc_state(pred, filt, window, allow_l, allow_s, gate, tr_l, tr_s, ti_l, ti_s, co_l, co_s):
    n = len(pred)
    out = {k: [] for k in ("sig", "nb", "ns", "el", "es", "lc", "sc")}
    lc_signal_hist = []          # var int lcSignal
    long_flip = short_flip = None  # ta.valuewhen(..., bar_index, 0)
    used_l = used_s = None         # var int lcUsedLongFlipBar / lcUsedShortFlipBar
    for t in range(n):
        prev = lc_signal_hist[-1] if lc_signal_hist else 0          # nz(lcSignal[1])
        if pred[t] > 0 and filt[t]:
            sig = 1
        elif pred[t] < 0 and filt[t]:
            sig = -1
        else:
            sig = prev
        lc_signal_hist.append(sig)
        change = 0 if t == 0 else sig - lc_signal_hist[-2]          # nz(ta.change(lcSignal))
        changed = change != 0
        new_buy = sig == 1 and changed
        new_sell = sig == -1 and changed
        if new_buy:
            long_flip = t
        if new_sell:
            short_flip = t
        long_in_window = long_flip is not None and t - long_flip <= window
        short_in_window = short_flip is not None and t - short_flip <= window
        long_fresh = used_l is None or long_flip != used_l
        short_fresh = used_s is None or short_flip != used_s
        entry_long = sig == 1 and long_in_window and long_fresh
        entry_short = sig == -1 and short_in_window and short_fresh
        long_cond = bool(allow_l and gate[t] and tr_l[t] and entry_long and ti_l[t] and co_l[t])
        short_cond = bool(allow_s and gate[t] and tr_s[t] and entry_short and ti_s[t] and co_s[t])
        if long_cond:
            used_l = long_flip
        if short_cond:
            used_s = short_flip
        for k, v in (("sig", sig), ("nb", new_buy), ("ns", new_sell), ("el", entry_long),
                     ("es", entry_short), ("lc", long_cond), ("sc", short_cond)):
            out[k].append(v)
    return out


def run_kernel(pred, filt, window, allow_l=True, allow_s=True, gate=None, tr_l=None, tr_s=None,
               ti_l=None, ti_s=None, co_l=None, co_s=None):
    n = len(pred)
    ones = np.ones(n, dtype=np.bool_)
    arrs = [np.ascontiguousarray(a if a is not None else ones, dtype=np.bool_)
            for a in (gate, tr_l, tr_s, ti_l, ti_s, co_l, co_s)]
    return _lc_state_k(np.asarray(pred, dtype=np.float64), np.ascontiguousarray(filt, dtype=np.bool_),
                       int(window), bool(allow_l), bool(allow_s), *arrs)


def test_fuzz_matches_reference():
    rng = np.random.default_rng(7)
    for case in range(3000):
        n = int(rng.integers(5, 60))
        pred = rng.choice([-8.0, -2.0, 0.0, 2.0, 8.0], size=n, p=[0.2, 0.15, 0.3, 0.15, 0.2])
        dens = rng.uniform(0.2, 0.95)
        b = lambda: rng.random(n) < dens  # noqa: E731
        filt, gate, tr_l, tr_s, ti_l, ti_s, co_l, co_s = (b() for _ in range(8))
        window = int(rng.integers(0, 6))
        al, as_ = bool(rng.random() < 0.85), bool(rng.random() < 0.85)
        k = run_kernel(pred, filt, window, al, as_, gate, tr_l, tr_s, ti_l, ti_s, co_l, co_s)
        r = ref_lc_state(pred, filt, window, al, as_, gate, tr_l, tr_s, ti_l, ti_s, co_l, co_s)
        for got, key in zip(k, ("sig", "nb", "ns", "el", "es", "lc", "sc")):
            assert list(np.asarray(got).tolist()) == [int(v) if key == "sig" else bool(v) for v in r[key]], (case, key)


def _pred_from_states(states):
    """states: list of +1 / -1 / 0 per bar -> prediction series (filter always true)."""
    return np.array([8.0 * s for s in states]), np.ones(len(states), dtype=bool)


def test_flip_is_consumed_once():
    pred, filt = _pred_from_states([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    _, nb, _, el, _, lc, _ = run_kernel(pred, filt, window=2)
    assert np.flatnonzero(nb).tolist() == [5]
    assert np.flatnonzero(lc).tolist() == [5]          # conditions true on 5..9, but the flip fires once
    assert np.flatnonzero(el).tolist() == [5]          # entryLong false afterwards (flip used)


def test_window_boundary_inclusive():
    pred, filt = _pred_from_states([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    gate = np.zeros(10, dtype=bool)
    gate[7] = True                                      # 7 - 5 = 2 <= window 2 -> allowed
    lc = run_kernel(pred, filt, window=2, gate=gate)[5]
    assert np.flatnonzero(lc).tolist() == [7]
    gate = np.zeros(10, dtype=bool)
    gate[8] = True                                      # 8 - 5 = 3 > 2 -> blocked
    lc = run_kernel(pred, filt, window=2, gate=gate)[5]
    assert not lc.any()


def test_window_zero_only_flip_bar():
    pred, filt = _pred_from_states([0, 0, 1, 1, 1])
    gate = np.array([True, True, False, True, True])
    lc = run_kernel(pred, filt, window=0, gate=gate)[5]
    assert not lc.any()


def test_reflip_after_opposite_allows_new_entry():
    pred, filt = _pred_from_states([0, 1, 1, 1, -1, -1, 1, 1])
    sig, nb, ns, _, _, lc, sc = run_kernel(pred, filt, window=3)
    assert np.flatnonzero(nb).tolist() == [1, 6]
    assert np.flatnonzero(ns).tolist() == [4]
    assert np.flatnonzero(lc).tolist() == [1, 6]
    assert np.flatnonzero(sc).tolist() == [4]


def test_filter_off_holds_signal_and_creates_no_flip():
    pred = np.array([8.0, 8.0, -8.0, -8.0, 0.0, 8.0])
    filt = np.array([True, True, False, False, True, True])
    sig, nb, ns, *_ = run_kernel(pred, filt, window=2)
    assert sig.tolist() == [1, 1, 1, 1, 1, 1]           # bar 0 flips from 0 but change is nz'd to 0 on bar 0
    assert not nb.any() and not ns.any()


def test_disallowed_side_does_not_consume_flip():
    pred, filt = _pred_from_states([0, 1, 1, 1])
    lc = run_kernel(pred, filt, window=3, allow_l=False)[5]
    assert not lc.any()


# ---------------------------------------------------------------------------------------------------
# Real data, DEV window only (sliced to <= 2022-12-31 23:00 BEFORE computing): after warm-up no
# indicator output is NaN, so the EMA/RMA mid-series-na reseed branch is never exercised on real data.
# ---------------------------------------------------------------------------------------------------
DATA = ROOT / "data" / "BTCUSDT_1h.csv"


@pytest.mark.skipif(not DATA.exists(), reason="data file not present")
@pytest.mark.parametrize("cfg", [{}, {"lcFeatureCount": 5, "lcF1String": "ADX", "lcF2String": "CCI",
                                      "lcF3String": "WT", "lcF4String": "RSI", "lcUseAdxFilter": True}])
def test_no_mid_series_nan_on_dev_data(cfg):
    df = pd.read_csv(DATA)
    df.index = pd.DatetimeIndex(pd.to_datetime(df.pop("time"), utc=True))
    df = df[df.index <= pd.Timestamp("2022-12-31 23:00", tz="UTC")]
    assert df.index.max() < pd.Timestamp("2023-01-01", tz="UTC")
    p = P.validate(cfg)
    sig = compute_signals(df, p)
    after = sig.iloc[2500:]                             # well past every warm-up length used
    for col in ("risk_atr", "nw_trend", "wt1", "wt2", "wwv_res", "sqz_val", "lc_prediction"):
        assert not after[col].isna().any(), col
    from engine import mlext as ml
    h, l, c = (df[k].to_numpy(float) for k in ("high", "low", "close"))
    for j in range(1, p["lcFeatureCount"] + 1):         # lc_prediction defaults to 0, so check features directly
        f = ml.series_from(p[f"lcF{j}String"], c, h, l, (h + l + c) / 3.0, p[f"lcF{j}ParamA"], p[f"lcF{j}ParamB"])
        assert not np.isnan(f[2500:]).any(), f"feature {j}"
