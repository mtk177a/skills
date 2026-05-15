---
name: implement-chain
description: 依頼整理から設計、実装、レビュー、確認までを段階的に進めたいときに使う。
---

# Implement Chain (実装チェーン)

## 目的

- 依頼整理から設計、実装、レビュー、確認までを、段階ごとの成果物を確認しながら進める。
- 各段階の停止条件、承認境界、受け渡し要約を明確にし、手戻りを減らす。

## 使う場面

- 前段のアウトプットを次段へ渡しながら、作業段階を明確に分けたいとき
- 設計、実装、レビュー、確認をまとめて進めたいとき
- 単発の実装ではなく、停止条件と確認観点を含めて段階的に進めたいとき

## 入力 (任意)

- 依頼文
- 対象ファイルや対象領域
- 制約
- 完了条件
- 実行可能なテストや lint コマンド

## 手順

1. 依頼の要点、対象、制約、完了条件を整理する。
2. `intake` 段階で、目的、完了条件、制約、前提、未解決事項を整理する。
3. `design` 段階で、変更方針、対象と対象外、リスク、テスト戦略を固める。
4. `build` 段階で、Red -> Green -> Refactor の順で実装を進める。
5. `code-review` 段階で、正しさ、安全性、回帰、テスト不足の観点を確認する。
6. `code-review` で Must-fix が出た場合は、まず `triage-review` 段階で指摘の採否と対応方針を整理する。仕様変更や承認事項、高リスク変更に触れる場合は chain を止めて承認を取り、それ以外は `build` 段階へ戻して修正後に再度 `code-review` を行う。
7. `code-review` の Must-fix が解消したら、Should-fix と Nice-to-have は未解決事項として整理し、`validate-fix` 段階で確認済み、未確認、残留リスクを整理する。
8. 各段の要点を必須項目付きの短い引き継ぎ要約に正規化し、次段へ渡す入力を明示してから進む。
9. 並列調査、高リスク判断、品質補強が必要な場合だけ、別 agent / subagent の利用を提案する。
10. docs / skills / AGENTS 編集や高リスク変更など承認が必要な作業に入る前は、chain を止めて承認を取る。
11. 最後に、chain 全体の結果、未解決事項、次の一手を統合して返す。

## 出力フォーマット

- チェーン対象: ...
- 現在の段階: `intake` | `design` | `build` | `code-review` | `validate-fix` | Done
- 条件付き段階: `triage-review` (`code-review` で Must-fix が出た場合のみ)
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
  - code-review: ...
  - triage-review (必要時のみ): ...
  - validate-fix: ...
- 未解決事項:
  - ...
- 次の一手: ...

## Companion skills (推奨)

- `draft-commit`
- `record-session-handoff`

## 境界

### Always:

- 段階は `intake` -> `design` -> `build` -> `code-review` -> `validate-fix` を基本として進める
- `code-review` の Must-fix は、まず条件付き段階として `triage-review` で採否と対応方針を整理し、承認不要な範囲に限って `build` 段階へ戻す
- `code-review` の Should-fix / Nice-to-have は未解決事項として扱い、自動で再実装しない
- 前段のアウトプットを必須項目付きで要約して次段へ渡す
- 別 agent / subagent は既定で使わず、必要な場合だけ提案する
- 承認境界と全体進行を管理し、最後に統合結果を返す

### Ask first:

- AGENTS.md / skills / docs の編集が必要な場合
- 依存追加や大きな設計変更が必要な場合
- 破壊的変更や高リスク変更が必要な場合

### Never:

- `build` より前に実装を始める
- `code-review` の重大指摘を無視して `validate-fix` へ進む
- Should-fix / Nice-to-have を Must-fix と同列に自動で実装へ戻す
- 承認が必要な変更を chain の流れで黙って実行する
