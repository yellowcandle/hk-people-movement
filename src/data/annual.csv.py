"""Observable Framework data loader — emit annual accounting CSV to stdout."""

import sys
from pathlib import Path

src = Path(__file__).resolve().parent.parent.parent / "data" / "hk_annual_population_accounting.csv"
sys.stdout.write(src.read_text())
