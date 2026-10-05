# choose-ai-execution-setup evals

## Purpose

Check that the Skill recommends an available execution setup for a concrete task, verifies decision-critical technical facts when it can, leaves unresolved user priorities to the user, and stops before starting the task or changing the client.

## Assets

- `evals.json`: executable behavior cases, including the original seven cases and three cases for the audited boundaries
- `triggers.json`: executable selection, near-miss, and coexistence cases
- `report.json`: compact results for the latest changed-responsibility candidate case
- `results.json`: historical evidence from the accepted 2026-07-30 revision; it is not evidence for the current candidate
- this README: responsibility coverage, execution choice, and evidence limits

The definitions use the repository's `{skill_name, evals}` contract. The old `current` condition now maps to `baseline`, which means the selected Git base revision; the old `no_skill` condition maps to `without-skill`. The historical `triage-agent-usage` comparison remains in `results.json` and is not implied by the new `baseline` condition. All original case prompts, expected behavior, assertion meanings and criticality, routing expectations, and routing coexistence Skills are preserved.

## Static checks

- Metadata names explicit setup advice and excludes implementation, setting changes, and learning calibration.
- Required capability and confirmed availability remain distinct.
- Model capability and reasoning effort remain separate.
- Recommendation states, prerequisites, unknowns, and the next actor make advice actionable.
- The Skill does not start the task, configure the client, grant permission, or automatically orchestrate agents.
- The English and Japanese instructions preserve the same conditions and boundaries.

## Coverage

| Responsibility or boundary | Plausible failure | Case or check |
| --- | --- | --- |
| Confirmed setup choice | Chooses unnecessary tools or an unavailable named setup | `confirmed-text-options` |
| Missing task or options | Invents an available setup | `missing-availability` |
| Independent dimensions | Substitutes reasoning for required access | `routine-high-impact` |
| Bounded parallelism | Counts an unconfirmed parent as a worker or ignores capacity | `parallel-independent-units` |
| Shared mutable state | Recommends conflicting parallel writes | `shared-write-conflict` |
| Task-design boundary | Invents implementation units | `undefined-work-units` |
| Learning boundary | Absorbs learning calibration | `learning-coexistence` |
| Technical fact finding | Asks the user for locally checkable tool and repository facts | `check-technical-availability` |
| Self-directed fact finding | Waits for an explicit check instruction instead of inspecting available workspace and Python access | `self-directed-technical-check` |
| User-owned trade-off | Silently ranks spending against privacy | `unresolved-user-tradeoff` |
| Selection boundary | Absorbs implementation, design, review, learning, or setting changes | `triggers.json` |

Behavior cases use their stated expected output and critical assertions. Routing cases use observed Skill loads and expected handlers.

## Execution and evidence

For a changed instruction, use the repository Runner's `targeted-candidate` path, select only cases that expose the changed responsibility, inspect the planned model-call count, then run the candidate once. Keep raw artifacts outside the repository. Add comparison or repetition only if the first result leaves a decision-relevant ambiguity. Unchanged selection metadata needs static review rather than another routing run.

The 2026-07-30 `results.json` records seven passing candidate behavior cases and eight passing trigger cases under Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, and a read-only sandbox. That evidence is historical; it does not establish the behavior of the current candidate or of other clients.

On 2026-10-04, Codex CLI 0.155.1 with `gpt-6-luna`, max reasoning, and a read-only sandbox completed `check-technical-availability` and `unresolved-user-tradeoff`; all six critical requirements passed. The separate `confirmed-text-options` regression run also passed: the response recommended the stated available Chat A and did not draft the announcement. That earlier report remains in Git history. The regression run remains in temporary artifacts and is summarized in Issue #54.

The follow-up review found that `check-technical-availability` explicitly requests checks, so its passing result does not establish self-directed fact finding. The new `self-directed-technical-check` candidate case omits that instruction. Under the same Codex CLI version, model, reasoning effort, and sandbox, the trace showed read-only workspace searches and Python availability checks initiated by the model. The response identified the absent project and read-only workspace and did not edit files or run project tests. All three critical requirements passed; `report.json` records this case and the exact candidate and evaluation-input hashes.

The migrated routing definition had omitted four coexistence Skills from the original definition. After restoring them at execution level, the Runner plan for `approved-implementation` listed all four, its catalog preflight passed, and the completed routing trace observed `implement-changes`, matching the expected handler. The routing run and its grades remain in temporary artifacts; Issue #54 records this follow-up result.

## Unverified boundaries

The remaining six original behavior cases and seven routing cases were not rerun on this revision. Real users may provide incomplete environment details, and client-specific tool visibility can vary. Repeat a case or test another client only when its behavior becomes relevant to an acceptance decision.
