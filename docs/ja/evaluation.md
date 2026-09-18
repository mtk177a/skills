> **注記:** このファイルは英語版 (`docs/evaluation.md`) の参考訳です。内容に差異がある場合は英語版を優先してください。

# Skill 評価

この文書では、このリポジトリで Skill の評価を選択、実行、記録、移行、レビューする方法を定めます。

目的は、変更を受け入れられるか判断するために必要な最小限の証拠を得ることです。\
編集のたびに自動で評価するものではなく、通常の Skill 変更で全ケース、`baseline`、反復実行、複数クライアントの組み合わせを要求するものでもありません。

## 評価の流れ

Skill を変更するときは、次の順序で進めます。

1. 変更した主張または責務を特定する。
2. その Skill の評価定義を移行する必要があるか判断する。
3. 必要十分な評価経路を選ぶ。
4. 変更した責務、既知の回帰、または影響し得る隣接境界を検出できるケースだけを選ぶ。
5. 計画を生成し、実行前にモデル呼び出し回数を確認する。
6. 承認した計画を 1 回実行する。
7. 計画したケースと条件の組み合わせの結果だけを採点する。
8. 停止理由と未検証の境界を記録する。
9. 現在の結果だけでは判断できない場合に限り、証拠を追加する。

Runner をファイル監視、編集後に動くフック、その他すべての変更を自動評価する仕組みへ接続しないでください。\
選択した経路で実行が必要な場合に、開発者またはレビュー担当のエージェントが明示的に呼び出します。

## 評価経路を選ぶ

| 変更の種類 | 経路 | 必要な証拠 |
| --- | --- | --- |
| 発見方法に影響しない文書、整形、意味を変えない表現、機械的なメタデータ | `static-only` | リポジトリ検査のみ |
| 局所的な指示、出力、安全性、その他の実行時責務 | `targeted-candidate` | 影響を受ける `candidate` ケースを、まず 1 回ずつ |
| `name`、`description`、呼び出し動作、隣接 Skill との責務境界 | `targeted-routing` | 関連する呼び出すべきケース、呼び出すべきでないケース、類似する別の依頼、曖昧な依頼、複数 Skill が共存するケース |
| 既知の回帰、大規模な再設計、成功条件の変更、`candidate` だけでは判断できない結果 | `baseline-comparison` | 判断に必要なケースについて、`candidate` と `baseline` または `without-skill` の対応する条件 |
| 明示的な環境対応の主張、または環境固有の失敗 | `target-environment` | 対象環境での直接実行 |

反復実行は既定の経路ではなく、追加調査です。\
観測された不安定さ、矛盾する証拠、または重大な失敗の影響により、もう一度の観測が判断に必要な場合だけ繰り返します。

パッケージと配布の確認は、通常の Skill 動作評価とは分けて扱います。\
配布動作が変わる場合だけ実行します。

## Skill を初めて実質的に変更するときに定義を移行する

既存の評価用ファイルをリポジトリ全体で一斉移行しません。\
既存 Skill の `SKILL.md`、実行時リソース、発見方法、責務、安全境界、または評価定義を PR で初めて実質的に変更するときに、その Skill の `evals.json` と `triggers.json` 全体を移行します。

README、参考訳の同期、意味を変えない文書やメタデータ、旧形式の評価結果だけの変更では移行を要求しません。\
一つの Skill に `evals.json` と `triggers.json` の両方がある場合は、実行可能な評価定義の形式が新旧混在しないよう、同じ PR で両方を移行します。

どちらか一方の評価定義だけが存在する場合は、もう一方を新規作成せず、存在するファイルだけを移行します。\
実行可能な評価定義を必要としない Skill では、移行だけを目的として新規作成しません。

### 移行例

旧形式の評価定義が両方ある場合は、同じ変更で両方を移行します。

移行前の `evals.json` は、たとえば次のような形式です。

```json
{
  "skill": "example-skill",
  "version": 1,
  "cases": [
    {
      "id": "behavior",
      "prompt": "Handle this request."
    }
  ]
}
```

