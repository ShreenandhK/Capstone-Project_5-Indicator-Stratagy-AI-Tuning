"""CLI guard tests (SPEC Sections 0, 6, 7) in a temporary CRB_BACKTEST_ROOT with SYNTHETIC data.

compute_signals is replaced by a spy that records the last bar it receives and returns random sparse
signals, so these tests never touch the real data file or the real signal engine.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import log_tools as lt  # noqa: E402
import run_backtest as rb  # noqa: E402


@pytest.fixture(scope="module")
def synthetic_csv(tmp_path_factory):
    rng = np.random.default_rng(42)
    idx = pd.date_range("2022-01-01 00:00", "2025-09-30 23:00", freq="h", tz="UTC")
    n = len(idx)
    c = 30000 * np.exp(np.cumsum(rng.normal(0, 0.006, n)))
    o = np.r_[30000.0, c[:-1]]
    df = pd.DataFrame({"time": idx.strftime("%Y-%m-%dT%H:%M:%SZ"), "open": o,
                       "high": np.maximum(o, c) * 1.002, "low": np.minimum(o, c) * 0.998, "close": c,
                       "volume": rng.uniform(1, 100, n)})
    path = tmp_path_factory.mktemp("synthdata") / "SYNTH_1h.csv"
    df.to_csv(path, index=False)
    return path


class Spy:
    def __init__(self, fail=False):
        self.calls = []
        self.fail = fail

    def __call__(self, df, p):
        self.calls.append({"max_time": df.index.max(), "rows": len(df)})
        if self.fail:
            raise RuntimeError("engine crash (simulated)")
        rng = np.random.default_rng(7)
        u = rng.random(len(df))
        return pd.DataFrame({"long_cond": u < 0.01, "short_cond": u > 0.99,
                             "lc_new_buy": rng.random(len(df)) < 0.01, "lc_new_sell": rng.random(len(df)) < 0.01,
                             "risk_atr": df["close"].to_numpy() * 0.005}, index=df.index)


@pytest.fixture
def env(tmp_path, monkeypatch, synthetic_csv):
    root = tmp_path / "bt"
    (root / "configs").mkdir(parents=True)
    monkeypatch.setenv("CRB_BACKTEST_ROOT", str(root))
    monkeypatch.setenv("CRB_DATA_FILE", str(synthetic_csv))
    spy = Spy()
    monkeypatch.setattr(rb, "compute_signals", spy)
    return root, spy


def cfg(root, nn, d):
    p = root / "configs" / f"run_{nn:02d}.json"
    p.write_text(json.dumps(d))
    return str(p)


def run_is(path):
    return rb.main(["is", "--config", path])


def n_logged(root):
    return lt.count_lines(root / "logs" / "tuning_log.jsonl")


def test_paths_redirected(env, synthetic_csv):
    root, _ = env
    P = lt.get_paths()
    assert P.root == root and P.data == synthetic_csv and P.jsonl == root / "logs" / "tuning_log.jsonl"


def test_run_ids_must_be_sequential(env):
    root, _ = env
    c1, c2, c3 = cfg(root, 1, {}), cfg(root, 2, {"exitHoldBars": 6}), cfg(root, 3, {"exitHoldBars": 8})
    assert run_is(c2) == 2 and n_logged(root) == 0
    assert run_is(c1) == 0 and n_logged(root) == 1
    for f in ("metrics.json", "trades.csv", "equity_daily.csv"):
        assert (root / "results" / "run_01" / f).exists()
    assert (root / "logs" / "tuning_log.md").exists() and (root / "logs" / "leaderboard.md").exists()
    assert run_is(c1) == 2 and n_logged(root) == 1          # cannot re-run a logged id
    assert run_is(c3) == 2 and n_logged(root) == 1
    assert run_is(c2) == 0 and n_logged(root) == 2
    recs = lt.read_jsonl(root / "logs" / "tuning_log.jsonl")
    assert [r["run_id"] for r in recs] == [1, 2]
    r2 = recs[1]
    assert r2["params_diff_vs_defaults"] == {"exitHoldBars": 6}
    for k in ("utc_timestamp", "config_hash", "params_full", "metrics", "gates", "eligible", "runtime_s", "data_sha256"):
        assert k in r2
    assert "stress" in r2["metrics"] and r2["metrics"]["stress"]["trades"] > 0      # stress sim executed
    md = (root / "logs" / "tuning_log.md").read_text()
    assert "## Run 02" in md and r2["config_hash"] in md and "<details>" in md
    assert repr(r2["metrics"]["sharpe"]) in md                                         # exact numbers
    assert lt.verify(lt.get_paths())[0] == []


def test_config_outside_configs_dir_refused(env, tmp_path):
    root, _ = env
    stray = tmp_path / "run_01.json"
    stray.write_text("{}")
    assert run_is(str(stray)) == 2 and n_logged(root) == 0


def test_26th_run_refused(env):
    root, _ = env
    for nn in range(1, 26):
        assert run_is(cfg(root, nn, {"exitHoldBars": nn})) == 0
    assert n_logged(root) == 25
    assert run_is(cfg(root, 26, {"exitHoldBars": 30})) == 2
    assert n_logged(root) == 25 and not (root / "results" / "run_26").exists()
    errors, _ = lt.verify(lt.get_paths())
    assert errors == []


def test_duplicate_hash_refused(env):
    root, _ = env
    assert run_is(cfg(root, 1, {})) == 0
    assert run_is(cfg(root, 2, {"exitHoldBars": 4})) == 2          # == Pine default -> same merged hash
    assert run_is(cfg(root, 2, {"initial_capital": 10000.0})) == 2  # fixed prop, same hash
    assert n_logged(root) == 1
    assert run_is(cfg(root, 2, {"exitHoldBars": 5})) == 0


def test_invalid_params_refused(env):
    root, _ = env
    assert run_is(cfg(root, 1, {"nwLookback": 5000})) == 2
    assert run_is(cfg(root, 1, {"notAParam": 1})) == 2
    assert run_is(cfg(root, 1, {"nwSrc": "open"})) == 2
    assert n_logged(root) == 0


def test_is_truncation_before_signals(env, synthetic_csv):
    root, spy = env
    raw_last = pd.to_datetime(pd.read_csv(synthetic_csv)["time"], utc=True).max()
    assert raw_last > rb.IS_END                                      # the file does contain later bars
    assert run_is(cfg(root, 1, {})) == 0
    assert len(spy.calls) == 1                                       # one signal pass feeds base + stress
    assert spy.calls[0]["max_time"] == pd.Timestamp("2025-06-30 23:00", tz="UTC")
    rec = lt.read_jsonl(root / "logs" / "tuning_log.jsonl")[0]
    assert rec["metrics"]["last_bar_time"] == "2025-06-30 23:00:00+00:00"
    tr = pd.read_csv(root / "results" / "run_01" / "trades.csv")
    assert (pd.to_datetime(tr["exit_time"], utc=True) <= rb.IS_END).all()
    assert (pd.to_datetime(tr["entry_time"], utc=True) >= rb.IS_START).all()


def test_load_data_truncates(synthetic_csv):
    df = rb.load_data(end_inclusive="2022-12-31 23:00", path=synthetic_csv)
    assert df.index.max() == pd.Timestamp("2022-12-31 23:00", tz="UTC") and df.index.tz is not None


def test_crash_does_not_consume_slot(env, monkeypatch):
    root, _ = env
    c1 = cfg(root, 1, {})
    monkeypatch.setattr(rb, "compute_signals", Spy(fail=True))
    with pytest.raises(RuntimeError):
        run_is(c1)
    assert n_logged(root) == 0
    monkeypatch.setattr(rb, "compute_signals", Spy())
    assert run_is(c1) == 0 and n_logged(root) == 1


def test_data_sha_mismatch_refused(env, tmp_path, monkeypatch, synthetic_csv):
    root, _ = env
    d = tmp_path / "d"
    d.mkdir()
    data = d / "X_1h.csv"
    data.write_bytes(synthetic_csv.read_bytes())
    (d / "X_1h.meta.json").write_text(json.dumps({"sha256": "0" * 64}))
    monkeypatch.setenv("CRB_DATA_FILE", str(data))
    assert run_is(cfg(root, 1, {})) == 2 and n_logged(root) == 0


def test_freeze_and_oos_once(env):
    root, spy = env
    assert run_is(cfg(root, 1, {})) == 0
    assert run_is(cfg(root, 2, {"exitHoldBars": 8})) == 0
    assert lt.main(["freeze"]) == 0
    frozen = root / "FROZEN_PARAMS.json"
    doc = json.loads(frozen.read_text())
    before = frozen.read_bytes()
    assert {"run_id", "config_hash", "params_full", "frozen_utc", "selection_rule", "is_metrics"} <= set(doc)
    assert lt.main(["freeze"]) == 2 and frozen.read_bytes() == before     # freeze refuses overwrite

    spy.calls.clear()
    assert rb.main(["oos", "--frozen", str(frozen)]) == 0
    oos = root / "results" / "OOS_FINAL"
    assert (oos / "LOCK").exists()
    for f in ("metrics.json", "trades.csv", "equity_daily.csv"):
        assert (oos / f).exists()
    assert spy.calls[0]["max_time"] == pd.Timestamp("2025-09-30 23:00", tz="UTC")   # continuous series
    m = json.loads((oos / "metrics.json").read_text())
    assert m["period"] == "OOS" and set(m["subperiods"]) == {"2025H2", "2026YTD"} and "gates" not in m
    tr = pd.read_csv(oos / "trades.csv")
    assert (pd.to_datetime(tr["entry_time"], utc=True) >= rb.OOS_START).all()
    assert rb.main(["oos", "--frozen", str(frozen)]) == 2                  # second OOS refused
    assert len(spy.calls) == 1


def test_oos_refuses_tampered_frozen(env):
    root, _ = env
    assert run_is(cfg(root, 1, {})) == 0
    assert lt.main(["freeze"]) == 0
    frozen = root / "FROZEN_PARAMS.json"
    doc = json.loads(frozen.read_text())
    doc["params_full"]["exitHoldBars"] = 9
    frozen.write_text(json.dumps(doc))
    assert rb.main(["oos", "--frozen", str(frozen)]) == 2
    assert not (root / "results" / "OOS_FINAL" / "LOCK").exists()


def test_verify_detects_tampered_config(env):
    root, _ = env
    c1 = cfg(root, 1, {"exitHoldBars": 6})
    assert run_is(c1) == 0
    assert lt.main(["verify"]) == 0
    Path(c1).write_text(json.dumps({"exitHoldBars": 7}))
    errors, _ = lt.verify(lt.get_paths())
    assert any("tampered" in e for e in errors)
    assert lt.main(["verify"]) == 1


def test_verify_detects_noncontiguous_and_missing_results(env):
    root, _ = env
    assert run_is(cfg(root, 1, {})) == 0
    jl = root / "logs" / "tuning_log.jsonl"
    rec = json.loads(jl.read_text().splitlines()[0])
    rec["run_id"] = 3
    jl.write_text(jl.read_text() + json.dumps(rec) + "\n")
    errors, _ = lt.verify(lt.get_paths())
    assert any("contiguous" in e for e in errors) and any("duplicate" in e for e in errors)
