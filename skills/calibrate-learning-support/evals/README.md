# calibrate-learning-support evals

## Purpose

Verify that `calibrate-learning-support` adjusts AI learning support around an active task so the user can retain or recover decision-relevant understanding without blocking authorized progress, taking over user-owned decisions, or turning every task into a lesson.

## Assets

- `triggers.json`: trigger, continuation, near-miss, and coexistence selection cases
- `evals.json`: executable behavior cases with hidden assertions, including preservation of the originating review output
- `results.json`: historical evidence for the revision evaluated in July 2026
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
| Originating workflow output | Replaces required review findings with a learning plan or calibration status | `review-output-preserved` | Finding and learning-support assertions |
| Trigger and continuation | Misses explicit learning intent or a follow-up checkpoint | `triggers.json` | Observable Skill load |
| Adjacent routing | Absorbs tool selection, ordinary implementation, general teaching, or request clarification; treats unfamiliarity alone as learning intent | `triggers.json` | Observable Skill load |

## Behavioral execution protocol

1. Use `scripts/run_skill_evaluation.py plan` to select only the cases and conditions needed for the changed responsibility and inspect the model-call count before execution.
2. Run the plan in the Runner's disposable fixtures. Keep assertions and expected conclusions out of executor input.
3. For multi-turn cases, grade the relevant turn against the assigned assertions and the visible prior conversation.
4. A failed critical assertion fails the case. A partial result without a critical failure is partial.
5. Keep raw prompts, responses, JSONL, and grader output outside the repository.
6. Repeat or compare conditions only when variation, an unexpected result, or failure impact could change the decision.

## Trigger execution protocol

Use the Runner's targeted routing path with the declared coexistence Skills. Count only successful Skill reads in a complete event stream; record an unavailable observation as inconclusive.

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

## Historical evidence

Evaluated on 2026-07-30 with Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox.

- The renamed candidate passed all five behavior cases and all 35 assigned requirements. The payment-retry case was rerun under the new name; the other four behavior grades reuse evidence from the accepted pre-rename revision because the executable workflow is unchanged.
- The previous-name and no-Skill conditions also passed all five cases and all 35 requirements. The previously recorded pairwise grader found the Skill materially better than no Skill for the payment-retry and cache-fix reconstruction cases and equivalent for the other three cases.
- All seven trigger, continuation, near-miss, and coexistence cases passed under both names. The new name therefore preserves observed routing rather than demonstrating a higher selection rate.
- After the adjacent execution-setup Skill was replaced, the exact `tool-and-model-selection` case loaded `choose-ai-execution-setup` without loading `calibrate-learning-support`. The other six trigger cases reuse accepted evidence because their inputs and relevant metadata are unchanged.
- `calibrate-learning-support` describes task-specific support and understanding recovery more directly than `calibrate-ai-learning`, without implying that the agent independently calibrates AI learning as a general system property.
- Claude and other clients were not executed.

See [`results.json`](results.json) for candidate hashes, the case-by-requirement matrix, pairwise comparison, observable Skill loads, and unverified items.

## Issue #53 evidence

On 2026-10-04, the working-tree candidate based on `b88af0cdcd07138c8e7341a8423a34331b0a84b6` was checked with Codex CLI 0.155.1, `gpt-6-luna`, maximum reasoning effort, and a read-only evaluation sandbox. The Runner used its isolated `auto` credential store setting. Raw artifacts remain outside this repository.

- `review-output-preserved`: execution and runtime isolation passed. Manual inspection found the requested review finding, its changed location, impact, and evidence; no learning plan displaced the finding.
- `deadline-execute-and-explain`: execution and runtime isolation passed. The answer returned the requested UTC expression and one-sentence reason without a lecture or checkpoint.
- `unfamiliar-domain-no-learning-request`: routing observed `implement-changes` alone, as expected.
- `explicit-learning-priority`: the model read a personal same-name Skill during execution despite the Runner's successful catalog and sandbox preflights. Runtime isolation failed, so this run supplies no candidate routing verdict.
- The other migrated cases were not executed because their responsibilities did not change in this audit. Historical results above remain historical evidence, not a current rerun.

### Next validation question

- In real multi-turn work, does the explicit calibration state continue to add value over ordinary model behavior often enough to justify the Skill's trigger and context cost?
