---
name: assess-risky-change-readiness
description: Assesses and prepares the safety controls, recovery strategy, evidence, and authorization state needed before a consequential or hard-to-recover change crosses into execution. Use when material operational, data, security, external-state, irreversibility, or recovery risks require more than an ordinary implementation handoff, or when another workflow identifies missing high-risk controls; not for routine change design, already authorized implementation whose controls are complete, review of a completed diff, failure investigation, general security review, or executing the change.
license: MIT
---

# Assess Risky Change Readiness

## Objective

- Determine whether a consequential or hard-to-recover change has enough evidence, safety controls, recovery preparation, and authority to cross into execution.
- Make the exact action, target, environment, execution boundary, material risks, and responsible handoff decision-ready.
- Stop at a read-only readiness or authorization handoff; do not approve or execute the change.

## Evidence and inputs

Gather what is available:

- objective, selected approach, exact action, target, environment, revision, data scope, and execution boundary
- affected users, systems, data, external state, credentials, and dependent operations
- preconditions, backup or restore evidence, monitoring, validation, and operational ownership
- proposed prevention, mitigation, detection, abort, recovery, compensation, and containment controls
- applicable policy, existing authorization, required decision owner, risk tolerance, and accepted loss
- assumptions, unresolved decisions, unknowns, and evidence that cannot be obtained within the current authority

Classify each material input as `Confirmed`, `Reported`, `Inferred`, `Assumed`, or `Unknown`.
Do not convert reported controls, proposed commands, or intended backups into confirmed evidence.

## Risk assessment

Assess the properties that make additional controls necessary rather than treating a category label as sufficient:

- reversibility and the point after which reversal is no longer possible
- recoverability, including recovery time, cost, completeness, and evidence
- blast radius across users, systems, regions, tenants, records, or external parties
- mutation of production, shared, persistent, or externally controlled state
- data loss, corruption, confidentiality, integrity, security, privacy, or compliance impact
- detectability, monitoring delay, and the reliability of abort signals
- authority to act, separation of duties, responsible owner, and escalation path
- uncertainty in the target, plan, dependencies, controls, or expected outcome

Use ordinary change design when these properties do not require additional execution controls.

## Workflow

1. Establish the exact action, target, environment, revision or data scope, execution boundary, intended outcome, and non-goals.
2. Determine whether the risk properties require controls beyond an ordinary implementation handoff.
3. Separate confirmed evidence from reported claims, inferences, assumptions, and unknowns.
4. Map each material risk to the controls that prevent or reduce it, the evidence that detects it, the signal and threshold that abort it, and the person or workflow responsible.
5. Select a realistic recovery treatment for each material failure mode: rollback, roll-forward, restore, compensation, containment, partial or manual recovery, or explicit acceptance of irreversible loss.
6. Verify that preconditions, go/no-go criteria, monitoring, abort authority, point of no return, recovery ownership, and post-action verification are decision-ready.
7. Determine the authorization state for the exact scope and controls without granting authority or requesting redundant approval.
8. Assign exactly one completion state and produce the handoff.

If the target or execution boundary is not identifiable, classify the result as `Blocked` rather than inventing a plan.
Treat a command as a proposed, unexecuted action unless supplied evidence establishes that it was already run.

## Completion states

Choose exactly one state in this order:

1. `Not applicable`: The change does not need safety controls beyond the ordinary design or implementation handoff.
2. `Blocked`: The Skill applies, but a material target, evidence, control, recovery, ownership, risk-acceptance, or authority gap prevents a responsible authorization or execution handoff.
3. `Ready for authorization`: Material controls and evidence are decision-ready, but the responsible authority has not approved the exact action, scope, and residual risk.
4. `Ready for execution handoff`: Material controls are decision-ready and the exact action and scope are already authorized for the identified execution owner.

`Blocked` takes precedence over authorization status when a material readiness gap remains.
This Skill records authorization; it does not create it.

## Control and recovery rules

- Do not require rollback when reversal is impossible or less safe than another treatment.
- Do not describe recovery as available without evidence that its prerequisites, procedure, owner, and expected limits are credible.
- Use roll-forward, restore, compensation, containment, or explicit loss acceptance when they match the failure mode better than rollback.
- Mark the result `Blocked` when a material irreversible loss lacks an authorized acceptance decision or when required recovery evidence is unavailable.
- Do not ask for a generic confirmation when the exact scope and controls are already authorized.
- Require a new decision only when the action, target, scope, control set, residual risk, or applicable authority materially differs from what was authorized.

## Reporting contract

Adapt the structure to the change and include:

- completion state and the reason for it
- exact action, target, environment, revision or data scope, and execution boundary
- evidence state for material inputs and unknowns
- applicability basis and material risk properties
- risk-to-control mapping covering prevention or mitigation, detection, abort condition, recovery treatment, owner, and residual risk
- preconditions, go/no-go criteria, monitoring, point of no return, and post-action verification
- authorization state, responsible decision owner, and any accepted loss
- next handoff and the conditions that would invalidate it

Omit empty sections and fixed step counts.
When commands are useful, ground them in inspected evidence and label them as unexecuted.

## Boundaries

- Use `clarify-request` when the objective, target, environment, authority, or success criteria are too undefined to assess.
- Use `explore-decision-space` when materially different safety or rollout strategies remain unsettled; return here after an approach is selected.
- Use `design-changes` for ordinary implementation design and accept its handoff when additional high-risk controls are needed.
- Hand authorized implementation to `implement-changes` or the originating authorized operator; do not absorb their execution responsibility.
- Do not review a completed diff, investigate a failure, perform a general security assessment, modify files, run proposed operations, approve the change, or execute it.
- Keep the Skill self-contained when adjacent Skills are unavailable and do not introduce another agent or subagent by default.
