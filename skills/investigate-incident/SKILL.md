---
name: investigate-incident
description: Investigate a production error or incident — organize failure paths, root-cause candidates, and next steps from a stack trace or log.
license: MIT
---

# Investigate Incident

## Purpose

- For errors occurring in production, investigate failure paths in the codebase and organize root-cause candidates with evidence.
- Offload trial-and-error exploration from the main context; return only what is needed to identify the cause.

## When to use

- When an error or incident occurs in production and you want to advance the codebase investigation first
- When you want to narrow root-cause candidates from a stack trace, log fragment, or failing feature
- When you want to organize reproduction conditions, failure paths, evidence, and open items before starting a fix implementation

## Input (optional)

- Error message
- Stack trace
- Affected feature and impact scope
- Whether reproduction steps are known
- Recent deploy / PR / feature flag information
- Suspicious files or modules
- Available verification commands

## Steps

1. Briefly organize the key facts, impact scope, known information, and missing information.
2. Identify entry points, failure location candidates, and related configuration in the codebase.
3. For noisy exploration or cutting between multiple candidates, organize verification angles and hypotheses as the investigation proceeds.
4. Separate what can be reproduced, what cannot, and the priority of hypotheses.
5. For each hypothesis, link code-level evidence, related files, and conditions to verify.
6. Explicitly state hypotheses, confirmed items, unknowns, and next branches; avoid baseless assertions.
7. Even if the cause cannot be confirmed, organize the leading hypotheses, additional information needed, and what to check next.
8. Do not proceed to fix implementation; compile a handoff for `design-changes` or `implement-changes` if needed.

## Output format

- Incident summary: ...
- Impact scope: ...
- Reproduction status: ...
- Failure path description: ...
- Leading hypotheses:
  - High: ...
  - Medium: ...
  - Low: ...
- Evidence files / config / functions: ...
- Confirmed: ...
- Unconfirmed: ...
- Next branches: ...
- Missing information: ...
- Next thing to check: ...
- Provisional containment options: ...
- Handoff for fix: ...

## Companion skills

- `design-changes`
- `record-session-handoff`

## Boundaries

### Always:

- Link evidence to files, configuration, functions, and commands
- Separate confirmed facts from unconfirmed items
- Show root-cause candidates with priority ordering
- Separate hypotheses, confirmed, unconfirmed, and next branches
- Organize investigation notes and handoff items separately

### Ask first:

- When access to external logging, monitoring tools, or issue trackers is needed
- When production data or production permissions would be used directly
- When proceeding to high-risk changes or containment operations

### Never:

- Silently make production changes or data changes
- Proceed to fix implementation or deploy as part of the investigation
- Close the investigation with baseless assertions
