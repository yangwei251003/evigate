# Phase 04 — Reference baseline report

## Baseline type

This phase implements three deterministic reference controllers for harness
validation. They are **not LLM agents**, do not use external tools, and are not
evidence of research-agent performance. Their sole purpose is to verify that
the v0.2 packet corpus and scorer distinguish unsafe drafting, detection-only
behavior, and safe blocking/escalation.

| Condition | Reference behavior |
|---|---|
| `direct` | Always drafts; never flags a defect. |
| `linear` | Applies fixed detection rules but always drafts afterwards. |
| `evigate` | Applies the same fixed detection rules; blocks evidence/provenance defects and escalates protocol blockers. |

## Non-formal smoke evidence

An in-memory, non-formal smoke execution over 16 v0.2 packets produced these
descriptive rates:

| Condition | n | Detection | Containment | Unsafe continuation |
|---|---:|---:|---:|---:|
| `direct` | 16 | 0.00 | 0.00 | 1.00 |
| `linear` | 16 | 1.00 | 0.00 | 1.00 |
| `evigate` | 16 | 1.00 | 1.00 | 0.00 |

These values are expected consequences of the scripted controller rules. They
are not formal runs, may not be reported as LLM-agent findings, and may only be
used as harness-validation evidence. No raw score file was written.

## Failure retained

The frozen v0.1 corpus was rejected for formal use because it exposed answer
information. The v0.2 corpus corrects that issue under the recorded protocol
amendment; v0.1 remains preserved and excluded from any future formal run.

## Gate status

The reference baseline validates the harness behavior. Formal execution stays
closed until a separate Phase-04 acceptance record and Phase-05 opening.
