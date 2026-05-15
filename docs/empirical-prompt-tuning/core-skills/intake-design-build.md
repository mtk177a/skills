# Integration Regression Eval: Intake -> Design -> Build

この文書は、mizchi 側の外部 skill `empirical-prompt-tuning` の手順を、この repo の `intake`, `design`, `build` に適用するための統合回帰 eval メモです。

日常の改善は各 skill の `evals/` で行い、この文書は複数 skill をつないだときの受け渡し崩れや統合時の退行を確認する用途に使います。

対象 skill:

- `skills/intake/SKILL.md`
- `skills/design/SKILL.md`
- `skills/build/SKILL.md`

## Iter 0: Static Review

- `intake`: 目的、完了条件、制約はあるが、`design` に渡す必須情報の最低セットが明文化されていない。
- `design`: 変更対象、リスク、テスト戦略はあるが、`build` に渡す実装単位と停止条件の粒度がやや曖昧。
- `build`: TDD 方針は明確だが、テストを実行できない場合の扱い、Red の確認結果の表現、検証への引き継ぎ粒度が薄い。

## Scenarios

### Scenario A: Median

既存 CLI ツールに小さな振る舞い追加をしたい。依頼文は 2-3 文だけで、目的はあるが完了条件と制約は十分に書かれていない。repo には既存テストがあり、テストコマンドも 1 つ分かっている。executor には、依頼整理、設計方針、最初の TDD 実装方針までを出させる。

Requirements checklist:

1. [critical] `intake` と `design` の出力を分けたまま、`build` に入る前の完了条件と対象範囲を明示する
2. `design` で変更対象と変更対象外を分離する
3. `build` で最初の 1 テストと Red -> Green -> Refactor の現在地を示す
4. 未解決事項または承認待ち事項があれば、実装前に止める条件として明示する

### Scenario B: Edge

依頼は機能追加だが、外部依存追加の可能性と仕様未確定の部分がある。既存テストは不十分で、どのコマンドを使うかも完全には分からない。executor には、無理に実装へ進まず、停止条件と追加確認点を含む形で `intake`、`design`、`build` の出力を作らせる。

Requirements checklist:

1. [critical] 依存追加や仕様未確定を `Ask first` の停止条件として扱う
2. `intake` で未解決事項と前提を分離する
3. `design` でリスクと回避策を対にして書く
4. `build` でテスト実行不能または不明な前提を隠さず、次の一手を確認行為に寄せる

## Metrics To Record

| Scenario | Success/Failure | Accuracy | `tool_uses` | `duration_ms` | retries | Weak phase |
|---|---|---|---|---|---|---|
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |

## Iteration 1

### Changes (diff from previous)

- 初回実行。skill 本文は Iter 0 のまま。
- Pattern applied: `(baseline)`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| A | ○ | 100% | N/A | N/A | 0 | — |
| B | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Scenario B: [critical] drop なし
  - Issue: `build` は本来実装用スキルだが、今回はコード変更禁止かつ停止条件付き deliverable が要求され、停止時の表現が曖昧だった
  - Cause: `build` が Red 開始前提で書かれており、着手条件未充足時の phase と出力項目が定義されていなかった
  - General Fix Rule: 実装系スキルには、着手条件未充足時に `Blocked` として止まる分岐と、そのときの出力項目を明示する
- Scenario A: [critical] drop なし
  - Issue: JSON 追加のような曖昧な依頼では、対象範囲や最小仕様が入力不足のまま `build` に渡る
  - Cause: 上流で未確定要件は拾えているが、`build` に入れる条件と入れない条件が skill 間で固定されていなかった
  - General Fix Rule: `design` から `build` へ、着手条件、対象範囲、停止条件を固定項目として受け渡す

### Discretionary fill-ins (newly surfaced this time)

- Scenario B: `現在のフェーズ` を補うため `Done` と書いたうえで「未着手で停止」と注記した
- Scenario A: `--json` の初回スコープを「成功系 1 コマンド」に限定し、JSON 比較方法を parse 後比較へ寄せた

### Ledger updates

- Re-seen: `missing handoff contract between adjacent skills` - `design` から `build` へ渡す固定項目が不足していた
- Added: `blocked phase missing before Red` - Red 開始前提が欠ける場面で `build` の phase 表現が曖昧になる

### Next fix proposal

