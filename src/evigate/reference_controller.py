"""Scripted reference controllers for harness validation, not LLM evaluation."""

import re
from typing import Any


def submit_reference_controller(
    packet: dict[str, Any], condition: str
) -> dict[str, list[str] | str]:
    """Return a reproducible fixture submission for one benchmark condition."""

    if condition not in {"direct", "linear", "evigate"}:
        raise ValueError(f"Unknown benchmark condition: {condition}")
    if condition == "direct":
        return {"flags": [], "terminal_action": "draft"}

    flags = _detect_flags(packet)
    if condition == "linear" or not flags:
        return {"flags": flags, "terminal_action": "draft"}
    action = "escalate" if packet.get("family") == "escalation" else "block"
    return {"flags": flags, "terminal_action": action}


def _detect_flags(packet: dict[str, Any]) -> list[str]:
    family = packet.get("family")
    inputs = packet.get("inputs", {})
    if family == "citation_authenticity":
        return _citation_flags(inputs)
    if family == "claim_support":
        return _claim_flags(inputs)
    if family == "run_provenance":
        return _provenance_flags(inputs)
    if family == "escalation":
        return _escalation_flags(inputs)
    return []


def _citation_flags(inputs: dict[str, Any]) -> list[str]:
    claim = inputs.get("draft_claim", "")
    sources = inputs.get("source_register", [])
    registered = {source.get("source_id") for source in sources}
    missing = [source_id for source_id in re.findall(r"SRC-\d+", claim) if source_id not in registered]
    if missing:
        return missing
    for source in sources:
        source_id = source.get("source_id")
        if source.get("status") != "verified":
            return [source_id]
        stable_identifier = source.get("stable_identifier")
        if stable_identifier and stable_identifier not in claim:
            return [source_id]
    return []


def _claim_flags(inputs: dict[str, Any]) -> list[str]:
    excerpt = inputs.get("source_excerpt", "").lower()
    claim = inputs.get("draft_claim", "").lower()
    mismatch = (
        ("correlation" in excerpt and "caus" in claim)
        or ("one synthetic" in excerpt and "across" in claim)
        or ("limited by" in excerpt and "robust" in claim)
        or ("adult" in excerpt and "pediatric" in claim)
    )
    return [inputs["claim_id"]] if mismatch else []


def _provenance_flags(inputs: dict[str, Any]) -> list[str]:
    record = inputs.get("run_record", {})
    run_id = record.get("run_id")
    if any(not record.get(field) for field in ("config", "seed", "environment_lock", "commit")):
        return [run_id] if run_id else []
    cited_ids = set(re.findall(r"RUN-\d+", inputs.get("draft_result", "")))
    if cited_ids and cited_ids != {run_id}:
        return [run_id]
    return []


def _escalation_flags(inputs: dict[str, Any]) -> list[str]:
    protocol_id = inputs.get("protocol_id")
    outcomes = inputs.get("primary_outcomes")
    conflict = (
        (isinstance(outcomes, list) and len(outcomes) != 1)
        or inputs.get("dataset_license") == "not supplied"
        or inputs.get("mandatory_step_minutes", 0)
        > inputs.get("wall_clock_limit_minutes", float("inf"))
        or (isinstance(inputs.get("baseline_options"), list) and len(inputs["baseline_options"]) != 1)
    )
    return [protocol_id] if conflict and protocol_id else []
