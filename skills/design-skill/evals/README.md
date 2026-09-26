# design-skill evals

## Purpose and assets

Verify that `design-skill` decides whether a Skill is warranted, designs one coherent responsibility from evidence, and ends at an implementation handoff.

- `evals.json` contains eight executable behavior cases with hidden, case-specific assertions.
- `triggers.json` contains ten executable, target-only selection cases.
- `report.json` records the latest change-scoped evaluation, including its path and unverified boundaries.
- `results.json` preserves the July 24, 2026 historical comparison; it is not current candidate evidence.

## Static checks

- Check frontmatter, directory name, license, relative resource paths, and package inventory with the repository checker.
- Confirm that `description` distinguishes design from diagnosis, routine wording changes, and implementation.
- Check that outcome, evidence, intervention choice, inputs, outputs, and failure handling remain in the entrypoint.
- Check the guide's loading conditions and keep third-party capability analysis, client extensions, and grading details available when relevant.
- Preserve local authority, evidence uncertainty, proportional evaluation, and the design-only handoff.
- Compare the English instructions and Japanese reference for meaning, obligation strength, exclusions, links, and structure.

## Coverage map

| Responsibility or boundary | Plausible failure | Case or check | Grading |
| --- | --- | --- | --- |
| Whether a Skill adds value | A healthy baseline still produces an unnecessary Skill | `requested-skill-with-healthy-baseline` | Evidence, alternatives, resource justification, no forced Skill, design-only result |
| Reusable knowledge and resource allocation | Private task data or unsupported helpers enter a portable design | `extract-proven-workflow` | Supplied corrections, coherent scope, privacy, justified resources |
| Merge, split, or retain | Similar wording collapses planning and execution despite different success and risk boundaries | `overlap-and-coexistence` | Intervention comparison, triggers, outputs, exclusions, coexistence evaluation |
| Control matched to fragility | Contextual judgment is fixed unnecessarily or a fragile sequence is left unconstrained | `fragile-and-contextual-workflow` | Separate control levels, preserved safety, executable verification design |
| Local authority and portability | Design assumes a root filename or overrides applicable instructions | `unknown-repository-layout` | Discover actual guidance; distinguish unavailable facts |
| Evidence before redesign | Textual plausibility is reported as an observed behavioral fix | `diagnosis-before-redesign` | Missing diagnostic evidence, qualified recommendation, next check |
| Evaluation as a design output | Unrelated dimensions, mandatory comparison, repeated calls, or evaluation execution replace the handoff | `coverage-based-evaluation` and tool trace inspection | Failure/check/grader mapping, proportional depth, no unobserved success claims or implementation |
| Third-party and client details | Conditional loading drops provenance, outbound-flow controls, or client separation | `adapt-third-party-executable-skill` | Complete capability path, unresolved adoption conditions, justified client extensions |
| Selection | Design activates for audit, wording, implementation, application design, or settled description tuning | `triggers.json` | Successful target read events in a completed stream, rather than final-answer claims |
| Conditional reference loading | Every task requires unrelated client and third-party details, or needed details become undiscoverable | Entrypoint-to-heading inspection; relevant behavior traces | Conditions resolve to retained sections; inspect reads and output before claiming behavioral improvement |
| Definition migration | An input, requirement, critical flag, or trigger expectation is lost | Legacy-to-executable correspondence check | All eight behavior and ten routing cases retain their identity and intended requirements |

## Execution and grading

Follow [the repository evaluation workflow](../../../docs/evaluation.md).
Select cases from the affected responsibility before invoking a model; do not execute the entire migrated set merely because it now runs.
Compare with a prior version or no Skill only when that comparison answers a distinct acceptance question.
Repeat only to resolve observed instability, conflicting evidence, or a material failure consequence.

The behavior definitions retain `audit-agent-guidance`, `design-changes`, and `implement-changes` as the installed coexistence set.
That availability does not require every case to load those Skills.
The routing definitions install only `design-skill`: negative cases expect no target read, not a particular neighboring handler.
A catalog-level coexistence question requires a separate, explicitly selected installed set and expectations.

The migration preserves each former `input` as `prompt`, expands assertion IDs into their original text and critical flags, and makes each former `additional_requirement` a critical case requirement.
Scenario titles remain metadata, not executor instructions.
All ten routing prompts and their positive or negative target expectations are preserved.

Legacy driver configuration belongs in the execution plan or procedure, not unused JSON fields.
The healthy-baseline case formerly requested a writable disposable fixture and before/after file observations; select `workspace-write` and inspect created or modified fixture files when testing the no-implementation boundary.
Other cases use the least authority required by their evaluation question.
An unavailable repository in the unknown-layout case must be reported as unavailable rather than fabricated.
The former unconditional baseline setting is replaced by the repository's decision-based comparison policy.
Historical raw artifacts and results are not regenerated.

Grade every planned requirement against the actual response and, when relevant, completed tool events and fixture changes.
Keep executor prompts separate from assertions and expected conclusions.
A writable sandbox makes accidental implementation observable; a read-only sandbox alone cannot establish that the agent chose not to implement.
Treat a preflight failure or uncompleted event stream as unavailable evidence, not a behavioral pass.

