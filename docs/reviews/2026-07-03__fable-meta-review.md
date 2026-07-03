---
title: Fable meta review
date: 2026-07-03
reviewer: Claude Fable
status: proposed
repository: mtk177a/skills
base_ref: 1c80f52edf655bd0d16bb262bef8a7db87721b4d
scope:
  - skill taxonomy
  - agent skills
  - descriptions
  - evaluations
  - public repository safety
  - multi-agent compatibility
do_not_treat_as_source_of_truth: true
---

# Fable meta review

> **本文書の位置づけ:** これは外部モデル (Claude Fable) による設計監査の**提案**であり、採用済み方針ではない。ここに書かれた内容は、人間または別モデルによるレビューを経て個別に採否を判断すること。本文書自体は `AGENTS.md` / `docs/*` の規範ではなく、`do_not_treat_as_source_of_truth: true` のとおり将来の agent が指示として従う対象でもない。
>
> 本文書は要望者(リポジトリ所有者)向けの日本語で書いている。リポジトリの正本言語ポリシー(英語正本)からは意図的に外れており、扱いは §16 の open question とした。

## 1. Executive summary

- このリポジトリの最大の論点は **「24 個の Skill がすべてプロセス系(SDLC の局面を動詞で切ったもの)であり、互いに・そして agent ハーネスの標準挙動と、発火条件が競合している」** ことである。ドメイン知識系 Skill が 1 つもなく、`scope-request` / `scope-implementation` / `clarify-request` / `design-changes` のような近縁 Skill 群を、agent が description だけで正しく選び分けられる根拠がない。
- 2 番目の論点は **評価の実行負債**。全 24 Skill に `evals/README.md` があるが、実行記録 (Iter N) を持つのは 3 Skill のみで、しかも日付不明。残り 21 は静的チェック+シナリオ定義のみ、つまり「blank-slate agent で再現できることの確認」という evals の存在目的が大半で未達成である。さらに、最大リスクである「24 個の中から正しい Skill が選ばれるか」(trigger 精度) を測る評価が 1 つも存在しない。
- 3 番目の論点は **互換性主張の温度差**。`docs/compatibility.md` は誠実に「検証済みは APM のみ」と書いているが、README 冒頭は "designed for Codex, Claude Code, GitHub Copilot, Gemini CLI" と読め、未検証の互換を匂わせる形になっている。
- 一方で、public repo としての安全衛生 (secrets 不在、`THIRD_PARTY_NOTICES.md`、license frontmatter、外部 Skill の verbatim copy 禁止、repo-local Skill の分離) は個人リポジトリとしては水準以上に整っている。
- 推奨は「大規模再設計 (Option C) ではなく、**description 文法の統一 → trigger 評価資産の新設 → 3 組の Skill 統合 (24→約 18) → 2 クライアントでの実測**」を 30 日で行う中規模改善 (Option B-lite) である。

## 2. Repository diagnosis

### 目的の再定義

このリポジトリは、個人が作成・保守する agent Skills を Agent Skills 仕様に沿って公開し、(1) 自分の複数 agent 環境 (Claude Code / Codex / Copilot / Gemini CLI) に APM 経由で配布し、(2) 他者が MIT で再利用できるようにするためのものである。実体は「開発プロセスの各局面での判断基準・出力契約を Skill 化した、個人のワークフロー標準ライブラリ」であり、ドメイン知識の配布物ではない。

### うまくいっている点

- **構造規律**: `skills/<name>/SKILL.md` 単位、kebab-case、frontmatter 必須 3 項目 (`name`/`description`/`license`) が全 24 Skill で守られている。
- **境界の型**: 全 Skill が `Always / Ask first / Never` の Boundaries 節を持ち、出力契約 (Output format) が定義されている。これは多くの公開 Skills repo より厳格。
- **public 安全衛生**: secrets・個人情報・内部 URL は見つからなかった。CC BY-SA 資料を削除した履歴まで `THIRD_PARTY_NOTICES.md` に記録されており、ライセンス意識が高い。
- **repo-local Skill の分離**: `.agents/skills/refresh-apm-lockfile/` を公開カタログから明示的に除外し、`.gitignore` の例外指定も正しい。
- **翻訳規律**: 全 `SKILL-ja.md` が「英語版が正本」注記を持つ (docs のテンプレートは英語文だが実ファイルは日本語文 — 軽微な形式ドリフト)。
- **compatibility.md の誠実さ**: 未検証を `—` で明示する表がすでにある。

### 現在の最大リスク

1. **Trigger 競合**: 近縁 Skill 群 (scope/clarify/design 系、review 系、delegation 系) の description が相互に区別しづらく、agent の選択が不安定になりうる。加えて Claude Code には bundled の `/code-review`・`/review` があり、`review-changes` と正面衝突する。
2. **Trigger 評価の不在**: 「発火すべき時に発火するか」「発火すべきでない時に発火しないか」を測る資産がゼロ。Claude Code 公式 docs も invocation と output quality を別軸で測ることを推奨している。
3. **評価の形骸化**: 21/24 Skill の evals が未実行。実行済み 3 件も日付不明で、計測項目 (steps/duration) が「取得できなかった」と注記されたまま。
4. **互換性主張と検証状態の乖離**: README の "designed for" 4 クライアントのうち検証済みは 0。検証済みは APM install のみ。
5. **Skill 境界と host repo ポリシーの衝突**: 各 Skill の `Never` / `Ask first` は消費側リポジトリの `AGENTS.md` と競合しうる強い行動制約 (例: `clarify-request` の「確認なしで実装に進むな」、`implement-changes` の TDD 既定化) をグローバルに持ち込む。
6. **手順書化の進行**: `draft-review-comments` は Steps 23 項目・162 行 evals を持ち、判断基準よりも網羅的手順が支配的。この密度が他 Skill にも伝播しつつある (`design-changes` 13 steps に readability 改善の特殊ケースが埋め込まれるなど)。
7. **メタ系 Skill の増殖**: `audit-agent-rules` / `design-agent-instructions` / `design-skill` に加え `triage-agent-usage` / `calibrate-ai-learning` と、メタ・自己言及系が 5 つあり、境界が曖昧 (§5)。
8. **SKILL-ja.md の frontmatter 重複**: `SKILL-ja.md` も同じ `name` と日本語 `description` の frontmatter を持つ。`SKILL.md` のみを探索するクライアントでは無害だが、`*.md` を広く走査するクライアントで同名 Skill が二重登録される可能性が未検証。
9. **人間向け Skill の混在**: `triage-agent-usage` / `calibrate-ai-learning` は「人間がどのツールを使うか・どこまで委任するか」を扱う。agent が自動発火させる Skill としては主語が曖昧で、発火してもユーザー期待とずれやすい。
10. **lockfile の自己参照ワークフローの複雑さ**: `apm.yml` が自リポジトリの Skill に依存する構造のため、lockfile 更新に使い捨てコピーが必要という運用制約が生じており、`refresh-apm-lockfile` という repo-local Skill を要するほど手順が重い。

