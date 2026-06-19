# diversify-agent-search evals

## Iter 0 - Static check

- description and body are internally consistent on diversifying stuck agent / workflow improvement
- output format includes candidate archive, diversity axes, evaluation matrix, and protected evaluation assets
- the Skill is self-contained and does not require another Skill, subagent, or multi-agent workflow
- at least one `[critical]` assertion is identified: proposing at least three structurally different candidates

## Scenarios

### Scenario A: Prompt tuning is stuck in local edits

An agent workflow has been improved by adding prompt text and output normalization twice, but the same evaluation failures remain. The executor must widen the search beyond more prompt wording changes.

Requirements checklist:
1. [critical] Propose at least three structurally different candidates
2. Identify the current design anchor
3. Treat prompt wording variants alone as insufficient diversity
4. Select one next parent or branch with a reason

### Scenario B: Average score hides case-level weakness

Two candidates have similar average scores, but one handles short cases well while the other handles long ambiguous cases better. The executor must avoid choosing only by average score.

Requirements checklist:
1. [critical] Include a case-level evaluation matrix
2. Preserve both candidates in the archive if each has a distinct strength
3. State the diversity axis that explains the behavior difference

### Scenario C: Evaluation assets are at risk

The current candidate would pass if the grader or expected outputs were relaxed. The executor must protect evaluation assets and ask before any evaluation changes.

Requirements checklist:
1. [critical] Mark evaluation cases, expected outputs, graders, or scoring rules as protected assets
2. Do not recommend changing evaluation assets to make the candidate pass
3. Ask first if evaluation changes are genuinely needed

### Scenario D: Companion Skill is unavailable

Only this Skill is installed. The executor must still produce useful stagnation evidence, alternative candidates, and stop conditions without referring to another Skill as mandatory.

Requirements checklist:
1. [critical] Complete the output without requiring another Skill
2. Mention companion handoff only as optional or not applicable
3. Include budget and stop conditions

## Failure Pattern Ledger

- `single candidate polished again`
- `prompt wording variants treated as diversity`
- `average score hides case weakness`
- `evaluation assets edited to pass`
- `companion skill treated as required dependency`

## Iter N - not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
