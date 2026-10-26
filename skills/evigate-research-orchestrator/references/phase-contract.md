# Phase contract

## Required progression

| Phase | Purpose | Required artifacts | Mandatory gate |
|---|---|---|---|
| 00 | Capability and project design | project state, design, implementation plan | human approval of candidate commit |
| 01 | Skill MVP | Skill, validators, tests, templates, acceptance report | human approval of candidate commit |
| 02 | Benchmark protocol | research questions, synthetic-task policy, outcomes, seeds, analysis plan | protocol freeze |
| 03 | Evidence registry | search log, verified source records, exclusion log | evidence acceptance |
| 04 | Baseline | reproducible baseline and failure report | baseline acceptance |
| 05 | Formal execution | immutable pre-run manifests, raw outputs, failures | formal-test opening |
| 06 | Analysis | derived tables, uncertainty, anomaly log | analysis acceptance |
| 07 | Claim mapping | claim-evidence graph and provenance audit | integrity gate |
| 08 | Draft and review | draft, integrity report, reviewer reports, revisions | final release |
| 09 | Package and archive | reproducibility manifest, license audit, lessons | publication decision |

## Transition rule

Before entering phase N, confirm that phase N-1 has `PASS.json` with `human_approved: true`, a candidate commit, and automated checks. A `PASS_CANDIDATE.json` is not approval. Retain every failed attempt as an artifact.

## Record roles

- A `SourceRecord` has a stable `source_id`, status, locator, verification method, and verification timestamp. Only `verified` records support manuscript claims.
- A `RunManifest` is written before execution and has a Run ID, configuration identifier, seed, environment lock, commit, command, budget, and output locations.
- A `ClaimLink` has a claim ID, claim kind, Source IDs, and—for measured or simulated claims—Run IDs.
- An `ImprovementProposal` is an auditable suggestion, not an instruction to mutate a project.

## Improvement proposal schema

```json
{
  "proposal_id": "IMP-001",
  "status": "proposed",
  "observed_artifact_id": "RUN-001",
  "affected_component": "skills/evigate-research-orchestrator/SKILL.md",
  "expected_benefit": "Reduce unregistered-result attempts.",
  "risk": "May make task intake more restrictive.",
  "validation": "Add a failing regression test and run the full suite.",
  "touches_frozen_material": false,
  "approval": null
}
```

Allowed statuses are `proposed`, `accepted`, `rejected`, and `superseded`. A proposal may be `accepted` only with an approval record. The CLI validates the record but never changes its status.
