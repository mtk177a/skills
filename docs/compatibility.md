# Compatibility

This document describes how Skills in this repository have been verified across agent clients, and what the expected compatibility posture is.

## Verification scope

Skills follow the [Agent Skills specification](https://agentskills.io/specification), which is a lightweight format adopted by Codex, Claude Code, GitHub Copilot, and Gemini CLI. Any client that discovers and loads `skills/<name>/SKILL.md` files should work with this repository.

Claude Code is the primary development and testing target. Other clients are expected to work if they support the standard `skills/<name>/SKILL.md` discovery format, but have not been formally verified.

The table below lists clients that have been explicitly tested. Clients not listed may work if they support the standard format, but are not claimed as supported.

| Client | Verified | Verified date | Scope |
|--------|----------|---------------|-------|
| Claude Code | — | — | install, list, invoke |
| Codex | — | — | install, list, invoke |
| GitHub Copilot / `gh skill` | — | — | install, list, invoke |
| Gemini CLI | — | — | install, list, invoke |
| APM (`apm install`) | ✓ | 2026-07-21 | install (apm 0.26.0), frozen dry-run, offline pack dry-run, audit |
| `npx skills add` | — | — | install |

Entries marked with `—` are pending verification.

## Installation paths

### Claude Code

```bash
apm install mtk177a/skills
```

Or add to your `apm.yml` dependencies:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### Individual Skill

```bash
apm install mtk177a/skills/skills/review-changes
```

## Validation

To check that Skills conform to the Agent Skills specification:

```bash
skills-ref validate
```

## Notes on untested clients

For clients not listed in the table: the Skills follow the standard `skills/<name>/SKILL.md` format. If the client discovers Skills via that path, they are likely to work. No compatibility is guaranteed or implied.
