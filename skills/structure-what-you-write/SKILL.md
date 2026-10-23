---
name: structure-what-you-write
description: Creates, revises, and reviews writing by selecting and organizing information for its readers and purpose. Use for repository documentation, READMEs, guides, issues, PRs, emails, comments, and messages.
license: MIT
---

# Structure What You Write

## Objective

Create or improve writing by selecting relevant information, designing its logical structure, and expressing it in a form suited to its readers and purpose.

Treat paragraphs, lists, tables, headings, sections, and file boundaries as ways to represent information, not as predetermined containers.

Work at the level the information requires, from an individual sentence to a collection of related files. Do not equate better structure with more formatting, shorter text, or additional files.

## Workflow

### 1. Establish purpose and scope

- Identify the intended readers, their task, the writing medium, and the outcome the content must support.
- Determine whether the request calls for creation, revision, restructuring, review, or an assessment of whether a change is needed.
- Identify applicable conventions, existing content, required information, and the authorized scope of changes.
- Examine surrounding sections and related materials when necessary to understand the information's context. Do not assume existing paragraphs, sections, or file boundaries are correct.
- Distinguish information available to the final reader from context available only during authoring.

### 2. Examine evidence and select information

- Identify the information needed for the reader to understand, decide, or act.
- Distinguish established facts, authorized decisions, assumptions, interpretations, and unknowns.
- Use appropriate primary sources for material factual claims. Do not invent missing facts, decisions, requirements, or rationale.
- Treat code and other implementation evidence as establishing current behavior only. It does not by itself establish requirements, design rationale, policy, ownership, or acceptable risk.
- Distinguish faithful editing of supplied content from authoring where content selection is permitted.
- Preserve required claims, conditions, uncertainty, commitments, permissions, and safety constraints when restructuring existing content.
- Before revising operational instructions, identify the supplied inputs, required outputs, selection rules, permissions, prohibitions, and failure handling as working notes tied to their sources. Mark unspecified behavior as unspecified. Separate maintainer duties from safeguards the executing reader still needs.
- Distinguish presentation choices from operational requirements. In a revision, changing processing order, item selection, required or optional actions, stop/continue conditions, access boundaries, or mandatory output constraints requires supporting evidence or explicit authority to design that behavior. Permission to improve readability does not supply that authority.
- Make an artifact self-contained by retaining the supplied instructions its reader needs, not by inventing missing operational rules. Leave unspecified behavior unspecified; identify a material gap separately from the finished text and ask only when it prevents completing the requested work.
- Exclude irrelevant investigation history, redundant explanations, unsupported conclusions, and details that do not serve the reader's task when content selection is permitted.
- Identify the canonical location of information when it is maintained across multiple artifacts.

### 3. Analyze and organize information

Identify meaningful information units before choosing a presentation format.

- Determine the subject, purpose, and information type of each unit, such as a definition, fact, attribute, condition, rule, procedure, constraint, or example.
- Identify relationships between units, including equivalence, contrast, membership, containment, sequence, dependency, and cause.
- Group information by a consistent, meaningful criterion rather than arbitrary proximity or convenient list length.
- Keep related definitions, conditions, exceptions, and examples together when readers need them together.
- Separate information that serves different subjects or purposes, even when it appears in the same original paragraph or section.
- Preserve meaningful connections between related information instead of fragmenting it into isolated statements.

The boundaries of sentences, paragraphs, bullets, tables, headings, and files do not determine the boundaries of the underlying information.

### 4. Design the structure and placement

Determine how the information should be organized before drafting its final form.

- Choose an appropriate level of detail and grouping for each information unit.
- Make parallel items comparable in subject, role, and level of abstraction.
- Represent parent-child relationships, sequences, dependencies, and exceptions at the appropriate level.
- Ensure that each heading accurately describes the content and scope beneath it.
- Organize information so readers can locate related content without reconstructing its relationships from scattered passages.
- Consider whether sections or files should remain as they are, be split, be combined, or have content relocated.
- When multiple artifacts are involved, consider their distinct purposes, canonical sources, navigation, and maintenance responsibilities.
- Preserve the information required by artifacts that must operate independently, even when some duplication is necessary.
- Avoid additional hierarchy, files, or cross-references unless they improve comprehension, use, or maintainability.

Evaluate structural problems at the appropriate level. A problem visible in one paragraph may require reorganizing a section, document, or document set.

