"""Derived analysis for committed formal benchmark records."""

from collections import defaultdict
from typing import Any


def aggregate_by_condition(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Aggregate only supplied raw records while retaining their Run IDs."""

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["manifest"]["condition"]].append(record)
    summary: dict[str, dict[str, Any]] = {}
    for condition in sorted(grouped):
        group = grouped[condition]
        count = len(group)
        summary[condition] = {
            "n": count,
            "run_ids": sorted(record["manifest"]["run_id"] for record in group),
            "detection_rate": sum(record["score"]["detection"] for record in group)
            / count,
            "containment_rate": sum(record["score"]["containment"] for record in group)
            / count,
            "unsafe_continuation_rate": sum(
                record["score"]["unsafe_continuation"] for record in group
            )
            / count,
        }
    return summary
