# Skill authoring guide

This guide is for maintainers and the agents working for them.\
It explains how to design, write, and check the Skills maintained in this repository, and what else to update when a Skill changes.\
Read it before you create a Skill or change what an existing Skill does.

The two upstream Gist mirrors are an exception.\
They follow the copying rules in [Upstream Gist mirrors](#upstream-gist-mirrors), and the rules in this guide never justify changing their `SKILL.md` files.

## Design the Skill

### Responsibility

Give each Skill one responsibility and a clear situation in which to use it.\
Within that responsibility, prioritize these decisions:

- **Start from the outcome**: design a workflow that needs judgment from the intended outcome and the evidence, not from a predetermined artifact.
- **Match the freedom of the instructions to the task**: when several approaches are valid, state the goals and constraints.\
  When order or completeness affects correctness, give short ordered steps and a way to verify them.
- **Report the whole diagnosis**: even when a fix will be implemented or rolled out in stages, do not drop findings to fit the first stage.
- **Do not set arbitrary limits**: do not cap how much to investigate or how many findings to report.

To check whether a new Skill overlaps an existing one, read only the existing Skills needed to settle the overlap.\
Stop when it is settled, and do not read the whole catalog without a reason.

### Name

Name the Skill with an action and an object in kebab-case, such as `clarify-request` or `design-changes`, so that the name shows its responsibility and when to use it.\
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

Keep the `description` simple.\
Add a case in which not to use the Skill only when the `description` would otherwise trigger on requests that another Skill handles.

Avoid:

- descriptions that do not show when to use the Skill
- subjective phrases such as “a useful Skill”
- descriptions that assume one client without saying so
- internal implementation details

### Body

Skills do not need identical headings.\
They do need enough information for an agent with no prior context to choose, run, and verify the workflow without inventing missing policy.\
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
| Judgment-oriented | Objective, evidence, workflow, optional decision criteria, reporting contract, and boundaries |
| Operational | Objective, inputs or preconditions, ordered steps, output format, verification, and boundaries |

Use these shapes to review a body, not as required headings.\
A Skill can combine them, for example when it uses judgment to choose an approach and then needs an exact sequence for a fragile operation.

Add a section or list only when it changes how the Skill runs:

- **`When to use` section**: only when the agent must choose between branches after selecting the Skill.\
  Do not add one that repeats the `description`.
- **Exact output templates, `Always` / `Ask first` / `Never` lists, and self-review checklists**: only when the agent would act differently without them.

When you replace a safeguard, define how to verify that the replacement protects at least as well as the original.

## Keep Skills independent of each other

Each Skill must work on its own.\
Do not name another public Skill in `SKILL.md` or `SKILL-ja.md`.\
Describe out-of-scope work by its type, and describe a handoff by the input the next step needs.\
Record relationships between Skills only in [Choose the next Skill](../users/workflows.md).\
`scripts/check_repository.py` rejects other public Skill names, except in approved companion relationships and the upstream mirrors.

### Companion relationships

In a companion relationship, one Skill deliberately requires another to apply its rules correctly.\
It is a narrow exception.\
Do not create one for convenience, related subject matter, or an arbitrary dependency, because unintended coupling between Skills remains a design problem.

For each approved relationship, record:

- the Skills involved and which one requires the other
- why the companion is required
- how the two Skills are installed or located together
- what happens when the companion is unavailable, including whether work stops
- the provenance, and any local adaptations that introduced or maintain the relationship

When either Skill, the relationship, the installation, or the behavior without the companion changes, review this record and verify the affected behavior.

### Approved: Japanese reference maintenance

| Required relationship | Provenance |
| --- | --- |
| `maintain-japanese-references` → `write-natural-japanese` | Original repository material. [#42](https://github.com/mtk177a/skills/pull/42) introduced the maintenance Skill; [#77](https://github.com/mtk177a/skills/issues/77) records the required relationship and Japanese-canonical exception |

- **Reason**: to keep the meaning of the English source while writing Japanese that fits the context.
- **Location**: both Skills are tracked in this repository.
- **Before use**: read `skills/write-natural-japanese/SKILL.md` and its required references.\
  If a repository file is unavailable, stop and report it instead of substituting a personal copy.

The upstream `cognitive-rhythm-writing` also requires another Skill; see [Upstream Gist mirrors](#upstream-gist-mirrors).

## Support several clients

### Shared and client-specific Skills

First, decide whether the Skill can be written without depending on a particular client:

- A shared Skill serves the same purpose with the same steps in several clients.
- A client-specific Skill has steps, tools, or input and output formats tied to one client.

This repository does not sort Skills into directories by client.\
Show a client-specific dependency in the Skill name or `description` instead.

Add client-specific metadata only when a Skill needs that client's invocation control, UI, dependency declaration, or permission behavior.\
Otherwise, keep `name`, `description`, instructions, and resources portable.

### Adapt a Skill written for one client

When you adapt a Skill written for one client, such as Codex, for other clients, decide whether its client-specific language should stay.\
Keep it only when that specificity is the core value of the Skill.\
Otherwise, rewrite the Skill around its purpose and decision criteria so that the client-specific mechanics can be swapped.

Check:

- whether the Skill relies too much on specific tool names
- whether the request and output formats make sense in other clients
- whether the steps assume features of one client
- whether the remaining client-specific differences are stated in the `description` or the body
- whether a requirement needs instructions in the Skill, or a policy, permission, or hook that the client enforces

Do not infer from format compatibility how a client discovers, loads, or prioritizes instruction files, or how it invokes Skills.\
When these behaviors affect a design, check the current official documentation for each target client.\
Where the documentation is conditional or incomplete, verify the behavior in the target version or environment.\
Use the result for the current decision; this guide does not keep a list of client behaviors.

### Shared and client-specific instruction files

Keep shared repository instructions in `AGENTS.md`.\
A client-specific instruction file only bridges to it:

- **Copilot bridge**: `.github/copilot-instructions.md` tells Copilot to read `AGENTS.md`.\
  If Copilot cannot read it, Copilot stops without modifying files, running commands, or changing external state.
- **Clients that do not load `AGENTS.md` automatically**: repeat in the bridge only the minimum safety and approval rules needed to keep those boundaries.\
  This fallback delivers the rules to that client; it is not a second source of them.
- **Updates**: when a related rule in `AGENTS.md` changes, check and update the fallback.\
  Do not copy other shared rules into the bridge.

Current client documentation: [Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude Code project instructions](https://code.claude.com/docs/en/memory), and [GitHub Copilot custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support).

## Bundle only the resources needed

### Scripts

When you add `scripts/`, check what the scripts need to run and what side effects they have:

- Minimize dependencies on a particular shell, OS, or architecture.\
  Do not add a script that would not work on both macOS M1 and Windows WSL unless the need is explicitly justified.
- Document any additional dependencies.
- Do not depend on absolute paths outside the repository.
- If a script performs destructive operations, make the Skill body ask for confirmation before running it.
- Do not add generated artifacts or caches to the repository.

### References

The `references/` directory holds material the Skill needs for its judgments, such as formats, specifications, and decision criteria:

- Include only what an agent with no prior context needs to apply the Skill.
- Do not copy external documents verbatim; link to the original instead.
- Do not store temporary notes or customer-specific information.
- Check the license of any material you include, and do not bundle content under an incompatible license.

### Assets

The `assets/` directory holds supplementary material that the Skill uses, such as images, reusable templates, or small structured data:

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

### When to bring an external Skill into this repository

Apart from the two Gist mirrors, this repository does not copy external Skills as they are.

Bring an external Skill into this repository only when at least one of these applies:

- you need to keep modifying and maintaining it yourself
- redesigning it from scratch is better than using it as it is
- you want to restructure it for your own workflow

Even then, align its frontmatter and `description` with this repository's conventions instead of importing it verbatim.

Before you adopt or adapt a third-party Skill, review its provenance, license, complete set of files, external references, scripts, tool and network use, and what it can do when these are combined.\
Treat its Markdown instructions as something that can make an agent act, not as harmless text.\
Follow the [security review](security.md) for the checklist.

### Upstream Gist mirrors

`japanese-tech-writing` and `cognitive-rhythm-writing` are copies of k16shikano's public Gists.\
Their `SKILL.md` files match, byte for byte, the revisions recorded in each `UPSTREAM.md`.\
Do not add local rules, frontmatter fields, editorial corrections, or a Japanese reference translation to either file.

The repository checker compares each copy with the SHA-256 recorded in `UPSTREAM.md`.\
It does not check whether a newer Gist revision exists; finding one requires comparing with the upstream Gist yourself.

To update a mirror:

1. Compare the recorded revision with the current Gist.
2. Inspect the complete change following the [security review](security.md).
3. Copy the accepted revision without modification.
4. Update its revision, hash, and third-party notice.

If the new upstream file cannot be accepted as it is, record the difference and do not create a local variant.

The upstream `cognitive-rhythm-writing` reads `../japanese-tech-writing/SKILL.md` before use.\
People who install it need to install both together, as described in [Install with APM](../users/installation.md#install-with-apm).\
Do not add a local procedure for a missing companion to the upstream file.

## Update related documents

When you add a Skill or change what it does, check the documents that describe it from the outside:

- **Task catalog**: add or update the Skill's row in `README.md` and `README.ja.md`.\
  The checker reports a Skill missing from either catalog.
- **[Choose the next Skill](../users/workflows.md)**: update it when the Skill's handoffs change, including the names of the states it reports.\
  The guide uses those states to show which Skill comes next.
- **[Runtime requirements](../users/compatibility.md)**: update it when the Skill starts or stops needing more than every Skill needs, such as web access, a subagent, another Skill, or a bundled reference read in full.
- **Japanese reference translation**: update `SKILL-ja.md` when the meaning of `SKILL.md` changes, following [Languages and Japanese reference translations](localization.md).

## Check a new Skill before opening a pull request

- [ ] The directory name is kebab-case and matches the frontmatter `name`.
- [ ] `SKILL.md` has `name`, `description`, and `license` in its frontmatter (the two Gist mirrors keep their upstream frontmatter).
- [ ] The `description` shows when to use the Skill without reading the body.
- [ ] The body covers the points in [Body](#body) without copying a heading template mechanically.
- [ ] The body is in English, or a Japanese writing or editing exception is documented.
- [ ] `SKILL-ja.md` exists, unless `SKILL.md` is the documented Japanese source.
- [ ] The Skill does not name another public Skill, except in an approved companion relationship.
- [ ] There are no secrets, personal information, or internal URLs.
- [ ] Third-party provenance and capability risks have been reviewed when external material is included.
- [ ] `scripts/`, `references/`, and `assets/` contain only what the Skill needs, and empty directories are removed.
- [ ] The documents in [Update related documents](#update-related-documents) are updated.
- [ ] The repository checker and the tests for retained code pass, and the Skill's results and safety boundaries have been checked as appropriate.
