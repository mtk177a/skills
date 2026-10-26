# Writing contexts and reader tasks

Use this reference when the medium, the reader, or the purpose affects what to write and how to organize it.\
These patterns support decisions, and they are not required section templates.\
The applicable conventions of the organization and the repository take precedence over these patterns.

## Choose by the task of the reader, not by the filename

Before you select a pattern, identify the question of the reader and the action that the reader wants.\
One medium can serve different purposes.\
For example, an Issue can record a defect, propose work, or document an investigation.\
A message can ask for a decision, or only report a result.\
Identify the main job of the content: to help readers find their way, act, look up facts, understand, review, or decide.\
Keep material together when one task of the reader benefits from it.\
Separate unrelated jobs when their combination makes either job harder.

| Task of the reader | Typical content | Main organizing principle |
| --- | --- | --- |
| Find the way | README, entry page, overview | The purpose and the shortest useful path first, with links to maintained details |
| Do an action | How-to guide, runbook, agent instruction | Preconditions, decisions, ordered actions, verification, recovery |
| Look up exact information | Specification, API reference, field definitions | Stable identifiers and comparable properties |
| Understand a design | Architecture explanation, design reasons | Scope, conceptual model, relationships, evidence, trade-offs |
| Assess a proposal | Design document, RFC | Problem, constraints, options, proposed choice, consequences, open decisions |
| Track work | Issue, task | Problem or result, current evidence, acceptance criteria, next action |
| Review a change | Pull request | Purpose, actual changes, effects, validation, open risk |
| Receive an update | Report, briefing | Results and changes, evidence, implications, decisions or next actions |
| Respond or decide | Email, review comment, chat message | The context to interpret the point, the request, the evidence, the next step |

## Entry documents and README files

**Question of the reader**: what is this, is it relevant to me, and where do I start?

- Identify the project or artifact, its purpose, and its intended audience, when they matter.
- When the README serves users or contributors, give the shortest supported path to start, use, or verify.
- Link to the source of truth for configuration, architecture, API reference, tutorials, and operational procedures, instead of copying them.
- Introduce each prerequisite before the command that needs it.\
  Put each success check next to the action that it validates.
- Keep the entry document an entry point, and put the complete reference, change log, design history, and operations manual elsewhere.
- Verify links, commands, compatibility claims, and each stated current status of the project.

A README for a library, a monorepo, and a personal knowledge base need different entry points.\
Use a general-purpose README outline only where the task of the reader needs it.

## Instructions for AI agents and scheduled tasks

**Question of the reader**: which result must I produce, with which inputs, decisions, limits, and checks?

- State the task to execute, the authorized scope, the required inputs, and the completion conditions that the agent can observe.
- Separate definitions and reference data from execution steps, decision conditions, and exception paths.
- Put each condition next to the decision or action that it governs.
- End each step with a completion criterion that the agent can check.
- State the wanted behavior.\
  Use a prohibition only for a hard guardrail that has no positive form.\
  Put the wanted behavior next to the prohibition.
- Keep only text that changes the behavior of the agent.\
  The model already knows general practices, so state only what is specific to the task.
- State each rule once, in the step where it applies.\
  Repeated statements of one boundary in different words add text, not certainty.
- State the established handling for missing evidence, access, or prerequisites.
- Give an exact output schema when an established later consumer requires it.\
  Otherwise, choose a helpful presentation, and keep incidental wording, order, or formatting optional.
- Keep the prerequisites that the task needs when it runs without the README of the directory or the authoring conversation.\
  This need decides where the information must be.\
  It does not authorize the design of new runtime behavior.
- Keep editorial history, unused alternatives, and rules for maintainers out of the task.\
  Include them only when the executing agent needs them.

The operational task can need a constraint that the README already explains to maintainers.\
Place content by the actual context of execution and reading.\
Duplication is acceptable when an independent artifact needs it.

## Design documents and RFCs

**Question of the reader**: what must we choose or approve, and why?

- State the problem, the desired result, the scope, the material constraints, and the decision criteria.
- Show the proposed design at the level that its evaluation needs.\
  Describe the alternatives and the material trade-offs on comparable dimensions.
- Separate the observed current behavior from the desired future behavior and from undecided proposals.
- Identify failure cases, migrations, verification, operational impacts, and open questions when they affect the decision.
- Keep the evidence and the recommendation separate from the act of approval.
- Put the requested decision where the reader sees it, outside implementation diaries and long investigation notes.

A design document becomes an accepted decision record only after the responsible party makes the decision.

## Specifications and reference material

**Question of the reader**: which exact behavior, value, type, contract, or constraint applies?

- Follow the conceptual structure of the system or interface when it helps lookup.
- For each entity or field, identify its type, permitted values, defaults, empty or absent states, constraints, and relevant exceptions.
- Present repeated properties consistently, so that readers can find and compare them.
- Separate normative requirements from observations, hypotheses, and proposals.
- Use verified schemas, code, generated references, or explicitly approved requirements before facts that you reconstructed by hand.
- Keep tutorials, historical debate, and persuasive narrative out of a lookup reference, unless they prevent a specific misunderstanding.

When generated reference data is the source of truth, link to it, or use the established generation process.\
Copy its values into a separately maintained document only when no link or generation process is available.

## Explanations of current architecture and behavior

**Question of the reader**: how is this system organized, and what does it do now?

