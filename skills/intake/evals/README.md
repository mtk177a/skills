# intake evals

`intake` の単体運用を評価するためのメモです。`design` や `build` への受け渡しではなく、この skill 単独で依頼整理と次判断の材料を返せるかを見ます。

## Iter 0

- `description` と本文が「依頼整理」に揃っているか
- 目的、完了条件、制約、前提、未解決事項が分離されているか
- 単体で次の判断や確認依頼に進める出力になっているか

## Scenarios

### Scenario A: あいまいな改善依頼

依頼文は短く、背景はあるが完了条件が曖昧。実装には入らず、依頼整理だけを求める。

Requirements checklist:

1. [critical] 目的と完了条件を分けて書く
2. 制約と前提を分けて書く
3. 未解決事項と確認したい点を分ける
4. 次のステップが単体で読んでも分かる

### Scenario B: 制約付きの不具合相談

症状と制約はあるが、再現条件や対象範囲が不足している。確認事項を明示し、無理に設計へ進まない。

Requirements checklist:

1. [critical] 情報不足を未解決事項として残す
2. 制約を前提や背景と混同しない
3. 確認したい点が具体的である

## Failure Ledger Seed

- `goal and done conflated`
- `constraints mixed with assumptions`
- `next step only meaningful inside a flow`
