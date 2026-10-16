# Worked examples and counterexamples

Use these examples to reason about ambiguous structural choices, not to copy a fixed format into every task.
Each example separates the symptom, the underlying information problem, one reasonable improvement, and circumstances in which the choice would change.
All examples are fictional and illustrate writing decisions rather than actual project configuration.

## 1. Do not bundle independent records into arbitrary bullets

**Problem:** Six independently named views are distributed across two bullets of three, with a checking instruction as a third peer.

**Before:**

````markdown
### Project views

- Overview, My queue, Agent queue.
- Waiting, Unclassified A, Unclassified B.
- Confirm the filters and displayed columns before use.
````

**Diagnosis:** The first two items are records, but the third is an instruction; the groups of three lack a meaningful classification axis.
The heading also implies all project views are listed, which may not be true.

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

**Decision changes when:** If the reader only needs six names, six bullets may be simpler than a table.
If the six views have two real functional categories, name those categories rather than grouping them by count.

## 2. Make shared parent topics explicit

**Problem:** Two related subtopics appear as independent sections.

**Before:**

````markdown
### View list

[View records]

### View checks

[Checks]
````

**Diagnosis:** The headings are logical peers syntactically, but both belong to the same task-specific topic.

**One improvement:**

````markdown
### Views used by this task

#### View list

[View records]

#### Checks when using these views

[Checks]
````

**Decision changes when:** If an existing parent heading already covers these two topics, do not create a redundant additional parent.
The chosen `h3` and `h4` levels are illustrative; use levels appropriate to the surrounding document.

## 3. Separate different information functions inside one section

**Problem:** A section titled "State and completion" contains a status table, a paragraph about observing work, a completion table, and a paragraph about PR evidence without signaling the transitions.

**Diagnosis:** State definitions, rules for interpreting progress, and completion criteria answer related but distinguishable questions.

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

**Decision changes when:** If the document is an extremely short status lookup sheet, one combined table or compact subsection may suffice.
Do not invent status transitions or completion conditions absent an authoritative source.

## 4. Define independent fields independently when lookup is the task

**Problem:** Two distinct multi-select fields are shown in one table only because both are multi-selects; special values and examples are buried in prose far below the table.

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
- Do not combine `None` with another action when they are mutually exclusive.
- Example: A prepared proposal may require `Review` without requiring `Research`.
````

**Diagnosis:** Each field is a separate reference entity; their repeated values and selection rules deserve local, comparable definitions.

**Decision changes when:** A single table may be better if the actual reader task is to compare fields by a shared criterion, or if their values and conditions are intentionally modeled as one domain.
Do not infer the meaning of unset or `None` from the name; obtain that definition from the actual system.

## 5. Turn long inline inventories into inspectable items when needed

**Before:**

````text
Before generating the report, inspect the title, status, category, repository, assignee, target date, deadline, update time, and linked artifact.
````

**Diagnosis:** The field names are independent check targets, but a long inline list makes omissions harder to spot during execution.

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

**Decision changes when:** A very short incidental list, such as "Check the title and status," remains natural as prose.
This is a usability decision, not a rule that one field always requires one bullet.

## 6. Attach checks and details to the correct procedural step

**Before:**

````markdown
1. Read the item and update it.
2. Report the result.

### Verification

Read the latest item before writing, then read it again after writing.
````

**Diagnosis:** One of the "verification" activities is a prerequisite to changing data; the other checks the result afterward.
The separate heading hides their order and relationship.

**One improvement:**

````markdown
1. **Inspect the current item.**
   - Read the latest state immediately before editing.
   - Check for changes made by someone else.
2. **Apply the authorized update.**
   - Change only the intended fields.
3. **Verify the update.**
   - Re-read the saved item.
   - Confirm the intended change and preservation of other fields.
4. **Report the result.**
   - Distinguish verified success, partial success, and unverified outcomes.
````

**Decision changes when:** A shared verification procedure can live elsewhere if it has an independently maintained purpose and the executing reader is guaranteed access to it.
Do not detach essential checks from a standalone instruction that cannot retrieve the referenced procedure.

## 7. Show a required output form instead of describing its formatting indirectly

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

**Diagnosis:** The intended structure is easier to reproduce and verify when represented directly.

**Decision changes when:** If the user asked for only a short natural-language answer and no stable report shape is needed, an exact template may create needless rigidity.
For machine-readable output, specify an actual schema rather than this illustrative sample.

## 8. Put maintainer rules in the maintainer's document

**Problem:** A self-contained scheduled task includes a lengthy statement about why unrelated agent clients must not inherit the task's permissions.
The statement is true in context but adds no instruction the executing task needs in order to stay within its own approved operations.

**Candidate organization:**

````text
Maintenance README
- Explains which task bodies are registered, who maintains them, and why editing a stored draft does not grant execution authority.

Standalone task body
- States what this task is authorized to read, change, or report, including essential denials and exception behavior.
````

**Diagnosis:** Repository governance and an executing agent's actual permission boundary serve different readers.

**Decision changes when:** If the task runs without the README and the disputed statement is necessary to prevent an unsafe action, retain the necessary operational rule in the task body.
Do not remove safety constraints merely because a related explanation exists elsewhere.

## 9. Do not apply a document template to a short message

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

**Better choice:** Keep the original two sentences in the same short message.
They give a result, supporting location, and an important qualification without becoming a multi-section document.

**Decision changes when:** A recurring report with several independent results or downstream fields may warrant stable labels or a template.

## 10. Do not force a document split merely because topics differ

**Situation:** A standalone agent task contains an objective, a table of accepted values, ordered execution steps, and a failure path.

**Overzealous restructuring:** Move the values and failure handling into two separate reference files to make each file "one information type."

**Better choice:** Preserve the required information in the standalone task when it cannot reliably load companion files at execution time.
Use nested sections to distinguish definitions, steps, and exceptions while keeping the task self-contained.

**Decision changes when:** If the execution environment guarantees dependency loading, a maintained external reference may avoid conflicting copies.
Verify that guarantee rather than assuming it.

## 11. Distinguish an appropriate source-of-truth move from an unauthorized edit

**Situation:** A README has a duplicated list of configuration options and the actual validated schema lives in a separate generated reference.

**Structural recommendation:** Keep a short description and a descriptive link in the README, and manage the precise values at the schema or generated reference.

**Permission boundary:** If the request authorizes only a README review, report the recommended cross-file change but do not edit the other file or change the configuration schema.

**Decision changes when:** A small, stable excerpt may be justified for quick onboarding or an offline workflow if the risk of divergence is addressed.

## Review prompts for every example

Before copying a pattern, ask:

- Which reader task made this structure appropriate?
- What did each row, column, bullet, heading, or file represent?
- What relationship was exposed by the improvement?
- Which details are facts of the example rather than general rules?
- What change in reader task, scope, medium, or execution environment would reverse the decision?
