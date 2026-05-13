"""Subset a display CJK font to only the characters used in dashboard headings.

Supports two source fonts:

  --source metrosung   (default)   ~/Library/Fonts/MetroSung_v1.0_FinalVersion.otf
                                   PROPRIETARY — verify the EULA before redistributing
                                   a subsetted WOFF in a public deploy.

  --source noto                    Noto Serif TC (SIL Open Font License)
                                   Auto-downloads to ~/.cache/hk-people-movement/
                                   if missing. Safe to redistribute.

Output goes to src/static/fonts/<name>-subset.{woff2,woff}. Same character set
(DISPLAY_STRINGS below) is used regardless of source font.

Run:
  python3 pipeline/subset_font.py                # MetroSung
  python3 pipeline/subset_font.py --source noto  # Noto Serif TC

After running with --source noto, update observablehq.config.js's @font-face
src to point at NotoSerifTC-subset.{woff2,woff} and rename the font-family if
needed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "src" / "static" / "fonts"
TXT_FILE = ROOT / "pipeline" / ".display-chars.txt"
CACHE_DIR = Path.home() / ".cache" / "hk-people-movement"

NOTO_URL = (
    "https://raw.githubusercontent.com/notofonts/noto-cjk/main/"
    "Serif/OTF/TraditionalChinese/NotoSerifCJKtc-Bold.otf"
)
NOTO_LICENSE_URL = (
    "https://github.com/notofonts/noto-cjk/blob/main/Serif/LICENSE"
)

SOURCES = {
    "metrosung": {
        "path": Path.home() / "Library/Fonts/MetroSung_v1.0_FinalVersion.otf",
        "output_name": "MetroSung-subset",
        "family": "MetroSung",
        "license": "Proprietary (verify EULA before public web deploy)",
        "url": None,
    },
    "noto": {
        "path": CACHE_DIR / "NotoSerifTC-Bold.otf",
        "output_name": "NotoSerifTC-subset",
        "family": "Noto Serif TC",
        "license": "SIL Open Font License 1.1",
        "url": NOTO_URL,
    },
}

# Every string the dashboard sets to the display font. Order doesn't matter.
DISPLAY_STRINGS = [
    # Brand / nav
    "香港人口流動",
    "數據實際上講緊咩",
    "方法論",
    # Artboard 01 — Landing
    "機場數據冇話畀你聽嘅移民真相。",
    "點解要做呢個 dashboard",
    "同 C&SD 恆等式矛盾",
    "漏咗主要入境通道",
    "組合變化扭曲走勢",
    "六章圖表",
    "人口恆等式",
    "空運 vs 統計處",
    "機場目的地",
    "大灣區陸路",
    "人才與移居",
    "必讀",
    "真正去咗邊",
    # Artboard 02 — Identity
    "人口係加減出嚟嘅，唔係望飛機嚟估嘅。",
    "每年人口變化分解",
    "實例：2022 → 2023",
    "點解重要",
    "其他",
    # Artboard 03 — Airport vs C&SD
    "同一個香港、同一啲年份，兩條線講緊兩個故事。",
    "兩條 series 並排",
    "3 年累計 · 差距 53 萬人，方向相反",
    "點解差距咁大",
    "短途來回唔完全抵銷",
    "高才通入境唔計港人",
    "回流醫病算「入境」",
    "陸路移居完全略咗",
    # Artboard 04 — Methodology
    "數據係咩、唔係咩、邊個來源、有咩 caveat。",
    "統計處點計人口",
    "已知 caveat",
    '2024 嘅「其他淨遷移」未計算到',
    "年中人口會修訂",
    "HKIA flight API 只保留 ~91 日",
    "高才通累計 ≠ 現時 stock",
    "內地港人 stock 係 2020 普查數字",
    "畀番原作者嘅好評",
    "所有來源",
    # Destination stats
    "想去但仲未去到嘅人，仲有 25,530。",
    # Heading-level punctuation
    "，。「」、·：；！？（）— — …",
    # Numerics in headings
    "+−×÷=≠≈",
    "0123456789",
    # Latin used in headings ("C&SD", "dashboard", "vs", "series", "caveat", "API", "stock")
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "&",
    # Safety margin
    "走勢趨上升下降流入流出簽證護照計劃年度月度季度報告",
]


def collect_chars() -> str:
    seen: dict[str, None] = {}
    for s in DISPLAY_STRINGS:
        for ch in s:
            if ch == " ":
                continue
            seen.setdefault(ch, None)
    return "".join(seen.keys())


def ensure_source(source: str) -> Path:
    spec = SOURCES[source]
    path = spec["path"]
    if path.exists():
        return path
    if spec["url"] is None:
        sys.exit(f"ERROR: source font not found at {path} and no download URL configured.")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {source} ({spec['url']}) → {path} ...")
    urlretrieve(spec["url"], str(path))
    sz = path.stat().st_size
    print(f"  Downloaded {sz/1024/1024:.1f} MB")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=list(SOURCES.keys()), default="metrosung")
    args = parser.parse_args()

    spec = SOURCES[args.source]
    src_font = ensure_source(args.source)

    chars = collect_chars()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TXT_FILE.write_text(chars, encoding="utf-8")
    print(f"Collected {len(chars)} unique characters → {TXT_FILE.relative_to(ROOT)}")

    out_woff2 = OUT_DIR / f"{spec['output_name']}.woff2"
    out_woff = OUT_DIR / f"{spec['output_name']}.woff"

    common_args = [
        "pyftsubset",
        str(src_font),
        f"--text-file={TXT_FILE}",
        "--no-hinting",
        "--desubroutinize",
        "--layout-features=*",
        "--name-IDs=*",
        "--notdef-glyph",
        "--no-notdef-outline",
        "--no-recalc-bounds",
        "--no-recalc-timestamp",
    ]

    r = subprocess.run([*common_args, "--flavor=woff2", f"--output-file={out_woff2}"], check=False)
    if r.returncode != 0:
        return r.returncode
    subprocess.run([*common_args, "--flavor=woff", f"--output-file={out_woff}"], check=False)

    sz_w2 = out_woff2.stat().st_size
    sz_w = out_woff.stat().st_size if out_woff.exists() else 0
    sz_src = src_font.stat().st_size

    print(
        f"\nSubsetted '{spec['family']}' ({args.source}):\n"
        f"  License    : {spec['license']}\n"
        f"  Source     : {sz_src/1024:.1f} KB ({sz_src:,} B)\n"
        f"  WOFF2      : {sz_w2/1024:.1f} KB ({sz_w2:,} B)  → {out_woff2.relative_to(ROOT)}\n"
        f"  WOFF       : {sz_w/1024:.1f} KB ({sz_w:,} B)  → {out_woff.relative_to(ROOT)}\n"
        f"  Compression: {sz_src/sz_w2:.0f}×"
    )

    print(
        f"\nTo activate, update observablehq.config.js head injection:\n"
        f'  font-family: "{spec["family"]}";\n'
        f'  src: url("/static/fonts/{spec["output_name"]}.woff2") format("woff2"),\n'
        f'       url("/static/fonts/{spec["output_name"]}.woff") format("woff");\n'
        f"And update --font-display stack in src/style.css to lead with \"{spec['family']}\"."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
