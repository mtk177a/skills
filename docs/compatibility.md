# Compatibility

This document separates portable Agent Skills format compatibility from client-specific discovery, invocation, permissions, and execution behavior. A Skill can be structurally valid and still fail to load, trigger, or execute as intended in a particular client.

The repository uses four evidence states. Each state applies only to the scope recorded for it and does not imply any unrecorded client behavior.

| State | Meaning |
| --- | --- |
| Format-compatible | The Skill package follows the Agent Skills specification. This does not establish that a client discovers or runs it. |
| Documented | Current official client documentation describes the relevant discovery, invocation, extension, or runtime behavior. The repository has not necessarily executed it. |
| Locally verified | A client version, date, and observed discovery or invocation result are recorded. Unobserved invocation paths remain unverified. |
| Behavior-tested | Targeted evaluation evidence records whether the Skill was selected and followed for a defined scenario set. This is scoped evidence, not a general support guarantee. |

## Compatibility layers

| Layer | Question |
| --- | --- |
| Format | Does the package provide a valid `SKILL.md` and directly discoverable resources? |
| Discovery and installation | Where does the client look, and how is the Skill delivered there? |
| Invocation | Can users invoke it explicitly, can the model select it implicitly, and can either path be disabled? |
| Client extensions | Does behavior depend on client-specific metadata, UI, tools, or lifecycle features? |
| Enforcement | Which permissions, sandbox, policy, or hook mechanisms actually constrain execution? |
| Runtime | Are scripts, dependencies, filesystem access, and network access available in the target environment? |
| Verification | Which of the preceding behaviors has been observed locally with a recorded version and date? |

Format compatibility is not evidence of client discovery, invocation, or behavioral compatibility. Official documentation establishes documented client behavior; only recorded local execution establishes local verification or behavior-tested status.

## Client matrix

| Client or layer | Documented posture |
| --- | --- |
| Codex | Official documentation describes implicit selection and, in Codex CLI or the IDE extension, explicit invocation through `/skills` or a `$` Skill mention. Optional `agents/openai.yaml` provides OpenAI-specific appearance and dependency metadata. Sandbox, approval, rules, tools, and runtime access remain separate from Skill prose. |
| Claude Code | Official documentation describes its own Skill discovery, invocation, frontmatter, permission, and hook behavior. These client-specific controls do not follow from portable Skill format compatibility. |
| GitHub Copilot / `gh skill` | Client-specific discovery, invocation, metadata, permissions, and runtime behavior must be checked against current official documentation and the target version. |
| Gemini CLI | Client-specific discovery, invocation, metadata, permissions, and runtime behavior must be checked against current official documentation and the target version. |
| Other clients | A client may be able to consume the standard package, but format compatibility alone does not establish discovery or execution. |
| APM | APM distributes the root `skills/` directory as a native `SKILL_BUNDLE`; it is not an execution client. Target selection and installation layout do not establish downstream invocation or behavior. |

Do not add client-specific metadata to every Skill merely because a client supports it. Add it only when the Skill needs that client's invocation control, UI presentation, tool dependency declaration, or permission behavior. Keep portable `name`, `description`, instructions, and resources as the common layer.

## Plugin runtime requirements

`mtk177a-skills` packages the public Skills without changing their instructions.\
Packaging makes those instructions and their resources available together; it does not provide the tools or permissions needed to carry them out.\
Use the inventory below to check the requirements for the intended task.

The executing agent must be able to read all bundled references; each Skill determines which references to read for the task.\
None of the current Skills bundles an executable script or requires installing a Python dependency, but tool-dependent tasks still need the target environment's tools and authorization.

