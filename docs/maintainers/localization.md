# Languages and Japanese reference translations

This guide is for maintainers and the agents working for them.\
It defines which language each kind of content uses, which files have Japanese reference translations, and when to update those translations.

## Choose the language

- **Skill bodies**: English by default.\
  See [Skill files](#skill-files) for the Japanese exception.
- **Commit summaries, Issue and PR titles, and `Summary` sections**: English, so that they are easy to search and scan.\
  Keep commit summaries short and specific, and follow the format in [Contributing](../../CONTRIBUTING.md).
- **Other Issue and PR sections, and comments**: Japanese by default.\
  They do not need to repeat everything in both languages.

## Skill files

Each Skill has one source file, `SKILL.md`, written in English by default.\
Keep proper nouns, configuration keys, and established technical terms in their original form.\
Use terms specific to one client only when they are essential to the Skill.

A Skill whose main purpose is writing or editing Japanese may use a Japanese `SKILL.md` as its source.\
Such a Skill has no `SKILL-ja.md`.\
Record the exception and where it was introduced in the list below.

| Skill | Introduced in |
| --- | --- |
| `skills/write-natural-japanese/` | [#43](https://github.com/mtk177a/skills/pull/43) |
| `.agents/skills/maintain-japanese-references/` | [#42](https://github.com/mtk177a/skills/pull/42); the exception is recorded in [#77](https://github.com/mtk177a/skills/issues/77) |

The two upstream Gist mirrors are also in Japanese.\
They follow the copying rules in [Upstream Gist mirrors](authoring.md#upstream-gist-mirrors), not this exception.

## Japanese reference translations

Japanese reference translations let the maintainer understand and review the repository without translating the same material repeatedly.\
The English source defines the requirements.\
A translation keeps its meaning and adds no requirements.

### Find the translation of a file

The following table lists each source file and its Japanese reference translation.\
When a source file changes, use the table to find its translation.

| Source file | Source language | Japanese reference translation |
| --- | --- | --- |
| `skills/<skill-name>/SKILL.md` | English, or Japanese for a recorded exception | `skills/<skill-name>/SKILL-ja.md`, only when the source is English |
| `README.md` | English | `README.ja.md` |
| `CONTRIBUTING.md` | English | `CONTRIBUTING-ja.md` |
| `AGENTS.md` | English | `AGENTS-ja.md` |
| `CLAUDE.md` | English | `CLAUDE-ja.md` |
| `docs/<audience>/*.md` | English | `docs/ja/<audience>/*.md` |
| `.agents/skills/<tracked-skill>/SKILL.md` | English, or Japanese for a recorded exception | `.agents/skills/<tracked-skill>/SKILL-ja.md`, only when the source is English |

`<audience>` is `users` or `maintainers`.

These files have no Japanese reference translation:

- the bundled resources of each Skill, such as `references/*.md`
- `THIRD_PARTY_NOTICES.md` and each `UPSTREAM.md`
- the files under `.github/`

If a new source file matches no row and is not in the list above, add a row for it.\
If the table does not identify exactly one translation for a file, do not guess a filename or create a translation.\
Report the undecided pair instead, so that it can be decided and recorded here.

### Add the notice

Start every Japanese reference translation with this notice, placed after the frontmatter if there is any.\
Adjust the filename and relative link to match the English source.

```markdown
> この文書は [英語版 SKILL.md](SKILL.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。
```

## Update translations when the source changes

When you add or change an English source, review its Japanese reference translation in the same change:

| Change to the English source | What to do with the translation |
| --- | --- |
| It affects the meaning or correct use. | Update or create the translation in the same change. |
| It does not affect what the Japanese conveys. | Leave the translation unchanged, and record why in the PR's verification or follow-up section. |

Meaning includes requirements, scope, exceptions, permissions, prohibitions, safety conditions, procedures, verification, links, and anything else needed for correct use.

Use the repository-local `maintain-japanese-references` Skill for this review and update.\
When a translation refers to a concept specific to this repository, or to a word that can point to different things, check the [glossary](glossary.md).
