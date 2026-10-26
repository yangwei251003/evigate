import json
from pathlib import Path

from evigate.validation import (
    validate_claim_links,
    validate_project_state,
    validate_run_manifest,
    validate_source,
    validate_improvement_proposal,
)


def test_project_state_requires_approved_pass_for_later_phase():
    state = {
        "current_phase": "02_protocol",
        "last_completed_phase": {"phase": "01_evidence", "status": "candidate"},
    }

    issues = validate_project_state(state)

    assert {issue.code for issue in issues} == {
        "STATE-PASS-REQUIRED",
        "STATE-APPROVAL-COMMIT-REQUIRED",
        "STATE-PASS-FILE-REQUIRED",
    }


def test_verified_source_requires_a_stable_id_and_authoritative_locator():
    issues = validate_source({"status": "verified"})

    assert [issue.code for issue in issues] == [
        "SOURCE-ID-REQUIRED",
        "SOURCE-LOCATOR-REQUIRED",
    ]


def test_run_manifest_requires_provenance_before_execution():
    issues = validate_run_manifest({"run_id": "RUN-001"})

    assert {issue.code for issue in issues} >= {
        "RUN-CONFIG-REQUIRED",
        "RUN-SEED-REQUIRED",
        "RUN-ENV-REQUIRED",
        "RUN-COMMIT-REQUIRED",
    }


def test_quantitative_claim_requires_evidence_and_registered_run():
    links = [
        {
            "claim_id": "CLAIM-001",
            "kind": "measured",
            "source_ids": [],
            "run_ids": [],
        }
    ]

    issues = validate_claim_links(links, run_ids={"RUN-001"}, source_ids={"SRC-001"})

    assert {issue.code for issue in issues} == {
        "CLAIM-EVIDENCE-REQUIRED",
        "CLAIM-RUN-REQUIRED",
    }


def test_improvement_proposal_requires_evidence_benefit_risk_and_validation():
    proposal = {"proposal_id": "IMP-001", "status": "proposed"}

    issues = validate_improvement_proposal(proposal, artifact_ids={"RUN-001"})

    assert {issue.code for issue in issues} == {
        "IMPROVEMENT-OBSERVATION-REQUIRED",
        "IMPROVEMENT-BENEFIT-REQUIRED",
        "IMPROVEMENT-RISK-REQUIRED",
        "IMPROVEMENT-VALIDATION-REQUIRED",
    }


def test_all_shipped_templates_validate():
    template_dir = Path("skills/evigate-research-orchestrator/templates")
    project_state = json.loads((template_dir / "project-state.json").read_text())
    source = json.loads((template_dir / "source-record.json").read_text())
    manifest = json.loads((template_dir / "run-manifest.json").read_text())
    links = json.loads((template_dir / "claim-links.json").read_text())
    proposal = json.loads((template_dir / "improvement-proposal.json").read_text())

    assert validate_project_state(project_state) == []
    assert validate_source(source) == []
    assert validate_run_manifest(manifest) == []
    assert validate_claim_links(links, {"RUN-001"}, {"SRC-001"}) == []
    assert validate_improvement_proposal(proposal, {"RUN-001"}) == []