移行前の `triggers.json` は、たとえば次のような形式です。

```json
{
  "skill": "example-skill",
  "version": 1,
  "cases": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handler": "example-skill"
    }
  ]
}
```

移行後の `evals.json` は、実行可能な挙動評価形式を使用します。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "behavior",
      "prompt": "Handle this request.",
      "expected_output": "A bounded result."
    }
  ]
}
```

移行後の `triggers.json` は、実行可能な呼び出し評価形式を使用します。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handlers": ["example-skill"]
    }
  ]
}
```

旧形式の `triggers.json` だけがある場合は、そのファイルだけを移行し、`evals.json` は新規作成しません。

移行前は次の形式です。

```json
{
  "skill": "example-skill",
  "version": 1,
  "cases": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handler": "example-skill"
    }
  ]
}
```

移行後は次の形式です。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "route",
      "prompt": "Handle this request.",
      "expected_handlers": ["example-skill"]
    }
  ]
}
```

実行可能な評価定義がなく、必要もない場合は、その状態を維持します。

移行前の構成は次のとおりです。

```text
skills/example-skill/evals/
└── README.md
```

移行後も構成は変わりません。

```text
skills/example-skill/evals/
└── README.md
```

評価定義の移行は、移行したすべてのケースを実行することではありません。\
移行後も、その PR で変更した責務に必要なケースだけを実行します。

旧形式の `{skill, cases}`、`scenarios`、および `triggers.json` は、リポジトリの履歴として引き続き有効です。\
モデルを使う経路では Codex を呼び出す前にこれらを拒否し、Skill 単位で全評価定義の移行が必要だと示します。\
`static-only` は評価ケースを読み込まないため、未移行の Skill にも使用できます。

## 評価用ファイルとスキーマ

再利用する評価用ファイルは Skill と同じ場所に置きます。

```text
skills/<skill-name>/
└── evals/
    ├── README.md       # 人が読む評価要件
    ├── evals.json      # 任意の挙動評価ケース
    ├── triggers.json   # 任意の呼び出し評価ケース
    ├── report.json     # 直近で評価した変更についての任意の記録
    └── results.json    # 任意の旧形式の履歴証拠
