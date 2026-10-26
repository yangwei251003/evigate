import json
from pathlib import Path

from evigate.benchmark_validation import (
    validate_answer_key,
    validate_execution_manifest,
    validate_packet,
)


def test_packet_requires_one_known_primary_defect():
    packet = {"task_id": "EB-001", "primary_defect": "unknown"}

    assert {issue.code for issue in validate_packet(packet)} == {
        "BENCHMARK-PACKET-SCHEMA-REQUIRED",
        "BENCHMARK-PACKET-FAMILY-REQUIRED",
        "BENCHMARK-PACKET-DEFECT-INVALID",
        "BENCHMARK-PACKET-INPUTS-REQUIRED",
        "BENCHMARK-PACKET-ACTIONS-REQUIRED",
    }


def test_answer_key_must_match_packet_and_declare_scoring_rules():
    key = {"task_id": "EB-001", "primary_defect": "citation_authenticity"}

    assert {issue.code for issue in validate_answer_key(key, "EB-002")} == {
        "BENCHMARK-KEY-TASK-MISMATCH",
        "BENCHMARK-KEY-DETECTION-REQUIRED",
        "BENCHMARK-KEY-CONTAINMENT-REQUIRED",
        "BENCHMARK-KEY-UNSAFE-REQUIRED",
    }


def test_execution_manifest_requires_identity_and_new_output_path(tmp_path):
    output = tmp_path / "already-exists.json"
    output.write_text("{}", encoding="utf-8")
    manifest = {"run_id": "RUN-001", "output_path": str(output)}

    assert {issue.code for issue in validate_execution_manifest(manifest)} == {
        "BENCHMARK-MANIFEST-TASK-REQUIRED",
        "BENCHMARK-MANIFEST-CONDITION-REQUIRED",
        "BENCHMARK-MANIFEST-SEED-REQUIRED",
        "BENCHMARK-MANIFEST-RUNTIME-REQUIRED",
        "BENCHMARK-MANIFEST-COMMIT-REQUIRED",
        "BENCHMARK-MANIFEST-ENV-REQUIRED",
        "BENCHMARK-MANIFEST-BUDGET-REQUIRED",
        "BENCHMARK-MANIFEST-STOP-REQUIRED",
        "BENCHMARK-OUTPUT-EXISTS",
    }


def test_frozen_corpus_has_sixteen_valid_packet_key_pairs():
    packets = sorted(Path("benchmark/packets").glob("EB-*.json"))

    assert len(packets) == 16
    for packet_path in packets:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        key_path = Path("benchmark/answer-keys") / packet_path.name
        key = json.loads(key_path.read_text(encoding="utf-8"))

        assert validate_packet(packet) == []
        assert validate_answer_key(key, packet["task_id"]) == []
        assert packet["primary_defect"] == key["primary_defect"]


def test_pilot_configuration_declares_conditions_runs_and_closed_gate():
    config = json.loads(
        Path("configs/evigatebench-v0.1.json").read_text(encoding="utf-8")
    )

    assert config["conditions"] == ["direct", "linear", "evigate"]
    assert config["planned_runs"] == 48
    assert config["seed_rule"] == "one fixed seed per task-condition combination"
    assert config["formal_runs_open"] is False


def test_v2_packet_hides_primary_defect_from_agent_visible_inputs():
    packet = {
        "schema_version": 2,
        "task_id": "EB2-001",
        "family": "citation_authenticity",
        "inputs": {
            "draft_claim": "Claim [SRC-404]",
            "source_register": [{"source_id": "SRC-001", "status": "verified"}],
        },
        "allowed_actions": ["flag", "block", "escalate", "draft"],
    }

    assert validate_packet(packet) == []
    assert "primary_defect" not in packet
    assert "defect_token" not in packet["inputs"]


def test_v2_frozen_corpus_has_sixteen_nonleaking_packet_key_pairs():
    packets = sorted(Path("benchmark/v0.2/packets").glob("EB2-*.json"))

    assert len(packets) == 16
    for packet_path in packets:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        key_path = Path("benchmark/v0.2/answer-keys") / packet_path.name
        key = json.loads(key_path.read_text(encoding="utf-8"))

        assert validate_packet(packet) == []
        assert validate_answer_key(key, packet["task_id"]) == []
        assert "primary_defect" not in packet
        assert "defect_token" not in packet["inputs"]


def test_v2_configuration_preserves_closed_formal_gate_and_scorer_only_keys():
    config = json.loads(
        Path("configs/evigatebench-v0.2.json").read_text(encoding="utf-8")
    )

    assert config["supersedes"] == "EviGateBench-v0.1"
    assert config["formal_runs_open"] is False
    assert config["answer_key_access"] == "scorer_only"