### 既存指示に引っ張られて見落としやすい論点

- `AGENTS.md` は「per-agent ディレクトリを作らない」「差異は name/description で表現」と定めるが、**その方式が実際に機能するかを確かめる手段 (per-client 検証) が用意されていない**。構成ルールが検証義務を代替してしまっている。
- `docs/workflows.md` の 5 段パイプライン (scope→design→implement→review→validate) は美しいが、**ハーネス (Claude Code の plan mode、TodoList、bundled review) がすでに同じ流れを内蔵している**。Skill 側の付加価値は「出力契約と判断基準」であって工程そのものではない、という視点が既存 docs からは出てこない。
- 「Skill は増やすもの」という暗黙前提。`design-skill` は新設時の重複チェックを求めるが、**既存 24 個を減らす・統合するための基準はどこにもない**。
- 「macOS M1 / Windows WSL 互換」という個人環境要件が `AGENTS.md` と `docs/authoring.md` に公開仕様として書かれている。秘匿情報ではないが、public 文書としては「POSIX シェル + Windows WSL で動くこと」等へ一般化した方が意図が伝わる。

## 3. Evidence map

### 重要な根拠ファイル(事実)

| ファイル | 根拠となる事実 |
| --- | --- |
| `README.md` | 24 Skills、"designed for Codex, Claude Code, GitHub Copilot, Gemini CLI"、APM install 手順 |
| `docs/compatibility.md` | 検証済みは APM (2026-06-10, apm 0.13.0) のみ。4 クライアントは `—` (pending) |
| `docs/evaluation.md` | blank-slate subagent プロトコル、Iter 0 静的チェック、mizchi/skills 由来の手法と明記 |
| `docs/workflows.md` | 5 段パイプラインと 3 つのワークフロー定義 |
| `skills/*/SKILL.md` (23) + `.agents/skills/refresh-apm-lockfile/` (1) | 全 24 Skill の frontmatter・Boundaries・Steps。license 欠落ゼロ |
| `skills/*/evals/README.md` | Iter N 実行記録を持つのは `audit-agent-rules` (Iter 2 まで) / `design-agent-instructions` / `design-skill` のみ。いずれも "date unknown" |
| `apm.yml` / `apm.lock.yaml` | 23 Skill の自己参照依存、lockfile は commit + sha256 で固定 (supply-chain 上は良い性質) |
| `THIRD_PARTY_NOTICES.md` | 帰属・ライセンスの整理、CC BY-SA 資料の削除記録 |
| git 履歴 | 約 50 commits、2026-05-18 〜 2026-06-19 の約 1 か月で構築された若いリポジトリ |

### 外部 docs / community 情報(信頼度つき)

| 情報 | 出典 | 信頼度 |
| --- | --- | --- |
| SKILL.md frontmatter は全項目 optional、`description` が発火判断の入口。description+when_to_use は一覧上 1,536 字で切られる。`disable-model-invocation` で自動発火を止められる。invocation 精度 (should-trigger / should-not-trigger) と出力品質を別々に測ることを推奨 | Claude Code 公式 docs (code.claude.com/docs/en/skills) | 高 |
| GitHub Copilot は 2025-12 に Agent Skills 対応を発表。VS Code にも Agent Skills docs あり | GitHub Changelog / VS Code docs | 高 |
| Agent Skills 標準は 2025-12 公開後、Codex CLI / Gemini CLI / Cursor 等 30+ プラットフォームに採用。`gh skill` コマンドが 2026-04 に登場、skills.sh (Vercel) が 2026-01 にディレクトリ開設 | community blog / 集約サイト (codex.danielvaughan.com, open-techstack.com, inference.sh 等) | 中 — 傾向として整合するが個別の数値・日付は一次情報での再確認が必要 |
| mizchi/skills は 59 Skills をドメイン別 (Frontend/AWS/SQL 等) に分類し、プロセス/メタ系は 7 個のみ。`waxa` CLI + `evals/eval.yaml` で評価を自動実行 | GitHub (mizchi/skills) | 中〜高 — リポジトリ実体は一次情報だが、要約は本レビュー時のスナップショット |
| agentskills.io/specification 本文 | 取得失敗 (HTTP 403) | **未確認** — 仕様の必須項目・字数制約は一次情報で要再確認 |

### 未確認だが確認すべき事項

- Agent Skills 仕様上の `name` / `description` の正確な制約 (文字数・文法) と、`license` を含む optional フィールドの正式な扱い。
- Codex / Copilot / Gemini CLI が `SKILL-ja.md` のような同 directory 内の追加 `.md` frontmatter をどう扱うか (重複登録の有無)。
- 各クライアントが「repo を丸ごと install」した際に `docs/` や `.agents/` を Skill 探索対象に含めるか。
- `gh skill` / `npx skills add` でこのリポジトリが実際に import できるか。

### 事実 / 推測 / 判断の区別

- **事実**: 上記ファイル引用、evals 実行状況、検証マトリクスの空欄。
- **推測**: 「近縁 description で agent の選択が不安定になる」— 構造からの推論であり、trigger 評価が存在しないため実測データはない (だからこそ trigger 評価が最優先)。
- **判断**: 統合候補の選定、Option B-lite の推奨、Do-not-do の内容。

## 4. Skill inventory

24 Skill (公開 23 + repo-local 1)。verdict は本レビューの提案であり決定ではない。

