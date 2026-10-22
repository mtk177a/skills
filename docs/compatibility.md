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

## Plugin runtime requirements

The `mtk177a-skills` 0.1.0 package includes all 29 public Skills without changing their bodies.
The following inventory describes required evidence and capabilities, not unconditional client support.
All included references must be readable by the executing agent; none of the current Skills bundles an executable script or requires installing a Python dependency.
Tool-dependent tasks still need the target environment's tools and authorization.

| Skills | Required inputs or execution conditions |
| --- | --- |
| `clarify-request`, `define-referents`, `explore-decision-space`, `calibrate-learning-support` | Conversation/task evidence; `define-referents` must also read its packaged reference. External facts require access when material. |
| `make-it-click`, `structure-what-you-write`, `write-natural-japanese` | Supplied text and context, plus the packaged references selected or required by the Skill; persistence requires authorized write access. |
| `japanese-tech-writing`, `cognitive-rhythm-writing` | Text to write/revise; `cognitive-rhythm-writing` must read the adjacent `japanese-tech-writing/SKILL.md`. Both unmodified mirrors and provenance files are included. |
| `choose-ai-execution-setup`, `assess-risky-change-readiness` | Evidence of available environments, capabilities, controls and authority; advice does not provision them or authorize execution. |
| `design-changes`, `design-agent-instructions`, `design-skill` | Access to the relevant existing implementation or instructions and constraints; `design-skill` includes its authoring reference. Design does not execute changes. |
| `audit-agent-guidance`, `investigate-failure`, `break-failure-loop` | In-scope guidance, failure/attempt evidence and relevant read-only inspection tools; missing behavioral evidence must remain unverified. |
| `curate-repo-docs`, `implement-changes` | Target files, applicable repository rules, authorized write access and the required validation tools; packaged references support document decisions or TDD. Missing execution capability is not successful implementation. |
| `review-changes`, `validate-fix`, `triage-review-feedback` | Actual diff/fix/findings and relevant source/specification evidence; commands or live checks require available tools. Untested claims remain unverified. |
| `draft-commit`, `draft-issue`, `draft-review-comments`, `summarize-changes` | A scoped change set, grounded request, or supplied findings as required by each Skill; repository/tracker access is conditional on the evidence needed. Drafting does not publish. |
| `record-session-handoff` | Current task evidence; authorized persistence if available, otherwise the Skill's explicit draft/not-written result. |
| `research-web-safely` | Live search/retrieval and observable citations for web verification; unavailable sources or tools cannot be reported as verified. |
| `revise-docs-fresh-eyes` | Codex or Claude Code with an authorized independent fresh subagent and access to the artifact; unavailable or prohibited subexecution must stop the workflow. Same-context rewriting is not a substitute. |

Repository-only `maintain-japanese-references` is excluded; its dependency on `write-natural-japanese` does not make it a public Skill.
References to other workflows do not automatically make those Skills mandatory companions.
When resources or instructions change, recheck the affected row and package references together.

## Plugin evidence and remaining checks

[Issue #100](https://github.com/mtk177a/skills/issues/100) records the personal probe `mtk177a-skills-probe` update from 0.1.0 to 0.1.1.
This evidence concerns three Skills and must not be treated as verification of the formal 29-Skill package.

| Surface | Evidence | Limits |
| --- | --- | --- |
| ChatGPT personal plugin | User-reported archive installation/update, with UI version and Skill count changing from two to three | Formal package upload remains user-operated; no auto-sync or downgrade evidence |
| Codex | Probe `explore-decision-space` appeared in the available catalog and its body was read; the seven uploaded source files were previously compared byte for byte | On 2026-10-23 the installed cache also contained `.codex-plugin/plugin.json`; installed file-set equality is not established, and the stage that added the compatibility file was not observed |
| Chat | Provided conversation PDFs show explicit requests for `define-referents` and `explore-decision-space` and outputs consistent with them | No independent tool trace proves body loading |
| dots | User relayed a dot's report that it read `clarify-request` and `define-referents` | Self-report, not an independently observed execution trace |
| Work | No separate runtime test recorded | Not executed |
| Cursor | Official documentation supports root `plugin.json` and local plugin loading | Not executed for this package |

Probe client/model versions and permission modes were not fully recorded; do not generalize these observations to other environments.
Formal-package verification remains pending upload and should cover a tool-independent Skill (`explore-decision-space`), references (`define-referents`), the mirror pair, and the unavailable-subagent boundary of `revise-docs-fresh-eyes` on affected surfaces.
Record version, date, installation route, explicit request, observable loading, output, missing capabilities, and `not exposed`/`not executed` separately.
Do not change account settings or create subagents just to manufacture a pass without authorization.
See [distribution](distribution.md) for build, installation, update, duplicate avoidance, and recovery.
