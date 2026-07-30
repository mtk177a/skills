> **注記:** 英語版 (`README.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# skills

[mtk177a](https://github.com/mtk177a) が作成・保守する個人用エージェント Skill リポジトリです。

各 Skill は [Agent Skills 仕様](https://agentskills.io/specification) に準拠しており、Codex、Claude Code、GitHub Copilot、Gemini CLI などの対応クライアントで利用できます。

> **無保証。** このリポジトリは個人が手の空いたときに保守するものです。Skill は予告なく変更・削除される場合があります。自己責任でご利用ください。

## Skill 一覧

開発作業全般をカバーする 25 の Skill を収録しています。

| Skill | 説明 |
| --- | --- |
| `audit-agent-guidance` | 永続的な agent guidance を期待する挙動、観測済みの利用状況、client semantics、評価証拠に照らして監査する |
| `break-failure-loop` | 新しい証拠がない同じ仮説による同等試行を停止し、診断、blocked、または探索拡張への引き継ぎを選ぶ |
| `calibrate-learning-support` | 作業を進めながら task 固有の理解、decision ownership、verification を保てるよう AI の learning support を調整する |
| `clarify-request` | 曖昧な依頼を、次の workflow を開始できるか、低影響な前提で進めるか、blocked と判断できるまで反復して明確化・構造化する |
| `cognitive-rhythm-writing` | 認知モードと未回収の緊張を管理し、日本語の説明文に緩急を設計する |
| `define-referents` | 曖昧な語を具体的な指示対象へ結び付け、命名上の制約を元の workflow へ返す |
| `design-agent-instructions` | AGENTS.md / CLAUDE.md / copilot-instructions.md / GEMINI.md を設計する |
| `design-changes` | 実装前に変更方針・影響範囲・リスク・確認方針を設計する |
| `design-skill` | Skill を新規作成・統合・分割・大幅な責務変更のどれで設計するか、実装前に判断する |
| `explore-decision-space` | 重要な意思決定が早期収束する前に、問題フレームまたは解決案を広げる |
| `draft-commit` | Git の staging 境界を保ちながら、原子的なコミット計画と Conventional Commits メッセージを作成する |
| `draft-issue` | 明確化した課題を Issue の起票案と起票手順に落とし込む |
| `draft-review-comments` | 整理済みの指摘と判断の意味を変えず、未投稿の PR コメント案へ変換する |
| `edit-for-readers` | 既存の草稿を読後目標に照らして編集し、重複を削って不足する文脈を特定する |
| `implement-changes` | 承認済みの変更を小さな単位で、TDD または適切な別の検証方法を使って実装する |
| `investigate-failure` | 環境を問わず、原因不明の error、failing test、regression、performance anomaly、予期しない技術的挙動を調査する |
| `japanese-tech-writing` | 日本語技術文書の整形・論証構成・用語・推敲の規範を適用する |
| `plan-risky-change` | リスクの高い・不可逆な変更を安全確認を明示して計画する |
| `record-session-handoff` | 次のセッションがコンテキストを失わずに再開できる引き継ぎ記録を残す |
| `research-web-safely` | 取得したコンテンツを命令として扱わず、追跡可能な Web 上の根拠を収集・評価する |
| `review-changes` | コード・文書・設定の差分を、根拠・影響・確信度・正規ラベル付きでレビューする |
| `summarize-changes` | 差分またはコミット範囲をレビューや文書化のために要約する |
| `triage-agent-usage` | 作業開始前に、必要十分な agent、tool、model capability、context、work-unit structure を選ぶ |
| `triage-review-feedback` | 既存レビュー指摘の出所、根拠、不確実性を保持し、採用・保留・却下と対応方針を決める |
| `validate-fix` | 特定の完了済み修正が元の指摘または期待動作を解消したか、適切な read-only evidence で検証する |

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

`cognitive-rhythm-writing` は `japanese-tech-writing` を必要とします。bundle から2件を一緒に導入します。

```bash
apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing
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
│   ├── security.md
│   └── workflows.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── SKILL-ja.md  # 任意の日本語参考訳
│       ├── evals/
│       ├── references/
│       ├── scripts/
│       └── assets/
```

`evals/`、`references/`、`scripts/`、`assets/` は任意であり、必要な Skill だけが持ちます。

## 作成と貢献

個人用リポジトリのため、外部からの貢献は想定していません。

このリポジトリ向けに独自作成したコードとコンテンツは、MIT ライセンスの範囲で利用・改変できます。第三者の著作物を基にしたファイルには個別のライセンスが適用されます。詳細は [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。Skill の構成は [docs/authoring.md](docs/authoring.md)、第三者または executable Skill の review は [docs/security.md](docs/security.md) を参照してください。

## ライセンス

このリポジトリで独自作成したコードとコンテンツには [MIT License](LICENSE) を適用します。第三者の著作物を基にした素材には、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載した個別の条件が適用されます。

Copyright (c) 2026 mtk177a
