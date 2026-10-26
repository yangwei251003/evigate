# EviGateBench v0.1 Pilot Protocol

## Registered question

Does EviGate improve detection or containment of pre-specified citation,
claim-support, run-provenance, and escalation defects compared with direct
drafting and a non-blocking linear workflow?

## Scope and conditions

The pilot evaluates workflow reliability only. It does not evaluate scientific
discovery, publication quality, cross-domain generalization, or researcher
replacement. It contains 16 fictional, static task packets, each with exactly
one seeded primary defect. The three conditions are `direct`, `linear`, and
`evigate`. Each receives identical visible inputs, tool allowance, output
schema, and budget; only the workflow controls differ.

## Planned execution

The frozen configuration is [configs/evigatebench-v0.1.json](../configs/evigatebench-v0.1.json).
The pilot has 48 planned executions: 16 packets multiplied by three
conditions. Every task-condition combination uses one fixed seed. Each run has
a 20-minute wall-clock ceiling, no external side effects, a pre-run manifest,
and a distinct output path. A timeout, refusal, runtime error, missing trace,
or scoring error is preserved as a failed outcome and is never silently
restarted or excluded.

## Outcomes and derivation

The primary outcomes are detection, containment, and unsafe continuation. A
deterministic answer key scores whether required defect tokens were flagged and
whether the terminal action safely blocked or escalated instead of drafting.
Derived rates equal the number of recorded positive outcomes divided by the
number of registered score records. Secondary measures are provenance
completeness, Ask-F1, unnecessary escalations, and trace completeness; they
remain descriptive in this pilot.

## Freeze and amendments

Formal runs are closed. No benchmark output is a research result until the
repository's required Phase-02 approval opens the next allowed activity. Any
change to the configuration, task corpus, scoring rules, budget, seed rule, or
outcome definition requires a dated entry in
[audit/PROTOCOL_AMENDMENTS.md](../audit/PROTOCOL_AMENDMENTS.md), a reviewable
Git change, and explicit human approval. The corpus contains no private data,
external full text, credentials, live journal interaction, or LLM-generated
code execution.
