---
name: structure-what-you-write
description: Creates, revises, and reviews writing by selecting and organizing information for its readers and purpose. Use for repository documentation, READMEs, guides, Issues, PRs, emails, comments, and messages.
license: MIT
---

# Structure What You Write

Select the relevant information, design its logical structure, and express it in a form that suits its readers and purpose.\
Paragraphs, lists, tables, headings, sections, and files are ways to represent information, not fixed containers.\
Work at the level that the information needs, from one sentence to a set of related files.\
Better structure can mean less formatting, a longer text, or fewer files.

## Workflow

### 1. Establish the purpose and the scope

- Identify the readers, their task, the medium, and the result that the content must support.
- Identify the request type: creation, revision, restructuring, review, or a decision about whether a change is needed.
- Identify the applicable conventions, the existing content, the required information, and the authorized scope of changes.
- Read the surrounding sections and related materials when you need them to understand the context.\
  Evaluate the existing paragraphs, sections, and file boundaries as part of the work.
- Separate the information that the final reader has from the context that exists only during authoring.

### 2. Examine the evidence and select the information

- Identify the information that the reader needs to understand, decide, or act.
- Separate established facts, authorized decisions, assumptions, interpretations, and unknowns.
- Use suitable primary sources for material factual claims.\
  Write only the facts, decisions, requirements, and reasons that a source supports.
- In a revision, check the existing claims that affect the reader's decisions, not only the structure and the wording.
- Code and other implementation evidence show the current behavior only.\
  Requirements, design reasons, policy, ownership, and acceptable risk need other evidence.
- Separate faithful editing of supplied content from authoring in which you can select content.
- When you restructure existing content, keep its required claims, conditions, uncertainty, commitments, permissions, and safety constraints.
- Before you revise operational instructions, record their parts as working notes with their sources.\
  The parts are the inputs, outputs, selection rules, permissions, prohibitions, and failure handling.\
  Mark behavior that the source does not specify as unspecified.\
  Separate the duties of maintainers from the safeguards that the executing reader still needs.
- Separate presentation choices from operational requirements.\
  Some changes in a revision change behavior: the processing order, item selection, required or optional actions, stop and continue conditions, access boundaries, or mandatory output constraints.\
  Make these changes only with supporting evidence or explicit authority to design that behavior.\
  Permission to improve readability does not give that authority.
- Make an artifact self-contained with the supplied instructions that its reader needs.\
  Leave unspecified behavior unspecified.\
  Report a material gap separately from the finished text, and ask about it only when it prevents the requested work.
- When you can select content, leave out unrelated investigation history, repeated explanations, and unsupported conclusions.\
  Also leave out details that the reader's task does not need.
- When several artifacts contain the same information, identify the source of truth.

### 3. Analyze and organize the information

Identify the units of information before you choose a presentation form.

- Identify the subject, purpose, and type of each unit.\
  Types include a definition, fact, attribute, condition, rule, procedure, constraint, and example.
- Identify the relations between units, such as equivalence, contrast, membership, containment, sequence, dependency, and cause.
- Group information by one consistent, meaningful criterion.
- Select the grouping from the decision that the reader makes.\
  When one item fits several options, organize by the options, and list the item under each option that it fits.
- Keep related definitions, conditions, exceptions, and examples together when readers need them together.
- Separate information that serves different subjects or purposes, even when it is in one paragraph or section of the source.
- Keep the connections between related information.

The boundaries of the underlying information can differ from the boundaries of sentences, paragraphs, bullets, tables, headings, and files.

### 4. Design the structure and the placement

Decide how to organize the information before you write its final form.

- Select the level of detail and the grouping for each unit of information.
- Make parallel items comparable in subject, role, and level of abstraction.
- Show parent-child relations, sequences, dependencies, and exceptions at the correct level.
- Make each heading describe the content and the scope below it.
- Give sibling headings the same kind of content and the same relation to their parent.\
  When procedure steps and reference material are in one document, put each group under its own parent heading.\
  An existing heading that already shows the relation is sufficient.
- Keep details that only one step uses inside that step.
- Write sibling headings in the same form, such as actions for procedure steps and nouns for reference material.
- Write each document for one main audience.\
  State that audience at the start when readers cannot infer it.\
  Put constraints for AI agents only in instructions for agents, not in guides for people.
- Organize the information so that readers can find related content in one place.
- Decide whether each section or file stays, is split, is combined, or has content moved.
- When several artifacts are involved, consider their purposes, sources of truth, navigation, and maintenance.
- Keep the information that each independent artifact needs, even when this causes some duplication.
- Use hierarchy to show containment.\
  Add depth when different kinds of content need it.\
  Add files or cross-references only when they improve understanding, use, or maintenance.

Evaluate a structural problem at the correct level.\
A problem in one paragraph can need a new organization of a section, a document, or a set of documents.\
Change only the requested scope, and propose changes outside that scope.

