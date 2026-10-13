# write-natural-japanese evals

SKILL.md is intentionally Japanese-canonical because this Skill's responsibility is Japanese writing and editing.
The Skill and its wording reference are original MIT-licensed material and do not adapt a third-party Skill.

## Evaluation assets

The behavior definitions live in evals.json and use the executable skill_name / evals format described in ../../../docs/evaluation.md.
The routing definitions live in triggers.json and use the same format with expected_handlers for direct routing observations.
The executor receives prompts without the assertions used for grading.
No historical results.json is committed for this Skill, and raw prompts, responses, JSONL events, and temporary fixtures remain outside the repository.
No report.json is committed for this change; the selected evidence is summarized here.

## Information architecture follow-up for Issue #98 — 2026-10-13

The main Skill now separates reader context, input role and change authority, source fidelity versus selectable material, grounded additions, local missing information, wording and structural limits, reference routing, and the full final-artifact check. The reference holds contextual wording decisions and examples. Its duplicated protection, Markdown, and final-check instructions were removed; the mixed-role storage example remains in a dedicated section. The final disclosure check now applies to material selected for writing, so it does not imply deletion of source claims during faithful translation or polishing. This is an information-architecture revision; passing behavioral examples alone cannot show that readers find it clearer.

External guidance consulted for this layout was the [Claude Agent Skills best-practices page](https://platform.claude.com/docs/ja/agents-and-tools/agent-skills/best-practices) and [OpenAI's Skills guidance](https://developers.openai.com/plugins/build/skills), accessed on 2026-10-13. Neither page identified a version number in the material reviewed, so the access date and URLs identify the consulted editions. The adopted scope is concise main instructions, direct reference links with stated read conditions, and a contents list in a long reference. No wording examples, templates, operational rules, or external Skill text were copied. The external pages' redistribution or adaptation licenses were not established; this change links to them without republishing their text. The repository Skill and reference remain original MIT-licensed material.

A read-only independent review of the pre-edit layout identified interleaved drafting decisions, duplicated protection and final-check instructions, and an unconditional disclosure check that could conflict with faithful editing. These findings guided the placement changes; no code or prose was accepted from that reviewer. The scope still ends at the prose needed for the requested finished artifact, rather than taking on standalone document-structure planning.

The final candidate plan selected N2, N4, N5, N7, and H, with five estimated model calls. One earlier plan was interrupted before it produced a run record because the candidate changed during execution; it is not graded evidence. The final five calls completed with Codex CLI 0.155.1, gpt-6-luna, max reasoning, read-only fixtures, the existing keyring credential, and a temporary HOME that isolated the personal same-name Skill. The Runner reported passing static, catalog, read-denial, and runtime isolation checks. N2 kept the faithful draft's investigation claim while the authorized summary omitted that detail and retained its uncertainty and review condition. N4 used 「保存状態」 for the explanation while retaining `storageState` and “Storage State”; its trace records a read of the relevant reference section. N5 produced a standalone notice with the `manual` default and `auto` behavior, without a made-up reason or public feature name. N7 kept A's section order and B's valid `#check` link after reordering, with the apply/review conditions intact. H preserved the source's requirements and technical names, used contextual Japanese rather than literal generic labels, and its trace records a complete `cat` of the reference. All five met their selected critical assertions on one run each; no naturalness score was allowed to offset a meaning, scope, or disclosure failure.

This focused run does not measure information-architecture readability, human comprehension, repeated-run stability, other clients or models, or every reference entry and Markdown form. D1/D2 discovery metadata and H's full-read condition were unchanged; D1/D2 were not rerun in this follow-up, and their earlier direct isolated observations remain the relevant routing evidence. The earlier N8 matched comparison found no measurable output gain for the conditional disclosure wording. The final candidate has no new matched baseline comparison because this follow-up primarily moves existing guidance and addresses the independent review's scope conflict.

## Restructure follow-up for Issue #98 — 2026-10-13

The Skill body now follows the judgment from input role and authorized change scope, through a grounded finished draft, to a full read of the final artifact. This implements the agreed distinction between faithful source text and selectable material; translation fidelity and independent fact research; visible reader context and private drafting discussion; and wording-only edits and authorized restructuring. It also states how to continue around local missing information, select only permissible content, and preserve conditions, links, anchors, and protected strings. The existing D1/D2 discovery boundary, named-expression reference reads, H's full-reference read, full-artifact check, and D3's explicit two-Skill use remain. The mixed-role relevant-section read added in the initial change remains too. No new dependency or external guide was added.

Before the body restructure, N5 (implicit material selection), N6 (unneeded versus indispensable unknowns), and N7 (wording-only versus full restructuring) each met the selected output requirements on one run. Those successes did not show that the prior instructions expressed the agreed decision flow. After the body restructure and before the last N4 trigger clarification, a six-call plan selected N2, N3, N5, N6, N7, and H; all six executions completed and met their selected assertions on one observation each. N5 directly checks standalone drafting without another writing Skill; N2 checks faithful editing and delegated summary; N3/N6 check known and missing facts; N7 checks structure authority, condition order, and anchor correspondence; H checks translation fidelity and a trace-recorded full reference read. The candidate ran with Codex CLI 0.155.1, gpt-6-luna, max reasoning, read-only fixtures, and the existing keyring credential store.

Adjacent checks exposed uncertainty. With the original HOME, D1 observed no handler as expected, while D2 completed the wording deliverable without loading the fixture Skill; its routing assertion failed. A D2 retry read a personal same-name Skill despite a passing Runner guard preflight. The Runner invalidated that execution, so its output is not candidate evidence. A temporary HOME with the existing CODEX_HOME and keyring login made the fixture available without changing user settings or credentials. A temporary symlink to the existing personal SKILL.md let the Runner deny both the temporary path and its resolved personal directory. Under this isolation, the catalog and read-denial preflights passed, D1 again observed no handler, and D2 read the fixture Skill as expected. A separately planned pre-restructure D2 run under the same isolation also read its fixture Skill. Both versions have the same description; the earlier non-read does not establish a description defect, although its exact cause remains unknown. The original-HOME permission-profile inconsistency is not resolved by this repository change.

N4 initially retained generic `storage state` and did not read the wording reference. After the relevant-section trigger named the mixed-role example explicitly, one N4 retest read that section and used 「保存状態」 while preserving the API and UI names. N8 compared the pre-restructure version and the final conditional wording under the same isolated setup: both retained the reader-relevant correction reason and omitted the irrelevant internal name. This supports the condition's intended behavior in one example but does not establish an output-quality gain. Repeated-run stability of N4 and D2 remains untested; neither output quality nor a successful catalog preflight substitutes for direct Skill-read evidence.

The restructure is a design decision supported by the adopted Issue scope, not a measured quality gain from passing cases: N5–N7 also passed before it. The selected final outputs do not establish repeated-run stability, human comprehension gains, all possible Markdown/link relationships, or behavior in other clients and models. Reader-shared-thread context and independent fact verification boundaries are explicit instructions but were not directly tested in the selected run. The evaluation definitions and prose evidence remain in this directory; raw artifacts remain outside the repository.

## Initial focused change for Issue #98 — 2026-10-13

The change tests input roles and requested scope with N1 (standalone drafting from public and private notes), N2 (faithful polishing versus delegated summary), N3 (a locally unknown behavior), and N4 (generic explanation beside an API identifier and a UI label). H checks translation meaning and the full-reference read after the wording change. D3 checks the explicitly requested coexistence of two Skills; its optional assertions now grade the finished text instead of attributing separate work to each Skill. D1 and D2 remain unchanged. The existing relevant-section read for named expressions and H's full-reference read are preserved; step 4 additionally calls for reading the relevant section when explanatory wording, an identifier, and a UI label share a context. N1 is the direct standalone drafting test, separate from D3.

Plans were inspected before execution: the initial current-version plan had four calls (N1–N4); after an authentication-store error, successful plans used one call for N1 and three for N2–N4. N4's three-condition comparison planned three calls. Each later decision-relevant retest planned one call. Runs used Codex CLI 0.155.1, gpt-6-luna, max reasoning, read-only fixtures, and the existing keyring credential store. The first four-call attempt completed no model outputs because its isolated default authentication sent no bearer credential (401); its case results are errors, not grades. No credentials or authentication settings were created or changed.

| Case | Current version | Final candidate and relevant comparison |
| --- | --- | --- |
| N1 | Pass: public notice from notes, without the internal working name or invented plans | Not rerun; drafting instructions were not changed |
| N2 | Pass: faithful version keeps claims and uncertainty; delegated summary retains critical conditions | Not rerun; scope instructions were not changed |
| N3 | Fail: changed “exception not emitted” to “exception does not occur” | Pass after clarifying the distinction; no claim about logs or screen notifications |
| N4 | Fail: generic `storage state` remained English | Without Skill and baseline also retained the English explanation. First candidate revision did too; the next removed the subject of the definition. Final candidate uses 「保存状態」 while preserving `storageState`, “Storage State”, and the definition |
| H | Previously passing record; not rerun on the current version | Pass on the candidate before the final N3 clarification; trace shows a complete `cat` read of the wording reference and the output preserves its facts, conditions, identifiers, and product name |
| D3 | Previously passing record; not rerun on the current version | Pass on the candidate before the final N3 clarification; direct routing observation loaded both named Skills, and output preserves `sync_mode` and the uncertain cause with clear headings and paragraphs |

N4's final candidate is one successful observation after two unsuccessful candidate observations. It is evidence for this selected example, not proof of stable improvement across repeated runs. The model outputs were graded for meaning and scope before naturalness; N3's stronger, unsupported claim was treated as a failure despite sounding natural. N1–N3 were not run without the Skill or under the final candidate unless shown above. No human reader comprehension study, other client, or other model was evaluated. No new external style guide was adopted or copied; the wording examples are original repository material.

## Selection for Issue #47

The changed responsibility is to treat a rewritten document as a new final artifact and recheck its semantics, certainty, scope, terminology, protected strings, Markdown syntax, and newly introduced mixed-language expressions.
The change also adds a conditional consistency pass for multiple related documents in one request.
The wording reference now distinguishes translation sources and references from formal or defined uses of 正本 without introducing unsupported uniqueness.
The evaluation definitions were fully migrated from the legacy scenarios format because this pull request materially changes the Skill and its evaluation definitions.

The selected model-backed paths are:

- targeted-candidate: C, I, and K.
- baseline-comparison: H, I, and J.
- targeted-routing: D1, D2, and D3.

C rechecks uncertainty, established terminology, quotation, and the existing investigation sequence.
H rechecks source-language translation, contextual wording, protected identifiers, and the requirement to read the full reference.
I checks the distinction between a translation source and a formal 正本 while preserving links, URLs, paths, and procedure names.
J checks the final pass over two related documents, cross-document terminology consistency, conditions, protected technical strings, and long-document drift.
K checks separation of a requested final artifact from requested editing reasons.
D1, D2, and D3 preserve the ordinary-response, explicit-wording-deliverable, and explicitly selected coexistence boundaries.

The remaining behavior cases A, B, E, F1, F2, and G were migrated but not rerun because the selected Issue #47 responsibilities do not require another observation of their unchanged acceptance questions.
Repetition was not performed because the executed cases completed without conflicting or unstable evidence.

## Human grading procedure

1. Generate a plan with scripts/run_skill_evaluation.py and inspect the estimated model-call count.
2. Run each approved plan once with an explicit maximum equal to or greater than the estimate.
3. Grade every planned assertion from the captured final output and direct routing observations.
4. Treat a missing or incomplete routing stream as inconclusive rather than inferring a handler from the final response.
5. Preview the change-scoped report without writing it when a committed report is not needed.
6. Keep unselected responsibilities and untested client or model behavior explicit.

## Executed evidence — 2026-09-17

The evaluations were rerun after correcting the JSON newline escapes in I/J/K and adding a fenced code block and list to J.
They ran in Codex CLI 0.155.0-alpha.2.6 with gpt-5.6-luna, max reasoning effort, and read-only execution.
The candidate and baseline fixtures were isolated to the target Skill and the required wording reference.
The repository static check embedded in each Runner execution passed.

| Path | Cases and conditions | Result |
| --- | --- | --- |
| targeted-candidate | C, I, K under candidate | Pass; 3 of 3 cases passed |
| baseline-comparison | H, I, J under candidate and baseline | Pass; all 6 case-condition results passed |
| targeted-routing | D1, D2, D3 under candidate | Pass; all 3 routing observations matched |

The direct routing observations were D1 with no handler, D2 with write-natural-japanese, and D3 with japanese-tech-writing plus write-natural-japanese.
The candidate outputs preserved uncertainty and established terms in C, separated translation-source meaning from 正本 in I, preserved protected strings, conditions, code fences, and list structure in J, and separated the completed prose from reasons in K.
The baseline comparison also passed the same I and J assertions, including the Markdown structure assertion.
The H traces directly recorded reads of SKILL.md and the full wording reference for both candidate and baseline conditions.

## Acceptance scope and unverified boundaries

The selected evidence supports the Issue #47 responsibilities in the recorded Codex and Luna environment.
It does not establish behavior for unselected cases, other clients, other models, other reasoning settings, or repeated-run stability.
It does not establish that every possible long document or multi-document request will be semantically consistent.
The selected acceptance evidence is summarized in this README; no current results.json report is committed.
