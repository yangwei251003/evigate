"""Pure validators for evidence-gated research artifacts."""

from typing import Any

from .models import Issue


def validate_project_state(state: dict[str, Any]) -> list[Issue]:
    """Require a recorded approved pass before a project enters later phases."""

    if state.get("current_phase") == "00_skill_design":
        return []

    completed = state.get("last_completed_phase") or {}
    issues: list[Issue] = []
    if completed.get("status") != "passed":
        issues.append(
            Issue(
                "STATE-PASS-REQUIRED",
                "Later phases require a human-approved PASS record.",
            )
        )
    if not completed.get("approved_commit"):
        issues.append(
            Issue(
                "STATE-APPROVAL-COMMIT-REQUIRED",
                "PASS record must name its approved commit.",
            )
        )
    if not completed.get("pass_file"):
        issues.append(
            Issue("STATE-PASS-FILE-REQUIRED", "PASS record path is required.")
        )
    return issues


def validate_source(source: dict[str, Any]) -> list[Issue]:
    """Validate the minimum provenance required for a scholarly source."""

    issues: list[Issue] = []
    if not source.get("source_id"):
        issues.append(Issue("SOURCE-ID-REQUIRED", "source_id is required."))
    if source.get("status") == "verified" and not source.get("locator"):
        issues.append(
            Issue(
                "SOURCE-LOCATOR-REQUIRED",
                "A verified source requires an authoritative locator.",
            )
        )
    return issues


def validate_run_manifest(manifest: dict[str, Any]) -> list[Issue]:
    """Validate provenance that must exist before an experiment can run."""

    requirements = (
        ("config", "RUN-CONFIG-REQUIRED", "A run configuration is required."),
        ("seed", "RUN-SEED-REQUIRED", "A random seed is required."),
        (
            "environment_lock",
            "RUN-ENV-REQUIRED",
            "An environment lock identifier is required.",
        ),
        ("commit", "RUN-COMMIT-REQUIRED", "A Git commit identifier is required."),
    )
    return [
        Issue(code, message)
        for field, code, message in requirements
        if not manifest.get(field)
    ]


def validate_claim_links(
    links: list[dict[str, Any]],
    run_ids: set[str],
    source_ids: set[str],
) -> list[Issue]:
    """Require source and run provenance for manuscript claims."""

    issues: list[Issue] = []
    for link in links:
        linked_source_ids = set(link.get("source_ids", []))
        linked_run_ids = set(link.get("run_ids", []))
        if not linked_source_ids:
            issues.append(
                Issue(
                    "CLAIM-EVIDENCE-REQUIRED",
                    "Claim requires at least one verified Source ID.",
                )
            )
        elif not linked_source_ids <= source_ids:
            issues.append(
                Issue(
                    "CLAIM-EVIDENCE-UNKNOWN",
                    "Claim references an unknown Source ID.",
                )
            )
        if link.get("kind") in {"measured", "simulated"}:
            if not linked_run_ids:
                issues.append(
                    Issue(
                        "CLAIM-RUN-REQUIRED",
                        "Quantitative claim requires a registered Run ID.",
                    )
                )
            elif not linked_run_ids <= run_ids:
                issues.append(
                    Issue(
                        "CLAIM-RUN-UNKNOWN",
                        "Claim references an unknown Run ID.",
                    )
                )
    return issues


def validate_improvement_proposal(
    proposal: dict[str, Any], artifact_ids: set[str]
) -> list[Issue]:
    """Validate a proposal without accepting, applying, or deleting it."""

    issues: list[Issue] = []
    if proposal.get("observed_artifact_id") not in artifact_ids:
        issues.append(
            Issue(
                "IMPROVEMENT-OBSERVATION-REQUIRED",
                "Proposal requires a registered observation artifact.",
            )
        )
    requirements = (
        (
            "expected_benefit",
            "IMPROVEMENT-BENEFIT-REQUIRED",
            "Proposal requires an expected benefit.",
        ),
        ("risk", "IMPROVEMENT-RISK-REQUIRED", "Proposal requires a risk statement."),
        (
            "validation",
            "IMPROVEMENT-VALIDATION-REQUIRED",
            "Proposal requires a validation method.",
        ),
    )
    issues.extend(
        Issue(code, message)
        for field, code, message in requirements
        if not proposal.get(field)
    )
    if proposal.get("touches_frozen_material") and not proposal.get("amendment_id"):
        issues.append(
            Issue(
                "IMPROVEMENT-AMENDMENT-REQUIRED",
                "Frozen-material proposal requires a protocol amendment ID.",
            )
        )
    if proposal.get("status") == "accepted" and not proposal.get("approval"):
        issues.append(
            Issue(
                "IMPROVEMENT-APPROVAL-REQUIRED",
                "Accepted proposal requires an explicit approval record.",
            )
        )
    return issues
