# Localization

This document describes the language policy for Skills and documentation in this repository.

## Canonical source language

`SKILL.md` is the single canonical source for each Skill. It is written in English by default.
A Skill whose core purpose is Japanese writing or editing may use a Japanese `SKILL.md` as its canonical source. In that case, document the exception and provenance and do not add a duplicate `SKILL-ja.md`.

Required frontmatter:

```yaml
---
name: skill-name
description: What the Skill does and when it should be used.
license: MIT
---
```

## Japanese reference translations

Japanese reference translations are maintained as a reusable comprehension and review cache for the primary maintainer.\
They reduce the need to translate the same technical material again whenever it is read or edited.

English remains the public and normative canonical source.\
A Japanese translation does not define requirements and must not introduce meaning that is absent from its canonical file.

When `SKILL.md` is canonical English, `SKILL-ja.md` is a non-canonical Japanese translation placed alongside it:

```
skills/<skill-name>/
├── SKILL.md       # English canonical
└── SKILL-ja.md   # Japanese reference translation
```

`SKILL-ja.md` must begin with a notice stating that the English version is the canonical source:

```markdown
> **Note:** The English version (`SKILL.md`) is the canonical source.
> This Japanese translation is provided as a reference only.
```

The same policy applies to other translated files:

| File | Canonical | Translation |
|------|-----------|-------------|
| `SKILL.md` | English by default; Japanese for a documented Japanese writing/editing exception | `SKILL-ja.md` when English is canonical |
| `README.md` | English | `README.ja.md` |
| `AGENTS.md` | English | `AGENTS-ja.md` |
| `CLAUDE.md` | English | `CLAUDE-ja.md` |
| `docs/*.md` | English | `docs/ja/*.md` |

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

See `AGENTS.md` for the full commit message convention.

## Language in Issues and pull requests

Write Issue and pull request titles and their `Summary` sections in English so the public repository remains discoverable and scannable.

Write the remaining body sections and comments in Japanese by default. A full English and Japanese duplication of the body is not required.
