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

Runner が扱う公式フィールドは `id`、`prompt`、`expected_output`、`files` です。\
文字列と整数の ID は文字列へ正規化します。\
`assertions` の文字列要素には `assertion-1` のような位置に基づく安定した ID を与え、既定では重大な要件として扱います。

リポジトリ固有拡張は、`id`、`text`、`critical` を持つ `assertions` のオブジェクト要素、明示的な `conditions`、埋め込みの `fixture.files`、ケースまたは最上位の `coexistence_skills`、会話履歴の入力、呼び出し評価用の `expected_handlers` です。\
期待する回答が実行担当エージェントに伝わらないよう、実行時の入力と `assertions`、`expected_output` を分離してください。

挙動評価ケースに `assertions` がなければ、Runner は `expected_output` から重大な `expected-output` 要件を一つ生成します。\
呼び出し評価ケースは、同じ最上位形式の `triggers.json` に置き、選択する各ケースへ `expected_handlers` 配列を指定します。

呼び出し評価では、Codex が JSONL に出力した、配置済み Skill に対する成功した読み取りイベントまたはツールイベントだけを数えます。\
読み込みを観測できない場合は `not_exposed` を記録し、呼び出し評価を `inconclusive` と判定します。最終応答の文面から処理した Skill を推測しません。

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

計画には、`candidate` となる Skill のうち、実行担当エージェントへ渡す可能性がある通常ファイルを、`evals/` を除いてすべて記録します。\
評価用ファイル、選択ケースが使うリポジトリ内の入力ファイル、共存させる Skill 全体のマニフェストは別々に記録します。\
シンボリックリンクは拒否し、マニフェストにないファイルを実行用ディレクトリへコピーしません。

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

計画が `--max-model-calls` を超える場合、または記録済みの `candidate`、評価入力、ケース入力、共存させる Skill のマニフェストが変わっている場合、`run` は開始しません。\
これらの検査は Codex の呼び出し前に行います。\
生成物の保存先ディレクトリがすでに存在する場合も拒否します。

各 Codex 呼び出しでは、一時セッション、JSONL 出力、計画済みのモデル、推論強度、`sandbox`、システムの一時ディレクトリに作る使い捨ての実行用ディレクトリを使用します。\
`candidate` 条件ではマニフェストに記録した作業ツリーの Skill、`baseline` 条件では確定済みの基準コミットにある Skill を配置し、`without-skill` 条件では対象 Skill を配置しません。\
`candidate` と併用 Skill のコピーから `evals/` を除外します。

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

評価記録には、評価目的、影響を受ける責務、選択した経路とケース・条件の組み合わせ、基準コミット、`candidate` のマニフェスト、選択した評価入力のハッシュ、実行環境、導出した結果、停止理由、未検証の境界を記録します。\
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

リポジトリ検査では、LLM を呼び出さずに、構造、新旧形式の混在、マニフェストの鮮度、記録の整合性を確認します。\
静的検査の合格は、実行時の品質、Skill の呼び出し、未検証のクライアントへの対応を証明しません。
