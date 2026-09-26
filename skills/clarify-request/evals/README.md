# clarify-request evaluation and audit

## Purpose and assets

Evaluate request-intent alignment, material clarification, and a self-contained agreed request or downstream handoff without inventing requirements or authority.

- `evals.json` contains executable behavior cases with hidden requirement-level grading.
- `triggers.json` contains executable routing cases and their declared coexistence Skills.
- `report.json` records the selected evaluation for the audited candidate.
- `results.json` preserves the historical 2026-07-28 evidence; it is not evidence for the current candidate.

## Issue #55 audit scope

The audit uses [Issue #49 audit criteria v2](https://github.com/mtk177a/skills/issues/49) for [Issue #55](https://github.com/mtk177a/skills/issues/55), whose v1 reference predates the current migration criterion.
The inspected base is `0f546d99eeb7cad1917e37ab226b305631e101ab`, on `main` with a clean working tree at the start.
No open repository PR was listed at planning time; recheck concurrent work before submitting changes.
Issues #51, #61, and #78 were closed; #32 remains open without blocking this audit.
Issue #38 had no recorded initial inventory in its body or comments, so this audit inspects the relevant metadata locally and does not claim that the catalog-wide audit is complete.

Expected behavior: express how the user's intent is understood before material follow-up questions, preserve corrections across turns, return the agreed request when alignment is complete, and distinguish clarification-only completion from returning to an already authorized workflow.

The initial target inventory consists of `SKILL.md`, `SKILL-ja.md`, this README, both evaluation definitions, and the historical results.
There are no target scripts, references, assets, upstream files, dependencies, authentication actions, or outbound destinations.
Safe inspection of relevant user-authorized evidence is the only data-access capability described by the Skill; discovery does not authorize downstream writes or external actions.
The MIT metadata is consistent with the repository's original-content policy and notices; no third-party import was identified.
The relevant adjacent responsibilities are request clarification, concrete terminology definition (`define-referents`), option exploration (`explore-decision-space`), understood-change design (`design-changes`), and authorized implementation (`implement-changes`).

## Findings and decisions

| Finding | Decision | Evidence and affected surface | Impact | Confidence and verification |
| --- | --- | --- | --- | --- |
| Understanding-check selection gap | Change needed | The original `description` did not name understanding checks; its clear-request rule allowed restructuring only for a structured handoff. A completed routing observation with the original candidate and the declared adjacent catalog recorded no Skill loads for `explicit-understanding-check`, although the answer paraphrased the request correctly. | The reported recurring intent-alignment workflow can bypass its reusable guidance. | High confidence in the observed miss and static omission; the metadata omission as its cause is an inference. Verify with the same request, catalog, client, and model after adding the trigger. |
| Clarification-only completion needs an explicit boundary | Change needed | Original Objective and Ready state required an intended next workflow; the boundaries said to use design or proceed to implementation. They did not explicitly distinguish an agreed meaning from permission for ordinary downstream work. Original forced-Skill behavior returned a Ready handoff without performing downstream work. | A standalone alignment request can be judged against unnecessary downstream entry conditions, or the handoff can be read as permission to continue. | High confidence in the missing scope distinction; an actual unauthorized action was not observed. Verify completion without another confirmation or downstream work, and preserve existing authority for an active originating task. |
| Iterative clarification and evidence/authority separation | No change needed in the existing rules | The body distinguishes facts, inference, assumptions, contradictions, missing authority, material gaps, and next-workflow-owned inputs. Historical evaluations recorded these behaviors for the accepted 2026-07-28 revision. | These protections must survive the focused trigger and completion correction. | High confidence in the static rules; historical runtime evidence is version-specific. Check partial and completed provider clarification on the current candidate; leave unselected safety cases unconfirmed for this revision. |
| Structure, provenance, optional resources, and client-specific metadata | No change needed | The package is self-contained, contains the required metadata, and requires no executable helper or companion Skill. The checker validates the maintained structure. | No evidence justifies a rename, split, new dependency, supporting-resource tree, or client-specific extension. | Static conclusion only; checker and file inspection can falsify it. Runtime compatibility outside the selected Codex environment remains unconfirmed. |
| Legacy evaluation definitions | Change needed under v2 | Both original definition files used `{skill, cases}`. Their complete sets now use `{skill_name, evals}`. | Model-backed evaluation otherwise stops before execution. | Verified by the executable contract, checker, and a source-to-migration comparison of inputs, fixtures, assigned assertions, critical flags, case-specific requirements, and target trigger inclusion/exclusion. |
| Explicit ambiguity and missing-information objective | Change needed | The initial audit wording replaced the original explicit objective with intent alignment; the existing clarification steps still identified and resolved material gaps. The final Objective explicitly retains both responsibilities. | Intent alignment must not obscure clarification of ambiguous or incomplete requests. | Static comparison confirms that only the first English Objective item changes from the initial audit candidate; verify partial clarification, understanding-first output, and standalone completion on the final candidate. |
| Japanese reference translation | Change needed | English trigger, purpose, interpretation order, Ready state, and downstream boundaries changed; the initial translation retained general English explanation words throughout. | The reference translation must express the same scope and authority conditions in natural Japanese. | Full-source comparison and full-text Japanese revision use repository-local `maintain-japanese-references`, repository `write-natural-japanese`, and its complete wording reference. Preserve identifiers and bilingual state labels; translate general explanation words and retain obligations, permissions, exclusions, and uncertainty. |
| Compound-command routing observability | Separate Issue needed | In the first option-exploration observation, the complete fixture `explore-decision-space/SKILL.md` appeared in command output, but a trailing empty-repository search made the compound command exit 1; the Runner reported no handler. | A successful Skill read can be undercounted when a later command in the same event fails. | High confidence from exact source-text inclusion in the completed command output. Recheck a realistic fixture; preserve the original observation and hand the Runner limitation to #49 for separate evaluation-infrastructure tracking, without changing an adjacent Skill. |

The focused update keeps one request-clarification responsibility rather than creating a separate understanding-check Skill or redesigning the workflow system.
A separate Skill would duplicate the clarification state and compete for the same request; removing the Skill would discard the existing material-question, iteration, and authority rules.
No target finding justifies edits to an adjacent Skill or distribution behavior; the routing-observation limitation belongs to evaluation infrastructure.

## Criteria and primary-source checks

The current sources were consulted on 2026-09-27; these observations support the audit decision, not a general claim of client compatibility.

- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills): metadata-based selection and progressive disclosure justify fixing the missing trigger in `description`, not only in the body.
- [Skills – Plugins](https://developers.openai.com/plugins/concepts/skills) and [Build skills – Plugins](https://developers.openai.com/plugins/build/skills): one recognizable user goal, meaningful inputs/output, and separate selection/output diagnosis fit this instruction-only workflow; tool-enforced permissions are not replaced by prose.
- The currently bundled Codex `skill-creator`: preserve user scope, avoid universal rules from a single example, and retain only guidance that changes decisions. The added interpretation and completion rules address the recurring usage reported in #55, with explicit protection for already authorized tasks.
- [Agent Skills specification](https://agentskills.io/specification): name, directory, description, license, and resource structure were checked; optional fields and recommended size bounds are not treated as quality targets.
- [Agent Skills evaluation guidance](https://agentskills.io/skill-creation/evaluating-skills), [PR #46](https://github.com/mtk177a/skills/pull/46), [Issue #78](https://github.com/mtk177a/skills/issues/78), and repository `docs/evaluation.md`: migrate definitions completely, keep grading hidden, isolate executions, and select only acceptance-relevant observations. The repository's targeted paths govern execution rather than requiring every comparison or case.
- [Model guidance](https://developers.openai.com/api/docs/guides/latest-model) and [Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/): avoid conflicting instructions and preserve the user/Skill authority relationship; catalog presence is distinct from observed full Skill loading.
- [OpenAI Academy Skills](https://academy.openai.com/public/clubs/work-users-ynjqu/resources/skills) and [Help Center Skills](https://help.openai.com/en/articles/20001066): a repeatable small workflow and actual capability boundaries are relevant; ChatGPT workspace administration is not asserted to govern this Codex package.

## Coverage and grading

| Responsibility or boundary | Acceptance-relevant failure | Case or check | Grading evidence |
| --- | --- | --- | --- |
| Understanding first | Bare affirmation or questions before an interpretation | `understanding-before-questions` | Final response order, preserved intent, material uncertainty, and tool trace |
| Standalone alignment completion | Reconfirms agreement, requests implementation detail, or starts design/execution | `alignment-complete-stop` | Self-contained agreed content, completion statement, and absence of downstream action |
| Existing execution authority | Requires another generic approval after a scope answer | `authorized-work-handoff` | Preserved authorization and return to the owning workflow without new authority |
| Partial clarification | Declares readiness before material criteria are supplied | `iterative-provider-clarification-turn-2` | Current-prefix response, narrower material questions, and preserved answered scope |
| Next-workflow readiness | Blocks on vendor choice or investigation owned by design | `iterative-provider-clarification` | Final handoff retains constraints and leaves technical facts with design |
| Understanding discovery | Responds without loading the target Skill | `explicit-understanding-check` | Completed JSONL and observed installed Skill reads |
| Continued clarification | Fails to select clarification after a user answer | `clarification-continuation` | Observed handlers |
| Adjacent responsibility boundaries | Routes terminology, option exploration, or authorized implementation back to clarification | `terminology-preflight`, `explore-supported-options`, `approved-implementation` | Exact observed handler sets in the declared catalog |
| Complete migration | Loses original inputs or hidden requirements | One-time legacy/source comparison and repository checker | All original behavior scenarios and routing cases retained |
| Japanese reference fidelity and wording | Drops a permission, condition, or boundary, or leaves unnecessary English explanation words | Full-text source/translation comparison and remaining-English scan | Preserved meaning and identifiers; natural Japanese explanations and headings |

The seven original behavior scenarios become twelve executable conversation-prefix cases so every originally supplied user-answer stage can be selected independently.
Each prefix retains its original assertions and case-specific requirements, conditional on the supplied stage; future user answers are not executor inputs or requirements for an earlier stage.
The seven routing inputs retain the original target inclusion/exclusion; negative cases additionally identify the appropriate declared adjacent handler.
Three behavior cases and three routing cases are added for the audit responsibilities and their immediate boundaries.

The Runner produces one response to the final supplied user turn per execution.
These prefix observations do not reproduce a live adaptive conversation with prior model-generated replies; they must not be reported as long-running conversational evidence.
Historical baseline mappings, model settings, separate-grader protocol, and results remain in `results.json` instead of controlling the current executable definitions.

Generate a Runner `plan` before execution, inspect call counts, and keep raw fixtures, responses, JSONL, plans, and grades in the system temporary directory.
Grade only the planned requirements from the response and trace; the invoking audit session grades behavior, while the Runner derives routing outcomes from observed file loads.
Stop when selected requirements resolve the acceptance question; add comparison or repetition only for ambiguity, conflicting observations, instability, or a changed acceptance decision.

## Initial audit observations

Evaluated on 2026-09-27 with Codex CLI 0.155.1, `gpt-6-luna`, `max` reasoning, a read-only native permission profile, and the existing keyring authentication store.
No authentication configuration or credentials were changed.
Catalog, fixture access, denial of personal target-Skill reads, and read-only write boundaries passed before completed executions.

- Before the instruction change, two forced-Skill behavior observations returned an understanding paraphrase and a Ready handoff without downstream action. They did not demonstrate an unauthorized action or a general output-quality defect.
- Before the metadata change, `explicit-understanding-check` completed without any observed Skill loads in the declared catalog.
- The initial audit candidate passed five selected behavior cases and all 28 assigned requirements. These observations precede the explicit Objective wording and full Japanese revision; they are not executions of the final candidate.
- Five selected routing cases ultimately produced their expected handler sets: `clarify-request` for understanding and continuation, `define-referents` for terminology, `explore-decision-space` for option exploration, and `implement-changes` for authorized implementation.
- The first exploration observation returned the full intended Skill source but was undercounted because a trailing search failed. The case received a realistic README with the claimed billing goal, constraints, and read-only authority, then was rerun once. The corrected case recorded the intended handler. The other four results were reused only after confirming identical normalized case inputs, target manifest, and coexistence manifests.
- Two initial CLI invocations failed with unauthenticated requests after isolation passed, and one earlier attempt stopped at OS-restricted catalog inspection before any model call. Those attempts supply no behavioral evidence. Explicit use of the existing keyring store resolved authentication; the isolated CLI launch used the host execution permission required by this environment.
- Repository checker, 150 unit tests, and `git diff --check` passed. The source-to-migration comparison retained all original behavior scenarios, conversation prefixes, fixture data, assigned requirement text/criticality, case-specific constraints, and original routing target inclusion/exclusion.

The selected observations answer the target acceptance questions, so no unchanged cases, additional baseline cycles, repetition, model matrix, or consumer installation was added.
This is targeted behavioral and routing evidence, not a comprehensive benchmark or proof of causal improvement across prompts.
The initial audit source hashes were `sha256:a1a4c9f553627e3357302ce5163eddbf656aa474a0b4b7326322f2c5d2a46ee4` for `SKILL.md` and `sha256:8e6a8d53cd72f34db8debf5d0aaaafab88f94c4ef6993b964b09c1685026a932` for `SKILL-ja.md`.

## Final candidate evidence

The final English Objective explicitly covers intent alignment and resolution of ambiguity and missing information without inventing requirements, authority, or risk acceptance.
Comparison with the initial audit candidate confirms that the English `description` and all remaining instructions are unchanged.
The entire Japanese reference was reviewed and revised, including headings, the English-source notice, general explanation words, and sentence structure; identifiers and bilingual classification/state labels remain intact.
Full-text comparison preserves obligations, permissions, exclusions, uncertainty, authority boundaries, and completion conditions.
The remaining-English scan found only frontmatter keys, license and file identifiers, Skill names, `Issue`/`Skill` terminology, and explicitly paired classification/state labels.
The evaluation definitions and historical `results.json` are unchanged from the initial audit candidate.

On 2026-09-27, the final candidate completed one read-only execution each of `iterative-provider-clarification-turn-2`, `understanding-before-questions`, and `alignment-complete-stop` with Codex CLI 0.155.1, `gpt-6-luna`, and `max` reasoning.
All three cases and their 16 assigned requirements passed; `report.json` binds these observations to the final English and Japanese source manifests.
Each execution passed catalog, fixture access, personal-Skill denial, and read-only boundary checks, and its completed trace reads only the fixture English Skill.
The partial provider answer led to material follow-up questions without repeated answered scope or premature readiness; the understanding check began with a paraphrase; the completed agreement retained its constraints and ended clarification without downstream work.
The model observations test the English instructions; Japanese quality is established by source comparison and full-text language review, not by those model executions.

No routing case was rerun: the English selection metadata and adjacent responsibility boundaries are unchanged by this correction.
The prior five-case behavior and routing observations above remain bound to the initial audit candidate rather than being relabeled as final-candidate executions.
Repository checker, 150 unit tests, and `git diff --check` passed after updating the final evaluation record.
The selected results and static comparisons resolve this correction's acceptance questions; unselected cases, additional comparisons, and repeated observations were not required.

## Unverified boundaries and handoff

Unselected behavior and routing cases, live long-running conversations, other models, and Claude Code or other clients are not established by this audit.
Re-evaluate when a concrete regression, changed responsibility, or environment-specific support claim makes those observations relevant.
Issue #49 should receive the v2 decision and completed per-Skill migration status; Issue #38 should receive the metadata/discovery result for its final catalog check.
Issue #55's v1 reference should be reconciled with v2 when its execution record is posted.
The compound-command observation limitation also needs separate evaluation-infrastructure tracking through #49; it is not evidence of a selection failure in #65.
These are handoff items, not evidence that tracker updates or catalog-wide verification have occurred.
