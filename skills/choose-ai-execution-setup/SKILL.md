---
name: choose-ai-execution-setup
description: Advises which available AI execution setup should handle a concrete task before work starts by deriving required access, tools, model capability and reasoning, context, permissions, verification, and agent topology. Use when the user explicitly asks which chat, coding agent, model, tool-enabled surface, or delegation setup to use; not for automatically orchestrating or executing an active task, designing implementation units, changing client settings, or calibrating learning support.
license: MIT
---

# Choose AI Execution Setup

## Objective

- Recommend an available AI execution setup for a concrete task without collapsing access, model capability, reasoning effort, context, permissions, verification, topology, cost, and latency into one scale.
- Make the recommendation actionable by identifying prerequisites, unconfirmed availability, and the actor responsible for the next step.
- Keep execution-setup advice separate from task design, task execution, client configuration, authorization, and learning calibration.

## Evidence

Gather what is available:

- the concrete task, intended outcome, and already-defined work units
- evidence and systems the setup must read, tools or environments it must access, and actions it must perform
- available chats, coding agents, models, reasoning settings, tools, permissions, and execution environments
- uncertainty, judgment, context volume, verification needs, reversibility, and consequence of error
- user-provided cost, latency, token, or privacy constraints

Distinguish confirmed availability from a required capability. Do not invent a named product, model, profile, tool, permission, or topology when the available choices are unknown.

## Decision workflow

1. Confirm that the request asks for execution-setup advice for a concrete task. If the task or relevant choices are too unclear to compare, state the missing evidence instead of guessing.
2. Derive the required access and tool capabilities from the evidence to read, actions to perform, and checks to run.
3. Select the model capability from ambiguity, judgment, consequence, and verification complexity. Do not use task importance or tool access as a proxy for model capability. If the available setups do not expose model capability separately, mark it as unconfirmed or non-differentiating.
4. Select reasoning effort separately from the model and execution surface. Do not use a reasoning setting as evidence of model capability. Increase reasoning only when deeper inference or verification is decision-relevant. If available reasoning settings are not confirmed, report the dimension as unconfirmed or non-differentiating instead of prescribing a default.
5. Determine the context that must be available and what can remain outside the active context.
6. Identify the permissions and side effects the setup would require. Treat them as prerequisites, not as authorization.
7. Choose the verification and review capability needed to establish the outcome.
8. Choose one session, sequential handoffs, independent review, or parallel agents only when work units are already defined. If implementation units still need to be designed, return that need to the owning design workflow.
9. Use parallel agents only when units are independent, do not contend for mutable state or files, have explicit ownership and completion checks, can be integrated by a parent, and save more than their coordination cost. Do not count an integrating parent as a worker or assign it a work unit unless its capability and availability for that unit are confirmed.
10. Apply user-stated cost, latency, token, and privacy constraints across the eligible choices. Do not call one setup lighter or heavier without naming the dimension.
11. Map the requirements to confirmed available choices. Before using `Recommendation ready`, verify that every required access, tool, environment, permission, and verification capability is confirmed for that choice. Otherwise use the applicable conditional, setup-change, or insufficient-evidence state.
12. State the recommendation, material alternatives, prerequisites, unknowns, and next actor.

## Completion states

Assign exactly one state:

- `Recommendation ready`: a confirmed available setup satisfies the task requirements and the responsible actor can start it.
- `Conditional recommendation`: the preferred setup is identifiable, but one stated low-scope availability or task condition must be confirmed before starting.
- `Setup change required`: no currently confirmed setup satisfies a required capability, permission, environment, or verification need.
- `Insufficient evidence`: the task, available choices, or another decision-critical input is too unclear to compare without inventing it.

## Reporting contract

Adapt the response to the decision. Include:

- the completion state
- the recommended available setup or the capability-level recommendation
- separate entries for access and tools, model capability, reasoning effort, context, permissions and side effects, verification and review, and topology; mark a dimension as unconfirmed or non-differentiating when it does not constrain the choice
- material cost, latency, token, or privacy constraints supplied by the user
- prerequisites, unconfirmed assumptions, and the actor responsible for the next step
- a task-design, configuration, or authorization handoff only when that boundary blocks the setup decision

For `Recommendation ready`, state that no gating prerequisite or decision-critical unknown remains. When topology is material, state whether its latency or specialization benefit exceeds its coordination and integration cost, or what evidence prevents that comparison.

Report `Model capability` and `Reasoning effort` separately. Never infer model capability from a statement about reasoning effort or infer reasoning effort from a model name. Before finalizing, verify that every model-capability claim is directly supported by the task; otherwise replace it with `unconfirmed` or `non-differentiating`.

When the user explicitly requests task-specific understanding or learning support, add an optional `calibrate-learning-support` handoff after the setup recommendation without designing its method.

Do not force a named model, profile, multiple agents, or a detailed comparison beyond recording whether each independent dimension constrains the decision.

## Boundaries

- Do not perform or orchestrate the task, create implementation work units, change client settings, switch models, grant permissions, or treat a recommendation as authorization.
- Do not choose the user's objective, scope, risk tolerance, substantive implementation design, or final adoption decision.
- Keep task-specific learning and understanding calibration with `calibrate-learning-support`; remain self-contained when that Skill is unavailable.
- Keep automatic agent and tool orchestration in the active agent's durable instructions, client configuration, and agent definitions rather than this distributed Skill.
