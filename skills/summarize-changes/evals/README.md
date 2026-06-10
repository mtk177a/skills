# summarize-changes evals

Evaluates `summarize-changes` in standalone operation. Checks whether it can produce a PR description or release handoff from a diff — including explicit impact, test status, and unconfirmed items.

## Iter 0

- `description` and body are aligned on "producing shareable summaries from a diff"
- Output follows the PR template or Release Handoff template
- Unconfirmed items are marked as unconfirmed
- Secrets are never included in the output
- Summarization without reading the diff is rejected

## Open items

- Audience-specific wording adjustment has not been tested
