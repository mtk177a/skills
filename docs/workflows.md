# Choose a Skill workflow

Start with the task you need to complete.\
These connections help select the next Skill; they are not an instruction to run every step or permission to perform its actions.

## Choose the starting point

| Task | Start with | Next step |
| --- | --- | --- |
| Clarify an ambiguous request | `clarify-request` | Design or implementation once the objective, scope, and authority are clear |
| Define ambiguous terms | `define-referents` | Return to the task with agreed meanings |
| Compare consequential alternatives | `explore-decision-space` | `design-changes` after selecting an approach |
| Plan an understood change | `design-changes` | `implement-changes` once the approach and authority are clear |
| Implement an agreed change | `implement-changes` | `review-changes` for a new diff; `validate-fix` for identified corrections |
| Diagnose unexpected behavior | `investigate-failure` | Design a correction or use the direct handoff below |
| Review a new diff or the entire updated diff | `review-changes` | Triage findings; draft a requested summary when there are no findings |
| Assess existing review feedback | `triage-review-feedback` | Implement authorized work or draft comments from the supplied decisions |
| Recheck identified fixes | `validate-fix` | Resolve remaining or fix-induced work |
| Diagnose problems with durable agent guidance | `audit-agent-guidance` | `design-skill` or `design-agent-instructions` |

Use the [Skill catalog](../README.md#skills) for other tasks and each Skill's instructions for its inputs, outputs, and boundaries.

## Change and failure handling

A typical change follows `clarify-request` → `design-changes` → `implement-changes` → `review-changes`.\
Skip clarification or design when their decisions are already sufficiently clear and authorized.

After `investigate-failure`, go directly to implementation only when the supported diagnosis, authorized objective, affected scope, expected outcome, safety controls, and verification are defined.\
Otherwise, use `design-changes`.\
Use `validate-fix` to check the correction against the original failure.

Investigation can support an incident but does not take over incident command or an approved stabilization procedure.

## Review and corrections

`review-changes` → `triage-review-feedback` → optional `draft-review-comments` → `implement-changes` → `validate-fix`

| Handoff | Required distinction |
| --- | --- |
| Review → triage | A finding's label, impact, and confidence do not decide whether to act. |
| Triage → implementation | Implement only authorized `Act now` work. Acceptance of a concern does not require the reviewer's proposed solution. |
| Triage → comment draft | Supply assessment, state, and response decision. A caller may supply these directly; drafting does not make the decisions. |
| Finding-free review → comment draft | Supply the conclusion, scope, performed checks, and limitations; no finding-specific triage is needed. |
| Correction → recheck | Use `validate-fix` for identified fixes. Use `review-changes` only for an explicitly requested full re-review. |

Comment drafts do not authorize posting or selecting a GitHub review action.\
Preserve the evidence and uncertainties across handoffs; missing context is not evidence of low risk.\
For a full re-review, distinguish fix-induced, newly observable, and late-discovered findings, and follow the Skill's rules for starting another correction round.

## Risk and stalled work

| Situation | Skill | Return condition |
| --- | --- | --- |
| Consequential action with material recovery, operational, security, or external-state risk | `assess-risky-change-readiness` | Exact action, controls, residual risk, and execution authority are ready. |
| Equivalent attempts repeat under an unchanged hypothesis without useful new evidence | `break-failure-loop` | A discriminating check changes the evidence or hypothesis; otherwise keep the branch paused. |
| The current design is exhausted and local checks cannot resolve the choice | `explore-decision-space` | Select a materially different approach, then design the change. |

Use readiness assessment based on the actual consequences, not merely a label such as “migration” or “production.”\
`Ready for authorization` is not authorization; `Ready for execution handoff` records existing authority and does not execute the action.\
Recovery may require restoration, compensation, containment, or accepted loss rather than rollback.

A stalled workflow may return directly to diagnosis or remain blocked.\
Do not require decision exploration for readily reversible work or when adequate alternatives already support the choice.

## Durable agent guidance

When the cause is uncertain, use `audit-agent-guidance` before designing a change.\
Use `design-skill` for a Skill's responsibility and boundaries, or `design-agent-instructions` for document roles and client loading relationships.\
Then use `design-changes` to define implementation and verification.

Skip the audit when the diagnosis is already supported.\
A design alone does not establish that unobserved behavior has been fixed.
