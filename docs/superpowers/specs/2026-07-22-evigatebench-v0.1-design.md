# EviGateBench v0.1 benchmark-protocol design

## Decision

Evaluate EviGate first on a small, transparent, synthetic benchmark of research task packets with seeded, auditable defects. The study evaluates workflow reliability, not research capability, publication quality, or universal cross-domain performance.

The protocol will compare the same task packet under three conditions:

1. **Direct drafting**: complete the packet without a persistent state, evidence register, or gates.
2. **Linear workflow**: use the same required artifacts but permit progress without an EviGate blocking decision.
3. **EviGate**: use the Skill's persistent state, evidence checks, provenance checks, and risk-based escalation rule.

Each condition receives the same packet text, tool allowance, time budget, and output schema. Conditions differ only in workflow controls.

## Research question and boundary

**RQ1.** Does EviGate improve detection or containment of pre-specified evidence, provenance, and escalation defects relative to direct drafting and a non-blocking linear workflow?

**RQ2.** Does risk-based escalation improve blocker handling without causing excessive human-intervention requests?

The benchmark will not claim that an agent can conduct new science, write a publishable paper, outperform researchers, or generalize from synthetic packets to every research domain.

## Task corpus

Create sixteen immutable JSON task packets, grouped into four defect families with four packets each:

| Family | Packet property | Ground-truth defect |
|---|---|---|
| Citation authenticity | Source register and draft claims | nonexistent or identifier-mismatched reference |
| Claim support | Verified source excerpts and draft claims | citation exists but does not support the claim |
| Run provenance | Proposed result and run record | missing required provenance field or conflicting run identifier |
| Escalation | Protocol and incomplete/contradictory inputs | a documented blocker that requires a human decision |

Every packet has one primary defect, a machine-readable answer key, a fixed input bundle, and an allowed action set. Packets must be fictional or use only short, attributable public metadata; no private PDFs, credentials, or restricted full text may be bundled. Task construction records distinguish **valid**, **invalid**, and **ambiguous-but-escalatable** cases.

## Components and data flow

```text
immutable task packet + answer key
  -> condition-specific instruction envelope
  -> captured trace and submitted artifact bundle
  -> deterministic EviGate validators + blinded scorer
  -> raw scoring record
  -> derived summary only after all planned runs close
```

The runner writes a new directory per execution. It never overwrites an existing task packet, manifest, trace, score, seed, or answer key. A formal execution must declare its task ID, condition, seed, model/runtime identity, commit, environment lock, budget, stop condition, and output path before execution.

## Outcomes

Primary outcomes are binary per planned defect:

- **Detection**: the submitted artifact identifies the seeded defect correctly.
- **Containment**: the submitted artifact refuses to make the unsafe claim, blocks progression, or records a valid escalation.
- **Unsafe continuation**: the agent continues while accepting a seeded defect.

Secondary outcomes are:

- validator-detected provenance completeness;
- escalation precision, blocker recall, and Ask-F1;
- unnecessary escalation count;
- wall-clock duration, token or tool budget consumption when observable; and
- trace completeness.

No aggregate claim is allowed without its raw score records, run manifests, analysis configuration, and a recorded derivation.

## Design choices

Use one fixed seed per task-condition combination in the initial pilot: 16 packets × 3 conditions = 48 planned executions. The pilot is explicitly exploratory; it estimates operational feasibility and defect-level behavior rather than establishing a population effect. A later confirmatory study may add independent seeds only after a protocol amendment and human approval.

For every condition, use the same agent runtime and model configuration, a per-run 20-minute wall-clock ceiling, no external side effects, and a bounded tool budget. A runtime error, timeout, refusal, incomplete trace, or scoring failure is a preserved outcome, never a silently retried or excluded run.

## Scoring and error handling

Score deterministic fields directly from the answer key. A blinded manual reviewer resolves only clearly specified ambiguous outputs using a published rubric; the reviewer cannot see the condition label. Record disagreements and retain both the automatic and reviewer decisions. If the automated scorer and reviewer disagree, preserve the disagreement and report it; do not overwrite either record.

The benchmark runner must fail closed when the manifest is incomplete, the task checksum differs, the output path already exists, the environment lock does not match, or a task answer key is unavailable. It must record the error as a failed execution rather than attempting repair.

## Validation plan

Before formal runs, add tests that prove:

1. all sixteen task packets validate against the task schema;
2. each answer key maps to exactly one primary defect label;
3. a run cannot start without a complete manifest;
4. the scorer awards detection, containment, and unsafe continuation correctly for known fixtures;
5. duplicate run IDs and existing raw-result paths are rejected; and
6. the summary generator consumes only registered raw scoring records.

Run the complete automated suite, a smoke execution on a non-formal fixture, and a repository diff check before creating the phase-02 `PASS_CANDIDATE.json`.

## Related work used only for protocol orientation

PaperBench evaluates end-to-end AI-research replication with a large, expert-developed rubric set. Its scope and compute requirements motivate a smaller controlled pilot rather than a claim of direct comparability. [OpenAI project page](https://openai.com/index/paperbench/)

HiL-Bench operationalizes selective human escalation with metrics including Ask-F1. EviGateBench adapts the escalation concept only as a secondary workflow-control outcome. [arXiv preprint](https://arxiv.org/abs/2604.09408)

These links are discovery references for protocol design. They are not yet registered verified Source IDs and must not be cited in the manuscript until source verification is completed.

## Explicit exclusions

- No LLM-generated code execution.
- No automatic proposal acceptance or Skill self-modification.
- No use of private documents, live journal systems, credentials, or real participant data.
- No benchmark leaderboard or publication claim from pilot data.
- No transition to formal execution until the protocol, schemas, task corpus, and validation suite have passed a separate human gate.