```

### `evals/README.md` に記載する内容

`evals/README.md` には、評価の目的、範囲、方法、証拠を人が確認できるように記載します。\
JSON で定義済みのケース入力や、その他の機械可読な詳細は重複して記載しないでください。

README には、次のうち該当する内容を記載することを推奨します。

1. 評価の目的と、確認対象となる Skill の責務。
2. `evals.json`、`triggers.json`、`report.json`、`results.json` など、存在する評価用ファイルの役割。
3. Skill の指示や同梱ファイルの構成に対する静的な確認事項。
4. 各責務または境界と、想定される失敗、それを検出できるケースまたは確認、採点方法を対応付けた表。
5. 必要な場合は、分離する条件、比較条件、再実行または停止の条件を含む実行手順と採点手順。
6. 評価したリビジョン、実行環境、選択したケース、結果、未実行の項目を含む現在の証拠。
7. 未検証の範囲と、追加の評価が有用になる条件。

次の構成は推奨例であり、見出しを固定するテンプレートではありません。

~~~markdown
# <skill-name> の評価

## 目的

この評価で確認する責務と、判断したい内容を記載する。

## 評価用ファイル

存在する各ファイルの役割を記載する。

## 静的な確認

モデルを実行せずに確認する、Skill の指示や構成上の性質を列挙する。

## カバレッジ対応表

| 責務または境界 | 想定される失敗 | シナリオまたは確認 | 採点 |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## 実行と採点

適用する実行手順、分離する条件、比較方法、停止条件だけを記載する。

## 現在の証拠

リビジョン、実行環境、選択したケース、結果、未実行の確認を記録する。

## 未検証の範囲

未検証の内容と、次の評価が判断に役立つ条件を記載する。
~~~

証拠に適した別の見出しを使用でき、該当しない項目は省略できます。\
失敗パターンの一覧や次の検証で確認する問いは任意とし、証拠の解釈や追加に役立つ場合だけ記載します。\
リポジトリ検査では README の見出しや構成を検証しません。\
既存の README は一括移行の対象とせず、評価定義または README を実質的に更新するときにこの指針を適用します。

### 基本項目とリポジトリ固有の拡張

実行可能な評価定義では、[Agent Skills の評価ガイド](https://agentskills.io/skill-creation/evaluating-skills) に示された項目を採用し、次のリポジトリ固有の項目と形式を追加しています。\
必須、条件付き、任意の分類は、Agent Skills 全体で共通する JSON スキーマではなく、このリポジトリの実行可能な評価定義に対して適用します。

| 由来 | 場所 | 項目または形式 | このリポジトリでの必要性 | 用途 |
| --- | --- | --- | --- | --- |
| Agent Skills の基本形式 | 最上位 | `skill_name` | 必須 | 評価対象の Skill を識別する。 |
| Agent Skills の基本形式 | 最上位 | `evals` | 必須 | 評価ケースを含む。 |
| Agent Skills の基本形式 | ケース | `id` | 必須 | ケースを識別し、文字列に正規化する。 |
| Agent Skills の基本形式 | ケース | `prompt` | 条件付き | 単一依頼形式の依頼と、リポジトリ固有の `conversation` 形式における現在の依頼を指定する。 |
| Agent Skills の基本形式 | ケース | `expected_output` | 任意。採点条件がない挙動評価ケースでは必須 | 成功とみなす結果を説明し、既定の採点要件の元にする。 |
| Agent Skills の基本形式 | ケース | `files` | 任意 | リポジトリ相対の入力ファイルを選択する。 |
| Agent Skills の基本形式 | ケース | `assertions` の文字列要素 | 任意。挙動評価ケースでは `assertions` または `expected_output` が必須 | 基本の文字列形式で採点条件を定義する。 |
| リポジトリ固有の拡張 | 最上位 | `execution.coexistence_skills` | 任意 | 選択したすべてのケースで併用する Skill を追加する。 |
| リポジトリ固有の拡張 | ケース | `title` | 任意 | 人が読めるケース名を正規化済みの計画に保持する。 |
| リポジトリ固有の拡張 | ケース | `turns` | 代替入力形式として条件付き | 評価入力となる会話全体を指定する。 |
| リポジトリ固有の拡張 | ケース | `authoring_turns` と `request` | 代替入力形式として条件付き | 過去の成果物執筆履歴と現在の依頼を分ける。 |
| リポジトリ固有の拡張 | ケース | `conversation` と `prompt` | 代替入力形式として条件付き | 完了済みの会話文脈と現在の依頼を分ける。`prompt` 自体は基本形式の項目である。 |
| リポジトリ固有の拡張 | ケース | `id`、`text`、`critical` を持つ `assertions` のオブジェクト要素 | 任意 | 基本形式の `assertions` に、安定した ID と重要度を追加する。 |
| リポジトリ固有の拡張 | ケース | `fixture` | 任意 | インラインの `fixture` ファイルを配置する。 |
| リポジトリ固有の拡張 | ケース | `coexistence_skills` | 任意 | 一つのケースで併用する Skill を追加する。 |
| リポジトリ固有の拡張 | ケース | `conditions` | 任意 | ケースを `candidate`、`baseline`、`without-skill` のうち指定した条件に限定する。 |
| リポジトリ固有の拡張 | 呼び出し評価定義 | ケース単位の `expected_handlers` を含む `triggers.json` | すべての呼び出し評価ケースで `expected_handlers` が必須 | 実行可能な形式を呼び出し判定にも使用し、空のハンドラー一覧も期待値として認める。 |

新しく実行可能にする定義は、[Agent Skills の評価形式](https://agentskills.io/skill-creation/evaluating-skills) に、明示的なリポジトリ固有拡張を加えた形にします。

```json
{
  "skill_name": "example-skill",
  "execution": {
    "coexistence_skills": ["adjacent-skill"]
  },
  "evals": [
    {
      "id": 1,
      "title": "Keep the change bounded",
      "prompt": "Handle this request.",
      "expected_output": "A bounded result.",
      "files": ["tests/fixtures/input.txt"],
      "assertions": [
        "The result states the boundary.",
        {
          "id": "no-expansion",
          "text": "The result does not expand the task.",
          "critical": false
        }
      ],
      "fixture": {
        "files": {
          "notes/context.txt": "Fixture content."
        }
      },
      "coexistence_skills": [],
      "conditions": ["candidate"]
    }
  ]
}
```

最上位では `skill_name`、`evals`、任意の `execution` オブジェクトだけを受け付けます。\
`execution` では `coexistence_skills` だけを受け付けます。\
入れ子の各オブジェクトでも、定められたフィールド以外は認めず、未知のフィールドは拒否します。

ケースでは `id`、`title`、後述する入力用フィールド、`expected_output`、`files`、`assertions`、`fixture`、`coexistence_skills`、`conditions`、`expected_handlers` だけを受け付けます。\
`id` は必須で、文字列と整数の ID を文字列へ正規化します。\
`title` は説明用の任意メタデータであり、空でない文字列を指定し、正規化済みの計画にも保持します。

## ケースの入力形式

各ケースでは、次の 4 形式のうち一つだけを使用します。

| 形式 | 必須の入力用フィールド | 意味 |
| --- | --- | --- |
| 単一依頼 | `prompt` | 独立した現在のユーザー依頼を一つ渡す |
| 会話全体 | `turns` | 評価入力となる会話全体を渡す |
| 執筆履歴と依頼 | `authoring_turns` と `request` | 成果物を執筆した履歴と現在の依頼を分けて渡す |
| 会話と依頼 | `conversation` と `prompt` | 完了済みの文脈と現在の依頼を分けて渡す |

次のケースは、採点用フィールドを省略して 4 形式を示しています。

```json
[
  {
    "id": "single",
    "prompt": "Handle this request."
  },
  {
    "id": "transcript",
    "turns": [
      {"role": "user", "content": "Start the task."},
      {"role": "assistant", "content": "What should I preserve?"},
      "Preserve the existing boundary."
    ]
  },
  {
    "id": "authoring",
    "authoring_turns": ["Draft the document."],
    "request": "Review it with fresh eyes."
  },
  {
    "id": "continued",
    "conversation": ["We selected option A."],
    "prompt": "Continue the implementation."
  }
]
```

`turns`、`authoring_turns`、`conversation` は、空でない配列にします。\
各要素には、ユーザー発言を表す空でない文字列、または `role` と `content` だけを持つオブジェクトを指定します。\
`role` に指定できる値は `user` と `assistant` だけです。

複数の形式を組み合わせたり、対で必要なフィールドの片方だけを指定したりしないでください。\
たとえば、`prompt` と `turns` の併用、`authoring_turns` のない `request`、`prompt` のない `conversation` は無効です。

## ケースの採点用フィールドと実行用フィールド

`evals.json` の挙動評価ケースには、空でない `assertions` の要素を一つ以上、または空でない `expected_output` が必要です。\
`assertions` がなければ、Runner は `expected_output` から `expected-output` 要件を一つ生成し、`critical` を `true` にします。

`assertions` の各要素には、空でない文字列、または空でない `id`、空でない `text`、真偽値の `critical` だけを持つオブジェクトを指定します。\
文字列の要素には `assertion-1` のような位置に基づく安定した ID を与え、`critical` の既定値は `true` とします。\
一つのケースの `assertions` 内で ID が重複してはいけません。

`triggers.json` の呼び出し評価ケースには、一意な Skill 名を並べた `expected_handlers` 配列が必要であり、`evals.json` ではこのフィールドを使用できません。\
空の `expected_handlers` 配列は有効で、どの Skill も依頼を処理すべきでないことを表します。\
呼び出し評価ケースでも、呼び出し判定以外の要件として `assertions` または `expected_output` を指定できます。

呼び出し評価の最小定義は次のとおりです。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "non-trigger",
      "prompt": "Answer an unrelated request.",
      "expected_handlers": []
    }
  ]
}
```

