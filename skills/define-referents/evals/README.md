# define-referents evals

## Purpose

Verify that `define-referents` makes the Grounding-then-Naming order observable, preserves uncertainty and context-specific semantic roles, and returns a naming constraint to the originating workflow without inventing missing meaning, forcing universal approval, creating unauthorized files, or taking over downstream work.

## Assets

- `triggers.json`: trigger, non-trigger, near-miss, continuation, and coexistence routing cases
- `evals.json`: executable behavior cases with hidden assertions and case-specific requirements
- `results.json`: historical baseline/candidate evidence from July 2026
- this README: static contract, coverage, protocol, and summarized result

## Static check

- `description` targets terminology-specific ambiguity and excludes overall request clarification, downstream authoring, mechanical edits, established-name reuse, and ordinary wording.
- The Skill ends with a referent-and-naming handoff rather than writing the downstream document, report, design, or code.
- Grounding and Naming use separate observable tables, and no candidate term or first-use definition appears in Grounding.
- `Ready`, `Decision required`, and `Blocked` have distinct entry and reporting conditions.
- Confirmation is conditional on a material semantic decision rather than universal.
- A separate table file requires explicit authorization.
- Semantic roles are contextual rather than a closed taxonomy, and table splitting follows meaning rather than row count.
- The bundled reference is self-contained and the external article is provenance only.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Observable Grounding before Naming | Generates a label or definition while supposedly grounding the referent | `threshold-condition-event`, `low-impact-local-identifier` | Response-order and content inspection |
| Distinct referents and sequence | Reuses one fluent label for a threshold, condition, and event or hides an unknown cause | `threshold-condition-event`, `incident-unknown-cause` | Requirement-level grader |
| Missing input handling | Invents the meaning of an underspecified boolean to complete the table | `underspecified-public-boolean` | Critical assertion |
| Conditional decision boundary | Always waits for confirmation or silently selects a public contract | `low-impact-local-identifier`, `public-contract-alternatives` | State and question inspection |
| Context-specific roles and semantic splitting | Forces actor, component, interface, or policy into the old role list or splits at six rows | `contextual-roles-coherent-flow` | Table inspection |
| File and downstream ownership | Creates a sidecar or drafts the design/code under the semantic-preflight Skill | `design-handoff-no-sidecar`, `implementation-handoff-no-edit` | Fixture hashes and response inspection |
| Correction recovery | Retains a naming proposal whose Grounding row was corrected | `corrected-grounding-row` | Response to a correction with an explicit prior Grounding/Naming handoff |
| Trigger boundary | Misses explicit referent work or absorbs clarification, ordinary design, implementation, investigation, and mechanical writing | `triggers.json` | Observable Skill load |
| Coexistence | Prevents or replaces the originating specialized workflow | design, incident, and implementation handoff cases | Requirement-level grader |

## Execution and grading

Use the common Runner and the path-selection rules in [docs/evaluation.md](../../../docs/evaluation.md).
Generate a plan, inspect the selected cases and model-call estimate, and execute only when new behavioral evidence is needed.
The July baseline commit `45bb765ca110bd3e0b4ab2294b7ed030a4ada55d` explains the historical comparison; it is not a mandatory baseline for future changes.

Behavior cases explicitly invoke the fixture Skill; routing cases leave selection to the executor and install the declared adjacent catalog.
The executor receives the visible request or conversation and fixture, not assertions or expected conclusions.
Grade assigned assertions against the final response, exposed tool events, and fixture state; distinguish actual write attempts from writes prevented by the sandbox.
The invoking session or a human supplies non-routing grades; a separate model grader is not required.
The Runner derives case outcomes from critical flags and grades and records routing only from successful Skill reads in a completed event stream.
An unexposed event stream is inconclusive, not a pass.

The correction case supplies an event-based prior assistant handoff followed by the original user correction to an interval state.
The Runner responds to the final user request once; this checks recovery from supplied context, not a live session generating both assistant turns.
The prior handoff is visible scenario input, not an expected answer to the correction.

Keep plans, prompts, responses, JSONL, fixture snapshots, and grades outside the repository in a temporary directory.
Run selected candidate cases once initially; add comparison or repetition only when it can change the acceptance decision.

## Failure Pattern Ledger

