---
name: audit-agent-guidance
description: AGENTS.md、CLAUDE.md、SKILL.md、エージェント向け参照資料などの永続的な agent guidance を、期待する挙動、観測済みの利用状況、client の意味論、評価証拠に照らして監査する。改訂前に guidance のスコープ、優先順位、trigger conflict、安全境界、context cost、systemic failure を診断するときに使う。通常のコードレビュー、新規 Skill の作成、standalone の Codex `.rules` policy review には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Audit Agent Guidance

## 目的

- 永続的な agent guidance が期待する挙動を生むかを診断し、成功または失敗の理由を説明する。
- 「agent guidance」を、永続的な指示、再利用可能な workflow、エージェント向け参照資料の総称として扱う。
- 単一の既存 Skill と、複数 surface にまたがる guidance system の両方を監査する。
- 現在の成果物や文書分割を正しいと前提にせず、期待する結果から始める。

## 証拠とスコープ

- 対象ファイルを挙げる前に、期待する挙動、失敗シグナル、利用者、client、model を定義する。
- 観測した証拠、妥当な推論、前提、未確認事項を区別する。
- 関連する指示文書、Skills、参照資料、policy files、client 設定、配布 metadata を発見する。重要な場合は、その権限、スコープ、読み込み順、優先順位、trigger、共存関係、permission、配布経路を記録する。
- loading、precedence、approval、Skill discovery の挙動が診断に影響し、リポジトリ内の一次情報で確定できない場合は、client の最新の公式仕様を確認する。
- 文面上の妥当性より trace、実行結果、eval、利用履歴を優先する。行動証拠がなければ静的監査と明示し、挙動を未確認のまま残す。

## Workflow

1. 成果物名に触れる前に、期待する挙動、失敗シグナル、影響を受ける利用者、関連する client と model を定義する。
2. 問題を捉え直し、暗黙の前提と別レイヤーの原因候補を明らかにする。現在の guidance を維持、削除、移動、統合、置換する反事実を検討する。
3. 関連する guidance surface、権限と permission の境界、読み込みと precedence の規則、trigger、共存時の挙動、配布経路を発見する。診断へ実質的に影響する場合は、client の最新の公式仕様を確認する。
4. trace、実行結果、eval、利用履歴などの行動証拠を集める。存在しない場合は静的監査であることと、挙動の影響が未確認であることを明示する。
5. 症状と根本原因を分け、監査で裏付けられた重要な finding をすべて報告する。根拠のない件数上限を設けない。
6. 各 finding に evidence、impact、confidence、影響 surface、反証または検証方法を付ける。重要度と確信度は別軸として扱う。
7. 局所修正と構造的解決策を比較する。必要な安全特性を維持し、guardrail を置き換える場合は同等以上の保護を検証する。診断の完全性と rollout の段階性を分ける。
8. 必要に応じて current guidance、no guidance、candidate を、単独時と隣接 surface との共存時で比較し、推奨案を検証可能にする。

## 評価軸

期待する挙動に関係する評価軸を使う。固定の優先順位は設けない。

- **Outcome alignment:** guidance が望む挙動と失敗時の処理を生むか
- **Authority / precedence:** authoritative source、override、conflict が意図どおり解決されるか
- **Surface fit:** 各指示が target client と利用者に実際に読み込まれ、理解される surface にあるか
- **Triggering / coexistence:** 関連する Skill や指示が正確に起動し、共存時にも正しく機能するか
- **Correctness / freshness:** 記述と client semantics が正確で最新か
- **Safety / integrity:** 必要な保護が曖昧さ、競合、置換、迂回を経ても維持されるか
- **Context cost:** 常時読み込みまたは trigger 時に読み込む内容が注意と token のコストに見合うか
- **Portability:** 未対応の client、model、環境、path の前提が明示されているか
- **Maintainability:** ownership、重複、coupling、変更経路を理解できるか
- **Observability / evalability:** 実際の挙動を trace し、比較し、現実的な証拠で反証できるか

## 報告契約

固定見出しを強制せず、監査に適した構成を選ぶ。次の情報を含める。

- 結論と監査範囲
- 確認済み evidence と未確認事項
- findings とその根本原因
- 現状維持や削除も含む代替案と trade-off
- 推奨案、段階的 rollout、検証方法

現在の guidance が妥当だと証拠が示す場合、変更を無理に提案しない。

## 境界

- 既存の durable guidance を診断する。新規 Skill の設計には `design-skill`、新規指示文書群の設計には `design-agent-instructions`、通常の diff review には `review-changes` を使う。
- standalone の Codex `.rules` command-policy review は対象外とする。より広い guidance system の approval 挙動へ影響する場合だけ、`.rules` を関連 surface に含める。
- 監査は read-only を既定とする。ユーザーの依頼が変更を許可し、対象環境の適用 policy が認める場合だけ編集する。配布 Skill 内で普遍的な追加 approval gate を作らない。
- 特定のファイル、見出し、`Never` section がないことだけを、期待する挙動との関係を示さず欠陥と扱わない。
- 局所修正が構造的変更より安全だと前提にしない。必要な安全特性と rollout risk に照らして両方を評価する。
