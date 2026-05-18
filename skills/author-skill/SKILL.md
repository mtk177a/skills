---
name: author-skill
description: 新しい Skill を設計・起草したいときや、既存 Skill を大きく作り直したいときに使う。
---

# Author Skill

## 目的

- 新しい Skill の提案を、既存ルールと重複確認を踏まえて組み立てる。
- 既存 Skill の大きな再設計時に、責務、境界、出力契約を整理する。

## 使う場面

- 新しい Skill を追加したい
- 既存 Skill を大きく改修したい (責務/境界/構成が変わる)
- どんな `name`、`description`、境界で定義すべきか決めたい
- 依頼がまだ抽象的で、まず利用場面を 1 文に固定してから Skill 案へ落としたい

## 入力 (任意)

- 目的、対象作業、想定利用者
- 関連する既存 Skill、README、docs
- 必要なら移行元 Skill や参考にしたい構成

## 手順

1. 一次情報として `skills/README.md` と `docs/skill-authoring.md` を確認する。
2. 目的、範囲、対象ユーザーを 1〜2 行で定義する。抽象的な依頼しかない場合は、先に利用場面を 1 文で固定する。
3. 既存 Skills との重複、競合、統合候補を確認する。
4. `name` と `description` を決める。利用場面が読み取れることを優先し、責務境界が未確定なら仮称のまま承認を取る。
5. 境界 (`Always` / `Ask first` / `Never`) を定義する。
6. 手順、出力フォーマット、必要なら補助ディレクトリ (`evals/`, `references/`, `scripts/`, `assets/`) の要否を決める。
7. 影響範囲 (`AGENTS.md` / docs / scripts / `apm.yml`) を列挙する。
8. 差分提案 → 承認 → 実装の順で進める。
9. Markdown 編集が含まれる場合は `format-markdown` の適用判断を行う。

## 出力フォーマット (提案時)

- 変更点の要約: ...
- 目的・範囲: ...
- 競合/重複: ...
- 一次情報: ...
- メタデータ:
  - name: ...
  - description: ...
- 手順:
  1. ...
- 境界:
  - Always: ...
  - Ask first: ...
  - Never: ...
- 補助ディレクトリの要否: ...
- 影響範囲: ...
- 承認: この方針で進めてよいですか？

## 境界

### Always:

- 目的・範囲・境界を明記する
- `skills/README.md` と `docs/skill-authoring.md` を一次情報として扱う
- 既存 Skills との重複を確認する
- `description` から利用場面が分かるようにする
- 入力が抽象的なときは、`name` を急いで確定せず利用場面を先に固定する

### Ask first:

- `AGENTS.md` の記述変更
- 既存 Skill の大幅な再設計

### Never:

- 勝手に大きな変更を実行する
- 依存追加や外部コードの無断流用

## 注意点 (任意)

原則:

- 変更は小さく・レビュー可能な単位
- 既存スタイルと整合
- 明確な境界 (`Always` / `Ask first` / `Never`)
- `description` は短く、利用場面が分かる表現を優先する
- 一般ガイドの全文再掲は避け、必要なルールは `docs/skill-authoring.md` への導線で補う
