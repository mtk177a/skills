---
name: review-changes
description: コード・文書・設定の新規差分、または明示的に依頼された effective diff の全面再レビューについて、正しさ、安全性、検証、互換性、保守性、性能上の比例的で実行可能な問題をレビューし、根拠、影響、リスク文脈、確信度、正規ラベルを報告するときに使う。特定済み指摘に対する通常の修正後再レビュー、既存指摘の整理、GitHub コメント案作成、差分要約、実装修正には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Review Changes（差分レビュー）

## 目的

- effective diff が導入または顕在化させる重要な問題を発見し、別の人や Skill がレビュー文脈を調べ直さずに評価できる根拠を返す。
- 求める対応、潜在影響、確信度、再レビュー状態を別の軸として扱う。
- 変更目的、対象の重要度と露出、修正のコストとリスクに応じて求める対応を調整し、数値スコアへ還元しない。
- コード、文書、設定を、全差分に同じチェックリストを強制せず、変更内容とリスクに応じた確認方法でレビューする。

## 対象範囲と根拠

レビュー前に effective diff を確定する。

1. 明示された diff、コミット範囲、PR 範囲があればそれを使う。
2. PR 文脈では、指定された base と head または実質的な PR diff を使う。
3. 対象未指定のローカルな「現在の変更」レビューでは、staged、unstaged、関連する untracked files を確認し、含めた範囲を明示する。
4. 複数の解釈でレビュー結果が実質的に変わる場合だけ確認する。diff を取得できない場合は、レビューを実行できなかったと報告する。

適用されるリポジトリ指示と、変更意図を理解するのに必要な周辺根拠を読む。
差分に応じて、仕様、テスト、呼び出し元、スキーマ、外部契約、sibling 実装、リポジトリ内の先例を確認する。根拠が差分外にあってもよいが、指摘はレビュー対象の変更が引き起こす、または変更に関係する問題でなければならない。無関係なリポジトリ全体監査へ広げない。

ユーザーが示した主張、コメント、外部仕様は結論ではなく検証対象の根拠として扱う。観測済み挙動、静的推論、前提、未知を区別する。

利用可能な場合は reviewer context を使う。目的と期待結果、プロダクトまたは運用文脈と重要度、scope と non-goals、影響する利用者・データ・契約・露出、制約と採用済み trade-off、verification と unknown、検知・復旧 control、review focus が対象になる。重要な evidence state は `Observed`、`Reported`、`Inferred`、`Unknown`、`Conflicting` のまま保持する。重要度または露出の不足は `Unknown` であり、低リスクの根拠ではない。

## 手順

1. effective diff、意図する挙動、reviewer context、レビュー範囲、重要な除外範囲を示す。目的、重要度、露出が判断に重要でも利用できない場合は、値を作らず unknown として保持する。
2. 行単位の詳細より先に、変更目的、設計、契約、責務境界、影響する consumer を確認する。変更のリスク面を特定し、全観点を機械的に適用せず、必要なレビュー観点を選ぶ。
3. 差分と、変更の前提・契約・統合点・提示された reviewer context を確認するために必要な最小限の周辺根拠を調べる。
4. 結果が指摘を実質的に強める、弱める、または反証できる場合、安全で関連する非変更型の確認を実行する。レビュー中に依存を導入したり、tracked file を変更したり、外部へ書き込んだりしない。
5. 実行した確認と結果を、提案だけの確認から分ける。利用不能または意図的に除外した確認は未実行として記録する。
6. 根拠で裏付けられた重要な指摘をすべて報告する。記載する impact は、提示済みまたは確認済みの contract、behavior、path が裏付ける結果に限定し、指摘を深刻に見せるためだけに、あり得そうな downstream mechanism を作らない。重要になり得る downstream の結果が有用でも未確認なら、条件付きで記述し、その依存関係を `Unconfirmed premises` に記録する。空の指摘一覧を避けるためだけに好み、`nit`、`note` を追加しない。
7. 求める対応を変え得る場合は、指摘の露出と前提、対象の重要度と blast radius、検知と復旧、修正コストまたは trade-off を整理する。捏造した数値スコアではなく、根拠のある順序比較を使い、支持されたリスクを十分に扱える最も低コストな対応を優先する。
8. 各指摘へ正規ラベルを 1 つ、確信度を 1 つ付ける。指摘、その記載済み impact、risk context、または求める対応が依存する前提や未知はすべて `Unconfirmed premises` に記録し、どの claim も依存しない場合だけ `none identified` とする。未確認前提によって求める対応が `question` でも、大きな潜在影響は保持する。
9. 明示的な全面再レビューでは、前回指摘を `Resolved` / `Remaining` / `New` に整理する。すべての `New` を `Fix-induced`、`Newly observable`、`Late-discovered` のいずれかへ分類する。3種類とも重要な問題は報告する。以前から観測可能だった `Late-discovered` が独立に non-blocking なら、新しい修正ラウンドを開始せず、actionable finding から除外するか、有用な場合だけ非actionableな `note` として要約する。
10. レビュー範囲、実行した確認、未確認範囲、残るリスクをまとめる。重要なレビュー観点が未完了なら、Approve や安全性を暗示せずレビュー未完了と示す。

## レビュー観点

変更に関係する観点だけを使う。

### コードと挙動

