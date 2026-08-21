---
name: design-changes
description: Designs an implementation-ready change approach, affected and excluded scope, risks, decision points, and verification coverage before code or configuration is changed. Use after the request and approach are understood and before implementation when impact or trade-offs need organizing; not for clarifying an undefined request, expanding unsettled problem frames or solution options, designing an Agent Skill, implementing changes, or assessing high-risk execution readiness and safety controls on its own.
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
- reviewer context that can affect later review calibration: product or operational criticality, affected users, data and contracts, exposure, accepted trade-offs, detection and recovery controls, and requested review focus

Distinguish `Observed`, `Reported`, `Inferred`, `Unknown`, and `Conflicting` material claims and planned verification. Do not infer low criticality or exposure from missing context. If the request is not understood well enough to define success and non-goals, route it to `clarify-request` before designing the change.

## Workflow

1. Restate the intended behavior, accepted scope, non-goals, and applicable constraints. Confirm that design can begin without inventing unresolved requirements.
2. Inspect the existing structure and identify the entry points, major branches, ownership boundaries, and current verification paths that the change can affect.
3. Before minimizing the diff, identify the smallest coherent boundary that fully addresses the confirmed cause and current requirements. Derive it from affected responsibilities, invariants, contracts, and known execution paths; then state its explicit non-targets and affected interfaces, modules, data, configuration, dependencies, and consumers.
   Preserve existing public inputs, signatures, and accepted call forms unless confirmed current evidence requires changing them. When terms such as missing or omitted could describe either an existing sentinel value or a new call form, resolve that distinction from the current contract and observed callers rather than broadening the interface by assumption.
   Do not infer a shared boundary from source-code similarity alone. Consolidate behavior when the evidence establishes the same current knowledge, responsibility, invariant, or contract; otherwise prefer small local duplication to a premature or incorrect abstraction.
4. Decide whether that boundary supports a local correction or requires a structural correction. Do not select a local patch merely because it changes fewer lines when it would leave a confirmed cause unresolved, duplicate an existing rule, bypass an established responsibility boundary, create inconsistent behavior across known paths, or require a known follow-up correction.
5. Compare the selected change with a structurally different alternative only when uncertainty, coupling, or rework cost makes that comparison decision-relevant. When a structural correction is required, explain why the local alternative is insufficient, which current responsibility or invariant it restores, which contracts it affects, and what remains unchanged.
6. When the change adds an abstraction, dependency, configuration surface, compatibility path, process, service, or deployment unit, record the current problem it solves, the evidence that the problem exists or is an accepted near-term requirement, the simpler alternative considered, why that alternative is insufficient, and the ongoing maintenance or operational cost. Separate required current work from optional future improvement.
7. Pair each material risk with a prevention, mitigation, detection, recovery, compensation, or containment strategy suited to the failure mode. Do not list a risk without explaining how the plan handles it.
8. Map each changed responsibility, behavior, regression risk, and failure boundary to a verification method and expected evidence. Reuse a check when it exposes multiple claims clearly; add another only for a distinct risk.
9. Define conditions to proceed, implementation scope, and stop conditions. Surface dependency additions, destructive operations, unresolved authority, and high-risk execution-readiness needs before implementation. When additional safety controls are needed, name the `assess-risky-change-readiness` handoff explicitly and stop this workflow at the ordinary change design.
10. Split the work into minimal reviewable units aligned with behavior and ownership. For readability changes, use the processing stages and the reader's unit of understanding rather than isolated whitespace or comment diffs.
11. Record material trade-offs and concepts the user or reviewer must understand when they affect acceptance, safety, or future maintenance.
12. Prepare planned reviewer context from the available evidence: objective and expected result; product or operational context and criticality; scope and non-goals; affected users, data, contracts, and exposure; constraints and accepted trade-offs; planned verification and unknowns; detection and recovery controls; and review focus. Include only relevant fields and preserve material evidence states instead of filling gaps.
13. Produce an implementation-ready handoff. Keep proposed checks separate from observed results and do not implement the change.

## Decision criteria

- Prefer the smallest coherent change that fully addresses the confirmed cause and current requirements while preserving established boundaries. Minimize incidental complexity only after establishing that sufficient boundary.
- Preserve existing style and design unless a demonstrated failure requires a structural change.
- Do not use speculative future flexibility to justify complexity, and do not use diff size to reject a structural correction required by current evidence.
- Use design principles only to clarify a current responsibility, contract, substitution, interface, or dependency problem. Do not add structure to optimize for principle conformance itself.
- Use an exact output template only when a downstream consumer requires it; otherwise report the required information in a structure suited to the change.
- Choose verification depth from impact and uncertainty: static checks, targeted regression, or repeated empirical evaluation. Do not use a universal test, scenario, alternative, or run count.
- Use `assess-risky-change-readiness` when material operational, data, security, external-state, irreversibility, or recovery risks require execution-readiness controls beyond an ordinary implementation handoff.

## Reporting contract

Use a structure suited to the change. Include:

- the recommended approach and its evidence, assumptions, and unresolved questions
- what changes and what remains unchanged
- why a local correction is sufficient or why a structural correction is required, when that choice is material
- required current work versus optional future improvement
- dependencies, affected boundaries, consumers, and compatibility impact
- material risks paired with mitigations or controls
- verification coverage: responsibility or risk → plausible failure → check and expected evidence
- planned reviewer context, including material unknowns and evidence states, sufficient for implementation and later review without declaring review severity
- conditions to proceed, implementation scope, stop conditions, and reviewable change units

Include alternative designs, module maps, migration details, rollback, or user explanation points only when they are material. Clearly label planned validation as unexecuted; do not present it as observed evidence.

## Boundaries

- Use `clarify-request` when the objective or success criteria are still undefined, `design-skill` for Agent Skill responsibility and trigger design, and `implement-changes` only after this handoff is accepted.
- Pair this Skill with `assess-risky-change-readiness` when a destructive, security-sensitive, migration, dependency, or other consequential change needs additional safety, recovery, evidence, or authorization-readiness controls. Use `explore-decision-space` before this Skill when a consequential decision still needs materially different problem frames or solution options; do not use it after an approach is adequately selected.
- When that high-risk boundary applies, name `assess-risky-change-readiness` in the implementation handoff and identify the unresolved readiness needs rather than claiming the ordinary design is sufficient authorization to execute.
- Keep the workflow read-only. Do not add dependencies, make destructive changes, or start implementation.
- Do not force fixed headings, empty checklist sections, a minimum number of alternatives, or a minimum number of tests.
- Do not use another agent or subagent by default; make the design decision with the available evidence and leave unresolved high-impact choices to the user.
