# design-skill evals

## Iter 0 — Static check

- description and body are internally consistent on "Skill design and drafting"
- `docs/authoring.md` are treated as primary sources
- overlap check, boundary definition, and auxiliary directory judgment can all be completed standalone
- the Skill functions as a proposal-assembly tool, not a general authoring guide recap

## Scenarios

### Scenario A: New Skill draft proposal

The user wants to add a new Skill but has not settled on `name`, `description`, boundaries, or auxiliary directory necessity. The executor must summarize a proposal skeleton based on primary sources and organize it as an approval-gated diff proposal.

Requirements checklist:
1. [critical] Proposal includes primary source references, overlap check, `name`/`description`, and boundaries
2. `description` is written in terms of usage context
3. Auxiliary directory necessity is addressed with reasoning
4. No large changes are executed before approval

### Scenario B: Redesign proposal with overlap against existing Skills

The Skill being designed partially overlaps with two existing Skills, and it is unclear whether to consolidate or create a separate Skill. The executor must organize the conflicts and consolidation candidates, and return the impact scope and minimal-diff policy.

Requirements checklist:
1. [critical] Explicitly identify overlaps and consolidation candidates with existing Skills
2. Propose a minimal-diff path forward
3. Address impact scope on `AGENTS.md` / docs / scripts / `apm.yml` as needed
4. Focus on judgment material for the proposal — avoid long general-guidance recaps

### Scenario C: Abstract request — stop at purpose clarification

The user describes their desired Skill only vaguely. The executor must clarify the purpose statement before proceeding to naming or boundary definition.

Requirements checklist:
1. [critical] Fix the purpose statement before moving to naming or boundary steps
2. Do not propose a name derived from the vague description
3. Surface what information is needed to proceed

## Failure Pattern Ledger

- `authoring guidance repeated without proposal framing`
- `overlap check omitted or shallow`
- `metadata proposed without trigger-oriented description`
- `abstract request reaches naming step too early`

## Iter 1 — date unknown

### Changes
- Initial run. Skill body unchanged from Iter 0.
- Pattern applied: `(baseline)`

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|
| A | × | N/A | N/A | 0 | Understanding |
| B | ○ | N/A | N/A | 0 | — |

Note: `spawn_agent` / `wait_agent` could not retrieve `tool_uses` or `duration_ms`; steps/duration are unrecorded for this iteration. Accuracy was 87.5% for Scenario A, 100% for Scenario B.

### Structured reflection

- Scenario A:
  - Issue: When the usage context is abstract, the Skill's logic for stopping at a provisional name rather than confirming it is not easily read from the first half of the body.
  - Cause: The overlap check and primary source reference are clear, but the stop condition for abstract inputs appears after the naming step in the procedure.
  - General Fix Rule: Authoring Skills that handle abstract inputs should explicitly surface the step of fixing the usage context in one sentence before the naming step.
- Scenario B:
  - Issue: Overlap candidate organization worked, but the judgment axis for absorbing into an existing Skill relied partially on supplementary reasoning.
  - Cause: The body requires an overlap check but does not provide examples for when to absorb into an existing Skill versus creating a new one.
  - General Fix Rule: Skills that handle overlap decisions should briefly exemplify the judgment axis for absorbing into an existing Skill.

### Ledger updates

- Re-seen: `metadata proposed without trigger-oriented description` — a provisional description was used, but could not be finalized for abstract inputs
- Added: `abstract request reaches naming step too early`

### Next fix proposal

- In "When to use" and "Steps," move forward the rule that abstract inputs require fixing the usage context in one sentence and stopping at a provisional name if responsibility boundaries are not yet confirmed
