# write-natural-japanese evals

`SKILL.md` is intentionally Japanese-canonical because the Skill's responsibility is Japanese writing and editing.
The Skill and reference are original MIT-licensed material and do not adapt a third-party Skill.

## Evaluation selection

- Affected responsibility: create a new language-level writing Skill and define its routing and coexistence boundary with `japanese-tech-writing`.
- Purpose: determine whether the Skill improves context-appropriate Japanese without changing meaning, certainty, quotations, or established terminology.
- Selected path: matched baseline comparison for subjective output quality, targeted cases for technical determinism and context-dependent uses of contract and gate terminology, plus routing and coexistence checks for the discovery boundary.
- Current targeted change: require the wording reference to be read when translating from another language into Japanese, because source-language expressions may not match the Japanese terms that trigger expression-specific reading.
- Current selected path: one candidate-only English-source translation case is sufficient to expose the changed reference-reading path, contextual translation, and preservation of a formal term; unchanged core, routing, and coexistence cases are not rerun.
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

### Scenario D1: Do not trigger for ordinary Japanese debugging

An ordinary debugging question is answered in Japanese but does not ask for writing or editing as its deliverable.
The executor must answer the question without loading `write-natural-japanese` merely because the response language is Japanese.

Requirements checklist:

1. [critical] Do not apply this Skill merely because the debugging response is Japanese
2. Answer the debugging question directly without turning it into a prose-editing task

### Scenario D2: Trigger for an explicit Japanese wording deliverable

A request names natural Japanese wording as its deliverable without naming this Skill.
The executor must load `write-natural-japanese`, preserve the supplied behavior and condition, and remove source-language interference.

Requirements checklist:

1. [critical] Load `write-natural-japanese` from the implicit wording request
2. [critical] Preserve the behavior for invalid values and the `reload_mode` condition
3. Replace unnecessary English generalities and source-language structure with natural Japanese
4. Preserve identifiers and return only the revised text

### Scenario D3: Compose explicitly selected Japanese writing Skills

A request names `write-natural-japanese` and `japanese-tech-writing` as the two available Skills to use on a technical article fragment.
The executor must read both Skills and apply their separate wording and document-structure responsibilities without treating either as a companion dependency.

Requirements checklist:

1. [critical] Read both named Skills
2. [critical] Preserve `sync_mode` and keep the race condition as a hypothesis
3. Apply `write-natural-japanese` to linguistic realization and wording
4. Apply `japanese-tech-writing` to headings, paragraphs, and argument structure
5. Return only the revised article fragment

### Scenario E: Preserve technical determinism

A technical note describes a detection process that returns the same result for identical input and uses `deterministic` to name that property.
The executor must revise the wording without reducing the property to merely automatic or routine processing.

Requirements checklist:

1. [critical] Preserve the same-input, same-result condition
2. [critical] Do not replace technical determinism with a claim only about mechanical or automatic execution
3. Preserve a technical term when translating it would lose the property
4. Do not add unsupported claims about randomness, implementation, or guarantees

### Scenario F1: Make generic contract wording concrete

A Japanese API design note calls an output requirement and a compatibility requirement a 「契約」 while also referring to contract testing as an established practice.
The executor must state the two requirements directly without removing the established technical term.

Requirements checklist:

1. [critical] Preserve the stated output requirements and compatibility guarantees
2. [critical] Express each generic use directly as the output behavior or requirement and the compatibility requirement it represents; retaining 「契約」 as the governing label does not satisfy this requirement
3. Preserve contract testing as an established technical term
4. Do not invent legal force, parties, enforcement, or violation behavior

### Scenario F2: Preserve defined and established contract terminology

A technical explanation uses contract testing and Design by Contract as established terms and explicitly defines `API contract` as a term used in its public specification.
The executor must preserve those semantic roles without mechanically translating `API contract` into 「API の契約」.

Requirements checklist:

1. [critical] Preserve what contract testing checks and its distinction from Design by Contract
2. [critical] Preserve contract testing, Design by Contract, and the explicitly defined `API contract`
3. Do not mechanically translate `API contract` into the generic Japanese phrase 「API の契約」
4. Do not add requirements, enforcement behavior, or legal meaning

