"""Lookahead / repainting proof: signals on a prefix equal signals on the full series over the overlap."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import params as P  # noqa: E402
from engine.signals import compute_signals  # noqa: E402

REQUIRED = ["long_cond", "short_cond", "lc_new_buy", "lc_new_sell", "risk_atr", "regime_gate", "trend_long",
            "trend_short", "entry_long", "entry_short", "timing_long", "timing_short", "confirm_long",
            "confirm_short", "lc_prediction", "lc_signal", "nw_trend", "wt1", "wt2", "wwv_direction", "sqz_val"]


def synthetic_gbm(n, seed=2024, start="2019-01-01"):
    rng = np.random.default_rng(seed)
    # hourly GBM, BTC-like: ~0.7 % hourly vol, regime-varying volatility
    vol = 0.007 * np.exp(0.5 * np.sin(np.arange(n) / 300.0))
    r = rng.normal(0.0, 1.0, n) * vol
    close = 20000.0 * np.exp(np.cumsum(r))
    open_ = np.r_[20000.0, close[:-1]]
    wick = np.abs(rng.normal(0.0, 1.0, (n, 2))) * vol[:, None] * 0.6
    high = np.maximum(open_, close) * (1.0 + wick[:, 0])
    low = np.minimum(open_, close) * (1.0 - wick[:, 1])
    volume = rng.lognormal(mean=7.0, sigma=0.6, size=n) * (1.0 + 50.0 * np.abs(r))
    idx = pd.date_range(start, periods=n, freq="h", tz="UTC")
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=idx)


PARAM_SETS = {
    "defaults": {},
    "rq_released_window": {
        "nwKernelType": "Rational Quadratic", "nwRelWeight": 2.5, "nwRequirePriceSide": True, "nwSlopeLen": 3,
        "sqzRegimeMode": "Released Within Window", "sqzReleaseWindow": 12, "sqzRequireMomExpansion": True,
        "lcMaxBarsBack": 1000, "lcFeatureCount": 3, "lcDistQuantile": 1.0, "lcNeighbors": 12,
        "lcEntryWindow": 5, "wwvMethod": "Traditional", "wwvMethodValue": 150.0, "wwvNormalize": True,
    },
    "notext_volthr_adx": {
        "wtTimingMode": "Not Overextended Only", "wtExtLevelSel": "Level 1", "wwvUseVolThreshold": True,
        "wwvAvgLen": 30, "wwvAvgMult": 0.8, "wwvPriceSource": "Open / Close",
        "lcUseAdxFilter": True, "lcAdxThreshold": 15, "lcAdxLen": 10, "lcSpacing": 3, "lcMaxBarsBack": 800,
        "lcF1String": "ADX", "lcF2String": "CCI", "lcF3String": "WT", "lcF4String": "RSI",
        "nwKernelType": "Epanechnikov", "nwLookback": 120, "sqzRegimeMode": "Not In Squeeze",
        "allowShorts": False,
    },
    "part_of_price": {
        "wwvMethod": "Part of Price", "wwvMethodValue": 400.0, "wwvPriceSource": "High / Low",
        "sqzReplicateQuirk": False, "sqzUseTrueRange": False, "sqzBbLen": 30, "sqzKcLen": 25,
        "nwKernelType": "Cosine", "nwBandwidth": 20, "lcUseRegimeFilter": False, "lcUseVolFilter": False,
        "lcMaxBarsBack": 600, "lcFeatureCount": 2, "lcHorizon": 8, "lcEntryWindow": 0, "riskAtrLen": 30,
        "lcDistQuantile": 0.5,
    },
}

N_FULL = 6000
N_PREFIX = 4500


@pytest.fixture(scope="module")
def frame():
    return synthetic_gbm(N_FULL)


def _assert_same(a: pd.Series, b: pd.Series, name: str):
    av, bv = a.to_numpy(), b.to_numpy()
    assert av.dtype == bv.dtype, name
    if av.dtype.kind == "f":
        same = (av == bv) | (np.isnan(av) & np.isnan(bv))
    else:
        same = av == bv
    if not same.all():
        first = int(np.argmin(same))
        raise AssertionError(f"column {name} differs first at bar {first}: prefix={av[first]!r} full={bv[first]!r}")


@pytest.mark.parametrize("name", list(PARAM_SETS))
def test_prefix_equals_full(frame, name):
    p = P.validate(PARAM_SETS[name])
    full = compute_signals(frame, p)
    pre = compute_signals(frame.iloc[:N_PREFIX], p)
    for col in REQUIRED:
        assert col in full.columns, col
    assert full.index.equals(frame.index)
    assert len(pre) == N_PREFIX
    for col in full.columns:
        _assert_same(pre[col], full[col].iloc[:N_PREFIX], col)
    for col in ["long_cond", "short_cond", "lc_new_buy", "lc_new_sell", "regime_gate", "trend_long",
                "entry_long", "timing_long", "confirm_long"]:
        assert full[col].dtype == bool
    # non-degenerate: the LC actually predicts and components toggle
    assert (full["lc_prediction"] != 0).sum() > 1000
    for col in ["regime_gate", "trend_long", "timing_long", "confirm_long", "lc_new_buy"]:
        assert 0 < full[col].sum() < N_FULL, col


def test_future_bar_perturbation_does_not_change_past(frame):
    p = P.validate({})
    base = compute_signals(frame, p)
    f2 = frame.copy()
    k = 5000
    f2.iloc[k:, f2.columns.get_loc("close")] *= 1.3
    f2.iloc[k:, f2.columns.get_loc("high")] *= 1.35
    f2.iloc[k:, f2.columns.get_loc("volume")] *= 10
    alt = compute_signals(f2, p)
    for col in base.columns:
        _assert_same(alt[col].iloc[:k], base[col].iloc[:k], col)
