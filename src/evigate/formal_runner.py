"""Formal execution for the deterministic reference-controller simulation."""

import json
from pathlib import Path
from typing import Any

from .benchmark_io import write_new_json
from .benchmark_validation import validate_answer_key, validate_execution_manifest, validate_packet
from .reference_controller import submit_reference_controller
from .scoring import score_submission


def execute_reference_run(
    manifest: dict[str, Any], packet_path: Path, key_path: Path
) -> dict[str, Any]:
    """Execute one pre-registered reference run and write a new raw artifact."""

    issues = validate_execution_manifest(manifest)
    if issues:
        raise ValueError([issue.code for issue in issues])
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    key = json.loads(key_path.read_text(encoding="utf-8"))
    packet_issues = validate_packet(packet)
    key_issues = validate_answer_key(key, packet.get("task_id", ""))
    if packet_issues or key_issues:
        raise ValueError(
            [issue.code for issue in [*packet_issues, *key_issues]]
        )
    if manifest["task_id"] != packet["task_id"]:
        raise ValueError("BENCHMARK-MANIFEST-TASK-MISMATCH")
    submission = submit_reference_controller(packet, manifest["condition"])
    record = {
        "manifest": manifest,
        "submission": submission,
        "score": score_submission(manifest["run_id"], key, submission),
    }
    write_new_json(Path(manifest["output_path"]), record)
    return record
