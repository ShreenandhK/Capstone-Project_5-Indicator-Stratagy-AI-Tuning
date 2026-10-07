"""Independent reference check of the broker against backtesting.py 0.6.6.

Synthetic GBM OHLCV + random sparse long/short signals, exitMode 'LC Fixed Hold', no SL/TP,
commission 0.075 %/side, zero slippage. The same strategy logic is re-implemented in a
backtesting.py Strategy.next (fixed hold counted from the fill bar, reversal = one order of
|pos| + q, sizing 10 % of mark-to-market equity at the signal-bar close, next-open fills).

Known, deliberately neutralised differences:
  * backtesting.py trades integer units. FractionalBacktest(fractional_unit=1e-8) makes one unit
    1e-8 BTC and the strategy floors q to whole units, so quantities differ by < 1e-8 BTC per trade
    (pnl effect ~1e-6 USD per trade). Tolerances below reflect that and nothing else.
  * backtesting.py never calls next() on bar 0 -> no signals on bar 0.
  * backtesting.py's finalize_trades closes leftovers at the last bar's OPEN, while the emulator's
    WindowEnd closes at the last CLOSE (TradingView-style). Signals are disabled on the final bars
    so both engines end flat and the end-of-data rule does not enter the comparison (the WindowEnd
    rule is covered by test_broker.py).
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.broker import simulate  # noqa: E402

backtesting = pytest.importorskip("backtesting")
from backtesting import Strategy  # noqa: E402
from backtesting.lib import FractionalBacktest  # noqa: E402

N = 3000
HOLD = 6
FU = 1e-8
COMM = 0.075


def _data(seed=11):
    rng = np.random.default_rng(seed)
    ret = rng.normal(0.0, 0.008, N)
    close = 20000.0 * np.exp(np.cumsum(ret))
    open_ = np.r_[20000.0, close[:-1]] * (1 + rng.normal(0, 0.0005, N))   # small gaps
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.002, N)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.002, N)))
    idx = pd.date_range("2020-01-01", periods=N, freq="h", tz="UTC")
    df = pd.DataFrame({"open": open_, "high": high, "low": low, "close": close,
                       "volume": rng.uniform(1, 10, N)}, index=idx)
    u = rng.random(N)
    long_c = u < 0.03
    short_c = u > 0.97
    long_c[0] = short_c[0] = False
    long_c[-3 * HOLD:] = short_c[-3 * HOLD:] = False
    sig = pd.DataFrame({"long_cond": long_c, "short_cond": short_c, "lc_new_buy": False, "lc_new_sell": False,
                        "risk_atr": 1.0}, index=idx)
    return df, sig


def _run_backtestingpy(df, sig):
    LONG = sig["long_cond"].to_numpy()
    SHORT = sig["short_cond"].to_numpy()

    class CRBHold(Strategy):
        def init(self):
            pass

        def next(self):
            i = len(self.data) - 1
            lc, sc = bool(LONG[i]), bool(SHORT[i])
            pos = self.position.size                 # whole units of FU
            in_long, in_short = pos > 0, pos < 0
            bars_from = (i - self.trades[-1].entry_bar + 1) if self.trades else 0
            hold_exp = bars_from >= HOLD
            long_exit = in_long and hold_exp and not sc
            short_exit = in_short and hold_exp and not lc
            q = int(0.10 * self.equity / self.data.Close[-1])   # Close is scaled by FU -> q in units
            if lc and not in_long:
                self.buy(size=abs(pos) + q)
            if sc and not in_short:
                self.sell(size=abs(pos) + q)
            if long_exit or short_exit:
                self.position.close()

    data = df.rename(columns=str.capitalize).tz_localize(None)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bt = FractionalBacktest(data, CRBHold, cash=10000, commission=COMM / 100, spread=0.0, margin=1.0,
                                trade_on_close=False, hedging=False, exclusive_orders=False,
                                finalize_trades=True, fractional_unit=FU)
        stats = bt.run()
    return stats


def test_crosscheck_fixed_hold_vs_backtestingpy():
    df, sig = _data()
    p = dict(exitMode="LC Fixed Hold", exitHoldBars=HOLD, riskUseSl=False, riskUseTp=False,
             riskSlMult=2.0, riskTpMult=3.0)
    costs = {"commission_pct": COMM, "slip_mode": "ticks", "slip_value": 0, "mintick": 0.01}
    tr, eq, info = simulate(df, sig, p, df.index[0], df.index[-1], costs)
    stats = _run_backtestingpy(df, sig)
    bt = stats["_trades"].sort_values(["EntryTime", "ExitTime"]).reset_index(drop=True)
    ours = tr.sort_values(["entry_time", "exit_time"]).reset_index(drop=True)

    assert len(ours) > 100 and (ours.exit_reason == "Reverse").sum() > 5
    assert (ours.exit_reason != "WindowEnd").all()
    assert len(ours) == len(bt)
    assert (ours.entry_time.dt.tz_localize(None).to_numpy() == bt.EntryTime.to_numpy()).all()
    assert (ours.exit_time.dt.tz_localize(None).to_numpy() == bt.ExitTime.to_numpy()).all()
    np.testing.assert_allclose(ours.entry_price.to_numpy(), bt.EntryPrice.to_numpy(), rtol=1e-12)
    np.testing.assert_allclose(ours.exit_price.to_numpy(), bt.ExitPrice.to_numpy(), rtol=1e-12)
    signed = np.where(ours.direction == "long", 1.0, -1.0) * ours.qty.to_numpy()
    np.testing.assert_allclose(signed, bt.Size.to_numpy(), rtol=0, atol=2 * FU)
    np.testing.assert_allclose(ours.pnl.to_numpy(), bt.PnL.to_numpy(), rtol=0, atol=1e-4)
    final_bt = float(stats["Equity Final [$]"])
    rel = abs(eq.iloc[-1] - final_bt) / final_bt
    print(f"\ncrosscheck: trades={len(ours)} reversals={(ours.exit_reason == 'Reverse').sum()} "
          f"final_ours={eq.iloc[-1]:.6f} final_bt={final_bt:.6f} rel_diff={rel:.3e} "
          f"max|dpnl|={np.abs(ours.pnl.to_numpy() - bt.PnL.to_numpy()).max():.3e}")
    assert rel < 1e-7
    # the whole mark-to-market curve agrees too
    bt_eq = stats["_equity_curve"]["Equity"].to_numpy()
    np.testing.assert_allclose(eq.to_numpy()[1:], bt_eq[1:], rtol=1e-7)
