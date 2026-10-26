"""Read-only command-line entry point for EviGate validators."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path

import yaml

from .benchmark_validation import validate_execution_manifest, validate_packet
from .io import load_list, load_mapping
from .validation import (
    validate_claim_links,
    validate_improvement_proposal,
    validate_project_state,
    validate_run_manifest,
    validate_source,
)


def main(argv: list[str] | None = None) -> int:
    """Validate one source record and return a stable process status."""

    parser = argparse.ArgumentParser(prog="evigate")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validators = {
        "validate-project-state": validate_project_state,
        "validate-run-manifest": validate_run_manifest,
        "validate-source": validate_source,
    }
    for command in validators:
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("record", type=Path)
    benchmark_manifest_parser = subparsers.add_parser("validate-benchmark-manifest")
    benchmark_manifest_parser.add_argument("record", type=Path)
    benchmark_packet_parser = subparsers.add_parser("validate-benchmark-packet")
    benchmark_packet_parser.add_argument("record", type=Path)
    claim_parser = subparsers.add_parser("validate-claim-links")
    claim_parser.add_argument("record", type=Path)
    claim_parser.add_argument("--run-id", action="append", default=[])
    claim_parser.add_argument("--source-id", action="append", default=[])
    improvement_parser = subparsers.add_parser("validate-improvement-proposal")
    improvement_parser.add_argument("record", type=Path)
    improvement_parser.add_argument("--artifact-id", action="append", default=[])
    args = parser.parse_args(argv)

    if args.command == "validate-claim-links":
        try:
            links = load_list(args.record)
        except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
            print(
                json.dumps(
                    [{"code": "RECORD-READ-ERROR", "message": str(error)}],
                    ensure_ascii=False,
                )
            )
            return 3
        issues = validate_claim_links(links, set(args.run_id), set(args.source_id))
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False))
        return 0 if not issues else 2

    if args.command == "validate-improvement-proposal":
        try:
            proposal = load_mapping(args.record)
        except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
            print(
                json.dumps(
                    [{"code": "RECORD-READ-ERROR", "message": str(error)}],
                    ensure_ascii=False,
                )
            )
            return 3
        issues = validate_improvement_proposal(proposal, set(args.artifact_id))
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False))
        return 0 if not issues else 2

    if args.command in {
        "validate-benchmark-manifest",
        "validate-benchmark-packet",
    }:
        try:
            record = load_mapping(args.record)
        except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
            print(
                json.dumps(
                    [{"code": "RECORD-READ-ERROR", "message": str(error)}],
                    ensure_ascii=False,
                )
            )
            return 3
        validator = (
            validate_execution_manifest
            if args.command == "validate-benchmark-manifest"
            else validate_packet
        )
        issues = validator(record)
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False))
        return 0 if not issues else 2

    if args.command in validators:
        try:
            record = load_mapping(args.record)
        except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
            print(
                json.dumps(
                    [{"code": "RECORD-READ-ERROR", "message": str(error)}],
                    ensure_ascii=False,
                )
            )
            return 3
        issues = validators[args.command](record)
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False))
        return 0 if not issues else 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
