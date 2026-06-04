# calibrate-ai-learning evals

`calibrate-ai-learning` の単体運用を評価するためのメモです。AI に丸投げせず、理解確認、委任範囲、根拠、未確認事項が残るかを見ます。

## Iter 0

- `description` と本文が「AI への委任深度調整と理解保護」に揃っているか
- 現在の理解、理解すべき概念、委任範囲、自分で判断すべき作業が分かれているか
- 答えの丸出しではなく、ヒント、考え方、実装例の順で支援する境界があるか
- 高リスク領域で、公式情報、既存実装、テスト結果による検証が残るか

## Scenarios

### Scenario A: 未知ライブラリの実装相談

初めて使うライブラリで機能実装をしたい。すぐコードを書くのではなく、理解すべき概念、AI に任せる調査、ユーザーが判断する採用可否を分ける。

Requirements checklist:

1. [critical] 即実装ではなく、理解すべき概念と委任範囲を先に出す
2. AI への依頼文が目的、制約、確認観点を含む
3. 検証に使う根拠が公式情報、既存実装、テスト結果のいずれかに結び付く
4. 確認問題が今回の作業内容に対応している

### Scenario B: AI レビュー指摘の採否相談

AI からレビュー指摘を受けたが、正しいか判断できない。採否理由、根拠、見抜き方を整理する。

Requirements checklist:

1. [critical] AI 指摘を未検証入力として扱う
2. 自分で判断すべき作業として採否理由の確認が残る
3. 次回の自力課題が、同種の指摘を見抜く練習になっている

### Scenario C: 修正後確認の説明準備

テストは通ったが、変更理由や未確認事項を説明できるか不安がある。説明ポイントと残る確認事項を整理する。

Requirements checklist:

1. [critical] テスト結果だけで完了扱いにしない
2. 現在の理解と未確認事項を分ける
3. ユーザーが説明すべき判断と検証根拠が対応している

## Failure Ledger Seed

- `answer dumped before calibration`
- `delegation scope unclear`
- `ai output treated as verified`
- `no self-check question`
