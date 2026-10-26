# Formal reference-controller analysis

## Inputs and provenance

This analysis derives exclusively from the 48 committed raw records listed in
`summary.json`. The raw-record commit is
`8ae315c5533b19a20ccbf3da4a1c2e25e3b5d6e6`; the analysis implementation commit
is `b6c13067bd53e4afb7ffd25e948233daa95f5b9e`.

## Descriptive summary

| Condition | Runs | Detection rate | Containment rate | Unsafe-continuation rate |
|---|---:|---:|---:|---:|
| Direct reference controller | 16 | 0.00 | 0.00 | 1.00 |
| Linear reference controller | 16 | 1.00 | 0.00 | 1.00 |
| EviGate reference controller | 16 | 1.00 | 1.00 | 0.00 |

## Interpretation boundary

These figures demonstrate only that the frozen scorer distinguishes three
scripted controller behaviors on the v0.2 synthetic corpus. The EviGate
controller is intentionally programmed to block or escalate after the same
fixed detector used by the linear condition. Consequently, the results do not
estimate model performance, effect sizes, uncertainty, scientific validity, or
the benefit of EviGate for autonomous research agents. No hypothesis test is
appropriate for this deterministic single-run simulation.

## Preserved anomalies and limitations

- The v0.1 corpus answer-leakage flaw is preserved in the amendment log and
  excluded from this analysis.
- Every condition uses a scripted controller; there are no independent seeds,
  independent models, human judges, or external task environments.
- The 16 tasks are synthetic and therefore do not measure real-paper writing,
  baseline reproduction, or scientific discovery.
