# Manuscript integrity report

## Scope

Audit target: `paper/EviGateBench_v0.2.md`.

## Citation checks

| Citation key | Source record | Result |
|---|---|---|
| `starace2025paperbench` | `SRC-PAPERBENCH-2025` | PASS: task/rubric framing is within declared support scope. |
| `trinh2026hilbench` | `SRC-HILBENCH-2026` | PASS: blocker and Ask-F1 framing is within declared support scope. |
| `liu2024agentbench` | `SRC-AGENTBENCH-2024` | PASS: eight-environment framing is within declared support scope. |

The manuscript contains three citation keys and all three occur in
`sources/VERIFIED_SOURCES.bib`. No orphaned citation was found.

## Quantitative claim checks

| Claim ID | Manuscript use | Run evidence | Result |
|---|---|---|---|
| CLM-004 | EviGate controller rates | 16 EviGate v0.2 Run IDs | PASS, but simulation-only. |
| CLM-005 | Direct controller rates | 16 Direct v0.2 Run IDs | PASS, but simulation-only. |
| CLM-006 | Linear controller rates | 16 Linear v0.2 Run IDs | PASS, but simulation-only. |

The results table matches `analysis/formal-v0.2/summary.json`. All numerical
language is explicitly limited to deterministic reference-controller
simulation. The paper makes no model-performance, causal, statistical, or
real-world reliability claim.

## Required disclosures

Data availability, ethics, author contributions, conflict of interest,
funding, limitations, and AI-use disclosure are present.

## Decision

**Integrity pass for an audited technical-report draft.** It is not
submission-ready as an empirical claim about LLM research agents because it
does not include independent model rollouts, blind human evaluation, or a
non-synthetic task suite.
