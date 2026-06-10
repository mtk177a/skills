# skills

A personal repository of agent Skills — authored and maintained by [mtk177a](https://github.com/mtk177a).

These Skills follow the [Agent Skills specification](https://agentskills.io/specification) and are designed for Codex, Claude Code, GitHub Copilot, Gemini CLI, and other compatible clients. See [docs/compatibility.md](docs/compatibility.md) for verification status.

> **No warranty.** This is a personal repository, maintained by one person on a best-effort basis. Skills may change or be removed without notice. Use at your own risk.

## Skills

23 Skills covering common development workflows:

| Skill | Description |
|-------|-------------|
| `audit-agent-rules` | Audit AGENTS.md / Skills / docs for naming, boundaries, approval rules, and heavy defaults |
| `break-failure-loop` | Stop and reframe when an agent has failed twice with the same error or approach |
| `calibrate-ai-learning` | Use when delegation is getting too deep or you want to maintain understanding while working |
| `clarify-request` | Use when a request is ambiguous — ask 1–4 clarifying questions or state assumptions |
| `design-agent-instructions` | Design AGENTS.md / CLAUDE.md / copilot-instructions.md / GEMINI.md instruction sets |
| `design-changes` | Design change scope, impact, risk, and verification approach before implementing |
| `design-skill` | Design a new Skill or significantly revise an existing Skill's responsibilities |
| `draft-commit` | Generate commit message drafts or commit split proposals from a diff |
| `draft-issue` | Turn a clarified request into an issue draft and filing steps |
| `draft-review-comments` | Turn organized findings into inline PR comments and a review summary |
| `format-markdown` | Format Markdown according to CommonMark conventions |
| `implement-changes` | Implement changes incrementally in a test-driven, safe manner |
| `investigate-incident` | Investigate an incident: gather facts, form hypotheses, isolate the cause |
| `plan-risky-change` | Plan a risky or irreversible change with explicit safety checks |
| `record-session-handoff` | Record a session handoff so the next session can resume without losing context |
| `research-web-safely` | Research a topic on the web while treating external content as untrusted input |
| `review-changes` | Review a diff for correctness bugs and categorize findings |
| `scope-implementation` | Narrow the scope of an implementation task before starting |
| `scope-request` | Clarify purpose, completion criteria, constraints, and open questions for a request |
| `summarize-changes` | Summarize changes in a diff or commit range for review or documentation |
| `triage-agent-usage` | Assess whether agent usage is appropriate and calibrate delegation level |
| `triage-review-feedback` | Sort review comments into accepted, deferred, and rejected; decide on approach |
| `validate-fix` | Verify a fix: summarize what was checked, what was not, and what risks remain |

## Installation

### Claude Code (APM)

```bash
apm install mtk177a/skills
```

Or declare as a dependency in your `apm.yml`:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### Individual Skill

```bash
apm install mtk177a/skills/skills/review-changes
```

### Other clients

Any client that discovers `skills/<name>/SKILL.md` files should work. See [docs/compatibility.md](docs/compatibility.md) for verified clients and installation paths.

## Repository structure

```text
.
├── README.md
├── README.ja.md
├── LICENSE
├── AGENTS.md
├── AGENTS-ja.md
├── CLAUDE.md
├── .github/
│   └── copilot-instructions.md
├── apm.yml
├── docs/
│   ├── authoring.md
│   ├── compatibility.md
│   ├── evaluation.md
│   ├── localization.md
│   └── workflows.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── SKILL-ja.md
│       ├── evals/
│       ├── references/
│       ├── scripts/
│       └── assets/
└── tasks/
```

`evals/`, `references/`, `scripts/`, and `assets/` are optional — only Skills that need them include them.

## Authoring and contribution

This is a personal repository. External contributions are not expected.

If you find a Skill useful and want to adapt it, the Apache-2.0 license allows that. See [docs/authoring.md](docs/authoring.md) for how Skills are structured.

## License

[Apache License 2.0](LICENSE)

Copyright 2026 mtk177a
