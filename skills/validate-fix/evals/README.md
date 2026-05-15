# validate-fix evals

`validate-fix` の単体運用を評価するためのメモです。修正差分と確認事実があれば、この skill 単独で確認済み、未確認、残留リスクを分けられるかを見ます。

## Iter 0

- `description` と本文が「修正後確認」に揃っているか
- 確認済み、未確認、未実施が分離されているか
- 元の指摘や対応方針がある場合の対応付けがあるか
- 単体で進行可否の判断材料になるか

## Scenarios

### Scenario A: 修正後の基本確認

修正差分、実施テスト、レビュー指摘一覧が与えられる。解消できた指摘と未確認事項を分ける。

Requirements checklist:

1. [critical] 確認済みと未確認を混同しない
2. 元の指摘との対応関係が見える
3. 残るリスクが具体的である

### Scenario B: 未実施範囲が残る確認

一部のテストが未実施で、確認事実も限定的。Done 扱いせずに残す。

Requirements checklist:

1. [critical] 未実施範囲を問題なし扱いにしない
2. 現時点の見解が根拠付きで書かれる
3. 次の追加確認が読み取れる

## Failure Ledger Seed

- `validated and untested conflated`
- `validation detached from original concern`
- `residual risk omitted`
