"""Pure validation for frozen benchmark records."""

from pathlib import Path
from typing import Any

from .benchmark_models import BenchmarkIssue

KNOWN_DEFECTS = {
    "citation_authenticity",
    "claim_support",
    "run_provenance",
    "escalation",
}


def finding(code: str, message: str) -> BenchmarkIssue:
    """Create a stable diagnostic."""

    return BenchmarkIssue(code=code, message=message)


def validate_packet(packet: dict[str, Any]) -> list[BenchmarkIssue]:
    """Validate the minimum agent-visible task-packet contract."""

    results: list[BenchmarkIssue] = []
    schema_version = packet.get("schema_version")
    if schema_version not in {1, 2}:
        results.append(
            finding(
                "BENCHMARK-PACKET-SCHEMA-REQUIRED",
                "Packet schema_version must be 1 or 2.",
            )
        )
    if packet.get("family") not in KNOWN_DEFECTS:
        results.append(
            finding("BENCHMARK-PACKET-FAMILY-REQUIRED", "Packet family must be known.")
        )
    if schema_version in {None, 1} and packet.get("primary_defect") not in KNOWN_DEFECTS:
        results.append(
            finding(
                "BENCHMARK-PACKET-DEFECT-INVALID",
                "Packet primary_defect must be known.",
            )
        )
    inputs = packet.get("inputs")
    if schema_version == 2 and (
        "primary_defect" in packet
        or (isinstance(inputs, dict) and "defect_token" in inputs)
    ):
        results.append(
            finding(
                "BENCHMARK-PACKET-LEAKS-DEFECT",
                "Version-2 packets must not expose a primary defect or defect token.",
            )
        )
    if not isinstance(packet.get("inputs"), dict):
        results.append(
            finding("BENCHMARK-PACKET-INPUTS-REQUIRED", "Packet inputs must be an object.")
        )
    if not isinstance(packet.get("allowed_actions"), list) or not packet["allowed_actions"]:
        results.append(
            finding(
                "BENCHMARK-PACKET-ACTIONS-REQUIRED",
                "Packet allowed_actions must be non-empty.",
            )
        )
    return results


def validate_answer_key(key: dict[str, Any], packet_id: str) -> list[BenchmarkIssue]:
    """Ensure a scorer-only answer key matches its packet and outcomes."""

    required = {
        "detection": "BENCHMARK-KEY-DETECTION-REQUIRED",
        "containment": "BENCHMARK-KEY-CONTAINMENT-REQUIRED",
        "unsafe_continuation": "BENCHMARK-KEY-UNSAFE-REQUIRED",
    }
    results = [
        finding(code, f"Answer key requires {field}.")
        for field, code in required.items()
        if field not in key
    ]
    if key.get("task_id") != packet_id:
        results.insert(
            0,
            finding(
                "BENCHMARK-KEY-TASK-MISMATCH",
                "Answer key must match packet task_id.",
            ),
        )
    return results


def validate_execution_manifest(manifest: dict[str, Any]) -> list[BenchmarkIssue]:
    """Refuse to begin a benchmark run without its provenance and budget."""

    required = {
        "task_id": "BENCHMARK-MANIFEST-TASK-REQUIRED",
        "condition": "BENCHMARK-MANIFEST-CONDITION-REQUIRED",
        "seed": "BENCHMARK-MANIFEST-SEED-REQUIRED",
        "runtime": "BENCHMARK-MANIFEST-RUNTIME-REQUIRED",
        "commit": "BENCHMARK-MANIFEST-COMMIT-REQUIRED",
        "environment_lock": "BENCHMARK-MANIFEST-ENV-REQUIRED",
        "budget": "BENCHMARK-MANIFEST-BUDGET-REQUIRED",
        "stop_condition": "BENCHMARK-MANIFEST-STOP-REQUIRED",
    }
    results = [
        finding(code, f"Execution manifest requires {field}.")
        for field, code in required.items()
        if not manifest.get(field)
    ]
    if manifest.get("output_path") and Path(manifest["output_path"]).exists():
        results.append(
            finding("BENCHMARK-OUTPUT-EXISTS", "Execution output path already exists.")
        )
    return results
