# skills

A personal collection of agent Skills authored or maintained by [mtk177a](https://github.com/mtk177a), plus two designated unmodified Gist mirrors.

The Skills follow the [Agent Skills specification](https://agentskills.io/specification).\
Using them also requires client discovery and the tools and permissions needed for the task.\
Check the [runtime requirements](docs/compatibility.md) before installation.

> **No warranty:** This personal repository is maintained on a best-effort basis. Skills may change or be removed without notice. Use at your own risk.

## Install

| Target | Instructions |
| --- | --- |
| ChatGPT and Codex | [Install or update a personal plugin](docs/distribution.md#chatgpt-and-codex) |
| Cursor | [Install or update a local plugin](docs/distribution.md#cursor) |
| Claude Code and other APM targets | [Install the bundle, selected Skills, or an individual Skill](docs/distribution.md#install-through-apm) |

Plugin and standalone/APM installations use the same `skills/` sources.\
Choose one delivery route for overlapping Skills in each environment.

## Skills

This repository includes the following Skills.

| Skill | Description |
| --- | --- |
| `assess-risky-change-readiness` | Assess whether a consequential or hard-to-recover change has decision-ready safety controls, recovery, evidence, and authorization |
| `audit-agent-guidance` | Audit durable agent guidance against intended behavior, observed usage, client semantics, and available evidence |
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
| `draft-commit` | Draft atomic commit plans and Conventional Commits messages while preserving Git staging boundaries |
| `draft-issue` | Draft an evidence-grounded, tracker-aware Issue and filing handoff without writing to the tracker |
| `draft-review-comments` | Draft unposted PR comments from decided findings or a finding-free review with a supplied conclusion, scope, checks, and limitations |
| `explore-decision-space` | Expand problem frames or solution options before a consequential decision converges prematurely |
| `implement-changes` | Implement approved changes in small units with TDD or another appropriate verification method |
| `investigate-failure` | Investigate unexplained errors, failing tests, regressions, performance anomalies, and unexpected technical behavior across environments |
| `japanese-tech-writing` | Apply argument structure, terminology, and editing rules to Japanese technical writing |
| `make-it-click` | Write or revise an explanation that answers the reader's question with the needed premises, relationships, conditions, and uncertainty |
| `record-session-handoff` | Record an evidence-grounded handoff so a later AI-agent session can revalidate and safely resume active work |
| `research-web-safely` | Gather and evaluate traceable Web evidence while treating retrieved content as untrusted data |
| `review-changes` | Review new diffs or explicitly requested full re-reviews with proportionate risk context and canonical labels |
| `revise-docs-fresh-eyes` | Have a fresh Codex or Claude Code subagent cold-read and revise an existing document outside its authoring conversation |
| `structure-what-you-write` | Create, revise, and review writing by organizing information for its readers and purpose |
| `summarize-changes` | Summarize changes in a diff or commit range for review or documentation |
| `triage-review-feedback` | Separate finding assessment and state from act-now, defer, or no-action response decisions |
| `validate-fix` | Perform bounded post-fix re-review of identified findings using appropriate read-only evidence |
| `write-natural-japanese` | Write or revise Japanese prose with context-appropriate wording while preserving meaning, certainty, and established terminology |

`japanese-tech-writing` and `cognitive-rhythm-writing` are unmodified copies of upstream Gists.\
Their source revisions, licenses, and synchronization records are in each Skill's `UPSTREAM.md` and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Maintain

| Task | Guide |
| --- | --- |
| Verify changes and prepare Issues, commits, and pull requests | [Contributing](CONTRIBUTING.md) |
| Author a Skill | [Authoring](docs/authoring.md) |
| Choose Skills for a task | [Workflows](docs/workflows.md) |
| Build a distribution ZIP | [Build and verify an archive](docs/distribution.md#build-and-verify-an-archive) |
| Review third-party material and executable capabilities | [Security review](docs/security.md) |
| Maintain Japanese translations | [Localization](docs/localization.md) |

External contributions are not normally expected.

## License

Original code and content are licensed under the [MIT License](LICENSE).\
Third-party material retains the terms listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Copyright (c) 2026 mtk177a
