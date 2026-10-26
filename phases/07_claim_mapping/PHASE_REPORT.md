# Phase 07 — Claim mapping report

## Claim graph

`claims/CLAIM_EVIDENCE_GRAPH.json` registers six claims. The three background
claims link to their verified scholarly Source IDs. The three quantitative
claims link to `SRC-EVIGATE-SIM-V02` and the exact 16 Run IDs for their
condition.

## Verification

- `validate-source SRC-EVIGATE-SIM-V02.json` emitted `[]`.
- `validate-claim-links` with all four Source IDs and all 48 Run IDs emitted
  `[]`.
- Full tests passed: 30 passed.

## Writing rule

The quantitative claims must use the label **deterministic reference-controller
simulation** in the paper. They must not be generalized to LLM agents, humans,
scientific discovery, or real publication quality.

## Gate status

The source and run provenance needed for drafting is complete. The manuscript
must remain within the six registered claim boundaries.