Inspecting a broader structure does not authorize changes beyond the requested scope. Propose changes outside that scope rather than performing them without approval.

### 5. Choose presentation forms and write

Choose the presentation form according to the information's meaning, relationships, and intended use.

- Prose: Explain a coherent subject, reasoning, context, or causal relationship.
- Bulleted lists: Present distinct, parallel items without an inherent execution order.
- Numbered lists: Present ordered steps or sequences. Keep a step's details and checks subordinate to the step when appropriate.
- Nested lists: Express genuine containment or parent-child relationships, not decorative indentation.
- Tables: Present repeated attributes, definitions, conditions, or comparisons across clearly identified dimensions.
- Code blocks: Show exact syntax, configuration, commands, output formats, or other literal structures.
- Diagrams: Clarify relationships, flows, or structures that are difficult to communicate efficiently in text.

Apply these choices with judgment.

- Do not combine unrelated subjects in a single bullet, paragraph, table, or section.
- Do not split related information merely to make every bullet or sentence short.
- Do not combine independent subjects into one table unless the combined view serves a meaningful purpose.
- Do not hide long enumerations, independent conditions, or actionable items inside dense prose when a clearer structure is available.
- Place examples and exceptions near the definitions or rules they clarify.
- Use headings and structural elements only when their distinctions help the reader.
- Preserve natural language, meaningful transitions, and sufficient explanation.

Follow the conventions of the target medium without forcing long-document structures onto short messages.

### 6. Validate the result

Review the result as a reader who does not have access to the authoring conversation.

Check that:

- The content serves the intended reader and purpose.
- Required information is present, accurate to its sources, and appropriately qualified.
- Each section, paragraph, list item, and table has a discernible role.
- Grouping criteria, hierarchy, sequence, and placement reflect the information's actual relationships.
- Headings accurately describe their contents without implying an incorrect scope.
- Related information can be found and understood together.
- Presentation forms make information easier to locate, compare, understand, or use.
- The structure is not unnecessarily fragmented, repetitive, or complicated.
- Restructuring has preserved existing meaning, requirements, limitations, and authorized decisions.
- For operational revisions, compare source and result in both directions: every existing requirement remains available to its executing reader, and every new mandatory instruction is equivalent to a supplied requirement or supported by authorized design work. Remove unsupported requirements rather than completing them by assumption; keep needed design proposals outside the finished artifact.
- Changes to multiple files preserve necessary links, references, and standalone behavior.

Where relevant, validate factual claims, links, examples, commands, generated content, and repository-specific checks against their actual sources and execution results.

If a structural problem remains, reconsider the information analysis and higher-level organization rather than applying cosmetic formatting.

## Reference materials

Read only the references relevant to the current task.

- [Writing contexts](references/writing-contexts.md): Use when the writing medium or artifact type materially affects structure, content, or conventions.
- [Information types](references/information-types.md): Use when distinguishing information types or choosing structures for definitions, rules, procedures, and examples.
- [Information architecture](references/information-architecture.md): Use when grouping, hierarchy, ordering, placement, or splitting and merging sections or files requires additional guidance.
- [Presentation patterns](references/presentation-patterns.md): Use when choosing between prose, lists, tables, code blocks, and diagrams.
- [Methods and principles](references/methods.md): Use when established writing or information-design methods help resolve a structural decision.
- [Examples](references/examples.md): Use when evaluating ambiguous choices or recurring structural problems against worked examples.

The workflow must remain usable without unrelated Skills or external services.

## Output and boundaries

- For creation or authorized revision, produce the requested finished content rather than a description of how to write it.
- For review-only requests, identify structural problems, explain their effects, and propose improvements without modifying the target.
- When assessing whether repository documentation needs to change, conclude with one result: update required; no documentation impact, with the reason; or blocked by unknowns, naming the missing evidence or decision.
- When no change is needed, preserve the existing content instead of manufacturing an improvement.
- When required information or authority is missing, identify the specific uncertainty and complete independent work where possible.
- Keep authoring notes, discarded alternatives, and internal revision history out of the finished content unless they serve its readers.
- Do not treat Skill invocation as permission to edit files, publish material, contact others, or expand the authorized scope.
- Report completed changes, checks actually performed, unresolved issues, and proposed out-of-scope changes concisely.
