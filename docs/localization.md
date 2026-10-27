# Localization

This document defines source languages, translation pairs, and update rules.

| Content | Language |
| --- | --- |
| Skill bodies | English by default; Japanese writing/editing exceptions follow the rules below |
| Commit summaries, Issue/PR titles, and `Summary` sections | English for discovery and scanning |
| Other Issue/PR sections and comments | Japanese by default; full bilingual duplication is not required |

Keep commit summaries short and specific.\
Follow [Contributing](../CONTRIBUTING.md) for their format.

## Canonical source language

`SKILL.md` is the single canonical source for each Skill.\
It is written in English by default.\
Preserve proper nouns, configuration keys, and established technical terms; use agent-specific jargon only when it is core to the Skill’s value.\
A Skill whose core purpose is Japanese writing or editing may use a Japanese `SKILL.md` as its canonical source.\
In that case, document the exception and provenance and do not add a duplicate `SKILL-ja.md`.

## Japanese reference translations

Japanese translations help the maintainer understand and review the repository without translating the same material repeatedly.\
The English file defines requirements; translations must preserve its meaning without adding requirements.

Use this notice at the start of every Japanese reference (after frontmatter, if present), with the source filename and relative link adjusted for that file:

```markdown
> この文書は [英語版 SKILL.md](SKILL.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。
```

The following table defines the maintained canonical-to-reference file pairs.\
Use it to identify the Japanese reference for a changed English file; add a new pair here when no listed path or pattern covers it.

| File | Canonical | Translation |
|------|-----------|-------------|
| `skills/<skill-name>/SKILL.md` | English by default; Japanese for a documented Japanese writing/editing exception | `skills/<skill-name>/SKILL-ja.md` when English is canonical |
| `README.md` | English | `README.ja.md` |
| `CONTRIBUTING.md` | English | `CONTRIBUTING-ja.md` |
| `AGENTS.md` | English | `AGENTS-ja.md` |
| `CLAUDE.md` | English | `CLAUDE-ja.md` |
| `docs/*.md` | English | `docs/ja/*.md` |
| `.agents/skills/<tracked-skill>/SKILL.md` | English by default; Japanese for a documented Japanese writing/editing exception | `.agents/skills/<tracked-skill>/SKILL-ja.md` when English is canonical |

If the table does not identify a unique counterpart, do not infer a filename or create a translation.\
Report the unresolved pair so the mapping can be decided and recorded here.

## Update translations with source changes

When a maintained English canonical file is added or changed, review its Japanese counterpart in the same change.

| Canonical change | Translation action |
| --- | --- |
| Affects meaning or correct use | Update or create the reference in the same change |
| Does not affect the Japanese meaning | Leave it unchanged; record the reason in the PR’s validation or follow-up section |

Meaning includes requirements, scope, exceptions, permissions, prohibitions, safety conditions, procedures, validation, links, and other information needed for correct use.

Use the repository-local `maintain-japanese-references` Skill to make this review and synchronization decision.\
Japanese-canonical Skills remain outside this workflow and do not receive a duplicate `SKILL-ja.md`.
