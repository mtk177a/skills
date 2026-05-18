# Core Skill Flows

未使用になった chain Skill の代わりに、現在の中核 Skill をどう並べて使うかの最小限の flow だけを残す。

## 基本フロー

`scope-request` -> `design-changes` -> `implement-changes` -> `review-changes` -> `validate-fix`

- `scope-request`: 依頼の目的、完了条件、制約、前提、未解決事項を整理する
- `design-changes`: 変更対象、対象外、リスク、テスト戦略、停止条件を設計する
- `implement-changes`: TDD 前提で小さく実装し、検証への引き継ぎを残す
- `review-changes`: 差分をレビューし、Must-fix / Should-fix / Nice-to-have を整理する
- `validate-fix`: 確認済み、未確認、残るリスクを分けて確認結果をまとめる

## レビュー指摘対応フロー

`triage-review-feedback` -> `implement-changes` -> `validate-fix`

- `triage-review-feedback`: 既存レビュー指摘を採用、保留、却下に分け、対応方針を決める
- `implement-changes`: 採用した指摘だけを対象に修正を進める
- `validate-fix`: 修正後の確認結果と未確認事項を整理する

## 停止条件

- docs / skills / AGENTS の編集
- 依存追加や大きな設計変更
- 破壊的変更や高リスク変更
- 仕様未確定のまま進む必要がある場合

上記に当たる場合は flow を止め、承認や追加確認を挟む。
