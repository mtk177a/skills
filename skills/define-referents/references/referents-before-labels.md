# Referents Before Labels

Use this guide to decide whether a proposed term is grounded enough to enter a document, design, explanation, or identifier set.

## Core rule

Describe what is being referred to, why it matters, which semantic role it has in the current reasoning, where it sits in the relevant relationships, and what remains uncertain before assigning a label. A plausible label is not evidence that these decisions are settled.

## Terms

- **Referent**: The concrete thing, condition, occurrence, value, record, objective, action, rule, boundary, or other subject that a term points to.
- **Semantic role**: The function a referent has in the current explanation or design, not a universal classification of the referent.
- **Working label**: A compact phrase that hides an unsettled purpose, referent, decision, relationship, or sequence.
- **Grounding table**: The label-free record of referents, roles, relationships, evidence, and uncertainty.
- **Naming table**: The later mapping from grounded rows to established terms, proposals, or concrete wording.
- **First-use definition**: A sentence that states precisely what a newly introduced term points to.

## Common role distinctions

The following roles cover recurring failure patterns but do not form a closed taxonomy.

| Role | Use it for |
| --- | --- |
| `start condition` | A predicate that determines when an action may begin |
| `state` | A condition that remains true over an interval |
| `event` | An occurrence at a point or transition |
| `value` | A scalar, measurement, threshold, or calculated result |
| `record` | Stored evidence, observations, logs, or structured results |
| `purpose` | The outcome the work is intended to achieve |
| `means` | An action or mechanism used to achieve a purpose |

Use another precise role when the current reasoning depends on an actor, entity, component, interface, artifact, constraint, policy, ownership boundary, or other distinction. Define the role in plain language when its meaning is not obvious.

Do not merge roles merely because they occur near each other. A threshold value, the condition that compares against it, and the event triggered by that condition require separate rows. Conversely, do not split one component into several supposed referents merely because the same component participates in several relationships.

## Decision rules

1. Replace a working label with a concrete sentence when its referent cannot be stated without unresolved alternatives such as “condition or event.”
2. Preserve the source sequence. Recording results is not the purpose when the purpose is to isolate a cause; it is a means that occurs before the isolation decision.
3. Prefer the user's terms and established domain terms. Introduce a new term only when it shortens repeated concrete wording without changing its boundaries.
4. Keep uncertainty explicit. Do not turn an unknown cause into a named component merely to make a plan sound complete.
5. Use different identifiers across prose and code only when their mapping remains explicit and one-to-one.
6. Split tables at a real change in purpose or reasoning stage, not at a fixed number of rows.
7. Ask for a decision only when unresolved alternatives change a public contract, domain boundary, or another material meaning. A low-impact local term can proceed once its grounding is complete.

## Two-phase validation

Validate the Grounding table before producing any Naming table:

- Search the Grounding table for candidate labels or definitions that presuppose a term. Replace them with concrete descriptions.
- Confirm that every row identifies its referent and relationship without relying on another row's candidate term.
- Check the evidence state. Unknown or inferred content must not appear confirmed.
- Keep distinct referents or materially different roles in distinct rows.

Then validate the Naming table:

- Hide the entire Naming table. The Grounding table must still identify each referent and its place in the reasoning.
- Read every candidate term alone. It must not truthfully name another row whose distinction matters.
- Require a precise first-use definition for each new term.
- Mark a term as `concrete wording` when no proposed label preserves the grounded boundary.
- When a Grounding row changes, treat its dependent naming rows as invalid until regenerated.

## Handoff boundary

This workflow constrains terminology; it does not supply the evidence, design, prose, implementation, or verification required by the originating task. Return the completed mapping to that workflow. A direct naming request may end with the Naming table, but a broader task must resume under its original responsibility and authorization.

Return tables in the response unless the user explicitly authorizes a separate artifact. Do not create a sidecar merely because the target document may be written.

## Source and adaptation

This independently authored guide is informed by Yuichi Uemura's article [“codexの独自用語乱立･曖昧問題への対策”](https://zenn.dev/u1/articles/codex-referent-before-label). The article calls the related workflow `semantic-generation`. No article or embedded Skill text is copied verbatim here.

The local workflow uses an observable Grounding-then-Naming split, conditional user decisions, and an explicit handoff boundary. These are local adaptations and do not require fetching the article at runtime.
