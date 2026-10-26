# Phase 06 — Analysis report

## Derived artifact

`analysis/formal-v0.2/summary.json` groups the 48 committed raw records by
condition and retains every contributing Run ID. The corresponding Markdown
report presents descriptive rates and the interpretation boundary.

## Quantitative values

The direct controller has detection/containment/unsafe-continuation rates of
0.00/0.00/1.00; the linear controller has 1.00/0.00/1.00; and the EviGate
controller has 1.00/1.00/0.00, each over 16 scripted runs.

Every value traces to `ANALYSIS-FORMAL-V0.2-001`, its raw-record list,
pre-registered manifests, seed, environment lock, and commits. These are
simulation-specific values, not LLM-agent results.

## Gate status

Analysis is ready for claim mapping with the required limitation language.
