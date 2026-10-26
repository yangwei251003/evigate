# Evidence registry search log

## Scope

This registry supports the systems-and-benchmark paper's background and metric
definitions. It does not support any EviGate outcome, because no formal
execution has occurred.

## Verified sources

| Source ID | Discovery route | Authoritative locator | Verification result |
|---|---|---|---|
| `SRC-PAPERBENCH-2025` | PaperBench benchmark query | arXiv record and OpenAI project page | title, authors, date, task count, rubric count, and reported score verified |
| `SRC-HILBENCH-2026` | selective-escalation benchmark query | arXiv v4 record | title, authors, blocker definition, and Ask-F1 definition verified |
| `SRC-AGENTBENCH-2024` | agent benchmark query | ICLR 2024 proceedings | title, venue, authors, and eight-environment description verified |

## Exclusions

- Search-result snippets, repository descriptions, and third-party news were
  used only for discovery and are not Source IDs.
- No full text, private PDF, API key, or restricted dataset was stored.
- Sources not listed in `sources/records/` may not support manuscript claims.
