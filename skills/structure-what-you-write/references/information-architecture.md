# Information architecture across writing scales

Use this reference when the problem concerns information boundaries, grouping, hierarchy, ordering, placement, or the division of content across artifacts.
The objective is a structure that reflects the information's relationships and the reader's work, not maximal subdivision or formal symmetry.

## Select the scale of the problem

Consider these nested scales without presuming the smallest is sufficient:

| Scale | Structural decision | Typical symptom |
| --- | --- | --- |
| Statement | Which claims belong in one sentence or clause? | Independent claims obscured in a long sentence |
| Paragraph or list item | What is one coherent unit? | Multiple unrelated subjects in one bullet |
| Table or content block | Which entities share comparable properties? | A table mixing unrelated definitions and instructions |
| Section or chapter | Which topics share a parent and which are siblings? | Two subjects under one vague heading, or related subsections placed as unrelated peers |
| Single artifact | What belongs in this document or message, and in what order? | Missing context, duplicated history, misplaced rules |
| Artifact collection | Which files own which information, and how are they connected? | Multiple sources of truth, excessive jumps, or an oversized all-purpose file |

A failure visible in a paragraph can originate in the structure of the whole document.
Before rewriting the paragraph, inspect enough surrounding material to determine its appropriate parent and destination.
Do not expand the editing scope merely because a broader problem is discovered.

## Construct a temporary information inventory

For complex content, identify the candidate units and their relationships before drafting an outline.
Keep this inventory as working material rather than publishing it in the finished artifact.

| Field | Question |
| --- | --- |
| Unit | What single subject, assertion, condition, action, or example is represented? |
| Function | Is it definition, fact, rule, condition, step, illustration, result, or context? |
| Reader need | What question does it answer or action does it support? |
| Source | Where is the evidence or authorized requirement? |
| Relationship | What is its parent, peer, prerequisite, exception, or consequence? |
| Destination | Where should readers encounter or retrieve it? |
| Status | Is it required, optional, redundant, unknown, or outside scope? |

Do not reproduce this inventory as a rigid table in a short writing task.
It exists to prevent premature commitment to the current layout.

## Determine meaningful units and groupings

A unit should support one coherent reader question or operation at the chosen level.
Related sentences can stay together even if they perform different micro-functions, such as a rule followed by its reason and exception.
Two adjacent sentences should not remain in the same paragraph merely because they were originally written on the same source line.

Check a proposed group:

1. Can the grouping be named without an artificial conjunction or vague label?
2. Do its members answer the same parent question or serve the same reader task?
3. Are the members peers, or does one explain, qualify, or depend on another?
4. Does grouping reduce context switching and lookup effort without hiding differences?
5. Would a reader need to inspect this group as a unit?

If the answers do not support one coherent group, split or relocate it.
If splitting removes important context or forces repetitive introductions, consider keeping it together.

### Maintain parallelism

Choose one organizing axis for each peer group: entities, operations, states, questions, time periods, responsibilities, or another meaningful dimension.
Do not mix an inventory of entities with an execution rule as peers in the same list.
Do not arbitrarily package six independent items into two bullets of three unless those two groups have real names and distinct purposes.
Maintain comparable granularity among peers when that makes scanning and comparison easier.
A necessary exception can be longer or more detailed; preserve the distinction rather than forcing equal length.

### Make containment explicit

If two subjects are both parts of a larger subject, introduce the meaningful parent when it helps navigation.
For example, "Views used by this task" can contain "View list" and "Checks performed when reading views".
Without their parent, two peer headings can misleadingly suggest unrelated scopes.
Conversely, do not add a parent heading when the existing surrounding heading already provides the relationship clearly.

### Name the actual scope

A heading is a promise about the section below it.
Use names that accurately specify subject, task, audience, or applicable subset.
A heading labeled "Project views" can imply completeness when the content covers only the six views used by one workflow.
A label that joins two distinct concerns with "and" is a signal to investigate, not automatic proof that a split is required.
Avoid generic headings such as "Details" or "Other" when a concrete heading is available.

## Order information by reader need

Choose an ordering principle and keep it intelligible:

