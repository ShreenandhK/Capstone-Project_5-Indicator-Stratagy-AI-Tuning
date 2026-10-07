"""Metric definitions vs hand-computed values (SPEC Sections 5, 7, 8). Synthetic arrays only."""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine import metrics as M  # noqa: E402
from engine.broker import simulate  # noqa: E402

G = 0.5772156649


def test_sharpe_hand():
    r = [0.01, -0.02, 0.03, 0.00]
    # mean = 0.005 ; squared deviations 0.000025+0.000625+0.000625+0.000025 = 0.0013 ; var(ddof=1)=0.0013/3
    assert M.sharpe(r) == pytest.approx(0.005 / math.sqrt(0.0013 / 3) * math.sqrt(365), rel=1e-12)
    assert M.sharpe(r) == pytest.approx(4.5889, abs=1e-4)
    assert M.sharpe(r, periods=1) == pytest.approx(0.24019223, abs=1e-8)
    assert math.isnan(M.sharpe([0.01]))
    assert math.isnan(M.sharpe([0.01, 0.01]))


def test_sortino_hand():
    r = [0.01, -0.02, 0.03, 0.00]
    # downside deviation = sqrt((0 + 0.0004 + 0 + 0) / 4) = 0.01
    assert M.sortino(r) == pytest.approx(0.5 * math.sqrt(365), rel=1e-12)
    assert M.sortino(r) == pytest.approx(9.552486585, abs=1e-8)


def test_max_drawdown_and_duration_hand():
    idx = pd.date_range("2021-03-01", periods=6, freq="h", tz="UTC")
    eq = pd.Series([100.0, 120.0, 90.0, 95.0, 130.0, 117.0], index=idx)
    dd, dur = M.max_drawdown(eq)
    assert dd == pytest.approx(25.0)                  # 120 -> 90
    assert dur == pytest.approx(3 / 24)               # below the 120 peak from 01:00 to 04:00
    eq2 = pd.Series([100.0, 90.0, 80.0, 85.0], index=idx[:4])  # never recovers
    dd2, dur2 = M.max_drawdown(eq2)
    assert dd2 == pytest.approx(20.0) and dur2 == pytest.approx(3 / 24)
    dd3, dur3 = M.max_drawdown(pd.Series([1.0, 2.0, 3.0], index=idx[:3]))
    assert dd3 == 0.0 and dur3 == 0.0


def test_profit_factor_and_streaks():
    assert M.profit_factor([10, -5, 20, -10]) == pytest.approx(2.0)
    assert M.profit_factor([5, 1]) == math.inf
    assert math.isnan(M.profit_factor([]))
    assert M.max_consecutive_losses([1, -1, -2, 3, -1, -1, -1, 2]) == 3


def test_psr_hand():
    # SR=0.1, T=101, normal moments: z = 0.1*10 / sqrt(1 + (3-1)/4*0.01) = 1/sqrt(1.005)
    assert M.psr(0.1, 101, 0.0, 3.0) == pytest.approx(norm.cdf(1 / math.sqrt(1.005)), rel=1e-12)
    assert M.psr(0.1, 101, 0.0, 3.0) == pytest.approx(0.84074, abs=1e-5)
    # skew -1, kurt 5, SR 0.2, T 50: den = 1 + 0.2 + 4/4*0.04 = 1.24 ; z = 0.2*7/sqrt(1.24)
    assert M.psr(0.2, 50, -1.0, 5.0) == pytest.approx(norm.cdf(1.4 / math.sqrt(1.24)), rel=1e-12)


def test_dsr_hand():
    trials = [0.05, 0.10, 0.15]            # var(ddof=1) = (0.0025 + 0 + 0.0025)/2 = 0.0025
    sr0 = 0.05 * ((1 - G) * norm.ppf(1 - 1 / 3) + G * norm.ppf(1 - 1 / (3 * math.e)))
    # PhiInv(2/3) = 0.430727 ; PhiInv(1 - 1/(3e)) = PhiInv(0.877374) = 1.16195
    # SR0 = 0.05 * (0.4227843*0.430727 + 0.5772157*1.16195) = 0.05 * 0.852804
    assert sr0 == pytest.approx(0.04264, abs=1e-5)
    dsr, s0, n, v = M.deflated_sharpe(0.15, 200, 0.0, 3.0, trials)
    assert n == 3 and v == pytest.approx(0.0025) and s0 == pytest.approx(sr0, rel=1e-12)
    z = (0.15 - sr0) * math.sqrt(199) / math.sqrt(1 + 0.5 * 0.15 ** 2)
    assert dsr == pytest.approx(norm.cdf(z), rel=1e-12)
    # a single trial -> no multiple-testing haircut: DSR = PSR(0)
    dsr1, s01, _, _ = M.deflated_sharpe(0.15, 200, 0.0, 3.0, [0.15])
    assert s01 == 0.0 and dsr1 == pytest.approx(M.psr(0.15, 200, 0.0, 3.0))


def test_moments_population_nonexcess():
    r = np.array([1.0, 2.0, 3.0, 10.0])
    m, sd = r.mean(), r.std()
    sk = np.mean((r - m) ** 3) / sd ** 3
    ku = np.mean((r - m) ** 4) / sd ** 4
    s, k = M.moments(r)
    assert s == pytest.approx(sk) and k == pytest.approx(ku)


