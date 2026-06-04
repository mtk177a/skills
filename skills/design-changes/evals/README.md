# design-changes evals

`design-changes` の単体運用を評価するためのメモです。`scope-request` の有無に関係なく、実装可否と変更方針を単独で判断材料にできるかを見ます。

## Iter 0

- `description` と本文が「実装前の設計判断」に揃っているか
- 変更対象と変更対象外が分かれているか
- リスク、回避策、テスト戦略が単体で理解できるか
- 実装へ進む条件と停止条件が明示されているか
- 変更前に理解すべき概念と、ユーザーが説明すべき判断が残るか

## Scenarios

### Scenario A: 小さな機能追加

既存コードの一部へ小さな振る舞い追加を行う。`scope-request` 結果がなくても、変更対象、対象外、テスト戦略を整理する。

Requirements checklist:

1. [critical] 実装へ進む条件と停止条件を分ける
2. 変更対象と変更対象外を分ける
3. リスクと回避策を対で書く
4. 変更単位が小さく分けられている

### Scenario B: 依存追加の可能性がある変更

実装案はあるが、依存追加や仕様確認が必要かもしれない。承認前提の論点を止める。

Requirements checklist:

1. [critical] Ask first 条件を停止条件として出す
2. テスト戦略が推測ではなく確認方針として書かれる
3. 単体でレビュー可能な方針になっている

### Scenario C: 未知技術を含む設計

既存パターンにない技術やライブラリを使う可能性がある。実装方針だけでなく、理解すべき概念とトレードオフを整理する。

Requirements checklist:

1. [critical] 変更前に理解すべき概念が具体的に挙がる
2. 主なトレードオフが実装判断と対応している
3. ユーザーが説明すべき判断が残る

## Failure Ledger Seed

- `target and non-target blurred`
- `risk listed without mitigation`
- `design-changes only usable as implement-changes handoff`
- `tradeoff not explainable`
