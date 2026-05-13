"""Fetch IMMD daily passenger traffic CSV, sort rows, write to data/.

Same upstream as atseed.co. Output is diff-stable (sorted).
"""

from __future__ import annotations

import csv
import io
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

URL = (
    "https://www.immd.gov.hk/opendata/eng/transport/immigration_clearance/"
    "statistics_on_daily_passenger_traffic.csv"
)
OUT = Path(__file__).resolve().parent.parent / "data" / "immd_daily_passenger_traffic_2021_2025.csv"
EXPECTED_HEADERS = [
    "Date",
    "Control Point",
    "Arrival / Departure",
    "Hong Kong Residents",
    "Mainland Visitors",
    "Other Visitors",
    "Total",
]


def fetch(retries: int = 3, backoff: float = 2.0) -> bytes:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            r = requests.get(URL, timeout=60, headers={"User-Agent": "hk-people-movement/0.1"})
            r.raise_for_status()
            return r.content
        except Exception as exc:  # noqa: BLE001 — surface anything to caller after retries
            last_exc = exc
            if attempt + 1 < retries:
                time.sleep(backoff * (2**attempt))
    raise RuntimeError(f"IMMD fetch failed after {retries} retries: {last_exc}")


def main() -> None:
    raw = fetch().decode("utf-8-sig")
    reader = csv.reader(io.StringIO(raw))
    rows = list(reader)
    if not rows:
        sys.exit("IMMD CSV is empty")
    header = [h.strip() for h in rows[0] if h.strip()]
    if header[: len(EXPECTED_HEADERS)] != EXPECTED_HEADERS:
        sys.exit(f"IMMD CSV header mismatch.\n got: {header}\n want: {EXPECTED_HEADERS}")

    body = [r for r in rows[1:] if any(c.strip() for c in r)]

    def sortkey(r: list[str]) -> tuple:
        try:
            dt = datetime.strptime(r[0], "%d-%m-%Y")
        except ValueError:
            dt = datetime.min
        return (dt, r[1], r[2])

    body.sort(key=sortkey)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(EXPECTED_HEADERS + [""])
        for r in body:
            w.writerow(r)
    print(f"Wrote {OUT.relative_to(OUT.parent.parent)} ({len(body):,} rows)")


if __name__ == "__main__":
    main()
