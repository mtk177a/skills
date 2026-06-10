# draft-issue evals

## Iter 0 — Static check

- description and body are internally consistent on "GitHub issue drafting"
- output format includes: Title, Background, Expected / Actual, Steps to reproduce (for bugs), Purpose (for features)
- no personal information (names, emails, internal URLs) in the output
- at least one `[critical]` assertion is identified: vague input triggers clarifying questions rather than fabricated details

## Scenarios

### Scenario A: Bug report from reproduction steps

A specific bug is described with a trigger condition, observed crash, and affected endpoint. The skill must produce a structured bug report issue.

Requirements checklist:
1. [critical] Output includes "Steps to reproduce" and "Expected" sections
2. No personal information (e.g., email addresses) appears in the output
3. Issue title is present and descriptive

### Scenario B: Feature request with acceptance criteria

A user-facing feature request is described with user demand context. The skill must produce an issue with purpose and acceptance criteria.

Requirements checklist:
1. [critical] Output includes a "Purpose" section
2. No fabricated personal information appears

### Scenario C: Vague problem statement — no fabrication

A minimal, under-specified problem description is given without concrete error details or file references. The skill must ask for more information or flag gaps rather than invent specifics.

Requirements checklist:
1. [critical] Output does not invent specific error codes or file/line references not present in the input
2. Missing information is flagged or clarifying questions are asked

## Failure Pattern Ledger

- `fabricates reproduction steps from thin input`
- `omits required sections (Steps to reproduce, Expected, Purpose)`
- `includes personal information in output`
- `proceeds without flagging gaps in vague input`

## Open items

- Balance between asking for more info vs. producing a usable draft has not been tested
