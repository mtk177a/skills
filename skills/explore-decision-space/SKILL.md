---
name: explore-decision-space
description: Expands the decision space before a consequential, hard-to-reverse choice converges prematurely on one problem frame or solution anchor, or after a recovery handoff has already established that an anchor is exhausted. Use to surface materially different problem frames when the problem is unsettled, or structurally different solution options after the frame is fixed, then narrow only with explicit constraints and evidence; not for clarifying missing request information, defining ambiguous terms, diagnosing whether repeated failures are stalled, planning an already selected approach, implementing changes, or running automated optimization.
license: MIT
---

# Explore Decision Space

## Objective

- Prevent a consequential decision from collapsing prematurely onto one problem frame or solution anchor.
- Expand the unsettled layer of the decision, preserve evidence and constraints, and narrow only when the available basis supports it.
- Return a decision-ready exploration or an explicit evidence or user-decision boundary without implementing the selected option.

## Evidence and decision state

Gather what is available:

- the objective, affected users or systems, success criteria, constraints, non-goals, authority, and reversibility
- the current problem frame, solution anchor, alternatives already considered, and reasons they were retained or rejected
- observed facts, reported results, assumptions, inferences, unknowns, and decision criteria
- prior attempts or a structural-search handoff when another workflow has established that an anchor is exhausted

Do not treat a supplied frame, favored option, score, or previous conclusion as authoritative merely because it is detailed. Preserve confirmed constraints while keeping disputed assumptions open.

Identify the unsettled layer:

- `Problem space`: what problem, causal structure, boundary, stakeholder need, or success definition should govern the decision is not yet settled.
- `Solution space`: the problem frame is sufficiently fixed, but the available approaches are anchored on one mechanism or design neighborhood.
- `Both`: the current solution anchor depends on an unsettled problem frame. Explore problem frames first and do not expand solution options across incompatible frames as though they were directly comparable.
- `No expansion needed`: the decision is low consequence, readily reversible, already supported by adequate alternatives and evidence, or better handled by an adjacent workflow.

## Workflow

1. Restate the preserved objective, confirmed constraints, current anchor, and unsettled layer. Separate observed facts, reported results, inference, assumptions, and unknowns that can change the decision.
2. Decide whether expansion is decision-relevant. If missing intent, authority, terminology, evidence access, or an originating diagnostic prevents valid exploration, stop with the appropriate handoff or evidence request instead of inventing it.
3. For `Problem space`, identify diversity axes that can change the meaning or boundary of the problem. Develop materially different frames and state for each: what it treats as the problem, what evidence supports or challenges it, what it preserves, what it excludes, and what observation would distinguish it.
4. Establish which problem frame is supported, conditionally selected, requires evidence, or requires a user value judgment. Do not move to solution expansion under a single asserted frame when material competing frames remain unresolved.
5. For `Solution space`, identify diversity axes that change mechanism, responsibility boundary, state representation, processing order, tool boundary, operational model, or another decision-relevant structure. Develop alternatives until the material axes and trade-offs needed for this decision are covered; do not target a fixed candidate count.
6. Compare frames or options against explicit criteria. Keep observed performance separate from predicted properties and mark unavailable comparisons as unknown.
7. Narrow only when evidence, constraints, or an authorized user preference supports it. Otherwise return the distinguishing evidence, decision, or experiment needed next. Never declare a winner merely to complete the workflow.
8. Return one completion state and hand control back without editing files, executing experiments, changing evaluation assets, or implementing an option.

## Completion states

- `No expansion needed`: Explain why additional divergence would not improve the current decision and identify the owning workflow when applicable.
- `Problem frames ready`: Materially different problem frames and their distinguishing conditions are explicit, but selecting a frame still needs evidence or a user judgment.
- `Options ready`: The governing problem frame and structurally different solution options are explicit, but selection still needs evidence or a user judgment.
- `Evidence needed`: A specific observation or comparison can distinguish material frames or options.
- `Selected for design`: One frame and option are supported strongly enough to hand off for implementation design, with the selection basis and rejected alternatives preserved.
- `Blocked`: Missing intent, authority, safety margin, or indispensable context prevents valid exploration.

## Reporting contract

Adapt the structure to the decision. Include:

- completion state and whether the unsettled layer is the problem space, solution space, both, or neither
- preserved objective, confirmed constraints, current anchor, and decision criteria
- observed facts, reported results, assumptions, inferences, and unknowns that affect the choice
- diversity axes and materially different problem frames or solution options
- for each frame or option, its structural difference, supporting and challenging evidence, conditions, trade-offs, and evidence status
- the comparison basis, rejected alternatives worth preserving, and unresolved value judgments
- the supported selection, distinguishing evidence, user decision, or adjacent-workflow handoff needed next

## Boundaries

- Keep the workflow read-only. Read evidence already within scope, but do not edit files, run the proposed experiment, alter evaluation cases or graders, implement an option, or make external writes.
- Do not invent requirements, evidence, authority, diversity, or certainty.
- Do not count wording variants as materially different frames or options.
- Do not force a fixed number of frames, options, iterations, or agents.
- Do not require another Skill, subagent, or multi-agent workflow to produce a useful result.
- Use `clarify-request` for missing purpose, success criteria, constraints, or authority; `define-referents` when terminology itself collapses distinct concepts; `break-failure-loop` to diagnose repeated equivalent attempts; `design-changes` after an approach is selected; and `implement-changes` only for authorized execution.
- Automated evolutionary search, repeated candidate execution, archive optimization, and score-driven mutation require a separate runner or tool and are outside this instruction-only Skill.
