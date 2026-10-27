# Choose the next Skill

This guide is for people who use several Skills on one piece of work.\
For each kind of work, it shows which Skill usually comes next.\
It also shows what the previous Skill must report before you move on.\
Choose the first Skill from the [task catalog](../../README.md#skills).

Most Skills end by reporting a state, such as `Ready for design`.\
Use that state to choose the next step.

The connections here are suggestions.\
You do not have to run every step, and a connection does not allow any action.\
Each Skill states its own inputs, outputs, and boundaries.

## Make a change

A change usually goes through four Skills:

1. **`clarify-request`**
   - Use it when the purpose, scope, or success criteria of the request are unclear.\
     Skip it when they are already clear.
   - Come back to it when another Skill, such as `define-referents`, `draft-issue`, or `record-session-handoff`, reports that the request itself is unclear.
2. **`design-changes`**
   - Use it to decide the approach, the affected scope, and how to verify the change.\
     Skip it when these are already clear and the change is allowed.
3. **`implement-changes`**
4. **`review-changes`**
   - Continue as described in [Review and fix changes](#review-and-fix-changes).

Two Skills fill specific gaps before or during these steps:

- When a term is ambiguous, use `define-referents`, then return to the step you were on with the agreed meaning.
- When a consequential choice has materially different options, use `explore-decision-space`.\
  When it reports `Selected for design`, continue with `design-changes`.

## Investigate a failure

1. **`investigate-failure`**
   - When it reports `Ready for implementation`, continue with `implement-changes`.
   - When it reports `Ready for design`, continue with `design-changes`.
   - When it reports `Diagnostic next` or `Blocked`, provide the missing input, or run the check that it names.\
     Then continue the investigation.
2. **`implement-changes`**, after design if needed
3. **`validate-fix`**
   - It checks the fix against the original failure.

When the investigation needs current public documentation, advisories, or vendor behavior as evidence, `research-web-safely` can gather it.\
The diagnosis stays with `investigate-failure`.

## Review and fix changes

A review usually goes through these Skills.\
Each Skill passes specific information to the next one and does not make the decisions that belong to the others.

1. **`review-changes`**
   - It reports findings with a label, impact, and confidence.\
     These do not decide whether to act on a finding.
2. **`triage-review-feedback`**
   - It decides a response for each finding: `Act now`, `Defer`, or `No action`.
   - Implement only the `Act now` work you allow.\
     Accepting a concern does not mean adopting the reviewer's proposed solution.
   - When it needs current public documentation to check a finding, `research-web-safely` can gather it.
3. **`draft-review-comments`**, only when you need comments
   - Pass it the assessment, state, and response decision of each finding.\
     It drafts comments without making these decisions.
   - For a review without findings, skip triage.\
     Pass the conclusion, the reviewed scope, the checks performed, and their limitations directly from `review-changes`.
   - A draft does not allow posting it or choosing a GitHub review action.
4. **`implement-changes`**
5. **`validate-fix`**
   - When a fix is not complete, return to `implement-changes`.
   - When it records a problem caused by the fix outside its target, review that problem with `review-changes`.
   - Use `review-changes` for the whole diff again only when you want a full re-review.

Pass the evidence and uncertainties along at each step.\
Missing context is not evidence of low risk.

## Describe changes

Two Skills describe changes without looking for problems:

- `summarize-changes` writes a change summary, such as a PR description or release note.
- `draft-commit` plans commit units and drafts their messages.

## Pause risky or stalled work

Pause the current work and use one of these Skills in the following situations:

1. **An action has material recovery, operational, security, or external-state risk: `assess-risky-change-readiness`**
   - Decide whether to use it from the actual consequences, not from a label such as “migration” or “production.”
   - Use it also when `design-changes` or `implement-changes` finds that additional high-risk controls are needed.
   - `Ready for authorization` means that the controls are ready but the person responsible has not yet approved the action.\
     `Ready for execution handoff` means that the action is already allowed; the Skill itself does not execute it.
2. **Equivalent attempts keep failing without new evidence: `break-failure-loop`**
   - When it reports `Diagnostic next`, run the check it names, then return to the work.
   - When it reports `Diversify`, continue with `explore-decision-space`.
   - When it reports `Blocked`, keep the work paused until the missing input or decision is available.
3. **A consequential choice has converged on one approach too early: `explore-decision-space`**
   - When it reports `Selected for design`, continue with `design-changes`.
   - Skip it for work that is easy to reverse, or for a choice that an adequate comparison already supports.

## Choose an execution setup and keep your understanding

Use `choose-ai-execution-setup` to choose the chat, agent, model, tool-enabled surface, or agent topology for a task.\
When you also want to keep your understanding of the work, continue with `calibrate-learning-support` within the chosen setup.

## Change agent instructions or Skills

These Skills apply to instructions that agents keep using, such as `AGENTS.md` files and Skills.

1. **`audit-agent-guidance`**
   - Use it when the cause of unexpected agent behavior is unclear.\
     Skip it when the cause is already supported by evidence.
2. **`design-skill` or `design-agent-instructions`**
   - Use `design-skill` for a Skill's responsibility and boundaries.
   - Use `design-agent-instructions` for the roles of instruction documents and how clients load them.
3. **`implement-changes`**
   - Both design Skills end with a handoff for implementation.\
     A design alone does not show that the unexpected behavior has been fixed.