| name | actual purpose | trigger (description が想定する発火) | overlap | risk | keep / revise / merge / remove |
| --- | --- | --- | --- | --- | --- |
| `scope-request` | 依頼を目的・完了条件・制約に構造化 | 依頼の背景・目的が不明瞭なとき | `clarify-request`, `scope-implementation`, `design-changes` | 近縁 3 Skill との選択が不安定 | **revise** (統合クラスタの中核として残す) |
| `clarify-request` | 曖昧な依頼に 1–4 の質問を返す | 依頼が多義的なとき | `scope-request` | 発火しすぎ (曖昧さは常にある)。`Never: 確認なしで実装に進まない` はグローバル制約として強すぎる | **revise** (質問行為に限定、Never を緩和) |
| `scope-implementation` | 実装前に対象/立入禁止ファイルと検証コマンドを固定 | 「Issue まるごと」等の広い依頼 | `scope-request`, `design-changes` | `scope-request` と役割が説明しないと区別できない | **merge** → `scope-request` または `design-changes` へ |
| `design-changes` | 実装前の変更設計・影響・検証戦略 | 実装前に設計したいとき | `plan-risky-change`, `scope-implementation` | 13 steps に readability 改善等の特殊ケースが混入し肥大 | **revise** (特殊ケースを references/ へ) |
| `plan-risky-change` | 危険な変更の計画+承認取得 | destructive / migration / dependency / security | `design-changes` | 低。境界は比較的明確 | **keep** |
| `implement-changes` | TDD での漸進実装 | 実装を進めるとき | ハーネス標準挙動 | TDD を全実装の既定にする「重い既定」。発火すれば常に TDD を要求 | **revise** (TDD は条件付き推奨に、または description で「TDD で進めたいとき」に限定) |
| `review-changes` | diff レビュー+正準ラベル付け | コードレビュー依頼時 | Claude Code bundled `/code-review`・`/review`、`draft-review-comments` | bundled skill との発火競合が未整理 | **revise** (bundled との差分=ラベル体系と後工程接続を description で明示) |
| `draft-review-comments` | 所見を GitHub インラインコメント化 | レビュー所見を PR コメントにするとき | `review-changes` | 23 steps の手順書化。判断基準が手順に埋没 | **revise** (steps を 8 前後へ圧縮、語彙・トーン規則は references/ へ) |
| `triage-review-feedback` | 受領コメントの採否振り分け | 他者/他 AI のレビューを受けたとき | `review-changes` (方向が逆) | 低。「受ける側」で区別明確 | **keep** |
| `validate-fix` | 修正後の確認済み/未確認/残リスク整理 | 修正後の検証時 | `review-changes` | 低 | **keep** |
| `summarize-changes` | diff の PR 説明・共有向け要約 | PR 説明を書くとき | `draft-commit`, `record-session-handoff` | 低 (本文に区別 Note あり — 良い先例) | **keep** |
| `draft-commit` | Conventional Commits 提案 | コミットメッセージ作成時 | ハーネスの commit 機能 | 低 | **keep** |
| `draft-issue` | 依頼を Issue 草案化 | Issue 化したいとき | `scope-request` | description が `(from scope-request)` と他 Skill 参照 — blank-slate で意味不明 | **revise** (description から skill 参照を除去) |
| `break-failure-loop` | 同一失敗 2 回で停止・再構成 | 同じエラー/アプローチで 2 回失敗 | `diversify-agent-search` | 低 (発火条件が数値的で良い) | **keep** (統合先として) |
| `diversify-agent-search` | 候補アーカイブ・多様性軸での探索拡張 | 同一設計近傍で停滞 | `break-failure-loop` | 発火しづらい (抽象概念が description の主語)。ニッチ | **merge** → `break-failure-loop` の escalation または references/ へ |
| `investigate-incident` | 本番エラーの原因調査 | stack trace / 障害発生時 | なし | 低 | **keep** |
| `triage-agent-usage` | タスクに適したツール/モデル重量の選定 | 作業開始前 | `calibrate-ai-learning` | 主語が人間 (ユーザーのツール選択)。agent 自動発火の価値が不明瞭。「作業開始前」は常時発火しうる | **merge** → `calibrate-ai-learning` と統合 |
| `calibrate-ai-learning` | 委任と自己理解のバランス調整 | 委任が深くなりすぎたとき | `triage-agent-usage` | 「深くなりすぎ」を誰がどう検知するか不明。発火困難 | **merge** (同上、統合後 `disable-model-invocation` 相当の手動起動も検討) |
| `record-session-handoff` | セッション間引き継ぎノート | セッション切替時 | ハーネスのセッション継続機能 | 保存場所が入力依存 (Ask first で担保 — 良い) | **keep** |
| `research-web-safely` | 外部情報を untrusted として調査 | Web 調査を含む依頼時 | ハーネスの標準的注意 | 手順よりポリシー性が強い。dotfiles のグローバル指示候補 | **keep** だが配置再考 (§5) |
| `format-markdown` | CommonMark 基準の整形 | Markdown スタイル修正時 | ハーネス標準挙動 | keyword 列挙 `(markdown, ...)` で発火しすぎの懸念。Markdown 編集は高頻度 | **revise or remove** (「スタイル統一を明示依頼されたとき」に限定) |
| `audit-agent-rules` | AGENTS/skills/docs の監査・小改善提案 | 指示文書の改善提案時 | `design-agent-instructions`, `design-skill` | メタ 3 兄弟の境界曖昧 (§5) | **revise** (「既存の監査」に限定を明文化) |
| `design-agent-instructions` | AGENTS.md 等の文書セット設計 | 指示文書の新設・再編時 | `audit-agent-rules` | Codex 固有の読み込み順 (`~/.codex/AGENTS.md`) が本文に固定されている | **revise** (loading order をクライアント別 references/ へ) |
| `design-skill` | 新規 Skill の設計・大幅改訂 | Skill 新設/大改訂時 | `audit-agent-rules` | 「大幅改訂」が audit と重なる | **revise** (改訂系は design-skill、監査提案は audit と役割文を相互に明記) |
| `refresh-apm-lockfile` (repo-local) | 使い捨てコピーで lockfile 更新 | この repo で lockfile 更新時 | なし | 低 (precondition が厳格で良い設計) | **keep** |

集計: keep 9 / revise 10 / merge 4 (→2 Skill に統合) / remove 候補 1 (`format-markdown` は revise で救済可)。統合後の想定は **約 18 Skill**。

## 5. Skill taxonomy redesign

### 現状の暗黙分類と問題

現状は `docs/workflows.md` の 5 段パイプラインが唯一の分類だが、24 Skill 中パイプラインに登場するのは 8 個で、残り 16 個の位置づけが README のフラットな表にしかない。全 Skill が「プロセス系」であるため、動詞 (scope/design/draft/triage/review/validate) の意味距離が近く、名前だけでは責務境界が読めない組が複数ある。

### 提案する分類軸 (docs に 1 ページ追加する想定)

