# Information architecture across writing scales

Use this reference for problems with the boundaries, grouping, hierarchy, order, or placement of information.\
It also covers the division of information across artifacts.\
The goal is a structure that shows the relationships of the information and the work of the reader.\
Maximum subdivision and formal symmetry are not goals.

## Select the scale of the problem

Consider these nested scales, and check the larger scales as well as the smallest one:

| Scale | Structural decision | Typical symptom |
| --- | --- | --- |
| Statement | Which claims belong in one sentence or clause? | Independent claims hidden in a long sentence |
| Paragraph or list item | What is one coherent unit? | Several unrelated subjects in one bullet |
| Table or content block | Which entities share comparable properties? | A table that mixes unrelated definitions and instructions |
| Section or chapter | Which topics share a parent, and which are siblings? | Two subjects under one vague heading, or related subsections placed as unrelated peers |
| Single artifact | What belongs in this document or message, and in what order? | Missing context, repeated history, misplaced rules |
| Artifact collection | Which files own which information, and how are they connected? | Several sources of truth, too many jumps, or one oversized file for all purposes |

A failure in a paragraph can come from the structure of the whole document.\
Before you rewrite the paragraph, read enough of the surrounding material to find its correct parent and destination.\
A broader problem that you find is a reason to report it, and the editing scope stays as requested.

## Make a temporary information inventory

For complex content, identify the possible units and their relationships before you draft an outline.\
Keep this inventory as working material, outside the finished artifact.

| Field | Question |
| --- | --- |
| Unit | Which single subject, assertion, condition, action, or example does it represent? |
| Function | Is it a definition, fact, rule, condition, step, illustration, result, or context? |
| Need of the reader | Which question does it answer, or which action does it support? |
| Source | Where is the evidence or the authorized requirement? |
| Relationship | What is its parent, peer, prerequisite, exception, or consequence? |
| Destination | Where must readers find or retrieve it? |
| Status | Is it required, optional, redundant, unknown, or outside the scope? |

For a short writing task, keep the inventory in your working notes, not as a formal table.\
The inventory keeps you from an early commitment to the current layout.

## Determine meaningful units and groups

At the chosen level, a unit supports one coherent question or operation of the reader.\
Related sentences can stay together when they have different small functions, such as a rule, its reason, and its exception.\
Group sentences by their meaning, not by the line of the source on which they were written.

Check a proposed group with these questions:

1. Can you name the group without an artificial conjunction or a vague label?
2. Do its members answer the same parent question, or serve the same task of the reader?
3. Are the members peers, or does one explain, qualify, or depend on another?
4. Does the group reduce context switches and lookup effort, and keep the differences visible?
5. Must a reader examine this group as a unit?

If the answers do not support one coherent group, split or move it.\
If a split removes important context or needs repeated introductions, consider keeping the group together.

### Keep peers parallel

Choose one organizing axis for each group of peers: entities, operations, states, questions, time periods, responsibilities, or another meaningful dimension.\
Keep a list of entities and a rule for execution in separate lists.\
Group independent items only under groups that have real names and different purposes.\
Keep the granularity of peers comparable when that makes scanning and comparison easier.\
A necessary exception can be longer or more detailed, and keeps its distinction from the other items.

### Make containment explicit

If two subjects are both parts of a larger subject, add the meaningful parent when it helps navigation.\
For example, "Views used by this task" can contain "View list" and "Checks performed when reading views".\
Without their parent, two peer headings can suggest unrelated scopes.\
When a heading around them already shows the relationship clearly, that heading is sufficient.

### Name the actual scope

A heading is a promise about the section below it.\
Use names that state the subject, task, audience, or subset exactly.\
For example, a heading "Project views" can suggest completeness when the content covers only the six views of one workflow.\
A label that joins two concerns with "and" is a signal to examine the section.\
It does not prove that the section needs a split.\
Use a concrete heading instead of a generic heading such as "Details" or "Other".

## Order information by the needs of the reader

Choose an ordering principle that the reader can follow:

