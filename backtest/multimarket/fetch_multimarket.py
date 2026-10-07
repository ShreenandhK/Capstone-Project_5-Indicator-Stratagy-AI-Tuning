"""Fetch daily OHLCV for the multi-market CRB backtest -> multimarket/data/<KEY>.csv + <KEY>.meta.json.

Data acquisition and data-quality checks only (no indicator / signal computation).

  BTCUSD_1D    Bitstamp  GET /api/v2/ohlc/btcusd/ step=86400      (TradingView BITSTAMP:BTCUSD)
  NIFTY_1D     Yahoo     GET /v8/finance/chart/^NSEI 1d            (TradingView NSE:NIFTY)
  HDFCBANK_1D  Yahoo     GET /v8/finance/chart/HDFCBANK.NS 1d      (TradingView NSE:HDFCBANK)
  RELIANCE_1D  Yahoo     GET /v8/finance/chart/RELIANCE.NS 1d      (TradingView NSE:RELIANCE)

CSV columns: time,open,high,low,close,volume. time = session DATE at 00:00:00Z (exchange-local date for NSE,
UTC day for Bitstamp), so one row per trading day and UTC-day grouping in the metrics is exact.
Yahoo OHLC is split/bonus-adjusted and NOT dividend-adjusted (TradingView NSE default). The still-forming
bar of the current day is dropped. OHLC inconsistencies are repaired (high/low widened) and counted in meta.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

OUT = Path(__file__).resolve().parent / "data"
UA = {"User-Agent": "Mozilla/5.0 (cip-project-backtest-data-fetch/1.0)"}

# Documented, inspected corrections of Yahoo errors (date ranges inclusive, exchange-local dates).
MANUAL_FIXES = {
    # the 1997-10-27 2:1 split is applied one week late: 7 bars stay unadjusted (+91 % in, -48 % out)
    "RELIANCE_1D": [("1997-10-27", "1997-11-04", 0.5)],
}

YAHOO = {
    "NIFTY_1D": ("^NSEI", "NSE:NIFTY"),
    "HDFCBANK_1D": ("HDFCBANK.NS", "NSE:HDFCBANK"),
    "RELIANCE_1D": ("RELIANCE.NS", "NSE:RELIANCE"),
}


def get_json(url: str, params: dict, tries: int = 8):
    for attempt in range(tries):
        wait = min(60, 2 ** attempt)
        try:
            r = requests.get(url, params=params, headers=UA, timeout=30)
            if r.status_code == 200:
                try:
                    return r.json()
                except ValueError:
                    pass
            print(f"  HTTP {r.status_code}; retry {attempt + 1} in {wait}s", file=sys.stderr)
        except requests.RequestException as exc:
            print(f"  {exc}; retry {attempt + 1} in {wait}s", file=sys.stderr)
        time.sleep(wait)
    raise RuntimeError(f"failed after {tries} tries: {url} {params}")


def fetch_bitstamp() -> pd.DataFrame:
    url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"
    start = 1313625600  # 2011-08-18, first Bitstamp day
    today = int(datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
    rows: dict[int, tuple] = {}
    while True:
        print(f"  bitstamp page from {datetime.fromtimestamp(start, timezone.utc):%Y-%m-%d}")
        ohlc = get_json(url, {"step": 86400, "limit": 1000, "start": start})["data"]["ohlc"]
        if not ohlc:
            break
        for x in ohlc:
            ts = int(x["timestamp"])
            if ts >= today:  # current UTC day still forming
                continue
            rows[ts] = (float(x["open"]), float(x["high"]), float(x["low"]), float(x["close"]), float(x["volume"]))
        last = int(ohlc[-1]["timestamp"])
        if last + 86400 >= today or last + 86400 <= start:
            break
        start = last + 86400
        time.sleep(1.5)
    ts = sorted(rows)
    return pd.DataFrame({
        "date": [datetime.fromtimestamp(t, timezone.utc).date() for t in ts],
        **{k: [rows[t][i] for t in ts] for i, k in enumerate(["open", "high", "low", "close", "volume"])},
    })


def fetch_yahoo(symbol: str) -> tuple[pd.DataFrame, list]:
    res = get_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
                   {"period1": 0, "period2": int(time.time()), "interval": "1d", "events": "split"})["chart"]["result"][0]
    off = int(res["meta"]["gmtoffset"])
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame({
        "date": [datetime.fromtimestamp(t + off, timezone.utc).date() for t in res["timestamp"]],
        **{k: pd.to_numeric(pd.Series(q[k], dtype=object), errors="coerce") for k in
           ["open", "high", "low", "close", "volume"]},
    })
    today_local = datetime.fromtimestamp(time.time() + off, timezone.utc).date()
    df = df[df["date"] < today_local]
    splits = sorted(({"date": datetime.fromtimestamp(int(s["date"]) + off, timezone.utc).date().isoformat(),
                      "ratio": s["splitRatio"]} for s in res.get("events", {}).get("splits", {}).values()),
                    key=lambda s: s["date"])
    return df, splits


def clean(df: pd.DataFrame, key: str, drop_filler: bool) -> tuple[pd.DataFrame, dict]:
    n0 = len(df)
    df = df.dropna(subset=["open", "high", "low", "close"])
    df = df[(df[["open", "high", "low", "close"]] > 0).all(axis=1)]
    dropped = n0 - len(df)
    df = df.sort_values("date").drop_duplicates("date", keep="last").reset_index(drop=True)
    fixes = []
    for a, b, factor in MANUAL_FIXES.get(key, []):
        m = (df["date"] >= date.fromisoformat(a)) & (df["date"] <= date.fromisoformat(b))
        df.loc[m, ["open", "high", "low", "close"]] *= factor
        fixes.append({"from": a, "to": b, "price_factor": factor, "rows": int(m.sum())})
    filler = []
    if drop_filler:  # Yahoo non-session rows: zero volume and o == h == l == c
        m = (df["volume"].fillna(0) <= 0) & (df["high"] == df["low"])
        filler = [d.isoformat() for d in df.loc[m, "date"]]
        df = df[~m].reset_index(drop=True)
    hi = df[["open", "high", "low", "close"]].max(axis=1)
    lo = df[["open", "high", "low", "close"]].min(axis=1)
    repaired = int(((df["high"] < hi) | (df["low"] > lo)).sum())
    df["high"], df["low"] = hi, lo
    ret = df["close"].pct_change()
    big = df.loc[ret.abs() > 0.20, "date"]
    dates = pd.to_datetime(df["date"])
    gap = dates.diff().dt.days
    return df, {
        "rows_dropped_na_or_nonpositive": int(dropped),
        "manual_fixes": fixes,
        "rows_dropped_zero_volume_flat": len(filler),
        "rows_dropped_zero_volume_flat_dates": filler,
        "rows_ohlc_repaired": repaired,
        "flat_bars_o_eq_h_eq_l_eq_c": int(((df["high"] == df["low"])).sum()),
        "zero_or_na_volume_bars": int((df["volume"].fillna(0) <= 0).sum()),
        "close_moves_gt_20pct": [{"date": d.isoformat(), "ret_pct": round(float(ret[i]) * 100, 2)}
                                 for i, d in big.items()],
        "calendar_gaps_gt_5_days": [{"after": df["date"][i - 1].isoformat(), "next": df["date"][i].isoformat(),
                                     "days": int(gap[i])} for i in np.flatnonzero(gap.fillna(0) > 5)],
    }


def write(key: str, df: pd.DataFrame, meta: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    csv = OUT / f"{key}.csv"
    out = pd.DataFrame({"time": [f"{d.isoformat()}T00:00:00Z" for d in df["date"]],
                        **{k: df[k] for k in ["open", "high", "low", "close", "volume"]}})
    out.to_csv(csv, index=False, float_format="%.10g")
    sha = hashlib.sha256(csv.read_bytes()).hexdigest()
    meta = {**meta, "fetched_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "rows": len(out),
            "first_bar": out["time"].iloc[0], "last_bar": out["time"].iloc[-1], "sha256": sha}
    (OUT / f"{key}.meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    q = meta["quality"]
    print(f"{key}: {meta['rows']} rows {meta['first_bar'][:10]} -> {meta['last_bar'][:10]} | dropped "
          f"{q['rows_dropped_na_or_nonpositive']} filler {q['rows_dropped_zero_volume_flat']} "
          f"(last {q['rows_dropped_zero_volume_flat_dates'][-5:]}) fixes {q['manual_fixes']} "
          f"repaired {q['rows_ohlc_repaired']} flat {q['flat_bars_o_eq_h_eq_l_eq_c']} "
          f"| >20% moves {[(m['date'], m['ret_pct']) for m in q['close_moves_gt_20pct']][:8]} "
          f"| gaps>5d {len(q['calendar_gaps_gt_5_days'])} {[(g['after'], g['days']) for g in q['calendar_gaps_gt_5_days']][:6]}")
    if "splits" in meta:
        print(f"  splits: {meta['splits']}")


def main(keys: list[str]) -> None:
    keys = keys or ["BTCUSD_1D", *YAHOO]
    for key in keys:
        if key == "BTCUSD_1D":
            df, q = clean(fetch_bitstamp(), key, drop_filler=False)  # Bitstamp no-trade days are real bars
            write(key, df, {"source": "Bitstamp GET https://www.bitstamp.net/api/v2/ohlc/btcusd/ step=86400",
                            "tradingview_symbol": "BITSTAMP:BTCUSD", "session_date": "UTC day", "quality": q})
        else:
            sym, tv = YAHOO[key]
            raw, splits = fetch_yahoo(sym)
            df, q = clean(raw, key, drop_filler=True)
            write(key, df, {"source": f"Yahoo Finance GET /v8/finance/chart/{sym} interval=1d (split-adjusted, "
                                      f"not dividend-adjusted)", "tradingview_symbol": tv,
                            "session_date": "Asia/Kolkata date", "splits": splits, "quality": q})
            time.sleep(1.0)


if __name__ == "__main__":
    main(sys.argv[1:])
