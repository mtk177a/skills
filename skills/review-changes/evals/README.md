# review-changes evals

`review-changes` の単体運用を評価するためのメモです。`triage-review-feedback` 前提ではなく、この Skill 単独で採否判断の材料になるレビュー結果を返せるかを見ます。

## Iter 0

- `description` と本文が「新規レビュー」に揃っているか
- `must` / `should` / `suggestion` / `question` / `nit` / `note` の正規ラベルが指摘ごとに付くか
- ラベルを付ける基準が明確か
- `Must-fix` / `Should-fix` / `Nice-to-have` を互換入力として受け取り、正規ラベルへ寄せられるか
- 各指摘に根拠があるか
- 各指摘に、なぜ問題か、どう見抜くかがあるか
- 単体で次の判断に進める情報量があるか

## Scenarios

### Scenario A: 小さな差分の新規レビュー

差分と関連仕様があり、`must` と `should` が混在する。採否判断自体は行わず、判断材料を返す。

要件チェックリスト:

1. [critical] 指摘ごとに具体的な根拠がある
2. 指摘ごとに正規ラベルが 1 つ付いている
3. `must` と `should` の基準が本文の定義と合っている
4. テスト手順か確認観点がある

### Scenario B: 仕様未確定を含むレビュー

差分の一部は仕様依存で断定できない。無理に `must` 化せず、`question` として残す。

要件チェックリスト:

1. [critical] 推測だけで重大指摘を作らない
2. 未確定仕様を `question` として分離する
3. 単体で triage に回せる情報がある

### Scenario C: API 契約と内部制約の切り分け

OpenAPI では non-nullable だが、内部保存先のカラムは nullable なケースを含む。DB 都合に引きずられず、外部契約違反として整理できるかを見る。

要件チェックリスト:

1. [critical] API やスキーマなどの外部契約を起点に指摘できる
2. DB nullable かどうかを別論点として切り分ける
3. 契約違反と実装都合を混ぜずに説明できる
4. 契約違反が明確なら `must` として分類できる

### Scenario D: 単数フィールド化と既存 cardinality の整合

relation table と複数件前提の sibling endpoint / 更新 SQL が既にある領域で、新しい差分だけが単数フィールドや 1 件取得に倒れているケースを含む。周辺実装を横断して cardinality 前提の崩れを指摘できるかを見る。

要件チェックリスト:

1. [critical] relation や sibling endpoint を見て既存 cardinality を確認できる
2. 単数化が後方互換や周辺 API 整合に与える影響を説明できる
3. 単一のコード片だけで完結した推測にしない

### Scenario E: 一貫性コメントの根拠を repo 内の先例で固める

不具合断定まではできないが、同じ責務の handler / wrapper / type と比べると、この差分だけ timezone や変換方針がずれているケースを含む。repo 内の先例を根拠に一貫性コメントの強さを決められるかを見る。

要件チェックリスト:

1. [critical] 同じ責務の実装を横断して repo 内の先例を根拠にできる
2. 先例が弱い場合は、断定しすぎず強さを落とせる
3. 単なる好みではなく、一貫性の差分として説明できる
4. 修正推奨なら `should`、任意改善なら `suggestion` として分類できる

### Scenario F: 学習に使えるレビュー指摘

差分レビューで問題を見つけたが、指摘だけでは次に同じ問題を見抜けない。なぜ問題か、どう見抜くかを丁寧に添える。

要件チェックリスト:

1. [critical] 各指摘の中に、根拠、なぜ問題か、どう見抜くか、確認観点が対応して残る
2. なぜ問題かが、仕様、事故リスク、保守性、テスト不足などの観点と接続されている
3. どう見抜くかが、今回の差分以外にも使える確認観点になっている
4. 指摘の採否は最終決定せず、判断材料として残す

### Scenario G: 軽微な提案と参考情報の分離

差分には命名の軽微な揺れ、任意の読みやすさ改善、将来注意の補足が含まれる。マージを止めない論点を強く分類しすぎないかを見る。

要件チェックリスト:

1. [critical] 軽微な命名や表記の指摘を `must` / `should` にしない
2. 任意の改善提案を `suggestion` として分類できる
3. 細かい指摘を `nit` として分類できる
4. 対応不要の背景共有を `note` として分類できる

### Scenario H: 旧ラベル入力の正規化

既存メモから `Must-fix` / `Should-fix` / `Nice-to-have` を受け取り、`review-changes` の通常出力として正規ラベルへ寄せる。

要件チェックリスト:

1. [critical] `Must-fix` / `Should-fix` / `Nice-to-have` を通常出力の主見出しにしない
2. `Must-fix` を `must` に寄せられる
3. `Should-fix` を `should` に寄せられる
4. `Nice-to-have` を内容に応じて `suggestion` または `nit` に寄せられる

### Scenario I: 再レビューの状態整理

前回指摘と今回差分があり、修正済み、未対応、新規発見が混在する。状態とラベルを混同せず、再レビュー結果として整理する。

要件チェックリスト:

1. [critical] 状態表記を `Resolved` / `Remaining` / `New` に統一する
2. 状態と正規ラベルを別軸で扱える
3. `Remaining` の `must` が残る場合、採否判断に使える根拠がある

## Failure Ledger Seed

- `findings lack evidence`
- `severity mixed with decision`
- `review only meaningful inside triage flow`
- `review not reusable for learning`
- `learning note detached from finding`
- `legacy labels used as primary output`
- `uncertain premise classified as must`
- `non-blocking suggestion escalated to should or must`
- `status mixed with label`
