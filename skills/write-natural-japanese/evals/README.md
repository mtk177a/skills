# write-natural-japanese evals

SKILL.md is intentionally Japanese-canonical because this Skill's responsibility is Japanese writing and editing.
The Skill and its wording reference are original MIT-licensed material and do not adapt a third-party Skill.

## Evaluation assets

The behavior definitions live in evals.json and use the executable skill_name / evals format described in ../../../docs/evaluation.md.
The routing definitions live in triggers.json and use the same format with expected_handlers for direct routing observations.
The executor receives prompts without the assertions used for grading.
No historical results.json is committed for this Skill, and raw prompts, responses, JSONL events, and temporary fixtures remain outside the repository.
No report.json is committed for this change; the selected evidence is summarized here.

## Restructure follow-up for Issue #98 — 2026-10-13

The Skill body now follows the judgment from input role and authorized change scope, through a grounded finished draft, to a full read of the final artifact. This implements the agreed distinction between faithful source text and selectable material; translation fidelity and independent fact research; visible reader context and private drafting discussion; and wording-only edits and authorized restructuring. It also states how to continue around local missing information, select only permissible content, and preserve conditions, links, anchors, and protected strings. The existing D1/D2 discovery boundary, named-expression reference reads, H's full-reference read, full-artifact check, and D3's explicit two-Skill use remain. The mixed-role relevant-section read added in the initial change remains too. No new dependency or external guide was added.

Before the body restructure, N5 (implicit material selection), N6 (unneeded versus indispensable unknowns), and N7 (wording-only versus full restructuring) each met the selected output requirements on one run. Those successes did not show that the prior instructions expressed the agreed decision flow. After the body restructure and before the last N4 trigger clarification, a six-call plan selected N2, N3, N5, N6, N7, and H; all six executions completed and met their selected assertions on one observation each. N5 directly checks standalone drafting without another writing Skill; N2 checks faithful editing and delegated summary; N3/N6 check known and missing facts; N7 checks structure authority, condition order, and anchor correspondence; H checks translation fidelity and a trace-recorded full reference read. The candidate ran with Codex CLI 0.155.1, gpt-6-luna, max reasoning, read-only fixtures, and the existing keyring credential store.

Adjacent checks exposed uncertainty. D1 directly observed no Skill handler as expected, but D2 completed the wording deliverable without loading the fixture Skill, so its routing assertion failed. A single D2 retry read a personal same-name Skill despite a passing Runner guard preflight; the Runner marked that execution invalid, and its output is not candidate evidence. N4 initially retained generic `storage state` and did not read the wording reference. After the relevant-section trigger named the mixed-role example explicitly, one N4 retest read that section and used 「保存状態」 while preserving the API and UI names. The D2 boundary and repeated-run stability of N4 remain unconfirmed; neither output quality nor a successful catalog preflight substitutes for direct Skill-read evidence.

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
