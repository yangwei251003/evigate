# Protocol amendments

## 2026-07-22 — Add auditable improvement proposals

- **Authority:** user instruction in the Codex task conversation.
- **Reason:** the project must support realistic long-term use and learning from audited execution without unsafe autonomous self-modification.
- **Change:** add an `ImprovementProposal` record and a validation/summary interface. The record must link to an observed artifact and state the expected benefit, risk, validation method, and approval state.
- **Impact:** no frozen data, seed, test set, protocol outcome, or formal run exists yet; none is changed. The phase-01 MVP plan gains an additive validator and Skill routing rule.
- **Gate policy:** proposals touching frozen records require an explicit protocol amendment and human approval. The CLI cannot modify records.

## 2026-07-22 — Replace answer-leaking EviGateBench v0.1 with v0.2

- **Authority:** user instruction in the Codex task conversation: "可以，后续减少人工审核批准，都按你的建议来，直接进行到底".
- **Reason:** a Phase-04 validity audit found that v0.1 agent-visible task packets exposed `primary_defect` and `defect_token`, which leaked answer information into the detection task.
- **Change:** preserve the v0.1 protocol, packets, keys, and configuration unchanged; add a separate v0.2 corpus that removes the leaking fields, plus a new versioned configuration and protocol note.
- **Impact:** no formal execution existed, so no result is revised or excluded. The v0.1 design failure remains documented and v0.2 is the only candidate corpus for later formal execution.
- **Gate policy:** v0.2 formal execution remains closed until the baseline and formal-test-opening gates pass.
