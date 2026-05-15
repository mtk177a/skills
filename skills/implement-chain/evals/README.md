# implement-chain evals

`implement-chain` の単体運用を評価するためのメモです。`intake` から `validate-fix` までの進行と承認境界を管理し、各段の受け渡し要約を保てるかを見ます。

## Iter 0

- `description` と本文が「段階的な実装チェーン」に揃っているか
- 標準段階と条件付き段階が分かれているか
- 受け渡し要約の必須項目が残るか
- 承認境界と停止条件が明確か

## Scenarios

### Scenario A: 通常の段階進行

依頼整理から設計、実装、レビュー、確認までを順に進める。重大指摘は出ない。

Requirements checklist:

1. [critical] `intake -> design -> build -> code-review -> validate-fix` の標準順序が保たれる
2. 各段の要点が次段へ受け渡される
3. 最終結果が段階ごとに残る

### Scenario B: code-review で Must-fix が出る

実装後レビューで重大指摘が出る。`triage-review` を条件付きで挟み、承認境界を崩さずに戻す。

Requirements checklist:

1. [critical] Must-fix を無視して `validate-fix` へ進まない
2. `triage-review` を条件付き段階として扱う
3. 承認が必要な変更なら chain を止める
4. `triage-review` の後は `build` に戻る
5. 修正後に再度 `code-review` を行う

## Failure Ledger Seed

- `conditional stage treated as default`
- `handoff summary missing required fields`
- `approval boundary bypassed inside chain`
- `must-fix loop skips rebuild or re-review`
