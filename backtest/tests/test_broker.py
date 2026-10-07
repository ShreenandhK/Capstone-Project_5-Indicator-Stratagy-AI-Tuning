"""Hand-computed broker scenarios (SPEC Section 4). All data synthetic."""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.broker import simulate  # noqa: E402

T0 = pd.Timestamp("2021-01-04 00:00", tz="UTC")   # synthetic calendar
ZERO = {"commission_pct": 0.0, "slip_mode": "ticks", "slip_value": 0, "mintick": 0.01}
TICKS2 = {"commission_pct": 0.0, "slip_mode": "ticks", "slip_value": 2, "mintick": 0.01}
BASE = {"commission_pct": 0.075, "slip_mode": "ticks", "slip_value": 2, "mintick": 0.01}


def P(**kw):
    p = dict(exitMode="LC Fixed Hold", exitHoldBars=96, riskUseSl=False, riskUseTp=False,
             riskSlMult=2.0, riskTpMult=3.0)
    p.update(kw)
    return p


def make(rows, long=(), short=(), nb=(), ns=(), atr=1.0):
    n = len(rows)
    a = np.asarray(rows, dtype=float)
    idx = pd.date_range(T0, periods=n, freq="h")
    df = pd.DataFrame({"open": a[:, 0], "high": a[:, 1], "low": a[:, 2], "close": a[:, 3],
                       "volume": np.ones(n)}, index=idx)
    df.index.name = "time"
    sig = pd.DataFrame(index=idx)
    for name, bars in (("long_cond", long), ("short_cond", short), ("lc_new_buy", nb), ("lc_new_sell", ns)):
        col = np.zeros(n, dtype=bool)
        col[list(bars)] = True
        sig[name] = col
    sig["risk_atr"] = atr if np.ndim(atr) else np.full(n, float(atr))
    return df, sig


def run(df, sig, p, costs=ZERO, ws=None, we=None):
    ws = df.index[0] if ws is None else ws
    we = df.index[-1] if we is None else we
    return simulate(df, sig, p, ws, we, costs)


FLAT = (100, 100.5, 99.5, 100)


def test_market_entry_next_open_with_slippage_and_commission():
    rows = [(100, 101, 99, 100), (102, 103.5, 101.5, 103), (103, 104.5, 102.5, 104)]
    df, sig = make(rows, long=[0])
    tr, eq, info = run(df, sig, P(), costs=BASE)
    assert len(tr) == 1
    t = tr.iloc[0]
    q = 0.10 * 10000 / 100.0                    # 10 units, sized at the signal-bar close
    entry = 102 + 0.02                          # open + 2 ticks
    ecomm = 0.00075 * entry * q
    assert t.entry_bar == 1 and t.qty == pytest.approx(q)
    assert t.entry_price == pytest.approx(entry, abs=1e-12)
    assert t.entry_commission == pytest.approx(ecomm, rel=1e-12)
    # mark-to-market at bar 1 close
    assert eq.iloc[1] == pytest.approx(10000 - entry * q - ecomm + q * 103, rel=1e-12)
    # window-end force close at bar 2 close - 2 ticks
    exitp = 104 - 0.02
    xcomm = 0.00075 * exitp * q
    assert t.exit_reason == "WindowEnd" and t.exit_price == pytest.approx(exitp, abs=1e-12)
    pnl = (exitp - entry) * q - ecomm - xcomm
    assert t.pnl == pytest.approx(pnl, rel=1e-12)
    assert t.return_pct == pytest.approx(pnl / (entry * q) * 100, rel=1e-12)
    assert eq.iloc[-1] == pytest.approx(10000 + pnl, rel=1e-12)
    assert info["final_equity"] == pytest.approx(10000 + pnl, rel=1e-12)
    assert eq.iloc[0] == 10000.0


