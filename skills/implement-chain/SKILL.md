---
name: implement-chain
description: 依頼整理から設計、実装、レビュー、確認までを段階的に進めたいときに使う。
---

# Implement Chain (実装チェーン)

## 目的

- custom agent を順番に起動し、依頼整理から設計、実装、レビュー、確認までを一連で進める。
- main agent は orchestration と承認境界の管理に徹し、各工程の責務は専用 agent に委譲する。

## 使う場面

- custom agent 主体で実装フローを完走させたいとき
- 前段のアウトプットを次段へ渡しながら、役割分担を固定したいとき
- 設計、実装、レビュー、確認をまとめて進めたいとき
- main agent 自身で進める `build` ではなく、custom agent orchestration に切り替えたいとき

## 入力 (任意)

- 依頼文
- 対象ファイルや対象領域
- 制約
- 完了条件
- 実行可能なテストや lint コマンド

## 手順

1. 依頼の要点、対象、制約、完了条件を整理する。
2. `intaker` を起動し、目的、完了条件、制約、前提、未解決事項を整理させる。
3. `intaker` の出力を引き継いで `designer` を起動し、変更方針、対象と対象外、リスク、テスト戦略を固める。
4. `designer` の出力を引き継いで `builder` を起動し、Red -> Green -> Refactor の順で実装させる。
5. `builder` の出力を引き継いで `reviewer` を起動し、正しさ、安全性、回帰、テスト不足の観点でレビューさせる。
6. `reviewer` が Must-fix を出した場合は、指摘と根拠を整理する。仕様変更や承認事項、高リスク変更に触れる場合は chain を止めて承認を取り、それ以外は `builder` へ戻して修正後に再度 `reviewer` を実行する。
7. `reviewer` の Must-fix が解消したら、Should-fix と Nice-to-have は未解決事項として整理し、結果を引き継いで `validator` を起動し、確認済み、未確認、残留リスクを整理させる。
8. 各段の要点を main agent が必須項目付きの短い引き継ぎ要約に正規化し、次段へ渡す入力を明示してから進む。
9. docs / skills / AGENTS 編集や高リスク変更など承認が必要な作業に入る前は、chain を止めて承認を取る。
10. 最後に、chain 全体の結果、未解決事項、次の一手を統合して返す。

## 出力フォーマット

- チェーン対象: ...
- 現在の段階: `intaker` | `designer` | `builder` | `reviewer` | `validator` | Done
- 直前の受け渡し要約:
  - 直前の段階: ...
  - 対象範囲 / 対象ファイル: ...
  - 実施したコマンド / テストと結果: ...
  - 次段が処理すべき論点: ...
  - 未解決事項 / 前提: ...
  - 承認待ち事項: `あり` | `なし`
- 進行ログ:
  - ...
- 最終結果:
  - intake: ...
  - design: ...
  - build: ...
  - review: ...
  - validate: ...
- 未解決事項:
  - ...
- 次の一手: ...

## Companion skills (推奨)

- `draft-commit`
- `record-session-handoff`

## 境界

### Always:

- custom agent は `intaker` -> `designer` -> `builder` -> `reviewer` -> `validator` の順に起動する
- `reviewer` の Must-fix は、承認不要な範囲に限って `builder` へ戻す
- `reviewer` の Should-fix / Nice-to-have は未解決事項として扱い、自動で再実装しない
- 前段のアウトプットを必須項目付きで要約して次段へ渡す
- main agent は承認境界と全体進行を管理する
- 各 agent の標準出力を残し、最後に統合結果を返す

### Ask first:

- AGENTS.md / skills / docs の編集が必要な場合
- 依存追加や大きな設計変更が必要な場合
- 破壊的変更や高リスク変更が必要な場合

### Never:

- `builder` より前に実装を始める
- `reviewer` の重大指摘を無視して `validator` へ進む
- Should-fix / Nice-to-have を Must-fix と同列に自動で実装へ戻す
- 承認が必要な変更を chain の流れで黙って実行する
