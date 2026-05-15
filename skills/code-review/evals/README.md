# code-review evals

`code-review` の単体運用を評価するためのメモです。`triage-review` 前提ではなく、この Skill 単独で採否判断の材料になるレビュー結果を返せるかを見ます。

## Iter 0

- `description` と本文が「新規レビュー」に揃っているか
- Must-fix / Should-fix / Nice-to-have の分離が明確か
- 各指摘に根拠があるか
- 単体で次の判断に進める情報量があるか

## Scenarios

### Scenario A: 小さな差分の新規レビュー

差分と関連仕様があり、Must-fix と Should-fix が混在する。採否判断自体は行わず、判断材料を返す。

Requirements checklist:

1. [critical] 指摘ごとに具体的な根拠がある
2. Must-fix / Should-fix / Nice-to-have が分かれている
3. テスト手順か確認観点がある

### Scenario B: 仕様未確定を含むレビュー

差分の一部は仕様依存で断定できない。無理に Must-fix 化せず、確認事項として残す。

Requirements checklist:

1. [critical] 推測だけで重大指摘を作らない
2. 未確定仕様を確認事項として分離する
3. 単体で triage に回せる情報がある

## Failure Ledger Seed

- `findings lack evidence`
- `severity mixed with decision`
- `review only meaningful inside triage flow`