`conditions` を指定する場合は、`candidate`、`baseline`、`without-skill` から重複なく選びます。\
`execution` とケース単位の `coexistence_skills` には Skill 名を指定し、それぞれの配列内で重複させません。\
`fixture` には、安全な相対パスと文字列の内容を対応付ける `files` オブジェクトだけを含めます。\
`fixture` を名前だけで参照する形式は実行できません。\
実行するには、ファイルの内容を `fixture.files` に直接記述します。

`files` の各要素には、区切り文字として `/` を使ったリポジトリ相対パスを指定します。\
共通の検証規則では、空のパス、NUL 文字を含むパス、絶対パス、Windows のドライブを含むパス、バックスラッシュ、親ディレクトリへの参照、正規化後に衝突するパスを拒否します。\
インライン fixture のパスでは、さらに `.agents/` と `.git/` を対象にできず、一つの場所をファイルとディレクトリの両方として使用することもできません。\
`files` の各パスは `fixture/inputs/` 配下、`fixture.files` の各パスは `fixture/` 配下に配置され、最終的な配置先が同一または親子関係になる組み合わせは拒否します。

期待する回答が実行担当エージェントに伝わらないよう、実行時の入力と `assertions`、`expected_output` を分離してください。

リポジトリ検査と Runner は、この共通の検証規則を使用します。\
未知のフィールド、未対応の入力の組み合わせ、不正な入れ子オブジェクト、安全でないパス、正規化後の ID 衝突、集合として扱う配列内の重複を含む不正な定義は、モデルを呼び出す前に拒否します。