- Put orientation before specialized detail when the reader has no working model.
- Put the result and the prerequisites before the steps in a guide to follow.
- Put definitions near the values and rules that use them.
- Put conditions before the actions that they govern.
- Put comparison criteria before the comparison of alternatives.
- Put evidence near the claims that it supports.
- In a status report, put the result and its significance before the chronology.\
  When the chronology is the subject of the report, it comes first.
- Put exceptions next to the rule that they qualify, when they change the execution or the interpretation.

Choose the order for each medium.\
A short reply, a long tutorial, and a reference catalog have different patterns of reading and retrieval.

## Decide whether to keep, split, merge, or move

Evaluate the actual possible structures, including the current structure without change.

| Choice | Use when | Watch for |
| --- | --- | --- |
| Keep | One task of the reader, a coherent subject, easy retrieval | Mixed purposes hidden under a broad heading |
| Split a block or section | Different subjects or information types need independent access | Fragments, repeated context, separated exceptions |
| Merge blocks or sections | Separate pieces answer one question together, or repeat each other | Loss of meaningful distinctions |
| Move a passage | It belongs to another step, parent topic, audience, or source of truth | Broken context, references, or dependencies across documents |
| Split a file | Different jobs of the reader, ownership, lifecycle, audience, or large independent lookups | Too much navigation, broken links, loss of independent instructions |
| Merge files | Readers switch between them repeatedly for one coherent task, and separate maintenance has no benefit | Oversized files, coupled update cycles, mixed audiences |
| Link instead of copying | An authoritative detail is maintained elsewhere, and a link serves the reader | Broken links, offline execution, inaccessible dependencies |
| Copy essential context | Artifacts must work independently, or safe execution depends on local context | Conflicting copies after later updates |

### Compare meaningful alternatives

When the choice has important effects, compare the current structure and at least one plausible restructuring against these criteria:

- the tasks of the readers and the cost of navigation
- semantic cohesion and the separation of different purposes
- completeness, local context, and the needs of independent execution
- sources of truth and the ownership of updates
- the frequency of change and the likelihood of divergence
- references, anchors, permissions, and later dependencies
- the amount of change and the scope that the user authorized

Split a file for the reasons in the table, not because of its length alone.\
When the readers or the execution contexts need independent copies, keep the copies, even when they duplicate content.

## Distinguish information structure from storage structure

An information topic and a file are different units.\
One file can present several topics, and several source files can form one published document.\
Navigation and links can show relationships, so each conceptual boundary does not need to be a file boundary.

When several artifacts use the same information, identify its source of truth.\
Also check whether the other artifacts can reliably retrieve it.\
For an agent instruction that runs from an independent task body, a cross-reference that may not load can be insufficient.\
For a repository README, a direct link to a maintained API reference can be better than a copied reference table.

## Validate the architecture

Check these questions:

- Can readers answer the key questions through the headings or links, without a reconstruction of scattered fragments?
- Does each parent contain the subjects that its label promises, and only related peers?
- Do the list items and table rows use a defensible organizing axis?
- Are definitions, conditions, examples, and checks next to the information that they qualify?
- Can readers still reach each removed, moved, or combined item, and is it accurate?
- Do links, anchors, tables of contents, references, and other consumers still resolve after the moves?
- Are the source-of-truth facts in the right place, and are independent instructions still complete?
- Did the edit stay within the authorized scope, and keep the unaffected work?

If failures remain, review the semantic model and the possible parent structure again, before you change only the formatting.

## Sources

- [Google Technical Writing: Organizing large documents](https://developers.google.com/tech-writing/two/large-docs)
- [OASIS DITA 2.0: The topic as the basic unit of information](https://dita-lang.org/2.0/dita/archspec/base/topicdefined)
- [OASIS DITA 2.0: Definition of DITA maps](https://dita-lang.org/2.0/dita/archspec/base/definition-of-ditamaps)
- [W3C WAI: Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/)
- [Information Mapping: Maps and Blocks](https://support.informationmapping.com/hc/en-us/articles/213440709-Structure-your-content-using-Maps-and-Blocks)
