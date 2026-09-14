# write-natural-japanese evals

`SKILL.md` is intentionally Japanese-canonical because the Skill's responsibility is Japanese writing and editing.
The Skill and reference are original MIT-licensed material and do not adapt a third-party Skill.

## Evaluation selection

- Affected responsibility: create a new language-level writing Skill and define its routing and coexistence boundary with `japanese-tech-writing`.
- Purpose: determine whether the Skill improves context-appropriate Japanese without changing meaning, certainty, quotations, or established terminology.
- Selected path: matched baseline comparison for subjective output quality, plus targeted routing and coexistence checks for the new discovery boundary.
- Escalation: repeat only a case whose first comparison is ambiguous, conflicting, or exposes unstable behavior.
- Untested boundary: behavior outside the executed Codex client and model remains unverified.

## Iter 0 — Static check

- the description limits implicit selection to work whose primary deliverable is Japanese prose
- ordinary Japanese conversation, mechanical proofreading, structure-only editing, and AI-text detection remain outside the responsibility
- the body preserves meaning, certainty, quotations, formal names, identifiers, and established terminology
- the reference treats listed expressions as contextual review prompts rather than banned words or fixed replacements
- `japanese-tech-writing` remains optional and controls document structure when both Skills apply
- every supporting reference is linked from `SKILL.md` with a condition for reading it
- no script, hook, external dependency, client-specific metadata, or companion relationship is introduced
- [critical] wording revision must not turn an uncertain or unverified claim into a confirmed fact
- [critical] wording revision must not change the technical behavior described by the source

## Behavioral scenarios

### Scenario A: Remove source-language interference and unnecessary English

A Japanese technical explanation retains English nominalization, general English labels, and source-language sentence structure.
The executor must produce a reader-facing explanation without changing its technical claims.

Requirements checklist:

1. [critical] Preserve every technical claim and condition in the source
2. Replace unnecessary English generalities with context-appropriate Japanese
3. Reconstruct sentences instead of applying word-for-word substitutions
4. Preserve code, configuration keys, and formal product terms
5. Do not append an explanation of the editing rules unless requested

### Scenario B: Make an underspecified failure observable

A draft says a setting is “silently ignored,” while the supplied facts establish that it is parsed successfully, produces no warning, and is not used during execution.
The executor must revise the sentence for a Japanese operational note.

Requirements checklist:

1. [critical] Preserve all three supplied behavioral facts
2. State what is not reported and where the value ceases to affect processing
3. Do not invent logging, exception, persistence, or recovery behavior
4. Do not rely on replacing one flagged phrase with another vague phrase

### Scenario C: Preserve established terms, quotation, and uncertainty

A Japanese investigation note correctly uses `既定値` and `原因を切り分ける`, quotes `正本` as the term under discussion, and identifies a race condition only as a hypothesis.
The executor must improve the wording without changing those semantic roles.

Requirements checklist:

1. [critical] Keep the race condition qualified as a hypothesis
2. Preserve `既定値` and the established troubleshooting use of `原因を切り分ける`
3. Preserve quoted language that is the object of analysis
4. Change a listed expression only when its context makes the change beneficial
5. Do not equate naturalness with removing every expression named in the reference

### Scenario D: Respect routing and coexistence boundaries

The routing check contains two matched requests: an ordinary debugging question answered in Japanese, and a request to revise the wording and argument structure of a Japanese technical article with both this Skill and `japanese-tech-writing` available.

Requirements checklist:

1. [critical] Do not apply this Skill merely because the debugging response is Japanese
2. Select this Skill when Japanese wording itself is an explicit deliverable
3. Allow `japanese-tech-writing` to control headings, paragraphs, and argument structure in the article case
4. Apply this Skill only to linguistic realization and wording in the coexistence case
5. Do not require either Skill as a companion of the other

## Comparison procedure

1. Run each baseline and candidate task once in separate ephemeral, read-only Codex sessions with the same model, reasoning setting, repository instructions, and user input.
2. Give the candidate session this Skill and only the supporting reference required by the scenario; do not reveal grading criteria to either executor.
3. Remove run labels and randomize output order before grading.
4. Use a separate Codex session to compare meaning preservation, technical accuracy, Japanese naturalness, terminology, and over-editing against the scenario checklist.
5. Record observable Skill-loading evidence when the client exposes it; otherwise mark routing as `not exposed` rather than inferring activation from wording.
6. Repeat only an ambiguous or conflicting case and state why the additional observation was needed.
7. Keep raw prompts and outputs in a disposable directory outside the repository, and commit only the summarized result.

## Iter 1 — Codex comparison

- Candidate commit: `9c36c94`
- Client: Codex CLI `0.154.0-alpha.6.2`
- Model: `gpt-6-astra`
- Reasoning effort: `none`
- Execution: separate ephemeral, read-only sessions with identical task text; the candidate session explicitly loaded this Skill
- Grading: a separate Codex session received outputs in blinded order and applied the scenario requirements

The first matched comparison covered source-language interference, observable failure behavior, and preservation of established terms, quotation, and uncertainty.
The grader found the baseline and candidate outputs equivalent in all three cases, with no critical requirement violations.
The baseline already produced strong Japanese and automatically loaded the existing `japanese-tech-writing` Skill for the technical-explanation case, so these prompts did not distinguish the new responsibility.

One additional comparison used a longer synthetic user announcement that combined unnecessary English, an underspecified import behavior, causal uncertainty, and a `source of truth` relationship.
The grader preferred the candidate output because it preserved the uncertainty and identifiers while making the nightly overwrite source explicit; the baseline left that relationship implicit and used `正本` without establishing its document-management meaning.
Neither output had a critical requirement violation.

The routing check installed this Skill and `japanese-tech-writing` together in a disposable repository and used Codex JSONL events as observable loading evidence.
An ordinary Japanese debugging request did not read either Skill.
A request covering both Japanese wording and technical-article structure read both `SKILL.md` files, then read `references/wording-decisions.md`; the resulting article preserved its measurements, uncertainty, and identifiers while applying the two responsibilities together.

### Result

- Output quality: pass for the evaluated candidate, with one discriminating case showing an improvement and three simpler cases showing no regression
- Meaning and certainty preservation: pass in all executed candidate cases
- Established terminology and quotation: pass in the preservation case
- Ordinary-conversation boundary: pass from observable absence of Skill reads in the debugging case
- Coexistence with `japanese-tech-writing`: pass from observable reads and the resulting article
- Repetition: not run because the discriminating result was unambiguous and no case produced conflicting evidence

The evidence supports this Skill on the executed Codex client and model only.
It does not establish improvement for every Japanese writing task or behavior in Claude Code, GitHub Copilot, Gemini CLI, other models, or other reasoning settings.
Raw prompts, outputs, and JSONL events were kept in a disposable directory and are not repository artifacts.
