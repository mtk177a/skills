---
name: choose-ai-execution-setup
description: Advises which available AI execution setup should handle a concrete task before work starts, from the access, tools, model capability, reasoning effort, context, permissions, verification, and agent topology that the task needs. Use when the user asks which chat, coding agent, model, tool-enabled surface, or delegation setup to use for a task.
license: MIT
---

# Choose AI Execution Setup

Recommend an available AI execution setup for a concrete task.\
Evaluate each dimension separately: access, model capability, reasoning effort, context, permissions, verification, topology, cost, and latency.\
Make the recommendation actionable, with its prerequisites, the availability that is not confirmed, and the person who acts next.\
The output is advice.\
The user starts the setup, changes settings, grants permissions, and decides on adoption.

## Workflow

1. **Confirm the task**

   Confirm that the user asks for setup advice for a concrete task.\
   Collect these items:

   - the task, the intended outcome, and any work units that are already defined
   - the evidence and systems that the setup must read, the tools and environments that it must access, and the actions that it must perform
   - the available chats, coding agents, models, reasoning settings, tools, permissions, and execution environments
   - the uncertainty, judgment, context volume, verification needs, reversibility, and the result of an error
   - the cost, latency, token, and privacy constraints, and the priorities that the user stated

   If the task or the choices are too unclear to compare, stop with the state `Insufficient evidence`.\
   Name the missing evidence.

2. **Check the availability**

   Separate a confirmed available choice from a required capability.\
   Verify critical technical facts with available read-only checks and authoritative documentation, before you ask the user for them.\
   Treat reported availability as reported until a check confirms it, and state what you cannot verify.\
   Name a specific product, model, profile, tool, permission, or topology only when it is confirmed as available.

3. **Derive the access and tools**

   Derive the necessary access and tools from the evidence to read, the actions to perform, and the checks to run.

4. **Select the model capability**

   Select the model capability from the ambiguity, the judgment, the result of an error, and the complexity of verification.\
   Base it on these properties of the task, not on the importance of the task or the tool access.\
   If the available setups do not show model capability separately, mark it as `unconfirmed` or `non-differentiating`.

5. **Select the reasoning effort**

   Select the reasoning effort separately from the model and the execution surface.\
   Increase it only when deeper inference or verification changes the decision.\
   If the available reasoning settings are not confirmed, mark the dimension as `unconfirmed` or `non-differentiating`.

6. **Determine the context, permissions, and verification**

   Determine the context that must be available, and what can stay outside the active context.\
   Identify the permissions and side effects that the setup needs, and treat them as prerequisites.\
   Choose the verification and review capability that can establish the outcome.

7. **Choose the topology**

   Choose one session, sequential handoffs, independent review, or parallel agents.\
   Choose a topology with several agents only when the work units are already defined.\
   If the units still need a design, return that need to the design workflow.\
   Use parallel agents only when all of these conditions are true:

   - The units are independent.
   - The units share no files or other state that changes.
   - Each unit has an owner and a completion check.
   - A parent agent can integrate the results.
   - The time saved is larger than the cost of coordination.

   Count an integrating parent as a worker only when its capability and availability for a unit are confirmed.

8. **Apply the constraints**

   Apply the cost, latency, token, and privacy constraints of the user to the eligible choices.\
   Name the dimension each time you call a setup lighter or heavier.\
   Eligible choices can differ on a trade-off that the user did not decide.\
   Then explain the results, and let the user choose.

9. **Map the requirements to the choices**

   Map each requirement to the confirmed available choices.\
   Done when each requirement has a confirmed choice, or is marked as unconfirmed or missing.

10. **Choose the state**

    - `Recommendation ready`: a confirmed available setup meets every requirement, and the responsible person can start it.\
      Use this state only when each access, tool, environment, permission, and verification capability is confirmed for that setup.
    - `Conditional recommendation`: the preferred setup is clear, but one stated, small condition of availability or of the task must be confirmed first.
    - `Setup change required`: no confirmed setup meets a required capability, permission, environment, or verification need.
    - `Insufficient evidence`: the task, the choices, or another critical input is too unclear to compare.

## Report

Include these items:

- the state
- the recommended setup, or the recommended capabilities
- a separate entry for each dimension: access and tools, model capability, reasoning effort, context, permissions and side effects, verification and review, and topology.\
  Mark a dimension that does not constrain the choice as `unconfirmed` or `non-differentiating`.
- the cost, latency, token, or privacy constraints that the user supplied
- the technical facts that you checked, the trade-offs left to the user, and the facts that are not verified
- the prerequisites, the unconfirmed assumptions, and the person who acts next
- a handoff for task design, configuration, or authorization, only when that boundary blocks the decision

For `Recommendation ready`, state that no blocking prerequisite or critical unknown remains.\
When the topology matters, compare its gain in time or specialization with its cost of coordination and integration.\
If evidence for that comparison is missing, state what is missing.

Report `Model capability` and `Reasoning effort` as separate entries, each based on its own evidence.\
Base each claim about model capability directly on the task, or replace it with `unconfirmed` or `non-differentiating`.

When the user asks for help to understand or learn the task, add a note after the recommendation.\
The note says that learning support is a separate, optional follow-up.

Keep the advice to what the decision needs.\
Name a model or a profile, recommend several agents, or give a detailed comparison only when a dimension needs it.\
Automatic orchestration of agents and tools belongs in the durable instructions, client configuration, and agent definitions of the active agent.
