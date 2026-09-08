# maintain-japanese-references evals

## Evaluation selection

The Skill adds a translation-maintenance responsibility and a discovery boundary beside Japanese-canonical Skills and tracker authoring.\
Use targeted candidate-only behavior checks for semantic decisions and targeted routing checks for the adjacent boundaries.\
Start with one candidate run per selected case, and require every critical requirement to pass before accepting the candidate.\
A critical failure blocks acceptance: correct the Skill or a defective fixture or grader, then rerun the affected case.\
Gather only the additional evidence needed to resolve an ambiguous, conflicting, or unstable result; add a baseline only when relative evidence can change acceptance, and compare another model only when distinguishing a Skill failure from a model limitation can change acceptance.

Reference environment: Codex with `gpt-5.6-luna`, medium reasoning, and a blank-slate single executor.\
Give the executor only `SKILL.md`, the scenario request, and the listed fixture files.\
Keep requirements and grading notes out of the executor input.

## Iter 0 — Static check

- The `description` identifies the repository, maintained inputs, intended decisions, and adjacent exclusions.
- The body defines maintained pairs, semantic-impact criteria, preservation requirements, ambiguity handling, output information, and authority boundaries.
- The Skill is self-contained and does not require `japanese-tech-writing` or another companion Skill.
- Violations marked `[critical]` below would produce an incorrect translation, an unauthorized change, or a responsibility-boundary failure.

## Coverage map

| Claim | Plausible failure | Scenario | Grader |
| --- | --- | --- | --- |
| Normative meaning is preserved | Translation weakens a requirement or drops an exception | A | Maintainer review against the canonical diff |
| Non-semantic edits do not create churn | Japanese file receives a no-op rewrite | B | Diff inspection and report check |
| Japanese-canonical Skills are excluded | Executor creates a duplicate `SKILL-ja.md` | C | File and report inspection |
| Tracker authoring does not activate this workflow | Executor drafts or translates tracker content | D | Output inspection |
| Changed pairs constrain the edit scope | Unrelated translations are modified | E | Diff inspection |
| Established terminology is preserved | Executor replaces an established term without evidence | F | Pair comparison and report inspection |

## Scenarios

### Scenario A: Normative semantic change

Provide an English canonical Skill diff that changes a `should` to `must` and narrows an exception, together with its current Japanese reference.\
Ask the executor to maintain the Japanese reference.

Requirements checklist:

1. [critical] The Japanese result preserves the stronger requirement and narrowed exception.
2. [critical] No English canonical content is changed and no new policy is invented.
3. The report identifies the pair and the semantic reason for the update.

### Scenario B: Non-semantic canonical edit

Provide a canonical diff limited to whitespace or source-line reflow that leaves rendered content and meaning unchanged, together with an aligned Japanese reference.

Requirements checklist:

1. [critical] The Japanese reference remains byte-for-byte unchanged.
2. The report records why no translation update was needed.

### Scenario C: Japanese-canonical Skill

Provide a documented Japanese-canonical writing Skill whose `SKILL.md` changes and has no `SKILL-ja.md`.\
Ask the executor to synchronize translations affected by the diff.

Requirements checklist:

1. [critical] No `SKILL-ja.md` is created or proposed.
2. The report identifies the Skill as outside this workflow.

### Scenario D: Tracker near-miss

Ask for a Japanese body for an Issue that already has an English title and `Summary`, without providing a changed maintained file.

Requirements checklist:

1. [critical] The executor does not apply this Skill to author or translate the Issue.
2. The response routes the request outside this workflow without changing repository files.

### Scenario E: Multiple changed files

Provide changed English canonical files for one document and one public Skill, aligned translations for both, and an unrelated translation pair.\
Make one canonical change semantic and the other non-semantic.

Requirements checklist:

1. [critical] Only the translation paired with the semantic change is modified.
2. Both changed pairs are reported, including the no-update reason.
3. The unrelated pair is not edited.

### Scenario F: Established terminology

Provide a canonical change, its Japanese counterpart, and nearby Japanese references that consistently retain an English technical term.\
Ask the executor to synchronize the pair.

Requirements checklist:

1. [critical] The established term is retained unless the canonical meaning requires a different term.
2. If the evidence supports multiple materially different translations, the executor reports the ambiguity instead of choosing silently.

## Results

### Iter 1 — 2026-09-08

The uncommitted working-tree candidate was evaluated once per scenario by one blank-slate Codex executor using `gpt-5.6-luna` with medium reasoning.\
The executor received `SKILL.md` and the six scenario inputs, did not receive the requirements or grading notes, and did not edit repository files.

| Scenario | Result | Evidence | Decision effect |
| --- | --- | --- | --- |
| A | pass | Preserved `must`, the explicit-request condition, and the requirement to disclose risk without changing canonical content | Supports acceptance of normative-meaning preservation |
| B | pass | Left the Japanese reference unchanged and reported source-line reflow as non-semantic | Supports acceptance of no-op handling |
| C | pass | Excluded the documented Japanese-canonical Skill and did not propose `SKILL-ja.md` | Supports acceptance of the Japanese-canonical exclusion |
| D | pass | Declined Issue authoring as outside the workflow and made no repository change | Supports acceptance of the tracker-authoring boundary |
| E | pass | Updated only the semantically affected translation, reported the reflow-only pair unchanged, and left the unrelated pair untouched | Supports acceptance of pair-scoped editing |
| F | pass | Preserved the established term `pull request` and reported no ambiguity | Supports acceptance of established-terminology preservation |

Maintainer review found no critical or non-critical requirement failure.\
These results accept the candidate for the six mapped responsibilities and boundaries without requiring a baseline or repetition.\
Deterministic repository validation checks structure, frontmatter, translation notices, links, and repository-local artifact boundaries but does not establish behavior on other models or clients.

## Next validation question

- If real use reveals a critical failure, correct the identified Skill, fixture, or grader defect and rerun the affected case before acceptance.
- If a result is ambiguous, conflicting, or unstable, gather only the additional evidence needed to resolve the acceptance decision; compare models only when model-specific support or a Skill-versus-model distinction is material.
