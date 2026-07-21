> **注記:** 英語版 (`AGENTS.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# AGENTS.md（日本語参考訳）

このファイルは、このリポジトリで作業するエージェント向けの指示です。
より深い階層に `AGENTS.md` があれば、そちらを優先します。

## 目的

- 自作したエージェント向け Skill と、自分で継続保守する Skill を管理する
- Codex、Claude Code、GitHub Copilot など複数のエージェントから参照しやすい単純な構成を保つ
- macOS M1 と Windows WSL の両方に対応するため、OS 固有の前提を持ち込まない

## 最初に読むもの

- `README.md`
- `docs/authoring.md`

Skill を作成・編集する際は、既存の `skills/*/SKILL.md` も確認して文体を合わせます。

## このリポジトリに入れるもの

- 自作した Skill
- 外部 Skill を参考にしつつ、自分で継続的に改変・保守している Skill
- Skill の運用ルール、作成ルール、移行メモ

## このリポジトリに入れないもの

- 外部 Skill の単純コピー
- 試験的・未整理な Skill
- 顧客名、社内 URL、秘密情報、API key、個人情報を含む内容
- チーム共有前提の運用ルール

## 構成ルール

- 基本単位は `skills/<skill-name>/SKILL.md`
- `<skill-name>` は kebab-case
- `SKILL.md` の frontmatter には最低限 `name`、`description`、`license` を入れる
- `evals/`、`references/`、`scripts/`、`assets/` は必要な場合のみ追加する
- `common/`、`codex/`、`claude-code/` のようなエージェント別分類ディレクトリは作らない
- エージェント固有の差分は Skill 名や `description` で表現し、ディレクトリ構造には反映しない

## 作業ルール

- 変更は小さく、レビューしやすい単位に保つ
- Skill 本文は英語を原則とする。日本語の執筆・推敲そのものを目的とする Skill は、日本語の `SKILL.md` を正本として重複する `SKILL-ja.md` を省略できる。例外と出典は文書化する。
- ローカル絶対パスや環境依存情報を埋め込まない
- Skill 本文では「いつ使うか」「何を入力にするか」「何を避けるか」を優先する
- 補助スクリプトや参照資料は、その Skill を成立させる最小限に絞る
- このリポジトリのコンテキストを持たないエージェントでも読めることを前提に書く

## APM の検証

- このリポジトリでは、dry-run ではない `apm install` や `apm update` を実行しない。リポジトリ内の Skill が `.agents/skills/` に展開され、グローバルにインストールされたコピーと重複表示されるため。
- このリポジトリでの通常検証には、Skill を展開しないコマンドを使う。

  ```bash
  apm install --frozen --dry-run --no-policy
  apm pack --dry-run --offline
  ```

- 完全な install と `apm audit --ci --no-policy` は、このリポジトリ外の使い捨てコピーでのみ実行する。
- `apm.yml` は手動で管理し、再生成しない。Skill の追加・削除・名前変更時に依存一覧を更新する。
- `apm.yml` はこのリポジトリ自身の Skill に依存しているため、Skill とマニフェストの変更をコミット・push してから lockfile を更新する。
- lockfile は、使い捨てコピーで `apm update --yes` を実行し、生成された `apm.lock.yaml` だけをこのリポジトリへ反映して更新する。
- `apm.lock.yaml` の更新は、`fix: refresh APM lockfile after <change>` のような summary を使って別コミットにする。
- エージェントツールによって作成されることがあるため、空の `.agents/` ディレクトリは許容する。
- `.agents/` 配下にレビュー用メモ、一時ファイル、その他の作業用成果物を保存しない。代わりに、このリポジトリ外の一時ディレクトリを使う。
- APM によって展開された `.agents/skills/` と `apm_modules/` が存在する場合は削除する。

## コミットメッセージ運用

- Conventional Commits を使い、summary は英語で短く具体的に書く
- 1 コミット 1 主題を基本とし、無関係な変更を混ぜない
- `skills/*/SKILL.md` はこのリポジトリの成果物として扱い、一律に `docs` としない
- 新しい Skill の追加や新しい振る舞いの追加: `feat`
- 既存 Skill の不整合や判断ミスの修正: `fix`
- rename・責務整理・構造再編など振る舞いを増やさない整理: `refactor`
- `README.md`、`docs/*`、`skills/*/evals/README.md` などの更新: `docs`
- `apm.yml` や参照更新: 主目的となる変更の type に合わせる

## 承認が必要な作業

- `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` の編集
- `skills/*/SKILL.md`、`docs/*`、運用ルール文書の編集
- 外部 Skill の取り込み、依存追加、配布元の変更
- リポジトリの責務やディレクトリ構成方針を変える変更

## 避けること

- 外部 Skill を無批判にコピーして置くこと
- 秘密情報や非公開情報を Skill・docs・scripts・assets に含めること
- OS 依存やエージェント依存を、説明なしに既定前提として持ち込むこと
- リポジトリルールを変える変更を承認なしで進めること