### Scenario G: Distinguish gates from entrances, checks, and controls

A Japanese delivery note uses 「ゲート」 or 「門」 for a starting point, an automated check, a human approval, and an access-control decision while also naming a product's Quality Gate.
The executor must express each role clearly without changing the formal product term.

Requirements checklist:

1. [critical] Preserve which step starts the process and which decisions prevent progress or access
2. Distinguish the starting point, automated check, human approval, continuation decision, and access control
3. Preserve the product's formal Quality Gate name
4. Do not treat every entrance as a pass/fail control or replace every gate expression with the same word

### Scenario H: Translate source-language wording through contextual guidance

An English technical explanation uses `API contract`, `silently fails`, `source of truth`, and `quality gate` for different roles while also naming the formal product feature DeployGuard Quality Gate.
The executor must read the wording reference and translate the general expressions according to the supplied facts without changing the formal term.

Requirements checklist:

1. [critical] Read `references/wording-decisions.md`; wording alone does not prove the read
2. [critical] Preserve the output, compatibility, validation, warning, runtime-use, schema-management, approval, and product-check facts
3. [critical] Translate the general source expressions by their stated roles instead of applying corresponding Japanese labels mechanically
4. [critical] Preserve `result_id`, `mode`, and DeployGuard Quality Gate
5. Do not invent legal meaning or behavior absent from the source
6. Return only the translated reader-facing text

## Comparison procedure

1. Run each selected task once in a separate ephemeral, read-only Codex session with the same model, reasoning setting, repository instructions, and user input for every condition being compared.
2. Use matched baseline and candidate sessions only for the scenarios whose acceptance depends on comparative output quality; use candidate-only sessions for routing and coexistence checks.
3. Give each candidate session this Skill and only the adjacent Skill or supporting reference required by the scenario; do not reveal grading criteria to the executor.
4. Grade each output against every requirement before comparing the two outputs.
5. For F1, treat generic 「契約」 retained as the governing label as a failure of the concrete-wording requirement even if the surrounding sentence states the underlying facts.
6. Remove run labels and randomize output order before comparing outputs that satisfy the critical requirements.
7. Use a separate Codex session to compare meaning preservation, technical accuracy, Japanese naturalness, terminology, and over-editing when independent comparative judgment is needed; record targeted requirement compliance separately from overall prose preference.
8. Record observable Skill-loading evidence when the client exposes it; otherwise mark routing as `not exposed` rather than inferring activation from wording.
9. Repeat only an ambiguous or conflicting case and state why the additional observation was needed.
10. Keep raw prompts and outputs in a disposable directory outside the repository, and commit only the summarized result.

## Evaluation fixtures

[`evals.json`](evals.json) contains the complete executor inputs, isolation, routing, and coexistence configurations, and hidden grading requirements for Scenarios A through E and F1 through H.
Executors receive only the shared executor instruction and the selected scenario prompt, except that the D1 routing-negative case omits the writing-specific shared instruction.
D2 tests implicit routing with only `write-natural-japanese` available, while D3 names both available Skills in the request without using a client-specific invocation syntax.
H tests the source-language translation path with only `write-natural-japanese` and its reference available.

## Current result — 2026-09-15

