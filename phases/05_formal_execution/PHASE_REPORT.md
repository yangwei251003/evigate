# Phase 05 — Formal execution report

## Execution scope

Executed the v0.2 **reference-controller simulation** only. These 48 runs are
deterministic scripted-controller outputs, not LLM-agent rollouts and not
evidence of general research-agent performance.

## Registered material

- 48 pre-run manifests in `runs/formal-v0.2/manifests/`.
- 48 immutable raw records in `runs/formal-v0.2/raw/`.
- Each manifest records task ID, condition, seed, runtime, configuration,
  commit, environment lock, budget, stop condition, and distinct output path.

## Execution validation

An independent post-run verification inspected all 48 raw records and checked:

1. raw record count equals manifest count;
2. score Run ID and task ID equal their manifest values; and
3. configuration, seed, environment lock, commit, budget, and stop condition
   are present in every manifest.

Result: `raw_provenance_validation=pass_48_of_48`.

## Restrictions

- The raw records may support only claims about this scripted simulation.
- They may not be described as independent model results, human evaluations,
  or evidence of EviGate's general effectiveness.
- No record was retried, replaced, deleted, or silently repaired.

## Gate status

Formal execution is complete. Aggregates and manuscript numbers may be derived
only in the analysis phase from the committed raw records.