def test_hold_expiry_closes_at_open_of_entry_bar_plus_hold():
    rows = [FLAT] * 3 + [(100, 101, 99, 100.5)] * 2 + [(107, 108, 106, 107)] + [FLAT] * 2
    df, sig = make(rows, long=[0])
    tr, eq, info = run(df, sig, P(exitHoldBars=4))
    assert len(tr) == 1
    t = tr.iloc[0]
    assert t.entry_bar == 1
    assert t.exit_bar == 5 and t.exit_price == 107.0 and t.exit_reason == "LC Exit"
    assert t.bars_held == 4
    assert info["bars_in_position"] == 4        # bars 1..4 held at the close


def test_intrabar_stop_fill_with_slippage():
    rows = [FLAT, (100, 100.5, 99.5, 100), (99.5, 99.8, 97.0, 97.5), FLAT]
    df, sig = make(rows, long=[0], atr=1.0)
    tr, _, _ = run(df, sig, P(riskUseSl=True), costs=TICKS2)
    t = tr.iloc[0]
    assert t.entry_price == pytest.approx(100.02)
    assert t.exit_reason == "SL" and t.exit_bar == 2
    assert t.exit_price == pytest.approx(98.0 - 0.02)       # stop 100 - 2*1, adverse slippage


def test_gap_through_stop_fills_at_open():
    rows = [FLAT, (100, 100.5, 99.5, 100), (97.0, 97.4, 96.0, 96.5), FLAT]
    df, sig = make(rows, long=[0], atr=1.0)
    tr, _, _ = run(df, sig, P(riskUseSl=True), costs=TICKS2)
    t = tr.iloc[0]
    assert t.exit_reason == "SL" and t.exit_bar == 2
    assert t.exit_price == pytest.approx(97.0 - 0.02)        # open (below stop 98) - slippage


def test_gap_through_limit_fills_at_open_without_slippage():
    rows = [FLAT, (100, 100.5, 99.5, 100), (105.0, 106.0, 104.0, 105.5), FLAT]
    df, sig = make(rows, long=[0], atr=1.0)
    tr, _, _ = run(df, sig, P(riskUseSl=True, riskUseTp=True), costs=TICKS2)
    t = tr.iloc[0]
    assert t.exit_reason == "TP" and t.exit_price == 105.0   # TP 103 gapped, limit: no slippage


@pytest.mark.parametrize("bar,reason,price", [
    ((100, 103.5, 97.5, 100), "SL", 98.0),    # h-o=3.5 > o-l=2.5 -> O-L-H-C: stop first
    ((100, 103.1, 96.5, 100), "TP", 103.0),   # h-o=3.1 <= o-l=3.5 -> O-H-L-C: limit first
    ((100, 103.0, 97.0, 100), "TP", 103.0),   # tie (3 <= 3) -> O-H-L-C
])
def test_long_sl_and_tp_same_bar_path_rule(bar, reason, price):
    rows = [FLAT, FLAT, bar, FLAT]
    df, sig = make(rows, long=[0], atr=1.0)     # stop 98, tp 103
    tr, _, _ = run(df, sig, P(riskUseSl=True, riskUseTp=True))
    t = tr.iloc[0]
    assert t.exit_reason == reason and t.exit_bar == 2 and t.exit_price == pytest.approx(price)


@pytest.mark.parametrize("bar,reason,price", [
    ((100, 102.5, 96.0, 100), "SL", 102.0),   # 2.5 <= 4 -> O-H-L-C: high (stop) first
    ((100, 104.0, 96.5, 100), "TP", 97.0),    # 4 > 3.5 -> O-L-H-C: low (limit) first
])
def test_short_sl_and_tp_same_bar_path_rule(bar, reason, price):
    rows = [FLAT, FLAT, bar, FLAT]
    df, sig = make(rows, short=[0], atr=1.0)    # stop 102, tp 97
    tr, _, _ = run(df, sig, P(riskUseSl=True, riskUseTp=True))
    t = tr.iloc[0]
    assert t.direction == "short"
    assert t.exit_reason == reason and t.exit_bar == 2 and t.exit_price == pytest.approx(price)


