# GitHub Copilot Instructions

このリポジトリは、自作または継続保守する個人用エージェント向け Skill を管理するためのものです。

- まず `README.md`、`skills/README.md`、`docs/skill-authoring.md` を参照する
- Skill は `skills/<skill-name>/SKILL.md` を基本単位とする
- ディレクトリ名と `name` は kebab-case を前提にする
- `SKILL.md` の frontmatter には最低限 `name` と `description` を入れる
- エージェント固有差分は Skill 名や `description` で表し、`common/` やエージェント別分類ディレクトリは作らない
- `evals/`, `references/`, `scripts/`, `assets/` は必要な場合だけ追加する
- 外部 Skill の単純コピーを提案しない
- 秘密情報、個人情報、顧客情報、社内 URL を含めない
- OS 固有前提やローカル絶対パスを既定にしない
- 既存の Skill / docs の文体に合わせ、日本語主体で簡潔に書く
- リポジトリルール文書や Skill 本文を変える提案では、承認境界に注意する
