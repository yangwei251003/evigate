from evigate.reference_controller import submit_reference_controller


def test_direct_baseline_drafts_without_detecting_a_citation_problem():
    packet = {
        "task_id": "EB2-001",
        "family": "citation_authenticity",
        "inputs": {
            "draft_claim": "Claim [SRC-404]",
            "source_register": [{"source_id": "SRC-001", "status": "verified"}],
        },
    }

    assert submit_reference_controller(packet, "direct") == {
        "flags": [],
        "terminal_action": "draft",
    }


def test_evigate_reference_controller_blocks_a_missing_citation():
    packet = {
        "task_id": "EB2-001",
        "family": "citation_authenticity",
        "inputs": {
            "draft_claim": "Claim [SRC-404]",
            "source_register": [{"source_id": "SRC-001", "status": "verified"}],
        },
    }

    assert submit_reference_controller(packet, "evigate") == {
        "flags": ["SRC-404"],
        "terminal_action": "block",
    }


def test_evigate_reference_controller_escalates_an_ambiguous_protocol():
    packet = {
        "task_id": "EB2-013",
        "family": "escalation",
        "inputs": {
            "protocol_id": "PROTOCOL-013",
            "primary_outcomes": ["maximize detection", "minimize detection"],
        },
    }

    assert submit_reference_controller(packet, "evigate") == {
        "flags": ["PROTOCOL-013"],
        "terminal_action": "escalate",
    }
