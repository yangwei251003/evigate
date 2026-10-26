---
name: evigate-research-orchestrator
description: Evidence-first orchestration for research-to-paper projects. Use when Codex needs to plan, execute, audit, or write an empirical, computational, review, or quantitative research project with phase gates, verified sources, reproducible runs, claim-to-evidence links, or auditable improvement proposals.
---

# EviGate Research Orchestrator

## Overview

Drive a research project through explicit artifacts, deterministic validation, and human approval gates. Treat the project state and registered artifacts as the source of truth; never use chat memory as scientific evidence.

## Start and resume

1. Read `PROJECT_STATE.yaml` and the latest phase report before changing any project artifact.
2. Run the applicable validators before creating a `PASS_CANDIDATE.json`. Install the local package with `python -m pip install -e .` when the `evigate` command is not available.
3. Check that the prior phase has a human-approved `PASS.json` tied to a commit before starting a later phase.
4. Record substantive decisions in versioned files. Ask for human approval at mandatory gates; absence of an objection is not approval.

Use the CLI only to inspect and validate records. It has no command that writes runs, accepts proposals, or changes a phase:

```text
evigate validate-source path/to/source.json
```

## Workflow

Select the current stage from `references/phase-contract.md`. Create only the artifacts listed for that stage and run its validation before handoff.

| Stage group | Required outcome | Human gate |
|---|---|---|
| Capability, question, evidence | verified sources and a bounded question | evidence scope |
| Protocol, data, baseline | frozen questions, outcomes, budgets, seeds, and baseline plan | protocol freeze |
| Experiment and analysis | immutable manifests, raw outputs, failure capture, derived analysis | formal-test opening and analysis acceptance |
| Claims and drafting | claim-evidence graph, paper outline, draft limited to registered results | integrity gate |
| Review and package | independent audit, response matrix, reproducibility package | final release |

If an output fails validation, preserve it and add an explicit failure record. Do not repair, replace, or exclude a formal artifact silently.

## Non-negotiable rules

1. Allow only verified Source IDs to support manuscript claims.
2. Verify that a source supports the exact claim; bibliographic existence alone is insufficient.
3. Freeze hypotheses, metrics, budgets, seeds, and failure criteria before formal results are opened.
4. Label every number as `measured`, `simulated`, or `illustrative`; never present synthetic output as field measurement.
5. Require a Run ID, configuration, seed, environment lock, commit, raw artifact, and validation result for every quantitative manuscript value.
6. Preserve all failures, timeouts, and negative results.
7. Do not claim superiority over an unreproduced baseline.
8. Keep LLM-generated experiment code in a bounded execution environment with a budget and stop condition.
9. Let reviewers audit drafts without silently rewriting them.
10. Mark automatic drafts as drafts until integrity, review, reproducibility, and human release gates pass.

## Domain and agent adapters

Use the `ml-empirical` defaults for the first project. Add a domain adapter only when it declares its required evidence, protocol fields, outcome types, safety constraints, and analysis rules. Do not copy domain-specific thresholds across fields without a documented rationale.

Keep agent adapters thin: they map artifact paths and tool vocabulary, not scientific standards. A Codex, Claude Code, Cursor, or OpenCode adapter must retain the same gates and artifact schema.

## Auditable improvement loop

After a run, audit, or review, inspect registered failure records and unresolved evidence gaps. Draft an `ImprovementProposal` using the template in `templates/`. It must identify the triggering artifact, affected component, expected benefit, risk, validation test, and frozen-material impact.

The system may adapt its next non-frozen task plan from an accepted proposal. It must not automatically accept, apply, delete, or conceal a proposal. Any change to a Skill, adapter, protocol, benchmark, or formal output requires a reviewable Git change; frozen materials additionally require a protocol amendment and explicit human approval.

## Resources

- Read `references/phase-contract.md` for allowed transitions, artifact contracts, and the improvement-proposal schema.
- Copy a template from `templates/` only into a new project artifact; never overwrite a formal record.
