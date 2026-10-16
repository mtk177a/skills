# Information types and semantic units

Use this reference to identify what each piece of information does before selecting headings, lists, tables, or prose.
The categories below are practical writing aids inspired by information typing; they are not a mandatory or mutually exclusive ontology.
Classify by the reader's question and use, not by keyword or grammatical form alone.

## Identify the information unit

For each candidate unit, determine:

- **Subject:** What entity, event, condition, or question does this describe?
- **Function:** Is it defining, reporting, constraining, instructing, deciding, comparing, or illustrating?
- **Reader use:** What must the reader understand, look up, decide, or do with it?
- **Relationship:** Is it a peer, example, exception, prerequisite, consequence, or child of another unit?
- **Authority:** Is it a verified observation, a stated requirement or decision, a proposal, an inference, or an unknown?

A sentence can contain several units, while several sentences can form one coherent unit.
Do not treat punctuation, source line breaks, or current list items as semantic boundaries.

## Practical types

| Type | Reader question | Natural organization | Typical failure |
| --- | --- | --- | --- |
| Concept or definition | What is it? | Name, distinguishing meaning, relationships | Mixing a definition with unrelated operating rules |
| Fact or observation | What is known or happened? | Claim with source, relevant context, time or scope | Presenting assumptions as verified facts |
| Attributes and allowed values | What fields, options, or properties exist? | One entity or field with consistent attributes and values | Hiding two distinct schemas in one undifferentiated list |
| Principle or constraint | What must, may, or must not happen? | Rule, scope, governing condition, exceptions | Listing permissions without their conditions |
| Decision rule | Under which condition is which choice appropriate? | Condition-to-action or condition-to-outcome mapping | Separating a condition from the action it governs |
| Procedure | What steps achieve the result? | Preconditions, ordered steps, checks | Detaching a check from the step it validates |
| Process or state model | How does a system progress or behave? | States, transitions, triggers, outcomes | Confusing descriptive flow with instructions to act |
| Comparison or trade-off | How do options differ? | Shared criteria with comparable evidence | Using inconsistent criteria across options |
| Example or counterexample | How does a rule apply? | Adjacent to rule, with interpretation | Treating an illustration as a universal rule |
| Reported status or result | What has changed or been verified? | Result, evidence, remaining work, uncertainty | Mixing attempted work with verified completion |

One block can use more than one type when the types jointly answer the same reader question.
Separate them when their independent purposes cause the reader to search through unrelated information.

## Classify evidence separately from information type

A definition, procedure, or report can be verified, proposed, inferred, or unknown.
The type describes the role of the information; the evidence state describes whether it can be asserted as fact or requirement.

| Evidence or authority state | Treatment in writing |
| --- | --- |
| Verified observation | State the observation with applicable source, scope, and time where material |
| Authorized requirement or decision | State as normative only within the scope of the authority that established it |
| Proposal | Label as a recommendation or option awaiting a decision |
| Inference | Identify it as interpretation; do not promote it to observed fact |
| Unknown or conflicting | Specify the uncertainty and its effect instead of inventing an answer |

For example, source code can establish a currently implemented branch, but cannot by itself prove why a business policy was chosen or that the behavior is a contractual requirement.
When editing supplied text faithfully, preserve its claims and qualification unless verification or content revision is authorized.

## Group definitions around the thing defined

When describing a configurable field, a useful information contract is:

- Field name and purpose.
- Field type and allowed values.
- Meaning and choice criteria for each value.
- Meaning of unset, absent, empty, unknown, and explicit no-action values, if applicable.
- Combinations, precedence, and invalid states where applicable.
- Rules for reading or changing the field, only to the degree the reader's task requires.
- An example when the definitions alone leave a consequential ambiguity.

The list is a coverage aid, not a required set of headings for every field.
A definition may need only two sentences if no choices or exceptions exist.

### Decide whether fields share a table

Use one table when comparing multiple fields on a small, stable set of shared attributes is the reader's task.
Use separate labeled blocks or tables when the reader needs to inspect each field's complete set of values, cases, and exceptions independently.
Do not group two fields merely because they happen to share a data type.
Do not split a genuinely useful comparison solely because it contains multiple named fields.

### Model missing and explicit-none states precisely

An empty value, an unassessed value, and an explicitly selected `None` may represent different states.
Record the meanings actually defined by the source, and avoid assuming that every system supports or distinguishes all three.
If a permitted value is `None`, document it alongside the other permitted values unless there is a concrete reason for a separate explanation.
Keep combination constraints adjacent to the values they constrain.

## Keep rules and examples distinguishable

A rule describes a condition that applies across cases.
An example illustrates one case under that rule.
A counterexample shows why a tempting grouping or presentation fails.

Do not turn details incidental to an example into a required step or general constraint.
For example, showing `Review` and `Decide` together does not imply that they must always be selected together.
When multiple examples are needed, give each example its own discernible unit rather than embedding a chain of cases in a dense paragraph.

## Process versus procedure

A **process** describes what happens: events, actors, state changes, dependencies, or conditions.
A **procedure** tells someone what to do: actionable steps, prerequisites, checks, and recovery.
The same workflow may warrant both, but do not make a descriptive flowchart substitute for explicit executable instructions.

## Sources

- [Information Mapping: Information types](https://support.informationmapping.com/hc/en-us/articles/213446789-Present-your-information-in-a-clear-and-consistent-way)
- [OASIS DITA 2.0: Information typing](https://dita-lang.org/2.0/dita/archspec/base/information-typing)
- [OASIS DITA 2.0: Topics](https://dita-lang.org/2.0/dita/archspec/base/topicdefined)