呼び出し評価では、Codex が JSONL に出力した、配置済み Skill に対する成功した読み取りイベントまたはツールイベントだけを数えます。\
`turn.completed` が含まれる場合だけ、呼び出し評価のイベント列が最後まで出力されたものとして扱います。\
イベント列が完了していて Skill の読み込みが一件もなければ、`handlers` が空の `observed` を記録します。\
この結果は、`expected_handlers` が空のケースで合格となり得ます。\
`turn.completed` がなければ `not_exposed` を記録し、呼び出し評価を `inconclusive` と判定します。最終応答の文面から処理した Skill を推測しません。

## トークンを使う前に計画する

リポジトリのルートで一時ディレクトリを作り、計画を生成します。

```bash
evaluation_tmp="$(mktemp -d)"

python3 scripts/run_skill_evaluation.py plan \
  --skill example-skill \
  --path targeted-candidate \
  --purpose "Check the changed output boundary." \
  --affected "output boundary" \
  --case bounded-change \
  --base-ref origin/main \
  --output "$evaluation_tmp/plan.json"
```

`plan` はモデルを呼び出しません。\
基準とするコミットを確定し、明示的に選んだケースと条件だけを展開し、モデル呼び出し回数の見積もりを表示して、正規化した JSON のダイジェストを持つスキーマバージョン 2 の計画を書き出します。

計画には、`candidate` 条件で使用する Skill に含まれ、実行担当エージェントへ渡される可能性のある通常ファイルを、`evals/` を除いてすべて記録します。\
各ファイルには SHA-256 と、`100644` または `100755` に正規化した Git の mode を含めます。\
評価用ファイル、選択ケースが使うリポジトリ内の入力ファイル、共存させる Skill 全体のマニフェストは別々に記録します。\
Skill の実行対象に含まれるシンボリックリンクは拒否し、マニフェストにないファイルを実行用ディレクトリへコピーしません。

モデルを使う経路では、一つ以上の `--case` が必要です。全ケースを暗黙に選ぶ指定はありません。\
既定の条件は `candidate` です。\
`baseline-comparison` の既定は `candidate` と `baseline` で、`without-skill` を含む明示的な `--condition` も指定できます。\
それ以外の経路では比較条件を指定できません。

既定のモデルは `gpt-5.6-luna`、推論強度は `max`、`sandbox` は `read-only` です。\
別の環境が評価上必要な場合は、これらを明示的に上書きします。

