# Localization

This document describes the language policy for Skills and documentation in this repository.

## Canonical source language

`SKILL.md` is the single canonical source for each Skill.\
It is written in English by default.\
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

## Keeping translations in sync

When a maintained English canonical file is added or changed, review its Japanese counterpart in the same change.

Update or create the Japanese reference when the canonical change affects meaning.\
Meaning includes requirements, scope, exceptions, permissions, prohibitions, safety conditions, procedures, validation, links, and other information needed to use the document correctly.

If the canonical change does not affect the Japanese meaning, leave the translation unchanged rather than creating a no-op edit.\
Record the reason in the pull request's `Validation` or `Risks / Follow-up` section so the review decision remains visible.

Use the repository-local `maintain-japanese-references` Skill to make this review and synchronization decision.\
Japanese-canonical Skills remain outside this workflow and do not receive a duplicate `SKILL-ja.md`.

## Language in Skill bodies

- Skill bodies: English by default; Japanese for a documented Japanese writing/editing exception
- Proper nouns, configuration keys, and established technical terms: keep in original form
- Avoid agent-specific jargon unless it is the core of the Skill's value

## Language in commit messages

Commit message summaries are written in English and kept short and specific.

See [Contributing](../CONTRIBUTING.md) for the full commit message and pull request title convention.

## Language in Issues and pull requests

Write Issue and pull request titles and their `Summary` sections in English so the public repository remains discoverable and scannable.

Write the remaining body sections and comments in Japanese by default.\
A full English and Japanese duplication of the body is not required.