- `candidate term or definition appears in Grounding`
- `distinct referents collapsed under one label`
- `missing meaning invented to finish a table`
- `low-impact naming stopped for universal confirmation`
- `material public meaning selected silently`
- `context-specific role forced into a closed taxonomy`
- `table split only because it exceeds six rows`
- `target-document authorization treated as sidecar authorization`
- `semantic preflight drafts or edits downstream content`
- `corrected grounding retains stale naming`
- `ordinary clarification, design, investigation, implementation, or mechanical writing routed to define-referents`

## Historical behavioral evidence

Evaluated on 2026-07-28 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The matched baseline/candidate evidence covers nine behavior cases and 46 assigned requirements.
- The candidate passed all 46 requirements and all nine cases after correcting one grader requirement that contradicted the confirmed need for two public facts. The baseline passed no case, with 21 passed, four partial, and 21 failed requirements.
- The candidate made Grounding-then-Naming observable, distinguished conditional confirmation from low-impact completion, supported context-specific roles and semantic table splitting, preserved missing information and corrections, and left design, failure investigation, and implementation ownership downstream.
- Nine current trigger, non-trigger, continuation, near-miss, and coexistence results remain applicable. The mechanical Markdown exclusion was changed from routing to the retired `format-markdown` Skill into an unhandled exclusion and has not been rerun.
- The 2026-07-30 identity migration reran the affected terminology handoff and routing case. Both passed while leaving evidence gathering and causal diagnosis with `investigate-failure`.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, observed Skill loads, grader-correction provenance, and unverified items.

## Issue #58 audit — September 27, 2026

### Scope and evidence

Expected behavior: ground terminology that could collapse distinct concepts, preserve evidence and user-owned semantic decisions, and return naming constraints so the originating task can continue within its existing responsibility and authority.

