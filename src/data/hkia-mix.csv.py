"""Observable Framework data loader — emit HKIA destination mix CSV."""

import sys
from pathlib import Path

src = Path(__file__).resolve().parent.parent.parent / "data" / "hkia_destination_mix_91d.csv"
sys.stdout.write(src.read_text())