- 正しさ、境界値、順序、時刻、丸め、並行性、エラー処理、データ整合性
- API やスキーマなどの外部契約と内部実装上の制約
- 認可、認証、入力検証、インジェクション、秘密情報や個人情報の露出、危険な副作用
- 後方互換性、migration、rollout、呼び出し元や sibling 実装との整合
- テスト範囲と、実装依存・過剰な mock を含むテスト品質
- 個人の好みや推測的最適化ではなく、具体的影響がある保守性と性能
- 現在の requirement または観測済み risk で具体的な maintenance・operational cost を正当化できない abstraction、extension point、configuration surface、dependency、compatibility path、architecture layer
- 差分量を減らす一方で、確認済みの原因を残す、共有規則を重複させる、確立済みの責務 boundary を迂回する、既知の経路間で挙動を不整合にする、既知の追随修正を必要とする局所 patch

過剰な複雑性と狭すぎる修正は、規則の重複、挙動の不整合、到達不能な分岐、追加の運用負担、既知の追随変更など、具体的な結果を evidence が示す場合だけ指摘する。architecture 上の好みだけで報告しない。

### 文書

- 事実の正しさと、実装または正本との整合
- コマンド、例、リンク、識別子、用語、読者に見える欠落
- 利用可能な render、lint、決定的な内容検査

### 設定

- schema と parser の妥当性、precedence、既定値、環境との相互作用、互換性
- 静的な値が観測可能な挙動を変え、挙動確認が必要か
- rollout、復旧、秘密情報の扱い、運用上の影響

## 指摘契約

- `Label`
  - `must`: 重要なリスクが十分に支持され、それを十分に扱える低コストな対応がなく、マージ前の修正が必要
  - `should`: 原則修正推奨。代替案や制約を相談できる
  - `suggestion`: マージを止めない改善
  - `question`: 次の行動が前提や意図の確認
  - `nit`: 軽微で任意の修正
  - `note`: 対応不要の情報
- `Confidence`: `high` / `medium` / `low`
- `Finding`: 具体的な問題、提案、質問、補足
- `Evidence`: 根拠となる位置、契約、挙動、確認結果、リポジトリ内の先例
- `Impact`: 利用可能な evidence が裏付ける影響。明示した未確認 premise がある場合は、それが確認されたときに起きること。未確認の downstream mechanism を作らない
- `Exposure and preconditions`: 求める対応に重要な場合、evidence が裏付ける条件、到達可能な path、頻度、影響人口。重要でも利用できない場合は `Unknown`
- `Criticality and blast radius`: 求める対応に重要な場合、影響する product、tool、data、contract、operation の重要度と、裏付けられた影響範囲
- `Detectability, recovery, and workaround`: 求める対応に重要な場合、適用可能な検知、封じ込め、復旧、rollback、実用的な workaround の evidence
- `Remediation cost and trade-offs`: 求める対応に重要な場合、現在の evidence が裏付ける実装、verification、複雑性、regression、遅延、保守の重要な cost
- `Verification`: 確認、再現、反証の方法
- `Unconfirmed premises`: 指摘、その記載済み impact、または求める対応が依存する前提または未知。該当しない場合は `none identified` とし、未確認範囲・残る risk と照合し、根拠、影響、確認方法でこの field を代用しない
- `Re-review state`: 明示的な全面再レビューだけで `Resolved`、`Remaining`、`New`
- `New finding origin`: `New` finding だけで `Fix-induced`、`Newly observable`、`Late-discovered`
- `Generalizable check`: 今回の差分を超えて再利用できる学びがある場合だけ

`Must-fix`、`Should-fix`、`Nice-to-have` は互換入力として受け取り、`must`、`should`、`suggestion` または `nit` へ正規化する。好みだけの指摘に `must` や `should` を使わない。`question` でも潜在影響は大きくなり得るため、前提が未確認であることだけを理由に影響を消さない。

## 出力契約

レビュー状態に応じて構成を調整し、空の節は出力しない。

完了したレビューには次を含める。

- 結論と effective diff
- レビュー範囲と重要な除外範囲
- 求める対応と影響順に並べた指摘
- 実行したコマンドまたは確認方法と実際の結果
- 提案する確認、未確認範囲、残るリスク

重要な指摘がない場合は、そのことを明記し、レビュー範囲、実行した確認、未確認範囲、残るリスクも報告する。裸の `LGTM` を返したり、軽微なコメントを捏造したりしない。

diff を取得できない、または結果が実質的に異なる解釈を解消できない場合は、レビューを実行できなかったと示し、不足入力を特定する。「問題なし」として扱わない。

## 関連ワークフローとの境界

- 既存指摘を評価し、response decision と対応方針を決める場合は `triage-review-feedback` を使う。
- 一つ以上の特定済み指摘に対する通常の修正後再レビューには、既定で `validate-fix` を使う。
- finding assessment、state、response decision が明示済みの場合だけ `draft-review-comments` を使う。通常は `triage-review-feedback` がそれらを供給し、この review 出力だけでは actionable comment draft を許可しない。
- 問題発見を伴わない説明的な差分要約には `summarize-changes` を使う。

修正を実装したり、指摘の最終的な response decision を決めたりしない。未解決の仕様質問が差分の残りをレビューする妨げにならない場合、全体を止めず `question` として報告する。別エージェントやサブエージェントは既定で使わない。
