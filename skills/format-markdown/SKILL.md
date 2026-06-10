---
name: format-markdown
description: Normalize Markdown style against CommonMark — evaluate and apply rules for blank lines, headings, lists, code fences, and link syntax. (markdown, commonmark, style, format, normalize)
license: MIT
---

# Format Markdown

## Purpose

Safely normalize and standardize Markdown against CommonMark.

## When to use

- When you want to fix inconsistent Markdown style
- When you want to align with common best practices
- When you want to evaluate changes against the existing style before applying

## Input (optional)

- Target scope
- Rules to prioritize
- Acceptable range of existing style deviations

## Steps

1. Confirm the target scope and purpose.
2. Refer to the [CommonMark specification](https://spec.commonmark.org) and categorize rules as recommended / context-dependent / discouraged.
3. Decide which rules to apply, focusing on recommended rules (exclude those that conflict).
4. If a change might conflict with existing style, get approval first.
5. After changes, present the diff and provide a rollback procedure if needed.
6. For large-scale changes, apply `plan-risky-change` first.

## Output format

- Judgment:
  - Recommended: ...
  - Context-dependent: ...
  - Discouraged: ...
- Change approach:
  - Scope: ...
  - Rules applied: ...
- Impact / risk: ...
- Rollback: ...
- Next step: ...

## Boundaries

### Always:

- State the rule validity assessment explicitly
- Explicitly state the potential for conflict with existing style

### Ask first:

- Large-scale changes or broad reformatting
- Changes that affect existing operational rules

### Never:

- Add dependencies or reuse external code without authorization
