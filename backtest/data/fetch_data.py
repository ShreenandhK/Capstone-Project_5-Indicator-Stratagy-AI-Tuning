"""
Fetch BTCUSDT 1h klines from Binance spot and write data/BTCUSDT_1h.csv + meta.json.

Per SPEC.md Section 0 (data rules):
  - source: Binance spot GET /api/v3/klines?symbol=BTCUSDT&interval=1h
  - range:  2022-01-01T00:00:00Z  ->  most recent FULLY CLOSED hourly bar
  - CSV columns exactly: time,open,high,low,close,volume
      time  = bar OPEN time, ISO8601 UTC, e.g. 2022-01-01T00:00:00Z
      volume = base-asset volume (kline field index 5)
  - sorted ascending, no duplicates
  - gaps (missing hours) are NOT filled -- they are detected and listed only
  - writes BTCUSDT_1h.meta.json: source, symbol, interval, fetched_utc, rows,
    first_bar, last_bar, gaps, sha256 (of the CSV file bytes)

This script performs NO strategy/indicator/signal computation -- data
acquisition and data-quality checks only.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time as time_module
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1h"
INTERVAL_MS = 3_600_000
START_TIME = datetime(2022, 1, 1, tzinfo=timezone.utc)
LIMIT = 1000

SLEEP_BETWEEN_REQUESTS_S = 0.35
MAX_RETRIES = 6
BACKOFF_BASE_S = 1.0
REQUEST_TIMEOUT_S = 30

DATA_DIR = Path(__file__).resolve().parent
CSV_PATH = DATA_DIR / "BTCUSDT_1h.csv"
META_PATH = DATA_DIR / "BTCUSDT_1h.meta.json"


def iso_z(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_page(session: requests.Session, start_ms: int, limit: int = LIMIT) -> list:
    """Fetch one page of klines, retrying with backoff on errors / 429 / 5xx."""
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "startTime": start_ms,
        "limit": limit,
    }
    last_exc = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = session.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT_S)
        except requests.RequestException as exc:
            last_exc = exc
            wait = BACKOFF_BASE_S * (2 ** attempt)
            print(f"  request error ({exc}); retrying in {wait:.1f}s", file=sys.stderr)
            time_module.sleep(wait)
            continue

        if resp.status_code == 200:
            return resp.json()

        if resp.status_code in (429, 418):
            retry_after = resp.headers.get("Retry-After")
            wait = float(retry_after) if retry_after else BACKOFF_BASE_S * (2 ** attempt)
            print(f"  rate limited (HTTP {resp.status_code}); waiting {wait:.1f}s", file=sys.stderr)
            time_module.sleep(wait)
            continue

        if 500 <= resp.status_code < 600:
            wait = BACKOFF_BASE_S * (2 ** attempt)
            print(f"  server error (HTTP {resp.status_code}); retrying in {wait:.1f}s", file=sys.stderr)
            time_module.sleep(wait)
            continue

        # Other 4xx (bad request, invalid symbol, etc.) -- not retryable.
        resp.raise_for_status()

    raise RuntimeError(
        f"Failed to fetch page starting at {start_ms} after {MAX_RETRIES} retries"
    ) from last_exc


def fetch_all_klines() -> tuple[list, int]:
    """Paginate from START_TIME to the most recent fully-closed hourly bar."""
    session = requests.Session()
    session.headers.update({"User-Agent": "cip-project-backtest-data-fetch/1.0"})

    start_ms = int(START_TIME.timestamp() * 1000)
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    all_rows: list = []
    page_num = 0
    reached_present = False

    while not reached_present:
        page_num += 1
        start_iso = iso_z(datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc))
        print(f"Fetching page {page_num} starting {start_iso} ...")
        klines = fetch_page(session, start_ms)

        if not klines:
            break

        for k in klines:
            close_time_ms = k[6]
            if close_time_ms >= now_ms:
                # Bar's close time is not yet in the past relative to fetch
                # time -> not fully closed. Drop it and stop (klines are
                # returned in ascending open_time order, so everything after
                # this point in the page would also be unclosed/forming).
                reached_present = True
                break
            all_rows.append(k)

        if reached_present:
            break

        last_open_time_ms = klines[-1][0]
        start_ms = last_open_time_ms + INTERVAL_MS

        time_module.sleep(SLEEP_BETWEEN_REQUESTS_S)

    return all_rows, now_ms


def build_dataframe(rows: list) -> pd.DataFrame:
    records = []
    for k in rows:
        open_time_ms = k[0]
        dt = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc)
        records.append(
            {
                "_open_time_ms": open_time_ms,
                "time": iso_z(dt),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),  # base-asset volume, kline field index 5
            }
        )
    df = pd.DataFrame.from_records(records)
    df = (
        df.sort_values("_open_time_ms")
        .drop_duplicates(subset="_open_time_ms", keep="first")
        .reset_index(drop=True)
    )
    return df


def validate(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    cols = ["open", "high", "low", "close", "volume"]

    if df[cols].isna().any().any():
        errors.append("NaN values found in OHLCV columns")

    open_times = df["_open_time_ms"].to_numpy()
    if len(open_times) != len(set(open_times.tolist())):
        errors.append("duplicate timestamps found")

    diffs = pd.Series(open_times).diff().dropna()
    if (diffs <= 0).any():
        errors.append("timestamps not strictly increasing")

    bad_high = df["high"] < df[["open", "close"]].max(axis=1)
    if bad_high.any():
        errors.append(f"{int(bad_high.sum())} bars with high < max(open,close)")

    bad_low = df["low"] > df[["open", "close"]].min(axis=1)
    if bad_low.any():
        errors.append(f"{int(bad_low.sum())} bars with low > min(open,close)")

    if (df["volume"] < 0).any():
        errors.append("negative volume found")

    return errors


def find_gaps(df: pd.DataFrame) -> list[dict]:
    """List consecutive-bar gaps (missing hourly bars). Does NOT fill them."""
    gaps = []
    open_times = df["_open_time_ms"].to_numpy()
    times_iso = df["time"].to_numpy()
    for i in range(1, len(open_times)):
        diff_ms = int(open_times[i] - open_times[i - 1])
        if diff_ms != INTERVAL_MS:
            missing = diff_ms // INTERVAL_MS - 1
            gaps.append(
                {
                    "start": str(times_iso[i - 1]),
                    "end": str(times_iso[i]),
                    "missing_bars": int(missing),
                }
            )
    return gaps


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    print(f"Fetching {SYMBOL} {INTERVAL} klines from {iso_z(START_TIME)} to most recent closed bar ...")
    rows, now_ms = fetch_all_klines()

    if not rows:
        print("No data fetched.", file=sys.stderr)
        sys.exit(1)

    df = build_dataframe(rows)
    errors = validate(df)
    gaps = find_gaps(df)

    out_df = df[["time", "open", "high", "low", "close", "volume"]]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(CSV_PATH, index=False)

    sha256_hex = sha256_of_file(CSV_PATH)

    meta = {
        "source": f"Binance spot GET {BASE_URL} symbol={SYMBOL} interval={INTERVAL}",
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "fetched_utc": iso_z(datetime.fromtimestamp(now_ms / 1000, tz=timezone.utc)),
        "rows": int(len(out_df)),
        "first_bar": str(out_df["time"].iloc[0]),
        "last_bar": str(out_df["time"].iloc[-1]),
        "gaps": gaps,
        "sha256": sha256_hex,
        "validation_errors": errors,
    }
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(out_df)} rows to {CSV_PATH}")
    print(f"First bar: {meta['first_bar']}   Last bar: {meta['last_bar']}")
    print(f"Gaps found: {len(gaps)}")
    gaps_sorted = sorted(gaps, key=lambda g: g["missing_bars"], reverse=True)
    for g in gaps_sorted[:10]:
        print(f"  gap: {g['start']} -> {g['end']}  ({g['missing_bars']} missing bars)")
    if len(gaps) > 10:
        print(f"  ... and {len(gaps) - 10} more gaps (see meta.json)")
    print(f"sha256: {sha256_hex}")

    if errors:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2)

    print("Validation OK: strictly increasing timestamps, no duplicates, "
          "high>=max(open,close), low<=min(open,close), no NaN, volume>=0.")


if __name__ == "__main__":
    main()
