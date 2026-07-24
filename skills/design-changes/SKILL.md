---
name: design-changes
description: Designs an implementation-ready change approach, affected and excluded scope, risks, decision points, and verification coverage before code or configuration is changed. Use after the request is understood and before implementation when impact or trade-offs need organizing; not for clarifying an undefined request, designing an Agent Skill, implementing changes, or handling high-risk approval and rollback planning on its own.
license: MIT
---

# Design Changes

## Objective

- Produce the smallest decision-complete approach that an implementation workflow can follow without rediscovering scope, risk, or verification decisions.
- Separate what will change from what will remain unchanged and make the impact boundary reviewable.
- Stop at an implementation handoff; do not edit the target files.

## Evidence and inputs

Gather what is available:

- intended behavior, accepted scope, constraints, and non-goals
- relevant entry points, modules, interfaces, data flows, configuration, and tests
- existing specifications, repository guidance, and established implementation patterns
- observed failures, traces, prior attempts, or design decisions
- dependency, migration, compatibility, security, and rollout constraints

Distinguish confirmed evidence, inference, assumptions, unknowns, and planned verification. If the request is not understood well enough to define success and non-goals, route it to request scoping before designing the change.

## Workflow

1. Restate the intended behavior, accepted scope, non-goals, and applicable constraints. Confirm that design can begin without inventing unresolved requirements.
2. Inspect the existing structure and identify the entry points, major branches, ownership boundaries, and current verification paths that the change can affect.
3. Define the smallest coherent change and its explicit non-targets. Identify affected interfaces, modules, data, configuration, dependencies, and consumers.
4. Compare the minimal change with a structurally different alternative only when uncertainty, coupling, or rework cost makes that comparison decision-relevant.
5. Pair each material risk with a prevention, mitigation, rollback, or detection strategy. Do not list a risk without explaining how the plan handles it.
6. Map each changed responsibility, behavior, regression risk, and failure boundary to a verification method and expected evidence. Reuse a check when it exposes multiple claims clearly; add another only for a distinct risk.
7. Define conditions to proceed, implementation scope, and stop conditions. Surface dependency additions, destructive operations, unresolved authority, and high-risk approval or rollback needs before implementation. When high-risk controls are needed, name the `plan-risky-change` handoff explicitly and stop this workflow at the ordinary change design.
8. Split the work into minimal reviewable units aligned with behavior and ownership. For readability changes, use the processing stages and the reader's unit of understanding rather than isolated whitespace or comment diffs.
9. Record material trade-offs and concepts the user or reviewer must understand when they affect acceptance, safety, or future maintenance.
10. Produce an implementation-ready handoff. Keep proposed checks separate from observed results and do not implement the change.

## Decision criteria

- Prefer the smallest change that preserves established boundaries and satisfies the intended behavior.
- Preserve existing style and design unless a demonstrated failure requires a structural change.
- Use an exact output template only when a downstream consumer requires it; otherwise report the required information in a structure suited to the change.
- Choose verification depth from impact and uncertainty: static checks, targeted regression, or repeated empirical evaluation. Do not use a universal test, scenario, alternative, or run count.
- Use `plan-risky-change` when the work needs explicit approval, rollback, or recovery controls beyond an ordinary implementation handoff.

## Reporting contract

Use a structure suited to the change. Include:

- the recommended approach and its evidence, assumptions, and unresolved questions
- what changes and what remains unchanged
- dependencies, affected boundaries, consumers, and compatibility impact
- material risks paired with mitigations or controls
- verification coverage: responsibility or risk → plausible failure → check and expected evidence
- conditions to proceed, implementation scope, stop conditions, and reviewable change units

Include alternative designs, module maps, migration details, rollback, or user explanation points only when they are material. Clearly label planned validation as unexecuted; do not present it as observed evidence.

## Boundaries

- Use `scope-request` when the objective or success criteria are still undefined, `design-skill` for Agent Skill responsibility and trigger design, and `implement-changes` only after this handoff is accepted.
- Pair this Skill with `plan-risky-change` for destructive, security-sensitive, migration, dependency, or other high-risk work that needs explicit controls. Use `diversify-agent-search` only when design work is stuck in one design neighborhood.
- When that high-risk boundary applies, name `plan-risky-change` in the implementation handoff rather than merely describing additional approval or rollback work.
- Keep the workflow read-only. Do not add dependencies, make destructive changes, or start implementation.
- Do not force fixed headings, empty checklist sections, a minimum number of alternatives, or a minimum number of tests.
- Do not use another agent or subagent by default; make the design decision with the available evidence and leave unresolved high-impact choices to the user.
