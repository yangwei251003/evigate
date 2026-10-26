# EviGate Research Orchestrator MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable, evidence-first research-orchestration Skill with deterministic project, evidence, run-manifest, and claim-link validation.

**Architecture:** Keep policy in the Skill and deterministic checks in a dependency-light Python package. The CLI reads project-local JSON/YAML-compatible records, emits structured diagnostics, and never mutates formal artifacts. Templates and domain adapters stay declarative so the Skill can be installed across agent environments.

**Tech Stack:** Python 3.12, `PyYAML` for the repository's YAML records, `pytest`, JSON records, Markdown Skill resources.

---

## File structure

| Path | Responsibility |
|---|---|
| `pyproject.toml` | Package metadata, console entry point, and test configuration. |
| `src/evigate/models.py` | Typed record shapes and stable diagnostic codes. |
| `src/evigate/validation.py` | Pure validation functions with no filesystem writes. |
| `src/evigate/io.py` | Safe JSON/YAML record loading for read-only validation commands. |
| `src/evigate/cli.py` | Read-only CLI commands and JSON diagnostic rendering. |
| `skills/evigate-research-orchestrator/SKILL.md` | Concise routing and phase-gate instructions. |
| `skills/evigate-research-orchestrator/references/phase-contract.md` | Full state transition and approval contract. |
| `skills/evigate-research-orchestrator/templates/` | Safe starting records for state, source, run, and claim links. |
| `tests/test_validation.py` | Unit tests for every mandatory invariant, including auditable improvement proposals. |
| `tests/test_cli.py` | Black-box tests for success and failure exit codes. |
| `benchmark/` | A later phase's immutable synthetic task packets and registered runs. |

### Task 1: Package skeleton and project-state validation

**Files:**
- Create: `pyproject.toml`
- Create: `src/evigate/__init__.py`
- Create: `src/evigate/models.py`
- Create: `src/evigate/validation.py`
- Create: `tests/test_validation.py`

- [ ] **Step 1: Write the failing project-state test**

```python
from evigate.validation import validate_project_state


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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_validation.py::test_project_state_requires_approved_pass_for_later_phase -v`

Expected: FAIL because `evigate.validation` does not exist.

- [ ] **Step 3: Implement the minimal model and validator**

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Issue:
    code: str
    message: str


def validate_project_state(state: dict[str, Any]) -> list[Issue]:
    completed = state.get("last_completed_phase") or {}
    if state.get("current_phase") == "00_skill_design":
        return []
    required = {
        "status": ("passed", "STATE-PASS-REQUIRED", "Later phases require a human-approved PASS record."),
        "approved_commit": (None, "STATE-APPROVAL-COMMIT-REQUIRED", "PASS record must name its approved commit."),
        "pass_file": (None, "STATE-PASS-FILE-REQUIRED", "PASS record path is required."),
    }
    return [
        Issue(code, message)
        for field, (expected, code, message) in required.items()
        if (completed.get(field) != expected if expected is not None else not completed.get(field))
    ]
```

- [ ] **Step 4: Run the focused test and full unit suite**

Run: `python -m pytest tests/test_validation.py -v`

Expected: PASS with the project-state test reported as passed.

- [ ] **Step 5: Commit the completed task**

```bash
git add pyproject.toml src/evigate tests/test_validation.py
git commit -m "feat: validate EviGate project state"
```

### Task 2: Evidence, manifest, and claim-link validators

**Files:**
- Modify: `src/evigate/validation.py`
- Modify: `tests/test_validation.py`

- [ ] **Step 1: Write failing tests for three evidence-provenance invariants**

```python
from evigate.validation import validate_claim_links, validate_run_manifest, validate_source


def test_source_must_have_stable_id_and_verified_locator():
    assert [issue.code for issue in validate_source({"status": "verified"})] == [
        "SOURCE-ID-REQUIRED", "SOURCE-LOCATOR-REQUIRED"
    ]


def test_run_manifest_requires_before_run_provenance_fields():
    assert {issue.code for issue in validate_run_manifest({"run_id": "R-1"})} >= {
        "RUN-CONFIG-REQUIRED", "RUN-SEED-REQUIRED", "RUN-ENV-REQUIRED", "RUN-COMMIT-REQUIRED"
    }


