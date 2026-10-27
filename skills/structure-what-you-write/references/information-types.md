# Information types and semantic units

Use this reference to identify what each piece of information does, before you select headings, lists, tables, or prose.\
The types below are practical aids for writing, based on information typing.\
They can overlap, and a piece of information can have more than one type.\
Classify by the question and the use of the reader, not by keywords or grammatical form.

## Identify the information unit

For each possible unit, identify these properties:

- **Subject**: the entity, event, condition, or question that it describes
- **Function**: whether it defines, reports, constrains, instructs, decides, compares, or illustrates
- **Reader use**: what the reader must understand, look up, decide, or do with it
- **Relationship**: whether it is a peer, an example, an exception, a prerequisite, a consequence, or a child of another unit
- **Authority**: whether it is a verified observation, a stated requirement or decision, a proposal, an inference, or an unknown

One sentence can contain several units, and several sentences can form one unit.\
Find the boundaries of units from their meaning.\
Punctuation, line breaks in the source, and current list items can differ from those boundaries.

## Practical types

| Type | Question of the reader | Natural organization | Typical failure |
| --- | --- | --- | --- |
| Concept or definition | What is it? | Name, distinguishing meaning, relationships | A definition mixed with unrelated operating rules |
| Fact or observation | What is known, or what happened? | Claim with its source, context, and time or scope | Assumptions presented as verified facts |
| Attributes and allowed values | What fields, options, or properties exist? | One entity or field with consistent attributes and values | Two different schemas hidden in one list |
| Principle or constraint | What must, may, or must not happen? | Rule, scope, governing condition, exceptions | Permissions listed without their conditions |
| Decision rule | Which choice is appropriate under which condition? | Mapping from condition to action or result | A condition separated from the action that it governs |
| Procedure | Which steps achieve the result? | Preconditions, ordered steps, checks | A check separated from the step that it validates |
| Process or state model | How does a system progress or behave? | States, transitions, triggers, results | A description of flow confused with instructions to act |
| Comparison or trade-off | How do the options differ? | Shared criteria with comparable evidence | Different criteria for different options |
| Example or counterexample | How does a rule apply? | Next to the rule, with an interpretation | An illustration treated as a general rule |
| Reported status or result | What changed, or what was verified? | Result, evidence, remaining work, uncertainty | Attempted work mixed with verified completion |

One block can use more than one type when the types answer the same question of the reader together.\
Separate the types when their independent purposes make the reader search through unrelated information.

## Classify the evidence separately from the type

A definition, a procedure, or a report can be verified, proposed, inferred, or unknown.\
The type describes the role of the information.\
The evidence state describes whether you can assert it as a fact or a requirement.

| Evidence or authority state | Treatment in writing |
| --- | --- |
| Verified observation | State the observation, with its source, scope, and time when they matter |
| Authorized requirement or decision | State it as a rule only within the scope of the authority that set it |
| Proposal | Label it as a recommendation or an option that waits for a decision |
| Inference | Label it as an interpretation, separate from observed facts |
| Unknown or conflicting | State the uncertainty and its effect, and leave the answer open |

For example, source code can show which branch is implemented now.\
It cannot alone show why a business policy was chosen, or that the behavior is a contractual requirement.\
When you edit supplied text faithfully, keep its claims and qualifications, unless verification or a revision of content is authorized.

## Group definitions around the thing defined

To describe a configurable field, cover these items:

- the name and the purpose of the field
- the type and the allowed values of the field
- the meaning of each value, and the criteria to choose it
- the meaning of unset, absent, empty, unknown, and explicit no-action values, when they apply
- combinations, precedence, and invalid states, when they apply
- the rules to read or change the field, only as far as the task of the reader needs
- an example, when the definitions alone leave an important ambiguity

The list helps you check coverage.\
It is not a set of required headings for every field.\
A definition can need only two sentences when it has no choices or exceptions.

### Decide whether fields share a table

Use one table when the reader compares several fields on a small, stable set of shared attributes.\
Use separate labeled blocks or tables when the reader must examine all values, cases, and exceptions of each field separately.\
Group fields by the task of the reader, not by a shared data type.\
Keep a useful comparison in one table, even when it contains several named fields.

### Model missing and explicit-none states precisely

An empty value, a value that nobody assessed, and an explicitly selected `None` can be different states.\
Record the meanings that the source actually defines.\
Some systems do not support or distinguish all three states.\
If `None` is a permitted value, document it with the other permitted values.\
Explain it separately only for a concrete reason.\
Keep each combination constraint next to the values that it constrains.

## Keep rules and examples separate

A rule describes a condition that applies across cases.\
An example shows one case under that rule.\
A counterexample shows why a tempting grouping or presentation fails.

Keep the details of an example as details of that example, not as required steps or general constraints.\
For example, an example that shows `Review` and `Decide` together does not require that they are always selected together.\
When several examples are necessary, give each example its own unit, not a chain of cases in a dense paragraph.

## Process and procedure

A **process** describes what happens: events, actors, state changes, dependencies, or conditions.\
A **procedure** tells someone what to do: steps, prerequisites, checks, and recovery.\
One workflow can need both.\
Give explicit instructions when the reader must act, even when a flowchart describes the same flow.

## Sources

- [Information Mapping: Information types](https://support.informationmapping.com/hc/en-us/articles/213446789-Present-your-information-in-a-clear-and-consistent-way)
- [OASIS DITA 2.0: Information typing](https://dita-lang.org/2.0/dita/archspec/base/information-typing)
- [OASIS DITA 2.0: Topics](https://dita-lang.org/2.0/dita/archspec/base/topicdefined)
