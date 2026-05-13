"""Maintain rolling 91-day window of HKIA outbound flight JSON under data/hkia_91d/.

API: hongkongairport.com flight info REST. Retention is ~91 days.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

URL_TEMPLATE = (
    "https://www.hongkongairport.com/flightinfo-rest/rest/flights/past?"
    "date={date}&lang=en&cargo=false&arrival=false"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "hkia_91d"
WINDOW_DAYS = 91


def fetch_day(date_str: str, retries: int = 3, backoff: float = 2.0) -> bytes:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            r = requests.get(
                URL_TEMPLATE.format(date=date_str),
                timeout=20,
                headers={"User-Agent": "hk-people-movement/0.1"},
            )
            r.raise_for_status()
            return r.content
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt + 1 < retries:
                time.sleep(backoff * (2**attempt))
    raise RuntimeError(f"HKIA fetch failed for {date_str} after {retries} retries: {last_exc}")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date()
    expected_days = {today - timedelta(days=i) for i in range(WINDOW_DAYS)}

    # Add missing days
    added = 0
    for d in sorted(expected_days):
        f = OUT_DIR / f"{d.isoformat()}.json"
        if f.exists():
            continue
        body = fetch_day(d.isoformat())
        f.write_bytes(body)
        added += 1

    # Prune old days
    pruned = 0
    expected_filenames = {f"{d.isoformat()}.json" for d in expected_days}
    for p in OUT_DIR.iterdir():
        if p.is_file() and p.name not in expected_filenames:
            p.unlink()
            pruned += 1

    print(f"HKIA window: added {added} day(s), pruned {pruned} old file(s), {WINDOW_DAYS} total")


if __name__ == "__main__":
    main()
