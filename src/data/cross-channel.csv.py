"""Observable Framework data loader — emit cross-channel comparison CSV."""

import sys
from pathlib import Path

src = Path(__file__).resolve().parent.parent.parent / "data" / "cross_channel_net_outflow_annual.csv"
sys.stdout.write(src.read_text())
