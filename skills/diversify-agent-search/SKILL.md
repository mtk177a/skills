---
name: diversify-agent-search
description: Use when agent, workflow, prompt, or code improvement is stuck in the same design neighborhood - widen the search with multiple candidates, an archive, diversity axes, and case-level evaluation.
license: MIT
---

# Diversify Agent Search

## Purpose

- Break out of single-candidate improvement loops where the agent keeps polishing the current approach.
- Reframe agent, workflow, prompt, or code improvement as candidate search with preserved lessons, structural alternatives, and protected evaluation assets.

## When to use

- The same direction has been tried two or more times without meaningful progress.
- Proposed fixes mostly add prompt text, regular expressions, output normalization, retries, or local patches.
- Evaluation focuses on an average score or latest best candidate while case-level strengths and weaknesses are unclear.
- The processing order, responsibility split, input chunking, retry policy, or LLM-vs-code boundary has not been reconsidered.
- A related Skill detects that work is converging on the same design neighborhood.

## Input (optional)

- Current candidate or workflow
- Attempt history and failed branches
- Evaluation cases, score summaries, or test results
- Constraints such as budget, latency, safety, maintainability, and reviewability
- Protected evaluation assets that must not be changed

## Steps

1. Identify the current anchor: what design assumption, candidate, or metric the work is orbiting.
2. List evidence of stagnation from attempts and evaluation results.
3. Mark protected evaluation assets; do not edit cases, expected outputs, graders, or scoring rules to make a candidate pass.
4. Create or update a candidate archive with both successful and failed branches.
5. Define diversity axes that represent structural differences, not wording differences.
6. Propose at least three structurally different candidates.
7. Compare candidates by case type, not only by average score.
8. Select the next parent or branch to extend, with a reason based on evidence and diversity.
9. Set a budget and stop conditions before further implementation.
10. If the search can be handled locally, return the plan directly; use companion Skills only if they are available and add value.

## Output format

- Current anchor: ...
- Evidence of stagnation:
  - ...
- Protected evaluation assets:
  - ...
- Candidate archive:
  - Candidate: ...
    Parent: ...
    Structural change: ...
    Strong cases: ...
    Weak cases: ...
    Lesson preserved: ...
- Diversity axes:
  - ...
- Alternative candidates:
  - ...
- Evaluation matrix:
  - ...
- Next parent / branch: ...
- Budget / stop conditions: ...
- Companion handoff if available: ...

## Boundaries

### Always:

- Preserve failed branches when they contain reusable evidence or lessons
- Propose at least three structurally different candidates
- Compare case-level behavior, not only average scores
- Separate evaluation assets from implementation candidates
- Keep the Skill useful even when no other Skill is installed

### Ask first:

- When changing evaluation cases, expected outputs, graders, or scoring rules is proposed
- When the search budget, latency, or implementation cost would grow significantly
- When a candidate would require dependency additions, external services, or destructive changes

### Never:

- Do not rewrite evaluation assets to make the current candidate look better
- Do not treat prompt wording variants as sufficient diversity by themselves
- Do not keep optimizing the current candidate without naming the design assumption being tested
- Do not require another Skill, subagent, or multi-agent workflow for the basic output

## Notes

- Structural diversity can include processing order, responsibility boundaries, input chunking, state representation, retry policy, tool boundaries, model selection, or which parts are fixed in code.
- If `break-failure-loop`, `design-changes`, or `validate-fix` is available, it can be used as a companion, but this Skill must still stand alone.
