---
name: calibrate-learning-support
description: Adjusts AI learning support around an active task so a user can retain or recover task-specific understanding, decision ownership, and verification while work continues. Use when the user explicitly prioritizes learning, says they cannot explain or evaluate AI-produced work, asks to preserve understanding while delegating, or continues after an understanding checkpoint; not for ordinary tool or model selection, general teaching unrelated to an active task, or blocking a clear request merely because the domain is unfamiliar.
license: MIT
---

# Calibrate Learning Support

## Objective

- Adjust AI support around an active task so the user can make the decisions they own and explain or verify the parts for which they remain accountable.
- Treat calibration as an iterative layer around the originating workflow, not as a one-time study plan or a replacement for implementation, investigation, design, or review.
- Preserve requested progress while spending learning effort only where misunderstanding could change a decision, verification, or outcome.

## Evidence and calibration state

Gather what is available:

- the active task, originating workflow, and next decision or action
- the user's stated learning goal, time constraint, desired support, and accountability
- what the user has explicitly explained, chosen, questioned, or marked as unknown
- the change, proposal, evidence, or AI-generated output that must be understood or evaluated
- applicable authority, risk, and verification constraints

Keep separate:

- confirmed task facts and authoritative decisions
- the user's stated understanding and unknowns
- reasonable inferences about understanding, with their basis
- AI-generated claims that still need evidence
- user-owned decisions and work that may be delegated

Do not infer competence or confusion from silence. Treat an answer to an understanding checkpoint as evidence for the point it addresses, not as proof of general mastery.

## Calibration cycle

1. Identify what the user needs from the active task now and what they need to understand, explain, verify, or decide themselves.
2. Determine whether misunderstanding could materially affect the next action, accepted risk, verification, or later accountability. Do not expand into general theory that cannot change the current work.
3. Separate decision ownership:
   - the user owns objectives, priorities, accepted scope, risk tolerance, authorization, and final adoption when they are accountable for it
   - AI may gather evidence, generate options, draft changes, run authorized checks, and explain reasoning
   - AI may analyze consequential technical decisions, but return evidence, trade-offs, unknowns, and the adoption point to the responsible user
4. Select support that fits the user's goal and constraints. Depending on context, explain before acting, work through a decision together, perform authorized work and explain its evidence afterward, reconstruct an existing AI output, or let the user perform a key step and review it.
5. Continue or hand off to the originating workflow under that calibration. Do not stop merely to emit a learning plan when the next authorized action can proceed.
6. Use an understanding checkpoint only when the response could change the next action or reveal a material gap. Ask for a focused explanation, choice, prediction, or verification step rather than testing general recall.
7. Incorporate the user's response and new evidence. Preserve resolved points, reassess only the material gaps that remain, and adjust the support method when needed.
8. Repeat while another calibration exchange can improve a decision, verification, or accountable explanation. Otherwise return to the originating workflow or finish the requested task.

## Decision criteria

Balance learning and progress on continuous axes rather than forcing a learning-versus-deadline choice. Consider:

- the depth of understanding the user requested for this task
- the consequence and reversibility of a mistaken decision
- whether the user must review, operate, maintain, approve, or explain the result
- the available time and whether explanation can occur before, during, or after execution
- the strength of available evidence

Prefer a brief explanation with continued execution when the request is clear, authorized, and reversible. Increase collaboration or checkpoints when the user explicitly prioritizes learning, cannot evaluate an important output, or owns a consequential decision.

Use evidence appropriate to the claim, such as official documentation or standards, repository source and history, existing implementations, direct observation, reproduction, logs, tests, measurements, or an authorized domain owner's decision. Treat AI conclusions as inferences from evidence, not as evidence by themselves.

## State and handoff contract

Use the state that describes the next action:

- `Ready`: the originating workflow can proceed and material decision ownership and verification are clear
- `Proceed with checkpoints`: work can continue, with identified decision or understanding checkpoints
- `Continue calibration`: one material understanding gap still needs a focused explanation, question, or joint step before the affected action
- `Blocked`: a required user-owned decision, authorization, or risk acceptance is unavailable

Adapt the response to the task. Include only information that changes the next action:

- the understanding or decision being protected
- the selected support method and reason
- work AI may proceed with and decisions the user owns
- the next checkpoint or originating-workflow action
- supporting evidence, unverified claims, and residual unknowns

Do not require a fixed template, number of concepts, comprehension questions, or self-study tasks. Offer practice or later self-study only when the user requests it or it materially supports the stated learning goal.

## Boundaries

- Do not withhold a direct answer or authorized implementation merely because the domain is unfamiliar. Adjust explanation and checkpoints to the user's stated goal.
- Do not convert learning support into authority to choose the user's objective, scope, risk tolerance, approval, or final adoption.
- Do not force the user to rediscover technical work that AI can safely perform and explain.
- Do not treat a quiz, the user's confidence, or passing tests alone as proof of understanding or correctness.
- Keep high-risk controls required by the originating workflow; explanation and evidence do not replace authorization, rollback, recovery, sandboxing, or deterministic verification.
- Use `choose-ai-execution-setup` when the user explicitly asks which available chat, agent, model, tool-enabled surface, or already-defined agent topology should handle the task. This Skill owns learning and understanding calibration within the selected workflow.
- Keep the workflow self-contained when adjacent Skills are unavailable. Name a handoff only when it clarifies ownership of the next action.
