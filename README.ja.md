> この文書は [英語版 README.md](README.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# skills

[mtk177a](https://github.com/mtk177a) が作成または保守しているエージェント向けの Skill と、指定した 2 つの Gist の無改変コピーをまとめた、個人用のリポジトリである。

各 Skill は [Agent Skills 仕様](https://agentskills.io/specification) に従っている。\
Skill が動くかどうかは、クライアントと、エージェントがアクセスできるものや許可されていることにも左右される。\
インストールする前に [実行条件](docs/ja/users/compatibility.md) を確認する。

> **無保証:** このリポジトリは、個人が可能な範囲で保守している。\
> Skill は、予告なく変更または削除することがある。\
> 利用は自己責任で行うこと。

## インストールする

インストール方法は 2 つあり、どちらも `skills/` にある同じ Skill をインストールする。

- **Plugin の ZIP**: ChatGPT で使える唯一の方法である。\
  ChatGPT にアップロードした Plugin は、Codex でも使える。
- **APM**: Claude Code、Codex、Cursor など、APM が対応しているクライアントで使う。

方法の選び方とインストールの手順は、[Skill のインストールと更新](docs/ja/users/installation.md#インストール方法を選ぶ) を参照する。

## Skill 一覧

作業に合う Skill を選ぶ。\
そのうえで、リンク先の Skill で、使う場面と、その Skill が出すものを確認する。\
一つの作業で複数の Skill を使う場合は、[次に使う Skill を選ぶ](docs/ja/users/workflows.md) を参照する。

### 依頼を明確にし、方針を選ぶ

| したいこと | Skill |
| --- | --- |
| 曖昧な依頼を明確にする | [`clarify-request`](skills/clarify-request/SKILL-ja.md) |
| 曖昧な用語が何を指すかを定める | [`define-referents`](skills/define-referents/SKILL-ja.md) |
| 問題の捉え方と解決案を広げて比較する | [`explore-decision-space`](skills/explore-decision-space/SKILL-ja.md) |
| 作業に合う AI の実行環境を選ぶ | [`choose-ai-execution-setup`](skills/choose-ai-execution-setup/SKILL-ja.md) |
| AI を使いながら、作業内容への理解と判断の主体性を保つ | [`calibrate-learning-support`](skills/calibrate-learning-support/SKILL-ja.md) |

### 設計し、実装し、原因を調べる

| したいこと | Skill |
| --- | --- |
| 実装の前に、範囲、リスク、検証方法を決める | [`design-changes`](skills/design-changes/SKILL-ja.md) |
| 許可された変更を実装し、検証する | [`implement-changes`](skills/implement-changes/SKILL-ja.md) |
| 予期しない挙動や失敗の原因を調べる | [`investigate-failure`](skills/investigate-failure/SKILL-ja.md) |
| 重大な操作の前に、安全対策、復旧方法、実行の許可を確かめる | [`assess-risky-change-readiness`](skills/assess-risky-change-readiness/SKILL-ja.md) |
| 失敗した試行の繰り返しを止め、次の確認を選ぶ | [`break-failure-loop`](skills/break-failure-loop/SKILL-ja.md) |

### 変更をレビューし、伝える

| したいこと | Skill |
| --- | --- |
| 新しい差分のレビューや、明示的に求められた差分全体の再レビューを行う | [`review-changes`](skills/review-changes/SKILL-ja.md) |
| 指摘を評価し、対応方針を決める | [`triage-review-feedback`](skills/triage-review-feedback/SKILL-ja.md) |
| 特定済みの修正を、元の指摘に照らして確かめる | [`validate-fix`](skills/validate-fix/SKILL-ja.md) |
| 判断済みのレビュー結果から、PR のコメントを下書きする | [`draft-review-comments`](skills/draft-review-comments/SKILL-ja.md) |
| Issue を投稿せずに下書きする | [`draft-issue`](skills/draft-issue/SKILL-ja.md) |
| コミットの分け方を決め、メッセージを下書きする | [`draft-commit`](skills/draft-commit/SKILL-ja.md) |
| 差分やコミット範囲を、読む人に合わせて要約する | [`summarize-changes`](skills/summarize-changes/SKILL-ja.md) |
| 別のセッションで作業を再開できるように、証拠とともに状態を記録する | [`record-session-handoff`](skills/record-session-handoff/SKILL-ja.md) |

### 調べて書く

| したいこと | Skill |
| --- | --- |
| 出典をたどれる形で Web を調べる | [`research-web-safely`](skills/research-web-safely/SKILL-ja.md) |
| 読む人に合わせて情報を選び、構成する | [`structure-what-you-write`](skills/structure-what-you-write/SKILL-ja.md) |
| 答えと、それを理解するのに必要な理由を説明する | [`make-it-click`](skills/make-it-click/SKILL-ja.md) |
| 意味を変えずに、自然な日本語で書き、推敲する | [`write-natural-japanese`](skills/write-natural-japanese/SKILL.md) |
| 日本語の技術文書の規範を適用する | [`japanese-tech-writing`](skills/japanese-tech-writing/SKILL.md) |
| 日本語の説明文に緩急を設計する | [`cognitive-rhythm-writing`](skills/cognitive-rhythm-writing/SKILL.md) |
| 許可された独立したサブエージェントに、文書を改稿させる | [`revise-docs-fresh-eyes`](skills/revise-docs-fresh-eyes/SKILL-ja.md) |

### Skill とエージェント向けの指示を保守する

| したいこと | Skill |
| --- | --- |
| エージェント向けの指示と実際の挙動のずれを診断する | [`audit-agent-guidance`](skills/audit-agent-guidance/SKILL-ja.md) |
| Skill の責務と範囲を設計する | [`design-skill`](skills/design-skill/SKILL-ja.md) |
| 指示ファイルの役割と、クライアントによる読み込み方を設計する | [`design-agent-instructions`](skills/design-agent-instructions/SKILL-ja.md) |

`japanese-tech-writing` と `cognitive-rhythm-writing` は、上流の Gist を改変せずにコピーしたものである。\
元の版、ライセンス、同期の記録は、各 Skill の `UPSTREAM.md` と [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) にある。

## 保守する

| 作業 | ガイド |
| --- | --- |
| 変更を検証し、Issue、コミット、PR を用意する | [変更の進め方](CONTRIBUTING-ja.md) |
| Skill を作る | [Skill 作成ガイド](docs/ja/maintainers/authoring.md) |
| Plugin の ZIP を作る | [Plugin の ZIP を作る](docs/ja/maintainers/packaging.md) |
| 第三者の資料と実行機能をレビューする | [Skill のセキュリティレビュー](docs/ja/maintainers/security.md) |
| 言語を選び、日本語参考訳を保守する | [言語と日本語参考訳](docs/ja/maintainers/localization.md) |
| このリポジトリの概念を指す用語を確認する | [用語集](docs/ja/maintainers/glossary.md) |

外部からの貢献は、通常は想定していない。

## ライセンス

独自に作成したコードと内容には、[MIT License](LICENSE) を適用する。\
第三者の資料には、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載した条件が引き続き適用される。

Copyright (c) 2026 mtk177a
