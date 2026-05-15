# review-fix-chain evals

`review-fix-chain` の単体運用を評価するためのメモです。既存レビュー指摘を、採否判断から修正、確認まで段階的に処理できるかを見ます。

## Iter 0

- `description` と本文が「既存レビュー指摘の修正チェーン」に揃っているか
- 標準段階と条件付き `code-review` が分かれているか
- `triage-review` を通してから `build` へ進むことが明確か
- 単体で未対応指摘と残留リスクが残るか

## Scenarios

### Scenario A: 通常のレビュー修正

既存レビュー本文があり、採用した指摘だけを修正して確認する。

Requirements checklist:

1. [critical] `triage-review -> build -> validate-fix` の標準順序が保たれる
2. 採否未整理の指摘を直接 `build` に流さない
3. 未対応の指摘が分かれて残る

### Scenario B: 修正後に追加レビューが必要

修正後に差分の再レビューが必要になり、`code-review` を条件付きで追加する。

Requirements checklist:

1. [critical] `code-review` を常設段階ではなく条件付きとして扱う
2. Must-fix が出たら `triage-review` に戻す
3. 新規レビュー用途に逸脱しない

## Failure Ledger Seed

- `review findings sent to build without triage`
- `optional code-review treated as mandatory`
- `chain drifts into new-review workflow`
