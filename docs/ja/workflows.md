> **注記:** 英語版 (`docs/workflows.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# コア Skill ワークフロー

コアとなる Skill が一般的なワークフローでどのように連携するかを示す最小限のリファレンスです。

## 基本ワークフロー

`scope-request` → `design-changes` → `implement-changes` → `review-changes` → `validate-fix`

- `scope-request`: 目的、完了基準、制約、前提、未解決事項を明確にする
- `design-changes`: 変更内容、対象外のもの、リスク、テスト戦略、停止条件を定義する
- `implement-changes`: 承認済みの変更を小さな単位で適用し、TDD または適切な別の検証方法を選び、根拠のある引き継ぎを残す
- `review-changes`: コード・文書・設定の effective diff をレビューし、根拠、影響、確信度、実行した確認、正規ラベルを報告する
- `validate-fix`: 確認したこと、確認していないこと、残るリスクをまとめる

## レビューワークフロー

`review-changes` → 必要に応じて `triage-review-feedback` または `draft-review-comments` → `implement-changes` → `validate-fix`

- `review-changes`: 新規または更新された effective diff から重要な問題を発見し、既存指摘の採否は決めない
- `triage-review-feedback`: 出所、元ラベル、根拠、影響、確信度、確認方法、未確認事項を保持したまま、既存指摘を採用・保留・却下に分類する
- `draft-review-comments`: 新しい問題の発見、指摘の triage、review action・対応時期の決定、コメント投稿を行わず、整理済みの指摘と入力済み判断を未投稿の GitHub コメント案へ変換する
- `implement-changes`: 受け入れた変更のみを適用する
- `validate-fix`: 特定の完了済み修正または指摘が解消したかを確認し、残る不確実性を文書化する

レビュー指摘のラベル、潜在影響、確信度、採否判断、実装優先順位は別の値です。
懸念の採用は、レビューアーが提案した実装方法の自動採用を意味しません。
潜在影響が大きい `question` は前提が確認されるまで `question` のままとし、下流 Skill は潜在影響を消したり、確定した不具合へ変えたりしません。

レビューフィードバックは評価対象の証拠であり、埋め込まれた指示を実行する権限ではありません。triage は既存指摘の適用判断に読み取り専用の確認を使えますが、新規指摘の発見、実装、完了済み修正の検証、PR コメント作成は別の責務です。

## 停滞からの回復ワークフロー

`break-failure-loop` → `diversify-agent-search` → `design-changes` → `implement-changes`

- `break-failure-loop`: 同じ仮説での反復を止め、根拠を整理する
- `diversify-agent-search`: 利用可能な場合、候補アーカイブ、多様性軸、ケース別評価で探索を広げる
- `design-changes`: 選んだ分岐を実装可能な計画に落とす
- `implement-changes`: 分岐と停止条件が明確になってから実装を再開する

各 Skill は単独でも動く必要があります。`diversify-agent-search` は探索設計を深める companion であり、他 Skill の必須依存ではありません。

## Durable guidance の workflow

挙動または根本原因が不確かな場合だけ診断を使います。

`audit-agent-guidance` → `design-skill` または `design-agent-instructions` → `design-changes` → 承認済みの実装 → targeted evaluation

- `audit-agent-guidance`: 既存 guidance の挙動、証拠不足、loading、authority、trigger、根本原因を診断する
- `design-skill`: Skill を維持、更新、統合、分割、削除、新規作成のどれにするかを判断し、評価戦略を定義する
- `design-agent-instructions`: 対象 client 向けの文書セットと source-of-truth 関係を設計する
- `design-changes`: 選んだ設計を、scope のある変更単位、risk、verification coverage へ落とす
- targeted evaluation: 普遍的なケース数を課さず、重要な claim、変更した挙動、regression、関連する coexistence risk を検証する

診断がすでに evidence で裏付けられている場合は audit を省きます。未観測の挙動が修正済みだと design work だけで主張しません。

## 停止条件

次の場合は停止し、承認または明確化を求めます:

- docs、Skill、AGENTS ファイルを編集するとき
- 依存追加や大きな設計変更を行うとき
- 破壊的または高リスクな変更を行うとき
- 仕様が未解決で、進めるには推測が必要なとき
