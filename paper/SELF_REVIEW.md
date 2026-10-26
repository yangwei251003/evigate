# Editorial self-review

## Decision: Major revision required before external submission

### Strengths

- Clear provenance from source records and claims to raw records.
- Explicit preservation of the v0.1 answer-leakage failure.
- Accurate separation of detection and containment in the simulated workflow.

### Major blockers

1. The three controllers are scripted, so their separation is constructed by
   design rather than independently measured.
2. The synthetic corpus has only 16 tasks and no blind human or external-model
   evaluation.
3. The task answer keys remain repository-visible; future actual-agent studies
   need a secret-scoring deployment arrangement.

### Required follow-up for a submission-grade empirical paper

Run independent, pre-registered LLM agents without answer-key access; add
repeated seeds where the runtime is stochastic; recruit blinded evaluators for
ambiguous cases; and compare against a public, legally reusable task suite.

## Current recommendation

Release this manuscript as a transparent technical-report draft and use it to
support the next independent-agent evaluation, not as evidence of general
research-agent reliability.
