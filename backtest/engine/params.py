"""Strategy parameters: Pine input defaults, fixed values, tunable bounds, validation, hashing.

Keys are the exact Pine input variable names of `Combined Role-Based Strategy.pine` (SPEC Section 2).
"""
from __future__ import annotations

import hashlib
import json
import math
import numbers

# ---------------------------------------------------------------------------------------------------
# DEFAULTS: every input.* of the .pine file, exact name and exact default.
# Type is carried by the Python type of the default: bool / int / float / str
# (input.source defaults are stored as the source name string).
# ---------------------------------------------------------------------------------------------------
DEFAULTS: dict = {
    # Strategy controls
    "allowLongs": True,
    "allowShorts": True,
    # Trend | Nadaraya-Watson
    "nwSrc": "close",
    "nwKernelType": "Gaussian",
    "nwLookback": 50,
    "nwBandwidth": 8,
    "nwHMult": 2.0,
    "nwRelWeight": 8.0,
    "nwSlopeLen": 1,
    "nwRequirePriceSide": False,
    # Entry | Lorentzian Classification
    "lcSource": "close",
    "lcNeighbors": 8,
    "lcMaxBarsBack": 2000,
    "lcIncludeFullHistory": False,
    "lcHorizon": 4,
    "lcSpacing": 4,
    "lcDistQuantile": 0.75,
    "lcEntryWindow": 2,
    # Entry | LC Feature Engineering
    "lcFeatureCount": 5,
    "lcF1String": "RSI",
    "lcF1ParamA": 14,
    "lcF1ParamB": 1,
    "lcF2String": "WT",
    "lcF2ParamA": 10,
    "lcF2ParamB": 11,
    "lcF3String": "CCI",
    "lcF3ParamA": 20,
    "lcF3ParamB": 1,
    "lcF4String": "ADX",
    "lcF4ParamA": 20,
    "lcF4ParamB": 2,
    "lcF5String": "RSI",
    "lcF5ParamA": 9,
    "lcF5ParamB": 1,
    # Entry | LC Prediction Filters
    "lcUseVolFilter": True,
    "lcVolMinLen": 1,
    "lcVolMaxLen": 10,
    "lcUseRegimeFilter": True,
    "lcRegimeThreshold": -0.1,
    "lcRegimeSrc": "ohlc4",
    "lcUseAdxFilter": False,
    "lcAdxThreshold": 20,
    "lcAdxLen": 14,
    # Timing | WaveTrend
    "wtSrc": "hlc3",
    "wtN1": 10,
    "wtN2": 21,
    "wtSigLen": 4,
    "wtCciConst": 0.015,
    "wtObLevel1": 60,
    "wtObLevel2": 53,
    "wtOsLevel1": -60,
    "wtOsLevel2": -53,
    "wtExtLevelSel": "Level 2",
    "wtTimingMode": "Recent Cross + Not Overextended",
    "wtCrossWindow": 5,
    # Confirmation | Weis Wave Volume
    "wwvMethod": "ATR",
    "wwvMethodValue": 14.0,
    "wwvPriceSource": "Close",
    "wwvUseTrueRange": "Auto",
    "wwvNormalize": False,
    "wwvUseVolThreshold": False,
    "wwvAvgLen": 20,
    "wwvAvgMult": 1.0,
    # Regime Gate | Squeeze Momentum
    "sqzSrc": "close",
    "sqzBbLen": 20,
    "sqzBbMult": 2.0,
    "sqzKcLen": 20,
    "sqzKcMult": 1.5,
    "sqzUseTrueRange": True,
    "sqzReplicateQuirk": True,
    "sqzRegimeMode": "Squeeze Off",
    "sqzReleaseWindow": 5,
    "sqzRequireMomExpansion": False,
    # Exits & Risk
    "exitMode": "Either (LC Default)",
    "exitHoldBars": 4,
    "riskUseSl": True,
    "riskUseTp": False,
    "riskAtrLen": 14,
    "riskSlMult": 2.0,
    "riskTpMult": 3.0,
}

