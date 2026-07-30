# calibrate-learning-support evals

## Purpose

Verify that `calibrate-learning-support` adjusts AI learning support around an active task so the user can retain or recover decision-relevant understanding without blocking authorized progress, taking over user-owned decisions, or turning every task into a lesson.

## Assets

- `triggers.json`: trigger, continuation, near-miss, and coexistence selection cases
- `evals.json`: previous-name, no-Skill, and candidate behavior cases with hidden requirement assignments
- `results.json`: compact evidence for the accepted revision after execution
- this README: static contract, coverage, protocol, and summarized results

## Static check

- `description` covers explicit learning intent, inability to evaluate AI output, preserving understanding while delegating, continuation after a checkpoint, and material negative boundaries.
- The body defines a multi-turn calibration cycle around an originating workflow rather than a one-time study plan.
- Learning depth and time pressure are continuous decision inputs rather than a binary choice.
- User-owned decisions, delegatable work, evidence, AI inference, and unknowns remain distinct.
- Clear authorized work is not blocked merely because the domain is unfamiliar.
- Checkpoints, concepts, questions, and self-study tasks have no fixed count and are emitted only when they can change the next action.
- The Skill remains self-contained and does not require a companion Skill, script, external source, or client-specific feature.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Task-specific calibration | Produces a generic curriculum or full implementation without protecting the requested understanding | `learning-priority-library-change` | Requirement-level grader |
| Progress under time pressure | Refuses a clear direct answer or forces a lesson because the domain is unfamiliar | `deadline-execute-and-explain` | Response inspection |
| Recovering understanding | Treats an AI patch or passing test as self-validating | `reconstruct-ai-generated-fix` | Evidence and unknowns grader |
| Iteration across turns | Treats one response as complete or repeats resolved material | `partial-understanding-continuation` | Per-turn transcript grader |
| Decision ownership | Approves a consequential production choice for the user or dumps all technical analysis back to them | `high-risk-adoption-decision` | Critical ownership assertions |
| Adaptive output | Always emits a quiz, fixed concept list, study plan, or template | All behavior cases | Cross-case inspection |
| Trigger and continuation | Misses explicit learning intent or a follow-up checkpoint | `triggers.json` | Observable Skill load |
| Adjacent routing | Absorbs tool selection, ordinary implementation, general teaching, or request clarification | `triggers.json` | Observable Skill load |

## Behavioral execution protocol

1. Load `calibrate-ai-learning` from baseline commit `82722ad5cfe003c164bb6b3736fae3612d4612a2` for the previous-name condition, use no Skill for the no-Skill condition, and use the working-tree `calibrate-learning-support` for the candidate.
2. Run each condition in a disposable directory with only the condition's Skill and declared task input.
3. For multi-turn cases, accumulate the visible conversation. Keep hidden assertions and expected conclusions out of executor input.
4. Use a separate grader with the transcript, assigned assertions, and hidden additional requirement.
5. A failed critical assertion fails the case. A partial result without a critical failure is partial.
6. Keep raw prompts, responses, JSONL, and grader output outside the repository.
7. Repeat only when variation, an unexpected result, or failure impact could change the design decision.

## Trigger execution protocol

Present each case as a Skill-selection task using only installed names and descriptions. Require the selector to open every selected `SKILL.md` so loading is observable. Count only an observed target file read; record an unavailable observation as `not exposed`.

## Failure Pattern Ledger

- `one-shot learning plan replaces active work`
- `unfamiliar domain blocks a clear request`
- `learning and deadline forced into a binary choice`
- `AI conclusion treated as evidence`
- `user-owned decision made by AI`
- `technical work unnecessarily returned to the user`
- `resolved understanding asked again`
- `quiz or self-study emitted without decision value`
- `tool selection routed to learning calibration`
- `originating workflow never resumes`

## Current revision

Evaluated on 2026-07-30 with Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The renamed candidate passed all five behavior cases and all 35 assigned requirements. The payment-retry case was rerun under the new name; the other four behavior grades reuse evidence from the accepted pre-rename revision because the executable workflow is unchanged.
- The previous-name and no-Skill conditions also passed all five cases and all 35 requirements. The previously recorded pairwise grader found the Skill materially better than no Skill for the payment-retry and cache-fix reconstruction cases and equivalent for the other three cases.
- All seven trigger, continuation, near-miss, and coexistence cases passed under both names. The new name therefore preserves observed routing rather than demonstrating a higher selection rate.
- After the adjacent execution-setup Skill was replaced, the exact `tool-and-model-selection` case loaded `choose-ai-execution-setup` without loading `calibrate-learning-support`. The other six trigger cases reuse accepted evidence because their inputs and relevant metadata are unchanged.
- `calibrate-learning-support` describes task-specific support and understanding recovery more directly than `calibrate-ai-learning`, without implying that the agent independently calibrates AI learning as a general system property.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, pairwise comparison, observable Skill loads, and unverified items.

### Next validation question

- In real multi-turn work, does the explicit calibration state continue to add value over ordinary model behavior often enough to justify the Skill's trigger and context cost?
