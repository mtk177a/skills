# Presentation patterns for structured writing

Use this reference after identifying information units and their relationships.
The choice of prose, list, table, code block, or diagram must follow what the reader needs to inspect, compare, understand, or perform.
The target medium's rendering, accessibility, and editorial conventions remain relevant.

## Select the form

| Form | Appropriate when | Avoid when |
| --- | --- | --- |
| Prose paragraph | Explaining one coherent subject, rationale, condition, or causal relationship | Multiple independent items or steps are buried in a dense sentence |
| Bulleted list | Showing unordered peers, choices, checks, or concise points | Items differ in category, or each requires a long separate discussion |
| Numbered list | Showing ordered actions or a genuinely ranked sequence | The order is arbitrary and numbering falsely implies progression |
| Nested list | Showing a parent item with its subordinate detail or checks | Nesting is decorative, inconsistent, or deeper than the relationships warrant |
| Table | Comparing entities by the same dimensions, defining repeated attributes or condition/outcome pairs | Cells contain unrelated essays, items lack shared dimensions, or one-column layout merely saves space |
| Code block | Showing exact syntax, a literal command, configuration, expected output, or a reusable output structure | A normal statement or conceptual relationship is being treated as literal syntax |
| Diagram | Showing a hierarchy, sequence, system boundary, dependency, or flow that benefits from visualization | The diagram merely repeats a short list or hides labels essential to comprehension |

For a small set of term/definition pairs, a definition list or labeled bullets may be clearer than a table.
A format is not intrinsically better because it appears more structured.

## Prose and paragraphs

Give each paragraph a coherent subject that can be summarized without mentioning unrelated topics.
A paragraph may have several sentences when the sentences develop the same claim, explanation, or exception.
Split at a genuine subject or function change, not at a predetermined sentence count.
Keep a rule near its qualifying condition and reason when they are needed together.
Avoid hard line breaks in the middle of a sentence.

### Embedded enumerations

A short inline list can be appropriate when each item is brief and the reader need not inspect the items separately.
Prefer vertical bullets or a table when the items are independently actionable, long, repeated, conditional, or likely to be checked one by one.

**Dense input:**

````text
Check the title, status, assignee, milestone, due date, category, priority, and last update for each item.
````

**More useful as an inspectable checklist when individual checks matter:**

````markdown
Check these fields for each item:

- `Title`
- `Status`
- `Assignee`
- `Milestone`
- `Due date`
- `Category`
- `Priority`
- `Last update`
````

The original sentence remains acceptable when the fields are incidental context and do not need individual verification.

## Bulleted lists and parallel items

Use one recognizable peer item per bullet, and write parallel labels or actions when readers compare items.
A bullet can contain several related sentences and subordinate details.
Do not force unrelated entities into a bullet just to reduce bullet count.
Do not split one meaningful action from the qualifications necessary to perform it safely.

**Poor grouping:**

````markdown
- Overview, Review queue, Waiting queue.
- Unassigned, Needs input, Archived.
- Verify the displayed fields before reading the queues.
````

The first two bullets contain arbitrarily bundled view names, while the third contains an instruction rather than a view.
A useful presentation would either list the six views as peers or place their repeated properties in a table, then separate the checking instruction.

## Numbered steps and subordinate checks

Give each step a clear action-oriented opening so readers can scan the sequence.
Keep prerequisite checks before the operation and result verification after it.
Use subordinate bullets for multiple inputs, checks, or outputs related to one step.

````markdown
1. **Inspect the current state.**
   - Read the latest source record.
   - Identify any concurrent edits and unresolved differences.
2. **Apply the approved change.**
   - Change only the authorized fields.
   - Record the operation's result.
3. **Verify the saved result.**
   - Read the updated record again.
   - Compare it with the intended change and preserved fields.
````

A verification subsection may be warranted for a large reusable topic, but do not detach it from the step sequence merely to create another heading.
Conversely, do not nest a logically independent process under an unrelated step solely to avoid a new section.

## Tables: entity, dimension, and scope

Before making a table, answer:

