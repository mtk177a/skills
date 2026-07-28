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

- The balance between asking for more information and producing a partial draft has been tested only for one highly underspecified bug report.

## Iter 1 — 2026-07-28

- Client: Codex CLI 0.145.0
- Model / reasoning: `gpt-5.6-sol` / high
- Candidate `SKILL.md`: `sha256:86d67d201c71dca806204909509e1dbf844f893fd8a430b822671c613f48a826`
- Targeted scenario: Scenario C only, after replacing the retired `scope-request` dependency with an iterative `clarify-request` handoff
- Observable loads: `draft-issue`, then `clarify-request`
- Result: pass; the response kept the Issue unposted, asked for the repository, issue type, export target, reproduction, expected and actual behavior, and environment, and did not invent error codes, file paths, line references, or reproduction details
- Unverified: Scenarios A and B were not rerun because their drafting contract was unchanged; duplicate and template checks against a real tracker were not executed; Claude and other clients were not executed
- Next validation question: After several clarification turns, does `draft-issue` resume with a self-contained draft without dropping earlier confirmed details?