| カテゴリ | Skill | 特徴 |
| --- | --- | --- |
| **core workflow** | scope-request (統合後), design-changes, implement-changes, review-changes, validate-fix | 5 段パイプライン。相互参照可・単独動作必須 |
| **delivery artifacts** | draft-commit, draft-issue, draft-review-comments, summarize-changes | 成果物の草案生成。発火は成果物名で判定しやすい |
| **feedback intake** | triage-review-feedback | 受領側。review-changes と方向が逆であることを description に明記 |
| **recovery** | break-failure-loop (diversify を吸収), investigate-incident | 異常時のみ発火。発火条件が数値・事象ベース |
| **session / knowledge ops** | record-session-handoff, research-web-safely | 横断的ポリシー・運用 |
| **meta (repo/instruction design)** | audit-agent-rules, design-agent-instructions, design-skill | 指示文書と Skill 自体を扱う。**新設: 既存監査は audit、文書セット新設は design-agent-instructions、Skill 単体の新設/改訂は design-skill、という 1 行の相互境界宣言を 3 Skill すべての本文に置く** |
| **delegation calibration (人間向け)** | triage-agent-usage + calibrate-ai-learning の統合 Skill | 主語が人間。自動発火より手動起動 (`/skill-name`) 向き。Claude Code なら `disable-model-invocation: true` の利用を検討 (他クライアント互換性は要確認) |
| **repo-local ops** | refresh-apm-lockfile | 公開カタログ外 (現状維持) |

### Skill / AGENTS / CLAUDE / docs / dotfiles の責務境界

| 置き場所 | 置くべきもの | 現状からの移動候補 |
| --- | --- | --- |
| `skills/*/SKILL.md` | 発火条件が特定でき、出力契約を持つ手続き・判断基準 | — |
| repo の `AGENTS.md` / `CLAUDE.md` | このリポジトリ自体の契約 (承認境界・構造規則)。常時読み込みなので短く | `docs/workflows.md` の Stop conditions は AGENTS.md と重複 — 片方を参照に |
| `docs/*` | 分類・評価・互換性など、常時読み込み不要の運用知識 | taxonomy ページ新設 |
| **dotfiles (個人 global instruction)** | 個人の普遍的な好み・ポリシーで、配布物として他者に押しつけるべきでないもの | `implement-changes` の「TDD を既定とする」姿勢、`research-web-safely` のポリシー部分、`clarify-request` の「確認なしに実装しない」制約は、dotfiles 側で持ち Skill 側は手続きだけにする選択肢がある |
| repo-local Skill (`.agents/skills/`) | この repo の保守専用手順 | 現状どおり |

原則の提案: **「消費側リポジトリの AGENTS.md と衝突しうる恒常的な行動制約は Skill の Never に書かない。Skill の Never はその Skill の出力に閉じた禁止のみとする」**。現状の一部 Never (例: clarify-request) はグローバル行動規範であり、host repo のポリシーと二重管理になる。

## 6. Description and trigger review

### 共通ルール案 (docs/authoring.md への追記候補)

1. **文法を統一する**: `<何をするか (三人称・動詞句)> — Use when <発火すべき状況>. <(任意) Not for <発火すべきでない状況>>`。現状は「Use when you want to…」(ユーザー視点) と「Verb object …」(機能視点) が混在している。
2. **発火すべきでない状況 (negative trigger) を近縁 Skill がある場合は必須にする**: 例 `review-changes` には "Not for processing review comments you received (use triage-review-feedback)" を入れる。24 個が同時にリストされる前提では、負の条件が選択安定性を決める。
3. **description に他 Skill 名を「入力の出所」として書かない**: `draft-issue` の "(from scope-request)" は blank-slate クライアントで意味を持たない。他 Skill 参照は本文 Companion skills 節のみに置く。
4. **keyword 列挙 `(a, b, c)` の使用基準を決める**: 現在 5 Skill だけが末尾 keyword を持つ。「ユーザーが自然に発する語」を 3–6 個、全 Skill で付けるか、全 Skill で外すかに統一する (Claude Code docs は自然な語をdescription に含めることを推奨)。
5. **長さの目安**: 80–160 字 (英語)。現状最長 `research-web-safely` (239 字) は本文の要約になっており、trigger 判断に不要な文を含む。
6. **主語の明確化**: 人間の行動を変える Skill (delegation calibration 系) は "Use when the user asks to …" と、発火主体が判別できる形にする。

### 発火しづらい description の例

- `calibrate-ai-learning`: "Use when delegation is getting too deep" — 「深すぎる」を agent が自己判定する契機がない。→ 手動起動前提にするか、"Use when the user says they don't understand the changes being made, or asks to learn rather than delegate" のように観測可能な発話に紐づける。
- `diversify-agent-search`: 概念語 (design neighborhood, diversity axes) が主語で、ユーザー発話と結びつかない。→ break-failure-loop 側から到達させる設計にすれば description の負担が消える。

### 発火しすぎる description の例

- `format-markdown`: keyword `(markdown, commonmark, style, format, normalize)` は Markdown を触るあらゆるタスクにマッチしうる。→ "Use when asked to normalize or restyle existing Markdown documents. Not for ordinary editing of Markdown content."
- `triage-agent-usage`: "Before starting work" は理論上すべての作業開始にマッチする。→ 明示依頼 ("which tool/model should I use") に限定。

### 競合する description の例と改善方向

- `scope-request` vs `clarify-request` vs `scope-implementation`: 「曖昧→質問する」(clarify) と「曖昧→構造化して返す」(scope) の 2 機能に統合・再命名し、implementation スコープ固定は design-changes の 1 節に吸収する。
- `review-changes` vs bundled `/code-review` (Claude Code): 差別化点 (正準ラベル体系、triage/draft-comments への接続) を description の先頭に出す。そうでなければ Claude Code 上では bundled が選ばれ続け、この Skill は事実上死蔵される。

### 代表的な Before/After

```yaml
# Before (draft-issue)
description: Turn a clarified request (from scope-request) into an Issue draft
  and filing steps. (issue, ticket, backlog, jira, redmine)

# After (案)
description: Draft a trackable issue (title, body, labels, links) from a request
  or bug report. Use when the user asks to file or prepare an issue on GitHub,
  Jira, Redmine, or Backlog. Not for writing PR descriptions.
```

## 7. Evaluation review

### 現状評価

- **形式は水準以上、実行が伴っていない。** 全 24 Skill に evals/README.md があり、`[critical]` 付きチェックリストと Failure Pattern Ledger の型は良い。しかし実行記録があるのは 3 Skill (audit-agent-rules は Iter 2 まで) のみで、日付は "date unknown"。docs/evaluation.md が定める「blank-slate 再現性の確認」は大半で未実施、という意味で **evals は現時点で「設計書」であって「検証結果」ではない**。
- **決定的な欠落は trigger 評価**。全シナリオが「Skill を与えたらチェックリストを満たすか」(出力品質) のみを測り、「24 個の候補から正しい Skill を選べるか」(invocation) を測っていない。本レビューの最大リスク (§2-1) に対する検証手段がない。
- 実行済み Iter の記録品質は高い (audit-agent-rules の Iter 1→2 は原因分析→修正→再発確認のループが機能している)。手法自体は健全で、足りないのは実行コストを下げる仕組みである (mizchi/skills は `waxa` CLI で自動化しているのに対し、本 repo は手動プロトコルのみ)。

