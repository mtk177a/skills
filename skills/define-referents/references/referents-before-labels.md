# Referents Before Labels

Use this rule to decide whether a proposed term is grounded enough to enter a document, design, or identifier set.

## Core rule

Describe what is being referred to, why it matters, which semantic role it has, and where it sits in the reasoning sequence before assigning a label. A plausible label is not evidence that these decisions are settled.

## Terms

- **Referent**: The concrete condition, state, occurrence, value, record, objective, or action that a term points to.
- **Semantic role**: The function the referent has in the current explanation or design.
- **Working label**: A compact phrase that hides an unsettled purpose, referent, decision, or sequence behind an abstract noun or verb.
- **First-use definition**: A sentence that states precisely what a newly introduced term points to.

## Role criteria

| Role | Use it for |
| --- | --- |
| `start condition` | A predicate that determines when an action may begin |
| `state` | A condition that remains true over an interval |
| `event` | An occurrence at a point or transition |
| `value` | A scalar, measurement, threshold, or calculated result |
| `record` | Stored evidence, observations, logs, or structured results |
| `purpose` | The outcome the work is intended to achieve |
| `means` | An action or mechanism used to achieve a purpose |

Do not merge roles because they occur near each other. A threshold value, the condition that compares against it, and the event triggered by that condition require separate rows even when a previous document used one phrase for all three.

## Decision rules

1. Replace a working label with a concrete sentence when its referent cannot be stated without alternatives such as “condition or event.”
2. Preserve the source sequence. Recording results is not the purpose when the purpose is to isolate a cause; it is a means that occurs before the isolation decision.
3. Prefer the user's terms and established domain terms. Introduce a new term only when it shortens repeated concrete wording without changing its boundaries.
4. Keep uncertainty explicit. Do not turn an unknown cause into a named component merely to make a plan sound complete.
5. Use different identifiers across prose and code only when their mapping remains explicit and one-to-one.

## Validation checks

- Hide the candidate-term column. The remaining cells must still identify each referent and its place in the sequence.
- Read every candidate term alone. It must not truthfully name another row with a different role.
- Compare the approved table with the body. Every central new term and identifier must trace to one row.
- Search headings and conclusions for abstract work labels. Replace any label that cannot trace to a row with a concrete sentence.

## Source and adaptation

This independently authored rule is informed by Yuichi Uemura's article [“codexの独自用語乱立･曖昧問題への対策”](https://zenn.dev/u1/articles/codex-referent-before-label). The article calls the related workflow `semantic-generation`. No article or embedded Skill text is copied verbatim here.
