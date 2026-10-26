---
name: calibrate-learning-support
description: Adjusts AI learning support around an active task, so that the user keeps or recovers task-specific understanding, decision ownership, and verification while the work continues. Use when the user prioritizes learning, says that they cannot explain or evaluate AI-produced work, asks to keep their understanding while they delegate, or continues after an understanding checkpoint.
license: MIT
---

# Calibrate Learning Support

Adjust AI support around an active task, so that the user can make their own decisions.\
The user must also be able to explain or verify the parts for which they are accountable.\
Treat the calibration as a repeated layer around the originating workflow, not as a study plan.\
The originating workflow keeps its implementation, investigation, design, or review.\
Keep the requested progress.\
Spend learning effort only where a misunderstanding could change a decision, a verification, or the result.

## Calibration cycle

1. **Identify the need**

   Collect these items:

   - the active task, the originating workflow, and the next decision or action
   - the learning goal, the time limit, the desired support, and the accountability that the user stated
   - what the user explained, chose, asked, or marked as unknown
   - the change, proposal, evidence, or AI output that the user must understand or evaluate
   - the authority, risk, and verification constraints that apply

   Identify what the user needs from the task now, and what the user must understand, explain, verify, or decide personally.\
   Base each conclusion about understanding on what the user said or did.\
   An answer to a checkpoint is evidence only for the point that it covers.

2. **Decide whether understanding matters here**

   Decide whether a misunderstanding could change the next action, the accepted risk, the verification, or later accountability.\
   Limit the explanation to what can change the current work.\
   Compare these factors on a scale, not as a choice between learning and the deadline:

   - the depth of understanding that the user asked for
   - the result and the reversibility of a wrong decision
   - whether the user must review, operate, maintain, approve, or explain the result
   - the available time, and whether the explanation can come before, during, or after the work
   - the strength of the available evidence

3. **Separate the decisions**

   - The user owns the objectives, priorities, scope, risk tolerance, authorization, and final adoption, when the user is accountable for them.
   - AI can gather evidence, generate options, draft changes, run authorized checks, and explain reasoning.
   - AI can analyze consequential technical decisions.\
     It returns the evidence, trade-offs, unknowns, and the point of adoption to the responsible user.

4. **Select the support**

   Select support that fits the goal and the constraints of the user.\
   The options include these methods:

   - Explain before you act.
   - Work through a decision together.
   - Do the authorized work, and explain its evidence afterward.
   - Reconstruct an existing AI output with the user.
   - Let the user do a key step, and review it.

   Use a short explanation with continued work when the request is clear, authorized, and reversible.\
   Use more collaboration or checkpoints when the user prioritizes learning, cannot evaluate an important output, or owns a consequential decision.\
   Give direct answers and authorized implementations, even in an unfamiliar domain.\
   Adjust the explanation to the goal of the user.\
   Let AI do the technical work that it can do safely and explain.

5. **Continue the work**

   Continue the work, or hand it to the originating workflow, with this calibration.\
   When the next authorized action can proceed, continue it instead of stopping for a learning plan.

6. **Use a checkpoint when it matters**

   Use an understanding checkpoint only when the answer could change the next action, or show a material gap.\
   Ask for a focused explanation, choice, prediction, or verification step, not for general recall.\
   A quiz result, the confidence of the user, or passing tests alone does not show understanding or correctness.

7. **Update after each answer**

   Add the answer of the user and the new evidence.\
   Keep the resolved points, reassess only the material gaps that remain, and adjust the support method when necessary.

8. **Repeat or return**

   Repeat while another exchange can improve a decision, a verification, or an accountable explanation.\
   Otherwise, return to the originating workflow, or finish the requested task.

Use evidence suitable for each claim, for example:

- official documentation or standards
- the source and history of the repository, and existing implementations
- direct observation, reproduction, logs, tests, and measurements
- the decision of an authorized domain owner

A conclusion of AI is an inference from evidence, not evidence.

Keep the high-risk controls that the originating workflow requires.\
Authorization, rollback, recovery, sandboxing, and deterministic verification stay in force, whatever the explanation says.

## State

Choose the state that describes the next action:

- `Ready`: the originating workflow can continue, and the decision ownership and the verification are clear.
- `Proceed with checkpoints`: the work can continue, with identified decision or understanding checkpoints.
- `Continue calibration`: one material gap in understanding still needs a focused explanation, question, or joint step before the affected action.
- `Blocked`: a required decision, authorization, or risk acceptance of the user is not available.

## Report

Deliver the result and the verification that the originating workflow requires, in its expected form.\
The calibration state and the learning support are additions to that result.\
Add only the information that changes the next action:

- the understanding or decision that the support protects
- the selected support method, and its reason
- the work that AI can continue, and the decisions that the user owns
- the next checkpoint, or the next action of the originating workflow
- the supporting evidence, the unverified claims, and the remaining unknowns

Offer practice or later self-study only when the user asks for it, or when it supports the stated learning goal.\
The choice of a chat, agent, model, tool-enabled surface, or agent topology belongs to a separate decision.
