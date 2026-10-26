# Phase 04 — Baseline acceptance report

## Delivered artifacts

- `src/evigate/reference_controller.py`: deterministic fixture controllers for
  direct, linear, and EviGate-style workflow behavior.
- `tests/test_reference_controller.py`: behavior tests for unsafe drafting,
  blocking, and escalation.
- `phases/04_baseline/BASELINE_REPORT.md`: non-formal smoke results and the
  boundary preventing their use as LLM-agent findings.
- `benchmark/v0.2/`: nonleaking versioned corpus created by protocol amendment.

## Acceptance evidence

| Check | Result |
|---|---|
| Full test suite | PASS — 28 passed |
| Project state validation | PASS — `[]` |
| Skill structure validation | PASS |
| Whitespace | PASS — `git diff --check` |

## Negative result and correction

The original v0.1 corpus exposed `primary_defect` and `defect_token` in
agent-visible inputs, invalidating it for formal comparison. It remains
preserved. Version 0.2 removes those fields under a recorded amendment and is
the only candidate for later formal execution.

## Qualifications

- The controllers are scripted harness fixtures, not independent agents or
  model rollouts.
- Their smoke rates are expected behavior checks and cannot be reported as
  scientific performance results.
- Formal execution remains closed.
