# author-skill evals

`author-skill` の単体運用を評価するためのメモです。新しい Skill の設計・起草や既存 Skill の大きな再設計を、既存ルールとの整合を保って提案できるかを見ます。

## Iter 0

- `description` と本文が「Skill の設計・起草」に揃っているか
- `skills/README.md` と `docs/skill-authoring.md` を一次情報として扱う前提が伝わるか
- 既存 Skill との重複確認、境界定義、補助ディレクトリ判断まで単体で回せるか
- 一般ガイドの再掲ではなく、提案組み立て Skill として機能するか

## Scenarios

### Scenario A: 新規 Skill の起草提案

ユーザーが新しい Skill を追加したいが、`name`、`description`、境界、補助ディレクトリの要否が未整理。executor には、一次情報を前提に提案の骨子をまとめ、承認前提の差分提案まで整理させる。

Requirements checklist:

1. [critical] 一次情報、重複確認、`name` / `description`、境界を含む提案になっている
2. `description` が利用場面ベースで書かれる
3. 補助ディレクトリの要否を理由付きで触れる
4. 承認前に大きな変更を実行しない

### Scenario B: 既存 Skill との重複を含む再設計提案

作りたい Skill が既存 2 Skill と部分的に役割重複しており、統合するか別 Skill にするか迷う。executor には、競合や統合候補を整理し、影響範囲と最小差分の方針を返させる。

Requirements checklist:

1. [critical] 既存 Skill との重複や統合候補を明示する
2. 最小差分で進める方針を出す
3. `AGENTS.md` / docs / scripts / `apm.yml` の影響範囲を必要に応じて挙げる
4. 一般論の長い再掲ではなく、提案時の判断材料に集中する

## Failure Ledger Seed

- `authoring guidance repeated without proposal framing`
- `overlap check omitted or shallow`
- `metadata proposed without trigger-oriented description`

## Iteration 1

### Changes (diff from previous)

- 初回実行。Skill 本文は Iter 0 のまま。
- Pattern applied: `(baseline)`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| A | × | 87.5% | N/A | N/A | 0 | Understanding |
| B | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Scenario A: [critical] drop なし
  - Issue: 新規 Skill の利用場面が抽象的だと、`name` を確定せず仮称で止める判断が本文前半からはやや読み取りにくい。
  - Cause: 一次情報確認と重複確認は明確だが、抽象依頼時の停止条件が `name` 決定手順より後ろにある。
  - General Fix Rule: 抽象入力を扱う authoring Skill では、利用場面を 1 文で固定してから命名する順序を早めに明示する。
- Scenario B: [critical] drop なし
  - Issue: 重複候補の整理はできたが、どの出力契約なら既存 Skill へ寄せるかの判断軸は補足推論に少し依存した。
  - Cause: 本文は重複確認を要求している一方、既存 Skill へ吸収する基準までは例示していない。
  - General Fix Rule: overlap handling を扱う Skill では、既存 Skill へ寄せる判断軸を短く例示する。

### Discretionary fill-ins (newly surfaced this time)

- Scenario A: 目的文が未確定なら仮称で止める、という運用を補って実行された。
- Scenario B: `design` と `scoped-implementation-plan` のどちらへ寄せるかは、出力契約ベースで補って判断された。

### Ledger updates

- Re-seen: `metadata proposed without trigger-oriented description` - 仮 `description` で補われたが、抽象依頼では確定しきれなかった
- Added: `abstract request reaches naming step too early`

### Next fix proposal

- `使う場面` と `手順` に、抽象依頼では利用場面を 1 文に固定し、責務境界が未確定なら仮称で止める旨を前倒しする

(Convergence check: 0 consecutive clears / 2 rounds remaining to stop condition)
