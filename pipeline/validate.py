"""Validate data/hk_population_master.json — every leaf number must have a sourced parent.

Walks the master JSON. For any dict that contains a numeric "value", "births", "deaths",
or a year-keyed integer, it MUST sit within a subtree that includes a "source" or "_source"
field. Fails build if any such leaf has no traceable source.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MASTER = Path(__file__).resolve().parent.parent / "data" / "hk_population_master.json"

NUMERIC_KEYS_REQUIRING_SOURCE = {
    "value",
    "births",
    "deaths",
    "natural_change",
    "net_out",
    "total",
    "applications_received",
    "applications_approved",
    "estimated_actually_arrived",
    "estimated_actually_arrived_incl_family",
    "cumulative_2021_2025",
    "cumulative_2021_2024_to_UK_CA_AU",
}


def has_source_in_lineage(lineage: list) -> bool:
    for level in lineage:
        if isinstance(level, dict):
            if "source" in level or "_source" in level:
                return True
    return False


def walk(node, lineage: list, path: str, failures: list[str]) -> None:
    if isinstance(node, dict):
        next_lineage = lineage + [node]
        for k, v in node.items():
            if k.startswith("_"):
                continue
            child_path = f"{path}.{k}"
            if k in NUMERIC_KEYS_REQUIRING_SOURCE and isinstance(v, (int, float)):
                if not has_source_in_lineage(next_lineage):
                    failures.append(f"{child_path} = {v}: no source in lineage")
            walk(v, next_lineage, child_path, failures)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, lineage, f"{path}[{i}]", failures)


def main() -> None:
    data = json.loads(MASTER.read_text())
    failures: list[str] = []
    walk(data, [], "$", failures)
    if failures:
        print(f"Validation failed ({len(failures)} unsourced numeric leaves):")
        for f in failures[:20]:
            print(f"  - {f}")
        sys.exit(1)
    print("All numeric leaves in master JSON have sourced lineage")


if __name__ == "__main__":
    main()