- Orientation before specialized detail when the reader lacks a working model.
- Outcome and prerequisites before steps in an executable guide.
- Definitions near the values and rules that use them.
- Conditions before the actions they govern.
- Comparison criteria before comparing alternatives.
- Evidence near the claims it supports.
- Result and its significance before supporting chronology in a status report, unless the chronology is the object of the report.
- Exceptions beside the rule they qualify when they change execution or interpretation.

Do not impose a single top-down order on every medium.
A brief reply, a long tutorial, and a reference catalog have different retrieval and reading patterns.

## Decide whether to keep, split, merge, or relocate

Evaluate the actual candidate structures, including leaving the current structure intact.

| Choice | Prefer when | Watch for |
| --- | --- | --- |
| Keep | One reader task, coherent subject, easy retrieval | Latent mixed purposes hidden by a broad heading |
| Split a block or section | Distinct subjects or information types need independent access | Fragmentation, repeated context, orphaned exceptions |
| Merge blocks or sections | Separate pieces jointly answer one question or repeat each other | Loss of meaningful distinctions |
| Relocate a passage | It belongs to another step, parent topic, audience, or canonical source | Broken context, references, or cross-document dependencies |
| Split a file | Different reader jobs, ownership, lifecycle, audience, or substantial independent lookup | Excessive navigation, dangling links, loss of standalone instructions |
| Merge files | Readers must repeatedly switch between them for one coherent task and independent maintenance brings no benefit | Oversized files, coupled update cycles, mixed audiences |
| Link rather than duplicate | An authoritative detail is maintained elsewhere and a link serves the reader | Broken links, offline execution, inaccessible dependencies |
| Duplicate essential context | Artifacts must work independently or safe execution depends on local context | Conflicting copies after future updates |

### Compare meaningful alternatives

When the choice is consequential, compare at least the status quo and one plausible restructuring against:

- Reader tasks and navigation cost.
- Semantic cohesion and separation of different purposes.
- Completeness, local context, and standalone execution needs.
- Canonical sources and update ownership.
- Change frequency and likelihood of divergence.
- References, anchors, permissions, and downstream dependencies.
- The amount of change and the user's authorized scope.

Do not split a file simply because it exceeds an arbitrary length.
Do not merge files solely to eliminate duplication when the readers or execution contexts require independent copies.

## Distinguish information structure from storage structure

An information topic is not necessarily a file.
Several topics can be presented together in one file, or separate source files can be assembled into one published document.
Navigation and links can express relationships without requiring every conceptual boundary to become a file boundary.

When information is used by multiple artifacts, identify its authoritative source and whether other artifacts can reliably retrieve it.
For an agent instruction executed from a standalone task body, a cross-reference that is not guaranteed to load may be insufficient.
For a repository README, a direct link to maintained API reference may be better than a copied reference table.

## Preserve the limits of authorization

Broader structural inspection is allowed only as needed to understand the requested target and propose a sound structure.
Review or planning does not itself authorize edits.
When a recommended split, merge, or relocation affects files outside the approved scope, present the proposal and expected consequences without making those changes.
Do not let a "small cleanup" silently change requirements, authority, public content, deployment settings, or historical records.

## Validate the architecture

- Can readers answer the key questions by following headings or links without reconstructing scattered fragments?
- Does every parent contain the subjects its label promises and no unrelated peers?
- Do list items and table rows use a defensible organizing axis?
- Are definitions, conditions, examples, and checks placed next to the information they qualify?
- Is a removed, moved, or combined item still reachable and accurately represented?
- Do links, anchors, table of contents, references, and other consumers still resolve after moves?
- Are canonical facts maintained in the right place and independently executable instructions still complete?
- Has the edit stayed within authorized scope and preserved unaffected work?

If failures remain, revisit the semantic model and possible parent structure instead of repeatedly changing formatting alone.

## Sources

- [Google Technical Writing: Organizing large documents](https://developers.google.com/tech-writing/two/large-docs)
- [OASIS DITA 2.0: The topic as the basic unit of information](https://dita-lang.org/2.0/dita/archspec/base/topicdefined)
- [OASIS DITA 2.0: Definition of DITA maps](https://dita-lang.org/2.0/dita/archspec/base/definition-of-ditamaps)
- [W3C WAI: Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/)
- [Information Mapping: Maps and Blocks](https://support.informationmapping.com/hc/en-us/articles/213440709-Structure-your-content-using-Maps-and-Blocks)
