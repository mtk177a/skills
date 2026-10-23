> この文書は [英語版 README.md](README.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# skills

[mtk177a](https://github.com/mtk177a) が作成・保守するエージェント向け Skill と、指定した Gist の無改変コピーを収録する個人用リポジトリ。

各 Skill は [Agent Skills 仕様](https://agentskills.io/specification) に従う。\
利用には、対象クライアントが Skill を読み込めることと、作業に必要な機能・権限が必要となる。\
導入前に [実行条件](docs/ja/users/compatibility.md) を確認する。

> **無保証:** 個人が可能な範囲で保守しているため、Skill は予告なく変更・削除する場合がある。自己責任で利用すること。

## 導入する

| 利用先 | 導入手順 |
| --- | --- |
| ChatGPT・Codex | [個人用 Plugin の導入・更新](docs/ja/users/installation.md#chatgpt-と-codex-で使う) |
| Cursor | [ローカル Plugin の導入・更新](docs/ja/users/installation.md#cursor-で使う) |
| Claude Code など APM の利用先 | [全体・選択・個別の導入](docs/ja/users/installation.md#apm-でインストールする) |

Plugin と単体・APM 導入は、同じ `skills/` の原本を使う。\
同じ環境では重複する Skill の導入方法を一つに揃える。

## Skill 一覧

目的に合う Skill を選び、リンク先で使用条件を確認する。\
複数の Skill を使う順序や引き継ぎは [ワークフロー](docs/ja/users/workflows.md) を参照する。

### 依頼・方針を整理する

| したいこと | Skill |
| --- | --- |
| 曖昧な依頼の目的・範囲を整理する | [`clarify-request`](skills/clarify-request/SKILL-ja.md) |
| 曖昧な用語が何を指すか定める | [`define-referents`](skills/define-referents/SKILL-ja.md) |
| 問題の捉え方や解決案を広げて比較する | [`explore-decision-space`](skills/explore-decision-space/SKILL-ja.md) |
| 作業に合う AI の実行環境を選ぶ | [`choose-ai-execution-setup`](skills/choose-ai-execution-setup/SKILL-ja.md) |
| AI を使いながら理解と判断の主体性を保つ | [`calibrate-learning-support`](skills/calibrate-learning-support/SKILL-ja.md) |

### 設計・実装・原因調査を進める

| したいこと | Skill |
| --- | --- |
| 実装前に変更範囲・リスク・検証方法を決める | [`design-changes`](skills/design-changes/SKILL-ja.md) |
| 許可された変更を実装・検証する | [`implement-changes`](skills/implement-changes/SKILL-ja.md) |
| 予期しない挙動や失敗の原因を調べる | [`investigate-failure`](skills/investigate-failure/SKILL-ja.md) |
| 重大な操作の前に安全対策・復旧方法・承認状況を確認する | [`assess-risky-change-readiness`](skills/assess-risky-change-readiness/SKILL-ja.md) |
| 成果のない試行の繰り返しを止め、次の確認を選ぶ | [`break-failure-loop`](skills/break-failure-loop/SKILL-ja.md) |

### レビュー・変更の記録・引き継ぎを行う

| したいこと | Skill |
| --- | --- |
| 新しい差分、または明示的に依頼された差分全体をレビューする | [`review-changes`](skills/review-changes/SKILL-ja.md) |
| レビュー指摘の妥当性と対応方針を分けて判断する | [`triage-review-feedback`](skills/triage-review-feedback/SKILL-ja.md) |
| 特定済みの修正を元の指摘に照らして確認する | [`validate-fix`](skills/validate-fix/SKILL-ja.md) |
| 判断済みのレビュー結果からコメントを下書きする | [`draft-review-comments`](skills/draft-review-comments/SKILL-ja.md) |
| 未投稿の Issue 案を作る | [`draft-issue`](skills/draft-issue/SKILL-ja.md) |
| コミットの分け方とメッセージを作る | [`draft-commit`](skills/draft-commit/SKILL-ja.md) |
| 差分やコミット範囲を読み手に合わせて要約する | [`summarize-changes`](skills/summarize-changes/SKILL-ja.md) |
| 別セッションで作業を再開できるように記録する | [`record-session-handoff`](skills/record-session-handoff/SKILL-ja.md) |

### 調査・執筆・推敲を行う

| したいこと | Skill |
| --- | --- |
| 出典を確認できる形で Web 調査を行う | [`research-web-safely`](skills/research-web-safely/SKILL-ja.md) |
| 読者と目的に合わせて情報を選び、構成する | [`structure-what-you-write`](skills/structure-what-you-write/SKILL-ja.md) |
| 読者の疑問に、必要な前提と理由をつないで答える | [`make-it-click`](skills/make-it-click/SKILL-ja.md) |
| 意味を保ちながら自然な日本語に整える | [`write-natural-japanese`](skills/write-natural-japanese/SKILL.md) |
| 日本語技術文書の論証・用語・推敲の規範を適用する | [`japanese-tech-writing`](skills/japanese-tech-writing/SKILL.md) |
| 日本語の説明文に緩急を設計する | [`cognitive-rhythm-writing`](skills/cognitive-rhythm-writing/SKILL.md) |
| 許可された独立サブエージェントに初見で改稿させる | [`revise-docs-fresh-eyes`](skills/revise-docs-fresh-eyes/SKILL-ja.md) |

### Skill・エージェント向け指示を整える

| したいこと | Skill |
| --- | --- |
| エージェント向け指示と挙動のずれを調べる | [`audit-agent-guidance`](skills/audit-agent-guidance/SKILL-ja.md) |
| Skill の責務・使用条件・境界を設計する | [`design-skill`](skills/design-skill/SKILL-ja.md) |
| 指示文書の役割とクライアントの読み込み関係を設計する | [`design-agent-instructions`](skills/design-agent-instructions/SKILL-ja.md) |

`japanese-tech-writing` と `cognitive-rhythm-writing` は、元の Gist を改変せずに収録している。\
出典の版、ライセンス、同期の記録は各 Skill の `UPSTREAM.md` と [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載している。

## 保守する

| 作業 | 文書 |
| --- | --- |
| 変更を検証し、Issue・コミット・PR にまとめる | [変更の進め方](CONTRIBUTING-ja.md) |
| Skill を作成する | [作成ガイド](docs/ja/maintainers/authoring.md) |
| Plugin の ZIP を作る | [Plugin の ZIP を作る](docs/ja/maintainers/packaging.md) |
| 外部資料や実行機能の安全性を確認する | [セキュリティレビュー](docs/ja/maintainers/security.md) |
| 日本語参考訳を更新する | [言語方針](docs/ja/maintainers/localization.md) |

外部からの貢献は通常想定していない。

## ライセンス

独自作成したコードとコンテンツには [MIT License](LICENSE) を適用する。\
第三者の著作物には、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載した個別の条件を適用する。

Copyright (c) 2026 mtk177a