def test_daily_returns_first_day_vs_start_equity():
    idx = pd.date_range("2021-05-01 00:00", periods=48, freq="h", tz="UTC")
    v = np.full(48, 10000.0)
    v[10:24] = 10100.0
    v[24:] = 9999.0
    r = M.daily_returns(pd.Series(v, index=idx), 10000.0)
    assert len(r) == 2
    assert r.iloc[0] == pytest.approx(0.01)
    assert r.iloc[1] == pytest.approx(9999 / 10100 - 1)


def test_subperiods_boundaries():
    idx = pd.DatetimeIndex(["2023-12-31 22:00", "2023-12-31 23:00", "2024-01-01 00:00", "2024-01-01 01:00"], tz="UTC")
    eq = pd.Series([10000.0, 10100.0, 10200.0, 10302.0], index=idx)
    trades = pd.DataFrame({"entry_time": pd.DatetimeIndex(["2023-12-31 23:00", "2024-01-01 00:00"], tz="UTC"),
                           "pnl": [5.0, -1.0]})
    sp = M.subperiod_stats(trades, eq, 10000.0, "IS")
    assert sp["2023"]["net_return_pct"] == pytest.approx(1.0)
    assert sp["2024"]["net_return_pct"] == pytest.approx(10302 / 10100 * 100 - 100)
    assert sp["2023"]["trades"] == 1 and sp["2024"]["trades"] == 1
    assert sp["2023"]["profit_factor"] == math.inf and sp["2024"]["profit_factor"] == 0.0
    assert math.isnan(sp["2025H1"]["net_return_pct"]) and sp["2025H1"]["trades"] == 0
    assert set(M.subperiod_stats(trades, eq, 10000.0, "OOS")) == {"2025H2", "2026YTD"}


def test_gates():
    base = {"trades": 100, "profit_factor": 1.01, "stress": {"net_return_pct": 0.1},
            "subperiods": {"2023": {"net_return_pct": 1.0}, "2024": {"net_return_pct": -1.0},
                           "2025H1": {"net_return_pct": 0.5}}}
    g = M.gates(base)
    assert all(x["pass"] for x in g.values())
    assert not M.gates({**base, "trades": 99})["G1"]["pass"]
    assert not M.gates({**base, "profit_factor": 1.0})["G2"]["pass"]
    assert not M.gates({**base, "stress": {"net_return_pct": 0.0}})["G3"]["pass"]
    subs = {"2023": {"net_return_pct": 1.0}, "2024": {"net_return_pct": -1.0}, "2025H1": {"net_return_pct": 0.0}}
    assert not M.gates({**base, "subperiods": subs})["G4"]["pass"]


def test_compute_metrics_integration_synthetic():
    rng = np.random.default_rng(3)
    idx = pd.date_range("2023-01-01", "2025-06-30 23:00", freq="h", tz="UTC")
    n = len(idx)
    c = 20000 * np.exp(np.cumsum(rng.normal(0, 0.005, n)))
    o = np.r_[20000.0, c[:-1]]
    df = pd.DataFrame({"open": o, "high": np.maximum(o, c) * 1.001, "low": np.minimum(o, c) * 0.999,
                       "close": c, "volume": 1.0}, index=idx)
    u = rng.random(n)
    sig = pd.DataFrame({"long_cond": u < 0.01, "short_cond": u > 0.99, "lc_new_buy": False, "lc_new_sell": False,
                        "risk_atr": 100.0}, index=idx)
    p = dict(exitMode="LC Fixed Hold", exitHoldBars=4, riskUseSl=True, riskUseTp=False, riskSlMult=2.0, riskTpMult=3.0)
    ws, we = idx[0], idx[-1]
    base = simulate(df, sig, p, ws, we, {"commission_pct": 0.075, "slip_mode": "ticks", "slip_value": 2, "mintick": 0.01})
    stress = simulate(df, sig, p, ws, we, {"commission_pct": 0.10, "slip_mode": "bps", "slip_value": 5})
    m = M.compute_metrics(*base, df, ws, we, period="IS", stress=stress)
    tr, eq, info = base
    assert m["trades"] == len(tr) and m["n_days"] == 912
    assert m["net_return_pct"] == pytest.approx((eq.iloc[-1] / 10000 - 1) * 100)
    assert m["buy_and_hold"]["net_return_pct"] == pytest.approx((c[-1] / o[0] - 1) * 100)
    assert m["stress"]["trades"] == len(stress[0])
    assert m["stress"]["net_return_pct"] < m["net_return_pct"]
    assert sum(m["exit_reasons"].values()) == m["trades"]
    assert m["long_trades"] + m["short_trades"] == m["trades"]
    assert sum(s["trades"] for s in m["subperiods"].values()) == m["trades"]
    # sub-period returns chain to the total
    tot = np.prod([1 + s["net_return_pct"] / 100 for s in m["subperiods"].values()])
    assert (tot - 1) * 100 == pytest.approx(m["net_return_pct"], rel=1e-9)
    assert set(m["gates"]) == {"G1", "G2", "G3", "G4"} and isinstance(m["eligible"], bool)
    assert 0 <= m["psr0"] <= 1
