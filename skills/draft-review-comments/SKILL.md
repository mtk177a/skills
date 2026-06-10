---
name: draft-review-comments
description: Turn organized findings into GitHub PR inline comments and a review summary.
license: MIT
---

# Draft Review Comments

## Purpose

- Convert already discovered and organized findings into review comment drafts that can be pasted into a GitHub PR.
- Organize the code location for each comment, how to split comments, and the structure of the review summary.
- Attach `must` / `should` / `suggestion` / `question` / `nit` / `note` labels to inline comment bodies; make the review summary a concise overall judgment that includes well-grounded positives and the remaining key actions.
- Keep the accuracy of findings and next actions while making it easy for the reviewee to decide and collaborate.

## When to use

- When you want to turn results from `review-changes` or `triage-review-feedback` into GitHub comments
- When you want to organize your own review findings into inline comments and a review summary
- When doing a re-review and need to return `Resolved` / `Remaining` / `New` organized
- When wording needs to include fix timing for a PR with predecessor/successor context
- When approving while leaving non-blocking comments or notes

## Input (optional)

- Finding content
- Target code location
- Label (`must` / `should` / `suggestion` / `question` / `nit` / `note`)
- Labels received from an upstream Skill (`Must-fix` / `Should-fix` / `Nice-to-have`) — these can be accepted
- Context:
  - Initial review / re-review
  - PR with predecessor/successor context / normal PR
  - Whether a fix can go in a follow-up PR
  - Desired tone (`gentle` / `standard` / `firm`); default is `gentle` when unspecified
  - Specified commit range / effective diff
- Previous findings list or summary of the current diff if needed
- Positives to include in the review summary if needed

## Steps

1. Break findings into one comment per concern.
2. If multiple symptoms come from the same root cause, combine them into one concern if that makes the reviewee's next action clearer.
3. For each finding, choose the minimal natural comment location, preferring the direct cause line over the result line.
4. Use `path:line` for a single line; use `path:start-end` when the concern spans a multi-line expression, conditional branch, function call, or an entire add/delete block.
5. Re-confirm each comment location just before producing the inline comment drafts.
6. When a PR has predecessor/successor context, a commit range, or an effective diff is specified, anchor positions and evidence to that range only.
7. Choose whether to return each finding as an inline comment, review summary, or general comment.
8. In the review summary, briefly state well-grounded positives first, then remaining key actions.
9. Attach a canonical label at the start of each inline comment body.
10. Structure comments as `fact → impact → expectation`.
11. Be unambiguous about whether a response is required, recommended, or optional.
12. Avoid over-specifying solutions; leave room for the reviewee to choose a better implementation.
13. Use code, behavior, and diff as the subject — not the person.
14. Avoid abstract phrases; explicitly state the needed identifiers, conditions, and value transitions.
15. When tone is unspecified, default to `gentle`: write observed fact → brief reason or impact → expected fix or confirmation.
16. In `gentle` tone, avoid interrogative pressure; when intent can be inferred, briefly acknowledge it before connecting to the concern and suggestion.
17. Adjust label strength through wording and request expressions.
18. Use assertion, concern language, or a confirmation question according to the strength of evidence.
19. Treat preference-level comments as suggestions, not blockers.
20. In re-reviews, first organize `Resolved` / `Remaining` / `New`.
21. For PRs with predecessor/successor context, include whether the fix goes in this PR or a preceding/following PR.
22. Write `must` findings at a granularity where it is clear what needs to be fixed to close the finding.
23. Review summaries and approval supplement comments should be returned as a short overall judgment, not a detailed label-by-label breakdown.

## Comment type guide

- Inline comment: local implementation problems, concerns where the direct cause can be identified
- Review summary: overall judgment, merge readiness, remaining key actions (1–3 sentences or at most 3 bullets)
- General comment equivalent: decisions to send to a follow-up PR, non-blocking comments left while approving

## Certainty guidelines

- Reproduced, clear spec basis, confirmed impact: assertion is appropriate
- Static reading, impact strongly inferred but not reproduced: use language like "appears to" / "seems like it would"
- Spec assumptions or intent unconfirmed: lean toward a confirmation question
- Do not mix facts, preferences, and best-practice suggestions; separate them in the comment when needed
- Severity and certainty are different axes; even a `must` should not be stated with false certainty if the premise is uncertain

## Label vocabulary

- `must`: fix required before merge; do not approve if this remains
- `should`: fix recommended in principle; discussion allowed with reason
- `suggestion`: improvement proposal; better but not required
- `question`: insufficient understanding, intent confirmation, or potential concern check
- `nit`: minor comment; optional by default
- `note`: reference information; no response needed
- Upstream labels: `Must-fix` → `must`, `Should-fix` → `should`, `Nice-to-have` → `suggestion` or `nit`
- Always use canonical labels in inline comment bodies
- In review summaries, avoid detailed per-label breakdowns; write only well-grounded positives, overall judgment, and key actions

## Comment wording policy

- Direct comments at code behavior, maintainability, and spec misalignment — not the reviewer's capabilities or attitude
- Write so that the required fix and reason are clear quickly — not so that strong accuracy means harsh wording
- `must` must not be ambiguous about the required fix, but do not use blaming or interrogative language
- `should` should include the reason while leaving room to discuss alternatives or constraints
- `suggestion` / `nit` / `note` should use wording that makes clear they do not block merge
- `question` should be written as a question, not a hidden requirement
- When specifying a solution, use "for example" if the reviewee might choose a better implementation
- Keep educational or background-sharing content minimal so the current next action is not buried
- Positives should point at observable facts in code, design, tests, or diff organization — not the reviewer's personal evaluation

## Output format

- Inline comment drafts:
  - Comment location: `path:line` or `path:start-end`
  - Comment body: `must: ...`
- Review summary draft:
  - Positives: ...
  - Remaining key actions: ...
- General comment equivalent:
  - ...
- Tone variations if needed:
  - Gentle: ...
  - Standard: ...
  - Firm: ...
- Approval supplement comment draft if needed:
  - ...
- Comment structure notes:
  - Concerns to split / concerns to combine / concerns to send to a follow-up PR

## Companion skills

- `review-changes`
- `triage-review-feedback`

## Boundaries

### Always:

- One comment per concern
- Combine same-root-cause concerns only when it does not increase noise
- When a commit range or effective diff is specified, anchor positions and evidence to that range
- Do not force a natural multi-line concern into a single line
- Structure comments as `fact → impact → expectation`
- Attach a canonical label at the start of each inline comment body
- Use code, behavior, and diff as the subject — not the person
- Do not obscure with abstract language; explicitly state needed identifiers and conditions
- In the review summary, briefly include well-grounded positives; do not bury key actions
- Default tone is `gentle`; avoid pressure-creating wording or interrogative language
- Do not treat non-blocking concerns as blockers
- Write with the assumption that the author may have intent or constraints; briefly acknowledge when helpful
- Do not treat preferences as blockers
- Match certainty of assertion to strength of evidence
- Write at a granularity where the next action is clear
- For inline comments, return target location and comment body as a set ready to paste into GitHub

### Ask first:

- When the validity of the finding itself is unconfirmed
- When comment location candidates are ambiguous and the choice changes the meaning

### Never:

- Discover new bugs
- Decide the accept/reject of a finding
- Perform implementation fixes
- Use wording that blames the author's capabilities or attitude
- Use interrogative or pressure-creating language when tone is unspecified or set to `gentle`
