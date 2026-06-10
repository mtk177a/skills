# summarize-changes evals

## Iter 0 — Static check

- description and body are internally consistent around "producing shareable summaries from a diff"
- output follows the PR template or Release Handoff template
- unconfirmed items are marked as unconfirmed
- secrets are never included in the output
- summarization without reading the diff is rejected
- at least one `[critical]` assertion is identified

## Scenarios

### Scenario A: PR description from a diff

A concrete code diff is provided. Produce a PR description that includes a summary section, does not contain secrets, and does not assert implementation intent beyond what the diff shows.

Requirements checklist:
1. [critical] Output includes a Summary section
2. No secrets or credentials appear in the output
3. Does not fabricate implementation steps not present in the diff

### Scenario B: Release handoff notes with unconfirmed items

A verbal description of changes is provided along with a known TBD item. Release notes must surface the unconfirmed item explicitly.

Requirements checklist:
1. [critical] Unconfirmed or TBD items are explicitly labeled as remaining
2. The specific TBD detail is preserved in the output, not silently dropped

### Scenario C: Boundary — no diff provided

A request to write a PR summary arrives with no diff. Should ask for the diff, not fabricate a summary.

Requirements checklist:
1. [critical] Does not fabricate summary content when no diff is provided
2. Does not begin output with "The PR adds" or "This change fixes" without evidence

## Open items

- Audience-specific wording adjustment has not been tested

## Failure Pattern Ledger

- `summary fabricated without diff`
- `unconfirmed items omitted`
- `secrets included in output`
