# Languages and Japanese reference translations

This guide is for maintainers and the agents working for them.\
It defines which language each kind of content uses, which English files have Japanese reference translations, and when to update those translations.

## Choose the language

| Content | Language |
| --- | --- |
| Skill bodies | English by default. See [Skill files](#skill-files) for the Japanese exception. |
| Commit summaries, Issue and PR titles, and `Summary` sections | English, so that they are easy to search and scan. |
| Other Issue and PR sections, and comments | Japanese by default. They do not need to repeat everything in both languages. |

Keep commit summaries short and specific, and follow the format in [Contributing](../../CONTRIBUTING.md).

## Skill files

Each Skill has one source file, `SKILL.md`, and it is written in English by default.\
Keep proper nouns, configuration keys, and established technical terms in their original form.\
Use agent-specific jargon only when it is essential to the Skill.

A Skill whose main purpose is writing or editing Japanese may use a Japanese `SKILL.md` as its source.\
In that case, document the exception and its provenance, and do not add a `SKILL-ja.md`.

## Japanese reference translations

Japanese reference translations let the maintainer understand and review the repository without translating the same material repeatedly.\
The English file defines the requirements.\
A translation keeps its meaning and adds no requirements.

Start every Japanese reference translation with this notice, placed after the frontmatter if there is any.\
Adjust the filename and relative link to match the English file.

```markdown
> この文書は [英語版 SKILL.md](SKILL.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。
```

The following table lists each English file and its Japanese reference translation.\
When an English file changes, use the table to find its translation.

| English file | Source language | Japanese reference translation |
| --- | --- | --- |
| `skills/<skill-name>/SKILL.md` | English, or Japanese for a documented exception | `skills/<skill-name>/SKILL-ja.md`, only when the source is English |
| `README.md` | English | `README.ja.md` |
| `CONTRIBUTING.md` | English | `CONTRIBUTING-ja.md` |
| `AGENTS.md` | English | `AGENTS-ja.md` |
| `CLAUDE.md` | English | `CLAUDE-ja.md` |
| `docs/<audience>/*.md` | English | `docs/ja/<audience>/*.md` |
| `.agents/skills/<tracked-skill>/SKILL.md` | English, or Japanese for a documented exception | `.agents/skills/<tracked-skill>/SKILL-ja.md`, only when the source is English |

`<audience>` is `users` or `maintainers`.

If a new English file matches no row, add a row for it here.\
If the table does not identify exactly one translation for a file, do not guess a filename or create a translation.\
Report the undecided pair instead, so that it can be decided and recorded here.

## Update translations when the source changes

When you add or change an English source file, review its Japanese translation in the same change:

| Change to the English file | What to do with the translation |
| --- | --- |
| It affects the meaning or correct use. | Update or create the translation in the same change. |
| It does not affect what the Japanese conveys. | Leave the translation unchanged, and record why in the PR's verification or follow-up section. |

Meaning includes requirements, scope, exceptions, permissions, prohibitions, safety conditions, procedures, verification, links, and anything else needed for correct use.

When a translation refers to a concept specific to this repository, or to a word that can point to different things, check the [glossary](glossary.md).

Use the repository-local `maintain-japanese-references` Skill to make this review and update.\
Skills whose source is Japanese are outside this process and do not get a `SKILL-ja.md`.