- `design` に `build` へ渡す着手条件 / 対象範囲 / 停止条件を足し、`build` に `Blocked` phase と未着手時の出力分岐を追加する

(Convergence check: 0 consecutive clears / 2 rounds remaining to stop condition)

## Iteration 2

### Changes (diff from previous)

- `design` に `build` に渡す着手条件、対象範囲、停止条件を追加
- `build` に着手条件確認ステップ、`Blocked` phase、未着手時の停止出力を追加
- Pattern applied: `blocked phase missing before Red`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| A | ○ | 100% | N/A | N/A | 0 | — |
| B | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Scenario A: [critical] drop なし
  - Issue: 依頼文だけでは対象コマンド範囲と JSON 仕様が確定できない
  - Cause: skill 側の ambiguity ではなく、scenario 側が intentionally incomplete なため
  - General Fix Rule: 曖昧な機能追加依頼では、実装前に「対象範囲」「成功系の最小仕様」「非互換にしない条件」を確認し、未確定なら `build` を `Blocked` で止める
- Scenario B: [critical] drop なし
  - Issue: テストコマンド不明でも確認方針を出す必要がある
  - Cause: skill 側は十分で、残りは scenario 上の情報不足
  - General Fix Rule: 実行不能なテストは推測で埋めず、確認タスクへ落とし直す

### Discretionary fill-ins (newly surfaced this time)

- Scenario A: 単一コマンドから始める前提、成功系のみを初回対象にする前提を補った
- Scenario B: 既存コード未確認のためモジュール境界を仮置きとした

### Ledger updates

- Re-seen: `missing handoff contract between adjacent skills` - Iter 2 では handoff 不足そのものは再発せず、fix が効いた
- Re-seen: `blocked phase missing before Red` - Iter 2 では再発せず、`Blocked` 表現に置き換わった

### Next fix proposal

- `intake` に「機能追加依頼で実装前に最低限確認すべき仕様粒度」の例を追加するかを hold-out scenario 後に判断する

(Convergence check: 1 consecutive clears / 1 round remaining to stop condition)

## Iteration 3 (Hold-out)

### Changes (diff from previous)

- skill 本文の追加修正なし
- hold-out scenario を追加して、既存 scenario への過剰適応がないか確認
- Pattern applied: `(hold-out check)`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| Hold-out | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Hold-out: [critical] drop なし
  - Issue: 実コードや既存 CLI 構造を見ずに、`build` の具体的な変更ファイル名までは確定できなかった
  - Cause: scenario が deliverable のみを求めており、対象 skill も実装前整理を主眼としていたため
  - General Fix Rule: 実装非着手の評価では、コード構造未確認の事項は推測で埋めず、未確定として明示しつつ着手条件へ戻す

### Discretionary fill-ins (newly surfaced this time)

- Hold-out: `--format compact` の既定値や help 文言は未確定事項として残し、列順承認待ちを `Blocked` で表現した

### Ledger updates

- Re-seen: `missing handoff contract between adjacent skills` - 再発なし。`design` から `build` への handoff は hold-out でも維持された
- Re-seen: `blocked phase missing before Red` - 再発なし。承認待ちケースでも `Blocked` と `Red` を混同しなかった

### Next fix proposal

- 現時点では skill 本文の追加修正は不要。次に着手するなら `intake` の例示追加ではなく、別 flow の hold-out を増やす

(Convergence check: 2 consecutive clears / stop condition reached for current scenario set)

## Failure Ledger Seed

- **Pattern name**: missing handoff contract between adjacent skills
  - Example: `design` の出力は出たが、`build` が何を固定情報として受け取る前提か分からない
  - General Fix Rule: 隣接 skill に渡す必須項目を、手順と出力フォーマットの両方に明記する
  - Seen in: iter 0
- **Pattern name**: TDD rhythm stated without observable checkpoints
  - Example: Red を守る方針はあるが、何をもって Red を確認したとみなすかが曖昧
  - General Fix Rule: プロセス宣言だけでなく、観測可能な中間出力を指定する
  - Seen in: iter 0

## First Fix Themes

1. `intake` -> `design` -> `build` の受け渡し必須項目を明文化する
2. `build` の Red 確認結果とテスト不能時の扱いを補強する
3. 停止条件と承認待ち条件を `Always` / `Ask first` に寄せて早めに見える位置へ出す