- State the system boundary and the major components before the details of individual modules.
- Organize by responsibilities, relationships, data flow, interfaces, and failure boundaries, not by a full list of classes.
- Explain the important dependencies, and why they matter to the investigation or maintenance task of the reader.
- Label what is directly verified, and where the current behavior is still unknown.
- Base the original design reasons, business requirements, and promised future behavior on evidence other than the implementation.
- When you describe current behavior from the implementation, present it as a description, not as a rule.\
  Record the examined revision when practical.
- Keep the current architecture separate from a proposal to change it, and from a historical decision record.

## Procedures, how-to guides, and runbooks

**Question of the reader**: how do I reach a result safely, and know that it worked?

- Start with the result and the relevant prerequisites.
- Write the actions in the order of execution, and show conditions at the decision point where they apply.
- Put each condition before the action that it governs.\
  Replace vague conditions, such as "as needed", with criteria that the reader can observe.
- Use commands that the reader can copy as written.\
  Give placeholders meaningful names, and explain them next to the example.
- Give each step a recognizable action.\
  Put the details, commands, cautions, and checks of the step below it, when that helps.
- State the expected results and practical completion checks, instead of a declaration of success after an attempted action.
- Include failure branches, escalation, rollback, or recovery when they are evidenced, authorized, and relevant.\
  When a requirement for them is missing, report the gap.
- Keep conceptual teaching and full command references elsewhere when they distract from execution.

A tutorial supports learning through a guided experience, and a how-to guide supports an actual task.\
Give a runbook the strictness of a runbook, and an explanation the pace of an explanation.

## Reports and briefings

**Question of the reader**: what changed, what matters, and what needs attention?

- Start with the result or the most important change for the intended reader.
- Group achievements, pending decisions, active work, blockers, risks, and unknowns by their actual roles.
- Attach evidence, dates, or links to the claims that need them.\
  Separate completed work from attempted or unverified work.
- Put each requested decision next to its options, its reasons, and the required response.
- Use a stable structure when readers compare recurring reports, and leave out empty categories.
- Keep a short status report about the status, not about the whole process of research and writing.

A recurring report can need an output skeleton for consistency.\
A single briefing can work better as a short narrative.

## Issues and task descriptions

**Question of the reader**: which problem or result does this item represent, and how will we know that it is done?

- State the observed problem or the desired result before implementation details.
- Separate current evidence, desired behavior, constraints, acceptance criteria, and optional ideas.
- For defects, give the reproduction steps and the observed and expected behavior, when they are available.
- Keep traceable dependencies and links, without a full restatement of related Issues.
- Keep a solution sketch that nobody approved as an option, not as a requirement.
- Follow the Issue template of the repository when it serves the requested purpose.\
  Leave sections out only when the local rules allow it.

Give each Issue a title that distinguishes it from its siblings.\
Leave out the context that the parent or the project already gives.

## Pull request descriptions

**Question of the reader**: what changed, why, what is affected, and what was verified?

- Describe the actual change and its purpose.\
  Separate the delivered behavior from the remaining work.
- Link the relevant Issues, decisions, artifacts, and evidence, without a copy of the full history of the work.
- Explain material effects on behavior, compatibility, operations, or security, when they apply.
- State the tests and checks that actually ran, their observed results, and the relevant checks that did not run.
- Separate a draft, a proposed change, a merged change, and a deployed or verified result.
- Make information for the review easy to scan.\
  Fill template sections only with specific content.

The PR template of the repository decides the required sections.\
Optional headings stay empty or absent when they have no content.

## Decision records

**Question of the reader**: what was decided, for which reasons, and with which consequences?

- Record these items:

  - the decision and its status
  - the context at the time and the material alternatives
  - the accepted consequences
  - the links to later decisions that replace it

- Keep the historical meaning of a past decision, even when current preferences differ.

- Base an accepted reason on the record of the decision, not on implementation evidence alone.

- Keep operational reference material and the current architecture separate from historical decision records.

## Emails, comments, and messages

**Question of the reader**: what am I told, what must I know, and which response or action is expected?

- Use the existing thread or conversation context of the recipient, when it is available.\
  The recipient has no access to private drafting notes.
- Put the main point, the requested action, or the decision near the start, when that suits the relationship and tone.
- Include facts, evidence, the owner, a deadline, and a link only when they are necessary and grounded.
- Make one main request, or clearly separate requests.\
  Put unrelated topics in separate messages or paragraphs.
- Use normal prose for short exchanges, and bullets for clearly separate points.\
  Use a table only when it makes a comparison much easier in the target medium.
- For a review comment, name the exact location and the observed problem, and explain its consequence.\
  Propose a change when it is useful.
- Separate suggestions from decisions, and make commitments only for yourself.
- Keep the tone and the established social context.\
  Give a short personal message the form of a short personal message.

## Sources

- [GitHub Docs: About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)
- [GitHub Docs: Managing and standardizing pull requests](https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests)
- [Google Technical Writing: Organizing large documents](https://developers.google.com/tech-writing/two/large-docs)
- [Google Technical Writing: Documents](https://developers.google.com/tech-writing/one/documents)
- [Diátaxis: Start here](https://diataxis.fr/start-here/)
- [OASIS DITA 2.0: Information typing](https://dita-lang.org/2.0/dita/archspec/base/information-typing)
- [Skill authoring best practices (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [`writing-for-agents` (Matt Pocock)](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
