"""Observable Framework data loader — emit GBA land per-checkpoint CSV.

Translates IMMD's English control point names into Traditional Chinese so the
chart axis matches the prose. Source data stays in English for traceability.
"""

import sys
from pathlib import Path

NAMES = {
    "Express Rail Link West Kowloon": "高鐵西九龍",
    "Heung Yuen Wai": "香園圍",
    "Hong Kong-Zhuhai-Macao Bridge": "港珠澳大橋",
    "Lo Wu": "羅湖",
    "Lok Ma Chau": "落馬洲",
    "Lok Ma Chau Spur Line": "落馬洲支線",
    "Man Kam To": "文錦渡",
    "Shenzhen Bay": "深圳灣",
}

src = Path(__file__).resolve().parent.parent.parent / "data" / "gba_land_hk_resident_annual.csv"
text = src.read_text()
for en, zh in NAMES.items():
    text = text.replace(f",{en},", f",{zh},")
sys.stdout.write(text)
