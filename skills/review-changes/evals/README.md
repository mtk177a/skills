# review-changes evals

`review-changes` の単体運用を評価するためのメモです。`triage-review-feedback` 前提ではなく、この Skill 単独で採否判断の材料になるレビュー結果を返せるかを見ます。

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

### Scenario C: API 契約と内部制約の切り分け

OpenAPI では non-nullable だが、内部保存先のカラムは nullable なケースを含む。DB 都合に引きずられず、外部契約違反として整理できるかを見る。

Requirements checklist:

1. [critical] API やスキーマなどの外部契約を起点に指摘できる
2. DB nullable かどうかを別論点として切り分ける
3. 契約違反と実装都合を混ぜずに説明できる

### Scenario D: 単数フィールド化と既存 cardinality の整合

relation table と複数件前提の sibling endpoint / 更新 SQL が既にある領域で、新しい差分だけが単数フィールドや 1 件取得に倒れているケースを含む。周辺実装を横断して cardinality 前提の崩れを指摘できるかを見る。

Requirements checklist:

1. [critical] relation や sibling endpoint を見て既存 cardinality を確認できる
2. 単数化が後方互換や周辺 API 整合に与える影響を説明できる
3. 単一のコード片だけで完結した推測にしない

### Scenario E: 一貫性コメントの根拠を repo 内の先例で固める

不具合断定まではできないが、同じ責務の handler / wrapper / type と比べると、この差分だけ timezone や変換方針がずれているケースを含む。repo 内の先例を根拠に一貫性コメントの強さを決められるかを見る。

Requirements checklist:

1. [critical] 同じ責務の実装を横断して repo 内の先例を根拠にできる
2. 先例が弱い場合は、断定しすぎず強さを落とせる
3. 単なる好みではなく、一貫性の差分として説明できる

## Failure Ledger Seed

- `findings lack evidence`
- `severity mixed with decision`
- `review only meaningful inside triage flow`
