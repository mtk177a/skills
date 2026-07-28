---
name: draft-issue
description: Turn a decision-ready bug report, improvement, or feature request into an Issue draft and filing steps. Use after the request is sufficiently clear or when drafting can expose remaining gaps; not for clarifying an ambiguous request on its own, implementing the work, or posting an Issue without confirmation. (issue, ticket, backlog, jira, redmine)
license: MIT
---

# Draft Issue

## Purpose

- Provide steps and a draft for filing a decision-ready request as a trackable Issue (GitHub / Jira / Redmine / Backlog / etc.).

## When to use

- When you want to turn a sufficiently clear bug report, improvement, or feature request into an Issue
- When you want to prepare a bug report or feature request template

## Input (optional)

- Target project / tracker
- Issue type (bug / improvement / feature request)
- Whether an existing template exists
- Labels / assignee

## Steps

1. Confirm the target project / tracker and issue type.
2. If the core of the Issue is unclear, apply `clarify-request` until the request is decision-ready or blocked; do not fabricate the problem, expected outcome, or use case.
3. Do a quick duplicate check against existing Issues (by title / keywords).
4. Check whether an Issue template exists; comply with it if one does.
5. Draft the title and body.
6. Decide on labels and assignee.
7. Organize links to related Issues / PRs if any.
8. Do a final review and confirm whether to create or keep as a draft.

## Output format

```markdown
# <Issue title>

## Body

### Bug report template
- Steps to reproduce:
- Expected result:
- Actual result:
- Environment:
- Additional information:

### Feature request template
- Problem / background:
- Expected outcome:
- Use case:
- Alternatives (optional):

## Labels
- <label>

## Assignee
- <person>

## Related links
- <Issue / PR / documentation>
```

## Boundaries

### Always:

- Confirm the target project / tracker and issue type
- Check for duplicate Issues
- Comply with existing templates when available
- Avoid including secrets

### Ask first:

- Whether to actually create the Issue (draft only vs. actual creation)
- When adding a new label is needed
- When the assignee is unknown

### Never:

- Include secrets
- Force operations that require permissions
- Create issues in bulk or automate without approval

## Notes (optional)

- When the request is vague, continue the `clarify-request` cycle until the Issue can be drafted without inventing material details or the request is blocked.
