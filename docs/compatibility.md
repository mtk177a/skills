# Compatibility

This document separates portable Agent Skills format compatibility from client-specific discovery, invocation, permissions, and execution behavior. A Skill can be structurally valid and still fail to load, trigger, or execute as intended in a particular client.

The repository uses four evidence states. Each state applies only to the scope recorded for it and does not imply any unrecorded client behavior.

| State | Meaning |
| --- | --- |
| Format-compatible | The Skill package follows the Agent Skills specification. This does not establish that a client discovers or runs it. |
| Documented | Current official client documentation describes the relevant discovery, invocation, extension, or runtime behavior. The repository has not necessarily executed it. |
| Locally verified | The repository records a client version, date, and observed discovery or invocation result. Unobserved invocation paths remain unverified. |
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

| Client or layer | Documented posture | Repository evidence | Current state |
| --- | --- | --- | --- |
| Codex | Official documentation describes implicit selection and, in Codex CLI or the IDE extension, explicit invocation through `/skills` or a `$` Skill mention. Optional `agents/openai.yaml` provides OpenAI-specific appearance and dependency metadata. Sandbox, approval, rules, tools, and runtime access remain separate from Skill prose. | Repository-local discovery and targeted implicit selection and behavior have been observed. Explicit `/skills` and `$` invocation, UI behavior, and live permission behavior have not been executed for this repository. | Documented; locally verified and behavior-tested for the recorded scenarios; explicit invocation unverified locally |
| Claude Code | Official documentation describes its own Skill discovery, invocation, frontmatter, permission, and hook behavior. These client-specific controls do not follow from portable Skill format compatibility. | No repository installation, discovery, explicit or implicit invocation, permission, or behavior run has been recorded. | Format-compatible; runtime behavior unverified |
| GitHub Copilot / `gh skill` | Client-specific discovery, invocation, metadata, permissions, and runtime behavior must be checked against current official documentation and the target version. | No repository installation, discovery, invocation, permission, or behavior run has been recorded. | Format-compatible; runtime behavior unverified |
| Gemini CLI | Client-specific discovery, invocation, metadata, permissions, and runtime behavior must be checked against current official documentation and the target version. | No repository installation, discovery, invocation, permission, or behavior run has been recorded. | Format-compatible; runtime behavior unverified |
| Other clients | A client may be able to consume the standard package, but format compatibility alone does not establish discovery or execution. | No client is locally verified unless a versioned repository-level or Skill-level record exists. | Unverified without a versioned record |
| APM | APM distributes the root `skills/` directory as a native `SKILL_BUNDLE`; it is not an execution client. Target selection and installation layout do not establish downstream invocation or behavior. | The bundle checks listed below have been executed. | Distribution verified for the recorded scope only |

Do not add client-specific metadata to every Skill merely because a client supports it. Add it only when the Skill needs that client's invocation control, UI presentation, tool dependency declaration, or permission behavior. Keep portable `name`, `description`, instructions, and resources as the common layer.

## Representative verification snapshot

The table preserves representative observations from recorded repository checks, not support claims inferred from documentation.
It is not a current or exhaustive inventory of later Skill-level evaluations.
Record later Skill-level behavior results in the relevant Skill evaluation assets under the path-dependent evidence responsibilities in [evaluation.md](evaluation.md).
When that evidence supports a client-specific compatibility state, include the relevant client version, date, and scenario scope.

| Target | Version | Verified date | Observed scope |
| --- | --- | --- | --- |
| Claude Code | — | — | Not executed; installation, discovery, explicit and implicit invocation, permissions, and behavior are unverified |
| Codex | 0.145.0 | 2026-07-24 | Repository-local discovery, observable target Skill open in 16 baseline/candidate selection runs, and 29 candidate/baseline behavior runs including five affected reruns; explicit `/skills` and `$` invocation, UI, and live permission behavior not executed |
| GitHub Copilot / `gh skill` | — | — | Not executed; installation, discovery, invocation, permissions, and behavior are unverified |
| Gemini CLI | — | — | Not executed; installation, discovery, invocation, permissions, and behavior are unverified |
| APM | 0.26.0 | 2026-09-15 | native bundle installation, `--skill` selection, individual Skill path installation, consumer-side frozen install, audit |
| Other clients, including `npx skills add` consumers | — | — | Not executed unless separately recorded |

When adding a client-level result to this snapshot, include the client and version, date, installation path, explicit and implicit invocation results when observable, adjacent Skills, model, permission mode, and any unexposed behavior.
Record Skill-level behavior results in that Skill's evaluation assets.
`not exposed` and `not executed` are not passes.

## Plugin runtime requirements

`mtk177a-skills` 0.1.0 packages all 29 public Skills without changing their instructions.\
Packaging makes those instructions and their resources available together; it does not provide the tools or permissions needed to carry them out.\
Use the inventory below to check the requirements for the intended task, and the [verification record](#plugin-evidence-and-remaining-checks) to see what has actually been observed.

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

## Plugin evidence and remaining checks

The formal 29-Skill package is awaiting upload and runtime verification.\
The observations below concern the three-Skill test plugin `mtk177a-skills-probe`, updated from 0.1.0 to 0.1.1 as recorded in [Issue #100](https://github.com/mtk177a/skills/issues/100).\
They establish only the stated observations, not verification of the formal package.

| Target | Evidence from the test plugin | What remains unverified |
| --- | --- | --- |
| ChatGPT personal plugin | The user reported archive installation and update; the UI showed a version change and an increase from two Skills to three | Automatic synchronization and direct downgrade. Uploading the formal package remains a user operation |
| Codex | `explore-decision-space` appeared in the available catalog and its body was read; the seven uploaded source files were previously compared byte for byte | Equality of the complete installed file set. On 2026-10-23 the cache also contained `.codex-plugin/plugin.json`, but the stage at which it was added was not observed |
| Chat | Supplied conversation PDFs contain explicit requests for `define-referents` and `explore-decision-space`, with outputs consistent with those requests | Body loading: no independent tool trace proves that it occurred |
| dots | The user relayed a dot's statement that it read `clarify-request` and `define-referents` | Independent confirmation: the evidence is a self-report, not an observed execution trace |
| Work | No separate runtime test recorded | Runtime behavior; not executed |

Client/model versions and permission modes were not fully recorded for these tests, so the observations cannot be generalized to other environments.\
For Cursor, official documentation describes root `plugin.json` and local plugin loading, but this package has not been tested there.

After the user uploads the formal package, check the following on the affected surfaces:

| Check | Skill to use | What the check covers |
| --- | --- | --- |
| A task without tool dependencies | `explore-decision-space` | Explicit use of a Skill whose core task does not require tools |
| Reading bundled references | `define-referents` | Access to the Skill's accompanying reference |
| Reading a required companion | `cognitive-rhythm-writing` and `japanese-tech-writing` | The required reading relationship between the two mirrors |
| An unavailable execution capability | `revise-docs-fresh-eyes` | Stopping when an independent subagent is unavailable |

Record the version, date, installation route, explicit request, observable loading, output, and missing capabilities.\
Distinguish behavior that was not exposed from checks that were not executed; neither is a passing result.\
Do not change account settings or create subagents without authorization merely to obtain a pass.

See [Plugin distribution](distribution.md) for building, installing, updating, avoiding duplicates, and recovering from a faulty version.

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