def test_stop_active_on_entry_bar():
    rows = [FLAT, (100, 100.5, 97.0, 99.0), FLAT, FLAT]
    df, sig = make(rows, long=[0], atr=1.0)
    tr, _, _ = run(df, sig, P(riskUseSl=True))
    t = tr.iloc[0]
    assert t.entry_bar == 1 and t.exit_bar == 1 and t.bars_held == 0
    assert t.exit_reason == "SL" and t.exit_price == 98.0


def test_stop_levels_fixed_at_signal_bar():
    # ATR changes after the signal bar must not move the stop.
    rows = [FLAT, FLAT, (100, 100.2, 96.5, 97.0), FLAT]
    atr = np.array([1.0, 5.0, 5.0, 5.0])
    df, sig = make(rows, long=[0], atr=atr)
    tr, _, _ = run(df, sig, P(riskUseSl=True))
    assert tr.iloc[0].exit_reason == "SL" and tr.iloc[0].exit_price == 98.0 and tr.iloc[0].exit_bar == 2


def test_reversal_long_to_short_qty_abs_pos_plus_q_and_hold_restarts():
    costs = {"commission_pct": 0.1, "slip_mode": "ticks", "slip_value": 0, "mintick": 0.01}
    rows = [FLAT, (100, 100, 100, 100), (110, 110, 110, 110), (111, 111, 111, 111),
            (111, 111, 111, 111), (111, 111, 111, 111), (112, 112, 112, 112), (112, 112, 112, 112)]
    df, sig = make(rows, long=[0], short=[2])
    tr, eq, _ = run(df, sig, P(exitHoldBars=3), costs=costs)
    assert list(tr.direction) == ["long", "short"]
    lt, st = tr.iloc[0], tr.iloc[1]
    q_long = 1000 / 100.0
    cash = 10000 - 100 * q_long - 0.001 * 100 * q_long
    E2 = cash + q_long * 110
    q_short = 0.10 * E2 / 110
    assert lt.exit_reason == "Reverse" and lt.exit_bar == 3 and lt.exit_price == 111
    assert lt.qty == pytest.approx(q_long)
    assert st.entry_bar == 3 and st.entry_price == 111 and st.qty == pytest.approx(q_short, rel=1e-12)
    # one fill of |pos|+q: total commission at bar-3 open = 0.1 % * 111 * (10 + q_short)
    assert lt.exit_commission + st.entry_commission == pytest.approx(0.001 * 111 * (q_long + q_short), rel=1e-12)
    assert lt.pnl == pytest.approx(11 * q_long - 1.0 - 0.001 * 111 * q_long, rel=1e-12)
    # hold of 3 counted from the reversal fill bar (3): close queued at bar 5, fills open of bar 6
    assert st.exit_reason == "LC Exit" and st.exit_bar == 6 and st.exit_price == 112


def test_long_exit_suppressed_when_short_cond():
    # (a) short_cond with a valid ATR -> reversal, not an LC Exit
    rows = [FLAT] * 6
    df, sig = make(rows, long=[0], short=[2], ns=[2])
    tr, _, _ = run(df, sig, P(exitMode="LC Signal Flip"))
    assert list(tr.exit_reason) == ["Reverse", "WindowEnd"]
    # (b) short_cond but risk_atr na -> no entry AND longExit suppressed -> long stays open
    atr = np.array([1.0, 1.0, np.nan, 1.0, 1.0, 1.0])
    df, sig = make(rows, long=[0], short=[2], ns=[2], atr=atr)
    tr, _, _ = run(df, sig, P(exitMode="LC Signal Flip"))
    assert len(tr) == 1 and tr.iloc[0].exit_reason == "WindowEnd" and tr.iloc[0].direction == "long"


