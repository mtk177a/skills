# Choose a Skill workflow

Start with the task you need to complete.\
These connections help select the next Skill; they are not an instruction to run every step or permission to perform its actions.

Choose the first Skill from the [task catalog](../../README.md#skills).\
Use this guide for the conditions that govern the next handoff.

- [Changes and failures](#change-and-failure-handling): when to move from design to implementation.
- [Reviews and corrections](#review-and-corrections): triage, comment drafting, and rechecks.
- [Risk and stalled work](#risk-and-stalled-work): when to pause and resume.
- [Execution setup](#execution-setup-and-learning-support): choosing a setup and learning support.
- [Agent guidance](#durable-agent-guidance): when to audit or design instructions.

Follow each Skill for its inputs, outputs, and boundaries.

## Change and failure handling

Use `define-referents` for ambiguous terms, then return to the task with agreed meanings.\
Use `explore-decision-space` for consequential alternatives, then `design-changes` after choosing an approach.

A typical change follows `clarify-request` → `design-changes` → `implement-changes` → `review-changes`.\
Skip clarification or design when their decisions are already sufficiently clear and authorized.

After `investigate-failure`, go directly to implementation only when the supported diagnosis, authorized objective, affected scope, expected outcome, safety controls, and verification are defined.\
Otherwise, use `design-changes`.\
Use `validate-fix` to check the correction against the original failure.

Investigation can support an incident but does not take over incident command or an approved stabilization procedure.

When the overall request is unclear, use `clarify-request`; Skills such as `define-referents`, `draft-issue`, and `record-session-handoff` report that need instead of clarifying the whole request themselves.\
When `investigate-failure` or `triage-review-feedback` needs current public documentation, advisories, or vendor behavior as evidence, `research-web-safely` can gather it; the originating Skill keeps the diagnosis or decision.

## Review and corrections

`review-changes` → `triage-review-feedback` → optional `draft-review-comments` → `implement-changes` → `validate-fix`

| Handoff | Required distinction |
| --- | --- |
| Review → triage | A finding's label, impact, and confidence do not decide whether to act. |
| Triage → implementation | Implement only authorized `Act now` work. Acceptance of a concern does not require the reviewer's proposed solution. |
| Triage → comment draft | Supply assessment, state, and response decision. A caller may supply these directly; drafting does not make the decisions. |
| Finding-free review → comment draft | Supply the conclusion, scope, performed checks, and limitations; no finding-specific triage is needed. |
| Correction → recheck | Use `validate-fix` for identified fixes. Use `review-changes` only for an explicitly requested full re-review. |

`validate-fix` hands a fix-induced problem outside its target to `review-changes`.\
Use `summarize-changes` for a descriptive change summary and `draft-commit` for commit units and messages; neither discovers problems.

Comment drafts do not authorize posting or selecting a GitHub review action.\
Preserve the evidence and uncertainties across handoffs; missing context is not evidence of low risk.\
For a full re-review, distinguish fix-induced, newly observable, and late-discovered findings, and follow the Skill's rules for starting another correction round.

## Risk and stalled work

| Situation | Skill | Return condition |
| --- | --- | --- |
| Consequential action with material recovery, operational, security, or external-state risk | `assess-risky-change-readiness` | Exact action, controls, residual risk, and execution authority are ready. |
| Equivalent attempts repeat under an unchanged hypothesis without useful new evidence | `break-failure-loop` | A discriminating check changes the evidence or hypothesis; otherwise keep the branch paused. |
| The current design is exhausted and local checks cannot resolve the choice | `explore-decision-space` | Select a materially different approach, then design the change. |

When `design-changes` or `implement-changes` finds that additional high-risk controls are needed, use `assess-risky-change-readiness` before execution.\
Use readiness assessment based on the actual consequences, not merely a label such as “migration” or “production.”\
`Ready for authorization` is not authorization; `Ready for execution handoff` records existing authority and does not execute the action.\
Recovery may require restoration, compensation, containment, or accepted loss rather than rollback.

A stalled workflow may return directly to diagnosis or remain blocked.\
Do not require decision exploration for readily reversible work or when adequate alternatives already support the choice.

## Execution setup and learning support

Use `choose-ai-execution-setup` to choose the chat, agent, model, tool-enabled surface, or agent topology for a task.\
When the user also wants to keep understanding of the work, continue with `calibrate-learning-support` within the selected setup.

## Durable agent guidance

When the cause is uncertain, use `audit-agent-guidance` before designing a change.\
Use `design-skill` for a Skill's responsibility and boundaries, or `design-agent-instructions` for document roles and client loading relationships.\
Then use `design-changes` to define implementation and verification.

Skip the audit when the diagnosis is already supported.\
A design alone does not establish that unobserved behavior has been fixed.
