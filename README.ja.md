> **注記:** 英語版 (`README.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# skills

[mtk177a](https://github.com/mtk177a) が作成・保守する個人用エージェント Skill リポジトリです。

各 Skill は [Agent Skills 仕様](https://agentskills.io/specification) に準拠しており、Codex、Claude Code、GitHub Copilot、Gemini CLI などの対応クライアントで利用できます。

> **無保証。** このリポジトリは個人が手の空いたときに保守するものです。Skill は予告なく変更・削除される場合があります。自己責任でご利用ください。

## Skill 一覧

開発作業全般をカバーする 27 の Skill を収録しています。

| Skill | 説明 |
|-------|------|
| `audit-agent-rules` | AGENTS.md / Skills / docs の命名・境界・承認ルール・既定の重さを監査する |
| `break-failure-loop` | 同じエラーや方針で 2 回以上失敗したときに立ち止まり再構成する |
| `calibrate-ai-learning` | 委任が深くなりすぎている時や、理解を保ちながら作業したい時に使う |
| `clarify-request` | 依頼が曖昧なときに 1〜4 個の確認質問をするか前提を明示して進む |
| `cognitive-rhythm-writing` | 認知モードと未回収の緊張を管理し、日本語の説明文に緩急を設計する |
| `define-referents` | 新語や曖昧語を導入する前に、具体的な指示対象と意味上の役割を固定する |
| `design-agent-instructions` | AGENTS.md / CLAUDE.md / copilot-instructions.md / GEMINI.md を設計する |
| `design-changes` | 実装前に変更方針・影響範囲・リスク・確認方針を設計する |
| `design-skill` | 新しい Skill を設計するか、既存 Skill の責務を大きく見直す |
| `diversify-agent-search` | 停滞した agent / workflow 改善を、複数候補・多様性軸・ケース別評価で広げる |
| `draft-commit` | 差分からコミットメッセージ案やコミット分割案を作成する |
| `draft-issue` | 明確化した課題を Issue の起票案と起票手順に落とし込む |
| `draft-review-comments` | 整理済みの指摘を GitHub PR の行コメントとレビュー要約に変換する |
| `format-markdown` | CommonMark 規約に従って Markdown を整形する |
| `implement-changes` | TDD 前提で小さく安全に変更を実装する |
| `investigate-incident` | インシデントを調査し、事実を集め、仮説を立て、原因を特定する |
| `japanese-tech-writing` | 日本語技術文書の整形・論証構成・用語・推敲の規範を適用する |
| `plan-risky-change` | リスクの高い・不可逆な変更を安全確認を明示して計画する |
| `record-session-handoff` | 次のセッションがコンテキストを失わずに再開できる引き継ぎ記録を残す |
| `research-web-safely` | 外部コンテンツを未検証入力として扱いながら Web でトピックを調査する |
| `review-changes` | 差分を正確性でレビューし、指摘を分類する |
| `scope-implementation` | 実装タスクの範囲を開始前に絞り込む |
| `scope-request` | 依頼の目的・完了条件・制約・未解決事項を整理する |
| `summarize-changes` | 差分またはコミット範囲をレビューや文書化のために要約する |
| `triage-agent-usage` | エージェント利用が適切か評価し、委任レベルを調整する |
| `triage-review-feedback` | レビュー指摘を採用・保留・却下に分け、対応方針を決める |
| `validate-fix` | 修正を検証し、確認済み・未確認・残るリスクを整理する |

## インストール

### Claude Code (APM)

```bash
apm install mtk177a/skills
```

または `apm.yml` の依存として宣言する場合:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### 個別 Skill のインストール

```bash
apm install mtk177a/skills/skills/review-changes
```

### その他のクライアント

`skills/<name>/SKILL.md` を探索するクライアントであれば動作します。検証済みクライアントとインストール方法については [docs/compatibility.md](docs/compatibility.md) を参照してください。

## リポジトリ構成

```text
.
├── README.md
├── README.ja.md
├── LICENSE
├── AGENTS.md
├── AGENTS-ja.md
├── CLAUDE.md
├── CLAUDE-ja.md
├── .github/
│   └── copilot-instructions.md
├── apm.yml
├── docs/
│   ├── authoring.md
│   ├── compatibility.md
│   ├── evaluation.md
│   ├── localization.md
│   └── workflows.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── SKILL-ja.md
│       ├── evals/
│       ├── references/
│       ├── scripts/
│       └── assets/
```

`evals/`、`references/`、`scripts/`、`assets/` は任意であり、必要な Skill だけが持ちます。

## 作成と貢献

個人用リポジトリのため、外部からの貢献は想定していません。

Skill を活用したい場合は、MIT ライセンスの範囲で自由に利用・改変できます。Skill の構成については [docs/authoring.md](docs/authoring.md) を参照してください。

## ライセンス

[MIT License](LICENSE)

Copyright (c) 2026 mtk177a