def test_entries_blocked_outside_window():
    rows = [FLAT] * 10
    df, sig = make(rows, long=[1, 7], short=[4])
    ws, we = df.index[2], df.index[7]
    tr, eq, info = run(df, sig, P(exitHoldBars=2), ws=ws, we=we)
    # bar-1 signal is before the window: ignored. bar-4 short: enters bar 5, hold 2 -> queued at 6, fills 7.
    # bar-7 long is on the last window bar: queued order discarded.
    assert len(tr) == 1
    t = tr.iloc[0]
    assert t.direction == "short" and t.entry_bar == 5 and t.exit_bar == 7 and t.exit_reason == "LC Exit"
    assert len(eq) == 6 and eq.index[0] == ws and eq.index[-1] == we
    assert info["window_bars"] == 6


def test_window_end_force_close_and_later_bars_ignored():
    rows = [FLAT, FLAT, FLAT, (100, 101, 99, 100.7), (150, 150, 150, 150), (150, 150, 150, 150)]
    df, sig = make(rows, long=[0])
    tr, eq, info = run(df, sig, P(), costs=TICKS2, we=df.index[3])
    assert len(tr) == 1
    t = tr.iloc[0]
    assert t.exit_reason == "WindowEnd" and t.exit_bar == 3
    assert t.exit_price == pytest.approx(100.7 - 0.02)
    assert eq.index[-1] == df.index[3]
    assert eq.iloc[-1] == pytest.approx(10000 + t.pnl, rel=1e-12)


def test_lc_signal_flip_exit():
    rows = [FLAT, FLAT, FLAT, FLAT, (101, 101, 101, 101), FLAT, FLAT]
    df, sig = make(rows, long=[0], ns=[3])
    tr, _, _ = run(df, sig, P(exitMode="LC Signal Flip", exitHoldBars=1))   # hold ignored in flip mode
    t = tr.iloc[0]
    assert t.exit_reason == "LC Exit" and t.exit_bar == 4 and t.exit_price == 101
    # Either mode: the earlier of flip (bar 3 -> fill 4) and hold 6 bars
    tr, _, _ = run(df, sig, P(exitMode="Either (LC Default)", exitHoldBars=6))
    assert tr.iloc[0].exit_bar == 4
    # Fixed-hold mode ignores the flip
    tr, _, _ = run(df, sig, P(exitMode="LC Fixed Hold", exitHoldBars=6))
    assert tr.iloc[0].exit_reason == "WindowEnd"


def test_short_flip_exit_uses_new_buy():
    rows = [FLAT] * 6
    df, sig = make(rows, short=[0], nb=[2], ns=[1])
    tr, _, _ = run(df, sig, P(exitMode="LC Signal Flip"))
    t = tr.iloc[0]
    assert t.direction == "short" and t.exit_reason == "LC Exit" and t.exit_bar == 3


def test_both_conditions_rejected():
    df, sig = make([FLAT] * 3, long=[1], short=[1])
    with pytest.raises(ValueError):
        run(df, sig, P())


def test_runtime_30k_bars():
    rng = np.random.default_rng(0)
    n = 30000
    c = 20000 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    o = np.r_[c[0], c[:-1]]
    h = np.maximum(o, c) * 1.002
    lo = np.minimum(o, c) * 0.998
    df, sig = make(np.c_[o, h, lo, c], atr=50.0)
    r = rng.random(n)
    sig["long_cond"] = r < 0.01
    sig["short_cond"] = (r > 0.99)
    sig["lc_new_sell"] = rng.random(n) < 0.02
    sig["lc_new_buy"] = rng.random(n) < 0.02
    tr, eq, info = simulate(df, sig, P(exitMode="Either (LC Default)", exitHoldBars=4, riskUseSl=True,
                                       riskUseTp=True), df.index[0], df.index[-1], BASE)
    assert len(tr) > 100
    assert info["runtime_s"] < 2.0
    # accounting identity: final equity = capital + sum(pnl)
    assert eq.iloc[-1] == pytest.approx(10000 + tr.pnl.sum(), rel=1e-9)
