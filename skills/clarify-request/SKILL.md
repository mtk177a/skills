---
name: clarify-request
description: Clarifies or structures an ambiguous request into a decision-ready handoff through an iterative cycle of resolving known facts, asking material questions, and stating low-impact assumptions. Use when the user asks to clarify, scope, or organize a request, when missing purpose, success criteria, constraints, environment, authority, or non-goals could materially change later work, or when continuing after the user answers clarification questions; not for designing an understood change, selecting implementation files, implementing, or reviewing.
license: MIT
---

# Clarify Request

## Objective

- Turn an ambiguous or insufficient request into a state that the intended next workflow can enter without inventing requirements, authority, or risk acceptance.
- Treat clarification as an iterative workflow across turns rather than a single batch of questions.
- Interrupt the user only for information or decisions that can materially change the next action.

## Evidence and clarification state

Gather what is available:

- the request and relevant conversation history, including prior questions and answers
- the intended next workflow and the information or authorization it requires
- applicable instructions, known environment details, related issues, errors, or constraints
- facts available through safe, relevant read-only inspection

Track these separately as clarification progresses:

- confirmed facts supplied by the user or authoritative sources
- reasonable inferences and their evidence
- explicit working assumptions
- unresolved questions and contradictions
- missing authorization or risk acceptance

Do not convert an inference, assumption, incomplete answer, or silence into a confirmed requirement.
Distinguish a value that exists but has not been supplied or observed from a decision that has not been made; do not relabel `unspecified` or `unknown` as `undecided`.

## Clarification cycle

1. Identify the intended next workflow and the minimum information and authority it needs. Decision-ready means ready for that workflow, not fully specified for every later step. Do not require the user to decide facts or technical choices that the next workflow is authorized and expected to investigate or design.
2. Incorporate the latest user response into the clarification state. Preserve answered points and carry every unresolved material gap forward until it is answered, explicitly superseded, no longer material to the intended next workflow, or assigned to that workflow as an open input. Surface contradictions with earlier information instead of choosing silently. When the latest response explicitly replaces an earlier condition and is unambiguous, record it as a correction rather than asking the user to confirm the same replacement again.
3. Identify gaps that could change the outcome, completion criteria, accepted scope, non-goals, constraints, environment, authority, external effects, risk, or verification feasibility. Resolve facts through safe read-only inspection when the target and inspection scope are already clear. Treat a gap as material at this stage only when the intended next workflow cannot resolve it within its authorized responsibility without inventing user intent, authority, or risk acceptance.
4. Classify each remaining gap:
   - **Blocking:** it could materially change the work or requires information, authorization, or risk acceptance that the agent cannot supply.
   - **Assumable:** it is low-impact, local, reversible, and supported by an established convention or available evidence.
   - **Irrelevant for now:** it does not affect the intended next workflow.
5. Before asking about a potentially blocking gap, check whether the intended next workflow can resolve it from authorized evidence and user-supplied decision criteria. If it can, retain the gap as an open input for that workflow and do not block clarification on it. Otherwise, ask only the questions needed to resolve the gap and explain briefly why each answer matters. Stop the affected downstream action, but do not stop unrelated safe discovery.
6. For assumable gaps, state the assumption, its basis, affected scope, and condition for revisiting it before proceeding. An assumption never substitutes for authorization or acceptance of a material risk.
7. After each user response, return to step 2. Do not treat completion of one question-and-answer round as completion of clarification. If an answer is partial, ask a narrower follow-up about the remaining material gap; do not repeat answered questions unchanged.
8. Finish only in one of these states:
   - **Ready:** the intended next workflow's entry conditions are satisfied, even if that workflow still has technical facts to investigate or design decisions to make within its authority.
   - **Proceed with assumptions:** only explicit low-impact assumptions remain.
   - **Blocked:** a material gap cannot be resolved safely because the user cannot answer, declines to decide, or required authority is unavailable.

## Decision criteria

- Do not impose a fixed number of questions, clarification turns, options, or assumptions. Continue only while another exchange can change readiness or safety.
- For `design-changes`, require a sufficiently confirmed outcome, success boundary, accepted scope and non-goals, material constraints, and authority to design. Leave implementation structure, affected files, vendor or dependency selection, detailed data mapping, and verification design open when resolving them is explicitly part of the design responsibility and the user has supplied the criteria needed to make those decisions.
- For direct `implement-changes`, require the implementation approach, authorized scope, exclusions, material risk decisions, and usable verification basis to be sufficiently settled; route unresolved design choices to `design-changes`.
- Offer options only when they accurately represent the material choices. Give a recommendation only when evidence, an established default, or explicit trade-offs support it.
- When a request contains multiple goals, determine whether they form one coherent outcome. Propose separation or ask for priority only when treating them together would change scope, sequencing, authorization, or reviewability.
- Do not reconcile apparently conflicting requirements by inventing phases, ordering, exceptions, or other connecting logic. Ask for reconciliation unless a later explicit answer clearly replaces the earlier condition.
- Do not question or restructure an already clear request unless the user explicitly asks for a structured handoff.
- If the user asks to proceed despite unresolved gaps, use assumptions only for the assumable class. Report a blocking gap as `Blocked`.

## Reporting contract

Adapt the response to the current state instead of emitting a fixed template.

When asking questions, include the unresolved point, why it affects the next action, the question, and any decision-relevant options or trade-offs. State which downstream action is waiting for the answer when that is not obvious.

When proceeding with assumptions, include each assumption, its basis, affected scope, and revisit condition.

When a structured handoff is requested or needed by the next workflow, include the confirmed intended outcome, material background or rationale needed to understand the request or evaluate downstream trade-offs, success or completion criteria, accepted scope, non-goals, constraints, assumptions, unresolved items or missing authority, and next action. After a multi-turn clarification reaches `Ready`, restate the confirmed information needed to make the handoff self-contained rather than reporting only what changed in the latest answer. Promote only user-supplied or authoritative information to confirmed requirements or background. Do not turn likely implementation consequences, generic best practices, or design possibilities into requirements, background, completion criteria, assumptions, or a selected method. Keep them as open inputs for the next workflow when material. Distinguish confirmed information from inference and omit empty fields.

For `Blocked`, state the unresolved material gap, what evidence or decision is missing, what remains unchanged, and what could unblock the request. Do not continue asking the same question without new information.

## Boundaries

- Use `design-changes` after the request is understood when implementation approach, affected boundaries, risks, or verification need design.
- Proceed directly to `implement-changes` only when the change is sufficiently clear, authorized, and low enough in uncertainty that a separate design handoff is unnecessary.
- Preserve targets and verification constraints supplied by the user or authoritative guidance, but do not invent or choose downstream implementation file boundaries, implementation approaches, or verification strategies. Do not implement changes, review a diff, or treat clarification as approval for destructive or external actions.
- Keep the workflow useful without requiring another Skill. Name a downstream Skill only when it helps make the handoff explicit.
