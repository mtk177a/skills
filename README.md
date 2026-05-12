# agent-skills

`mtk177a/agent-skills` は、自作した Agent Skill と、自分で継続的に手を入れて保守する Agent Skill を管理するための個人用リポジトリです。

Codex、Claude Code、GitHub Copilot など複数の coding agent から参照しやすい、単純で移植しやすい構成を維持します。MacBook Pro M1 と Windows WSL の両方で扱う前提のため、OS 固有の前提を持ち込まない方針です。

## このリポジトリに入れるもの

- 自作した skill
- 外部 skill を参考にしつつ、自分で内容を見直して改変した skill
- skill の運用ルール、作成ルール、移行メモ

## このリポジトリに入れないもの

- 外部 skill のコピー置き場
- 一時的に試すだけの未整理な skill
- 顧客名、社内 URL、秘密情報、API key、個人情報を含む内容
- team skills repo に置くべき共有前提の運用ルール

外部 skills の導入管理は、このリポジトリではなく dotfiles 側の `apm.yml` / `apm.lock.yaml` で行う想定です。この repo は「何を配布・同期するか」ではなく、「自分が保守する skill の中身をどう持つか」に責務を絞ります。

## 移行方針

将来的な移行元は `mtk177a/codex-config` の `skills/personal` 配下です。

ただし今回は初期整備のみとし、skill 本体は新規作成しません。先にこの repo の器を整え、既存 skill を手動で移してから `frontmatter` と `description` を見直す運用にします。

既存 skill をそのまま機械的にコピーするのではなく、移行時に次を確認します。

- この repo に置くべき自作 skill か
- Codex 固有の前提を残すべきか、他 agent でも読める形に寄せるべきか
- `name` と `description` が現在の用途に合っているか

## ディレクトリ構成

```text
.
├── README.md
├── docs/
│   ├── migration-from-codex-config.md
│   └── skill-authoring.md
└── skills/
    ├── .gitkeep
    ├── README.md
    └── <skill-name>/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

`references/`, `scripts/`, `assets/` は必要な skill のみが持つ任意ディレクトリです。最初から `common/`, `codex/`, `claude-code/` のような分類ディレクトリは作りません。agent 固有の違いは skill 名または `description` で区別します。

## Skill の作成ルール

- skill 名は kebab-case にする
- 各 skill は `skills/<skill-name>/SKILL.md` を必須とする
- `SKILL.md` の必須 frontmatter は `name` と `description`
- `description` は「いつ使う skill なのか」がすぐ分かるように書く
- 補助ファイルは、その skill のディレクトリ配下に閉じる

詳細は [skills/README.md](/home/motoki/projects/personal/agent-skills/skills/README.md) と [docs/skill-authoring.md](/home/motoki/projects/personal/agent-skills/docs/skill-authoring.md) にまとめます。

## 外部 skills との責務分離

外部 skill はこの repo にコピーしません。たとえば `gh skill`、`microsoft apm`、`vercel-labs/skills` のような外部配布物は、dotfiles 側で導入と固定を管理します。

- dotfiles: `apm.yml` / `apm.lock.yaml` で外部 skills の取得元とバージョンを管理する
- `agent-skills`: 自作または自分で改変した skills の中身を管理する
- project repo: プロジェクト固有の設定や運用ドキュメントを持つ
- team skills repo: チーム共有前提の skill や運用ルールを持つ

この分離により、個人用の試行錯誤と共有用の整備を混ぜずに保てます。

## 利用例

`gh skill` から参照する場合は、この repo の `skills/<skill-name>/SKILL.md` を参照対象として扱いやすい構成にしておきます。実行は不要ですが、README 上の例としては次のような形を想定します。

```bash
# gh skill から特定 skill を参照するイメージ
gh skill view ./skills/my-skill/SKILL.md
```

`microsoft apm` から参照する場合も、agent 固有の分類ディレクトリを増やさず、単純な `skills/<skill-name>/` 構成を保つことで扱いやすくします。

```bash
# apm でローカル skill ディレクトリを参照するイメージ
apm skill inspect ./skills/my-skill
```

上記コマンドはあくまで利用イメージです。実際の導入や配布の管理は dotfiles 側で行い、この repo 自体は skill ソースの保管場所として使います。

## 将来の位置づけ

この repo は個人用です。将来的に team skills repo を別で持つ場合も、この repo とは分離します。

- 個人用 repo: 自分の作業スタイルに合わせた skill を素早く改善する
- team repo: 共有前提の品質基準、レビュー、サポート範囲を持つ

この前提を維持することで、個人用 skill の更新速度と、共有物としての安定性を両立しやすくします。
