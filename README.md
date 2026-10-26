# skills

A personal collection of agent Skills authored or maintained by [mtk177a](https://github.com/mtk177a), plus two designated unmodified Gist mirrors.

The Skills follow the [Agent Skills specification](https://agentskills.io/specification).\
Whether a Skill works also depends on the client, and on what the agent can access and do.\
Check the [runtime requirements](docs/users/compatibility.md) before installation.

> **No warranty:** The owner maintains this personal repository on a best-effort basis.\
> The owner can change or remove Skills without notice.\
> Use at your own risk.

## Install

There are two installation methods, and both install the same Skills from `skills/`:

- **Plugin ZIP**: the only method for ChatGPT.\
  A plugin uploaded to ChatGPT is also available in Codex.
- **APM**: for Claude Code, Codex, Cursor, and the other clients that APM supports.

To choose a method and install, see [Install and update the Skills](docs/users/installation.md#choose-an-installation-method).

## Skills

Choose a Skill by task.\
Then read the linked Skill to see when to use it and what it produces.\
To use several Skills on one piece of work, see [Choose the next Skill](docs/users/workflows.md).

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
| Review a new diff, or re-review the whole diff when explicitly requested | [`review-changes`](skills/review-changes/SKILL.md) |
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
| Author a Skill | [Skill authoring guide](docs/maintainers/authoring.md) |
| Build the plugin ZIP | [Build the plugin ZIP](docs/maintainers/packaging.md) |
| Review third-party material and executable capabilities | [Skill security review](docs/maintainers/security.md) |
| Choose the language and maintain Japanese reference translations | [Languages and Japanese reference translations](docs/maintainers/localization.md) |
| Check the terms used for repository concepts | [Glossary](docs/maintainers/glossary.md) |

External contributions are not normally expected.

## License

Original code and content are licensed under the [MIT License](LICENSE).\
Third-party material retains the terms listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Copyright (c) 2026 mtk177a
