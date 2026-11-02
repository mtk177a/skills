# Worked examples and counterexamples

Use these examples to reason about unclear structural choices, not as a fixed format to copy.\
Each example separates the symptom, the underlying information problem, one reasonable improvement, and the conditions that would change the choice.\
All examples are fictional, and they show writing decisions, not the configuration of a real project.

## 1. Present independent records as peers

**Problem**: six independently named views are in two bullets of three, with a check instruction as a third peer.

**Before:**

````markdown
### Project views

- Overview, My queue, Agent queue.
- Waiting, Unclassified A, Unclassified B.
- Confirm the filters and displayed columns before use.
````

**Diagnosis**: the first two items are records, and the third is an instruction.\
The groups of three have no meaningful axis of classification.\
The heading also suggests that the list contains all project views, which may be false.

**One improvement:**

````markdown
### Views used by this task

#### View list

| View | Filter | Purpose |
| --- | --- | --- |
| Overview | `is:open` | Inspect open items |
| My queue | `is:open user-action:required` | Inspect user actions |
| Agent queue | `is:open agent-action:required` | Inspect agent actions |
| Waiting | `is:open status:Pending` | Inspect waiting items |
| Unclassified A | `is:open no:user-action` | Inspect items with no user classification |
| Unclassified B | `is:open no:agent-action` | Inspect items with no agent classification |

#### Checks when using these views

- Verify the active filter for each view.
- Verify the fields needed for this task are displayed.
````

**The choice changes when**: the reader needs only the six names.\
Then six bullets can be simpler than a table.\
If the six views have two real functional categories, name those categories, and group by them, not by count.

## 2. Make a shared parent topic explicit

**Problem**: two related subtopics appear as independent sections.

**Before:**

````markdown
### View list

[View records]

### View checks

[Checks]
````

**Diagnosis**: the headings are peers in the syntax, but both belong to the same topic of the task.

**One improvement:**

````markdown
### Views used by this task

#### View list

[View records]

#### Checks when using these views

[Checks]
````

**The choice changes when**: an existing parent heading already covers these two topics.\
Then that heading is sufficient, and no new parent is necessary.\
The levels `h3` and `h4` are examples.\
Use the levels that fit the surrounding document.

## 3. Separate different information functions inside one section

**Problem**: a section titled "State and completion" contains a status table, a paragraph about observed work, a completion table, and a paragraph about PR evidence.\
It does not show where one function ends and the next starts.

**Diagnosis**: state definitions, rules to interpret progress, and completion criteria answer related, but different, questions.

**One improvement:**

````markdown
### Case assessment

#### Status values

| Status | Meaning |
| --- | --- |
| `Todo` | Work is accepted but not started |
| `In Progress` | Actual work is underway |
| `Pending` | Progress is blocked by a known condition |
| `Done` | Agreed completion conditions are verified |

#### Interpreting progress

- Use observed work, not merely an updated timestamp, as evidence of progress.
- Record the blocking condition before marking an item as pending.

#### Completion criteria

| Item | Evidence for completion |
| --- | --- |
| Issue | All agreed acceptance conditions are satisfied |
| PR | The agreed code change has been merged, if merge is the intended outcome |

A merged PR does not by itself establish that deployment or all related Issue requirements are complete.
````

**The choice changes when**: the document is a very short sheet to look up status.\
Then one combined table or a compact subsection can be sufficient.\
Take status transitions and completion conditions from an authoritative source.

## 4. Define independent fields separately when the task is lookup

**Problem**: two different multi-select fields are in one table only because both are multi-selects.\
Their special values and examples are in prose far below the table.

**One improvement:**

````markdown
### Current actions

#### Reviewer actions

| Value | Use when | Clear when |
| --- | --- | --- |
| `Decide` | A decision is required | The decision is recorded or no longer required |
| `Review` | An existing result needs review | The review is completed or unnecessary |
| `None` | No action is needed after assessment | A new action is needed |

#### Worker actions

| Value | Use when | Clear when |
| --- | --- | --- |
| `Research` | Evidence must be gathered | The needed evidence is obtained or no longer required |
| `Verify` | A result needs verification | Verification is completed or unnecessary |
| `None` | No action is needed after assessment | A new action is needed |

