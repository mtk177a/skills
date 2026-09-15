# write-natural-japanese evals

`SKILL.md` is intentionally Japanese-canonical because the Skill's responsibility is Japanese writing and editing.
The Skill and reference are original MIT-licensed material and do not adapt a third-party Skill.

## Evaluation selection

- Affected responsibility: create a new language-level writing Skill and define its routing and coexistence boundary with `japanese-tech-writing`.
- Purpose: determine whether the Skill improves context-appropriate Japanese without changing meaning, certainty, quotations, or established terminology.
- Selected path: matched baseline comparison for subjective output quality, a targeted regression case for the discovered deterministic-wording ambiguity, plus targeted routing and coexistence checks for the new discovery boundary.
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

### Scenario E: Preserve technical determinism

A technical note describes a detection process that returns the same result for identical input and uses `deterministic` to name that property.
The executor must revise the wording without reducing the property to merely automatic or routine processing.

Requirements checklist:

1. [critical] Preserve the same-input, same-result condition
2. [critical] Do not replace technical determinism with a claim only about mechanical or automatic execution
3. Preserve a technical term when translating it would lose the property
4. Do not add unsupported claims about randomness, implementation, or guarantees

## Comparison procedure

1. Run each baseline and candidate task once in separate ephemeral, read-only Codex sessions with the same model, reasoning setting, repository instructions, and user input.
2. Give the candidate session this Skill and only the supporting reference required by the scenario; do not reveal grading criteria to either executor.
3. Remove run labels and randomize output order before grading.
4. Use a separate Codex session to compare meaning preservation, technical accuracy, Japanese naturalness, terminology, and over-editing against the scenario checklist.
5. Record observable Skill-loading evidence when the client exposes it; otherwise mark routing as `not exposed` rather than inferring activation from wording.
6. Repeat only an ambiguous or conflicting case and state why the additional observation was needed.
7. Keep raw prompts and outputs in a disposable directory outside the repository, and commit only the summarized result.

## Iter 1 — Codex comparison (Luna rerun)

- Evaluation date: `2026-09-14`
- Candidate source: PR #43 working tree after the deterministic-wording fix; no commit was created for this evaluation
- Client: Codex CLI `0.154.0`
- Model: `gpt-5.6-luna`
- Reasoning effort: `max`
- Sandbox: separate ephemeral, read-only sessions with identical task text
- Execution: baseline fixtures omitted the target Skill; candidate fixtures contained the current Skill and reference under a unique temporary path, and candidate loading was confirmed from JSONL command output
- Grading: direct checklist grading plus a separate Luna session with baseline and candidate outputs in blinded order

The A–E matched comparison passed every assigned critical requirement.
Cases A through D preserved the stated behavior, conditions, uncertainty, identifiers, quotation, and established terminology.
Case E preserved the technical property that identical input produces identical output, and the candidate output did not reduce `deterministic` to merely mechanical or routine processing.

The first blinded grader pass was excluded from the result because its Case C fixture omitted the source word 「キャッシュ」 and its Case A judgment assumed a warning-versus-notification distinction that the source did not specify.
A targeted Luna re-grade with the corrected Case C facts and the original Case A wording passed both cases with no supported critical violation.

The routing check used a disposable candidate repository and JSONL loading evidence.
An ordinary Japanese debugging request did not read either target Skill.
A request covering both Japanese wording and technical-article structure read the local `write-natural-japanese/SKILL.md`, `japanese-tech-writing/SKILL.md`, and `references/wording-decisions.md`, and the resulting draft preserved the uncertainty and identifier while applying both responsibilities.

Installed global copies of the target Skills were disabled with exact `skills.config` path overrides for the accepted runs.
User configuration remained loaded because `--ignore-user-config` selected an authentication route that returned `401` before model execution; those attempts were excluded from pass evidence.
No global target Skill content was observed in the accepted traces.

### Result

- Output quality: pass for A–E under direct checklist grading and the corrected blinded re-grade
- Meaning and certainty preservation: pass in all five matched cases
- Technical determinism regression: pass in the targeted Case E
- Established terminology and quotation: pass in Case C
- Ordinary-conversation boundary: pass from observable absence of target Skill reads
- Coexistence with `japanese-tech-writing`: pass from observable reads of both Skills and the target reference
- Static validation: `git diff --check` and `python3 scripts/check_repository.py` passed after the fix
- Repetition: targeted re-grade performed for A and C because the first grader had an invalid fixture and an ambiguous judgment; no conflicting supported finding remained

The evidence supports this Skill on the executed Codex CLI `0.154.0` with `gpt-5.6-luna` at `max` reasoning only.
It does not establish behavior in Claude Code, GitHub Copilot, Gemini CLI, other models, other reasoning settings, or other execution environments.
Raw prompts, outputs, and JSONL events were kept in disposable directories outside the repository and are not repository artifacts.
