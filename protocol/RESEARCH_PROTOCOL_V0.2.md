# EviGateBench v0.2 Pilot Protocol

This protocol supersedes v0.1 for any future formal execution. Its research
question, conditions, number of planned runs, budget, outcomes, and failure
preservation policy are unchanged from
[v0.1](RESEARCH_PROTOCOL.md). The authoritative configuration is
[configs/evigatebench-v0.2.json](../configs/evigatebench-v0.2.json).

## Validity correction

The preserved v0.1 task packets exposed `primary_defect` and `defect_token` to
the evaluated agent. That made the planned detection outcome answer-visible and
invalidated v0.1 for formal comparison. Version 0.2 retains the original task
families and answer keys but removes both answer-revealing fields from all
agent-visible packets. The answer keys remain scorer-only artifacts.

No v0.1 execution was performed. The correction creates a new, versioned test
corpus rather than modifying the v0.1 packets, keys, or configuration. Formal
runs remain closed pending the required later phase gate.