| Task and Skills | Required inputs or capabilities |
| --- | --- |
| Clarify a request or decision: `clarify-request`, `define-referents`, `explore-decision-space`, `calibrate-learning-support` | Conversation and task context; access to external facts when they affect the judgment. `define-referents` also requires reading its bundled reference. |
| Write or explain: `make-it-click`, `structure-what-you-write`, `write-natural-japanese` | Text and context, plus the bundled references selected or required by the Skill. Saving the result requires authorized write access. |
| Write Japanese technical prose: `japanese-tech-writing`, `cognitive-rhythm-writing` | Text to write or revise. `cognitive-rhythm-writing` requires reading the adjacent `japanese-tech-writing/SKILL.md`. |
| Assess execution conditions: `choose-ai-execution-setup`, `assess-risky-change-readiness` | Evidence of available environments, capabilities, controls, and authority. Advice does not supply these capabilities or authorize execution. |
| Design a change: `design-changes`, `design-agent-instructions`, `design-skill` | Access to relevant existing implementation, instructions, and constraints. These Skills produce designs, not implemented changes. |
| Investigate guidance or failures: `audit-agent-guidance`, `investigate-failure`, `break-failure-loop` | In-scope guidance, evidence of failures or previous attempts, and relevant read-only inspection tools. Missing behavioral evidence remains unverified. |
| Edit repository content: `curate-repo-docs`, `implement-changes` | Target files, applicable repository rules, authorized write access, and the required validation tools. Missing execution capability cannot be reported as successful implementation. |
| Review changes or findings: `review-changes`, `validate-fix`, `triage-review-feedback` | The actual diff, fix, or findings and relevant source/specification evidence. Commands or live checks require corresponding tools; untested claims remain unverified. |
| Draft a change summary or tracker item: `draft-commit`, `draft-issue`, `draft-review-comments`, `summarize-changes` | A scoped change set, grounded request, or supplied findings, as required by each Skill. Repository or tracker access is needed when the evidence requires it; drafting does not publish. |
| Record a handoff: `record-session-handoff` | Evidence of the current task and, when available, authorized access to save the result. Otherwise, return the draft or not-written result specified by the Skill. |
| Research the web: `research-web-safely` | Live search/retrieval and observable citations. Unavailable sources or tools cannot support a claim of verification. |
| Revise with a fresh agent: `revise-docs-fresh-eyes` | Codex or Claude Code, access to the artifact, and an authorized independent subagent without the authoring conversation. If subexecution is unavailable or prohibited, stop; rewriting in the same context is not a substitute. |

The package includes the authoring reference for `design-skill`, the document-decision and TDD references used by the editing Skills, and both unmodified Gist mirrors with their provenance files.\
The mirror pair's required reading relationship is preserved by keeping them adjacent.\
A mention of another workflow does not, by itself, make that Skill a mandatory companion.

Repository-only `maintain-japanese-references` is excluded from public distribution.\
Its dependency on the public `write-natural-japanese` Skill does not make the maintenance Skill public.\
When instructions or resources change, review both the affected requirements above and the references in the package.

## Installation paths

### Claude Code through APM

```bash
apm install mtk177a/skills
```

Or declare the package in `apm.yml`:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### Individual Skill

```bash
apm install mtk177a/skills/skills/review-changes
```

APM may target multiple clients. Verify the resolved path and discovery behavior for the specific target instead of treating the installation command as execution evidence.

## Validation

Use `skills-ref` when it is available to check Agent Skills format conformance:

```bash
skills-ref validate
```

Distribution changes require a pushed candidate commit. Verify that exact commit from disposable consumer directories outside this repository, covering the full bundle, affected `--skill` selections, affected individual Skill paths, and the consumer-generated lockfile:

```bash
apm install 'mtk177a/skills#<commit>' --target agent-skills --no-policy
apm install --frozen --dry-run --no-policy
apm audit --ci --no-policy
```

These commands do not prove triggering, instruction following, permission behavior, or output quality. Use the targeted evaluation procedure in [evaluation.md](evaluation.md) for those claims and [security.md](security.md) for third-party and executable capability review.

## Current sources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)

Client extensions and runtime behavior change more frequently than the core package format. Recheck the current official source when one of those details affects a design or audit.