def test_quantitative_claim_requires_registered_run_and_evidence():
    links = [{"claim_id": "C-1", "kind": "measured", "source_ids": [], "run_ids": []}]
    assert {issue.code for issue in validate_claim_links(links, {"R-1"}, {"S-1"})} == {
        "CLAIM-EVIDENCE-REQUIRED", "CLAIM-RUN-REQUIRED"
    }
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m pytest tests/test_validation.py -k "source or manifest or quantitative" -v`

Expected: FAIL because the three validator functions do not exist.

- [ ] **Step 3: Implement pure validators with stable, machine-readable issue codes**

```python
def validate_source(source: dict[str, Any]) -> list[Issue]:
    issues = []
    if not source.get("source_id"):
        issues.append(Issue("SOURCE-ID-REQUIRED", "source_id is required."))
    if source.get("status") == "verified" and not source.get("locator"):
        issues.append(Issue("SOURCE-LOCATOR-REQUIRED", "Verified source requires an authoritative locator."))
    return issues


def validate_run_manifest(manifest: dict[str, Any]) -> list[Issue]:
    required = {"config": "RUN-CONFIG-REQUIRED", "seed": "RUN-SEED-REQUIRED", "environment_lock": "RUN-ENV-REQUIRED", "commit": "RUN-COMMIT-REQUIRED"}
    return [Issue(code, f"{field} is required before execution.") for field, code in required.items() if not manifest.get(field)]


def validate_claim_links(links: list[dict[str, Any]], run_ids: set[str], source_ids: set[str]) -> list[Issue]:
    issues = []
    for link in links:
        if not set(link.get("source_ids", [])) <= source_ids:
            issues.append(Issue("CLAIM-EVIDENCE-UNKNOWN", "Claim references an unknown Source ID."))
        if not link.get("source_ids"):
            issues.append(Issue("CLAIM-EVIDENCE-REQUIRED", "Claim requires at least one verified Source ID."))
        if link.get("kind") in {"measured", "simulated"} and not link.get("run_ids"):
            issues.append(Issue("CLAIM-RUN-REQUIRED", "Quantitative claim requires a registered Run ID."))
    return issues
```

- [ ] **Step 4: Run the focused tests and full suite**

Run: `python -m pytest -v`

Expected: PASS; invalid fixtures must produce the exact codes asserted above.

- [ ] **Step 5: Commit the completed task**

```bash
git add src/evigate/validation.py tests/test_validation.py
git commit -m "feat: validate evidence and result provenance"
```

### Task 3: Read-only CLI and Skill package

**Files:**
- Create: `src/evigate/cli.py`
- Modify: `pyproject.toml`
- Create: `skills/evigate-research-orchestrator/SKILL.md`
- Create: `skills/evigate-research-orchestrator/references/phase-contract.md`
- Create: `skills/evigate-research-orchestrator/templates/project-state.json`
- Create: `skills/evigate-research-orchestrator/templates/source-record.json`
- Create: `skills/evigate-research-orchestrator/templates/run-manifest.json`
- Create: `skills/evigate-research-orchestrator/templates/claim-links.json`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write a failing CLI integration test**

```python
import json
import subprocess
import sys


def test_validate_source_returns_nonzero_for_unverifiable_record(tmp_path):
    record = tmp_path / "source.json"
    record.write_text(json.dumps({"status": "verified"}), encoding="utf-8")
    result = subprocess.run([sys.executable, "-m", "evigate.cli", "validate-source", str(record)], capture_output=True, text=True)
    assert result.returncode == 2
    assert "SOURCE-ID-REQUIRED" in result.stdout
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_cli.py::test_validate_source_returns_nonzero_for_unverifiable_record -v`

Expected: FAIL because the `evigate.cli` module is unavailable.

- [ ] **Step 3: Implement the CLI with no mutation commands**

```python
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evigate")
    subparsers = parser.add_subparsers(dest="command", required=True)
    source_parser = subparsers.add_parser("validate-source")
    source_parser.add_argument("record", type=Path)
    args = parser.parse_args(argv)
    if args.command == "validate-source":
        issues = validate_source(json.loads(args.record.read_text(encoding="utf-8")))
        print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False))
        return 0 if not issues else 2
    return 1