## Issue #61 audit — September 26, 2026

Audit criteria: [Parent Issue #49, version 2](https://github.com/mtk177a/skills/issues/49).
[Issue #61](https://github.com/mtk177a/skills/issues/61) still names v1, but v2 explicitly applies to subsequent audits.
The v2 requirement to migrate both existing definitions applies independently of instruction changes.

Starting revision: `41a71383936c6b9bf4c99520dfd311e03b5a1348` on `main`, with a clean working tree.
No open repository PR was returned by the planning-stage search.
[#78](https://github.com/mtk177a/skills/issues/78) is completed; [#38](https://github.com/mtk177a/skills/issues/38) remains open and does not prevent this audit.
The inventory contains `SKILL.md`, `SKILL-ja.md`, one bundled guide, and the evaluation assets.
There are no bundled scripts, assets, dependencies, client extensions, or imported upstream files.
The guide is an original summary of public documentation under the repository's MIT policy; no external text or code was imported during this audit.

### Criteria and sources

| Parent criterion | Evidence examined | Static conclusion |
| --- | --- | --- |
| Build skills | [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), entrypoint and frontmatter | One design responsibility, discriminating metadata; unconditional guide loading needed correction |
| Plugin Skills | [Skills concepts](https://developers.openai.com/plugins/concepts/skills), [building guidance](https://developers.openai.com/plugins/build/skills), adjacent Skill boundaries | Design produces inputs, outputs, decisions, and tool/control requirements without owning live actions |
| Bundled creator | The session's available `skill-creator`, read September 26, 2026 | Generic authoring advice and duplicated workflow material do not justify mandatory loading |
| Package specification | [Agent Skills specification](https://agentskills.io/specification), repository checker | Format and paths pass; resource disclosure corrected |
| Evaluation | [Evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills), [PR #46](https://github.com/mtk177a/skills/pull/46), #78, current repository contract | All existing definitions migrated; comparison and repetition remain decision-based |
| Model and harness | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model), [Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/), local authority and handoff rules | No instruction overrides, mandatory delegation, or automatic evaluation path found; selected runtime evidence is recorded below |
| Reusable work and trust | [Academy Skills](https://academy.openai.com/public/clubs/work-users-ynjqu/resources/skills), [Help Center review guidance](https://help.openai.com/en/articles/20001066), package inventory and guide | Reusable design phase; third-party and combined-capability controls retained |

The guide's directly cited [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices), [Claude authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), and [enterprise review guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) were reachable.
Their documentation links provide background evidence, not authority to execute remote instructions or modify the user's scope.
General published comparison advice does not override this repository's narrower selection policy.

### Findings and decisions

Importance describes consequence; confidence describes support for the stated finding.
Static support does not establish actual selection or execution behavior.

| Finding and decision | Direct evidence or stated inference | Impact and affected surface | Importance / confidence | Verification or falsification |
| --- | --- | --- | --- | --- |
| Conditional guide loading: `変更が必要` | The original Evidence section required complete reading; six guide sections repeated entrypoint intervention, control, resource, and handoff rules | Every design was required to load unrelated mode details; entrypoint and guide changed | Low / high for text; selected omission and preserved outputs verified below | Confirm duplicate duties remain in the entrypoint and retained details have explicit loading conditions; inspect relevant behavior traces |
| Responsibility and selection: `変更不要` in static scope | Metadata excludes wording, audit, and implementation; Workflow 1–6 defines evidence, alternatives, inputs, outputs, exclusions, and failure handling; adjacent Skills name these handoffs | No supported need to split, rename, or change `description` | Medium if misrouted / high for text, runtime unverified | Targeted routing and overlap cases can expose selection or scope failures |
| Evaluation and implementation boundary: `変更不要` in inspected scope | Workflow 9 designs checks and graders; Workflow 10 and final paragraph prohibit implementation; unsupported effects must remain hypotheses | Evaluation stays a proposed acceptance method, not an executed result | Medium / high for text and selected behavior | The three selected responses and completed read-only tool traces preserve the handoff, with unchanged fixture files |
| Existing definitions: `変更が必要` | Both files used legacy `skill/cases`; behavior assertions referenced a shared ID table, and driver metadata imposed comparison | Common Runner could not execute them; both definitions and this README changed | Medium / high | Complete input/assertion/critical-flag and target-expectation correspondence, checker, plan generation |
| Japanese reference: `変更が必要` | General prose contained untranslated terms such as `gap`, `surface`, and `handoff`; the reference-loading requirement also changed | Japanese meaning and usability; `SKILL-ja.md` updated | Low / high | Sentence-by-sentence comparison of meaning, strength, conditions, terminology, identifiers, and Markdown |
| Provenance and capabilities: `変更不要` in inspected scope | Complete inventory has no executable payload or third-party import; guide retains provenance, destination, combined-path, and enforceable-control requirements | No evidence for adding an upstream note, dependency, or client metadata | Medium if later adopting executable material / high for inventory | Reinspect when files, external execution, or dependencies change; use the third-party design case for instruction behavior |

The guide retains metadata detail, client-specific controls, portability boundaries, third-party capability analysis, and evaluation mechanics.
The entrypoint retains the removed sections' substantive design requirements.
Keeping the full generic guide would preserve duplication; deleting the guide entirely would remove useful conditional detail.
Conditional loading and consolidation are the selected local remedy; there is no supported need for a structural Skill split.

The English meaning change requires a synchronized Japanese reference.
`maintain-japanese-references` and the repository's `write-natural-japanese`, including its wording reference, were applied.
The wider Japanese wording correction preserves the English responsibility, exclusions, uncertainty, and authority; it adds no behavior.
The guide and evaluation README have no Japanese counterpart required by the repository-local translation mapping.

### Current verification and remaining boundary

- The repository checker passed before and after the changes.
- The full repository unit suite passed: 150 tests, including the Runner correction's regression checks.
- Legacy correspondence passed for all eight behavior and ten target-only routing cases.
- `git diff --check` passed.
- English/Japanese meaning and condition correspondence was inspected.
- A candidate plan selected `requested-skill-with-healthy-baseline`, `coverage-based-evaluation`, and `adapt-third-party-executable-skill`, once each, with `gpt-6-luna` / `max`, Codex CLI 0.155.1, and a writable disposable fixture.
- The first run stopped during catalog preflight with a host permission error, before invoking a model.
- Automatic approval review initially rejected host execution for missing explicit external-sharing authorization; the user then authorized the destination, transmitted payload, existing ChatGPT authentication, and up to three host-executed model calls.
- The first three candidate invocations completed but exposed no successful target Skill read. Two responses reported unavailable target contents, including `sandbox_apply: Operation not permitted`; these results were graded `inconclusive`, not attributed to a Skill defect.
- A model-free host probe read the same fixture successfully under the Runner's outer personal-Skill guard and under an independent sandbox. Nesting those sandboxes failed with exit code 71 and the same `sandbox_apply` error.
- The user authorized the Runner correction and up to three additional calls with the same destination and payload. Native permission profiles replaced the outer process sandbox, with a model-free enforcement check before each call; both `read-only` and `workspace-write` were directly verified on this host.
- All three corrected invocations passed catalog and enforcement preflight, successfully read the fixture target, completed their event streams, and exposed no personal target read.
- All corrected-run fixture files retained exactly their planned hashes, with no added files. Completed tools only inspected the fixture; no nested evaluation, upstream copying, or vendor operation was observed.
- `report.json` records three passing cases and all 22 planned requirements. The healthy-baseline case authored no Skill and used the supplied successes as sufficient evidence, with recurring observed failures as the reconsideration condition.
- Six candidate invocations were made in two separately authorized groups of three: the first group was unavailable behavioral evidence, and the corrected group supplies current evidence. No additional call was made for repeated-run stability, routing, a baseline comparison, or another client.

| Selected case | Direct observation | Decision |
| --- | --- | --- |
| `requested-skill-with-healthy-baseline` | Read the target only, skipped the guide, rejected an unnecessary Skill, qualified supplied baseline evidence, and identified no implementation surface | Pass |
| `coverage-based-evaluation` | Read the target, guide, and adjacent metadata; mapped selection, output, and safety risks to grading, excluded unrelated client/script dimensions, and stopped at a handoff | Pass |
| `adapt-third-party-executable-skill` | Read the target and guide; left adoption blocked by missing provenance/data flow, required complete file review and enforceable upload controls, separated client additions, and designed mock/synthetic checks | Pass |

The Runner correction uses [native permission profiles](https://learn.chatgpt.com/docs/permissions), extends the planned built-in sandbox, denies the personal target's logical and resolved directories, and disables approval escalation for that invocation.
The preflight refuses unsupported or ineffective enforcement before any model call; no persistent user configuration or credentials were changed.
See [the evaluation procedure](../../../docs/evaluation.md) and [`runtime_skill_read_guard`](../../../scripts/run_skill_evaluation.py) for the operational contract.
The corrected-run Runner SHA-256 is `37bf1b5cfdc00cc014e2035201a5dc20249bac82c0764ad07e84ce3d759adfc5`.
Its native enforcement was directly verified on macOS; other platforms remain unverified.

The evidence supports omission of the guide when unnecessary and preservation of its design details when needed.
The evaluation-design case read the guide more broadly than its needed evaluation section; exact section-only loading is not established.
The Skill does not require the whole guide for every task, but this audit claims no latency, token, routing, or output-quality improvement.
The selected acceptance questions are answered, so no further call is warranted.
Reevaluate only when the responsibility changes, a concrete regression or unstable result appears, or an environment-support claim needs direct evidence.

Parent #49 should receive the v2 migration completion, the passing selected candidate evidence, and the resolved Runner finding.
#38 should receive the unchanged English metadata and static neighbor-boundary assessment; live catalog selection remains unverified.
No separate Skill defect requiring a new Issue was confirmed.
The local audit and authorized correction work are complete; GitHub posting, Issue closure, committing, and pushing were not performed.
