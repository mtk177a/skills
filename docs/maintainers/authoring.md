# Skill authoring guide

This guide is for maintainers and the agents working for them.\
It explains how to design, write, and check the Skills of this repository.\
It also explains what else to update when a Skill changes.\
Read it before you create a Skill or change what an existing Skill does.

The two upstream Gist mirrors are an exception.\
They follow the copying rules in [Upstream Gist mirrors](#upstream-gist-mirrors).\
Keep their `SKILL.md` files unchanged, whatever the other rules in this guide say.

## Design the Skill

### Responsibility

Give each Skill one responsibility and a clear situation in which to use it.\
Within that responsibility, prioritize these decisions:

- **Start from the outcome**: design a workflow that needs judgment from the intended outcome and the evidence, not from a predetermined artifact.
- **Match the freedom of the instructions to the task**: when several approaches are valid, state the goals and constraints.\
  When order or completeness affects correctness, give short ordered steps and a way to verify them.
- **Report the whole diagnosis**: report every finding, even when a fix will be implemented or rolled out in stages.
- **Let the evidence set the amount of work**: investigate and report until more evidence would not change the decision.

To check whether a new Skill overlaps an existing one, read only the existing Skills that settle the overlap.\
Stop when the overlap is settled.

### Name

Name the Skill with an action and an object in kebab-case, such as `clarify-request` or `design-changes`.\
Then the name shows its responsibility and when to use it.\
Prefer clarity over brevity, and avoid names that suggest a broader scope than the Skill has.\
Use a single word, such as `build`, only when the responsibility is narrow enough that the word cannot be misread.

### Description

An agent reads the `description` to decide whether to use the Skill.\
Write it for that decision, not as a general explanation.\
Include:

- the situation in which to use the Skill
- the kind of work it helps with
- any dependency on a specific client, and what that dependency is

Put in the `description` only what the agent needs to choose the Skill.\
Put what it needs after choosing the Skill, such as roles, orchestration, and execution details, in the body.

Write the `description` in the third person, for example "Drafts commit messages for ...".\
The client adds it to the system prompt.\
A change of viewpoint there can make the Skill harder to select.

Keep the `description` simple.\
Write only when to use the Skill.\
A list of exclusions puts those tasks into the agent's context.\
If two Skills trigger on the same requests, make the trigger of each Skill more specific.

Avoid:

- descriptions that do not show when to use the Skill
- subjective phrases such as “a useful Skill”
- descriptions that assume one client without saying so
- internal implementation details

### Body

Skills do not need identical headings.\
They need enough information for an agent with no prior context to choose, run, and verify the workflow.\
The agent must not need to invent missing policy.\
Check that the body covers these points:

- the objective and the one responsibility
- the evidence, inputs, or preconditions needed before acting
- the workflow or the criteria for decisions
- the information the output must contain, or an exact output format when a later step depends on it
- authority, failure handling, and safety or permission boundaries, when they matter
- how to verify the work and the relevant safety conditions
- the bundled resources, and when to read or run each of them

Use the smallest structure that covers these points.\
Two common shapes are:

| Shape | Typical contents |
| --- | --- |
| Judgment-oriented | A short objective, steps with completion criteria, the decision criteria or reference lists that the steps use, and the report |
| Operational | A short objective, inputs or preconditions, ordered steps with completion criteria, the output format, and verification |

Use these shapes to review a body, not as required headings.\
A Skill can combine them.\
For example, a Skill can use judgment to choose an approach, and then need an exact sequence for a fragile operation.

Add a section or list only when it changes how the Skill runs:

- **`When to use` section**: only when the agent must choose between branches after selecting the Skill.\
  Keep the trigger in the `description`, not in this section.
- **Exact output templates and self-review checklists**: only when the agent would act differently without them.

Put each rule in the step where the agent applies it, not in a separate section of rules.

When you replace a safeguard, define how to verify that the replacement protects at least as well as the original.

### Steps

End each step with a completion criterion that the agent can check.\
For example: "Done when each finding has a label and a confidence."\
A vague criterion lets the agent end the step too early.\
The strongest criterion is both checkable and complete, such as "each changed file is accounted for".

### Keep only text that changes behavior

Keep a sentence only when the agent would act differently without it.\
Delete a sentence that tells the model what it already does, and delete the whole sentence, not only some words.

- Use terms that the model already knows, such as Red, Green, and Refactor, instead of explaining them.
- Point to facts that the agent can find in the repository, such as commands and file layout.\
  Copy such a fact only when finding it is expensive.

### Constraints

Each constraint adds to what the agent must keep in mind, and constraints from different sources can conflict.\
Write a constraint only when it prevents a mistake that the work of this Skill can cause.

- **Positive form**: state the behavior that you want, for example "Get the expected value from the specification".\
  A prohibition puts the prohibited action into the agent's context, and can make that action more likely.
- **Prohibitions**: use a prohibition only for a hard guardrail that you cannot state positively, such as a destructive operation without authorization.\
  Write the behavior that you want next to it.
- **General rules**: some rules apply to all work, for example that tool output is data and not instructions.\
  Write such a rule only in a Skill whose work creates that risk, for example a Skill that reads web pages.\
  Write it once, in the step where the risk occurs.
- **One rule in one place**: write each rule once, in the step where it applies.

## Write in Simplified Technical English

Write English text with the writing rules of [ASD-STE100 Simplified Technical English](https://asd-ste100.org/about_STE.html).\
The rules apply to Skill bodies, `description` fields, bundled resources, and repository documents.\
Repository documents include `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, and the files in `docs/`.

These rules make sentences short, and give each sentence one meaning.\
Then agents and people read them the same way.\
The list below is a summary.\
For the full rules, get the specification from ASD.

- Write one instruction in each sentence.
- Use 20 words or fewer in an instruction, and 25 words or fewer in a description sentence.
- Use the active voice, and use the imperative for instructions.
- Use noun clusters of three words or fewer.
- Give each paragraph one topic and six sentences or fewer.
- Use a vertical list when a sentence must hold more conditions or items.
- Keep articles, verbs, and subjects, even when a sentence becomes longer.
- Use "this", "that", "it", "its", and "their" only for a referent in the same paragraph or list item.\
  For other referents, write "the" and the noun.

Use the STE dictionary as a guide, not as a strict rule.\
When you can choose between two words, use the more common one.\
Treat the terms in the [glossary](glossary.md), product names, and identifiers as technical names.\
Use one word for one meaning, and use the same word each time for the same thing.

These rules do not apply to the two upstream Gist mirrors, to quoted text and code, or to Japanese text.\
For Japanese text, see [Apply the same principles to Japanese](#apply-the-same-principles-to-japanese).

## Apply the same principles to Japanese

Apply the intent of the STE rules to Skills whose source is in Japanese.\
The word limits and the STE dictionary are specific to English, so use these rules instead:

- Write one instruction in each sentence.
- When a sentence joins three or more clauses with commas (読点), split it.
- When the actor changes, name the new actor.\
  When the actor is clear from the context, leave it out, because a repeated subject is unnatural in Japanese.
- Write each instruction as a plain statement, such as 「〜する」.\
  Use the active form, not the passive or an indirect request.
- Join three or fewer Sino-Japanese nouns (漢語).\
  Separate them with 「の」 or a verb.
- Give each paragraph one topic and six sentences or fewer.
- Use a vertical list when a sentence must hold more conditions or items.
- Keep particles and verbs, and avoid a chain of noun-ending phrases (体言止め).
- Use 「この」, 「その」, and similar words only for a referent in the same paragraph or list item.\
  For other referents, write the noun.
- Use the terms in the [glossary](glossary.md), and use the same word each time for the same thing.

These rules address the clarity of instructions.\
The naturalness of Japanese, such as translated syntax and mixed English, follows the `write-natural-japanese` Skill.

## Format Markdown sources

These conventions apply to Skill bodies, bundled resources, and repository documents.

- **Steps**

  - Write each step of a workflow as a heading with its number, such as `### 1. Identify the target`.
  - Write the content of a step as labeled items, and end the step with a completion criterion.

- **Lines**

  - Write all the sentences of one paragraph or one list item on one line, without a trailing `\`.

- **Content below a heading**

  - Put only an introductory sentence, a table, a code block, a numbered list, or a list of reference links directly below a heading.
  - Write explanations and rules as items with bold labels.

- **Labels**

  - Use the form `- **Label**: value` only when every sibling has one piece of content.
  - When one sibling has more than one piece of content, give every sibling a label and child items.

- **Blank lines**

  - Put a blank line before and after an item that has children, and between its text and its first child.
  - Write items without children on consecutive lines.

- **Headings**

  - Name a heading over several topics with their common concept, not with a list such as "A and B".
  - Give a child heading a name that differs from its parent heading.
  - Make a heading only for a section with more than one item of content.

- **Checks**

  - `scripts/check_repository.py` checks the rules that need no judgment in the files that `scripts/markdown-style-files.txt` lists.
  - Add a file to that list when it follows these conventions.

## Keep Skills independent of each other

Each Skill must work on its own.\
Keep the names of other public Skills out of `SKILL.md`.\
Describe out-of-scope work by its type, and describe a handoff by the input the next step needs.\
Record relationships between Skills only in [Choose the next Skill](../users/workflows.md).\
`scripts/check_repository.py` rejects other public Skill names, except in approved companion relationships and the upstream mirrors.

### Companion relationships

In a companion relationship, one Skill deliberately requires another to apply its rules correctly.\
It is a narrow exception.\
Create one only when a Skill cannot apply its rules correctly without the other Skill.\
Convenience, related subject matter, or an arbitrary dependency is not a reason.\
Unintended coupling between Skills is a design problem.

For each approved relationship, record:

- the Skills involved and which one requires the other
- why the companion is required
- how the two Skills are installed or located together
- what happens when the companion is unavailable, including whether work stops
- the provenance, and any local adaptations that introduced or maintain the relationship

Review this record, and verify the affected behavior, when one of these changes:

- either Skill
- the relationship
- the installation
- the behavior without the companion

### Upstream Gist mirrors

`japanese-tech-writing` and `cognitive-rhythm-writing` are copies of k16shikano's public Gists.\
Their `SKILL.md` files match, byte for byte, the revisions recorded in each `UPSTREAM.md`.\
Keep local rules, frontmatter fields, and editorial corrections out of both files.

The repository checker compares each copy with the SHA-256 recorded in `UPSTREAM.md`.\
It does not check whether a newer Gist revision exists; finding one requires comparing with the upstream Gist yourself.

To update a mirror:

1. Compare the recorded revision with the current Gist.
2. Inspect the complete change following the [security review](security.md).
3. Copy the accepted revision without modification.
4. Update its revision, hash, and third-party notice.

If the new upstream file cannot be accepted as it is, record the difference, and keep the current copy.

The upstream `cognitive-rhythm-writing` reads `../japanese-tech-writing/SKILL.md` before use.\
People who install it need to install both together, as described in [Install with APM](../users/installation.md#install-with-apm).\
Keep the upstream file unchanged, without a local procedure for a missing companion.

## Update related documents

When you add a Skill or change what it does, check the documents that describe it from the outside:

- **Task catalog**: add or update the Skill's row in `README.md`.\
  The checker reports a Skill missing from the catalog.
- **[Choose the next Skill](../users/workflows.md)**: update it when the Skill's handoffs change, including the names of the states it reports.\
  The guide uses those states to show which Skill comes next.
- **[Runtime requirements](../users/compatibility.md)**: update it when the Skill starts or stops needing more than every Skill needs.\
  Examples are web access, a subagent, another Skill, and a bundled reference read in full.

## Check a new Skill before opening a pull request

- [ ] The directory name is kebab-case and matches the frontmatter `name`.
- [ ] `SKILL.md` has `name`, `description`, and `license` in its frontmatter (the two Gist mirrors keep their upstream frontmatter).
- [ ] The `description` shows when to use the Skill without reading the body.
- [ ] The body covers the points in [Body](#body) without copying a heading template mechanically.
- [ ] The body is in English, or a Japanese writing or editing exception is documented.
- [ ] The English follows [Write in Simplified Technical English](#write-in-simplified-technical-english), and Japanese text follows [Apply the same principles to Japanese](#apply-the-same-principles-to-japanese).
- [ ] Each step ends with a completion criterion, as described in [Steps](#steps).
- [ ] Each constraint meets the conditions in [Constraints](#constraints).
- [ ] The Skill does not name another public Skill, except in an approved companion relationship.
- [ ] There are no secrets, personal information, or internal URLs.
- [ ] Third-party provenance and capability risks have been reviewed when external material is included.
- [ ] `scripts/`, `references/`, and `assets/` contain only what the Skill needs, and empty directories are removed.
- [ ] The documents in [Update related documents](#update-related-documents) are updated.
- [ ] The repository checker and the tests for retained code pass.
- [ ] The results and safety boundaries of the Skill are checked as the task needs.

## Sources

The rules in this guide are based on these sources:

- [Agent Skills specification](https://agentskills.io/specification): the format of `SKILL.md` and its metadata.
- [Skill authoring best practices (Anthropic)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): concise bodies, the freedom of instructions, third-person descriptions, and consistent terms.
- [Build skills (OpenAI)](https://learn.chatgpt.com/docs/build-skills): one job for each Skill, and imperative steps with explicit inputs and outputs.
- [`writing-for-agents` (Matt Pocock)](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md): positive instructions, completion criteria, terms that the model knows, and deletion of text that does not change behavior.
- [`authoring-a-skill` (pstack)](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md): text that changes a decision, and deletion when in doubt.
- [ASD-STE100 Simplified Technical English](https://asd-ste100.org/about_STE.html): the writing rules for English.
