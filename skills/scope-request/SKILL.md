---
name: scope-request
description: Clarify the scope of a request or problem — make purpose, completion criteria, constraints, and assumptions explicit.
license: MIT
---

# Scope Request

## Purpose

- Shape a vague request or problem into a form usable for decision-making and next actions on its own.
- Before starting, clarify the purpose, background, completion criteria, and constraints to reduce rework downstream.

## When to use

- When the background or purpose of a request is unclear
- When you want to establish completion criteria and constraints up front
- When you want to organize a bug or improvement request into an actionable unit

## Input (optional)

- Request text
- Related issues or error messages
- Known constraints

## Steps

1. Briefly summarize the key points, purpose, and background of the request.
2. Define the completion criteria (how "done" is determined).
3. Organize constraints (deadline, technology, operational, organizational) and assumptions.
4. Separately state what is out of scope and what is unresolved.
5. If ambiguity remains, list items to clarify; apply `clarify-request` if needed.
6. Organize the next steps so that this output alone is sufficient to proceed to the next judgment or requester confirmation.
7. Only when high-risk assumption gaps or significant ambiguity remain, explicitly state the need for additional confirmation.

## Output format

- Request summary: ...
- Purpose: ...
- Background: ...
- Completion criteria: ...
- Constraints: ...
- Assumptions: ...
- Out of scope: ...
- Unresolved items: ...
- Next steps: ...
- Items to confirm: ...

## Companion skills

- `clarify-request`
- `draft-issue`

## Boundaries

### Always:

- Separate purpose from completion criteria
- Record background and unresolved items separately
- Organize to a granularity where the output alone is sufficient for the next decision
- Do not use another agent / subagent by default; return organized results from this Skill alone first

### Ask first:

- When there appear to be significant interpretation differences in requirements or constraints

### Never:

- Assert a major implementation approach while still disorganized
- Proceed to design or implementation without a confirmed purpose