This audit uses [Parent Issue #49, audit criteria v2](https://github.com/mtk177a/skills/issues/49) for [Issue #58](https://github.com/mtk177a/skills/issues/58), whose v1 reference predates the mandatory definition-migration rule.
The starting commit is `da06da6710571c1f070fb05e13c93bf2298747fb`, on `main` with a clean working tree and no open repository PR listed.
The relevant prior audits are #51, #61, and #55; #78 is completed.
Issue #38 has no initial catalog inventory recorded in its body or comments; the relevant metadata and adjacent boundaries were inspected locally, without claiming the catalog-wide work is complete.

The complete target inventory is `SKILL.md`, `SKILL-ja.md`, `references/referents-before-labels.md`, this README, both definition files, and `results.json`.
There are no target scripts, assets, dependencies, client extensions, or upstream synchronization files.
The Skill permits relevant read-only evidence inspection within a clear target and scope; it does not specify credential access, a network-send path, or a downstream edit.
The reference's Zenn URL is attribution, and the entrypoint explicitly prohibits fetching that article at runtime.
The reference and `THIRD_PARTY_NOTICES.md` describe independently authored material inspired by the article, rather than imported article text; the MIT metadata agrees with that recorded provenance.
No external code or instruction package was imported by this audit.

Before editing, all five file hashes in the historical candidate record matched the working tree exactly.
The unchanged English entrypoint and reference retain those hashes after this audit.
Historical executions remain evidence for their recorded clients, models, catalog, and sandbox; they do not establish current implicit selection or end-to-end resumption of an originating task.
The current local tools include Python 3.14.6 and Codex CLI 0.155.1.
The audit used the existing main session without delegation or changing its model settings; no evaluation model was invoked.

### Criteria and sources

Official sources were inspected on September 27, 2026.
Published recommendations were kept separate from package requirements and directly observed behavior.

| Parent criterion | Source and inspection | Conclusion within static scope |
| --- | --- | --- |
| Focus and discovery | [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), frontmatter, adjacent descriptions | One terminology responsibility; the material trigger is at the beginning of the 620-character description |
| Workflow and controls | [Skills concepts](https://developers.openai.com/plugins/concepts/skills), [Build skills](https://developers.openai.com/plugins/build/skills), entrypoint and reference | Inputs, ordered grounding, output states, and authority boundaries are explicit; prose does not claim to enforce tool permissions |
| Necessary detail | The session's bundled `skill-creator`, entrypoint and complete reference | Observable two-phase output protects a concrete semantic invariant; the reference adds role distinctions and application examples for the same workflow |
| Format and disclosure | [Agent Skills specification](https://agentskills.io/specification), repository checker | Name, directory, description, license, and relative references conform; no new metadata or resource is needed |
| Evaluation | [Evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills), [PR #46](https://github.com/mtk177a/skills/pull/46), #78, current repository contract | Migrate both existing definitions; preserve hidden grading and choose execution independently |
| Context and authority | [Model guidance](https://developers.openai.com/api/docs/guides/latest-model), [Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/), local instructions | No instruction-priority override, automatic evaluation, or mandatory delegation; actual host loading remains environment-specific |
| Reuse and trust | [Academy Skills](https://academy.openai.com/public/clubs/work-users-ynjqu/resources/skills), [Help Center](https://help.openai.com/en/articles/20001066), inventory and provenance | A reusable terminology phase with scoped evidence access and no bundled execution or outbound-data chain |

### Findings and decisions

Importance describes consequence; confidence describes evidence for the finding.
The four Japanese decision labels match #49.

| Finding and decision | Evidence and affected surface | Impact / confidence | Verification or falsification |
| --- | --- | --- | --- |
| Selection and responsibility: `変更不要` within static scope | English metadata excludes ordinary wording, established-name reuse, overall clarification, and downstream authoring. Current adjacent `clarify-request`, `design-changes`, `investigate-failure`, and `implement-changes` retain distinct responsibilities. Historical routing includes positive, continuation, near-miss, and coexistence cases. | Material if misrouted / high for text; current routing not executed | Use relevant trigger and near-miss cases if discovery changes; inspect actual Skill-read events rather than response wording |
| Grounding, naming, and handoff: `変更不要` within inspected scope | Workflow 3–8 and the table rules separate concrete referents from names, invalidate dependent names after corrections, and end the Skill while the originating workflow resumes. Historical behavior records cover these constraints without target mutation. | Material if concepts or authority are conflated / high for text and historical record; live resumption unverified | `threshold-condition-event`, `corrected-grounding-row`, and the design/implementation handoff cases expose the relevant local failures; a live originating task is needed for a resumption claim |
| Required reference: `変更不要` on current evidence | The 73-line reference shares the entrypoint's safeguards but adds definitions, role distinctions, and examples for one semantic workflow, rather than unrelated client or domain modes. The 91-line entrypoint relies on those distinctions. | Additional context on every activation / high for inventory; medium for the inference that complete reading remains proportionate | Consolidation or conditional reading would need to preserve the role and relationship distinctions. No measured latency, token, or quality benefit is claimed for retaining or changing the split |
| Missing facts and material decisions: `変更不要` within inspected scope | Evidence rules call for safe inspection of discoverable facts. Missing grounding yields a question or `Blocked`; settled low-impact naming is `Ready`; public/domain semantic alternatives require `Decision required`. The incomplete-boolean and low-impact cases test opposite boundaries. | Material if meaning is invented or work stops unnecessarily / high for text; historical behavior is version-specific | Use `underspecified-public-boolean`, `public-contract-alternatives`, and `low-impact-local-identifier` when these conditions change |
| Existing definitions and execution documentation: `変更が必要` | Both definitions used legacy `{skill, cases}`; assertions referenced a shared table, case-specific requirements were a separate unsupported field, and the README prescribed a permanent baseline and separate model grader. Both definitions and this README now follow the current executable contract. | Blocks the common Runner or loses grading intent / high | Compare every original input, fixture, assigned assertion, critical flag, case-specific requirement, and routing expectation; validate and generate plans without invoking a model |
| Japanese reference quality: `変更が必要` | The reference translation mixed general explanation words such as `workflow`, `reference`, `grounding`, and `handoff` into Japanese sentences and used an unexplained general-purpose translation of `contract`. `SKILL-ja.md` now expresses those meanings in Japanese, with original table names at first use and unchanged state/identifier strings. | Reader burden and avoidable ambiguity / high for text | Compare all sentences with the unchanged English source, preserving selection, mandatory reading, order, uncertainty, user decisions, file authority, links, and Markdown tables |
| Provenance and capability boundary: `変更不要` within static scope | Complete inventory has no executable payload, dependency, authentication action, or outbound destination; the article link is expressly provenance-only. Table-file creation needs explicit authority. | Material if later extended with tools or external data / high for inventory; runtime safety not established | Reinspect when capabilities or sources change; write-enabled behavioral safety and unseen external sources are not passes |
| Current host behavior: `未確認` | No model-backed run was selected. Historical records exclude real-session implicit activation, long-running handoff, other clients, and the current mechanical Markdown exclusion. | Limits runtime conclusions / high confidence in the evidence gap | Use a targeted routing or live-environment run when a changed responsibility or support claim requires it |

Keeping the current package preserves the tested semantic safeguards and avoids an unsupported rewrite.
Consolidating the reference could remove repeated safeguards, but would also move its semantic examples into the entrypoint or require conditional loading rules without current failure evidence.
Removing the Skill would discard the observable grounding-before-naming invariant; no evidence supports that remedy.
There is no supported need to rename, split, add dependencies, or change distribution.

### Migration and translation verification

All nine behavior cases and ten routing cases are retained.
The 46 original assigned assertion statements and their critical flags are expanded into case-local assertion objects.
Each of the nine original hidden case-specific requirements is preserved as an additional critical `case-specific-requirement` assertion; the new definition therefore has 55 grading requirements, not a new 55-requirement behavioral pass.
Per-case `adjacent_skill` values become `coexistence_skills`, and the routing definition retains the full original five-Skill catalog.
Each expected handler becomes an array; the unhandled mechanical case uses an empty array.

The correction case preserves both original user messages and adds a fixed prior assistant event mapping as visible conversation context.
This is necessary because the common Runner produces only the final response; two user turns alone would not provide a stale naming proposal to invalidate.
The fixture provides the earlier proposal, not the expected interval-state answer.
Live two-turn generation remains unverified by the migrated definition.
Legacy driver settings and protocol metadata are explained here or retained in historical results rather than copied into unsupported JSON fields.

The English entrypoint and reference are unchanged, so there is no English semantic change to synchronize.
The Japanese reference correction was checked with `write-natural-japanese` and its complete wording guide against the English source.
The canonical-source notice from [Issue #4](https://github.com/mtk177a/skills/issues/4), metadata identity, relative link, table columns, state labels, permissions, prohibitions, and uncertainty are preserved.
No separate Japanese file is required for this evaluation README.

### Validation and remaining scope

The selected execution path is `static-only`: definition migration, execution-documentation alignment, and a meaning-preserving Japanese reference correction do not change the canonical Skill's discovery or runtime responsibility.
Model-call count: zero.
Validation results:

- Complete source-to-migration comparison passed for all nine behavior cases, 46 original assigned assertions and critical flags, nine case-specific requirements, ten routing cases, visible inputs, fixtures, and coexistence declarations; the correction case's added prior assistant context was checked separately.
- The English entrypoint, reference, and historical results are byte-for-byte unchanged from the starting commit; the Japanese notice and table structures are preserved, and full-source review preserves the English requirements.
- The Runner generated a `static-only` plan with zero estimated calls and completed it with `--max-model-calls 0`; its run record reports a passing static check and an empty execution list.
- Plans covering all migrated behavior and routing definitions were generated solely to validate normalization, input forms, references, and case selection. They estimate nine and ten calls respectively, but neither model-backed plan was executed.
- `python3 scripts/check_repository.py` passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` passed all 150 tests.
- `git diff --check` passed.

The acceptance question is resolved by the complete migration comparison, successful executable-contract plans, and deterministic checks; no canonical runtime change or conflicting behavioral evidence requires a new model run.

No new behavioral or routing pass is claimed.
Comparison, repetition, all-case model execution, other clients, domain-specific naming quality outside the represented cases, and distribution installation tests were not selected.
Distribution tests are unnecessary because installation and delivery paths did not change.
Historical `results.json` is retained without rewriting its recorded environment or candidate hashes.

Issue #49 should receive the v2 decision, completed definition migration, unchanged canonical runtime, Japanese wording correction, and the explicit static-only limit.
Issue #38 should retain the missing initial inventory and current-host discovery limits for its catalog-wide follow-up.
No separate adjacent-Skill defect was confirmed, and no additional Issue is required on the available evidence.
GitHub posting, Issue closure, commits, and pushes are outside this local audit result.