#### Shared interpretation

- An unset field means not yet assessed, if the system defines it that way.
- An explicit `None` means assessed with no current action, if the system defines it that way.
- Use `None` alone, when `None` and the other actions are mutually exclusive.
- Example: A prepared proposal may require `Review` without requiring `Research`.
````

**Diagnosis**: each field is a separate reference entity.\
Its repeated values and selection rules need local, comparable definitions.

**The choice changes when**: the actual task of the reader is to compare the fields on a shared criterion, or their values and conditions form one domain on purpose.\
Then one table can be better.\
Take the meaning of unset and `None` from the actual system, not from the name.

## 5. Turn long inline lists into items that the reader can check

**Before:**

````text
Before generating the report, inspect the title, status, category, repository, assignee, target date, deadline, update time, and linked artifact.
````

**Diagnosis**: the field names are independent targets of a check.\
In a long inline list, a missing item is harder to see during execution.

**One improvement:**

````markdown
Before generating the report, inspect these fields for each relevant item:

- `Title`
- `Status`
- `Category`
- `Repository`
- `Assignee`
- `Target date`
- `Deadline`
- `Updated`
- `Linked artifact`
````

**The choice changes when**: the list is very short and incidental, such as "Check the title and status".\
Then the prose stays natural.\
This is a decision about usability, not a rule that each field needs its own bullet.

## 6. Attach checks and details to the correct step

**Before:**

````markdown
1. Read the item and update it.
2. Report the result.

### Verification

Read the latest item before writing, then read it again after writing.
````

**Diagnosis**: one of the verification activities is a prerequisite of the change, and the other checks the result afterward.\
The separate heading hides their order and their relationship.

**One improvement:**

````markdown
1. **Inspect the current item**

   - Read the latest state immediately before editing.
   - Check for changes made by someone else.

2. **Apply the authorized update**

   - Change only the intended fields.

3. **Verify the update**

   - Re-read the saved item.
   - Confirm the intended change and preservation of other fields.

4. **Report the result**

   - Distinguish verified success, partial success, and unverified outcomes.
````

**The choice changes when**: a shared verification procedure has its own maintained purpose, and the executing reader can always reach it.\
Then it can live elsewhere.\
For an independent instruction that cannot retrieve the referenced procedure, keep the essential checks in the instruction.

## 7. Show a required output form directly

**Before:**

````text
Produce a report with results first, then decisions, then remaining work, and for each decision include the reason and question, but leave out empty parts.
````

**One improvement:**

````markdown
Use the following order and omit sections with no material content:

```text
Results
- <verified result and evidence>

Decisions needed
- <decision, recommendation, reason, and requested answer>

Remaining work
- <next action, owner, blocker if any>
```
````

**Diagnosis**: the reader can reproduce and verify the intended structure more easily when it is shown directly.

**The choice changes when**: the user asked for only a short answer in natural language, and no stable report shape is necessary.\
Then an exact template adds needless rigidity.\
For output that a machine reads, give an actual schema instead of this illustrative sample.

## 8. Put rules for maintainers in the document for maintainers

**Problem**: an independent scheduled task contains a long statement about why unrelated agent clients do not inherit the permissions of the task.\
The statement is true, but it adds no instruction that the executing task needs to stay within its own approved operations.

**Candidate organization:**

````text
Maintenance README
- Explains which task bodies are registered, who maintains them, and why editing a stored draft does not grant execution authority.

Standalone task body
- States what this task is authorized to read, change, or report, including essential denials and exception behavior.
````

**Diagnosis**: the governance of the repository and the actual permission boundary of the executing agent serve different readers.

**The choice changes when**: the task runs without the README, and the statement is necessary to prevent an unsafe action.\
Then keep the necessary operational rule in the task body.\
Keep each safety constraint where the executing agent needs it, even when a related explanation exists elsewhere.

## 9. Keep a short message short

**Input:**

````text
The requested review is complete. The test result is linked in the PR, but deployment has not been verified yet.
````

**Poor transformation:**

````markdown
## Overview

The requested review is complete.

## Verification

The test result is linked in the PR.

## Limitations

Deployment has not been verified yet.
````

**Better choice**: keep the original two sentences in one short message.\
They give a result, the location of the evidence, and an important qualification, without a document of several sections.

