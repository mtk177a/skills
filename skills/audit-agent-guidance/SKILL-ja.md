---
name: audit-agent-guidance
description: AGENTS.md、CLAUDE.md、SKILL.md、エージェント向け参照資料などの永続的な agent guidance を、期待する挙動、観測済みの利用状況、client の意味論、評価証拠に照らして監査する。改訂前に guidance のスコープ、優先順位、trigger conflict、安全性または第三者 trust boundary、context cost、systemic failure を診断するときに使う。通常の code / script vulnerability review、新規 Skill の作成、standalone の Codex `.rules` policy review には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Audit Agent Guidance

## 目的

- 永続的な agent guidance が期待する挙動を生むかを診断し、成功または失敗の理由を説明する。
- 「agent guidance」を、永続的な指示、再利用可能な workflow、エージェント向け参照資料の総称として扱う。
- 単一の既存 Skill と、複数 surface にまたがる guidance system の両方を監査する。
- current artifact を確認する前に期待する挙動を1文で述べ、現在の成果物や文書分割を正しいと前提にしない。

## 証拠とスコープ

- 対象ファイルを挙げる前に、期待する挙動、失敗シグナル、利用者、client、model を定義する。
- 観測した証拠、妥当な推論、前提、未確認事項を区別する。
- 関連する指示文書、Skills、参照資料、policy files、client 設定、配布 metadata を発見する。重要な場合は、その権限、スコープ、読み込み順、優先順位、trigger、共存関係、permission、配布経路を記録する。
- 第三者 content または executable capability が関係する場合は、配布する全ファイルと直接参照する全ファイル、provenance、実際の remote destination、scripts、dependencies、tools、filesystem / network access、外部へ出られる data flow を列挙する。個別 permission ではなく、組み合わさった capability chain を評価する。
- loading、precedence、approval、Skill discovery の挙動が診断に影響し、リポジトリ内の一次情報で確定できない場合は、client の最新の公式仕様を確認する。
- 文面上の妥当性より trace、実行結果、eval、利用履歴を優先する。行動証拠がなければ静的監査と明示し、挙動を未確認のまま残す。
- 評価を広げる前に、重要な guidance の claim または変更案を、起こり得る失敗、それを露出できるシナリオまたは確認、採点方法へ対応付ける。scenario 件数と反復は、判断に関係する evidence を増やす場合にだけ使う。

## Workflow

1. 期待する挙動を1文で書き、その後、成果物名に触れる前に失敗シグナル、影響を受ける利用者、関連する client と model を定義する。
2. 問題を捉え直し、暗黙の前提と別レイヤーの原因候補を明らかにする。現在の guidance を維持、削除、移動、統合、置換する反事実を検討する。
3. 関連する guidance surface、権限と permission の境界、読み込みと precedence の規則、trigger、共存時の挙動、配布経路を発見する。第三者または executable Skill では、provenance、外部指示と redirect、commands と tools、data access、outbound destination、capability chain 全体を制約する control を追跡する。診断へ実質的に影響する場合は、client の最新の公式仕様を確認する。
4. trace、実行結果、eval、利用履歴などの行動証拠を集める。存在しない場合は静的監査であることと、挙動の影響が未確認であることを明示する。
5. 症状と根本原因を分け、監査で裏付けられた重要な finding をすべて報告する。根拠のない件数上限を設けない。
6. すべての material finding に完全な record を使い、evidence、impact、confidence、影響 surface、反証または検証方法を付ける。項目を暗黙にしたり、まとめの validation section だけへ置いたりしない。重要度と確信度は別軸として扱う。
7. 局所修正と構造的解決策を比較する。必要な安全特性を維持し、guardrail を置き換える場合は同等以上の保護を検証する。診断の完全性と rollout の段階性を分ける。
8. risk と不確実性に比例した評価で、推奨案を検証可能にする。current guidance、no guidance、candidate の単独時または共存時の比較は、その条件が重要な失敗を区別できる場合にだけ行う。

## 評価軸

期待する挙動に関係する評価軸を使う。固定の優先順位は設けない。

- **Outcome alignment:** guidance が望む挙動と失敗時の処理を生むか
- **Authority / precedence:** authoritative source、override、conflict が意図どおり解決されるか
- **Surface fit:** 各指示が target client と利用者に実際に読み込まれ、理解される surface にあるか
- **Triggering / coexistence:** 関連する Skill や指示が正確に起動し、共存時にも正しく機能するか
- **Correctness / freshness:** 記述と client semantics が正確で最新か
- **Safety / integrity:** 必要な保護が曖昧さ、競合、置換、迂回、信頼できない外部指示、data access と outbound capability の組み合わせを経ても維持されるか
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
- 推奨案と検証方法、および変更を推奨する場合の段階的 rollout

第三者または executable Skill の finding では、trust boundary、関係する capability と data path、destination、deterministic control または不足している control を特定する。複合 risk を、個別には許容可能な permission の一覧へ分解して弱めない。

現在の guidance が妥当だと証拠が示す場合、変更を無理に提案しない。

## 境界

- 既存の durable guidance を診断する。新規または大幅に scope を変える Skill の設計には `design-skill`、新規 instruction set または診断後の再編には `design-agent-instructions`、通常の diff review には `review-changes` を使う。
- script と tool の挙動が Skill の instruction、trust、data-flow boundary を構成する場合は監査へ含める。単独の implementation vulnerability review は、適切な code または security review workflow へ回し、この audit を一般的な code analysis へ拡張しない。
- standalone の Codex `.rules` command-policy review は対象外とする。より広い guidance system の approval 挙動へ影響する場合だけ、`.rules` を関連 surface に含める。
- 監査は read-only を既定とする。ユーザーの依頼が変更を許可し、対象環境の適用 policy が認める場合だけ編集する。配布 Skill 内で普遍的な追加 approval gate を作らない。
- 特定のファイル、見出し、`Never` section がないことだけを、期待する挙動との関係を示さず欠陥と扱わない。
- 局所修正が構造的変更より安全だと前提にしない。必要な安全特性と rollout risk に照らして両方を評価する。
- 固定の finding 数、scenario 数、run 数を完全性の証拠として扱わない。重要な claim と失敗境界が被覆され、追加 evidence が判断を変えない時点で止める。
