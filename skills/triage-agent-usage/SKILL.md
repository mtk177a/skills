---
name: triage-agent-usage
description: Before starting work, separate the right agent, tool, and model weight for the task.
license: MIT
---

# Triage Agent Usage

## Purpose

- Before starting, determine which tool and what model weight should be used.
- Prevent jumping into a heavy agent session immediately; secure sufficient capability while keeping usage costs low.

## When to use

- When you are about to ask AI to do work but are unsure which tool to start with
- When you want to separate up front whether the task is implementation with repo reading, text organization, or incident investigation
- When you want to judge whether there is a genuine reason to use a high-capability model

## Decision axes

- Does the task require reading the repository?
- Does it require changes across multiple files?
- Does it require delegating implementation and test execution?
- Is this an agent, workflow, prompt, or code improvement loop that may need candidate search?
- Is there uncertainty that requires a high-capability model?
- Is the cost of failure and rework high?
- Is the priority learning or meeting a deadline?
- Is this work where the person can review the output and explain the reasoning?

## Recommended heuristics

- Text organization, emails, design notes: standard chat (ChatGPT / Claude.ai)
- IDE completion, simple single-function fixes: completion model
- Small existing-pattern implementations: lightweight coding agent
- Multi-file changes with test execution: Codex or Claude Code
- Repeated agent / workflow / prompt improvement: treat as search design, not only another local edit
- Unknown-cause incidents, security, billing, authorization: use a high-capability model explicitly

## Steps

1. Summarize the request in 1–2 lines and classify it as: implementation, investigation, or text organization.
2. If the repo does not need to be read, first consider standard chat.
3. If the repo needs to be read but changes are local and follow existing patterns, consider completion or a lightweight coding agent.
4. If multi-file changes and test execution are needed, consider Codex or Claude Code.
5. If unknown-cause incidents, security, billing, authorization, or destructive changes are involved, use a high-capability model explicitly.
6. If the work is repeated agent, workflow, prompt, or code improvement, decide whether candidate search and case-level evaluation are needed before recommending another local edit.
7. If learning is a strong priority, separate tasks to delegate to AI from decisions the person must make themselves.
8. When choosing a heavier option, have the reason ready to state in one line.
9. After selecting a tool, cut work units as small as possible and minimize the context to pass.

## Output format

- Recommended tool: ...
- Recommended model / profile: ...
- Work units: ...
- Minimum context to pass: ...
- Search design needed?: ...
- Things the person should decide first: ...
- Prerequisites for understanding and review: ...

## Boundaries

### Always:

- Consider whether the lightest option is sufficient first
- Do not classify repeated self-improvement loops as simple local edits without checking for search design needs
- State the reason for using a heavy agent session
- Keep passed context to the minimum
- When learning is a priority, separate what the person can explain from what to delegate to AI

### Ask first:

- When high-risk work is about to proceed with only a lightweight model or completion
- When a high-capability model will be used but what to delegate is unclear

### Never:

- Default to proposing a heavy coding agent for work that does not require reading the repository
- Leave the reason for model selection unclear when proceeding with high-rework-cost work
