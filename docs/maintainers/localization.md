# Languages

This guide is for maintainers and the agents working for them.\
It defines the language of each kind of content.

## Choose the language

- **Skill bodies**: English by default.\
  See [Skill files](#skill-files) for the Japanese exception.
- **Repository documents**: English.\
  This repository keeps no Japanese reference translations.
- **Commit summaries, Issue and PR titles, and `Summary` sections**: English, so that they are easy to search and scan.\
  Keep commit summaries short and specific, and follow the format in [Contributing](../../CONTRIBUTING.md).
- **Other Issue and PR sections, and comments**: Japanese by default.\
  They do not need to repeat everything in both languages.

## Skill files

Each Skill has one source file, `SKILL.md`, written in English by default.\
Keep proper nouns, configuration keys, and established technical terms in their original form.\
Use terms specific to one client only when they are essential to the Skill.

A Skill whose main purpose is writing or editing Japanese may use a Japanese `SKILL.md` as its source.\
Record the exception and where it was introduced in the list below.

| Skill | Introduced in |
| --- | --- |
| `skills/write-natural-japanese/` | [#43](https://github.com/mtk177a/skills/pull/43) |

The two upstream Gist mirrors are also in Japanese.\
They follow the copying rules in [Upstream Gist mirrors](authoring.md#upstream-gist-mirrors), not this exception.

## Use the glossary

Check the [glossary](glossary.md) for concepts of this repository, and for words that can point to different things.\
Add an entry only for one of these:

- a concept specific to this repository
- a word that currently points to two things that need to be distinguished

Add a general word only when its meanings mix, not only because its wording varies.\
For each entry, write what it refers to and why the distinction matters.
