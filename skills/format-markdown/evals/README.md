# format-markdown evals

Evaluates `format-markdown` in standalone operation. Checks whether it can reformat Markdown for consistency without changing the content — and refuse to scope-creep into rewriting.

## Iter 0

- `description` and body are aligned on "Markdown formatting, not content rewriting"
- Heading hierarchy is corrected without content changes
- Tables and lists are normalized
- Content rewrite requests are declined as out of scope

## Open items

- Edge case: what counts as "formatting" vs "clarification of wording" has not been tested