**The choice changes when**: a recurring report has several independent results or fields for later use.\
Then stable labels or a template can help.

## 10. Split a document only when the split helps the reader

**Situation**: an independent agent task contains an objective, a table of accepted values, ordered execution steps, and a failure path.

**Overzealous restructuring**: move the values and the failure handling into two separate reference files, so that each file has "one information type".

**Better choice**: keep the required information in the independent task when the task cannot reliably load other files when it runs.\
Use nested sections to separate definitions, steps, and exceptions, and keep the task self-contained.

**The choice changes when**: the execution environment guarantees that dependencies load.\
Then a maintained external reference can prevent conflicting copies.\
Verify that guarantee before you rely on it.

## 11. Separate a source-of-truth move from an unauthorized edit

**Situation**: a README has a copied list of configuration options, and the validated schema is in a separate generated reference.

**Structural recommendation**: keep a short description and a descriptive link in the README.\
Manage the exact values in the schema or the generated reference.

**Permission boundary**: if the request authorizes only a review of the README, report the recommended change across files.\
Keep the other file and the configuration schema unchanged.

**The choice changes when**: a quick onboarding or an offline workflow needs a small, stable excerpt, and the risk of divergence is handled.\
Then the excerpt can be justified.

## 12. Turn cases in prose into a table of conditions and results

**Problem**: the result of a nightly job depends on two counts, and the section explains the cases in sentences.

**Before:**

````markdown
If no rows qualify and the job writes no output, the job succeeds and removes the old rows for that day.
The job treats a day on which it excludes all rows in the same way.
The job fails before the update if it writes no output for qualified rows, or if it writes output when no rows qualify.
````

**Diagnosis**: the reader must combine two conditions in four cases, but the sentences give the cases in a different order.\
The second sentence is an exception that the reader must map back to the first case.

**One improvement:**

````markdown
| Qualified rows | Output rows | Result |
| --- | --- | --- |
| 0 (including days on which all rows are excluded) | 0 | Succeeds, and removes the old rows for that day |
| 1 or more | 0 | Fails before the update |
| 0 | 1 or more | Fails before the update |
| 1 or more | 1 or more | Runs the other output checks, and saves the rows |
````

**The choice changes when**: only one condition decides the result.\
Then one conditional sentence is clearer than a table.

## 13. Separate the topics of a section with labels

**Problem**: an "Output" section has a table of columns, then sentences about checks before the save, then a sentence about identifiers, then sentences about reruns.\
Only blank lines separate these topics.

**Diagnosis**: the section answers three questions: what the job saves, which results it rejects, and what a rerun changes.\
The sentence about identifiers belongs to the rerun behavior, but it is between the table and the checks.

**One improvement:**

````markdown
## Output

**Saved columns**

| Column | Content |
| --- | --- |
| `id` | Identifier of the row |
| `day` | Target day |
| `count` | Number of qualified rows |

**Checks before the save**

- Each `day` equals the target day.
- Each `count` is 0 or more.

**Reruns**

- A rerun replaces all rows of the target day, and keeps the rows of other days.
- A rerun creates new values of `id`.
````

**The choice changes when**: a topic needs several paragraphs or its own subsections.\
Then give it a heading at the next level.

## 14. Use the identifier of the object that the reader works with

**Problem**: a document about data sources calls the tables "orders", "customer data", and "access history".\
The reader writes queries against `shop_orders`, `customers`, and `web_access_logs`.

**Diagnosis**: the labels are readable, but the reader must map each label to a table before using the document.\
A label such as "input" also does not say which object it refers to.

**One improvement:** use the table names in headings and table rows, and add a short plain-language label where it helps.

````markdown
### `shop_orders` (orders)

One row for each order.
````

**The choice changes when**: the reader does not work with the identifiers, for example in a summary for managers.\
Then the plain-language name can be sufficient.

## Review questions for each example

Before you copy a pattern, ask these questions:

- Which task of the reader made this structure appropriate?
- What did each row, column, bullet, heading, or file represent?
- Which relationship did the improvement show?
- Which details are facts of the example, and not general rules?
- Which change of the task, scope, medium, or execution environment would reverse the decision?