### evals の最低基準 (提案)

1. シナリオ 2 本以上、各シナリオに `[critical]` 1 項目以上 (現状達成)。
2. **should-trigger プロンプト 3 本 / should-not-trigger プロンプト 3 本** (近縁 Skill に流れるべき文面を必ず含む) — 新設。
3. 最低 1 回の blank-slate 実行記録 (日付必須。"date unknown" は不可)。
4. 実行できない場合は「not yet executed」を Iter 表に明記 (正直さの担保 — docs/evaluation.md の既存原則を強制化)。

### 優先的に追加すべき scenario

1. **混同ペア判別**: 「この依頼はどの Skill か」を問う discrimination テスト — (scope-request | clarify-request | scope-implementation)、(review-changes | triage-review-feedback | draft-review-comments)、(break-failure-loop | diversify-agent-search)、(triage-agent-usage | calibrate-ai-learning)。
2. **非発火テスト**: 通常の Markdown 編集で `format-markdown` が発火しないこと。通常実装依頼で `plan-risky-change` が発火しないこと。
3. **ハーネス競合テスト** (Claude Code 限定): bundled `/code-review` 存在下で `review-changes` がいつ選ばれるかの観測。
4. **description-only テスト**: 本文を与えず description だけで agent が用途を正しく説明できるか (description 品質の直接測定)。

### blank-slate 再現性の評価

プロトコル (docs/evaluation.md) 自体は再現可能な書き方だが、(a) subagent 生成手段がツール依存で記録されない、(b) 評価者=作者で独立性がない、(c) 実行がほぼ無い、の 3 点で「再現できる検証になっているか」への回答は現状 **No (設計はあるが証拠がない)**。まず簡易ランナー (シナリオ+SKILL.md を子 agent に渡して checklist 判定を出力するスクリプト 1 本) を用意し、実行コストを下げることが先決。

## 8. Public safety review

### 安全チェックリスト (この repo 用・提案)

- [ ] secrets / token / API key / 鍵形式文字列が本文・scripts・evals に無い (`gitleaks` 等での定期スキャンを推奨)
- [ ] 個人情報 (メールアドレス・氏名・所属) が git 管理ファイル本文に無い (commit metadata は除く)
- [ ] 会社固有・顧客固有の手順、内部 URL、非公開サービス名が無い
- [ ] ローカル絶対パス (`/Users/...`, `C:\...`, `~` 直書き) が無い
- [ ] evals の実行記録に実プロジェクトの固有情報 (社内 repo 名・実データ) を書き込まない — **将来リスク: Iter 記録は実セッション由来の情報が最も混入しやすい場所**
- [ ] `references/` `assets/` の第三者コンテンツはライセンス確認済みで `THIRD_PARTY_NOTICES.md` に記録
- [ ] scripts はネットワーク・削除操作の範囲が本文の宣言と一致 (refresh-apm-lockfile.sh は `/tmp` 配下の使い捨てコピーに閉じており宣言と一致 — 確認済み)
- [ ] `SKILL-ja.md` を含む全訳文にも同じ基準を適用

### 今回の確認結果

- **問題は検出されなかった** (事実)。grep ベースの走査で secrets・内部 URL・ローカルパスは無し。`THIRD_PARTY_NOTICES.md` による帰属管理と CC BY-SA 資料の削除記録は good practice。
- 軽微な指摘 2 件: (1) 「macOS M1 / Windows WSL」という個人環境の列挙は一般化可能 (§2)。(2) `record-session-handoff` は運用すると個人メモが生まれる構造だが、保存先を Ask first にしており repo 内混入は防がれている。`AGENTS.md` の「`.agents/` に作業メモを置かない」規則と併せて防御は妥当。
- **supply-chain 視点**: 消費側は `apm.lock.yaml` の commit + sha256 で固定でき、改竄検知の下地はある。逆方向 (この repo が外部 Skill を取り込む際) は「verbatim copy 禁止・出所確認」の既存ルールが prompt-injection 混入の一次防御として機能する。追加提案: 外部由来文面を取り込む際「命令形の文 (imperative) を含む引用をそのまま Skill 本文に写さない」を authoring ルールに 1 行加えると、semantic trigger manipulation への備えが明文化される。

## 9. Compatibility roadmap

### 現状評価

| クライアント | 主張 (README/docs) | 実態 | 評価 |
| --- | --- | --- | --- |
| Claude Code | designed for + 「primary development and testing target」 | 開発は Claude Code 上だが compatibility.md の Verified 欄は `—` | **矛盾気味**: primary target なのに未検証表記。install/list/invoke の 3 点を記録すればすぐ ✓ にできる |
| Codex | designed for | 未検証 | 「期待できるが未検証」。Agent Skills 標準採用の報告 (信頼度中) はあるが自リポジトリでの実測なし |
| GitHub Copilot | designed for | 未検証 | 同上。公式が 2025-12 に対応発表 (信頼度高) なので検証コストは低いはず |
| Gemini CLI | designed for | 未検証 | 同上 |
| APM | install 手順記載 | **検証済み** (2026-06-10, apm 0.13.0) | 唯一の verified。妥当 |
| `npx skills add` / `gh skill` | compatibility.md に行あり | 未検証 | — |

**構造的問題**: README の "designed for X, Y, Z" は設計意図の表明だが、初見の読者には対応表明に読める。compatibility.md への参照はあるものの、**主張の強い側 (README) と正確な側 (compatibility.md) が分離しており、強い側が先に目に入る**。

### 検証ロードマップ (提案)

- **Phase 1 (即時・30 日内)**: Claude Code で install / list / invoke / trigger を実測し記録。README の文言を "follows the Agent Skills specification; verified on: Claude Code, APM — see docs/compatibility.md" に変更し、「検証済み」と「仕様準拠により期待できる (未検証)」を README 上でも分離する。
- **Phase 2 (60 日内)**: Copilot (公式対応済みで最も検証しやすい) + Codex のどちらか 1 つで同 3 点を実測。`SKILL-ja.md` の二重登録有無をこのとき確認。
- **Phase 3 (必要になったら)**: Gemini CLI / `gh skill` / `npx skills add`。**全クライアント検証を目標にしない** — 個人リポジトリの保守コストに対して割に合わない。verified 2 クライアント+仕様準拠宣言で十分。
- 検証手順自体を `docs/compatibility.md` に「再現可能なチェックリスト」(install コマンド → 一覧に出るか → 1 Skill を発火させる固定プロンプト) として書くと、将来のクライアント追加時に同じ基準で ✓ を付けられる。

