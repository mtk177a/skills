# skills

A personal collection of agent Skills authored or maintained by [mtk177a](https://github.com/mtk177a), plus two designated unmodified Gist mirrors.

The Skills follow the [Agent Skills specification](https://agentskills.io/specification).\
Using them also requires client discovery and the tools and permissions needed for the task.\
Check the [runtime requirements](docs/users/compatibility.md) before installation.

> **No warranty:** This personal repository is maintained on a best-effort basis. Skills may change or be removed without notice. Use at your own risk.

## Install

| Target | Instructions |
| --- | --- |
| ChatGPT and Codex | [Install or update a personal plugin](docs/users/installation.md#upload-the-plugin-zip-to-chatgpt) |
| Cursor | [Install or update a local plugin](docs/users/installation.md#extract-the-plugin-zip-for-cursor) |
| Claude Code and other APM targets | [Install the bundle, selected Skills, or an individual Skill](docs/users/installation.md#install-with-apm) |

Plugin and standalone/APM installations use the same `skills/` sources.\
Choose one delivery route for overlapping Skills in each environment.

## Skills

Choose by task, then follow the linked Skill for its conditions and boundaries.\
See [workflows](docs/users/workflows.md) for sequencing and handoffs.

### Clarify and choose an approach

| Task | Skill |
| --- | --- |
| Clarify an ambiguous request | [`clarify-request`](skills/clarify-request/SKILL.md) |
| Define what ambiguous terms refer to | [`define-referents`](skills/define-referents/SKILL.md) |
| Compare different problem frames and solutions | [`explore-decision-space`](skills/explore-decision-space/SKILL.md) |
| Choose an AI execution environment for the task | [`choose-ai-execution-setup`](skills/choose-ai-execution-setup/SKILL.md) |
| Preserve understanding and decision ownership while using AI | [`calibrate-learning-support`](skills/calibrate-learning-support/SKILL.md) |

### Design, implement, and investigate

| Task | Skill |
| --- | --- |
| Plan scope, risks, and verification before implementation | [`design-changes`](skills/design-changes/SKILL.md) |
| Implement an authorized change and verify it | [`implement-changes`](skills/implement-changes/SKILL.md) |
| Investigate unexpected behavior and failures | [`investigate-failure`](skills/investigate-failure/SKILL.md) |
| Assess safety, recovery, and authorization before a consequential action | [`assess-risky-change-readiness`](skills/assess-risky-change-readiness/SKILL.md) |
| Stop repeated failed attempts and choose the next diagnostic step | [`break-failure-loop`](skills/break-failure-loop/SKILL.md) |

### Review and communicate changes

| Task | Skill |
| --- | --- |
| Review a new diff or explicitly requested full re-review | [`review-changes`](skills/review-changes/SKILL.md) |
| Assess findings and decide how to respond | [`triage-review-feedback`](skills/triage-review-feedback/SKILL.md) |
| Recheck identified fixes against their original findings | [`validate-fix`](skills/validate-fix/SKILL.md) |
| Draft PR comments from supplied review decisions | [`draft-review-comments`](skills/draft-review-comments/SKILL.md) |
| Draft an Issue without posting it | [`draft-issue`](skills/draft-issue/SKILL.md) |
| Plan commit units and draft their messages | [`draft-commit`](skills/draft-commit/SKILL.md) |
| Summarize a diff or commit range for its readers | [`summarize-changes`](skills/summarize-changes/SKILL.md) |
| Record evidence for resuming work in another session | [`record-session-handoff`](skills/record-session-handoff/SKILL.md) |

### Research and write

| Task | Skill |
| --- | --- |
| Research the Web with traceable evidence | [`research-web-safely`](skills/research-web-safely/SKILL.md) |
| Select and organize information for the reader | [`structure-what-you-write`](skills/structure-what-you-write/SKILL.md) |
| Explain an answer and the reasoning needed to understand it | [`make-it-click`](skills/make-it-click/SKILL.md) |
| Write and revise natural Japanese without changing meaning | [`write-natural-japanese`](skills/write-natural-japanese/SKILL.md) |
| Apply Japanese technical-writing rules | [`japanese-tech-writing`](skills/japanese-tech-writing/SKILL.md) |
| Design pacing in explanatory Japanese prose | [`cognitive-rhythm-writing`](skills/cognitive-rhythm-writing/SKILL.md) |
| Have an authorized independent subagent revise a document | [`revise-docs-fresh-eyes`](skills/revise-docs-fresh-eyes/SKILL.md) |

### Maintain Skills and agent instructions

| Task | Skill |
| --- | --- |
| Diagnose gaps between agent guidance and behavior | [`audit-agent-guidance`](skills/audit-agent-guidance/SKILL.md) |
| Design a Skill’s responsibility and boundaries | [`design-skill`](skills/design-skill/SKILL.md) |
| Design instruction files and client loading relationships | [`design-agent-instructions`](skills/design-agent-instructions/SKILL.md) |

`japanese-tech-writing` and `cognitive-rhythm-writing` are unmodified copies of upstream Gists.\
Their source revisions, licenses, and synchronization records are in each Skill's `UPSTREAM.md` and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Maintain

| Task | Guide |
| --- | --- |
| Verify changes and prepare Issues, commits, and pull requests | [Contributing](CONTRIBUTING.md) |
| Author a Skill | [Authoring](docs/maintainers/authoring.md) |
| Build the plugin ZIP | [Build a plugin archive](docs/maintainers/packaging.md) |
| Review third-party material and executable capabilities | [Security review](docs/maintainers/security.md) |
| Maintain Japanese translations | [Localization](docs/maintainers/localization.md) |

External contributions are not normally expected.

## License

Original code and content are licensed under the [MIT License](LICENSE).\
Third-party material retains the terms listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Copyright (c) 2026 mtk177a
