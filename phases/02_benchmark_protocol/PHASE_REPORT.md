# Phase 02 — Benchmark Protocol report

## Objective

Freeze an offline-first pilot protocol for evaluating whether EviGate detects
or safely contains seeded research-workflow defects. This phase creates no
formal execution, quantitative result, or manuscript finding.

## Delivered artifacts

- `benchmark/packets/`: 16 fictional, immutable, agent-visible task packets.
- `benchmark/answer-keys/`: matching scorer-only answer keys for the four
  registered defect families.
- `configs/evigatebench-v0.1.json`: three conditions, 48 planned pilot runs,
  fixed-seed rule, ceiling, outcomes, and closed formal-run gate.
- `protocol/RESEARCH_PROTOCOL.md`: registered question, scope, failures,
  derivation policy, and amendment rule.
- `src/evigate/benchmark_*.py` and `src/evigate/scoring.py`: deterministic
  validators, non-overwriting artifact writing, and descriptive scoring.

## Automated evidence

| Check | Command | Result |
|---|---|---|
| Full test suite | `python -m pytest -v` | PASS — 22 passed |
| Project state | `python -m evigate.cli validate-project-state PROJECT_STATE.yaml` | PASS — `[]` |
| Skill structure | `python <USER_HOME>\\.codex\\skills\\.system\\skill-creator\\scripts\\quick_validate.py skills\\evigate-research-orchestrator` | PASS |
| Whitespace | `git diff --check` | PASS |

## Controls demonstrated

- Packets and answer keys have stable IDs, one declared defect family, and
  machine-readable scoring rules.
- A run manifest requires task, condition, seed, runtime, commit, environment
  lock, budget, stop condition, and a new output path.
- Existing artifacts cannot be overwritten by the benchmark writer.
- Score derivation is deterministic and preserves unsafe continuation as a
  first-class outcome.
- The registered configuration has `formal_runs_open: false`.

## Qualifications

- The task corpus is a synthetic pilot; it does not demonstrate real-world
  research-agent reliability or publication quality.
- No agent rollout, external tool action, formal run, or quantitative study
  result has been generated in this phase.
- The answer keys are intended for scoring only and must not be provided to an
  evaluated agent.

## Gate status

Automated acceptance checks passed. The next phase may only establish and
verify the evidence registry; formal execution remains closed.
