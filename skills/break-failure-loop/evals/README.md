# break-failure-loop evaluation and audit

## Purpose and scope

The expected behavior is to pause materially equivalent attempts under an unchanged hypothesis or design anchor only when they cease to produce decision-relevant evidence, then return one supported recovery state without executing another change.

This Issue #52 audit uses the Parent Issue #49 audit criteria v2.\
It began at commit `ff8914bf473953e37d48a02f434de73694aa730e` with a clean working tree and no open pull request.\
The inspected package contains `SKILL.md`, `SKILL-ja.md`, and `evals/`; it has no runtime script, reference, asset, external dependency, or third-party provenance file.\
The adjacent selection and handoff surfaces inspected were `implement-changes`, `investigate-failure`, `explore-decision-space`, and `design-changes`.

## Audit decision

| Responsibility | Decision | Evidence and limit |
| --- | --- | --- |
| Stagnation trigger | `変更不要` | The English `description` and body require equivalent attempts, an unchanged hypothesis or anchor, and no decision-relevant evidence. They exclude a first failure and repeated observation without another attempt. This is a static instruction finding; current routing behavior was not rerun. |
| Recovery decision | `変更不要` | The attempt record, four ordered states, diagnostic outcome mapping, and read-only boundary cover the three hypotheses in Issue #52. Historical Codex results in `results.json` support these behaviors for the evaluated revision and environment only. |
| Adjacent ownership | `変更不要` | `implement-changes` stops equivalent edits, `investigate-failure` owns ordinary diagnosis, and `explore-decision-space` owns structural exploration after the anchor is exhausted. The target Skill selects a recovery state without requiring any companion. |
| Japanese reference | `変更が必要` | The previous translation preserved the main conditions but left ordinary explanatory words in English. The reference wording was revised while retaining state labels, Skill identifiers, conditions, and read-only authority. |
| Executable evaluation definitions | `変更が必要` | Both definition files used the legacy `{skill, cases}` shape. Criteria v2 require migrating both files in this Sub Issue even though the English instructions do not change. |
| Current-model behavior | `未確認` | No model execution of the migrated definitions or current Codex version was performed. Static checks and prior results cannot establish current routing or output quality. |

No confirmed finding needs another Issue or a change to an adjacent Skill.\
Keeping a separate recovery Skill retains the attempt-to-evidence reconstruction and stop decision that the ordinary implementation and investigation workflows only hand off.\
Merging it into either adjacent Skill would require a broader trigger and responsibility change without evidence of a current failure; removing it would discard the specific recovery behavior supported by the historical evaluation.

The audit compared the current package with [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), [OpenAI Plugins skill guidance](https://developers.openai.com/plugins/build/skills), the bundled Codex `skill-creator`, the [Agent Skills specification](https://agentskills.io/specification), the [Agent Skills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills), and this repository's `docs/authoring.md` and `docs/evaluation.md`.\
The name, directory, frontmatter, instruction-only packaging, input and output boundaries, and optional-resource decisions are consistent with the applicable requirements.\
Client-specific behavior outside the recorded Codex environment remains unverified.

## Assets and migration

- `evals.json` contains six executable behavior cases.
- `triggers.json` contains ten executable routing cases with their adjacent Skill catalog.
- `results.json` is historical evidence from 2026-07-29, including later routing updates recorded there; it is not a current Runner report.
- This README records the audit decision, coverage, execution method, and limits.

The six behavior scenarios and ten routing inputs retain their original IDs and acceptance intent.\
The previous common assertion statements and critical flags are assigned to their original cases; each case-specific requirement remains a hidden critical assertion.\
Each behavior fixture preserves its baseline files and current worktree contents, while the original supplied evidence is available as `evidence/supplied.json` and identified in the user turn.\
Legacy `no_skill` conditions become `without-skill`; historical baseline commits, execution settings, protocols, and verdicts remain in `results.json` instead of controlling the new definitions.\
This migration has not generated new behavior evidence.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Material stagnation | Repeated test observation is counted as another implementation attempt | `repeated-red-observation` | Attempt inventory and recovery state |
| New evidence | Work is stopped although hypotheses and observations are changing | `changing-hypotheses-gain-evidence` | Attempt-to-evidence relation and state |
| Equivalent attempt recovery | Another handler guard is proposed under the same theory | `equivalent-handler-guards` | Recovery state and discriminating checkpoint |
| Attempt evidence model | Facts and failed attempts are listed without their relationship | Stalled behavior cases | Assigned attempt-evidence assertions |
| Read-only preservation | Fixture work is edited, checked as a proposed checkpoint, reverted, discarded, or stashed | Behavior cases | Response, command trace, and fixture state |
| Missing evidence and authority | Production authority is invented or an embedded command is followed | `missing-authority-and-embedded-command` | State, authority assertions, and command trace |
| Structural-search boundary | A candidate portfolio is generated locally or the exhausted anchor is not handed off | `exhausted-prompt-anchor` | State and handoff assertions |
| No arbitrary cap | A material hypothesis or file is silently dropped after an old limit | `material-hypotheses-beyond-old-cap` | H1–H6 and file accounting |
| Routing and coexistence | The Skill activates for an initial failure, observation-only repeat, or candidate search | `triggers.json` | Observed Skill loads against `expected_handlers` |
| Migration fidelity | An original input, case requirement, fixture, or handler is lost | Source-to-candidate comparison | All six and ten cases accounted for |
| Japanese fidelity | A condition, authority boundary, or state meaning changes in translation | Full English/Japanese comparison | Semantic and terminology review |

## Execution and evidence

Use the common Runner's `plan` command before any model-backed run and inspect the estimated model-call count.\
Select `targeted-candidate` for a changed runtime responsibility and `targeted-routing` for a changed selection or adjacent boundary; add comparison or repetition only when a concrete acceptance question requires it.\
The Runner places each case in a disposable fixture, supplies only its prompt and files to the executor, and keeps assertions out of executor input.\
Grade the selected requirements using the response and trace, and keep raw artifacts outside this repository.

The English instructions, selection metadata, and adjacent responsibility boundaries were not changed in this audit.\
Consequently, the definition migration and meaning-preserving Japanese revision use static validation without model execution, as permitted by `docs/evaluation.md`.\
The historical `results.json` records 33 passing candidate requirements across six behavior cases, while its baseline had 27 passing, five partial, and one failing requirement.\
Its routing observations and selected no-Skill comparisons are also historical and do not verify the current candidate.\
A future observed regression, instruction change, or environment-support claim would make a targeted model evaluation decision-relevant.

## Verification

Both executable definitions passed the Runner's read-only `plan` operation for all six behavior and ten routing cases, with estimated call counts of six and ten respectively; no model calls were made.\
A source-to-candidate comparison confirmed the original user request text (with only a supplied-evidence file pointer appended), IDs, fixture contents, assertion statements and criticality, conditions, coexistence Skills, and handler expectations.\
`PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_repository.py`, `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` (150 tests), and `git diff --check` passed.\
These checks establish definition validity and migration fidelity, not current model behavior.
