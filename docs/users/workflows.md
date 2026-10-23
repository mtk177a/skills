# Choose the next Skill

This guide is for people who use several Skills on one piece of work.\
It shows which Skill usually comes next and the condition for moving on.\
Choose the first Skill from the [task catalog](../../README.md#skills).

The connections here are suggestions.\
They do not require you to run every step, and they do not authorize any action.\
Each Skill states its own inputs, outputs, and boundaries.

## Changes and failures

A typical change goes through four Skills:

`clarify-request` → `design-changes` → `implement-changes` → `review-changes`

Skip clarification or design when its decisions are already clear enough and authorized.

Before or during this flow, two Skills help with specific gaps:

- When a term is ambiguous, use `define-referents`, then return to the work with the agreed meaning.
- When a consequential choice has materially different options, use `explore-decision-space`, then use `design-changes` after choosing an approach.

When the overall request is unclear, use `clarify-request`.\
Skills such as `define-referents`, `draft-issue`, and `record-session-handoff` report that need instead of clarifying the whole request themselves.

For a failure, start with `investigate-failure`.\
Move directly to implementation only when the diagnosis is supported and the authorized objective, affected scope, expected outcome, safety controls, and verification are all defined.\
Otherwise, use `design-changes` next.\
After the correction, use `validate-fix` to check it against the original failure.

When `investigate-failure` or `triage-review-feedback` needs current public documentation, advisories, or vendor behavior as evidence, `research-web-safely` can gather it.\
The originating Skill still makes the diagnosis or decision.

An investigation can support incident response, but it does not take over incident command or an approved stabilization procedure.

## Reviews and fixes

A review usually goes through these Skills, with comment drafting only when needed:

`review-changes` → `triage-review-feedback` → `draft-review-comments` (optional) → `implement-changes` → `validate-fix`

Each handoff passes specific information, and the receiving Skill does not make decisions that belong to the earlier one:

- **Review → triage**: a finding's label, impact, and confidence do not decide whether to act on it.
- **Triage → implementation**: implement only authorized `Act now` work.\
  Accepting a concern does not require adopting the reviewer's proposed solution.
- **Triage → comment draft**: pass the assessment, state, and response decision.\
  A caller may supply them directly, but the drafting step does not make these decisions.
- **Review without findings → comment draft**: pass the conclusion, the reviewed scope, the checks performed, and their limitations.\
  No finding-by-finding triage is needed.
- **Fix → recheck**: use `validate-fix` for identified fixes.\
  Use `review-changes` again only when a full re-review is explicitly requested.

`validate-fix` hands a problem caused by the fix but outside its target to `review-changes`.\
In a full re-review, distinguish problems caused by the fix, problems that became visible only after it, and problems that were visible before, and follow the Skill's rules for starting another round of fixes.

Throughout these handoffs, keep the evidence and uncertainties.\
Missing context is not evidence of low risk.\
A comment draft does not authorize posting it or choosing a GitHub review action.

Two other Skills describe changes without looking for problems: use `summarize-changes` for a change summary and `draft-commit` for commit units and messages.

## Risky or stalled work

Pause the current work and use one of these Skills in the following situations:

| Situation | Skill | Condition for returning to the work |
| --- | --- | --- |
| An action has material recovery, operational, security, or external-state risk | `assess-risky-change-readiness` | The exact action, controls, remaining risk, and execution authority are ready. |
| Equivalent attempts repeat under an unchanged hypothesis without useful new evidence | `break-failure-loop` | A check that distinguishes the hypotheses changes the evidence or the hypothesis. |
| The current design cannot proceed and local checks cannot settle the choice | `explore-decision-space` | A materially different approach is selected and the change is designed. |

When `design-changes` or `implement-changes` finds that additional high-risk controls are needed, use `assess-risky-change-readiness` before execution.\
Decide whether to use it from the actual consequences, not from a label such as “migration” or “production.”\
`Ready for authorization` does not mean authorized, and `Ready for execution handoff` records existing authority without executing the action.\
Recovery may require restoration, compensation, containment, or accepting a loss rather than a rollback.

Until a distinguishing check changes the evidence or hypothesis, keep the stalled branch paused.\
After `break-failure-loop`, the work may return directly to diagnosis or remain blocked.\
Do not require option exploration for work that is easy to reverse or for a choice already supported by an adequate comparison.

## Execution setup and learning support

Use `choose-ai-execution-setup` to choose the chat, agent, model, tool-enabled surface, or agent topology for a task.\
When you also want to keep your understanding of the work, continue with `calibrate-learning-support` within the chosen setup.

## Agent instructions and Skills

These Skills apply to instructions that agents keep using, such as `AGENTS.md` files and Skills.

When the cause of unexpected agent behavior is unclear, use `audit-agent-guidance` before designing a change.\
Skip the audit when the cause is already supported by evidence.\
Then design the fix with one of these Skills:

- `design-skill` for a Skill's responsibility and boundaries
- `design-agent-instructions` for the roles of instruction documents and how clients load them

Finally, use `design-changes` to define the implementation and verification.\
A design alone does not show that the unexpected behavior has been fixed.
