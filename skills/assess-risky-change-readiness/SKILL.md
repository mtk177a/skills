---
name: assess-risky-change-readiness
description: Assesses whether a consequential or hard-to-recover change has the safety controls, recovery plan, evidence, and authorization that it needs before execution, and prepares what is missing. Use when operational, data, security, external-state, irreversibility, or recovery risks need more than an ordinary implementation plan.
license: MIT
---

# Assess Risky Change Readiness

Decide whether a risky change is ready to execute.\
Make the action, the target, the risks, the controls, and the decision owner clear enough for a decision.\
The output is a readiness assessment.\
The decision owner approves the change, and the execution owner runs it.

## Workflow

1. **Identify the change**

   State the exact action, target, environment, revision or data scope, execution boundary, intended result, and exclusions.\
   Done when each item is known.\
   If the target or the execution boundary is not known, stop with the state `Blocked`.\
   If the objective, authority, or success criteria are not clear, report what the user must clarify.

2. **Collect the evidence**

   Collect these items:

   - the affected users, systems, data, external state, credentials, and dependent operations
   - the preconditions, backup or restore evidence, monitoring, validation, and operational owners
   - the proposed controls to prevent, reduce, detect, abort, recover, compensate, and contain
   - the applicable policy, the existing authorization, the decision owner, the risk tolerance, and any accepted loss

   Mark each material input as `Confirmed`, `Reported`, `Inferred`, `Assumed`, or `Unknown`.\
   Mark a control, command, or backup as `Confirmed` only when evidence shows that it exists or ran.\
   Treat a command as proposed and not run, unless evidence shows that it already ran.

3. **Decide whether extra controls are necessary**

   Assess the properties of the change, not only its category:

   - reversibility, and the point after which reversal is not possible
   - recoverability: the time, cost, completeness, and evidence of recovery
   - the blast radius across users, systems, regions, tenants, records, or external parties
   - changes to production, shared, persistent, or externally controlled state
   - the impact on data, confidentiality, integrity, security, privacy, or compliance
   - detectability, the delay of monitoring, and the reliability of abort signals
   - the authority to act, the separation of duties, the owner, and the escalation path
   - the uncertainty in the target, plan, dependencies, controls, or expected result

   If ordinary change design is sufficient, finish with the state `Not applicable`.\
   If the approach or the safety strategy is not selected yet, report that it must be selected first.

4. **Map the risks to controls**

   For each material risk, record these items:

   - the controls that prevent or reduce it
   - the evidence that detects it
   - the signal and threshold to abort
   - the person or workflow that owns the response

   Done when each material risk has all four items, or the missing item is a readiness gap.

5. **Select the recovery treatment**

   For each material failure mode, select a realistic treatment:

   - rollback, roll-forward, restore, compensation, or containment
   - partial or manual recovery
   - explicit acceptance of a loss that cannot be recovered

   Select rollback only when reversal is possible and safer than the other treatments.\
   Describe a recovery as available only when evidence shows credible preconditions, procedure, owner, and limits.\
   For a loss that cannot be recovered, identify who can accept it.\
   Also state the exact loss and the scope of that decision.

6. **Check the execution conditions**

   Check that these items are ready for a decision:

   - the preconditions and the go/no-go criteria
   - the monitoring and the authority to abort
   - the point of no return
   - the recovery owner
   - the verification after the action

7. **Determine the authorization state**

   Record whether the decision owner authorized the exact action, scope, controls, and remaining risk.\
   If the exact scope and controls are already authorized, use that authorization.\
   Ask for a new decision only when the action, target, scope, controls, risk, or authority changed materially.

8. **Choose the state**

   Choose the first state that applies:

   1. `Not applicable`: the change needs no controls beyond the ordinary design or implementation handoff.
   2. `Blocked`: a material gap in the target, evidence, controls, recovery, ownership, or decision authority prevents a responsible handoff.\
      A pending approval from a known decision owner is not a gap.
   3. `Ready for authorization`: the controls and evidence are ready, and the decision owner is known.\
      The owner has not yet approved the exact action, scope, and remaining risk, including any loss that cannot be recovered.
   4. `Ready for execution handoff`: the controls are ready, and the exact action and scope are authorized for the execution owner.

   `Ready for authorization` records that a decision is pending.\
   The decision owner accepts the loss and gives the permission to execute.

## Report

Include these items:

- the state and its reason
- the exact action, target, environment, revision or data scope, and execution boundary
- the evidence state of the material inputs and the unknowns
- why this assessment applies, and the material risk properties
- for each risk, the prevention or reduction, the detection, the abort condition, the recovery treatment, the owner, and the remaining risk
- the preconditions, the go/no-go criteria, the monitoring, the point of no return, and the verification after the action
- the authorization state, the decision owner, and any accepted loss
- the next handoff, and the conditions that make it invalid

Ground each useful command in inspected evidence, and label it as not run.
