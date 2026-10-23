# Writing contexts and reader tasks

Use this reference when the medium, intended reader, or purpose materially affects what information belongs in the writing and how it should be organized.
These are decision aids, not mandatory section templates.
Applicable organizational and repository conventions take precedence over the patterns below.

## Choose by reader task, not filename

Before selecting a pattern, identify the reader's question and desired action.
The same medium may serve different purposes: an issue may record a defect, propose work, or document an investigation; a message may ask for a decision or merely report a result.
Identify whether the content primarily helps readers orient themselves, act, look up facts, understand reasons, review a proposal, or make a decision.
Keep material together when a single reader task benefits from it; separate unrelated jobs when their combination makes either harder.

| Reader task | Typical content | Primary organizing principle |
| --- | --- | --- |
| Orient and navigate | README, entry page, overview | Purpose and shortest useful path first; link to maintained detail |
| Perform an action | How-to, runbook, agent instruction | Preconditions, decisions, ordered actions, verification, recovery |
| Look up exact information | Specification, API reference, field definitions | Stable identifiers and comparable properties |
| Understand a design | Architecture explanation, design rationale | Scope, conceptual model, relationships, evidence and trade-offs |
| Assess a proposal | Design doc, RFC | Problem, constraints, options, proposed choice, consequences, open decisions |
| Track work | Issue, task | Problem or outcome, current evidence, acceptance criteria, next action |
| Review a change | Pull request | Purpose, actual changes, effects, validation, unresolved risk |
| Receive an update | Report, briefing | Results and changes, evidence, implications, decisions or next actions |
| Respond or decide | Email, review comment, chat message | Context needed to interpret the point, request, evidence, next step |

## Entry documents and README files

**Reader question:** What is this, is it relevant to me, and where do I start?

- Identify the project or artifact, its purpose, and intended audience where material.
- Give the shortest supported start, usage, or verification path when the README serves users or contributors.
- Link to canonical configuration, architecture, API reference, tutorials, and operational procedures instead of duplicating them.
- Introduce prerequisites before a command that depends on them, and place success checks beside the action they validate.
- Avoid turning the entry document into a complete reference, change log, design history, and operations manual at once.
- Verify links, commands, compatibility claims, and any stated current project status.

A README for a library, a monorepo, and a personal knowledge base need different entry points.
Do not copy a general-purpose README outline where the reader task does not require it.

## Instructions for AI agents and scheduled tasks

**Reader question:** What outcome should I produce, with which inputs, decisions, limits, and checks?

- State the executable task, authorized scope, required inputs, and observable completion conditions.
- Distinguish definitions and reference data from execution steps, decision conditions, and exceptional paths.
- Put conditions next to the decisions or actions they govern.
- State established handling for missing evidence, access, or prerequisites. In a revision, preserve the supplied handling; do not invent new validation rules, stop/continue decisions, or permissions to make the task appear complete. Surface a material unspecified case separately when needed.
- Give an exact output schema when an established downstream consumer requires it. Otherwise choose a helpful presentation without turning incidental wording, ordering, or formatting into a new mandatory execution constraint.
- Preserve the task's standalone prerequisites when it is executed without the directory README or the authoring conversation.
- Standalone use determines where required information must be available; it does not authorize designing additional runtime behavior. New task design must stay within the explicitly authorized design scope.
- In a revision, check the source-to-result correspondence before finalizing: preserve each execution safeguard locally and justify each new imperative against a supplied requirement. For example, presenting a reporting requirement as bullets does not authorize imposing a new record sort order, exact output string, or malformed-record policy.
- Keep editorial history, unused alternatives, and rules for maintainers of the instruction repository out of the executable task unless the executing agent needs them.
- Avoid repeating the same permission boundary in multiple phrasings merely to increase apparent certainty.

The operational task may need a constraint even if the repository README already explains the same constraint to maintainers.
Correct content placement follows the actual execution and reading context, not a universal ban on duplication.

## Design documents and RFCs

**Reader question:** What should we choose or approve, and why?

- Establish the problem, desired outcome, scope, material constraints, and decision criteria.
- Show the proposed design at the level necessary to evaluate it; describe alternatives and material trade-offs on comparable dimensions.
- Separate observed current behavior from desired future behavior and undecided proposals.
- Identify failure cases, migrations, verification, operational impacts, and unresolved questions when they affect the decision.
- Keep evidence and the proposed recommendation separate from the act of approving it.
- Do not bury the requested decision inside an implementation diary or exhaustive investigation notes.

A design document is not an accepted decision record until the responsible party has made the decision.

## Specifications and reference material

**Reader question:** Which exact behavior, value, type, contract, or constraint applies?

- Follow the conceptual structure of the system or interface where doing so helps lookup.
- Identify each entity or field, its type, permitted values, defaults, empty or absent states, constraints, and relevant exceptions.
- Present repeated properties consistently so that readers can locate and compare them.
- Distinguish normative requirements from observations, hypotheses, and proposals.
- Prefer verified schemas, code, generated references, or explicitly approved requirements to manually reconstructed facts.
- Avoid tutorials, historical debate, and persuasive narrative inside a lookup reference unless they prevent a specific misunderstanding.

When generated reference data is the canonical source, link to it or use the established generation process rather than copying values into an independently maintained document.

