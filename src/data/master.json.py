"""Observable Framework data loader — emit master JSON (sources + meta)."""

import sys
from pathlib import Path

src = Path(__file__).resolve().parent.parent.parent / "data" / "hk_population_master.json"
sys.stdout.write(src.read_text())
