---
name: design-changes
description: Use before implementing to design the change approach, impact scope, risks, and verification strategy.
license: Apache-2.0
---

# Design Changes

## Purpose

- Solidify the change approach before implementation; clarify impact scope and verification strategy.
- Produce an implementable design for the requirements, and determine a change approach and test strategy usable on their own for review and go/no-go decisions.

## When to use

- When you want to separate what to change from what not to change
- When you want to organize dependencies and risks before implementing
- When you want to define the testing and verification approach up front

## Input (optional)

- Output from `scope-request`
- Related files or existing specifications
- Notes on understanding existing code or configuration

## Steps

1. Review the existing structure and entry points.
2. If the primary purpose is readability improvement, first identify the entry point, major branches, overall flow, and helper groups.
3. For long files, understand the grouping by processing stage before writing the change plan.
4. Separate what to change from what not to change.
5. Organize dependencies, module boundaries, and impact scope.
6. For changes like indentation, comment, blank line, or commented-out code cleanup, define change units at the granularity the reader follows, not at local diffs.
7. List risks and mitigations.
8. Decide the test strategy and verification approach.
9. Explicitly state the conditions for proceeding to implementation, the scope, and stop conditions.
10. Split change units into minimal diffs; explicitly flag anything that should proceed only with approval.
11. Explicitly state concepts to understand before changing, key tradeoffs, and decisions the user must be able to explain.
12. If high-risk or uncertain design decisions remain, explicitly state the need for additional confirmation.

## Output format

- Design summary: ...
- What to change: ...
- What not to change: ...
- Dependencies and impact: ...
- Module boundaries: ...
- Concepts to understand before changing: ...
- Key tradeoffs: ...
- Decisions the user must explain: ...
- Key risks: ...
- Mitigations: ...
- Test strategy: ...
- Verification approach: ...
- Conditions to proceed to implementation: ...
- Implementation scope: ...
- Stop conditions (Ask first): ...
- Change units: ...
- Self-review checklist: ...

## Companion skills

- `plan-risky-change`

## Boundaries

### Always:

- Separate what to change from what not to change
- Pair risks with verification approach
- State the test strategy explicitly
- State conditions to proceed and stop conditions explicitly
- For readability improvements, define change units at the granularity the reader follows
- Leave concepts to understand and decisions to explain
- Match existing style and design
- Do not use another agent / subagent by default; return design decisions from this Skill first

## Self-review checklist

- Does the plan make the entry points and major branches immediately clear?
- Are change units aligned with comment granularity and roles?
- Do change units match the reader's unit of understanding?
- Can the user explain the key tradeoffs in their own words?

### Ask first:

- When dependency additions or large design changes are needed
- When large-scale reorganization or destructive changes are needed

### Never:

- Start large changes without a design
- Proceed with large structural rewrites without approval