## 10. Root-cause review

1. **Skill 増殖の根因 — 分解単位の選択**: この repo は「SDLC の局面 × 動詞」で Skill を切っている。ドメイン (SQL、AWS、フロントエンド…) で切る場合と違い、プロセス動詞は意味空間が連続的で、切れば切るほど近縁 Skill が生まれる。24 個という数そのものより、**全てが同一の連続空間に載っていること**が trigger 競合の根因。mizchi/skills がプロセス/メタ系を 59 中 7 個に抑えているのは対照的。
2. **責務重複の根因 — 「増やす」ガードはあるが「減らす」基準がない**: `design-skill` は新設時の重複チェックを課すが、既存 Skill 間の統合・廃止を促す仕組み (定期棚卸し、使用実績の記録) がない。増殖は一方向に進む。
3. **評価不足の根因 — 手法の輸入とツールの非輸入**: evals の型は mizchi/skills から輸入されたが、実行を安価にする自動化 (waxa 相当) は輸入されなかった。手動プロトコルの実行コストが高く、「型を書く」ことが「検証する」ことの代替物になった (形式の充足が目的化する典型パターン)。
4. **multi-agent 対応の根因 — 検証責務の所在が構成ルールに転嫁**: 「per-agent ディレクトリを作らない」という構成ポリシーが先に確立し、それで互換性問題が解決したかのような認知が生まれた。実際には互換性は構成ではなく各クライアントの discovery / frontmatter 解釈で決まり、それは実測でしか確認できない。
5. **public safety が良好な根因 (正の根因分析)**: 「外部 Skill を verbatim copy しない」「repo-local を分離する」という初期の 2 決定が、ライセンス・秘匿情報・supply-chain の 3 リスクを同時に抑えている。この 2 決定は今後も維持すべき資産。
6. **dotfiles 境界の根因 — 個人ポリシーの置き場が他にない**: TDD 既定・確認必須・Web 調査ポリシーのような個人の普遍的態度が Skill に混入しているのは、バージョン管理された「個人 global instruction の置き場」がこの repo しかない (または分離されていない) ため。dotfiles 側の受け皿を明確にしない限り、Skill の Never にグローバル規範が書かれ続ける。

## 11. Improvement options

### Option A: Minimal improvement (description と主張の修正のみ)

- 内容: 全 description の文法統一 + negative trigger 追加、README 互換性文言の修正、draft-issue 等の他 Skill 参照除去。ファイル移動・統合なし。
- 効果: trigger 競合の一部緩和、互換性主張の誠実化。1–2 日で完了。
- リスク: 24 個という構造問題と評価負債は残る。「直した感」で根本対処が先送りされる恐れ。
- 捨てる代替案: description の機械的な keyword 全付与 (根拠なく発火率だけ上げるのは逆効果)。

### Option B: Medium redesign (統合 + trigger 評価 + 2 クライアント検証) — 推奨

- 内容: A の全部 + (1) 3 組の統合で 24→約 18 (scope 系、recovery 系、delegation 系)、(2) trigger 評価資産 (should/should-not プロンプト) の新設と混同ペアの実測、(3) taxonomy ページの docs 追加、(4) Claude Code + 1 クライアントの実測 verified 化、(5) 長大 Skill (draft-review-comments 等) の steps 圧縮と references/ 退避。
- 効果: 発火安定性の主因 (近縁 Skill 数と負の条件欠如) に直接作用。評価が「設計書」から「検証結果」に変わる最初の一歩。apm.yml/lockfile 更新は既存の refresh-apm-lockfile ワークフローで処理可能。
- リスク: Skill 統合はリネームを伴い、既に install 済みの利用者 (主に作者自身の他環境) に breaking。deprecation 手順 (旧名 Skill を 1 リリース残すか、README で告知) が必要。工数はレビュー・翻訳込みで数週間。
- 捨てる代替案: 全 24 を一斉リネームして分類 prefix を付ける案 (`review--changes` 等) — 名前は流通資産なので破壊コストが高く、taxonomy は docs で表現すれば足りる。

### Option C: Fundamental redesign (2 層構造への再創設)

- 内容: core pack (5–7 Skill) + opt-in pack に再編、個人ポリシーを dotfiles へ全面移管、eval 自動化ツール導入 (waxa 採用 or 自作)、per-client CI マトリクス、`apm.yml` の自己参照構造の見直し。
- 効果: 構造問題を最も根本的に解決。評価も自動化で継続可能に。
- リスク: 個人リポジトリの保守キャパに対して過大。全 Skill リネーム+再翻訳+再評価で 1–2 か月停止。外部ツール (waxa) への依存はメンテ方針の確認が必要 (この repo の「外部物は出所と保守方針を確認してから」原則に自ら従うべき)。**現時点では効果対コストが合わない**。
- 捨てる代替案: per-agent ディレクトリの導入 — AGENTS.md の既存決定が正しく、標準仕様の方向性 (単一フォーマット横断) とも一致する。復活させるべきでない。

## 12. Recommended plan

**推奨: Option B を 30 日で、以下の順序で実施する。** 原則: 「主張の修正 (安い・非破壊) → 評価資産 (判断材料を作る) → 統合 (破壊的変更は実測データを見てから)」の順に並べ、統合の判断を trigger 実測の後に置く。