- Candidate source: working tree based on `d5b4200c41f1c42f4616517c3c16e62994a68332`
- `SKILL.md` SHA-256: `2e1fed1d442d64e9969705a4b44deacb98df0c811468ecda15be63399b64cf2b`
- `references/wording-decisions.md` SHA-256: `a63a19f2d11313a50d7d91f2209757c0000ad0ef04e64b845aa6b77b90f07b88`
- Fixture SHA-256: `eb58a0fb35afaac5f67e16aff201c623b8301ec7207797d5028662b591c3f50c`
- Client: Codex CLI `0.154.0-alpha.6.2`
- Model: `gpt-5.6-luna`
- Reasoning effort: `max`
- Retained evidence: the matched baseline and candidate results for A through C, E, F1, F2, and G, and the routing-negative result for D1, remain applicable because their inputs, requirements, and evaluated Skill content are unchanged
- New execution: D2 and D3 each ran once as candidate-only tasks in separate ephemeral, read-only sessions
- Isolation: D2 contained only the recorded working-tree copy of `write-natural-japanese`; D3 also contained the repository copy of `japanese-tech-writing`; exact global copies of adjacent writing Skills were disabled
- Invocation: `codex exec --ephemeral --json --ignore-rules --skip-git-repo-check --sandbox read-only --model gpt-5.6-luna -c 'model_reasoning_effort="max"' -c 'skills.config=[<disabled-global-adjacent-skills>]' -C <disposable-fixture> -`
- Authentication: user configuration remained loaded because the earlier `--ignore-user-config` route failed before model execution; no global target Skill content was observed in the accepted traces
- Grading: the retained baseline comparisons use direct requirement checks and the existing blinded Luna comparison; D2 and D3 use direct requirement and observable-load checks because no relative prose judgment is needed
- Repetition: D2 and D3 were not repeated because their first results were complete and unambiguous; the earlier G repetition remains applicable

| Scenario | Evidence | Decision |
| --- | --- | --- |
| A | Preserved all technical conditions and removed source-language interference; both matched outputs passed, with the baseline preferred overall | Pass |
| B | Preserved parsing, warning, and runtime-use facts without relying on the vague phrase; the candidate was preferred | Pass |
| C | Preserved uncertainty, established terms, quotation, identifiers, and investigation order; the candidate was preferred | Pass |
| D1 | Answered the debugging question directly without reading `write-natural-japanese/SKILL.md` | Pass |
| D2 | Read `write-natural-japanese/SKILL.md` without the Skill being named, preserved the invalid-value and `reload_mode` conditions, and removed the source-language interference | Pass |
| D3 | Read both named Skill files, preserved `sync_mode` and the hypothesized cause, and applied wording and article-structure responsibilities in the output | Pass |
| E | Preserved the same-input, same-settings, same-result property without reducing it to automatic execution; the candidate was preferred | Pass |
| F1 | Read the Skill and reference, replaced generic 「契約」 with guaranteed behavior and a compatibility requirement, and preserved `contract testing`; the candidate was preferred | Pass |
| F2 | Preserved contract testing, Design by Contract, and the explicitly defined `API contract`; both outputs passed, with the baseline preferred overall | Pass |
| G | Preserved the workflow and DeployGuard Quality Gate and expressed the start, test, approval, access decision, and formal quality check as separate roles; evidence for automated-check wording remains limited | Pass |

### Acceptance decision

The current candidate is accepted in the recorded Codex and Luna reference environment for the evaluated responsibilities.
Every critical requirement passed, including implicit selection of `write-natural-japanese`, explicit coexistence with `japanese-tech-writing`, context-dependent contract wording, and preservation of meaning, certainty, identifiers, and established terminology.

The prior D2 observations are excluded from acceptance evidence because that fixture incorrectly made implicit selection of an adjacent independent Skill part of the target Skill's coexistence requirement.
The replacement D2 evaluates implicit routing of `write-natural-japanese`, while D3 evaluates composition after both independent Skills have been named for use.
Implicit selection of `japanese-tech-writing` is not evaluated and is not an acceptance requirement for this Skill.

Before the final suite, a focused F1 candidate check exposed that the earlier conditional reference link did not reliably cause the executor to read the reference.
The final candidate adds the expression names to the `SKILL.md` reference-reading condition; the complete result table uses only executions made after that correction.

Static validation passed with the bundled `quick_validate.py`, `python3 scripts/check_repository.py`, JSON parsing, and `git diff --check` before model execution.
The same checks passed again after this result record was updated.

This evidence applies only to the recorded working-tree content on Codex CLI `0.154.0-alpha.6.2` with `gpt-5.6-luna` at `max` reasoning.
Claude Code, GitHub Copilot, Gemini CLI, other models, other reasoning settings, and other execution environments remain unverified.
Raw prompts, outputs, JSONL events, and the blinding map were kept in a disposable directory outside the repository and are not repository artifacts.
