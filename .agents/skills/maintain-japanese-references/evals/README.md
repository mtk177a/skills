# maintain-japanese-references evals

## Purpose and assets

This repository-local Skill maintains Japanese references when English repository files change, and it requires the repository's `write-natural-japanese` before a translation decision.\
[#77](https://github.com/mtk177a/skills/issues/77) covers its Japanese `SKILL.md`, required companion, and discovery boundary.

| Asset | Role |
| --- | --- |
| `evals.json` | Executable behavior cases H, I, and J. |
| `triggers.json` | Executable routing cases for K maintenance and Issue-only authoring. |
| `README.md` | Coverage, method, results, and limits across the evaluation paths. |

There is no `report.json` because behavior, routing, and the focused I retry have separate plans and reports.\
There is no `results.json`; earlier manual observations are recorded below.\
The case prompts, fixtures, expected handlers, and assertions live in the JSON definitions.

## Coverage and grading

| Responsibility or boundary | Failure to expose | Case or check | Evidence |
| --- | --- | --- | --- |
| Required companion and faithful Japanese | Skips the companion or weakens an obligation | H | Completed reads of both repository Skills and the full wording reference before editing; English unchanged; Japanese diff. |
| Missing companion | Uses a personal replacement or edits anyway | I | Catalog isolation, candidate read, no Japanese edit, and missing-file response. |
| Meaning-preserving source edit | Rewrites an aligned reference or skips the companion | J | Both Skill reads, Git diff, and no-update reason. |
| English maintenance request | Fails to select the candidate or edits beyond the changed pair | K maintenance | Complete event stream, observed handlers, successful reads, and document diff. |
| Issue authoring exclusion | Applies reference maintenance to an Issue draft | K Issue-only | Complete event stream with no candidate read and no file edit. |
| Package and definition consistency | Malformed metadata, links, or evaluation definitions | Repository checker | `python3 -B scripts/check_repository.py`. |

Historical manual cases A–F covered normative meaning, no-op edits, Japanese-canonical exclusion, tracker authoring, edit scope, and established terminology.\
Historical case G covered optional coexistence before #77 made the companion mandatory.\
The new model run selected H, I, J, and K because they directly cover the changed responsibilities.

## Execution and stopping rule

Plan behavior and routing separately with `--skill-source repository-local`, the needed `--case` values, `gpt-5.6-luna`, and `--reasoning-effort max`; inspect the model-call count before `run --execute`.\
The Runner binds the candidate, definitions, case files, and companion files by hash, then creates a disposable fixture for each case.\
For H, I, J, and K maintenance, the fixture commits the previous document text and applies the current text so the executor can inspect a real Git diff.\
It places the `write-natural-japanese` package only in cases that require the companion; its bundled reference is available there.\
It keeps normal Codex authentication, disables personal copies of the candidate and required companion plus plugins for the invocation, and checks the model-visible Skill catalog before a model call.\
A missing, shortened, duplicated, or wrongly located candidate description, or a visible personal companion without a fixture copy, stops execution.

The model receives the case request and fixture, not the grading requirements.\
Grade the planned requirements from completed events, successful reads, the final response, and file diffs.\
A missing `turn.completed` or incomplete read evidence is inconclusive; a critical failure is not a pass.\
Correct an observed fixture, isolation, or Skill defect and plan only the affected retry before another model call.

## Current evidence: 2026-09-21

The [PR #84](https://github.com/mtk177a/skills/pull/84) candidate was evaluated from branch head `cd6e95acf6b3c383b6f77f3d215762e84f954cac` with uncommitted Runner and definition changes.\
The candidate `SKILL.md` hash was `sha256:30eb36bf5df84d48b4d326b18891553de526d073b2ab85d1b92a1fe41938105c` in all three plans.\
The environment was Codex CLI 0.154.0, `gpt-5.6-luna` with `max` reasoning, normal authentication, and one disposable workspace per execution.\
The behavior plan selected H, I, and J for three calls with digest `sha256:e169a98025107496bf3a3555268ce532b1afbade31a00ddc5b53e5fbeba86959`.\
The routing plan selected K maintenance and K Issue-only for two calls with digest `sha256:3bd5ee3d0412c1389dc406f98f759ea4951789df4a8096e78dc809a04feaf22d`.\
Requirements, call counts, candidate hash, and stopping conditions were recorded before any model execution.

The first behavior launch stopped before a model call because the sandbox could not inspect the Codex Skill catalog.\
The same plan then produced complete H, I, and J turns.\
H and J passed.\
The first I turn stopped without editing, but read a personal `write-natural-japanese` because the isolation setting only disabled companions present in that fixture; it failed isolation.\
The Runner was corrected to disable that personal Skill even when absent from the fixture and to reject its presence during catalog preflight.\
A one-call I retry plan with digest `sha256:e6914eac53fce32ba9f2cde22654e4de6fba65b1c7e306dfb880c40b1e4de85a` was recorded before the retry.\
The completed retry passed: the personal companion was absent from the catalog, no personal copy was read, the Japanese file stayed unchanged, and the missing repository file was reported.\
The routing plan then ran once per case and both cases passed.\
Six model calls were made in total: the original five plus the focused I retry.

| Case | Result | Observed evidence |
| --- | --- | --- |
| H | Pass | Read the candidate, companion, and entire wording reference before editing; changed only the Japanese document from permission to obligation while retaining the condition and pre-merge deadline. |
| I, first run | Fail | Stopped without editing but read a personal companion that was visible in the catalog. |
| I, retry | Pass | No personal companion was visible or read; reported the missing repository file and made no Japanese edit. |
| J | Pass | Read both Skills, left the aligned Japanese document unchanged, and explained that source-line reflow did not change meaning. |
| K maintenance | Pass | `turn.completed` and successful reads identified the fixture candidate and companion; the full wording reference was read; only the Japanese document was edited. |
| K Issue-only | Pass | `turn.completed` showed no maintenance Skill read; the executor drafted an Issue body without editing files. |

The temporary machine-graded reports record H/J as pass and initial I as fail, I retry as pass, and both K cases as pass.\
The repository checker passed during each completed run.\
Plans, raw events, and grading files remain outside the repository; this README preserves their decision-relevant results without combining distinct paths into one report.

## Earlier evidence and limits

On 2026-09-08, six manual A–F scenarios passed with an uncommitted candidate for [PR #42](https://github.com/mtk177a/skills/pull/42), `gpt-5.6-luna`, and medium reasoning.\
On 2026-09-21, manual G passed with candidate `900594f5effbfbc5a93e026438aa55d0a2ad9767`, and manual H, I, J, and K work used medium reasoning before the executable definitions existed.\
The first manual H missed the wording reference and the first manual I used a personal replacement; the Skill instructions were corrected and affected cases subsequently passed.\
A later isolated manual K maintenance run read the repository candidate and companion and updated only Japanese; its prior no-Git attempt had been inconclusive.\
Those observations informed the new cases, but there is no preserved evidence that the earlier H, I, and J runs had pre-execution plans.\
The new plans do not retroactively establish those earlier procedures.

The current results cover this candidate and these fixtures in Codex CLI with Luna max.\
Other models and clients, a baseline comparison, repeated successful runs, and unselected historical cases remain unverified.\
New evidence is needed if real use reveals a critical failure, an environment-specific issue, or instability that would change acceptance.
