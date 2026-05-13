"""Derive aggregated CSVs under data/ from primary sources.

Reads:
  - data/hk_population_master.json (hand-curated)
  - data/immd_daily_passenger_traffic_2021_2025.csv
  - data/hkia_91d/*.json
  - data/legco_sources/openflights_airports.dat (optional; falls back to inline patches)

Writes:
  - data/hk_annual_population_accounting.csv
  - data/gba_land_hk_resident_annual.csv
  - data/cross_channel_net_outflow_annual.csv
  - data/hkia_destination_mix_91d.csv
"""

from __future__ import annotations

import collections
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MASTER = DATA / "hk_population_master.json"
IMMD = DATA / "immd_daily_passenger_traffic_2021_2025.csv"
HKIA_DIR = DATA / "hkia_91d"
OPENFLIGHTS = DATA / "legco_sources" / "openflights_airports.dat"

GBA_LAND_POINTS = [
    "Express Rail Link West Kowloon",
    "Heung Yuen Wai",
    "Hong Kong-Zhuhai-Macao Bridge",
    "Lo Wu",
    "Lok Ma Chau",
    "Lok Ma Chau Spur Line",
    "Man Kam To",
    "Shenzhen Bay",
]


# Region classifier — same as the hand analysis. Keep in sync with src/data/ pages.
TAIWAN_IATA = {
    "TPE", "TSA", "KHH", "RMQ", "TNN", "TTT", "HUN", "MZG", "KNH", "MFK",
    "LZN", "GNI", "CMJ", "KYD", "WOT", "HCN",
}
MAINLAND_IATA_PATCH = {"TFU", "INC", "PKX", "HFE"}


def region_of(country: str | None, iata: str) -> str:
    if iata in TAIWAN_IATA:
        return "Taiwan"
    if iata == "MFM":
        return "Macau"
    if iata == "HKG":
        return "Hong Kong"
    if iata in MAINLAND_IATA_PATCH or country == "China":
        return "Mainland China"
    if country == "Japan":
        return "Japan"
    if country == "South Korea":
        return "South Korea"
    if country in {"Thailand", "Singapore", "Philippines", "Malaysia", "Vietnam",
                   "Indonesia", "Cambodia", "Laos", "Myanmar", "Brunei", "Timor-Leste"}:
        return "SE Asia"
    if country in {"United Kingdom", "Ireland"}:
        return "UK/Ireland"
    if country == "Canada":
        return "Canada"
    if country in {"Australia", "New Zealand", "Fiji", "Papua New Guinea",
                   "Palau", "Northern Mariana Islands"}:
        return "Australia/NZ/Pacific"
    if country == "United States":
        return "USA"
    if country in {"India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal",
                   "Bhutan", "Maldives"}:
        return "South Asia"
    if country in {"United Arab Emirates", "Qatar", "Saudi Arabia", "Bahrain",
                   "Kuwait", "Oman", "Iran", "Iraq", "Turkey", "Israel",
                   "Jordan", "Lebanon", "Uzbekistan", "Kazakhstan"}:
        return "Middle East/CAsia"
    if country in {"France", "Germany", "Netherlands", "Italy", "Spain",
                   "Switzerland", "Belgium", "Austria", "Sweden", "Norway",
                   "Denmark", "Finland", "Poland", "Portugal", "Greece",
                   "Hungary", "Czech Republic", "Russia", "Mongolia"}:
        return "Europe/Mongolia"
    if country in {"Ethiopia", "Egypt", "South Africa", "Kenya", "Mauritius",
                   "Morocco", "Tanzania", "Nigeria", "Tunisia"}:
        return "Africa"
    if country in {"Brazil", "Argentina", "Chile", "Peru", "Mexico", "Colombia"}:
        return "Latin America"
    return "Other"


def load_iata_country() -> dict[str, str]:
    table: dict[str, str] = {}
    if not OPENFLIGHTS.exists():
        return table
    with OPENFLIGHTS.open(encoding="utf-8") as f:
        for row in csv.reader(f, quotechar='"'):
            if len(row) >= 5 and row[4] and row[4] != "\\N":
                table[row[4]] = row[3]
    return table