```

- [ ] **Step 4: Run CLI and package tests**

Run: `python -m pytest -v && python -m evigate.cli --help`

Expected: PASS, then a help screen listing only validation commands.

- [ ] **Step 5: Validate the Skill metadata and commit the task**

Run: `python <USER_HOME>\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/evigate-research-orchestrator`

Expected: validation succeeds with no frontmatter or naming errors.

```bash
git add pyproject.toml src/evigate skills tests
git commit -m "feat: add EviGate skill and validation CLI"
```

### Task 4: Auditable improvement-proposal validation

**Files:**
- Modify: `src/evigate/validation.py`
- Modify: `tests/test_validation.py`
- Create: `skills/evigate-research-orchestrator/templates/improvement-proposal.json`
- Modify: `skills/evigate-research-orchestrator/SKILL.md`

- [ ] **Step 1: Write the failing test for an untraceable proposal**

```python
from evigate.validation import validate_improvement_proposal


def test_improvement_proposal_requires_observation_risk_and_validation():
    proposal = {"proposal_id": "IMP-001", "status": "proposed"}
    assert {issue.code for issue in validate_improvement_proposal(proposal, {"RUN-001"})} == {
        "IMPROVEMENT-OBSERVATION-REQUIRED",
        "IMPROVEMENT-RISK-REQUIRED",
        "IMPROVEMENT-VALIDATION-REQUIRED",
    }
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_validation.py::test_improvement_proposal_requires_observation_risk_and_validation -v`

Expected: FAIL because `validate_improvement_proposal` does not exist.

- [ ] **Step 3: Implement validation that cannot accept or apply a proposal**

```python
def validate_improvement_proposal(proposal: dict[str, Any], artifact_ids: set[str]) -> list[Issue]:
    issues = []
    if proposal.get("observed_artifact_id") not in artifact_ids:
        issues.append(Issue("IMPROVEMENT-OBSERVATION-REQUIRED", "Proposal requires a registered observation artifact."))
    if not proposal.get("risk"):
        issues.append(Issue("IMPROVEMENT-RISK-REQUIRED", "Proposal requires a risk statement."))
    if not proposal.get("validation"):
        issues.append(Issue("IMPROVEMENT-VALIDATION-REQUIRED", "Proposal requires a validation method."))
    return issues
```

- [ ] **Step 4: Run the full test suite and validate the template**

Run: `python -m pytest -v`

Expected: PASS. Confirm the new template has `status: "proposed"`; no command accepts or applies it.

- [ ] **Step 5: Commit the completed task**

```bash
git add src/evigate/validation.py tests/test_validation.py skills/evigate-research-orchestrator
git commit -m "feat: add auditable improvement proposals"
```

### Task 5: Phase-01 acceptance evidence and human gate

**Files:**
- Create: `phases/01_skill_mvp/PHASE_REPORT.md`
- Create: `phases/01_skill_mvp/PASS_CANDIDATE.json`
- Modify: `PROJECT_STATE.yaml`

- [ ] **Step 1: Add a failing test for the valid template set**

```python
def test_all_shipped_templates_validate():
    project_state = json.loads(Path("skills/evigate-research-orchestrator/templates/project-state.json").read_text())
    source = json.loads(Path("skills/evigate-research-orchestrator/templates/source-record.json").read_text())
    manifest = json.loads(Path("skills/evigate-research-orchestrator/templates/run-manifest.json").read_text())
    links = json.loads(Path("skills/evigate-research-orchestrator/templates/claim-links.json").read_text())
    assert validate_project_state(project_state) == []
    assert validate_source(source) == []
    assert validate_run_manifest(manifest) == []
    assert validate_claim_links(links, {"RUN-001"}, {"SRC-001"}) == []
```

- [ ] **Step 2: Run the test to verify templates are incomplete**

Run: `python -m pytest tests/test_validation.py::test_all_shipped_templates_validate -v`

Expected: FAIL until every template satisfies the validators.

- [ ] **Step 3: Complete only the templates and report facts from executed tests**

```markdown
# Phase 01 Skill MVP report

## Automated evidence

- Package tests: record the exact command, timestamp, and passed/failed count.
- Skill validation: record the exact command and result.
- Scope: validation tooling only; no scientific result is claimed.
```

- [ ] **Step 4: Run the entire validation set and create the candidate record**

Run: `python -m pytest -v; python <USER_HOME>\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/evigate-research-orchestrator`

Expected: all tests and Skill checks pass before writing `PASS_CANDIDATE.json`.

- [ ] **Step 5: Commit and request explicit human approval**

```bash
git add PROJECT_STATE.yaml phases/01_skill_mvp
git commit -m "docs: record EviGate MVP acceptance candidate"
```

Do not create `PASS.json` or enter the benchmark phase until the user explicitly approves this exact commit.
