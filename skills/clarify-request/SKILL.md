---
name: clarify-request
description: Use when a request is ambiguous (clarify, questions, requirements) — ask 1–4 clarifying questions, or state assumptions and proceed.
license: Apache-2.0
---

# Clarify Request

## Purpose

Resolve ambiguity in a request to prevent incorrect implementation and rework.

## When to use

- When purpose, scope, constraints, or environment are unclear, and there is a risk of incorrect implementation or rework
- When a request has multiple valid interpretations (e.g., which environment? what priority? how much to automate?)

## Steps

1. Present **1–4 numbered clarifying questions**.
2. Where possible, provide **options (A/B/C) plus a recommendation (default)**.
3. If the user says "proceed on assumptions," list the **assumptions as bullet points** before proceeding.

## Output format

```text
Questions:
1) ...
2) ...
Recommendation: ...
(If proceeding on assumptions) Assumptions:
- ...
```

## Boundaries

### Always:

- Do not start a major direction decision or file edit without the user's answer or explicit assumptions

### Ask first:

- (none)

### Never:

- Proceed with implementation or major direction decisions without clarification
