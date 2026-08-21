> **注記:** 英語版 (`docs/evaluation.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill の評価

このドキュメントは、このリポジトリの Skill に使用する評価アプローチを説明します。

## 評価選択の原則

変更を受け入れられるか判断するために必要な最小限の証拠を選びます。最初に機械的なリポジトリ検証を使います。実行時動作、発見方法、または責務境界が変わる場合だけ、モデルを使う動作評価を追加し、影響を受ける責務、既知の regression、または影響があり得る隣接境界を露出できるケースだけを選びます。

`SKILL.md` が変更されたという事実だけでは、動作評価を要求しません。公開していること自体も、package 全体、model matrix、client matrix の評価を要求しません。

次の表で評価経路を選びます。

| 変更の形 | 選択する経路 | 必要な被覆 |
| --- | --- | --- |
| 文書、整形、意味を保つ表現修正、または発見方法へ影響しない機械的な metadata 変更 | **静的検証のみ** | 機械的なリポジトリ検査 |
| 局所的な指示、出力、安全動作、その他の実行時責務の変更 | **対象を限定した候補版のみ** | 変更された責務、既知の regression、または影響があり得る隣接境界を露出する候補版ケースだけ。選択した各ケースを最初は 1 回実行する |
| `name`、`description`、呼び出し動作、または隣接 Skill との責務境界の変更 | **対象を限定した routing または coexistence** | 関係する should-trigger、should-not-trigger または near-miss、曖昧、coexistence ケースだけ |
| 既知の regression、大規模な再設計、分割・統合、主観的品質目標の変更、成功契約の変更、または候補版だけでは曖昧な結果 | **baseline 比較** | 判断に関係するケースについて条件を揃えた baseline と candidate の証拠 |
| 観測された不安定性、矛盾する証拠、または重大な失敗影響 | **反復** | 受入上の問いを解決するために必要な追加観測だけ |
| 明示的な環境対応の主張、環境固有の不具合、または client 固有の発見方法、権限、tool、hook、実行時動作の変更 | **model/client 固有** | 影響を受ける環境上での直接評価だけ |
| 配布または catalog の動作変更 | **package 評価** | 影響を受ける配布・catalog の検査。通常の Skill 動作評価とは分離する |

通常の公開 Skill 変更では、package、model、client の matrix を要求しません。評価規模は、普遍的なケース数ではなく、選択した挙動の被覆から決めます。公式 guidance では、3 件または 3–5 件のシナリオが例や組織的な出発点として示されることがあります。このリポジトリでは、その数を普遍的な最小値・最大値として扱いません。

## Companion Skill の例外

`docs/authoring.md` に承認済みの companion 関係を記録していない限り、Skill は自己完結していなければなりません。文書化されていない依存は static validation で失敗とします。文書化された関係も、一般的な依存機構にはしません。

承認済みの関係では、static validation により、関係、理由、導入方法、companion 不在時の動作、provenance、評価場所が、一覧と影響を受ける Skill 資産の間で一致していることを確認します。関係またはその実行時動作が変わる場合、targeted behavioral evaluation では、変更の影響に応じて次のリスクの一方または両方を扱います。

- **Coexistence:** 依存する Skill が指定順で companion を読み、適用される制約を維持する。
- **Companion 不在:** 依存する Skill が文書化された停止または fallback の動作を守り、許可されていない部分的な成果を出さずに、サポートする導入方法を案内する。

変更された Skill の責務、関係、導入方法、または companion 不在時の動作を被覆する確認だけを再実行します。この例外を、いずれかの Skill が文書化された関係から独立して動作する証拠として扱いません。

## 評価の深さを選ぶ

次の規則を順に適用します。

1. 影響を受ける claim または責務と、実行時動作、発見方法、責務境界のどれが変わるかを特定する
2. いずれも変わらない場合は、機械的なリポジトリ検証を実行して終了する
3. 実行時動作が変わる場合は、影響を受ける候補版ケースだけを選ぶ。選択した各ケースについて 1 回の観測から始める
4. 発見方法または責務境界が変わる場合は、関係する routing、near-miss、曖昧、coexistence ケースだけを追加する
5. 表に示した条件により追加証拠が受入判断を変え得る場合だけ、baseline 比較、反復、model/client 固有評価、package 評価へ強化する

無関係な core、capability、routing、coexistence の suite を自動的に追加しません。static check は runtime の挙動を証明しません。targeted regression は、未検証の client や model での挙動を証明しません。suite を機械的に広げず、その限界を明示します。

## 評価選択記録

次だけを記録します。

- 影響を受ける claim または責務
- 選択した経路と、それで十分な理由
- 選択したケースまたは機械的検査
- 受入主張を限定する未検証境界

既存の評価 README または変更記録を使います。繰り返し作業から追加構造の必要性が確認されるまでは、評価選択記録に共通 metadata schema を要求しません。

## 証拠の再利用

評価済みの内容、責務、環境との関係、要件が引き続き適用できる場合だけ、過去の証拠を再利用します。新しい対象限定の証拠は、実際に評価した revision へ結び付けます。現在の内容が変わった場合は、以前の合格を候補版全体の証拠とせず、どの過去要件が引き続き適用できるかを特定します。

現在の判断に引き続き必要で、Git 履歴だけでは不十分な場合に限り、過去の結果を別に保持します。それ以外は Git 履歴を利用します。Skill の別の部分が変わったという理由や、合格状態を更新するだけの目的で、変更されていない証拠を再実行しません。

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

普遍的な反復回数や合格閾値は使いません。観測された不安定な結果、矛盾する証拠、または重大な失敗影響により追加観測が判断を変え得る場合だけ反復します。固定回数を cost-bounded smoke test として使う場合は理由を記録し、統計的保証として扱いません。

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

- 確認する claim または変更と、評価した候補版 revision
- 選択した経路、終了理由、実行した検査またはケース、結果、根拠
- LLM を実行した場合の client、model、reasoning
- 結論を限定する未検証範囲
- 比較を実行した場合だけ、baseline の識別情報と一致させた条件

raw trace、完全な response、credential、環境固有の absolute path はこのファイルへ保存しません。対応する README の結果要約から link します。

`results.json` は、現在採用中の Skill revision に対する簡潔な evidence として扱います。実行ごとに日付付きファイルを追加せず、同じ candidate の再実行や修正結果を 1 つの record へ統合して更新します。過去に採用した result は、評価対象の Skill source とともに Git 履歴で保持します。

採用とはリポジトリ上の revision を特定することであり、それだけでは behavior または trigger を実行して合格したことを意味しません。pass は、評価した revision と、引き続き適用できることを明示した未変更の requirement だけに適用します。採用中の Skill source が変わった場合は、`results.json` を更新するか、影響を受ける evidence を `superseded` または `unverified` と明示するか、ファイルを削除します。欠けている provenance を推測して補わず、古い candidate が現行 source であると誤解させる hash や pass claim を残しません。

このリポジトリでは、共通の結果 schema を要求しません。既存のローカル schema が引き続き有用な場合は維持しますが、選択した評価経路に適用される項目だけを記録します。候補版だけの結果に、baseline、比較 matrix、trigger rate、利用量 metadata、grader 呼び出しを要求しません。

## evals/README.md の構成例

```markdown
# <skill-name> evals

## Iter 0 — Static check

- description と本文が内部的に一致している
- 出力フォーマットが定義されているか明確に示されている
- Skill が自己完結しているか、承認済みの companion 関係を持つ
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

選択した要件を、機械的なリポジトリ検査、fixture の状態、正確な出力項目、hash、trace、その他の客観的な観測だけで確認できる場合は、LLM を使いません。

モデル実行が必要な通常のモデル非依存動作では、Codex、`gpt-5.6-luna`、max reasoning を基準環境として使います。選択した各ケースについて、候補版 1 回から始めます。これは低コストの基準環境であり、対応環境の一覧でも、別の model または client の証拠でもありません。

受け入れる claim が別の model または client に実質的に依存する場合は、選択したケースをその対象環境で直接実行します。対象には、明示的な対応 claim、環境固有の不具合、client 固有の発見方法、権限、tool、hook、実行時動作が含まれます。対象環境で実行する前に、Luna の事前評価を要求しません。

Luna の実行が失敗した場合、または結果が曖昧な場合は、まず、その結果だけで指示または fixture の不備が確認できるか判断します。Skill の失敗と model 能力の限界を区別することで受入判断が変わる場合だけ、別 model へ強化します。Luna の合格または失敗を、実行していない model や client の証拠として扱いません。

behavioral evaluation は blank-slate executor で実行します。リポジトリの履歴を持たず、シナリオに必要な Skill と入力だけを受け取る agent または client session です。

**Blank-slate executor protocol:**

1. リポジトリ context を持たない新しい executor を起動する
2. `SKILL.md`、許可した補助ファイル、シナリオ入力、必要な環境を渡す
3. 非公開 assertion、期待結論、grader note を executor の入力へ含めない
4. executor 自身に pass/fail を宣言させず、結果と公開された trace を取得する
5. 適用される各 requirement を採点し、判定根拠を記録する

適用される構成だけを選びます。

- **Isolation:** 不足を隠しうる隣接 Skill を有効にせず、対象 Skill を単独で評価する
- **Coexistence:** 起こり得る trigger、authority、workflow の競合がある場合に、隣接 Skill や instruction surface と一緒に評価する

最初に十分となる採点方法を次の順で使います。

1. 客観的な要件には機械的 assertion を使う
2. 判断を要する要件には、短い rubric に基づく maintainer の直接レビューを使う
3. 反復可能または独立した model 判断が実質的に有用な場合だけ、別の blank-slate LLM grader を使う

LLM grader は任意であり、既定で executor より高性能な model である必要はありません。隠された正解と採点基準を executor の入力へ含めません。executor の self-report は混乱の診断には使えますが、独立して観測できる要件の唯一の証拠にはしません。

このアプローチは、[mizchi/skills](https://github.com/mizchi/skills) に記載されている empirical prompt-tuning 手法を参考にしています。`THIRD_PARTY_NOTICES.md` を参照してください。

## Iter 0 静的チェック

シナリオを書く前に、Iter 0 の静的チェックを実施します。

1. `description` と本文が内部的に一致している
2. 出力フォーマットが定義されているか明確に示されている
3. Skill が自己完結しているか、必要な Skill と companion 不在時の動作を記録した承認済みの companion 関係を持つ
4. 違反時に scenario を fail とすべき箇所だけが critical requirement として特定されている
5. 影響を受ける claim と変更した挙動が、起こり得る失敗と採点方法へ対応付けられている

実行時動作、発見方法、責務境界へ影響しない場合は、機械的検証の後に終了します。それ以外の場合は、Iter 0 を通過してから、選択したシナリオだけを `evals/README.md` に整備します。

## ベースライン比較

相対的な証拠が受入判断を変え得る場合だけ、baseline 比較を実行します。対象は、既知の regression、大規模な再設計・分割・統合、主観的品質目標の変更、成功契約の変更、候補版だけでは曖昧な結果です。Skill が公開されていること、Skill 本文が変わったこと、または変更を大幅と表現できることだけを理由に baseline を実行しません。

比較を選択した場合は、判断対象に応じて、前バージョンまたは Skill なしの状態を使います。baseline は commit、content hash、保持した snapshot のいずれかで特定します。両側で同じ task input、fixture、client、model、reasoning settings、sandbox、grading policy を使います。

隣接 surface が不足を隠すか、変更した挙動と競合し得る場合だけ coexistence を確認します。historical benchmark は文脈として保持できますが、通常の regression baseline は直前の挙動です。

対象 model または client が利用できない場合は `not executed` と記録します。利用可能な対象で新しい paired baseline/candidate run を追加できますが、異なる environment の結果を黙って統合しません。

選択した各条件について 1 回の観測から始めます。不安定な結果、矛盾する証拠、実行不備、または重大な失敗影響により、追加観測が受入判断に有用となった場合だけ反復します。

## 停止規則

次の条件を満たしたら、評価の拡張または再実行を止めます。

- 影響を受ける claim、変更した挙動、既知の regression、関連する境界のすべてに採点経路がある
- 残した各シナリオが固有のリスクを担う
- 観測結果が現在の判断に十分な程度まで安定しているか、残る不安定性が明示されている
- 追加の検査または実行をしても受入判断が変わらない

未採点の requirement がある、結果が競合する、高影響な境界が未検証である、次の実行で競合する説明を区別できる場合は、評価を継続または深掘りします。

## 結果 metadata と artifact の扱い

受け入れる結論の範囲を限定するために必要な最小限の証拠を記録します。

- 確認する claim または変更
- 選択した経路と終了理由
- 実行した検査またはケースと結果
- LLM を実行した場合の client、model、reasoning
- 結論を限定する未検証範囲
- 比較を実行した場合だけ、baseline の識別情報と一致させた条件

token 数、model 呼び出し数、turn 数、tool 呼び出し数、所要時間は、client が公開し、現在のコストまたは受入判断に使う場合だけ記録します。取得できないデータを推測しません。

リポジトリ全体の状態機械を導入せず、必要に応じて次の単純な evidence state を使います。

- `not executed`: 検査を省略した、または実行できなかった
- `not exposed`: client が観測値を公開しなかった
- `unverified`: 受け入れた claim に適用可能な証拠がない
- `superseded`: 後の内容または証拠が以前の claim を置き換えた

いずれの状態も pass ではありません。

raw JSONL、認証情報、完全な session log は、リポジトリ外の一時ディレクトリまたは保持期間を制御した CI artifact だけに保存します。credential、raw session、未加工の trace を commit しません。現在採用中の revision に対する簡潔な evidence は `results.json` に残し、それ以前に採用した claim は、対応する Skill source とともに Git 履歴で監査します。

## 情報源の解釈

- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) は evaluation-first の反復とシナリオ件数の例を示しています。
- [Anthropic Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise) は組織向けの3–5 query 要件と、trigger、isolation、coexistence、instruction-following、output-quality、利用 model の被覆を推奨しています。
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) は Skill description に対する prompt test を推奨し、明示的・暗黙的な Skill invocation を説明しています。

このリポジトリでは、これらの情報源から挙動軸と evidence-first の方向性を採用し、suite の規模はローカルな責務と失敗被覆から決めます。
