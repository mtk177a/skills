# Core Skills Empirical Review

このディレクトリは、外部 skill `empirical-prompt-tuning` を使って `intake`, `design`, `build`, `code-review`, `triage-review`, `validate-fix` を empirical に見直すための補助資料です。

ここでいう `empirical-prompt-tuning` は、この repo の local skill ではなく、[mizchi/skills](https://github.com/mizchi/skills) にある外部 skill `empirical-prompt-tuning` を指します。つまり、ここにあるファイルはこの repo の skill 本体ではなく、`mizchi/skills` 側の `empirical-prompt-tuning` を使って自作 skill 群を評価するためのローカル運用メモです。

このディレクトリには、skill 単体ではなく複数 skill をまたぐフロー評価の資産を置きます。

- `intake-design-build.md`: 依頼整理から設計、実装方針までの評価計画
- `code-review-triage-validate.md`: レビュー、採否判断、修正確認までの評価計画
- `subagent-prompt-template.md`: blank-slate executor に渡す共通プロンプト雛形

## 使い方

1. まず各 flow ドキュメントの Iter 0 を読み、`description` と本文のズレ、受け渡し不足を静的に確認する。
2. flow ごとの scenario と requirements checklist を固定する。
3. `subagent-prompt-template.md` を土台に fresh subagent を起動し、各 scenario を実行させる。
4. Success / Accuracy / `tool_uses` / `duration_ms` / retries / unclear points を記録する。
5. 修正は 1 テーマずつに絞り、再評価する。

## 補足

- ここでいう empirical review は、session 内で blank-slate subagent を使って回す軽量評価を前提とする。
- 手順や判断基準の原典は mizchi 側の `empirical-prompt-tuning` skill にあり、このディレクトリはその適用先をこの repo の core skills 向けに具体化したもの。
- `waxa` は eval シナリオや ledger を YAML 化して継続運用するための CLI で、初回の論点抽出が終わってから導入を検討する。