# Strategy properties from the strategy() declaration (not inputs; fixed, SPEC Section 2).
STRATEGY_PROPS: dict = {
    "initial_capital": 10000.0,
    "percent_of_equity": 10.0,
    "pyramiding": 0,
    "commission_pct": 0.075,
    "slippage_ticks": 2,
    "mintick": 0.01,
}

# FIXED: not tunable; validate() rejects any change.
FIXED_INPUTS: dict = {
    "nwSrc": "close",
    "lcSource": "close",
    "lcRegimeSrc": "ohlc4",
    "wtSrc": "hlc3",
    "sqzSrc": "close",
    "wtCciConst": 0.015,
    "lcIncludeFullHistory": False,
    "wwvUseTrueRange": "Auto",
}
FIXED: dict = {**FIXED_INPUTS, **STRATEGY_PROPS}

_FEATURES = ["RSI", "WT", "CCI", "ADX"]

# BOUNDS (inclusive): (lo, hi) tuple for int/float, list of options for strings, `bool` for booleans.
BOUNDS: dict = {
    # Strategy
    "allowLongs": bool,
    "allowShorts": bool,
    # NW
    "nwKernelType": ["Gaussian", "Epanechnikov", "Triangular", "Quartic", "Cosine", "Rational Quadratic"],
    "nwLookback": (10, 300),
    "nwBandwidth": (1, 50),
    "nwHMult": (0.5, 5.0),
    "nwRelWeight": (0.25, 25.0),
    "nwSlopeLen": (1, 20),
    "nwRequirePriceSide": bool,
    # LC
    "lcNeighbors": (4, 30),
    "lcMaxBarsBack": (500, 5000),
    "lcHorizon": (1, 20),
    "lcSpacing": (2, 10),
    "lcDistQuantile": (0.5, 1.0),
    "lcEntryWindow": (0, 10),
    "lcFeatureCount": (2, 5),
    "lcUseVolFilter": bool,
    "lcVolMinLen": (1, 10),
    "lcVolMaxLen": (2, 50),
    "lcUseRegimeFilter": bool,
    "lcRegimeThreshold": (-1.0, 1.0),
    "lcUseAdxFilter": bool,
    "lcAdxThreshold": (5, 50),
    "lcAdxLen": (5, 50),
    # WT
    "wtN1": (3, 40),
    "wtN2": (5, 60),
    "wtSigLen": (2, 10),
    "wtObLevel1": (30, 100),
    "wtObLevel2": (20, 100),
    "wtOsLevel1": (-100, -30),
    "wtOsLevel2": (-100, -20),
    "wtExtLevelSel": ["Level 1", "Level 2"],
    "wtTimingMode": ["Recent Cross + Not Overextended", "Not Overextended Only"],
    "wtCrossWindow": (0, 20),
    # WWV
    "wwvMethod": ["ATR", "Traditional", "Part of Price"],
    "wwvMethodValue": (1.0, 2000.0),
    "wwvPriceSource": ["Close", "Open / Close", "High / Low"],
    "wwvNormalize": bool,
    "wwvUseVolThreshold": bool,
    "wwvAvgLen": (2, 100),
    "wwvAvgMult": (0.1, 3.0),
    # SQZ
    "sqzBbLen": (5, 60),
    "sqzBbMult": (0.5, 4.0),
    "sqzKcLen": (5, 60),
    "sqzKcMult": (0.5, 4.0),
    "sqzUseTrueRange": bool,
    "sqzReplicateQuirk": bool,
    "sqzRegimeMode": ["Squeeze Off", "Not In Squeeze", "Released Within Window"],
    "sqzReleaseWindow": (1, 50),
    "sqzRequireMomExpansion": bool,
    # Exit
    "exitMode": ["LC Signal Flip", "LC Fixed Hold", "Either (LC Default)"],
    "exitHoldBars": (1, 96),
    "riskUseSl": bool,
    "riskUseTp": bool,
    "riskAtrLen": (2, 50),
    "riskSlMult": (0.5, 8.0),
    "riskTpMult": (0.5, 12.0),
}
for _k in range(1, 6):
    BOUNDS[f"lcF{_k}String"] = list(_FEATURES)
    BOUNDS[f"lcF{_k}ParamA"] = (2, 50)
    BOUNDS[f"lcF{_k}ParamB"] = (1, 20)
