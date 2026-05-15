---
name: record-session-handoff
description: AIエージェントとの会話で決定事項を外部メモ化し、別セッションへ安全に引き継ぐ。session memory, handoff, notes, context continuity
---

# Record Session Handoff (セッション横断メモ運用)

## 目的

- セッションごとの決定事項・未決事項・次アクションを外部メモとして残し、別セッションでも同じ文脈で再開できる状態を作る。

## 使う場面

- 会話コンテキストが長くなり、別セッションに切り替えたいとき
- 複数フェーズの作業を分けて進めたいとき
- 一度決めた方針を次回以降も再利用したいとき

## 入力 (任意)

- 対象プロジェクト名
- 現在のタスク名
- セッションログの保存先
- 最新 handoff の保存先
- 永続化する decisions の保存先
- 今回の決定事項/未決事項
- 次セッションで最初にやること

## 手順

1. メモ対象のプロジェクトを特定する。
2. セッション開始時に、入力された最新 handoff の保存先を確認し、前回からの継続事項を明確化する。
3. 作業中に重要な決定事項だけを抽出し、確定/保留を分ける。
4. セッション終了時に、入力されたセッションログの保存先へ記録を作成または更新する。
5. 入力された最新 handoff の保存先に、次セッション用の要約を更新する。
6. 確定した方針だけを、入力された decisions の保存先へ昇格する。

## 出力フォーマット

```md
Session Log:
- Date: YYYY-MM-DD
- Topic: ...
- Decisions:
  - ...
- Open Questions:
  - ...
- Next Actions:
  - ...

Handoff (latest):
- Current Goal: ...
- Must-keep Context:
  - ...
- First Step Next Session:
  - ...
```

## 境界

### Always:

- セッション開始時に最新 handoff を確認する
- セッション終了時に Decisions / Open Questions / Next Actions を残す
- 確定事項と未確定事項を分離して記録する

### Ask first:

- 既存の運用ルール文書 (AGENTS.md / docs) への反映
- 保存先が未指定のまま運用を始めること

### Never:

- 会話履歴だけを唯一の記録として扱う
- 未確定事項を確定事項として `decisions` に記録する
- 秘密情報をメモに書く

## 注意点 (任意)

- 1セッション1ログを基本にし、肥大化したログは次回開始前に要約する。
- 形式は固定しすぎず、必須項目 (Decisions / Open Questions / Next Actions) を優先する。
- 出力テンプレートは英語で記述している。セッション間の引き継ぎは agent や人間を問わず参照されるため、英語で統一している。
