---
name: triage-agent-usage
description: Selects an appropriate agent, tool, model capability, and work-unit size before work starts. Use when deciding between chat, completion, a coding agent, or heavier reasoning, or when operational delegation needs to be divided; not for calibrating learning or understanding during the work, choosing the substantive implementation design, or performing the task itself.
license: MIT
---

# Triage Agent Usage

## Objective

- Select the lightest execution surface and model capability that can perform the task with acceptable correctness and rework risk.
- Divide operational delegation into reviewable work units and pass only the context each unit needs.
- Keep tool and capability selection separate from substantive task decisions and learning calibration.

## Evidence

Gather what is available:

- the task type and expected outcome
- whether repository, external-system, or execution access is required
- affected scope, verification needs, uncertainty, reversibility, and cost of failure
- available tools, models, profiles, permissions, and environment constraints
- whether independent context, specialist analysis, or parallel work has a concrete benefit

Do not infer that a heavier agent is better merely because the task is important. Do not recommend a named tool or profile that is unavailable or whose capability is unverified.

## Selection workflow

1. Classify the operational work needed, such as text organization, repository implementation, investigation, review, or external-system interaction.
2. Identify the capabilities required to read the evidence, act within the authorized scope, and verify the result.
3. Start with the lightest available execution surface that satisfies those capabilities. Escalate model or agent weight when uncertainty, consequence, context volume, or verification complexity gives a concrete reason.
4. Decide whether the work needs one session, independent context, specialist review, or parallel units. Do not introduce another agent by default.
5. Divide delegated work by coherent outcome, ownership, and verification boundary. Avoid work units so broad that their evidence or changes cannot be reviewed.
6. Minimize the context for each unit without omitting its objective, constraints, relevant evidence, authority, and completion check.
7. State the recommendation and the reason for any heavier capability, additional agent, or broader context.
8. Hand off the selected execution setup. Leave implementation design, investigation conclusions, and adoption decisions to the workflow that owns them.

## Decision criteria

Examples are heuristics, not a fixed tool mapping:

- use ordinary chat when repository or execution access is unnecessary
- use completion or a lightweight coding surface for small, established-pattern edits when its output can be reviewed locally
- use a coding agent when repository discovery, multi-file changes, or test execution are required
- use stronger reasoning when the task has important unresolved uncertainty, high-cost rework, security or authorization consequences, or ambiguous evidence
- use independent or parallel agents only when context isolation, specialist judgment, or latency reduction outweighs coordination and review cost

If the user wants to preserve or recover understanding while the selected workflow proceeds, return an optional handoff to `calibrate-ai-learning`. Do not decide the teaching method, comprehension checkpoints, or user learning depth in this Skill.

## Reporting contract

Adapt the response to the decision. Include:

- recommended execution surface or tool
- required model capability or profile when a choice is material
- reason for escalation beyond the lightest adequate option
- work units and their ownership
- minimum context, permissions, and verification expected for each unit
- unverified availability or capability assumptions
- optional learning-calibration handoff when the user requested it

Do not force a named model, profile, multiple agents, or a fixed template when the available evidence does not require one.

## Boundaries

- Do not perform the task, select its substantive implementation, or treat tool selection as authorization.
- Do not make high-impact requirements, scope, risk tolerance, or adoption decisions for the user.
- Do not recommend a heavy coding agent for work that does not need its repository or execution capabilities.
- Do not use another agent or subagent by default; require a concrete context, specialization, verification, or latency benefit.
- Keep learning and understanding calibration with `calibrate-ai-learning`, while remaining self-contained when that Skill is unavailable.
