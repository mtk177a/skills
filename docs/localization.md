# Localization

This document describes the language policy for Skills and documentation in this repository.

## English as the canonical source

`SKILL.md` is the single canonical source for each Skill. It is written in English.

Required frontmatter:

```yaml
---
name: skill-name
description: What the Skill does and when it should be used.
license: Apache-2.0
---
```

## Japanese translations

`SKILL-ja.md` is a non-canonical Japanese translation of `SKILL.md`, placed alongside it:

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
| `SKILL.md` | English | `SKILL-ja.md` |
| `README.md` | English | `README.ja.md` |
| `AGENTS.md` | English | `AGENTS-ja.md` |
| `docs/*.md` | English | `docs/ja/*.md` |

## Keeping translations in sync

When a commit changes an English file, the corresponding Japanese translation must be updated in the same commit.

If a quick update is made and the Japanese translation is not ready, note the gap in the commit message and open a follow-up.

## Language in Skill bodies

- Skill bodies: English
- Proper nouns, configuration keys, and established technical terms: keep in original form
- Avoid agent-specific jargon unless it is the core of the Skill's value

## Language in commit messages

Commit message summaries are written in Japanese (this repository's working language for the author).
Technical terms and proper nouns remain in English within the summary.

See `AGENTS.md` for the full commit message convention.
