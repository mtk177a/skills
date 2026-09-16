> **注記:** このファイルは英語版 (`README.md`) の参考訳です。内容に差異がある場合は英語版を優先してください。

# skills

[mtk177a](https://github.com/mtk177a) が作成・保守する個人用エージェント Skill リポジトリです。

各 Skill は [Agent Skills 仕様](https://agentskills.io/specification) に準拠しています。
形式上の互換性だけでは、クライアントによる探索や実行時の動作まで確認できません。
このリポジトリには Codex を対象とした限定的な動作確認結果がありますが、Claude Code、GitHub Copilot、Gemini CLI などのクライアントは未検証です。
証拠の状態と検証範囲は [docs/ja/compatibility.md](docs/ja/compatibility.md) を参照してください。

> **無保証。** このリポジトリは、個人が可能な範囲で保守しています。Skill は予告なく変更・削除される場合があります。自己責任でご利用ください。

## Skill 一覧

開発作業全般をカバーする 27 の Skill を収録しています。

| Skill | 説明 |
| --- | --- |
| `audit-agent-guidance` | 継続的に適用するエージェント向け指示を、期待する挙動、観測済みの利用状況、クライアントの仕様、評価結果に照らして監査する |
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
| `explore-decision-space` | 重要な意思決定が早期に収束する前に、問題の捉え方や解決案の選択肢を広げる |
| `draft-commit` | Git のステージング境界を保ちながら、変更単位ごとのコミット計画と Conventional Commits メッセージを作成する |
| `draft-issue` | 根拠と課題管理システムの確認状況を保ったまま、未投稿の Issue 案と投稿に必要な引き継ぎ情報を作る |
| `draft-review-comments` | 評価、現在の状態、対応方針が明示された指摘から、未投稿の PR コメント案を作る |
| `revise-docs-fresh-eyes` | 執筆時の会話を受け取らない Codex または Claude Code のサブエージェントに、既存文書を初見で読ませ、改稿を完結させる |
| `implement-changes` | 承認済みの変更を小さな単位で、TDD または適切な別の検証方法を使って実装する |
| `investigate-failure` | 環境を問わず、原因不明のエラー、失敗するテスト、回帰、性能上の異常、予期しない技術的挙動を調査する |
| `japanese-tech-writing` | 日本語技術文書の整形・論証構成・用語・推敲の規範を適用する |
| `assess-risky-change-readiness` | 重大または復旧困難な変更について、安全対策、復旧方法、証拠、承認状況が実行判断に十分かを評価する |
| `record-session-handoff` | 後続の AI エージェントが状態を再検証し、安全に作業を再開できるよう、証拠に基づく引き継ぎを記録する |
| `research-web-safely` | 取得したコンテンツを命令として扱わず、追跡可能な Web 上の根拠を収集・評価する |
| `review-changes` | 新規差分または明示的に依頼された全面再レビューについて、リスクに見合った背景情報と所定のラベルを添えて問題点を報告する |
| `summarize-changes` | 差分またはコミット範囲をレビューや文書化のために要約する |
| `triage-review-feedback` | 指摘の妥当性と現在の状態を、`Act now`・`Defer`・`No action` の対応方針とは分けて評価する |
| `validate-fix` | 特定済みの指摘に対する通常の修正後レビューを、適切な読み取り専用の証拠を使って限定的に行う |
| `write-natural-japanese` | 意味、確度、定着した用語を保ちながら、文脈に合う表現で日本語の文章を作成・推敲する |

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

`cognitive-rhythm-writing` は `japanese-tech-writing` を必要とします。バンドルから 2 つを一緒に導入します。

```bash
apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing
```

### その他のクライアント

標準の `skills/<name>/SKILL.md` パッケージを検出できるクライアントは、形式上の互換性を持つ可能性があります。
ただし、このリポジトリはクライアントごとの証拠を記録していない実行時動作を対応済みとは扱いません。
文書化された動作、ローカルでの検証結果、インストール方法は [docs/ja/compatibility.md](docs/ja/compatibility.md) を参照してください。

## リポジトリの検証

リポジトリのルートで、機械的かつ読み取り専用の整合性検査を実行します。

```bash
python3 scripts/check_repository.py
```

リポジトリに不整合がなければ終了コード `0`、対応が必要な不整合を検出した場合は `1`、呼び出し方法または検査自体に失敗した場合は `2` を返します。LLM を呼び出したりリポジトリの内容を変更したりせず、構造、メタデータ、リンク、参考訳の注記、評価結果、配備時に生成されるファイルを確認します。

この検査は、Skill 評価の静的検証を担います。挙動、呼び出し、比較、モデルを使う評価が必要な場合に、それらを置き換えるものではありません。

## Skill 評価 Runner

Codex を呼び出す前に、共通 Runner で対象を選択し、評価コストを確認します。

```bash
python3 scripts/run_skill_evaluation.py plan --help
```

Runner は編集後に評価を自動実行せず、全ケースを暗黙に選択しません。\
モデルを使う経路では、実行可能な `{skill_name, evals}` 形式を使用します。旧形式の評価用ファイルは、各 Skill を初めて実質的に変更するときに Skill 単位で移行します。移行前でも `static-only` は使用できます。\
経路の選択、実行、採点、簡潔な評価記録の扱いは [docs/ja/evaluation.md](docs/ja/evaluation.md) を参照してください。

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

このリポジトリ向けに独自作成したコードとコンテンツは、MIT ライセンスの範囲で利用・改変できます。第三者の著作物を基にしたファイルには個別のライセンスが適用されます。詳細は [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。Skill の構成は [docs/ja/authoring.md](docs/ja/authoring.md)、第三者が提供する Skill や実行可能な Skill の確認方法は [docs/ja/security.md](docs/ja/security.md) を参照してください。

## ライセンス

このリポジトリで独自作成したコードとコンテンツには [MIT License](LICENSE) を適用します。第三者の著作物を基にした素材には、[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) に記載した個別の条件が適用されます。

Copyright (c) 2026 mtk177a
