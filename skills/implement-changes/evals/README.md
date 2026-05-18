# implement-changes evals

`implement-changes` の単体運用を評価するためのメモです。`design-changes` の出力がなくても、着手可否、現在地、次の一手を安全に返せるかを見ます。

## Iter 0

- `description` と本文が「main agent による小さな実装」に揃っているか
- `Blocked` と Red/Green/Refactor が分かれているか
- 着手条件未充足時の止まり方が明確か
- 検証への引き継ぎ内容が残るか

## Scenarios

### Scenario A: design-changes なしの小修正

変更要求、対象ファイル、テストコマンドだけが与えられる。着手条件を自分で整理し、最初の 1 テストを決める。

Requirements checklist:

1. [critical] `design-changes` がなくても着手条件を確認する
2. 最初の 1 テストが明示される
3. 現在のフェーズが `Blocked` / `Red` / `Green` / `Refactor` のいずれかで示される

### Scenario B: 仕様未確定で停止

依頼はあるが、仕様とテスト方針が足りない。無理に Red へ入らず止まる。

Requirements checklist:

1. [critical] 不足前提を隠さず `Blocked` で止まる
2. 次の一手が確認行為になっている
3. 停止理由と対象範囲が両方残る

## Failure Ledger Seed

- `requires design-changes output to function`
- `blocked and red conflated`
- `next step skips missing prerequisite`
