#!/usr/bin/env bash
# Pin a new LegCo source PDF to data/legco_sources/ and remind the user
# to update data/hk_population_master.json with any new numbers.
#
# Usage: scripts/add-legco-source.sh <PaperNo>
# Example: scripts/add-legco-source.sh ISSH33/2025
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <PaperNo>  (e.g. ISSH33/2025)"
  exit 2
fi

PAPER_NO="$1"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$ROOT/data/legco_sources"
mkdir -p "$OUT_DIR"

# Query LegCo RPDB API for the PDF filename
RESP=$(curl -sL --max-time 15 -A "hk-people-movement/0.1" \
  -X POST "https://app7.legco.gov.hk/rpdb/en/api/Search2" \
  -H "Content-Type: application/json" \
  -d "{\"PaperNo\":\"${PAPER_NO%%/*}\",\"Size\":50,\"Page\":1}")

# Try TC first, fall back to EN
FILE=$(echo "$RESP" | python3 -c "
import json, sys
d = json.load(sys.stdin)
want = '${PAPER_NO}'
for p in d.get('data', []):
    if p.get('PaperNo') == want:
        pdfs = p.get('PDFPath', [])
        if pdfs:
            f = pdfs[-1]
            print(f.get('tc') or f.get('en') or '')
            break
")

if [ -z "$FILE" ]; then
  echo "Could not resolve PDF filename for ${PAPER_NO}" >&2
  exit 1
fi

# Year directory inferred from PaperNo /YYYY
YEAR=${PAPER_NO##*/}
URL="https://app7.legco.gov.hk/rpdb/en/uploads/${YEAR}/${PAPER_NO%%[0-9]*}/${FILE}"

echo "Fetching: $URL"
curl -sL --max-time 30 -A "hk-people-movement/0.1" "$URL" -o "$OUT_DIR/$FILE"

if [ "$(stat -f%z "$OUT_DIR/$FILE" 2>/dev/null || stat -c%s "$OUT_DIR/$FILE")" -lt 10000 ]; then
  echo "Downloaded file is suspiciously small (<10KB); aborting." >&2
  rm -f "$OUT_DIR/$FILE"
  exit 1
fi

echo "✓ Pinned $OUT_DIR/$FILE"
echo
echo "Next steps:"
echo "  1. Read the PDF for any new numbers."
echo "  2. Update data/hk_population_master.json — every new number needs a 'source' field."
echo "  3. Run: python3 pipeline/validate.py"
echo "  4. Run: python3 pipeline/parse_legco.py  (spot-check against pinned PDFs)"
echo "  5. Run: python3 pipeline/build_aggregates.py"
