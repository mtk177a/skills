---
name: audit-agent-rules
description: Audit AGENTS.md / skills / docs for naming, boundaries, approval rules, and heavy defaults — propose small, safe improvements.
license: Apache-2.0
---

# Audit Agent Rules

## Purpose

- Review `AGENTS.md`, `skills/*/SKILL.md`, and `docs` against actual usage.
- Prioritize small, safe, reviewable improvement proposals over broad rewrites.

## When to use

- When you want to propose improvements to `AGENTS.md` / `skills/*/SKILL.md` / `docs`
- When you want to check Skill names, `description`, boundaries, approval rules, or responsibility misalignment
- When you want to return small improvement proposals from Safety, Cost / Context, Consistency, or Clarity perspectives

## Prerequisites (important)

- `AGENTS.md` and Skills are configuration contracts and must be treated more carefully than ordinary code changes.
- Final judgment on approval boundaries follows `AGENTS.md`; this Skill audits and proposes within that assumption.
- Do not directly edit `AGENTS.md` / Skills / docs without explicit user approval.
- Even for typo-level fixes, produce a proposal first, then edit.

## Steps

1. Identify the target (`AGENTS.md` / `skills/*/SKILL.md` / `docs`).
2. Surface problems and improvement opportunities across the following dimensions (up to 5 findings):
   - Safety: secrets, destructive operations, approval boundaries, sandbox assumptions
   - Cost / Context: long always-loaded files, content that could be moved to a Skill, heavy model / reasoning / MCP / subagent defaults, absence of failure-loop stop rules
   - Consistency: duplicate rules, contradictions, scattered definitions
   - Clarity: vague approval conditions, scope, boundaries
   - Maintainability: overly long files, overloaded responsibilities, hard-to-update content
   - Triggerability: Skill names or `description` that are weak triggers, or wording that is misaligned with actual usage
   - Rule layering: evaluate heading/title naming and body/contract conventions separately; do not treat accepted expression differences as drift
3. Select one minimal, safe first change and propose it.

## Output format (fixed)

Always produce the following sections.

### 1. Summary

- What to improve and how (1–2 sentences)

### 2. Motivation

- Why this is needed (preventing incidents, reducing rework, readability, etc.)

### 3. Proposed changes

- List of files to change
- Diff or full revised content (for short changes)

### 4. Risk / Compatibility

- Impact on existing workflows, risk of unintended behavior

### 5. Next step

- Ask: "Is it OK to proceed with this change?"

## Priority order

1. Safety (highest)
2. Cost / Context
3. Consistency
4. Clarity
5. Maintainability
6. Expressiveness (nice-to-have)

## Avoid

- Do not immediately propose large refactors or full rewrites
- Do not propose changes that weaken guardrails
- Do not inflate proposals in pursuit of perfect generalization
- Do not propose dependency additions or workflow-breaking changes without prior discussion

## Boundaries

### Always:

- Do not directly edit `AGENTS.md` / Skills / docs without explicit user approval
- Start from the minimal, safe change

### Ask first:

- Before actually editing `AGENTS.md` / `skills/*/SKILL.md` / `docs`
- When a naming change or responsibility reorganization would affect users

### Never:

- Execute edits without approval

## Common improvement patterns (reference)

- `AGENTS.md` is too long → move details to Skills (`AGENTS.md` is for entry points and contracts only)
- Always-loaded files are too long → keep only contracts; move decision steps and checklists to Skills
- Too many Skills → consolidate role overlaps, clean up Skill names and `description` to improve trigger accuracy
- Heavy model / reasoning / MCP / subagent defaults → shift to lighter defaults; make heavy choices conditional
- No failure-loop protection → add stop conditions, hypothesis updates, and a single-next-step rule
- docs is disorganized → create an index in `docs/`
