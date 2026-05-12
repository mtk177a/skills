---
name: codex-create-skill
description: Codex 向けに Skill を新規作成したいときや、大きく作り直したいときに使う。
---

# Skill Authoring (Skill作成手順)

## 目的

Skill を安全・一貫した品質で作るための手順とチェックリストを提供する。

## 使う場面

- 新しい Skill を追加したい
- 既存 Skill を大きく改修したい (責務/境界/構成が変わる)

## 入力 (任意)

- 特になし

## 手順

1. 目的・範囲・対象ユーザーを1〜2行で定義する
2. 既存 Skills との重複/競合を確認する
3. `name` と `description` を決める (トリガー語を含める)
4. 境界 (Always / Ask first / Never) を定義する
5. 手順と出力テンプレートを設計する
6. 影響範囲 (AGENTS.md / docs / scripts) を列挙する
7. 差分提案 → 承認 → 実装の順で進める
8. Markdown 編集が含まれる場合は `format-markdown` の適用判断を行う

## 出力フォーマット (提案時)

- 変更点の要約: ...
- 目的・範囲: ...
- 競合/重複: ...
- メタデータ:
  - name: ...
  - description: ...
- 手順:

  1) ...

- 境界:
  - Always: ...
  - Ask first: ...
  - Never: ...
- 影響範囲: ...
- 承認: この方針で進めてよいですか？


## 境界

### Always:

- 目的・範囲・境界を明記する
- 既存 Skills との重複を確認する

### Ask first:

- AGENTS.md の記述変更
- 既存 Skill の大幅な再設計

### Never:

- 勝手に大きな変更を実行する
- 依存追加や外部コードの無断流用

## 注意点 (任意)

原則:

- 変更は小さく・レビュー可能な単位
- 既存スタイルと整合
- 明確な境界 (Always/Ask/Never)
- description は短く、トリガー語を含める

標準フォーマット (推奨):
以下の構成に統一する。

1. H1タイトル
2. 目的
3. 使う場面
4. 入力 (任意)
5. 手順
6. 出力フォーマット
7. 境界 (Always / Ask first / Never)
8. 注意点 (任意)

テンプレート例:

```markdown
---
name: <skill-name>
description: <日本語の短い説明 (trigger wordsは英語でOK)>
---

# <Skill Title>

## 目的

- ...

## 使う場面

- ...

## 入力 (任意)

- ...

## 手順

1. ...

## 出力フォーマット

## 境界

### Always:

- ...

### Ask first:

- ...

### Never:

- ...

## 注意点 (任意)

- ...
```
