# draft-review-comments evals

## Iter 0 — Static check

- description and body are internally consistent on "drafting review comment text"
- scope is limited to formatting pre-organized findings into GitHub PR comments — no new finding discovery or accept/reject decisions
- each line comment returns position and comment body as a pair
- `path:line` and `path:start-end` are used appropriately depending on range
- each line comment body starts with a canonical label
- `must` / `should` / `suggestion` / `question` / `nit` / `note` differences are reflected in the comment text
- input labels `Must-fix` / `Should-fix` / `Nice-to-have` are accepted and mapped to canonical labels
- assertion strength is proportional to evidence strength
- line comment / review summary / overall comment types are used distinctly
- review summary and overall comments do not force a position
- review summary remains a brief overall judgment, not a label-by-label detail list
- review summary includes at least one evidence-backed positive point
- related findings are aggregated without excess or omission
- `Approve with comments` text does not read as a de facto blocker
- `Nice-to-have`-level items do not read as merge blockers
- default tone is non-pressuring even without a tone specification
- comments are directed at code behavior and next action, not at the author's ability or attitude
- at least one `[critical]` assertion is identified per scenario

## Scenarios

### Scenario A: First-review comment drafts

Two or three findings with target positions and labels are provided, including a strong-evidence `must`, a static-analysis-based `should`, and a minor `Nice-to-have` suggestion.

Requirements checklist:
1. [critical] Each line comment body starts with a canonical label
2. Position and comment body correspond to each other
3. Expected action is clear from each comment
4. Static-analysis-based findings avoid over-assertion
5. `Nice-to-have`-level items return with `suggestion` or `nit` tone that does not block merging
6. Each comment covers exactly one point

### Scenario B: Re-review organization

A summary of previous findings and current diff is provided. `Resolved` / `Remaining` / `New` categories must be distinguished in the comment drafts and review summary. Includes a point where approving with a supplementary comment is appropriate.

Requirements checklist:
1. [critical] `Remaining` is not confused with `New`
2. `Resolved` items are not re-raised unnecessarily
3. Review summary includes a concise state-diff
4. Approval supplementary comment does not read as a merge blocker
5. Review summary and supplementary comments do not force a position reference
6. Review summary does not become a label-by-label detail list

### Scenario C: Follow-up allowance for chained PRs

A PR branched from a feature or issue branch contains points that originated in this PR but could reasonably be fixed in a follow-up PR. Includes cases where an overall comment is more natural than a line comment.

Requirements checklist:
1. [critical] It is clear whether a point is required now or allowed in follow-up
2. Non-blocking points are not escalated
3. The reason for deferring to a follow-up PR is stated
4. An overall comment without a position reads naturally when that form is chosen

### Scenario D: Aggregation of shared root cause

Two symptoms arise from the same root cause; commenting separately would add noise.

Requirements checklist:
1. [critical] The two symptoms are consolidated into one point based on root cause
2. Consolidation does not make the next action ambiguous
3. Comment position is placed at the direct cause line, not the symptom line

### Scenario E: Concrete condition specificity

A finding about a conditional branch or null check is drafted as a comment. The comment must include the relevant identifier or condition expression rather than abstract references like "this condition."

Requirements checklist:
1. [critical] Comment reads in the order: expected result, current behavior, concrete condition
2. Identifiers or condition expressions are specified where necessary
3. Specificity does not make the comment excessively verbose

### Scenario F: Comment position anchored to a specified diff

The PR involves chained branches or an explicitly specified diff range; line numbers and cause locations differ in the current working tree versus the specified range. Comment positions, type names, and cause explanations must be anchored to the specified commit range.

Requirements checklist:
1. [critical] `path:line` or `path:start-end` matches a position in the specified diff
2. Current working tree state or adjacent PR state is not mixed into the rationale
3. The direct cause line is prioritized
4. Type names and diff descriptions in the comment body are consistent with the specified range

### Scenario G: Multi-line comment position

A finding whose root cause spans multiple lines (a multi-line condition, function call, or added/deleted block) is drafted as a comment. The skill must return a range rather than collapsing to a single line when appropriate.

Requirements checklist:
1. [critical] If the entire range is the point, `path:start-end` is returned
2. Points that need only a single line are not unnecessarily range-specified
3. One comment still covers exactly one point even with a range
4. The comment body corresponds to the expression, condition, or block within the range

### Scenario H: Default soft tone

A mix of `must` / `should` / `suggestion` / `question` / `nit` / `note` findings is formatted without a tone specification. Correctness and expected actions must be preserved while the default tone remains measured.

Requirements checklist:
1. [critical] Without a tone spec, comment endings are not interrogative or pressuring
2. `must` comments still have unambiguous expected actions
3. Comments are directed at the code, not the author
4. Non-blocking points do not read as de facto merge blockers
5. Short rationale or impact is included where needed
6. Comments leave room for the reviewer to choose a better implementation rather than dictating a solution

### Scenario I: Questions and reference information

Findings include a prerequisite-check `question` and a no-action-needed `note`. Neither should read as a blocking fix request.

Requirements checklist:
1. [critical] `question` does not read as an assertive fix demand
2. `note` does not appear to require action
3. Both `question` and `note` are treated as non-blocking in the review summary

### Scenario J: Concise review summary

After returning multiple line comment drafts, the review summary is limited to evidence-backed positives, an overall judgment, and key actions only — without duplicating the detail of individual comments.

Requirements checklist:
1. [critical] Review summary fits in 1–3 sentences or at most 3 bullets
2. Review summary does not become a label-by-label detail list
3. At least one evidence-backed positive point is included briefly
4. The positive point does not bury the key action
5. Line comments retain canonical labels and concrete actions
6. Merge decision and remaining key actions are clear from the summary alone

### Scenario K: No new findings introduced (boundary)

Two pre-organized findings are provided for formatting only. The skill must not introduce additional findings not present in the input.

Requirements checklist:
1. [critical] No additional findings are added beyond what was provided
2. No transition phrases implying extra discoveries appear in the output

## Failure Pattern Ledger

- `multiple points mixed into one comment`
- `comment tone stronger than the label warrants`
- `line comment body missing canonical label`
- `review summary becomes a label-by-label detail list`
- `review summary is psychologically heavy with findings only`
- `unsupported positive statement written`
- `assertion stronger than evidence`
- `comment position and body do not correspond`
- `findings with shared root cause split too finely`
- `next action dropped from review summary`
- `Approve with comments reads as a de facto blocker`
- `review summary forces path:line unnecessarily`
- `multi-line comment collapsed to single line`
- `single-line-sufficient comment unnecessarily range-specified`
- `Nice-to-have escalated to merge-blocking text`
- `follow-up allowance phrasing is ambiguous`
- `comment position anchored to working tree instead of specified diff`
- `default tone sounds stronger than intended`
- `soft-tone spec still sounds interrogative`
- `comment directed at author rather than code`
- `non-blocking text reads as a de facto blocker`
- `solution over-specified, leaving no room for reviewer judgment`
