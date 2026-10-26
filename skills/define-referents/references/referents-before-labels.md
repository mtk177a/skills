# Referents Before Labels

Use this guide for the semantic decisions of the Skill: what a term refers to, which role it has, and whether a proposed term is grounded enough to use.\
`SKILL.md` gives the steps, the table formats, and the output.

## Core rule

Before you assign a label, state these items:

- what the term refers to
- why it matters
- its semantic role in the current reasoning
- its place in the relevant relationships
- what is still uncertain

A plausible label is not evidence that these items are settled.

## Terms

- **Referent**: the concrete thing, condition, occurrence, value, record, objective, action, rule, boundary, or other subject that a term points to.
- **Semantic role**: the function of a referent in the current explanation or design.\
  The same referent can have another role in other reasoning.
- **Working label**: a short phrase that hides an unsettled purpose, referent, decision, relationship, or sequence.
- **First-use definition**: a sentence that states exactly what a new term points to.

## Common roles

These roles cover recurring failures.\
Use another precise role when the reasoning needs it.

| Role | Use it for |
| --- | --- |
| `start condition` | A predicate that decides when an action can begin |
| `state` | A condition that stays true over an interval |
| `event` | An occurrence at a point or a transition |
| `value` | A scalar, a measurement, a threshold, or a calculated result |
| `record` | Stored evidence, observations, logs, or structured results |
| `purpose` | The result that the work must achieve |
| `means` | An action or a mechanism that achieves a purpose |

Other roles include an actor, an entity, a component, an interface, an artifact, a constraint, a policy, and an ownership boundary.\
Define a role in plain language when its meaning is not obvious.

Give each role its own row, even when the roles occur near each other.\
For example, a threshold value, the condition that compares against it, and the event that the condition starts need three rows.\
Keep one row for one component, even when the component has several relationships.

## Decision rules

1. Replace a working label with a concrete sentence when it needs open alternatives, such as "condition or event".
2. Keep the order of the source.\
   For example, when the purpose is to isolate a cause, recording results is a means that comes before the isolation decision, not the purpose.
3. Use the terms of the user and established domain terms first.\
   Introduce a new term only when it shortens repeated concrete wording without a change to its boundaries.
4. Keep uncertainty visible.\
   An unknown cause stays unknown, even when a named component would make a plan sound complete.
5. Use different identifiers in prose and in code only when their mapping stays explicit and one-to-one.

## Source

This guide is an independent summary.\
It is informed by the article of Yuichi Uemura, [“codexの独自用語乱立･曖昧問題への対策”](https://zenn.dev/u1/articles/codex-referent-before-label), which calls the related workflow `semantic-generation`.\
It contains no text copied from the article or from its embedded Skill.

The split into grounding and naming, the conditional decisions of the user, and the handoff to the originating work are local adaptations.\
This guide contains everything that the Skill needs, so read this guide, not the article.
