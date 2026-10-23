> この文書は [英語版 README.md](README.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# skills

[mtk177a](https://github.com/mtk177a) が作成・保守するエージェント向け Skill と、指定した Gist の無改変コピーを収録する個人用リポジトリ。

各 Skill は [Agent Skills 仕様](https://agentskills.io/specification) に従う。\
利用には、対象クライアントが Skill を読み込めることと、作業に必要な機能・権限が必要となる。\
導入前に [実行条件](docs/ja/compatibility.md) を確認する。

> **無保証:** 個人が可能な範囲で保守しているため、Skill は予告なく変更・削除する場合がある。自己責任で利用すること。

## 導入する

| 利用先 | 導入手順 |
| --- | --- |
| ChatGPT・Codex | [個人用 Plugin の導入・更新](docs/ja/distribution.md#chatgpt-と-codex) |
| Cursor | [ローカル Plugin の導入・更新](docs/ja/distribution.md#cursor) |
| Claude Code など APM の利用先 | [全体・選択・個別の導入](docs/ja/distribution.md#apm-で導入する) |

Plugin と単体・APM 導入は、同じ `skills/` の原本を使う。\
同じ環境では重複する Skill の導入方法を一つに揃える。

## Skill 一覧

以下の Skill を収録する。

| Skill | 説明 |
| --- | --- |
| `assess-risky-change-readiness` | 重大または復旧困難な変更について、安全対策、復旧方法、証拠、承認状況が実行判断に十分かを評価する |
| `audit-agent-guidance` | 継続的に適用するエージェント向け指示を、期待する挙動、観測済みの利用状況、クライアントの仕様、利用できる証拠に照らして監査する |
| `break-failure-loop` | 新しい証拠がないまま同じ仮説で同等の試行を繰り返す状況を止め、診断、進行不能の報告、別案の探索のいずれへ引き継ぐかを選ぶ |
| `calibrate-learning-support` | 作業を続けながら、その作業に関する理解、判断の主体性、検証可能性を保てるように AI による学習支援を調整する |
| `choose-ai-execution-setup` | 具体的な作業に使う AI の実行環境を、アクセス手段、モデル、推論、コンテキスト、権限、検証方法、エージェント構成の観点から提案する |
| `clarify-request` | 曖昧な依頼を、次の作業を始められるか、影響の小さい前提で進められるか、進行不能かを判断できるまで、段階的に明確化・構造化する |
| `cognitive-rhythm-writing` | 認知モードと未回収の緊張を管理し、日本語の説明文に緩急を設計する |
| `curate-repo-docs` | リポジトリで管理する文書を必要最小限かつ根拠に基づく内容に整え、適切な場所で管理し、検証する |
| `define-referents` | 曖昧な語を具体的な指示対象へ結び付け、命名上の制約を元の作業へ返す |
| `design-agent-instructions` | AGENTS.md / CLAUDE.md / copilot-instructions.md / GEMINI.md を設計する |
| `design-changes` | 実装前に変更方針・影響範囲・リスク・確認方針を設計する |
| `design-skill` | Skill を新規作成・統合・分割・大幅な責務変更のどれで設計するか、実装前に判断する |
| `draft-commit` | Git のステージング境界を保ちながら、変更単位ごとのコミット計画と Conventional Commits メッセージを作成する |
| `draft-issue` | 根拠と課題管理システムの確認状況を保ったまま、未投稿の Issue 案と投稿に必要な引き継ぎ情報を作る |
| `draft-review-comments` | 評価・状態・対応方針が決まった指摘、または結論・確認範囲・実施した確認・制約が示された指摘 0 件のレビューから、未投稿の PR コメント案を作る |
| `explore-decision-space` | 重要な意思決定が早期に収束する前に、問題の捉え方や解決案の選択肢を広げる |
| `implement-changes` | 承認済みの変更を小さな単位で、TDD または適切な別の検証方法を使って実装する |
| `investigate-failure` | 環境を問わず、原因不明のエラー、失敗するテスト、回帰、性能上の異常、予期しない技術的挙動を調査する |
| `japanese-tech-writing` | 日本語技術文書の論証構成・用語・推敲の規範を適用する |
| `make-it-click` | 読者の疑問に答えるため、必要な前提、情報の関係、条件、不確実性を示して説明文を作成・修正する |
| `record-session-handoff` | 後続の AI エージェントが状態を再検証し、安全に作業を再開できるよう、証拠に基づく引き継ぎを記録する |
| `research-web-safely` | 取得したコンテンツを命令として扱わず、追跡可能な Web 上の根拠を収集・評価する |
| `review-changes` | 新規差分または明示的に依頼された全面再レビューについて、リスクに見合った背景情報と所定のラベルを添えて問題点を報告する |
| `revise-docs-fresh-eyes` | 執筆時の会話を受け取らない Codex または Claude Code のサブエージェントに、既存文書を初見で読ませ、改稿を完結させる |
| `structure-what-you-write` | 読者と目的に合わせて情報を整理し、文章を作成・修正・レビューする |
| `summarize-changes` | 差分またはコミット範囲をレビューや文書化のために要約する |
| `triage-review-feedback` | 指摘の妥当性と現在の状態を、`Act now`・`Defer`・`No action` の対応方針とは分けて評価する |
| `validate-fix` | 特定済みの指摘に対する通常の修正後レビューを、適切な読み取り専用の証拠を使って限定的に行う |
| `write-natural-japanese` | 意味、確度、定着した用語を保ちながら、文脈に合う表現で日本語の文章を作成・推敲する |

`japanese-tech-writing` と `cognitive-rhythm-writing` は、元の Gist を改変せずに収録している。\
出典の版、ライセンス、同期の記録は各 Skill の `UPSTREAM.md` と [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載している。

## 保守する

| 作業 | 文書 |
| --- | --- |
| 変更を検証し、Issue・コミット・PR にまとめる | [変更の進め方](CONTRIBUTING-ja.md) |
| Skill を作成する | [作成ガイド](docs/ja/authoring.md) |
| 作業に使う Skill を選ぶ | [ワークフロー](docs/ja/workflows.md) |
| 配布用 ZIP を作る | [アーカイブの生成・検証](docs/ja/distribution.md#アーカイブを生成検証する) |
| 外部資料や実行機能の安全性を確認する | [セキュリティレビュー](docs/ja/security.md) |
| 日本語参考訳を更新する | [言語方針](docs/ja/localization.md) |

外部からの貢献は通常想定していない。

## ライセンス

独自作成したコードとコンテンツには [MIT License](LICENSE) を適用する。\
第三者の著作物には、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載した個別の条件を適用する。

Copyright (c) 2026 mtk177a
