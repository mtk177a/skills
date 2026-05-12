# skills/ ディレクトリ運用ルール

`skills/` 配下には、1 skill ごとに 1 ディレクトリを作ります。各 skill は次の構成を基本にします。

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

`SKILL.md` は必須です。`references/`, `scripts/`, `assets/` は必要な場合だけ追加します。

## 基本ルール

- 各 skill は `skills/<skill-name>/SKILL.md` とする
- `<skill-name>` は kebab-case にする
- skill の種類ごとに `common/`, `codex/`, `claude-code/` などの分類ディレクトリは作らない
- agent 固有の違いは skill 名または `description` で区別する

## SKILL.md の必須 frontmatter

`SKILL.md` には最低限、次の frontmatter を入れます。

```yaml
---
name: my-skill
description: いつ使う skill かが分かる短い説明
---
```

### `name` の書き方

- ディレクトリ名と整合する名前にする
- kebab-case を使う
- 役割が伝わる短い名前にする

### `description` の書き方

- 「何をする skill か」だけでなく「いつ使う skill か」が分かるように書く
- 特定 agent 依存の前提があるなら、その前提が読み取れるように書く
- 長すぎる一般論ではなく、利用場面が想像できる表現にする

## scripts/ を置く場合の注意

- スクリプトは、その skill を成立させる補助処理に限定する
- OS 依存、シェル依存、ローカル環境依存が強いものは避ける
- 実行に追加依存が必要なら、`SKILL.md` か関連ドキュメントに明記する
- 秘密情報やローカル絶対パスを埋め込まない

## references/ を置く場合の注意

- skill の判断材料になるメモ、テンプレート、参照資料だけを置く
- 外部サイトの内容を無批判にコピーしない
- 一時メモ置き場にしない
- 顧客情報、社内 URL、秘密情報を含めない

## assets/ を置く場合の注意

- 画像、テンプレート断片、配布可能な補助素材のみを置く
- ライセンスや配布条件が不明な外部素材は入れない
- 大きすぎる生成物や一時ファイルは置かない

## 新規 skill 作成時のチェックリスト

- ディレクトリ名は kebab-case になっているか
- `skills/<skill-name>/SKILL.md` を作っているか
- `name` と `description` の frontmatter を入れているか
- `description` から利用場面が分かるか
- Codex 専用前提を残すべきか、他 agent でも使える表現に寄せるべきか確認したか
- `scripts/`, `references/`, `assets/` は本当に必要なものだけに絞っているか
- secrets、個人情報、社内固有情報を含めていないか
