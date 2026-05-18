# agent-skills

自作したエージェント向け Skill と、自分で継続的に手を入れて保守するエージェント向け Skill を管理するための個人用リポジトリです。

Codex、Claude Code、GitHub Copilot など複数のコーディングエージェントから参照しやすい、単純で移植しやすい構成を維持します。
MacBook Pro M1 と Windows WSL の両方で扱う前提のため、OS 固有の前提を持ち込まない方針です。

## このリポジトリに入れるもの

- 自作した Skill
- 外部 Skill を参考にしつつ、自分で内容を見直して改変した Skill
- Skill の運用ルール、作成ルール、移行メモ

## このリポジトリに入れないもの

- 外部 Skill のコピー置き場
- 一時的に試すだけの未整理な Skill
- 顧客名、社内 URL、秘密情報、API key、個人情報を含む内容
- チーム Skill リポジトリに置くべき共有前提の運用ルール

外部 Skill の導入管理は、このリポジトリではなく dotfiles 側の `apm.yml` / `apm.lock.yaml` で行う想定です。
このリポジトリは「何を配布・同期するか」ではなく、「自分が保守する Skill の中身をどう持つか」に責務を絞ります。

## ディレクトリ構成

```text
.
├── README.md
├── docs/
│   ├── migration-from-codex-config.md
│   ├── skill-authoring.md
│   └── empirical-prompt-tuning/
│       └── core-skills/
└── skills/
    ├── README.md
    └── <skill-name>/
        ├── SKILL.md
        ├── evals/
        ├── references/
        ├── scripts/
        └── assets/
```

`references/`, `scripts/`, `assets/`, `evals/` は必要な Skill のみが持つ任意ディレクトリです。
最初から `common/`, `codex/`, `claude-code/` のような分類ディレクトリは作りません。
エージェント固有の違いは Skill 名または `description` で区別します。

複数 Skill をまたぐ経験的レビューのように、`empirical-prompt-tuning` Skill に基づく評価運用の補助資料は `docs/empirical-prompt-tuning/` 配下に置きます。

## Skill の作成ルール

- Skill 名は kebab-case にする
- 各 Skill は `skills/<skill-name>/SKILL.md` を必須とする
- `SKILL.md` の必須 frontmatter は `name` と `description`
- `description` は「いつ使う Skill なのか」がすぐ分かるように書く
- 補助ファイルは、その Skill のディレクトリ配下に閉じる

詳細は [skills/README.md](skills/README.md) と [docs/skill-authoring.md](docs/skill-authoring.md) にまとめます。

## 外部 Skill との責務分離

外部 Skill はこのリポジトリにコピーしません。
たとえば `gh skill`、`microsoft apm`、`vercel-labs/skills` のような外部配布物は、dotfiles 側で導入と固定を管理します。

- dotfiles: `apm.yml` / `apm.lock.yaml` で外部 Skill の取得元とバージョンを管理する
- `agent-skills`: 自作または自分で改変した Skill の中身を管理する
- プロジェクトリポジトリ: プロジェクト固有の設定や運用ドキュメントを持つ
- チーム Skill リポジトリ: チーム共有前提の Skill や運用ルールを持つ

この分離により、個人用の試行錯誤と共有用の整備を混ぜずに保てます。

## 利用例

`gh skill` から参照する場合は、このリポジトリの `skills/<skill-name>/SKILL.md` を参照対象として扱いやすい構成にしておきます。
実行は不要ですが、README 上の例としては次のような形を想定します。

```bash
# gh skill から特定 skill を参照するイメージ
gh skill view ./skills/my-skill/SKILL.md
```

`microsoft apm` から参照する場合も、エージェント固有の分類ディレクトリを増やさず、単純な `skills/<skill-name>/` 構成を保つことで扱いやすくします。

リポジトリルートには `apm.yml` を置き、このリポジトリ全体を「個別 Skill を束ねる APM パッケージ」としても扱えるようにします。
各 Skill ディレクトリは `SKILL.md` を持つため、`skills/<skill-name>` を個別パッケージとして参照する運用も継続できます。

```bash
# リポジトリ全体を 1 つのパッケージとして入れる
apm install mtk177a/agent-skills

# 特定 skill だけを個別に入れる
apm install mtk177a/agent-skills/skills/review-changes
apm install mtk177a/agent-skills/skills/draft-commit
```

インストール先のプロジェクトリポジトリに Harness Marker や `targets:` がない場合は、`apm install --target claude` のように target を明示します。
依存を宣言で管理したい場合は、利用側の `apm.yml` に次のように書けます。

```yaml
dependencies:
  apm:
    - mtk177a/agent-skills
    - mtk177a/agent-skills/skills/review-changes
```

実際の導入や配布の管理は dotfiles 側または利用側プロジェクトの `apm.yml` / `apm.lock.yaml` で行い、このリポジトリ自体は Skill ソースの保管場所兼 APM パッケージとして扱います。

このリポジトリをプライベートのまま `apm` で利用することもできます。
ただし、利用側には対象リポジトリへの読み取り権限と、GitHub プライベートリポジトリを取得できる認証設定が必要です。
認証情報はこのリポジトリや `apm.yml` に含めず、利用側の環境変数や git / APM の認証設定で扱います。

## 将来の位置づけ

このリポジトリは個人用です。将来的にチーム Skill リポジトリを別で持つ場合も、このリポジトリとは分離します。

- 個人用リポジトリ: 自分の作業スタイルに合わせた Skill を素早く改善する
- チームリポジトリ: 共有前提の品質基準、レビュー、サポート範囲を持つ

この前提を維持することで、個人用 Skill の更新速度と、共有物としての安定性を両立しやすくします。
