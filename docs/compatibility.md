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
| APM | APM distributes this repository as an `agent-skills` package; it is not an execution client. Target selection and installation layout do not establish downstream invocation or behavior. | The package checks listed below have been executed. | Distribution verified for the recorded scope only |

Do not add client-specific metadata to every Skill merely because a client supports it. Add it only when the Skill needs that client's invocation control, UI presentation, tool dependency declaration, or permission behavior. Keep portable `name`, `description`, instructions, and resources as the common layer.

## Representative verification snapshot

The table preserves representative observations from recorded repository checks, not support claims inferred from documentation.
It is not a current or exhaustive inventory of later Skill-level evaluations.
Later client versions, dates, and scenario scopes remain recorded in each Skill's `evals/README.md` and optional `results.json`; see [evaluation.md](evaluation.md) for those evidence responsibilities.

| Target | Version | Verified date | Observed scope |
| --- | --- | --- | --- |
| Claude Code | — | — | Not executed; installation, discovery, explicit and implicit invocation, permissions, and behavior are unverified |
| Codex | 0.145.0 | 2026-07-24 | Repository-local discovery, observable target Skill open in 16 baseline/candidate selection runs, and 29 candidate/baseline behavior runs including five affected reruns; explicit `/skills` and `$` invocation, UI, and live permission behavior not executed |
| GitHub Copilot / `gh skill` | — | — | Not executed; installation, discovery, invocation, permissions, and behavior are unverified |
| Gemini CLI | — | — | Not executed; installation, discovery, invocation, permissions, and behavior are unverified |
| APM | 0.26.0 | 2026-07-21 | install resolution, frozen dry-run, offline pack dry-run, audit |
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

Also run the repository's frozen non-deploying APM check:

```bash
apm install --frozen --dry-run --no-policy
```

Neither command proves triggering, instruction following, permission behavior, or output quality. Use the targeted evaluation procedure in [evaluation.md](evaluation.md) for those claims and [security.md](security.md) for third-party and executable capability review.

## Current sources

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)

Client extensions and runtime behavior change more frequently than the core package format. Recheck the current official source when one of those details affects a design or audit.