| # | 単位 (PR/issue) | 目的 | 対象ファイル | 完了条件 | 検証方法 | ロールバック |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | README 互換性文言の修正 | 未検証互換を匂わせない | `README.md`, `README.ja.md` | verified / expected-unverified が README 上で区別される | 目視 + compatibility.md との整合確認 | revert のみ |
| 2 | Claude Code 実測 verified 化 | primary target の検証記録 | `docs/compatibility.md` (+ja) | install/list/invoke の 3 点に日付入り ✓ | 記録された手順の再実行 | revert のみ |
| 3 | description 全面改訂 | trigger 文法統一・negative trigger 導入 | `skills/*/SKILL.md` (+ja), `docs/authoring.md` (+ja), `README.md` の表 | 全 24 が統一文法。近縁 Skill に Not-for 句。他 Skill 参照ゼロ | #4 の trigger 評価で改訂前後比較 | Skill 単位 revert 可 (1 Skill 1 commit) |
| 4 | trigger 評価資産の新設 | 混同ペアの実測 | `docs/evaluation.md` (+ja), `skills/*/evals/README.md` (混同 4 ペア分から開始) | should/should-not 各 3 プロンプト、blank-slate で 1 回実行・日付入り記録 | 実行記録そのもの | 追記のみなので不要 |
| 5 | 統合 1: delegation 系 | triage-agent-usage + calibrate-ai-learning → 1 Skill | 当該 2 Skill、`apm.yml`, README, workflows | 旧 2 Skill の deprecation 告知、新 Skill の evals Iter 0 完了 | 統合後 Skill で旧シナリオが通る | 旧ディレクトリ復元 (git) |
| 6 | 統合 2: recovery 系 | diversify-agent-search → break-failure-loop へ吸収 | 同上パターン | 同上 | 同上 | 同上 |
| 7 | 統合 3: scope 系 | scope-implementation → scope-request or design-changes | 同上パターン | 同上 (#4 の実測結果で吸収先を決定) | 同上 | 同上 |
| 8 | lockfile 更新 | manifest 整合 | `apm.lock.yaml` | frozen dry-run 通過 | 既存 refresh-apm-lockfile Skill | 旧 lockfile 復元 |
| 9 | taxonomy ページ + 境界原則 | 分類と Skill/AGENTS/dotfiles 境界の明文化 | `docs/` 新規 1 ページ (+ja), `docs/authoring.md` | §5 の表相当が docs 化 | 目視レビュー | revert のみ |
| 10 | 手順書化の圧縮 | draft-review-comments 等の steps 削減 | `skills/draft-review-comments/` (+references/ 新設) | steps ≤ 10、語彙・トーン規則は references/ へ | 既存 evals シナリオが通る | revert |

実施順序: 1 → 2 → 3 → 4 → (4 の結果を確認) → 5 → 6 → 7 → 8 → 9 → 10。#5–7 は各々独立 PR とし、旧 Skill 名の deprecation は README の変更履歴節で告知する。すべて既存の承認境界 (AGENTS.md「docs/Skills 編集は承認後」) に従い、着手前に所有者承認を得ること。

## 13. Do-not-do list

- **Option C (全面再設計) を今やらない**: 実測データ (trigger 評価) なしの再設計は、同じ問題を別の形で作り直すだけになる。
- **per-agent ディレクトリを作らない**: 既存決定が正しい。標準仕様の単一フォーマット方針とも一致。
- **全 Skill の一斉リネームをしない**: 名前は APM 依存参照 (`mtk177a/skills/skills/<name>`) として流通済み。統合対象以外は温存。
- **メタ系 Skill を追加しない**: audit / design-agent-instructions / design-skill の 3 つで既に飽和。本レビューの知見も新 Skill 化せず docs へ。
- **evals の「型」をこれ以上精緻化しない**: 実行されない形式の追加は負債。次に増やすのは実行記録のみ。
- **30+ クライアント互換の追求をしない**: verified 2 + 仕様準拠宣言で個人 repo としては十分。
- **「美しいが危険」な既存設計への注意**: `docs/workflows.md` の 5 段パイプラインは整った見た目に反して、ハーネス内蔵ワークフローとの二重化を促す。パイプライン記述を拡張する方向の作業 (工程の追加、Skill 間の必須依存化) は避ける。各 Skill の単独動作原則 (現在明文化済み) を優先。
- **SKILL-ja.md の自動生成 CI 化を急がない**: 翻訳同期は現状手動で回っている。CI 化はクライアント互換検証 (優先度上) の後。
- **`clarify-request` の Never のような全域制約を他 Skill に増やさない**: host repo の AGENTS.md と衝突する制約は Skill に持ち込まない (§5 の原則)。

## 14. Proposed issues / PRs

他モデルが実装しやすい粒度で 8 件。番号は §12 の実施順序に対応。

1. **docs: align README compatibility claims with verification status**
   - 背景: README は 4 クライアント "designed for"、検証済みは APM のみ。
   - 目的: 未検証互換を匂わせる表現の解消。
   - 対象: `README.md`, `README.ja.md`。
   - 完了条件: "verified" と "spec-compliant, not yet verified" が README 上で区別され、compatibility.md と矛盾しない。
   - 検証: 両ファイルの目視レビューと相互参照確認。
2. **docs: record Claude Code verification in compatibility matrix**
   - 背景: primary target なのに Verified 欄が `—`。
   - 目的: install / list / invoke を実測し日付入りで記録。
   - 対象: `docs/compatibility.md`, `docs/ja/compatibility.md`。
   - 完了条件: Claude Code 行が ✓ + 日付 + 手順記録。
   - 検証: 記録された手順を第三者 (別セッションの agent) が再実行して同結果。
3. **feat: unify description grammar across all skills**
   - 背景: ユーザー視点/機能視点の混在、他 Skill 参照、keyword 列挙の不統一 (§6)。
   - 目的: `<what> — Use when <trigger>. Not for <anti-trigger>` への統一。
   - 対象: `skills/*/SKILL.md` + `SKILL-ja.md` (24 組), `docs/authoring.md` (+ja) のルール追記, README の Skill 表。
   - 完了条件: 全 description が新文法。近縁 Skill (§6 の 4 ペア) に Not-for 句。`(from scope-request)` 型の参照ゼロ。
   - 検証: 静的チェック (grep) + issue #4 の trigger 評価での前後比較。
4. **feat: add trigger evaluation assets for confusable skill pairs**
   - 背景: invocation を測る評価が存在しない (§7)。
   - 目的: 混同 4 ペア (scope 系 / review 系 / recovery 系 / delegation 系) に should-trigger / should-not-trigger 各 3 プロンプトを定義し、blank-slate で 1 回実行。
   - 対象: `docs/evaluation.md` (+ja), 該当 `skills/*/evals/README.md`。
   - 完了条件: プロンプト定義 + 日付入り実行記録 (未実行項目は "not yet executed" 明記)。
   - 検証: 実行記録の存在と、判定基準が第三者に再現可能であること。
5. **refactor: merge triage-agent-usage and calibrate-ai-learning**
   - 背景: 委任度調整という同一責務の 2 分割 (§4)。
   - 目的: 1 Skill (例: `calibrate-delegation`) へ統合、手動起動前提の設計に。
   - 対象: 当該 2 ディレクトリ、`apm.yml`, `README.md` (+ja), `docs/workflows.md` (+ja)。
   - 完了条件: 新 Skill の SKILL.md/SKILL-ja.md/evals Iter 0、旧 2 Skill の削除と README での告知、lockfile は別 PR。
   - 検証: 旧 evals シナリオの critical 項目が新 Skill で通る。
6. **refactor: absorb diversify-agent-search into break-failure-loop**
   - 背景: 発火困難な独立 Skill より、break-failure-loop からの escalation が自然 (§4, §6)。
   - 目的: 探索多様化の判断基準を break-failure-loop の references/ または本文節へ移す。THIRD_PARTY_NOTICES.md の帰属記載は移動先に合わせ更新。
   - 対象: 当該 2 ディレクトリ、`apm.yml`, README (+ja), workflows (+ja), `THIRD_PARTY_NOTICES.md`。
   - 完了条件・検証: #5 と同型。
7. **refactor: fold scope-implementation into scope-request or design-changes**
   - 背景: scope 3 兄弟の判別困難 (§4)。吸収先は issue #4 の実測で決める。
   - 対象・完了条件・検証: #5 と同型。**#4 完了までブロック**。
8. **docs: add skill taxonomy and placement-boundary page**
   - 背景: 分類が README のフラット表しかない。Skill/AGENTS/dotfiles 境界が暗黙 (§5)。
   - 目的: §5 の分類表と「Never に全域制約を書かない」原則の docs 化。
   - 対象: `docs/` 新規ページ (+ja), `docs/authoring.md` (+ja) からの参照。
   - 完了条件: 全 Skill が一意のカテゴリを持ち、境界原則が authoring ルールに載る。
   - 検証: 新規 Skill 追加のチェックリストからカテゴリ判定に到達できること。

(補助: #8 の後に draft-review-comments の steps 圧縮、lockfile refresh を随時。)

## 15. Handoff prompts for implementation agents

### 最初の 3 タスクと指示プロンプト

**Task 1 → issue #1 (README 互換性文言)**

> mtk177a/skills で README.md と README.ja.md のみを編集してください。現在 "designed for Codex, Claude Code, GitHub Copilot, Gemini CLI" と読める互換性主張を、docs/compatibility.md の検証状態と整合させます: 「Agent Skills 仕様に準拠。検証済みクライアントは docs/compatibility.md を参照。仕様準拠クライアントでは動作が期待できるが未検証」という構造に書き換えてください。Skills 表・インストール手順は変更しないこと。他のファイルは編集しないこと。完了条件: README と compatibility.md の間に矛盾する主張がないこと。

**Task 2 → issue #3 (description 統一)**

> mtk177a/skills の skills/*/SKILL.md 全 23 個の frontmatter description を次の文法に統一してください: `<三人称の動詞句で何をするか> — Use when <観測可能な発火状況>. Not for <近縁 Skill に譲る状況> (近縁がある場合のみ)`。制約: (1) description 内で他 Skill 名を入力の出所として参照しない、(2) 長さは英語 80–160 字目安、(3) scope-request/clarify-request/scope-implementation、review-changes/triage-review-feedback/draft-review-comments、break-failure-loop/diversify-agent-search、triage-agent-usage/calibrate-ai-learning の各ペアには相互の Not-for を必ず入れる、(4) 本文は変更しない、(5) SKILL-ja.md の description と README 両言語の表も同時に更新する。1 Skill = 1 commit とし、着手前に全 24 件の変更案一覧を提示して承認を得ること。

**Task 3 → issue #4 (trigger 評価)**

> mtk177a/skills で docs/evaluation.md に「Trigger evaluation」節を追加し、混同しやすい 4 ペア (scope 系 3 Skill、review 系 3 Skill、recovery 系 2 Skill、delegation 系 2 Skill) それぞれに should-trigger プロンプト 3 本と should-not-trigger プロンプト 3 本を該当 skills/*/evals/README.md に定義してください。その後、リポジトリ文脈を持たない blank-slate subagent に「全 Skill の name+description 一覧+テストプロンプト」だけを渡し、どの Skill を選ぶかを記録、日付入りで evals/README.md に Iter として追記してください。実行できなかった項目は "not yet executed" と明記すること。SKILL.md 本文は変更しないこと。

### 実装後に人間が確認すべき判断点

- Task 1: 互換性の弱め方が過剰でないか (マーケティング的にどこまで言いたいかは所有者の判断)。
- Task 2: 統一文法で失われるニュアンスがないか。特に review-changes の description が Claude Code bundled /code-review との差別化として妥当か。旧 description の方が実際の発火が良いケースは revert する。
- Task 3: 実測で混同が確認されたペアについて、§12 #5–7 の統合をそのまま進めるか、description 改善で足りるかの分岐判断 (これは人間の意思決定事項)。

## 16. Open questions

### 人間 (所有者) が決めるべきこと

1. **このリポジトリの一次顧客は誰か**: 自分の複数環境への配布が主なら統合・削減の自由度は高い。外部利用者の獲得も目的なら、リネーム・統合の deprecation 手順を丁寧にする必要がある。§12 の実行速度に直結する。
2. **TDD 既定・確認必須などの個人ポリシーを dotfiles に移すか**: 移すなら dotfiles 側の受け皿 (global instruction の管理方針) を先に決める必要がある。本レビューでは repo 外の dotfiles を確認できていない。
3. **delegation 系統合 Skill を自動発火させるか手動起動限定にするか**: `disable-model-invocation` は Claude Code 拡張であり、他クライアントでの等価機能は未確認。
4. **本レビュー文書を含む `docs/reviews/` の言語ポリシー**: 本文書は日本語で書いた。英語正本ポリシーに合わせて英訳を正本化するか、レビュー文書は例外とするか。

### 追加調査が必要なこと

5. agentskills.io 仕様本文の一次確認 (今回 403 で取得不能)。`name`/`description` の制約と optional フィールドの正式定義。
6. `SKILL-ja.md` の frontmatter が各クライアントの discovery で二重登録を起こすか (Claude Code 以外)。
7. `gh skill` / `npx skills add` でのこのリポジトリの実際の挙動。

### 今回のレビューで判断不能だったこと

8. **各 Skill の実際の発火頻度・有効性**: 使用ログが存在しないため、「発火しづらい」等の指摘はすべて構造からの推論である。trigger 評価 (#4) が最初の実データになる。
9. **scope-implementation の吸収先** (scope-request か design-changes か): 実測なしでは決められないため、§12 で #4 の後ろに置いた。
10. **review-changes と Claude Code bundled /code-review の実際の競合挙動**: bundled skill の選好は Claude Code のバージョン・文脈に依存し、今回の静的監査では観測できない。
