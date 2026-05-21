# break-failure-loop evals

`break-failure-loop` の単体運用を評価するためのメモです。同じ失敗の反復を止め、試行履歴、仮説、次の一手を圧縮して返せるかを見ます。

## Iter 0

- `description` と本文が「失敗ループの停止」に揃っているか
- 事実と推測が分かれているか
- 仮説数と次の一手の上限が守られているか
- 実装継続より停止を提案できるか

## Scenarios

### Scenario A: 同じテストが 2 回以上失敗

同系統の修正を重ねても解決していない。履歴を整理し、次の確認を 1 つに絞る。

Requirements checklist:

1. [critical] 次の一手を 1 つだけ提案する
2. 成功した確認と失敗した確認を分ける
3. 仮説を最大 3 つに絞る

### Scenario B: 追加変更より停止が妥当

変更量だけが増えており、同じ仮説のまま続けるのが危険。停止判断を返す。

Requirements checklist:

1. [critical] 続行ではなく停止を提案できる
2. 停止理由が事実ベースである
3. 追加で読むべきファイルが絞られている

## Failure Ledger Seed

- `facts and hypotheses conflated`
- `next step not narrowed`
- `keeps editing despite repeated same-path failures`
