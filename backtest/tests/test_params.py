import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine import params as P  # noqa: E402

PINE = ROOT.parent / "Combined Role-Based Strategy.pine"

_INPUT_RE = re.compile(r"^\s*(\w+)\s*=\s*input\.(bool|int|float|string|source)\(\s*([^,]+?)\s*,", re.M)


def _parse_pine_inputs():
    text = PINE.read_text(encoding="utf-8")
    out = {}
    for name, kind, raw in _INPUT_RE.findall(text):
        if kind == "bool":
            val = {"true": True, "false": False}[raw]
        elif kind == "int":
            val = int(raw)
        elif kind == "float":
            val = float(raw)
        elif kind == "string":
            assert raw[0] == raw[-1] == "'"
            val = raw[1:-1]
        else:
            val = raw
        assert name not in out, f"duplicate input {name}"
        out[name] = (kind, val)
    return out


def test_pine_inputs_match_defaults_or_frozen():
    """Before the study is frozen the .pine inputs equal engine DEFAULTS (the Pine baseline used for run 01).
    After `log_tools.py freeze`, the .pine is updated to FROZEN_PARAMS.json and must equal that instead.
    DEFAULTS itself must never change: every logged config_hash is computed over DEFAULTS-merged dicts."""
    import json

    pine = _parse_pine_inputs()
    assert len(pine) > 70
    assert set(pine) == set(P.DEFAULTS), (set(pine) ^ set(P.DEFAULTS))
    frozen = ROOT / "FROZEN_PARAMS.json"
    expected = json.loads(frozen.read_text(encoding="utf-8"))["params_full"] if frozen.exists() else P.DEFAULTS
    types = {"bool": bool, "int": int, "float": float, "string": str, "source": str}
    for name, (kind, val) in pine.items():
        d = P.DEFAULTS[name]
        assert type(d) is types[kind], (name, kind, type(d))
        assert expected[name] == val, (name, expected[name], val)


def test_every_default_is_fixed_or_bounded_and_in_bounds():
    for k, v in P.DEFAULTS.items():
        assert (k in P.FIXED) != (k in P.BOUNDS), k
    full = P.validate({})
    assert full == P.DEFAULTS
    assert P.validate(dict(P.DEFAULTS)) == P.DEFAULTS


def test_validate_rejections():
    bad = [
        {"unknownKey": 1},
        {"nwLookback": 5},
        {"nwLookback": 301},
        {"nwLookback": 50.0},
        {"nwLookback": True},
        {"allowLongs": 1},
        {"nwHMult": "2.0"},
        {"nwHMult": True},
        {"nwHMult": float("nan")},
        {"nwKernelType": "Laplace"},
        {"lcF1String": "MACD"},
        {"lcDistQuantile": 0.49},
        {"wtOsLevel1": -20},
        {"nwSrc": "open"},
        {"wtCciConst": 0.02},
        {"lcIncludeFullHistory": True},
        {"wwvUseTrueRange": "Never"},
        {"initial_capital": 5000},
        {"commission_pct": 0.1},
        {"wwvMethodValue": 0.5},
    ]
    for cfg in bad:
        with pytest.raises(ValueError):
            P.validate(cfg)


def test_validate_accepts_and_casts():
    full = P.validate({"nwHMult": 3, "lcNeighbors": 12, "sqzRegimeMode": "Not In Squeeze",
                       "nwSrc": "close", "initial_capital": 10000})
    assert type(full["nwHMult"]) is float and full["nwHMult"] == 3.0
    assert full["lcNeighbors"] == 12
    assert "initial_capital" not in full
    assert P.diff_vs_defaults(full) == {"nwHMult": 3.0, "lcNeighbors": 12, "sqzRegimeMode": "Not In Squeeze"}
    assert P.diff_vs_defaults(P.validate({})) == {}


def test_config_hash():
    a = P.config_hash(P.validate({}))
    b = P.config_hash(dict(reversed(list(P.validate({}).items()))))
    assert a == b and len(a) == 12 and re.fullmatch(r"[0-9a-f]{12}", a)
    assert P.config_hash(P.validate({"lcNeighbors": 9})) != a
    assert P.config_hash(P.validate({"initial_capital": 10000})) == a
