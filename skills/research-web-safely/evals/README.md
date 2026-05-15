# research-web-safely evals

`research-web-safely` の単体運用を評価するためのメモです。Web 調査が必要な状況で、出典の信頼度、不確実性、安全な再構成を単体で返せるかを見ます。

## Iter 0

- `description` と本文が「安全な Web 調査」に揃っているか
- 公式優先と複数ソース確認が分かれているか
- 出典の信頼度と不確実性が残るか
- 外部コードをそのまま提案しない前提が明確か

## Scenarios

### Scenario A: 公式ドキュメント中心の仕様確認

あるライブラリの最新仕様を調べ、公式ドキュメントを主根拠に提案する。

Requirements checklist:

1. [critical] 公式ソースを最優先として扱う
2. 根拠に Source type と信頼度がある
3. 結論と注意点が分かれている

### Scenario B: 公式情報が薄いベストプラクティス調査

公式情報だけでは足りず、GitHub や技術ブログも補助的に見る。不確実性を隠さない。

Requirements checklist:

1. [critical] 公式情報不足を明示する
2. 補助ソースを公式と同列に扱わない
3. 外部コードは再構成した安全な例として提示する

## Failure Ledger Seed

- `official source not prioritized`
- `confidence omitted`
- `external code copied verbatim`
