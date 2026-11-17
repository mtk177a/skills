# Presentation patterns for structured writing

Use this reference after you identify the information units and their relationships.\
Choose the form from what the reader must inspect, compare, understand, or do.\
The rendering, accessibility, and editorial conventions of the target medium also apply.

## Select the form

| Form | Use when | Use another form when |
| --- | --- | --- |
| Prose paragraph | You explain one coherent subject, reason, condition, or cause | Several independent items or steps are hidden in a dense sentence |
| Bulleted list | You show unordered peers, choices, checks, or short points | The items differ in category, or each needs a long separate discussion |
| Numbered list | You show ordered actions or a real ranked sequence | The order is arbitrary, and numbers would suggest a false progression |
| Nested list | You show a parent item with its details or checks | The nesting is only decorative, inconsistent, or deeper than the relationships |
| Table | You compare entities on the same dimensions, or define repeated attributes or pairs of condition and result | The cells contain unrelated long text, the items share no dimensions, or a table of one column only saves space |
| Code block | You show exact syntax, a literal command, configuration, expected output, or a reusable output structure | The content is a normal statement or a conceptual relationship |
| Diagram | You show a hierarchy, sequence, system boundary, dependency, or flow that a picture makes clearer | The diagram only repeats a short list, or hides labels that the reader needs |

For a small set of pairs of a term and a definition, a definition list or labeled bullets can be clearer than a table.\
Choose a form for its fit to the information, not for how structured it looks.

## Prose and paragraphs

Give each paragraph one coherent subject that you can summarize without unrelated topics.\
A paragraph can have several sentences when they develop the same claim, explanation, or exception.\
Start a new paragraph at a real change of subject or function, not after a fixed number of sentences.\
Keep a rule near its condition and its reason when the reader needs them together.\
Keep each sentence free of hard line breaks.

### Lists inside sentences

A short list inside a sentence is suitable when each item is brief, and the reader does not examine the items separately.\
Use vertical bullets or a table when the items are long, repeated, or conditional.\
Also use them when the reader acts on or checks each item separately.

**Dense input:**

````text
Check the title, status, assignee, milestone, due date, category, priority, and last update for each item.
````

**More useful as a checklist when each check matters:**

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

The original sentence is still acceptable when the fields are only context, and need no separate verification.

## Bulleted lists and parallel items

Put one recognizable peer item in each bullet, and write parallel labels or actions when readers compare the items.\
A bullet can contain several related sentences and details.\
Give unrelated entities separate bullets, even when that makes the list longer.\
Keep one meaningful action together with the qualifications that the reader needs to do it safely.

**Poor grouping:**

````markdown
- Overview, Review queue, Waiting queue.
- Unassigned, Needs input, Archived.
- Verify the displayed fields before reading the queues.
````

The first two bullets bundle view names arbitrarily, and the third bullet contains an instruction, not a view.\
A useful presentation lists the six views as peers, or puts their repeated properties in a table.\
It then puts the check instruction separately.

## Numbered steps and their checks

Start each step with a clear action, so that readers can scan the sequence.\
Put prerequisite checks before the operation, and verification of the result after it.\
Use bullets below a step for several inputs, checks, or outputs of that step.\
When a step contains several paragraphs or code blocks, give each step its own heading, such as `### 2. Build the archive`.\
Keep the details and the checks of that step under its heading.

````markdown
1. **Inspect the current state**

   - Read the latest source record.
   - Identify concurrent edits and unresolved differences.

2. **Apply the approved change**

   - Change only the authorized fields.
   - Record the result of the operation.

3. **Verify the saved result**

   - Read the updated record again.
   - Compare it with the intended change and the preserved fields.
````

A large reusable topic can need a separate verification subsection.\
Keep the verification connected to the steps that it checks.\
Give a logically independent process its own section, not a place under an unrelated step.

## Tables: entity, dimension, and scope

Before you make a table, answer these questions:

1. What does one row represent?
2. What does one column represent?
3. Can each relevant row be read under the same headings?
4. Does the table serve lookup or comparison better than separate blocks?
5. Is the table short and narrow enough for the intended medium?

Use an identifying first column, and short, clear headings.\
Keep the categories and the definitions consistent across rows.\
Split a large table when separate tasks of the reader or independent entities become easier to understand.\
Keep a useful comparison in one table, even when each concept could have its own section.

### Repeated records

When each saved view has a name, a filter, and a use, the rows represent views, and the columns represent attributes.

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

A label such as "All project views" would be incorrect if the table covers only the views of this task.

### Independent field definitions

When the job is to document two different fields, separate field definitions can be more useful than one large table with an owner column.

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

This example is hypothetical.\
Verify the permitted values and the meaning of `None` in the actual system.\
If the real task is to compare the two schemas on common dimensions, one comparison table can be better.

## Conditions, exceptions, and state values

A table with a condition column and an action column works well when readers scan many alternatives.\
A short conditional sentence is often better for one simple condition.\
Values such as blank, unset, unknown, or `None` can have important operational differences.\
Then put their meanings and their valid combinations next to the definition of the field.\
Take their meanings from the source, and keep them in one place.

## Literal output structures

Use a fenced block when the reader or the agent must produce a recognizable, literal format.\
Show an exact output skeleton as a skeleton, not as a long paragraph.

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

The inner skeleton is an example, and empty sections stay out of the output.\
When a later machine reads the output, give a real schema or format contract, not an illustrative placeholder.

## Diagrams and other visuals

Use a diagram to show relationships that text or a table would show awkwardly.\
State whether an arrow means sequence, dependency, information flow, responsibility, or something else.\
An arrow means execution order or synchronization only when the diagram states it.\
Keep the essential labels and decisions in the text as well, because a diagram renderer may not be available.

## Accessibility and rendering

- Use descriptive headings and link text, not only visual cues.
- Use real table headers, and use tables for data, not for layout.
- Keep tables narrow for email, mobile chat, and narrow viewers.
- Keep a list of one column as a list, unless a two-dimensional relationship exists.
- Use code fences for literal values, not to imitate a table.
- Inspect the rendered Markdown when indentation, nested blocks, tables, or links can break.

## Sources

- [Google Technical Writing: Lists and tables](https://developers.google.com/tech-writing/one/lists-and-tables)
- [Google Developer Style Guide: Tables](https://developers.google.com/style/tables)
- [Google Technical Writing: Paragraphs](https://developers.google.com/tech-writing/one/paragraphs)
- [Google Style Guide: Paragraph structure](https://developers.google.com/style/paragraph-structure)
- [Microsoft Writing Style Guide: Lists](https://learn.microsoft.com/en-us/style-guide/scannable-content/lists)
- [Microsoft Writing Style Guide: Tables](https://learn.microsoft.com/en-us/style-guide/scannable-content/tables)
- [W3C WAI: Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/)
