# AGENTS.md

このファイルは `~/.codex/AGENTS.md` を、このリポジトリ向けに補足・上書きするための指示です。
より深い階層に `AGENTS.md` があれば、そちらを優先します。

## このリポジトリの目的

- 自作したエージェント向け Skill と、自分で継続保守するエージェント向け Skill を管理する
- Codex、Claude Code、GitHub Copilot など複数のエージェントから参照しやすい単純な構成を保つ
- MacBook Pro M1 と Windows WSL の両方で扱えるよう、OS 固有前提を持ち込まない

## 一次情報として先に読むもの

- `README.md`
- `skills/README.md`
- `docs/skill-authoring.md`

Skill 作成や編集では、既存の `skills/*/SKILL.md` も確認し、書きぶりを合わせます。

## このリポジトリに入れるもの

- 自作した Skill
- 外部 Skill を参考にしつつ、自分で内容を見直して改変した Skill
- Skill の運用ルール、作成ルール、移行メモ

## このリポジトリに入れないもの

- 外部 Skill の単純コピー
- 一時的に試すだけの未整理な Skill
- 顧客名、社内 URL、秘密情報、API key、個人情報を含む内容
- チーム共有前提の運用ルール

## 構成ルール

- Skill は `skills/<skill-name>/SKILL.md` を基本単位とする
- `<skill-name>` は kebab-case を使う
- `SKILL.md` の frontmatter には最低限 `name` と `description` を入れる
- `evals/`, `references/`, `scripts/`, `assets/` は必要な Skill だけが持つ
- `common/`, `codex/`, `claude-code/` のようなエージェント別分類ディレクトリは作らない
- エージェント固有の違いはディレクトリ構成ではなく Skill 名や `description` で表現する

## 作業ルール

- 変更は小さく、レビューしやすい単位に保つ
- 文書本文は日本語主体で書き、固有名詞・設定キー・既存で定着した技術用語だけを英語で残す
- 本文中の一般概念としては `Agent` / `Subagent` ではなく `エージェント` / `サブエージェント` を使う
- リポジトリ固有ルールは一般論で膨らませず、このリポジトリで必要な契約だけを書く
- Skill 本文は、何をするかより「いつ使うか」「何を入力にするか」「何を避けるか」を優先して書く
- 他のエージェントでも読まれる前提で、ローカル絶対パスや環境依存情報を埋め込まない
- 追加スクリプトや補助資料は、その Skill を成立させる最小限に絞る

## コミットメッセージ運用

- コミットメッセージは Conventional Commits を使い、summary は日本語で短く具体的に書く
- 1 つのコミットは 1 主題を基本とし、無関係な変更を混ぜない
- `skills/*/SKILL.md` はこのリポジトリの成果物として扱い、一律に `docs` としない
- 新しい Skill の追加や、既存 Skill に新しい振る舞いを加える変更は `feat` を基本にする
- 既存 Skill の不整合や判断ミスの修正は `fix` を基本にする
- Skill の rename、責務整理、構造再編など、振る舞いを増やさない整理は `refactor` を基本にする
- `README.md`、`docs/*`、`skills/*/evals/README.md` など、説明や評価記録の更新は `docs` を基本にする
- `apm.yml` や参照更新は、それ単体ではなく主目的となる変更の type に合わせる

## 承認が必要な作業

- `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` の編集
- `skills/*/SKILL.md`、`docs/*`、運用ルール文書の編集
- 外部 Skill の取り込み、依存追加、配布元の変更
- リポジトリの責務やディレクトリ構成方針を変える変更

## 避けること

- 外部配布 Skill を無批判にコピーして置くこと
- 秘密情報や非公開情報を Skill、docs、scripts、assets に含めること
- OS 依存やエージェント依存を、説明なしに既定前提として持ち込むこと
- リポジトリルールを変える変更を、承認なしで進めること
