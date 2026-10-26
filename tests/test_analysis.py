from evigate.analysis import aggregate_by_condition


def test_aggregate_by_condition_preserves_run_ids_and_rates():
    records = [
        {
            "manifest": {"condition": "direct", "run_id": "RUN-001"},
            "score": {
                "detection": False,
                "containment": False,
                "unsafe_continuation": True,
            },
        },
        {
            "manifest": {"condition": "evigate", "run_id": "RUN-002"},
            "score": {
                "detection": True,
                "containment": True,
                "unsafe_continuation": False,
            },
        },
    ]

    assert aggregate_by_condition(records) == {
        "direct": {
            "n": 1,
            "run_ids": ["RUN-001"],
            "detection_rate": 0.0,
            "containment_rate": 0.0,
            "unsafe_continuation_rate": 1.0,
        },
        "evigate": {
            "n": 1,
            "run_ids": ["RUN-002"],
            "detection_rate": 1.0,
            "containment_rate": 1.0,
            "unsafe_continuation_rate": 0.0,
        },
    }
