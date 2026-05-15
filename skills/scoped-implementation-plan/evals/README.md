# scoped-implementation-plan evals

`scoped-implementation-plan` の単体運用を評価するためのメモです。広い依頼を、Goal、編集範囲、検証方法、停止条件が明確な小さな実装単位へ落とせるかを見ます。

## Iter 0

- `description` と本文が「探索範囲を絞る実装前計画」に揃っているか
- Goal と Non-goal が分かれているか
- 編集可否ファイルと Stop conditions が残るか
- 検証コマンド不明時に推測で埋めないことが明確か

## Scenarios

### Scenario A: 広い Issue を小さく切る

依頼範囲が広い。今回やることとやらないこと、読むファイル、編集範囲を固定する。

Requirements checklist:

1. [critical] Goal と Non-goal を分ける
2. `Files allowed to edit` と `Files not to edit` が両方ある
3. Done when が小さくレビュー可能な粒度である

### Scenario B: 検証方法が不明なままの依頼

実装対象は見えているが、どのテストやコマンドで確認すべきか分からない。推測せず止まる。

Requirements checklist:

1. [critical] 検証コマンド不明時に未確定として止まる
2. scope 拡大条件が Stop conditions に残る
3. docs や設定変更が必要なら Ask first 境界として扱う

## Failure Ledger Seed

- `goal and non-goal blurred`
- `editable boundary missing`
- `validation command guessed`
