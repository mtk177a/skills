# Compatibility

This document separates portable Agent Skills format compatibility from client-specific discovery, invocation, permissions, and execution behavior. A Skill can be structurally valid and still fail to load, trigger, or execute as intended in a particular client.

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

Format compatibility is not evidence of behavioral compatibility. Record official documentation and local execution evidence separately.

## Client matrix

| Client or layer | Format and discovery posture | Invocation and client extensions | Enforcement and runtime posture | Local verification |
| --- | --- | --- | --- | --- |
| Codex | Supports Agent Skills and repository or user Skill discovery as documented by Codex | Implicit selection and explicit `$skill` / picker invocation; optional `agents/openai.yaml` supplies Codex UI metadata and dependencies | Sandbox, approval, rules, and available tools are separate from Skill prose; runtime access depends on the active Codex environment | Targeted repository-local selection and behavior only |
| Claude Code | Supports Skills in Claude Code discovery and plugin surfaces | Implicit selection and `/skill-name`; frontmatter such as `disable-model-invocation` and `user-invocable` changes invocation; `context: fork` changes execution context | `allowed-tools` preapproves listed tools but does not prohibit others; permission deny rules enforce denials in settings, while CLI `--disallowedTools` and SDK `disallowed_tools` are surface-specific controls; hooks and settings remain separate control surfaces | Pending |
| GitHub Copilot / `gh skill` | Expected to work when the client discovers the standard Skill package | Client-specific invocation and metadata behavior must be checked against the target version | Permission, tool, and runtime behavior is unverified | Pending |
| Gemini CLI | Expected to work when the client discovers the standard Skill package | Client-specific invocation and metadata behavior must be checked against the target version | Permission, tool, and runtime behavior is unverified | Pending |
| APM | Distributes this repository as an `agent-skills` package; it is not an execution client | Target selection and installation layout are APM concerns, not Skill invocation semantics | Installation and audit policy do not prove downstream client behavior | Verified as listed below |
| Claude API Skills | Uses the API Skill execution environment rather than Claude Code's local runtime | Do not project Claude Code frontmatter or local plugin behavior onto the API surface | Network and package availability are constrained by the API execution environment and must be checked in current API documentation | Not tested |

Do not add client-specific metadata to every Skill merely because a client supports it. Add it only when the Skill needs that client's invocation control, UI presentation, tool dependency declaration, or permission behavior. Keep portable `name`, `description`, instructions, and resources as the common layer.

## Verification record

The table records observed repository checks, not support claims inferred from documentation.

| Target | Version | Verified date | Observed scope |
| --- | --- | --- | --- |
| Claude Code | — | — | Not executed |
| Codex | 0.145.0 | 2026-07-24 | repository-local discovery, observable target Skill open in 16 baseline/candidate selection runs, and 29 candidate/baseline behavior runs including five affected reruns; explicit `$skill`, UI, and live permission behavior not tested |
| GitHub Copilot / `gh skill` | — | — | Not executed |
| Gemini CLI | — | — | Not executed |
| APM | 0.26.0 | 2026-07-21 | install resolution, frozen dry-run, offline pack dry-run, audit |
| `npx skills add` | — | — | Not executed |

When recording a new result, include the client and version, date, installation path, explicit and implicit invocation results when observable, adjacent Skills, model, permission mode, and any unexposed behavior. `not exposed` and `not executed` are not passes.

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
