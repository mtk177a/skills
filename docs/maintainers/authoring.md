# Skill authoring guide

This guide is for maintainers and the agents working for them.\
It explains how to design, write, and check the Skills maintained in this repository.

The two upstream Gist mirrors are an exception.\
They follow the copying rules in [Upstream Gist mirrors](#upstream-gist-mirrors), and the rules in this guide never justify changing their `SKILL.md` files.

Follow [Languages and Japanese reference translations](localization.md) for the language of Skill bodies and for updating translations.

## Design the Skill

### Responsibility

Give each Skill one responsibility and a clear context in which to use it.\
Prioritize these design decisions:

- Design workflows that need judgment from the intended outcome and evidence, not from a predetermined artifact.
- Match the freedom of the instructions to how fragile the task is and how much it depends on context.\
  When several approaches are valid, state goals and constraints.\
  When order or completeness affects correctness, give short ordered steps and a way to verify them.
- Keep complete diagnosis separate from staged implementation or rollout.
- Do not set arbitrary limits on how much to investigate or how many findings to report.

When comparing a new Skill with existing ones, read only the examples needed to resolve overlapping responsibilities and reach a judgment.\
Stop when that purpose is met, and do not read the whole catalog without a reason.

Put design guidance that must travel with a Skill in that Skill's own `references/` directory.

### Name

Name the Skill as an action and an object in kebab-case, such as `clarify-request` or `design-changes`, so that the name shows its responsibility and when to use it.\
Prefer clarity over brevity, and avoid names that suggest a broader scope than the Skill has.\
Use a single word, such as `build`, only when the responsibility is narrow enough that the word cannot be misread.

### Description

The `description` is what an agent reads to decide whether to use the Skill, so it is not a general explanation.\
Include:

- the situation in which to use the Skill
- the kind of work it helps with
- any dependency on a specific agent, and what that dependency is

Write about when to use the Skill rather than how it runs.\
Put everything needed for automatic selection in the `description`, and put what the agent needs after loading the Skill, such as roles, orchestration, and execution details, in the body.

Avoid:

- vague descriptions that do not show when to use the Skill
- subjective phrases such as “a useful Skill”
- descriptions that assume Codex without saying so
- internal implementation details in the frontmatter

### Body

Skills do not need identical headings.\
They do need enough information for an agent with no prior context to choose, run, and verify the workflow without inventing missing policy.\
Check that the body covers these responsibilities:

- the objective and one coherent responsibility
- complete trigger context, and any important exclusions, in `description`
- the evidence, inputs, or preconditions needed before acting
- the workflow or decision logic
- the required output information, or an exact output format when a later step depends on it
- authority, failure handling, and safety or permission boundaries when they matter
- verification of the work and of the relevant safety conditions
- bundled resources, and when to read or run them

Use the smallest structure that covers these responsibilities.\
Two common shapes are:

| Shape | Typical contents |
| --- | --- |
| Judgment-oriented | Objective, evidence, workflow, optional decision criteria, reporting contract, and boundaries |
| Operational | Objective, inputs or preconditions, ordered steps, output format, verification, and boundaries |

These shapes are for review, not required headings.\
A Skill can combine them when it uses judgment to choose an approach and then needs an exact sequence for a fragile operation.

Do not add a `When to use` section that only repeats the `description`.\
Keep one only when the agent needs to choose between branches after the Skill has been selected.\
Likewise, use exact output templates, `Always` / `Ask first` / `Never` lists, and self-review checklists only when they change how the Skill runs.

When you replace a safeguard, define how to verify that the replacement protects at least as well.

When you change a Skill's instructions or resources, also review its entry in [Runtime requirements and client differences](../users/compatibility.md) and the references packaged with it.

## Keep Skills independent of each other

Each Skill must work on its own.\
Do not name another public Skill in `SKILL.md` or `SKILL-ja.md`.\
Describe out-of-scope work by its type, and describe a handoff by the input the next step needs.\
Record relationships between Skills only in the [Skill workflow guide](../users/workflows.md).\
`scripts/check_repository.py` enforces this rule, except for approved companion relationships and the upstream mirrors.

### Companion relationships

A companion relationship is a narrow exception: one Skill deliberately requires another to apply its rules correctly.\
Do not create one for convenience, related subject matter, or an arbitrary dependency.\
Unintended coupling between Skills remains a design problem.

Record the following for each approved relationship:

- the direction of the relationship and the Skills involved
- why the companion is required
- the supported installation method
- what happens when the companion is unavailable, including whether work stops
- the provenance and local adaptations that introduced or maintain the relationship

When either Skill, the relationship, the installation method, or the behavior without the companion changes, review this record and verify the affected behavior.

### Approved: Japanese reference maintenance

| Required relationship | Provenance |
| --- | --- |
| `maintain-japanese-references` → `write-natural-japanese` | Original repository material. [#42](https://github.com/mtk177a/skills/pull/42) introduced the maintenance Skill; [#77](https://github.com/mtk177a/skills/issues/77) records the required relationship and Japanese-canonical exception |

- **Reason**: to keep the English meaning while using Japanese that fits the context.
- **Location**: both Skills are tracked in this repository.
- **Before use**: read `skills/write-natural-japanese/SKILL.md` and its required references.\
  If a repository file is unavailable, stop and report it instead of substituting a personal copy.

The upstream `cognitive-rhythm-writing` also requires another Skill; see [Upstream Gist mirrors](#upstream-gist-mirrors).

## Support multiple agents

### Shared and agent-specific Skills

First, check whether the Skill can be written without depending on a particular agent:

- A shared Skill serves the same purpose with the same steps across several agents.
- An agent-specific Skill has steps, tool availability, or input and output formats tied to one agent.

This repository does not use classification directories.\
Show differences in the Skill name or `description` instead.

Add client-specific metadata only when a Skill needs the corresponding invocation control, UI, dependency declaration, or permission behavior.\
Otherwise, keep `name`, `description`, instructions, and resources portable.

### Adapt a Codex-only Skill for other agents

When adapting a Codex-specific Skill for Claude Code or GitHub Copilot, decide whether its Codex-specific language should stay.\
Keep it only when that specificity is the core value of the Skill.\
Otherwise, rewrite the Skill around its purpose and decision criteria so that the mechanics can be swapped.

Do not infer how a client discovers, loads, or prioritizes instruction files, or how it invokes Skills, from format compatibility alone.\
When these behaviors affect a design, check the current official documentation for each target client.\
Where the documentation is conditional or incomplete, verify the behavior in the target version or environment.\
Use the result for the current decision instead of maintaining a list of client behaviors here.

When adapting, check:

- whether the Skill relies too much on specific tool names
- whether the request and output formats make sense for other agents
- whether the steps assume Codex-specific features
- whether agent-specific differences are described in `description` or the body
- whether shared guidance has one source, and client-specific bridge files duplicate only a documented minimum of safety and approval rules
- whether any retained safety and approval fallback still matches its source rules
- whether a requirement needs behavioral guidance or a client-enforced policy, permission, or hook

### Shared and client-specific instruction files

Keep shared repository instructions in `AGENTS.md`.

- **Copilot bridge**: instruct Copilot to read `AGENTS.md`.\
  If it cannot, Copilot stops without modifying files, running commands, or changing external state.
- **Clients that do not load `AGENTS.md` automatically**: repeat in the bridge only the minimum safety and approval rules needed to keep those boundaries.\
  This fallback is a delivery measure, not a second source of the rules.
- **Updates**: when a related rule in `AGENTS.md` changes, check and update the fallback.\
  Do not duplicate other shared rules.

Current client documentation: [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code project instructions](https://code.claude.com/docs/en/memory), and [GitHub Copilot custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support).

## Bundle only the resources needed

### Scripts

When adding `scripts/`, check what they need to run and what side effects they have:

- Minimize dependencies on a particular shell, OS, or architecture.
- Document any additional dependencies.
- Do not depend on absolute paths outside the repository.
- If a script performs destructive operations, make the Skill body ask for confirmation before running it.
- Do not add generated artifacts or caches to the repository.

Avoid scripts that would not work on both macOS M1 and Windows WSL unless the need is explicitly justified.

### References

The `references/` directory holds material the Skill needs when making judgments, such as formats, specifications, and decision criteria:

- Include only what an agent with no prior context needs to apply the Skill.
- Do not copy external documents verbatim; link to the original instead.
- Do not store temporary notes or customer-specific information.
- Check the license of any material you include, and do not bundle content under an incompatible license.

### Assets

The `assets/` directory holds supplementary material to distribute, such as images, reusable templates, or small structured data:

- Include only material with clear provenance and a compatible license.
- Do not add generated artifacts, caches, or temporary files.
- Keep large binary files out of the repository unless they are truly necessary.

## Keep secrets and private information out

Never include the following in Skill bodies, scripts, references, or assets:

- API keys, tokens, or passwords
- customer names or personal information
- internal URLs, internal procedures, or other non-public operational information
- references to secret files that exist only in a local environment

Write Skills on the assumption that other environments and agents may read them.\
For environment-specific information, use variable names or placeholders.

## Import external Skills

### When to fork or copy an external Skill

Apart from the two Gist mirrors, external Skills are not copied into this repository as they are.\
Installing external Skills is managed in dotfiles through `apm.yml` and `apm.lock.yaml`.

Bring a Skill into this repository only when at least one of these applies:

- you need to keep modifying and maintaining it yourself
- redesigning it from scratch is better than using it as it is
- you want to restructure it for your own workflow

Even then, align its frontmatter and `description` with this repository's conventions instead of importing it verbatim.

Before adopting or adapting a third-party Skill, review its provenance, license, complete set of files, external references, scripts, tool and network use, and combined capabilities.\
Treat its Markdown instructions as something that can make an agent act, not as inherently safe text.\
Follow the [security review](security.md) for the repository checklist.

### Upstream Gist mirrors

`japanese-tech-writing` and `cognitive-rhythm-writing` are copies of k16shikano's public Gists.\
Their `SKILL.md` files match, byte for byte, the revisions recorded in each `UPSTREAM.md`.\
Do not add local rules, frontmatter fields, editorial corrections, or a Japanese reference translation to either file.

The repository checker compares each copy with the SHA-256 recorded in `UPSTREAM.md`.\
It does not check whether a newer Gist revision exists; that requires an explicit comparison with the upstream Gist.

To update a mirror:

1. Compare the recorded revision with the current Gist.
2. Inspect the complete change following the [security review](security.md).
3. Copy the accepted revision without modification.
4. Update its revision, hash, and third-party notice.

If the new upstream file cannot be accepted as it is, record the difference and do not create a local variant.

The upstream `cognitive-rhythm-writing` requires `../japanese-tech-writing/SKILL.md` before use.\
Install both together with the [selected installation](../users/installation.md#install-with-apm).\
Do not add a local procedure for a missing companion to the upstream file.

## Check a new Skill before opening a pull request

- [ ] The directory name is kebab-case and matches the frontmatter `name`.
- [ ] `SKILL.md` exists with `name`, `description`, and `license` in its frontmatter (the two Gist mirrors keep their upstream frontmatter).
- [ ] The `description` shows when to use the Skill without reading the body.
- [ ] The body covers the responsibilities in [Body](#body) without copying a heading template mechanically.
- [ ] The body is in English, or a Japanese writing or editing exception is documented.
- [ ] A Japanese reference translation, `SKILL-ja.md`, exists unless `SKILL.md` is the documented Japanese source.
- [ ] The Skill does not name another public Skill, except in an approved companion relationship.
- [ ] There are no secrets, personal information, or internal URLs.
- [ ] Third-party provenance and capability risks have been reviewed when external material is included.
- [ ] `scripts/`, `references/`, and `assets/` contain only what the Skill needs, and empty directories are removed.
- [ ] The repository checker and the tests for retained code pass, and the Skill's results and safety boundaries have been checked as appropriate.
