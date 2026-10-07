"""numba LC ANN vs a slow literal pure-Python translation of the SPEC 3.3 pseudo-code (DEVIATION D1)."""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.signals import lc_ann_predictions  # noqa: E402


def slow_ann(feat, y, feature_count, M, K, spacing, q):
    n = len(y)
    predictions = []
    distances = []
    prediction = 0.0
    out = []
    for t in range(n):
        last_d = -1.0
        if t >= M:
            for i in range(t - M, t):
                d = 0.0
                for k in range(feature_count):
                    d = d + math.log(1 + abs(feat[t][k] - feat[i][k]))
                if d >= last_d and i % spacing != 0:
                    last_d = d
                    distances.append(d)
                    predictions.append(float(y[i]))
                    if len(predictions) > K:
                        last_d = distances[math.floor(K * q + 0.5)]
                        distances.pop(0)
                        predictions.pop(0)
            prediction = sum(predictions)
        out.append(prediction)
    return np.array(out)


@pytest.fixture(scope="module")
def synth():
    rng = np.random.default_rng(7)
    n = 900
    feat = rng.random((n, 5))
    # smooth-ish features (like normalized oscillators) plus leading NaN warm-up in some columns
    for k in range(5):
        feat[:, k] = np.convolve(feat[:, k], np.ones(5) / 5, mode="same")
    feat[:25, 1] = np.nan
    feat[:40, 3] = np.nan
    feat[410, 2] = np.nan  # isolated na
    feat = np.ascontiguousarray(feat)
    price = 100 + np.cumsum(rng.normal(0, 1, n))
    H = 4
    y = np.zeros(n, dtype=np.int64)
    for t in range(H, n):
        y[t] = -1 if price[t - H] < price[t] else (1 if price[t - H] > price[t] else 0)
    y[::37] = 0
    return feat, y


@pytest.mark.parametrize("spacing,q,K,fc", [
    (4, 0.75, 8, 5),
    (2, 0.5, 8, 5),
    (3, 1.0, 8, 4),
    (7, 0.9, 8, 2),
    (10, 0.6, 8, 3),
    (4, 0.75, 5, 5),
])
def test_ann_matches_slow_reference(synth, spacing, q, K, fc):
    feat, y = synth
    M = 300
    fast = lc_ann_predictions(feat, y, fc, M, K, spacing, q)
    slow = slow_ann(feat.tolist(), y.tolist(), fc, M, K, spacing, q)
    assert np.array_equal(fast, slow)
    assert np.all(fast[:M] == 0.0)
    assert np.any(fast[M:] != 0.0)
