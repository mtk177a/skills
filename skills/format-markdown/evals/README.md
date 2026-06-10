# format-markdown evals

## Iter 0 — Static check

- description and body are internally consistent on "Markdown formatting, not content rewriting"
- heading hierarchy is corrected without content changes
- tables and lists are normalized
- content rewrite requests are declined as out of scope
- at least one `[critical]` assertion is identified: content rewrite requests are refused

## Scenarios

### Scenario A: Broken heading hierarchy

A Markdown document has a heading hierarchy that skips levels (e.g., H1 followed by H3, then H2). The skill must correct the structure without changing any text content.

Requirements checklist:
1. [critical] Heading levels are adjusted to maintain proper hierarchy
2. No content text is changed or rewritten
3. No indication that a rewrite was performed

### Scenario B: Inconsistent list formatting

A Markdown list mixes bullet styles (`-` and `*`) and has inconsistent indentation. The skill must normalize the list style and indentation without altering content.

Requirements checklist:
1. [critical] List style is made consistent throughout
2. Content of list items is unchanged
3. No content changes are made or announced

### Scenario C: Content rewrite request declined (boundary)

A request combines formatting with a content change (e.g., "also make section 2 clearer"). The skill must apply formatting only and decline the content rewrite portion as out of scope.

Requirements checklist:
1. [critical] The content rewrite portion is declined or noted as out of scope
2. No rewritten version of the requested section is produced

## Failure Pattern Ledger

- `content rewritten under the guise of formatting`
- `scope creep accepted without flagging`
- `heading hierarchy change alters meaning`
- `list normalization changes item content`

## Open items

- Edge case: what counts as "formatting" vs "clarification of wording" has not been tested
