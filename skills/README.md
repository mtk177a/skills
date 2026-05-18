# skills/ ディレクトリ運用ルール

`skills/` 配下には、1 Skill ごとに 1 ディレクトリを作ります。各 Skill は次の構成を基本にします。

```text
skills/<skill-name>/
├── SKILL.md
├── evals/
├── references/
├── scripts/
└── assets/
```

`SKILL.md` は必須です。`evals/`, `references/`, `scripts/`, `assets/` は必要な場合だけ追加します。

## 基本ルール

- 各 Skill は `skills/<skill-name>/SKILL.md` とする
- `<skill-name>` は kebab-case にする
- Skill の種類ごとに `common/`, `codex/`, `claude-code/` などの分類ディレクトリは作らない
- エージェント固有の違いは Skill 名または `description` で区別する

## SKILL.md の必須 frontmatter

`SKILL.md` には最低限、次の frontmatter を入れます。

```yaml
---
name: my-skill
description: いつ使う Skill かが分かる短い説明
---
```

### `name` の書き方

- ディレクトリ名と整合する名前にする
- kebab-case を使う
- 役割が伝わる短い名前にする
- リポジトリ固有やエージェント固有の Skill は、`codex-*` のような短い接頭辞で区別してよい

### `description` の書き方

- 「何をする Skill か」だけでなく「いつ使う Skill か」が分かるように書く
- 特定のエージェント依存の前提があるなら、その前提が読み取れるように書く
- 長すぎる一般論ではなく、利用場面が想像できる表現にする

## scripts/ を置く場合の注意

- スクリプトは、その Skill を成立させる補助処理に限定する
- OS 依存、シェル依存、ローカル環境依存が強いものは避ける
- 実行に追加依存が必要なら、`SKILL.md` か関連ドキュメントに明記する
- 秘密情報やローカル絶対パスを埋め込まない

## references/ を置く場合の注意

- Skill の判断材料になるメモ、テンプレート、参照資料だけを置く
- 外部サイトの内容を無批判にコピーしない
- 一時メモ置き場にしない
- 顧客情報、社内 URL、秘密情報を含めない

## evals/ を置く場合の注意

- Skill 単体の経験的レビューやシナリオメモを置く
- シナリオ、チェックリスト、ledger seed のような「再実行可能な評価資産」を優先する
- 複数 Skill をまたぐ評価は、`empirical-prompt-tuning` Skill に基づく運用資料として、個別 Skill に重複配置せず `docs/empirical-prompt-tuning/` 配下にまとめる
- 実行ログの生データを無制限に溜めず、要点だけを残す

## assets/ を置く場合の注意

- 画像、テンプレート断片、配布可能な補助素材のみを置く
- ライセンスや配布条件が不明な外部素材は入れない
- 大きすぎる生成物や一時ファイルは置かない

## 新規 Skill 作成時のチェックリスト

- ディレクトリ名は kebab-case になっているか
- `skills/<skill-name>/SKILL.md` を作っているか
- `name` と `description` の frontmatter を入れているか
- `description` から利用場面が分かるか
- Codex 専用前提を残すべきか、他のエージェントでも使える表現に寄せるべきか確認したか
- `scripts/`, `references/`, `assets/` は本当に必要なものだけに絞っているか
- 秘密情報、個人情報、社内固有情報を含めていないか
