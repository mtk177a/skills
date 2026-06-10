---
name: triage-review-feedback
description: Sort review comments from humans or other AI into accepted, deferred, and rejected — decide on a response approach.
license: Apache-2.0
---

# Triage Review Feedback

## Purpose

- Organize external review comments into a state where accept/reject decisions and a response approach can be determined.

## When to use

- When you receive a review from GitHub Copilot or another agent
- When you want to translate human review comments into implementation
- When you want to organize the validity and priority of findings

## Input (optional)

- Review body
- Target diff
- Related specifications or background
- Output from `review-changes`

## Steps

1. Summarize the review findings.
2. For each finding, separate whether it can be judged from local implementation alone, or whether it requires confirming external specifications or platform behavior.
3. For each finding, decide: accept, defer, or reject.
4. Write the reason for the decision.
5. For accepted findings, decide priority and response approach.
6. Extract findings that require additional confirmation as open items.
7. Treat findings that depend on external specifications or platform behavior as unverified input; do not automatically accept until verified against official documentation or primary sources.
8. When decision material is insufficient, explicitly state additional confirmation items; suggest using another agent / subagent only when needed.

## Output format

- Review summary: ...
- Findings:
  - ...
- Decisions:
  - ...
- Reasons for decisions:
  - ...
- Response approach:
  - ...
- Additional items to confirm:
  - ...

## Companion skills

- `research-web-safely`

## Boundaries

### Always:

- Separate the description of a finding from the reason for the accept/reject decision
- Attach priority to accepted findings
- Write the response approach to a granularity sufficient to proceed to implementation or defer
- Do not automatically accept findings that depend on external specifications or platform behavior without verification against official documentation or primary sources
- Do not use another agent / subagent by default; return accept/reject decisions from this Skill alone first

### Ask first:

- When a judgment that changes the spec itself is needed

### Never:

- Decide accept/reject without a reason