del _k


def _is_bool(v) -> bool:
    return isinstance(v, bool) or type(v).__name__ == "bool_"


def _coerce(key: str, value, proto):
    """Type-check `value` against the type of `proto`; return the coerced value or raise ValueError."""
    if isinstance(proto, bool):
        if not _is_bool(value):
            raise ValueError(f"{key}: expected bool, got {type(value).__name__} ({value!r})")
        return bool(value)
    if isinstance(proto, int):
        if _is_bool(value) or not isinstance(value, numbers.Integral):
            raise ValueError(f"{key}: expected int, got {type(value).__name__} ({value!r})")
        return int(value)
    if isinstance(proto, float):
        if _is_bool(value) or not isinstance(value, numbers.Real):
            raise ValueError(f"{key}: expected float, got {type(value).__name__} ({value!r})")
        fv = float(value)
        if not math.isfinite(fv):
            raise ValueError(f"{key}: non-finite value {value!r}")
        return fv
    if isinstance(proto, str):
        if not isinstance(value, str):
            raise ValueError(f"{key}: expected str, got {type(value).__name__} ({value!r})")
        return value
    raise ValueError(f"{key}: unsupported prototype type {type(proto).__name__}")


def validate(cfg: dict) -> dict:
    """Merge `cfg` over DEFAULTS with strict checks. Returns the full merged dict (DEFAULTS keys only).

    Raises ValueError on: unknown key, wrong type, out-of-bounds value, invalid option, change to a FIXED key.
    Strategy-property keys (STRATEGY_PROPS) are accepted only if equal to their fixed value and are not
    stored in the returned dict (so the config hash is identical whether or not they are supplied).
    """
    if cfg is None:
        cfg = {}
    if not isinstance(cfg, dict):
        raise ValueError(f"config must be a dict, got {type(cfg).__name__}")
    full = dict(DEFAULTS)
    for key, value in cfg.items():
        if key in STRATEGY_PROPS:
            proto = STRATEGY_PROPS[key]
            v = _coerce(key, value, proto)
            if v != proto:
                raise ValueError(f"{key} is FIXED at {proto!r}; got {value!r}")
            continue
        if key not in DEFAULTS:
            raise ValueError(f"unknown parameter key: {key!r}")
        proto = DEFAULTS[key]
        v = _coerce(key, value, proto)
        if key in FIXED_INPUTS:
            if v != FIXED_INPUTS[key]:
                raise ValueError(f"{key} is FIXED at {FIXED_INPUTS[key]!r}; got {value!r}")
            full[key] = v
            continue
        b = BOUNDS.get(key)
        if b is None:
            raise ValueError(f"{key}: no bounds defined (not tunable)")
        if b is bool:
            pass
        elif isinstance(b, list):
            if v not in b:
                raise ValueError(f"{key}: invalid option {v!r}; allowed {b}")
        else:
            lo, hi = b
            if not (lo <= v <= hi):
                raise ValueError(f"{key}: {v!r} out of bounds [{lo}, {hi}]")
        full[key] = v
    return full


def config_hash(full: dict) -> str:
    s = json.dumps(full, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def diff_vs_defaults(full: dict) -> dict:
    return {k: v for k, v in full.items() if k not in DEFAULTS or DEFAULTS[k] != v or type(DEFAULTS[k]) is not type(v)}