### 5. Choose presentation forms and write

Choose each presentation form from the meaning, relations, and use of the information:

- **Prose**: explain one subject, reasoning, context, or cause.
- **Bulleted lists**: show separate, parallel items without an order of execution.
- **Numbered lists**: show ordered steps.\
  When a step has short details, give the step a bold name, and put the details below it as bullets.\
  When a step contains several paragraphs or code blocks, give each step its own heading.
- **Nested lists**: show real containment or parent-child relations.
- **Tables**: show repeated attributes, definitions, conditions, or comparisons across clear dimensions.\
  When a cell needs several sentences or independent conditions, use headings or lists.
- **Code blocks**: show exact syntax, configuration, commands, output formats, or other literal structures.
- **Diagrams**: show relations, flows, or structures that are hard to show efficiently in text.

Apply these choices with judgment:

- Give each bullet, paragraph, table, or section one subject.
- Keep related information together, even when a bullet or a sentence becomes longer.
- Combine independent subjects into one table only when the combined view has a clear use.
- Show long lists, independent conditions, and actions in a clear structure, not inside dense prose.
- Put examples and exceptions near the definitions or rules that they explain.
- Start each section with its point: what the section lets the reader do or know.\
  Put qualifications and limits after that point, inside the step or item that they affect.\
  Put a warning before an action only when the reader must know it before the action.
- Show the logical relations between sentences, such as cause, contrast, and condition, with explicit connecting words.
- Name the actor each time it changes between the reader, another person, an agent, or a system.\
  Use a name that has the same meaning for every reader.\
  For example, "the user" can mean different people when both people and agents read the document.
- Use one term for one referent.\
  Check that the ordinary meaning of the term matches what actually happens.
- Use headings and other structural elements when their distinctions help the reader.
- Keep natural language, meaningful transitions, and sufficient explanation.

Follow the conventions of the target medium.\
Give a short message the structure of a short message.

### 6. Validate the result

Read the result as a reader who did not see the authoring conversation, and check these items:

- The content serves the intended reader and purpose.

- The required information is present, correct to its sources, and suitably qualified.

- Each section, paragraph, list item, and table has a clear role.

- The grouping criteria, hierarchy, order, and placement match the real relations of the information.

- Each heading describes its content, and suggests no incorrect scope.

- A reader of only the headings can tell the topic of each section.

- The opening sentences of each section state its point.

- When several sections or documents changed together, each section meets the criteria in this list.\
  A corrected structure alone does not complete the revision.

- The reader can find and understand related information together.

- Each presentation form makes the information easier to find, compare, understand, or use.

- The structure is as simple as the information allows, without extra fragments or repetition.

- The restructured content keeps its meaning, requirements, limits, and authorized decisions.

- For operational revisions, compare the source and the result in both directions:

  - Each existing requirement is still available to its executing reader.
  - Each new mandatory instruction equals a supplied requirement, or authorized design work supports it.

  Remove unsupported requirements.\
  Keep necessary design proposals outside the finished artifact.

- Changes to several files keep the necessary links, references, and independent behavior.

When they apply, check factual claims, links, examples, commands, generated content, and repository checks.\
Check them against their sources and against the results of running them.\
If a structural problem remains, review the information analysis and the higher-level organization again.

## References

Read only the references that apply to the current task:

- [Writing contexts](references/writing-contexts.md): when the medium or the type of artifact affects the structure, content, or conventions.
- [Information types](references/information-types.md): when you separate information types, or choose structures for definitions, rules, procedures, and examples.
- [Information architecture](references/information-architecture.md): when grouping, hierarchy, order, placement, or the split and merge of sections or files needs more guidance.
- [Presentation patterns](references/presentation-patterns.md): when you choose between prose, lists, tables, code blocks, and diagrams.
- [Methods and principles](references/methods.md): when established writing or information-design methods help a structural decision.
- [Examples](references/examples.md): when you compare an unclear choice or a recurring structural problem with worked examples.

## Output

- For creation or an authorized revision, produce the finished content, not a description of how to write it.

- For a review only, identify the structural problems, explain their effects, and propose improvements.\
  Keep the target unchanged.

- When you assess whether repository documentation needs to change, give one result:

  - an update is required
  - no documentation impact, with the reason
  - blocked by unknowns, with the missing evidence or decision

- When no change is needed, keep the existing content.

- When required information or authority is missing, identify the specific uncertainty, and complete the independent work.

- Keep authoring notes, rejected alternatives, and internal revision history out of the finished content, unless they serve its readers.

- Edit files, publish material, or contact other people only within the authorized scope.

- Report the completed changes, the checks that you ran, the open issues, and the proposed changes outside the scope.\
  Separate structural changes from changes of sentences, and state where the depth of revision differs between sections.
