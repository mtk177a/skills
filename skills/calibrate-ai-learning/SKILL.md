---
name: calibrate-ai-learning
description: Use when delegation to AI agents is getting too deep, or when you want to maintain understanding while working in an unfamiliar domain.
license: Apache-2.0
---

# Calibrate AI Learning

## Purpose

- Calibrate the scope of AI delegation so the user retains judgment, verification, and accountability.
- When work is about to proceed with insufficient understanding, separate concepts to learn from tasks to delegate.

## When to use

- When you feel you cannot explain the reason for a change or accept/reject a decision because too much has been delegated to AI
- When working in an unfamiliar technology, library, or design domain, and you want to organize what to understand first
- When you want to decide what to ask AI and what to judge yourself before starting implementation or review
- When you want to adjust the depth of support based on whether the priority is learning or meeting a deadline

## Input (optional)

- The task, thing to build, or problem to fix
- What you currently understand and what you do not
- Whether the priority is learning or meeting a deadline
- Proposals, code, or review comments already received from AI
- Available primary sources, existing implementations, test commands

## Steps

1. Summarize the request briefly; separate current understanding from unknowns.
2. Narrow the concepts, prerequisites, and decision criteria needed for the task to 3–5.
3. Confirm whether the priority is learning or meeting a deadline; decide the depth of AI support.
4. Separate tasks that can be delegated to AI from decisions the user must make themselves.
5. Organize the request to AI so that purpose, constraints, and points to verify are clear.
6. Create short comprehension-check questions.
7. Narrow self-study tasks to try with little or no AI support to 1–2.
8. For high-risk areas, explicitly state which of official documentation, existing implementations, or test results will be used for verification.

## Output format

- Current understanding: ...
- Concepts to understand:
  - ...
- Tasks that can be delegated:
  - ...
- Decisions to make myself:
  - ...
- Request to AI: ...
- Comprehension check questions:
  - ...
- Self-study tasks for next time:
  - ...
- Evidence to use for verification: ...

## Companion skills

- `triage-agent-usage`
- `design-changes`
- `review-changes`
- `validate-fix`

## Boundaries

### Always:

- Separate current understanding from unknowns
- Separate delegatable tasks from decisions to make yourself
- Keep concepts to understand focused on what is needed for the current task, not general theory
- For high-risk areas, explicitly state which available evidence will be used for verification; leave unverified items as open
- Treat AI-generated content as unverified input; leave evidence and open items

### Ask first:

- When the depth of support would change significantly depending on whether the priority is learning or a deadline
- When the user is about to fully delegate a high-accountability, high-risk decision to AI

### Never:

- Default to revealing answers without engagement
- Proceed on an important decision using only AI conclusions, without evidence or comprehension checks
- Move directly to implementation without organizing what concepts need to be understood in an unfamiliar domain
