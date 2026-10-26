import json
import subprocess
import sys


def test_validate_source_returns_nonzero_for_an_unverifiable_record(tmp_path):
    record = tmp_path / "source.json"
    record.write_text(json.dumps({"status": "verified"}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "evigate.cli", "validate-source", str(record)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "SOURCE-ID-REQUIRED" in result.stdout


def test_validate_project_state_reads_yaml_and_reports_a_missing_pass(tmp_path):
    record = tmp_path / "PROJECT_STATE.yaml"
    record.write_text(
        "current_phase: 02_protocol\nlast_completed_phase:\n  status: candidate\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "evigate.cli", "validate-project-state", str(record)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "STATE-PASS-REQUIRED" in result.stdout


def test_validate_run_manifest_reports_missing_provenance(tmp_path):
    record = tmp_path / "run-manifest.json"
    record.write_text(json.dumps({"run_id": "RUN-001"}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "evigate.cli", "validate-run-manifest", str(record)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "RUN-CONFIG-REQUIRED" in result.stdout


def test_validate_claim_links_rejects_an_unknown_run_id(tmp_path):
    record = tmp_path / "claim-links.json"
    record.write_text(
        json.dumps(
            [
                {
                    "claim_id": "CLAIM-001",
                    "kind": "measured",
                    "source_ids": ["SRC-001"],
                    "run_ids": ["RUN-UNKNOWN"],
                }
            ]
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "evigate.cli",
            "validate-claim-links",
            str(record),
            "--run-id",
            "RUN-001",
            "--source-id",
            "SRC-001",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "CLAIM-RUN-UNKNOWN" in result.stdout


def test_validate_improvement_proposal_rejects_unapproved_frozen_change(tmp_path):
    record = tmp_path / "improvement-proposal.json"
    record.write_text(
        json.dumps(
            {
                "proposal_id": "IMP-001",
                "status": "proposed",
                "observed_artifact_id": "RUN-001",
                "expected_benefit": "Improve audit coverage.",
                "risk": "May add validation time.",
                "validation": "Add a regression test.",
                "touches_frozen_material": True,
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "evigate.cli",
            "validate-improvement-proposal",
            str(record),
            "--artifact-id",
            "RUN-001",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 2
    assert "IMPROVEMENT-AMENDMENT-REQUIRED" in result.stdout


def test_validation_reports_structured_diagnostic_for_malformed_yaml(tmp_path):
    record = tmp_path / "broken.yaml"
    record.write_text("current_phase: [\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "evigate.cli", "validate-project-state", str(record)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 3
    assert "RECORD-READ-ERROR" in result.stdout
