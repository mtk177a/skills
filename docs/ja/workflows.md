> **注記:** 英語版 (`docs/workflows.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# コア Skill ワークフロー

コアとなる Skill が一般的なワークフローでどのように連携するかを示す最小限のリファレンスです。

## 基本ワークフロー

`scope-request` → `design-changes` → `implement-changes` → `review-changes` → `validate-fix`

- `scope-request`: 目的、完了基準、制約、前提、未解決事項を明確にする
- `design-changes`: 変更内容、対象外のもの、リスク、テスト戦略、停止条件を定義する
- `implement-changes`: TDD で段階的に構築し、検証のための明確な引き継ぎを残す
- `review-changes`: 差分をレビューし、発見事項を `must` / `should` / `suggestion` / `nit` に分類する
- `validate-fix`: 確認したこと、確認していないこと、残るリスクをまとめる

## レビューフィードバックワークフロー

`triage-review-feedback` → `implement-changes` → `validate-fix`

- `triage-review-feedback`: 既存のレビューコメントを受け入れ・延期・却下に分類し、方針を決める
- `implement-changes`: 受け入れた変更のみを適用する
- `validate-fix`: 検証結果と残る未解決事項を文書化する

## 停滞からの回復ワークフロー

`break-failure-loop` → `diversify-agent-search` → `design-changes` → `implement-changes`

- `break-failure-loop`: 同じ仮説での反復を止め、根拠を整理する
- `diversify-agent-search`: 利用可能な場合、候補アーカイブ、多様性軸、ケース別評価で探索を広げる
- `design-changes`: 選んだ分岐を実装可能な計画に落とす
- `implement-changes`: 分岐と停止条件が明確になってから実装を再開する

各 Skill は単独でも動く必要があります。`diversify-agent-search` は探索設計を深める companion であり、他 Skill の必須依存ではありません。

## 停止条件

次の場合は停止し、承認または明確化を求めます:

- docs、Skill、AGENTS ファイルを編集するとき
- 依存追加や大きな設計変更を行うとき
- 破壊的または高リスクな変更を行うとき
- 仕様が未解決で、進めるには推測が必要なとき
