# Integration Regression Eval: Code Review -> Triage Review -> Validate Fix

この文書は、mizchi 側の外部 Skill `empirical-prompt-tuning` の手順を、このリポジトリの `code-review`, `triage-review`, `validate-fix` に適用するための統合回帰 eval メモです。

日常の改善は各 Skill の `evals/` で行い、この文書は複数 Skill をつないだときの判断写像や確認漏れの退行を確認する用途に使います。

対象 Skill:

- `skills/code-review/SKILL.md`
- `skills/triage-review/SKILL.md`
- `skills/validate-fix/SKILL.md`

## Iter 0: Static Review

- `code-review`: レビュー観点は厚いが、`triage-review` に渡すべき最小情報が明文化されていない。
- `triage-review`: 採用、保留、却下の判断はあるが、優先順位と実装可能な対応方針の粒度が揃っていない。
- `validate-fix`: 確認済み / 未確認 / リスクの分離はあるが、レビュー指摘との対応関係と Done 判断の境界が薄い。

## Scenarios

### Scenario A: Median

小さな修正差分に対して新規レビューを行い、その後レビュー指摘の採否を整理し、修正後の確認結果をまとめる。指摘は 2-3 件で、Must-fix と Should-fix が混ざる。executor には、レビュー、採否判断、確認結果を混ぜずに分離して出力させる。

Requirements checklist:

1. [critical] `code-review` の Must-fix / Should-fix / Nice-to-have を `triage-review` で採用、保留、却下へ変換し、その理由を残す
2. `code-review` の各指摘に根拠がある
3. `triage-review` で採用した指摘に優先順位または対応方針がある
4. `validate-fix` で確認済み、未確認、残るリスクを分離する

### Scenario B: Edge

レビュー指摘の一部が仕様論を含み、すぐには採否を決められない。修正後もテスト未実施範囲が残る。executor には、無理に全部採用せず、保留と追加確認を明示したうえで、`validate-fix` で未確認事項を伏せずに残させる。

Requirements checklist:

1. [critical] 仕様判断が必要な指摘は `triage-review` で保留または追加確認に回し、自動採用しない
2. `code-review` が仕様不一致や安全性の観点を優先して扱う
3. `validate-fix` が未実施範囲を Done 扱いにしない
4. 最終出力で残留リスクと次の一手が読み取れる

## Metrics To Record

| Scenario | Success/Failure | Accuracy | `tool_uses` | `duration_ms` | retries | Weak phase |
|---|---|---|---|---|---|---|
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |

## Iteration 1

### Changes (diff from previous)

- 初回実行。Skill 本文は Iter 0 のまま。
- Pattern applied: `(baseline)`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| A | ○ | 100% | N/A | N/A | 0 | — |
| B | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Scenario A: [critical] drop なし
  - Issue: `validate-fix` は本来「修正後確認」だが、scenario では実修正差分ではなく「既存差分 + 実施済み確認事実」だけが与えられた
  - Cause: Skill 側の致命的な ambiguity というより、flow 評価の都合で `validate-fix` を前倒しで読ませている
  - General Fix Rule: 修正実体がない状態で `validate-fix` を使う場合は、確認対象を「提示済み差分と実施済み確認事実」に限定し、採用指摘の解消は未確認として明示する
- Scenario B: [critical] drop なし
  - Issue: 仕様変更の可能性がある指摘と、安全性リスクの指摘が同時に存在した
  - Cause: `triage-review` の境界が効いており、仕様論点は保留、安全性論点は採用として切り分けられた
  - General Fix Rule: 仕様変更を含むレビュー指摘は、安全性バグと分離し、採用前に期待挙動と互換性確認を必須にする

### Discretionary fill-ins (newly surfaced this time)

- Scenario A: `Nice-to-have` を要件上の triage ラベルへ合わせるため `保留` に寄せた
- Scenario B: 成功系 1 回の目視確認を、安全性や仕様妥当性の根拠には使わず限定的な確認結果として扱った

### Ledger updates

- Re-seen: `severity classification does not map to triage decisions` - 今回は再発せず、Must/Should/Nice-to-have から採用/保留への変換は通った
- Re-seen: `validation detached from review intent` - 顕在化はしたが、Skill 補完ではなく scenario 側の制約として処理できた

### Next fix proposal

- すぐに Skill 本文は変えず、hold-out scenario で `validate-fix` が元指摘との対応付けを保てるかを追加確認する

(Convergence check: 1 consecutive clears / 1 round remaining to stop condition)

## Iteration 2 (Hold-out)

### Changes (diff from previous)

- Skill 本文の追加修正なし
- hold-out scenario を追加して、Must-fix が 0 件のときも triage と validate の対応関係が崩れないか確認
- Pattern applied: `(hold-out check)`

### Execution results (per scenario)

| Scenario | Success/Failure | Accuracy | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|---|
| Hold-out | ○ | 100% | N/A | N/A | 0 | — |

`spawn_agent` / `wait_agent` では `tool_uses` と `duration_ms` を取得できなかったため、この iteration の steps / duration は未記録。

### Structured reflection (newly surfaced this time)

- Hold-out: [critical] drop なし
  - Issue: `label` が両名未設定時に空文字になるが、それが仕様か不明なまま差分だけでは確定できない
  - Cause: 関連仕様が scenario に与えられておらず、Skill も未確認事項を未確認のまま残すことを要求しているため
  - General Fix Rule: 仕様依存のレビュー論点は、重大度を下げてもよいが、既知の未確認事項として明示し、採否判断と検証項目に接続する

### Discretionary fill-ins (newly surfaced this time)

- Hold-out: `nickname` 追加は任意改善という補足を優先し、Must-fix に引き上げず Nice-to-have 扱いに寄せた

### Ledger updates

- Re-seen: `severity classification does not map to triage decisions` - 再発なし。Must-fix 不在でも採用/保留整理を維持できた
- Re-seen: `validation detached from review intent` - 再発なし。元指摘と未確認事項の対応関係を hold-out でも保てた

### Next fix proposal

- 現時点では Skill 本文の追加修正は不要。次に着手するなら、実修正後の validate を含む別種 scenario を増やす

(Convergence check: 2 consecutive clears / stop condition reached for current scenario set)

## Failure Ledger Seed

- **Pattern name**: severity classification does not map to triage decisions
  - Example: Must-fix と採用の関係は見えるが、Should-fix / Nice-to-have が triage 上どう扱われるかが曖昧
  - General Fix Rule: 前段の分類を後段の判断ラベルへどう写像するかを明文化する
  - Seen in: iter 0
- **Pattern name**: validation detached from review intent
  - Example: 修正後確認の結果はあるが、どの指摘が解消されたのか結びつかない
  - General Fix Rule: `validate-fix` に、元の指摘または対応方針との対応付けを求める
  - Seen in: iter 0

## First Fix Themes

1. `code-review` -> `triage-review` の受け渡し項目と判断写像を明文化する
2. `triage-review` の採用時フォーマットに優先順位と対応方針を固定項目として入れる
3. `validate-fix` に、解消した指摘 / 未解消の指摘 / 未確認範囲の切り分けを足す
