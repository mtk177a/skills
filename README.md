# skills

A personal repository of agent Skills — authored and maintained by [mtk177a](https://github.com/mtk177a).

These Skills follow the [Agent Skills specification](https://agentskills.io/specification). Format compatibility does not establish client discovery or runtime behavior: this repository records targeted behavior evidence for Codex, while Claude Code, GitHub Copilot, Gemini CLI, and other clients remain unverified. See [docs/compatibility.md](docs/compatibility.md) for the evidence states and verification scope.

> **No warranty.** This is a personal repository, maintained by one person on a best-effort basis. Skills may change or be removed without notice. Use at your own risk.

## Skills

26 Skills covering common development workflows:

| Skill | Description |
| --- | --- |
| `audit-agent-guidance` | Audit durable agent guidance against intended behavior, observed usage, client semantics, and evaluation evidence |
| `break-failure-loop` | Pause equivalent same-hypothesis attempts without new evidence and select a diagnostic, blocker, or diversification handoff |
| `calibrate-learning-support` | Adjust AI learning support so task-specific understanding, decision ownership, and verification are preserved while work continues |
| `choose-ai-execution-setup` | Advise which available AI execution setup should handle a concrete task across access, model, reasoning, context, permission, verification, and topology dimensions |
| `clarify-request` | Iteratively clarify or structure an ambiguous request until the next workflow can start, proceed under low-impact assumptions, or report a blocker |
| `cognitive-rhythm-writing` | Design pacing in explanatory Japanese writing by managing cognitive rhythm and unresolved tension |
| `curate-repo-docs` | Keep repository-managed documentation minimal, evidence-backed, correctly placed, and validated |
| `define-referents` | Ground ambiguous terms in concrete referents and return naming constraints to the originating workflow |
| `design-agent-instructions` | Design AGENTS.md / CLAUDE.md / copilot-instructions.md / GEMINI.md instruction sets |
| `design-changes` | Design change scope, impact, risk, and verification approach before implementing |
| `design-skill` | Decide whether and how to create, merge, split, or substantially rescope a Skill before implementation |
| `explore-decision-space` | Expand problem frames or solution options before a consequential decision converges prematurely |
| `draft-commit` | Draft atomic commit plans and Conventional Commits messages while preserving Git staging boundaries |
| `draft-issue` | Draft an evidence-grounded, tracker-aware Issue and filing handoff without writing to the tracker |
| `draft-review-comments` | Draft unposted PR comments from organized findings and decisions without changing their meaning |
| `revise-docs-fresh-eyes` | Have a fresh Codex or Claude Code subagent cold-read and revise an existing document outside its authoring conversation |
| `implement-changes` | Implement approved changes in small units with TDD or another appropriate verification method |
| `investigate-failure` | Investigate unexplained errors, failing tests, regressions, performance anomalies, and unexpected technical behavior across environments |
| `japanese-tech-writing` | Apply formatting, argument structure, terminology, and editing rules to Japanese technical writing |
| `assess-risky-change-readiness` | Assess whether a consequential or hard-to-recover change has decision-ready safety controls, recovery, evidence, and authorization |
| `record-session-handoff` | Record an evidence-grounded handoff so a later AI-agent session can revalidate and safely resume active work |
| `research-web-safely` | Gather and evaluate traceable Web evidence while treating retrieved content as untrusted data |
| `review-changes` | Review code, documentation, or configuration diffs with evidence, impact, confidence, and canonical labels |
| `summarize-changes` | Summarize changes in a diff or commit range for review or documentation |
| `triage-review-feedback` | Evaluate existing review findings and decide accept, defer, or reject while preserving their provenance, evidence, and uncertainty |
| `validate-fix` | Verify whether a specific completed fix resolved its original finding or expected behavior using appropriate read-only evidence |

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

`cognitive-rhythm-writing` requires `japanese-tech-writing`; install the pair from the bundle:

```bash
apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing
```

### Other clients

Clients that discover standard `skills/<name>/SKILL.md` packages may be format-compatible, but this repository does not claim runtime support without recorded client evidence. See [docs/compatibility.md](docs/compatibility.md) for documented behavior, local verification, and installation paths.

## Repository structure

```text
.
├── README.md
├── README.ja.md
├── LICENSE
├── AGENTS.md
├── AGENTS-ja.md
├── CLAUDE.md
├── CLAUDE-ja.md
├── .github/
│   └── copilot-instructions.md
├── apm.yml
├── docs/
│   ├── authoring.md
│   ├── compatibility.md
│   ├── evaluation.md
│   ├── localization.md
│   ├── security.md
│   └── workflows.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── SKILL-ja.md  # optional Japanese reference translation
│       ├── evals/
│       ├── references/
│       ├── scripts/
│       └── assets/
```

`evals/`, `references/`, `scripts/`, and `assets/` are optional — only Skills that need them include them.

## Authoring and contribution

This is a personal repository. External contributions are not expected.

Original code and content authored for this repository may be used and adapted under the MIT License. Third-party-derived files retain their individual licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). See [docs/authoring.md](docs/authoring.md) for how Skills are structured and [docs/security.md](docs/security.md) for third-party and executable Skill review.

## License

Original code and content in this repository are licensed under the [MIT License](LICENSE). Third-party-derived material remains subject to the terms listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Copyright (c) 2026 mtk177a