## Current architecture and behavior explanations

**Reader question:** How is this system organized, and what does it do now?

- State the system boundary and major components before detailing individual modules.
- Organize around responsibilities, relationships, data flow, interfaces, and failure boundaries rather than an indiscriminate inventory of classes.
- Explain important dependencies and why they matter to the reader's investigation or maintenance task.
- Label what is directly verified and where current behavior remains unknown.
- Do not infer an original design rationale, business requirement, or promised future behavior from implementation alone.
- When describing current behavior from implementation, present it as descriptive rather than normative, and record the examined revision when practical.
- Separate the current architecture from a proposal to change it or from a historical decision record.

## Procedures, how-to guides, and runbooks

**Reader question:** How do I reach a particular outcome safely and know it worked?

- Start with the outcome and relevant prerequisites.
- Express actions in the order in which they must be performed; show conditionals at the relevant decision point.
- Put a condition before the action it governs, and replace vague conditions such as "as needed" with observable criteria.
- Prefer commands that can be copied as written. Give placeholders meaningful names and explain them next to the example.
- Give each step a recognizable action, with subordinate details, commands, cautions, and checks placed beneath that step when appropriate.
- State expected results and practical completion checks rather than declaring success after an attempted action.
- Include failure branches, escalation, rollback, or recovery only when evidenced, authorized, and relevant. Do not invent them to make a procedure look complete; report the missing requirement instead.
- Keep conceptual education and exhaustive command references elsewhere if they distract from execution.

A tutorial is for learning through a guided experience; a how-to is for accomplishing an actual task.
Do not force a tutorial's pacing into a runbook or a runbook's strictness into an explanation.

## Reports and briefings

**Reader question:** What changed, what matters, and what needs attention?

- Lead with the outcome or most consequential change for the intended reader.
- Group achievements, pending decisions, active work, blockers, risks, and unknowns by their actual roles.
- Attach evidence, dates, or links to the claims that need them; distinguish completed from attempted or unverified work.
- Put each requested decision next to its options, grounds, and required response.
- Use a stable structure when readers compare recurring reports, but omit irrelevant empty categories.
- Do not turn a short status report into an account of the entire research and writing process.

A recurring report may need an output skeleton for consistency; a one-off briefing may work better with a short narrative.

## Issues and task descriptions

**Reader question:** What problem or outcome does this item represent, and how will we know it is done?

- State the observed problem or desired outcome before implementation details.
- Separate current evidence, desired behavior, constraints, acceptance criteria, and optional ideas.
- Identify reproducible steps and observed versus expected behavior for defects when available.
- Preserve traceable dependencies and links without restating entire related issues.
- Do not turn an unapproved solution sketch into a committed requirement.
- Follow the repository's issue template when it serves the requested purpose; leave sections out only when local rules permit.

Issue titles should distinguish the item from its siblings without repeating context already provided by the parent or project.

## Pull request descriptions

**Reader question:** What changed, why, what is affected, and what was verified?

- Describe the actual change and its purpose; distinguish delivered behavior from remaining work.
- Link relevant issues, decisions, artifacts, and evidence without copying the full work history.
- Explain material behavioral, compatibility, operational, or security effects where relevant.
- State tests and checks actually performed, their observed results, and relevant unperformed checks.
- Distinguish a draft, proposed change, merged change, and deployed or verified outcome.
- Make review-relevant information easy to scan, but avoid filling template sections with generic claims or repetitive detail.

The repository's PR template is authoritative for required sections, not proof that every optional heading needs content.

## Decision records

**Reader question:** What was decided, on what grounds, and with what consequences?

- Record a decision, its status, the contemporaneous context, material alternatives, accepted consequences, and superseding links.
- Preserve its historical meaning instead of silently rewriting a past decision to reflect current preferences.
- Do not create an accepted rationale from implementation evidence alone.
- Keep operational reference material and current architectural truth separate from historical decision records.

## Emails, comments, and messages

**Reader question:** What am I being told, what do I need to know, and what response or action is expected?

- Use the recipient's existing thread or conversation context where available, without assuming access to private drafting notes.
- Put the main point, requested action, or decision near the beginning when appropriate for the relationship and tone.
- Include sufficient facts, evidence, owner, deadline, and link only when necessary and grounded.
- Keep one primary request or clearly differentiated requests; separate unrelated topics rather than hiding them inside one long paragraph.
- Choose normal prose for short exchanges, bullets for genuinely distinct points, and a table only when it makes comparison materially easier in the target medium.
- For review comments, name the exact location and observed problem, explain its consequence, and propose an actionable change when warranted.
- Separate suggestions from decisions and avoid making commitments on the recipient's behalf.
- Preserve tone and established social context rather than adding formal headings to a short personal message.

## Sources

- [GitHub Docs: About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [GitHub Docs: Managing and standardizing pull requests](https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests)
- [Google Technical Writing: Organizing large documents](https://developers.google.com/tech-writing/two/large-docs)
- [Google Technical Writing: Documents](https://developers.google.com/tech-writing/one/documents)
- [Diátaxis: Start here](https://diataxis.fr/start-here/)
- [OASIS DITA 2.0: Information typing](https://dita-lang.org/2.0/dita/archspec/base/information-typing)
