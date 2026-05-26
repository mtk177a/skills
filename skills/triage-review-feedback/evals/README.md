# triage-review-feedback evals

`triage-review-feedback` の単体運用を評価するためのメモです。外部レビューや `review-changes` 結果を受け取り、この Skill 単独で採否と対応方針を決められるかを見ます。

## Iter 0

- `description` と本文が「採否判断」に揃っているか
- 採用、保留、却下の区別が明確か
- 採用時の優先順位と対応方針があるか
- 単体で実装着手または保留判断へ進めるか

## Scenarios

### Scenario A: 通常のレビュー指摘整理

2-3 件のレビュー指摘を受け取り、採用、保留、却下を整理する。

Requirements checklist:

1. [critical] 各指摘に採否理由がある
2. 採用した指摘に優先順位がある
3. 対応方針が実装可能な粒度で書かれる

### Scenario B: 仕様論点を含むレビュー

一部の指摘は仕様判断が必要で、即採用できない。保留と追加確認を明示する。

Requirements checklist:

1. [critical] 仕様判断が必要な指摘を自動採用しない
2. 保留理由と確認事項がある
3. 単体で次の判断者へ渡せる

### Scenario C: AI 指摘の外部仕様依存を裏取りする

AI レビューが GitHub Actions などのプラットフォーム構文や外部仕様の誤りを断定しているが、入力には公式根拠がない。未検証のまま採用せず、確認か却下に落とせるかを見る。

Requirements checklist:

1. [critical] 公式ドキュメントや一次情報なしに自動採用しない
2. 採否判断と、必要な確認アクションが分かれている
3. 根拠が得られない段階では保留、公式根拠で誤りと分かれば却下にできる

## Failure Ledger Seed

- `decision without rationale`
- `accepted item lacks actionable plan`
- `triage depends on prior flow-specific labels`