## 承認した計画を実行する

モデル呼び出し回数の上限を明示して計画を実行します。

```bash
python3 scripts/run_skill_evaluation.py run \
  --plan "$evaluation_tmp/plan.json" \
  --artifacts-dir "$evaluation_tmp/artifacts" \
  --execute \
  --max-model-calls 1
```

計画が `--max-model-calls` を超える場合、または記録済みの `candidate`、評価入力、ケース入力、共存させる Skill のマニフェストが変わっている場合、`run` は開始しません。実行可能属性の変更もマニフェストの変更として扱います。\
これらの検査は Codex の呼び出し前に行います。\
生成物の保存先ディレクトリがすでに存在する場合も拒否します。

各 Codex 呼び出しでは、一時セッション、JSONL 出力、計画済みのモデル、推論強度、`sandbox`、システムの一時ディレクトリに作る使い捨ての実行用ディレクトリを使用します。\
`candidate` 条件ではマニフェストに記録した作業ツリーの Skill、`baseline` 条件では確定済みの基準コミットにある通常ファイルを配置し、どちらも正規化した実行可能属性を再現します。\
`baseline` 条件ではシンボリックリンクなどの未対応の Git tree 項目を拒否し、`without-skill` 条件では対象 Skill を配置しません。\
`candidate` と併用 Skill のコピーから `evals/` を除外します。

選択したケースの入力ファイルは、`fixture/inputs/<リポジトリ相対パス>` へコピーします。\
Runner はコピー前に入力元とコピー先を再確認するため、ケース入力がリポジトリ内の入力元ファイルを上書きすることはありません。

挙動評価では対象 Skill の使用を実行担当エージェントに明示します。\
呼び出し評価では Skill の選択を強制せずに依頼を渡します。

スキーマバージョン 2 の `run.json` は計画ファイルの絶対パスを持たず、正規化済みの計画とダイジェストを埋め込みます。\
実際に実行したケースと条件の組み合わせ、実行環境、静的検査の結果、呼び出し評価の観測、一時的な生成物の保存先にある未加工の実行結果の場所も記録します。

未加工の JSONL、標準エラー出力、最終応答、使い捨ての実行用ディレクトリ、計画、実行記録は、システムの一時ディレクトリ内だけに残します。\
これらをコミットしないでください。

## 計画した結果を採点する

Runner は、採点のために別のモデルを自動で呼び出しません。\
呼び出し元の Codex セッションまたは人が、呼び出し評価以外の要件に対するスキーマバージョン 2 の採点結果 JSON を作成します。

```json
{
  "schema_version": 2,
  "results": [
    {
      "case_id": "bounded-change",
      "condition": "candidate",
      "requirements": [
        {
          "id": "expected-output",
          "status": "pass",
          "evidence": "The result states the boundary without expanding the task."
        }
      ],
      "evidence": "The selected requirement passed."
    }
  ]
}
```

ケース全体の `status` は入力しません。\
Runner が要件ごとの `status` と、計画に記録した `critical` フラグから次の順序で導出します。

1. 実行担当エージェントまたは要件の `error` は `error` とする。
2. `critical` が `true` の要件に対する `fail` は `fail` とする。
3. `critical` が `false` の要件に対する `fail`、またはいずれかの `inconclusive` は `inconclusive` とする。
4. すべての要件が `pass` なら `pass` とする。

Runner は直接観測から、`critical` が `true` の `routing-handlers` 要件を追加して採点するため、採点結果 JSON ではこれを繰り返しません。\
採点結果 JSON は完了したケースと条件の組み合わせ、および呼び出し評価以外の要件に正確に一致する必要があり、不足、重複、計画外の結果は拒否します。

証拠は簡潔で、判断に必要な内容に限定してください。\
完全な依頼文、応答、実行履歴、標準エラー出力、JSONL イベント、認証情報、環境固有の絶対パスを採点結果 JSON に貼り付けないでください。

## 評価記録を確認して書き込む

リポジトリを変更する前に、簡潔な評価記録をプレビューします。

