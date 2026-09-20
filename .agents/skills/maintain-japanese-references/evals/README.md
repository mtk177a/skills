# maintain-japanese-references evals

This repository-local Skill is Japanese-canonical because it maintains Japanese prose.\
It was introduced by [#42](https://github.com/mtk177a/skills/pull/42); [#77](https://github.com/mtk177a/skills/issues/77) records the move to one Japanese `SKILL.md` and the required use of `write-natural-japanese`.\
Both Skills are original repository material.

This README is the only evaluation asset for the repository-local Skill.\
It records manually executed scenarios because the common Runner selects `skills/<name>`, not `.agents/skills/<name>`.\
No `evals.json`, `triggers.json`, `report.json`, or `results.json` exists here.

## Evaluation selection

The Skill maintains Japanese translations of English repository files while excluding Japanese-canonical Skills and tracker authoring.\
The current change makes `write-natural-japanese` mandatory, changes the Skill's canonical language and description, and removes its duplicate reference translation.\
Use targeted candidate checks for the required companion, natural wording, and missing-companion behavior, plus a direct routing observation for the changed description.\
Start with one candidate run per selected case, and require every critical requirement to pass before accepting the candidate.\
A critical failure blocks acceptance: correct the Skill or a defective fixture or grader, then rerun the affected case.\
Gather only the additional evidence needed to resolve an ambiguous, conflicting, or unstable result; add a baseline only when relative evidence can change acceptance, and compare another model only when distinguishing a Skill failure from a model limitation can change acceptance.

Reference environment: Codex with `gpt-5.6-luna`, medium reasoning, and a blank-slate single executor.\
Give the executor the repository-local `SKILL.md`, `write-natural-japanese` and its required reference, the scenario request, and the listed fixture files, except in the missing-companion case.\
Keep requirements and grading notes out of the executor input.

## Iter 0 — Static check

- The `description` identifies the repository, maintained inputs, intended decisions, and adjacent exclusions.
- The body defines maintained pairs, semantic-impact criteria, preservation requirements, ambiguity handling, output information, and authority boundaries.
- The `SKILL.md` is Japanese-canonical, has no duplicate `SKILL-ja.md`, and requires the repository's `write-natural-japanese` before any translation decision.
- The instructions stop the workflow and identify the unavailable file when the companion cannot be read.
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
| Required Japanese wording support is applied | Executor skips the companion or leaves unnatural translated prose | H | Successful Skill reads, pair comparison, and prose review |
| Missing companion stops the workflow | Executor makes a translation decision without the required Skill | I | File and response inspection |
| No-op decisions still use the companion | Executor skips the companion or rewrites an aligned reference | J | Successful Skill reads, diff and report inspection |
| Japanese description selects the Skill for an English-language maintenance request | Executor fails to load the Skill, or loads it for tracker authoring | K | Direct successful Skill-read events and final output inspection |

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

### Scenario G: Optional coexistence before Issue #77

Provide an English canonical document change that strengthens a requirement, its outdated Japanese reference, and both Skills.\
Ask the executor to synchronize the reference while making the Japanese sentence natural.

Requirements checklist:

1. [critical] The Japanese result preserves the strengthened requirement and changes only the affected pair.
2. [critical] Natural wording does not add or remove policy, exceptions, or uncertainty.
3. The executor treats natural wording as subordinate to source fidelity and does not treat either Skill as a required companion.

This scenario records the prior optional relationship.\
Its passing result cannot establish the current required relationship.

### Scenario H: Required companion and natural wording

Provide an English requirement change and an outdated Japanese reference whose existing sentence follows English syntax awkwardly.\
Ask explicitly for `maintain-japanese-references` and an aligned, natural Japanese update without naming its companion.

Requirements checklist:

1. [critical] The executor reads both Skill files and the wording reference required for translation.
2. [critical] The Japanese result expresses the changed obligation and conditions naturally without changing their meaning or editing unrelated files.
3. The report identifies the pair, update reason, and checks.

### Scenario I: Missing companion

Provide the repository-local Skill, an English change, and its Japanese reference, but omit `skills/write-natural-japanese/SKILL.md`.

Requirements checklist:

1. [critical] The executor stops the translation decision and makes no file edit.
2. The response identifies the missing companion file.

### Scenario J: No-op change with required companion

Provide an English source-line reflow and an aligned Japanese reference.\
Ask whether the Japanese file needs an update without naming the companion.

Requirements checklist:

1. [critical] The executor reads both Skills before deciding.
2. [critical] The Japanese reference remains byte-for-byte unchanged.
3. The report explains why no translation update is needed.

### Scenario K: Discovery after Japanese-language conversion

In a disposable repository fixture, request Japanese-reference maintenance for a changed English document in English, without naming either Skill.\
In a separate near-miss, request Issue-body authoring without a changed maintained file.

Requirements checklist:

1. [critical] The maintenance request produces a successful read of `maintain-japanese-references` and its companion before a translation decision, with selection attributable to the candidate description.
2. [critical] The Issue-only request does not select `maintain-japanese-references`.
3. A missing or incomplete read-event stream is inconclusive rather than a pass.

## Results

### Iter 1 — 2026-09-08

The uncommitted working-tree candidate later included in [#42](https://github.com/mtk177a/skills/pull/42) was evaluated once per scenario by one blank-slate Codex executor using `gpt-5.6-luna` with medium reasoning.\
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
These results supported the earlier candidate for the six mapped responsibilities and boundaries without requiring a baseline or repetition.\
Deterministic repository validation checks public Skill structure and frontmatter, this repository-local Skill's translation notice and artifact boundary, and links.\
It does not validate this Skill's frontmatter or establish behavior on other models or clients.

### Iter 2 — 2026-09-21

Scenario G was evaluated once with the candidate `SKILL.md` at `900594f5effbfbc5a93e026438aa55d0a2ad9767` and `write-natural-japanese` in a disposable fixture by Codex CLI 0.154.0 using `gpt-5.6-luna` with medium reasoning.\
The fixture contained only the two Skill sources from this public repository, the wording reference, and a synthetic English/Japanese document pair.\
The executor received the request and fixture, not the requirements checklist.

| Scenario | Result | Evidence | Decision effect |
| --- | --- | --- | --- |
| G | pass | Loaded both Skills; changed only the Japanese pair's `更新してもよい` to `更新する必要があります`; preserved the condition, scope, `pull request`, and Markdown structure | Supports coexistence without weakening canonical meaning or expanding the edit scope |

All critical requirements for the then-optional relationship passed.\
This result does not verify required use, missing-companion behavior, or discovery after the Japanese conversion.\
One initial CLI invocation using `--ignore-user-config` returned 401 before a model response; the successful run used the normal configuration.\
The common evaluation Runner currently selects `skills/<name>`, so this repository-local Skill was evaluated in a disposable directory rather than through that Runner.\
The canonical and Japanese frontmatter were checked directly for required fields, name/directory match, and field lengths.\
No baseline, repeated run, or other client was needed to resolve that earlier change's acceptance question; those paths remain unverified.

### Iter 3 — 2026-09-21

The Japanese-canonical candidate was exercised in disposable directories with Codex CLI 0.154.0, `gpt-5.6-luna`, medium reasoning, and one executor per run.\
The local Skill, companion, wording reference, and synthetic document pair were copied from this repository; case I intentionally omitted the companion.\
The executor did not receive the requirements checklist.\
The common Runner cannot plan this repository-local Skill, so the direct command and file events were reviewed manually.

H and J used Skill SHA-256 `d08754c2b81fb6056d3dcf7f8f1bc075228623ee98969d604557f6c5df426ab0`.\
I and K used the final candidate SHA-256 `30eb36bf5df84d48b4d326b18891553de526d073b2ab85d1b92a1fe41938105c`.\
The only Skill change between those hashes clarified that a missing repository companion cannot be replaced by a personal copy; it does not change the present-companion path tested by H and J.

| Scenario | Result | Direct evidence | Decision effect |
| --- | --- | --- | --- |
| H | pass after correction | The executor read both repository Skill files and the full wording reference, changed only the Japanese document, preserved `must` and the pre-merge condition, and replaced the unnatural `更新を提供` phrasing with `更新する` | Supports required use and faithful, natural output when the companion exists |
| I | pass after correction | With the repository companion absent, the executor reported the missing files and made no edit | Supports the missing-companion stop rule |
| J | pass | The executor read both repository Skill files, left the aligned Japanese document byte-for-byte unchanged, and explained the source-line reflow | Supports required use during a no-op decision |
| K maintenance request | inconclusive for discovery | The executor read the repository-local Skill and companion and updated the Japanese document, but a personal copy with the same Skill name was loaded first | Cannot attribute initial selection to the Japanese candidate description |
| K Issue-only near-miss | pass | A complete turn produced an Issue draft with no read of `maintain-japanese-references` | Supports the tracker-authoring exclusion in this environment |

The first H run produced a faithful and natural translation but did not read the wording reference.\
The Skill was changed to require that read explicitly, and the affected case passed on rerun.\
The first I run substituted a personal copy of the missing companion and edited the translation.\
The Skill was changed to prohibit that substitution, and the affected case passed on rerun.\
An initial CLI launch could not write its local state database, before any executor response; the evaluation runs above completed after using the permitted execution environment.

No baseline or repeated success run was needed for H, I, or J after the observed defects were corrected.\
Automatic discovery from the Japanese description alone, other clients and models, and unselected historical scenarios remain unverified.\
An isolated environment without a same-named personal Skill would make another routing observation decision-relevant.

## Next validation question

- If real use reveals a critical failure, correct the identified Skill, fixture, or grader defect and rerun the affected case before acceptance.
- If a result is ambiguous, conflicting, or unstable, gather only the additional evidence needed to resolve the acceptance decision; compare models only when model-specific support or a Skill-versus-model distinction is material.
