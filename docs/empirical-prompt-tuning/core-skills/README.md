# Core Skills Empirical Review

このディレクトリは、外部 Skill `empirical-prompt-tuning` を使って `scope-request`, `design-changes`, `implement-changes`, `review-changes`, `triage-review-feedback`, `validate-fix` を empirical に見直すための補助資料です。

ここでいう `empirical-prompt-tuning` は、このリポジトリの local Skill ではなく、[mizchi/skills](https://github.com/mizchi/skills) にある外部 Skill `empirical-prompt-tuning` を指します。つまり、ここにあるファイルはこのリポジトリの Skill 本体ではなく、`mizchi/skills` 側の `empirical-prompt-tuning` を使って自作 Skill 群を評価するためのローカル運用メモです。

このディレクトリには、Skill 単体ではなく複数 Skill をまたぐ統合評価の資産を置きます。

通常の中核 Skill の並べ方は [core-skill-flows.md](../../core-skill-flows.md) を参照します。

- `scope-design-implement.md`: 依頼整理から設計、実装方針までの統合回帰評価計画
- `review-triage-validate.md`: レビュー、採否判断、修正確認までの統合回帰評価計画
- `subagent-prompt-template.md`: blank-slate executor に渡す共通プロンプト雛形

## 使い方

1. まず対象 Skill の単体 eval を先に回し、個別の改善論点を切り分ける。
2. そのうえで各 flow ドキュメントの Iter 0 を読み、受け渡し不足や統合時の崩れを静的に確認する。
3. flow ごとの scenario と requirements checklist を固定する。
4. `subagent-prompt-template.md` を土台に先入観のないサブエージェントを起動し、各 scenario を実行させる。
5. Success / Accuracy / `tool_uses` / `duration_ms` / retries / unclear points を記録する。
6. 大きな修正や複数 Skill にまたがる修正のあとに再評価する。

## 補足

- ここでいう empirical review は、session 内で先入観のないサブエージェントを使って回す軽量な統合回帰評価を前提とする。
- 手順や判断基準の原典は mizchi 側の `empirical-prompt-tuning` Skill にあり、このディレクトリはその適用先をこのリポジトリの core skills 向けに具体化したもの。
- `waxa` は eval シナリオや ledger を YAML 化して継続運用するための CLI で、初回の論点抽出が終わってから導入を検討する。
