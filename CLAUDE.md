# CLAUDE.md

このファイルは Claude Code 向けの補助文書です。リポジトリの正式な契約は `AGENTS.md` を優先します。

## 最初に確認すること

- `AGENTS.md`
- `README.md`
- `skills/README.md`
- `docs/authoring.md`

## このリポジトリで期待する振る舞い

- `skills/<skill-name>/SKILL.md` を基本単位として扱う
- 新規 Skill や編集対象 Skill では、frontmatter の `name` と `description` を前提に整合を取る
- 既存の Skill や docs の文体に合わせ、日本語主体で簡潔に書く
- エージェント固有差分は Skill 名や説明で表し、エージェント別ディレクトリを増やさない

## 進め方

- 実装前に既存の Skill と関連 docs を読み、重複や矛盾を避ける
- Skill 本文では、利用場面、前提条件、禁止事項、出力期待を優先する
- 外部 Skill の導入はコピーではなく、必要なら参照元と保守方針を明示して相談する

## 承認境界

- `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` の編集は承認後に行う
- `skills/*/SKILL.md` や `docs/*` の編集も承認後に行う
- 依存追加やリポジトリ方針変更は、理由と影響を示してから進める

## 禁止事項

- 秘密情報、個人情報、社内情報を追加しない
- 一時メモや未整理な試作を、そのままリポジトリに残さない
- OS 固有コマンドやローカル環境前提を、説明なしに埋め込まない
