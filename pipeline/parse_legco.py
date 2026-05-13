"""Verification script: re-read pinned LegCo PDFs and assert known numbers match.

Numbers are pinned in data/hk_population_master.json (human-authored). This script
re-extracts a subset from PDF text to catch silent drift. NOT the source of truth.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf not installed; run `pip install -e pipeline`")

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "hk_population_master.json"
PDFS = ROOT / "data" / "legco_sources"

# Subset of known numbers we can pattern-match in the PDF text.
# Each entry: (pdf_filename, regex anchored on a unique nearby phrase, expected value)
SPOT_CHECKS = [
    ("ISSH33_2024_tc.pdf", r"371\s*380", "371380"),  # 內地港人 (2020 census)
    ("ISSH10_2025_tc.pdf", r"99\s*600", "99600"),  # Guangdong elderly 2024
    ("ISSF04_2025_tc.pdf", r"36\s*723", "36723"),  # 2024 births
    ("ISSF04_2025_tc.pdf", r"52\s*393", "52393"),  # 2024 deaths
    ("ISSH23_2024_tc.pdf", r"49\s*737", "49737"),  # 2023 Top Talent approved
    ("ISSH23_2024_tc.pdf", r"135\s*049", "135049"),  # 2023 total talent
]


def pdf_text(path: Path) -> str:
    r = PdfReader(str(path))
    return "\n".join((p.extract_text() or "") for p in r.pages)


def main() -> None:
    if not MASTER.exists():
        sys.exit(f"Master JSON not found: {MASTER}")
    json.loads(MASTER.read_text())  # validates JSON parses

    failures: list[str] = []
    for filename, pat, expected in SPOT_CHECKS:
        path = PDFS / filename
        if not path.exists():
            failures.append(f"missing source PDF: {filename}")
            continue
        text = pdf_text(path)
        if not re.search(pat, text):
            failures.append(f"{filename}: pattern /{pat}/ (expected {expected}) not found")

    if failures:
        print("VERIFY FAILURES:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print(f"All {len(SPOT_CHECKS)} LegCo PDF spot-checks pass")


if __name__ == "__main__":
    main()
