# write-natural-japanese evals

SKILL.md is intentionally Japanese-canonical because this Skill's responsibility is Japanese writing and editing.
The Skill and its wording reference are original MIT-licensed material and do not adapt a third-party Skill.

## Evaluation assets

The behavior definitions live in evals.json and use the executable skill_name / evals format described in ../../../docs/evaluation.md.
The routing definitions live in triggers.json and use the same format with expected_handlers for direct routing observations.
The executor receives prompts without the assertions used for grading.
No historical results.json is committed for this Skill, and raw prompts, responses, JSONL events, and temporary fixtures remain outside the repository.
No report.json is committed for this change; the selected evidence is summarized here.

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