def annual_accounting(master: dict) -> list[dict]:
    pop = master["midyear_population"]
    vital = master["vital_statistics"]
    owp = master["one_way_permit_arrivals"]
    air = master["atseed_co_airport_net"]
    talent = master["talent_admission_schemes_approved"]["annual_breakdown"]

    rows: list[dict] = []
    year_keys = [y for y in list(pop.keys()) + list(vital.keys()) if not y.startswith("_") and y.isdigit()]
    years = sorted({int(y) for y in year_keys})
    pop_by_year = {int(y): pop[y].get("value") for y in pop if not y.startswith("_") and y.isdigit()}
    for y in years:
        ys = str(y)
        midpop = pop_by_year.get(y)
        v = vital.get(ys, {})
        natchg = v.get("natural_change")
        owp_val = owp.get(ys) if isinstance(owp.get(ys), int) else None
        air_net = air.get(ys, {}).get("net_out")
        tt = talent.get(ys, {})
        prev_pop = pop_by_year.get(y - 1)  # only compute YoY when previous year is consecutive
        yoy = midpop - prev_pop if (midpop is not None and prev_pop is not None) else None
        netmv = (yoy - natchg) if (yoy is not None and natchg is not None) else None
        other = (netmv - owp_val) if (netmv is not None and owp_val is not None) else None
        rows.append({
            "year": y,
            "midyear_pop": midpop,
            "natural_change": natchg,
            "owp_arrivals": owp_val,
            "yoy_pop_change": yoy,
            "net_movement": netmv,
            "other_net_migration": other,
            "atseed_airport_hk_net_out": air_net,
            "top_talent_approved": tt.get("top_talent"),
            "total_talent_approved": tt.get("total"),
        })
    return rows


def gba_land(immd_path: Path) -> tuple[list[dict], list[dict]]:
    annual = collections.defaultdict(lambda: {"a": 0, "d": 0})
    air_annual = collections.defaultdict(lambda: {"a": 0, "d": 0})
    with immd_path.open(encoding="utf-8") as f:
        r = csv.reader(f)
        next(r)
        for row in r:
            if len(row) < 5:
                continue
            try:
                hk = int(row[3])
                dt = datetime.strptime(row[0], "%d-%m-%Y")
            except ValueError:
                continue
            cp = row[1]
            ad = row[2]
            key_dir = "a" if ad == "Arrival" else "d"
            if cp == "Airport":
                air_annual[dt.year][key_dir] += hk
            elif cp in GBA_LAND_POINTS:
                annual[(dt.year, cp)][key_dir] += hk

    per_cp = [
        {
            "year": y,
            "control_point": cp,
            "hk_arrivals": v["a"],
            "hk_departures": v["d"],
            "net_out": v["d"] - v["a"],
        }
        for (y, cp), v in sorted(annual.items())
    ]

    agg = collections.defaultdict(lambda: {"a": 0, "d": 0})
    for (y, _), v in annual.items():
        agg[y]["a"] += v["a"]
        agg[y]["d"] += v["d"]

    cross = []
    for y in sorted(set(list(agg.keys()) + list(air_annual.keys()))):
        air_net = air_annual[y]["d"] - air_annual[y]["a"]
        land_net = agg[y]["d"] - agg[y]["a"]
        cross.append({
            "year": y,
            "airport_net_out": air_net,
            "land_net_out": land_net,
            "combined_net_out": air_net + land_net,
        })
    return per_cp, cross


def hkia_mix(window_dir: Path, iata_country: dict[str, str]) -> list[dict]:
    region_totals: collections.Counter = collections.Counter()
    for p in sorted(window_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        for day in data or []:
            for flight in day.get("list", []):
                for dest in flight.get("destination", []) or []:
                    country = iata_country.get(dest)
                    region_totals[region_of(country, dest)] += 1

    total = sum(region_totals.values()) or 1
    return [
        {
            "region": r,
            "operations": c,
            "share_pct": round(100 * c / total, 2),
        }
        for r, c in region_totals.most_common()
    ]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> None:
    if not MASTER.exists():
        sys.exit(f"Missing {MASTER}")
    master = json.loads(MASTER.read_text())

    write_csv(
        DATA / "hk_annual_population_accounting.csv",
        annual_accounting(master),
        [
            "year",
            "midyear_pop",
            "natural_change",
            "owp_arrivals",
            "yoy_pop_change",
            "net_movement",
            "other_net_migration",
            "atseed_airport_hk_net_out",
            "top_talent_approved",
            "total_talent_approved",
        ],
    )

    if IMMD.exists():
        per_cp, cross = gba_land(IMMD)
        write_csv(
            DATA / "gba_land_hk_resident_annual.csv",
            per_cp,
            ["year", "control_point", "hk_arrivals", "hk_departures", "net_out"],
        )
        write_csv(
            DATA / "cross_channel_net_outflow_annual.csv",
            cross,
            ["year", "airport_net_out", "land_net_out", "combined_net_out"],
        )
    else:
        print(f"Skipped GBA/cross-channel: {IMMD} not found (run fetch_immd first)")

    iata_country = load_iata_country()
    if HKIA_DIR.exists() and iata_country:
        write_csv(
            DATA / "hkia_destination_mix_91d.csv",
            hkia_mix(HKIA_DIR, iata_country),
            ["region", "operations", "share_pct"],
        )
    else:
        print(f"Skipped HKIA mix: need {HKIA_DIR} and {OPENFLIGHTS}")

    print("Aggregates rebuilt")


if __name__ == "__main__":
    main()