```bash
python3 scripts/run_skill_evaluation.py report \
  --run "$evaluation_tmp/artifacts/run.json" \
  --grades "$evaluation_tmp/grades.json" \
  --stopping-reason "The selected case answered the acceptance question." \
  --unverified "Unselected responsibilities"
```

`report` は別の計画を受け取りません。\
`run.json` に埋め込まれた計画情報を参照し、ダイジェスト、実行環境、実行したケースと条件の組み合わせ、`candidate` のマニフェスト、評価入力を再検証します。

プレビューを確認してから `--write` を付けてください。\
指定すると、`skills/<skill-name>/evals/report.json` をスキーマバージョン 2 で置き換えます。

評価記録には、評価目的、影響を受ける責務、選択した経路とケース・条件の組み合わせ、基準コミット、ハッシュと mode を含む `candidate` のマニフェスト、選択した評価入力のハッシュ、実行環境、導出した結果、停止理由、未検証の境界を記録します。\
計画情報の複製、未加工の依頼文、応答、JSONL、絶対パス、認証情報、共存させる Skill のマニフェストは含めません。

リポジトリ検査では、個別結果と集計結果の `status` を再計算し、対象 Skill と選択した評価入力が現在も一致することを確認します。\
後から共存させる Skill だけが無関係に変わっても、承認済みの評価記録を古いものとして扱いません。

評価記録は一つの変更に限定した評価を記述するもので、Skill 全体の品質を表すものではありません。\
未選択ケースは古いケースや未実行のケースとして記録せず、省略します。\
次に評価を伴う変更でこのファイルを置き換え、以前の記録は Git 履歴に残します。

`results.json` は旧形式の履歴証拠として引き続き有効です。\
リポジトリ検査では JSON の基本構造と Skill 名などの識別情報を確認しますが、`candidate` のハッシュが現在の Skill と一致することは要求しません。\
Skill の別の部分が変わっただけで、旧形式の評価結果を更新または移行しません。

## 停止と追加調査

選択した `candidate` ケースを 1 回ずつ観測し、その結果で受け入れ可否を判断でき、選択した重要な要件がすべて採点され、未検証範囲が明示されていれば停止します。

次のいずれかを解消するために必要な証拠だけを追加します。

- 選択した要件が未採点である
- ケースまたは採点規則に不備がある
- `candidate` の証拠が曖昧、または別の観測と矛盾する
- 観測された不安定さにより反復が判断に必要になった
- 以前の Skill または Skill なしの動作との比較が受け入れ判断に必要である
- 重要な環境固有の主張が未検証である

ケースや採点方法の不備を補うために Skill を変更しないでください。\
先に評価入力を修正します。

## 評価の十分性をレビューする

選択した証拠が変更した責務を覆っているかは、レビュワーが判断します。\
リポジトリ検査では記録の整合性を確認できますが、意味上の十分性は判断できません。

評価不足を指摘するには、次のすべてを特定する必要があります。

- 評価されていない変更責務
- 受け入れ判断に影響する、具体的で起こり得る失敗
- 記録済みの確認ではその失敗を検出できない理由
- 判断に必要な最小限の追加ケース、条件、または機械的検査

未選択ケース、無関係な評価一式、未移行の Skill、旧形式の `results.json`、以前の評価記録が更新されていないという理由だけで、評価不足を指摘しません。\
判断に関係する失敗へ結び付けずに、固定のケース数、`baseline`、反復、Skill なし条件、モデルの組み合わせ評価を要求しません。

## リポジトリの検査

評価記録の書き込み後または評価用ファイルの変更後に、同じ入力から同じ結果を得られる検証をすべて実行します。

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests
```

リポジトリ検査では、LLM を呼び出さずに、構造、新旧形式の混在、マニフェストに記録した内容と実行可能属性が現在も一致すること、`candidate` の実行対象にシンボリックリンクがないこと、記録の整合性を確認します。\
静的検査の合格は、実行時の品質、Skill の呼び出し、未検証のクライアントへの対応を証明しません。
