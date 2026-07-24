> **注記:** 英語版 (`docs/evaluation.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill の評価

このドキュメントは、このリポジトリの Skill に使用する評価アプローチを説明します。

## 評価原則

評価規模は、普遍的なケース数ではなく、挙動の被覆から決めます。

シナリオを追加または削除する前に、簡潔な coverage map を作ります。

| Skill の claim または変更 | 起こり得る失敗 | シナリオまたは確認 | 採点方法 |
| --- | --- | --- | --- |
| `<主張する挙動>` | `<観測可能な失敗>` | `<入力と環境>` | `<deterministic check、rubric、reviewer>` |

重要な責務、変更した挙動、既知の regression、関連する境界がすべて観測可能な形で失敗でき、残した各シナリオが固有のリスクを担うなら、suite は十分です。目標件数へ合わせるためにシナリオを増やしたり、上限内に収めるためだけに削ったりしません。

公式 guidance では、3件または3–5件のシナリオが例や組織的な出発点として示されることがあります。このリポジトリでは、その数を普遍的な最小値・最大値として扱いません。

## 評価の深さを選ぶ

現在の不確実性を解消できる最も低コストな段階を使います。

1. **Static validation:** すべての Skill 変更で使います。metadata、内部整合、自己完結性、参照、境界、出力契約を確認します。
2. **Targeted behavioral regression:** 指示、trigger、共存、安全挙動、出力要件が変わる場合に使います。影響を受けるリスクと隣接リスクを担うシナリオだけを実行します。
3. **Empirical prompt tuning:** 観測済みの失敗、高い影響、不安定な挙動、大幅な再設計により反復証拠のコストが正当化される場合に、baseline/candidate の反復比較を使います。

static check は runtime の挙動を証明しません。targeted regression は、未検証の client や model での挙動を証明しません。suite を機械的に広げず、その限界を明示します。

## Skill ごとの評価資産

各 Skill は `evals/` ディレクトリを持ちます。README は必須です。反復評価の再現性を高める場合は、任意の構造化資産を追加します。

```text
skills/<skill-name>/
└── evals/
    ├── README.md       # 目的、手順、結果要約、振り返り
    ├── triggers.json   # 任意の trigger、non-trigger、near-miss ケース
    ├── evals.json      # 任意の実課題、入力、assertion、baseline 条件
    └── results.json    # 現在採用中の revision に対する任意の簡潔な evidence record
```

この構造へ合わせるためだけに、既存 Skill を一括移行しません。他の Skill は、それぞれを次に大幅改訂するときに構造化資産へ移行できます。

## 評価資産の責務

### evals/README.md

人が読む評価契約と結果の要約を保持します。

- 目的と期待する挙動
- 実行手順と環境
- 静的確認とシナリオの概要
- 結果、失敗、未実行項目の要約
- iteration の記録と次の検証課題

見出しは固定しません。README を raw evidence の代用にせず、raw trace を埋め込みません。

### evals/triggers.json

次の再利用可能なケースを置く任意資産です。

- `should-trigger`
- `should-not-trigger`
- 対象責務に似ているが別の workflow に属する near-miss
- 実行回数、observability 規則、合格基準

trigger ケースは、実際の責務境界と起こり得る誤起動から選びます。隣接 Skill や似た依頼が合理的に競合し得る場合は near-miss が有用です。無関係な negative case は任意の control であり、必須被覆ではありません。

普遍的な反復回数や合格閾値は使いません。確率的な変動、予期しない結果、model 差、誤起動の影響により追加観測が判断を変え得る場合に反復します。固定回数を cost-bounded smoke test として使う場合は理由を記録し、統計的保証として扱いません。

client が公開する evidence だけを trigger 判定に使います。Skill load が観測できない場合は `not exposed` と記録し、出力の文面から load event を推測しません。

### evals/evals.json

次を置く任意資産です。

- 現実的な課題と入力
- 行動 assertion と critical requirement
- baseline 条件
- isolation と coexistence の構成

期待する答えを課題文へ埋め込まず、判断の誤りを露出できるだけの現実性を持たせます。executor の入力と採点基準を分離します。実際のユーザーが提供する証拠はシナリオに含められますが、採点を容易にするためだけに期待する finding や結論を名指ししません。

### evals/results.json

README の集計だけでは、一時 artifact の削除後に実行済み revision を監査できない場合に、この任意 asset を使います。次を記録します:

- 変更されない baseline commit または content hash と candidate file hash
- client、model、reasoning、date、正規化した invocation、判定集約 policy
- baseline/candidate の verdict と根拠を含む簡潔な case-by-requirement matrix
- 観測可能な trigger result、deterministic fixture check、未確認事項

raw trace、完全な response、credential、環境固有の absolute path はこのファイルへ保存しません。対応する README の結果要約から link します。

`results.json` は、現在採用中の Skill revision に対する簡潔な evidence として扱います。実行ごとに日付付きファイルを追加せず、同じ candidate の再実行や修正結果を1つの record へ統合して更新します。過去に採用した result は、評価対象の Skill source とともに Git 履歴で保持します。

採用中の Skill source が変わった場合は、`results.json` を更新するか、影響を受ける evidence を superseded または unverified と明示するか、ファイルを削除します。古い candidate が現行 source であると誤解させる hash や pass claim を残しません。以前の evidence を再利用する場合は、変更されていない requirement と評価済み content を明示的に特定できることを条件とします。

現在の判断に引き続き必要で、Git 履歴だけでは不十分な場合に限り、過去の result を別名で保持します。たとえば、比較不能な client または評価方式、直接再現できる状態を保つ必要がある既知の regression、外部監査要件です。その目的と削除条件を README に記録します。固定件数に合わせて result file を保持または削除しません。

## evals/README.md の構成例

```markdown
# <skill-name> evals

## Iter 0 — Static check

- description と本文が内部的に一致している
- 出力フォーマットが定義されているか明確に示されている
- Skill が自己完結している
- material claim と critical requirement が特定されている

## Coverage map

| Claim | Failure | Scenario | Grader |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## Scenarios

### Scenario A: <タイトル>

<1文のコンテキスト>

Requirements checklist:
1. [critical] <違反時に scenario を fail とする要件>
2. <その他の要件>

## Failure Pattern Ledger

- `<既知の失敗パターン>`

## Iter N — YYYY-MM-DD

### Changes

- <前回からの変更内容>

### Execution results

| Scenario | Result | Evidence | Weak phase |
| --- | --- | --- | --- |
| A | pass / fail / unstable | ... | — |

### Next validation question

- <次の実行で判断が変わり得る問い>
```

## 評価の実施方法

このリポジトリに共通の `/eval` command や必須の外部 framework はありません。各 runnable suite で使った正確な command、script、client workflow、manual procedure を記録します。反復実行の再現性が実質的に上がる場合だけ wrapper を追加します。

behavioral evaluation は blank-slate executor で実行します。リポジトリの履歴を持たず、シナリオに必要な Skill と入力だけを受け取る agent または client session です。

**Blank-slate executor protocol:**

1. リポジトリ context を持たない新しい executor を起動する
2. `SKILL.md`、許可した補助ファイル、シナリオ入力、必要な環境を渡す
3. 非公開 assertion、期待結論、grader note を executor の入力へ含めない
4. executor 自身に pass/fail を宣言させず、結果と公開された trace を取得する
5. 適用される各 requirement を採点し、判定根拠を記録する

次の両方を、関連する場合に評価します。

- **Isolation:** 不足を隠しうる隣接 Skill を有効にせず、対象 Skill を単独で評価する
- **Coexistence:** 起こり得る trigger、authority、workflow の競合がある場合に、隣接 Skill や instruction surface と一緒に評価する

観測できない項目は `not exposed`、実行しなかった項目は `not executed` と記録します。どちらも合格として扱いません。

客観的な結果には deterministic check を優先し、判断を要する requirement には executor と分離した grader または reviewer を優先します。executor の self-report は混乱の診断には使えますが、唯一の pass/fail 証拠にはしません。実行前に run 単位と case 単位の判定集約方法を定義します。

このアプローチは、[mizchi/skills](https://github.com/mizchi/skills) に記載されている empirical prompt-tuning 手法を参考にしています。`THIRD_PARTY_NOTICES.md` を参照してください。

## Iter 0 静的チェック

シナリオを書く前に、Iter 0 の静的チェックを実施します。

1. `description` と本文が内部的に一致している
2. 出力フォーマットが定義されているか明確に示されている
3. Skill が自己完結している
4. 違反時に scenario を fail とすべき箇所だけが critical requirement として特定されている
5. 重要な claim と変更した挙動が、起こり得る失敗と採点方法へ対応付けられている

Iter 0 を通過してから、`evals/README.md` にシナリオを整備します。

## ベースライン比較

Skill を大幅に改訂するときは、candidate を前バージョン、または前バージョンを利用できない場合は Skill なしの状態と比較します。baseline は commit、content hash、保持した snapshot のいずれかで特定します。両側で同じ task input、client、model、reasoning settings、environment、grading policy を使います。

隣接 surface が不足を隠すか、変更した挙動と競合し得る場合だけ coexistence を確認します。historical benchmark は文脈として保持できますが、通常の regression baseline は直前の挙動です。

対象 model または client が利用できない場合は `not executed` と記録します。利用可能な対象で新しい paired baseline/candidate run を追加できますが、異なる environment の結果を黙って統合しません。

## 停止規則

次の条件を満たしたら、評価の拡張または再実行を止めます。

- 重要な claim、変更した挙動、既知の regression、関連する境界のすべてに採点経路がある
- 残した各シナリオが固有のリスクを担う
- 観測結果が現在の判断に十分な程度まで安定しているか、残る不安定性が明示されている
- 追加実行をしても現在の設計、rollout、confidence の判断が変わらない

未採点の requirement がある、結果が競合する、高影響な境界が未検証である、次の実行で競合する説明を区別できる場合は、評価を継続または深掘りします。

## 結果 metadata と artifact の扱い

次を記録します。

- client、model、reasoning 設定、date
- run count と trigger rate
- 根拠付きの assertion 結果
- coverage map と判定集約規則
- isolation と coexistence の構成
- client が公開する場合は token と duration
- `not executed` と `not exposed` の項目

raw JSONL、認証情報、完全な session log は、リポジトリ外の一時ディレクトリまたは保持期間を制御した CI artifact だけに保存します。credential、raw session、未加工の trace を commit しません。現在採用中の revision に対する簡潔な evidence は `results.json` に残し、それ以前に採用した claim は、対応する Skill source とともに Git 履歴で監査します。

## 情報源の解釈

- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) は evaluation-first の反復とシナリオ件数の例を示しています。
- [Anthropic Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) は組織向けの3–5 query 要件と、trigger、isolation、coexistence、instruction-following、output-quality、利用 model の被覆を推奨しています。
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) は Skill description に対する prompt test を推奨し、明示的・暗黙的な Skill invocation を説明しています。

このリポジトリでは、これらの情報源から挙動軸と evidence-first の方向性を採用し、suite の規模はローカルな責務と失敗被覆から決めます。