1. What does one row represent?
2. What does one column represent?
3. Can every relevant row be interpreted under the same headings?
4. Does the table serve lookup or comparison better than separate blocks?
5. Is the table short and narrow enough for the intended medium?

Use an identifying first column and concise, unambiguous headings.
Keep categories and definitions consistent across rows.
Split an unwieldy table if separate reader tasks or independent entities would be easier to understand.
Do not split a useful comparison merely to give every concept its own section.

### Repeated records

When each saved view has a name, filter, and use, the rows represent views and the columns represent attributes.

````markdown
### Views used for this task

| View | Filter | Purpose |
| --- | --- | --- |
| Overview | `is:open` | Find currently open items |
| Waiting | `status:Pending` | Inspect blocked or waiting items |
| Needs review | `review:required` | Inspect items requiring review |

#### Checks when reading these views

- Verify each view's current filter.
- Verify that its expected fields are visible.
````

A label such as "All project views" would be inaccurate if the table covers only the views used by this task.

### Independent field definitions

When the job is to document two distinct fields, separate field definitions can be more useful than adding an owner column to one large table.

````markdown
#### Human actions

| Value | Select when | Clear when |
| --- | --- | --- |
| `Decide` | A human decision is required | The decision has been made or is no longer required |
| `Review` | An existing deliverable needs review | Review is completed or no longer needed |
| `None` | The field was assessed and no human action is needed | A new action becomes necessary |

#### Agent actions

| Value | Select when | Clear when |
| --- | --- | --- |
| `Research` | Evidence is missing and investigation is needed | The needed evidence is obtained or no longer required |
| `Verify` | A result needs validation | Validation is completed or no longer required |
| `None` | The field was assessed and no agent action is needed | A new action becomes necessary |
````

This example is hypothetical; permitted values and the semantics of `None` must be verified for the actual system.
If the real task is to compare the two schemas by common dimensions, a unified comparison table may be preferable.

## Conditions, exceptions, and state values

A two-column condition/action table works well when readers scan many alternatives.
A short conditional sentence is often better for one simple condition.
When values such as blank, unset, unknown, or `None` have operationally important differences, place their meanings and valid combinations beside the relevant field definition.
Do not scatter them across unrelated paragraphs or silently infer their semantics.

## Literal output structures

Use a fenced block when the reader or agent needs to produce a recognizable, literal format.
Do not describe an exact output skeleton in a sprawling paragraph if showing the skeleton is clearer.

````markdown
### Report format

Use only sections with material content.

```text
Results
- <verified outcome and source>

Decisions needed
- <decision, recommendation, supporting reason, requested response>

Remaining work
- <owner, next step, blocker or uncertainty>
```
````

The inner skeleton is an example, not a requirement to fill empty sections.
Where a downstream machine consumes the output, provide a real schema or format contract rather than an illustrative placeholder.

## Diagrams and other visuals

Use a diagram to clarify relationships that text or a table would make awkward.
State whether an arrow means sequence, dependency, information flow, responsibility, or something else.
Do not imply execution order or synchronization merely because nodes are connected.
Keep the essential labels and decisions accessible in text, especially where the diagram renderer may be unavailable.

## Accessibility and rendering

- Prefer descriptive headings and link text to visual-only cues.
- Use genuine table headers and avoid tables for arbitrary layout.
- Avoid overly wide tables in email, mobile chat, and narrow viewers.
- Keep one-column lists as lists unless a two-dimensional relationship exists.
- Use real code fences for literal values, not to imitate the appearance of a table.
- Inspect rendered Markdown when indentation, nested blocks, tables, or links are likely to be fragile.

## Sources

- [Google Technical Writing: Lists and tables](https://developers.google.com/tech-writing/one/lists-and-tables)
- [Google Developer Style Guide: Tables](https://developers.google.com/style/tables)
- [Google Technical Writing: Paragraphs](https://developers.google.com/tech-writing/one/paragraphs)
- [Google Style Guide: Paragraph structure](https://developers.google.com/style/paragraph-structure)
- [Microsoft Writing Style Guide: Lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)
- [Microsoft Writing Style Guide: Tables](https://learn.microsoft.com/en-us/style-guide/scannable-content/tables)
- [W3C WAI: Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/)
