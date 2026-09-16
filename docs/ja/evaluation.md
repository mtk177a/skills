> **注記:** 英語版 (`docs/evaluation.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill の評価

この文書では、このリポジトリで Skill の評価を選択、実行、記録、レビューする方法を定めます。

目的は、変更を受け入れられるか判断するために必要な最小限の証拠を得ることです。\
編集のたびに評価を自動実行せず、通常の Skill 変更に全ケース、baseline、反復実行、クライアントの組み合わせ評価を求めません。

## 評価手順

Skill を変更するときは、次の順序で進めます。

1. 変更された主張または責務を特定します。
2. 後述の表から必要十分な評価経路を選びます。
3. 変更された責務、既知の回帰、または影響を受ける可能性がある隣接境界を露出できるケースだけを選びます。
4. 実行前に計画を生成し、モデル呼び出し回数を確認します。
5. 承認した計画を 1 回実行します。
6. 計画したケースと条件の結果だけを採点します。
7. 停止理由と未検証の境界を記録します。
8. 現在の結果だけでは判断できない場合に限り、証拠を追加します。

Runner をファイル監視、編集後 hook、その他の revision ごとに自動評価する仕組みへ接続しません。\
選択した経路で実行が必要な場合に、開発者またはレビュー担当のエージェントが明示的に呼び出します。

## 評価経路を選ぶ

| 変更内容 | 経路 | 必要な証拠 |
| --- | --- | --- |
| 発見方法へ影響しない文書、書式、意味を変えない文言、機械的な metadata | `static-only` | repository checker のみ |
| 局所的な指示、出力、安全性、その他の実行時責務 | `targeted-candidate` | 影響を受ける candidate ケースを最初に 1 回ずつ実行 |
| `name`、`description`、呼び出し動作、隣接 Skill との責務境界 | `targeted-routing` | 関連する trigger、non-trigger、near-miss、曖昧、coexistence ケース |
| 既知の回帰、大幅な再設計、成功条件の変更、candidate 単独では曖昧な結果 | `baseline-comparison` | 判断に必要なケースについて、candidate と `baseline` または `without-skill` を同じ条件で比較 |
| 明示的な環境対応の主張または環境固有の失敗 | `target-environment` | 影響を受ける環境での直接実行 |

反復は既定の経路ではなく、評価を強化する手段です。\
観測済みの不安定性、矛盾する証拠、重大な失敗結果により、追加観測が判断へ影響する場合だけ反復します。

package と配布の検査は、通常の Skill 動作評価から分けます。\
配布動作が変わる場合だけ実行します。

## 評価資産

再利用する資産は Skill と同じ場所に置きます。

```text
skills/<skill-name>/
└── evals/
    ├── README.md       # 人が読む評価契約
    ├── evals.json      # 任意の動作ケース
    ├── triggers.json   # 任意の routing ケース
    ├── report.json     # 直近の評価対象変更に対する任意の記録
    └── results.json    # 任意の legacy 履歴証拠
```

反復評価の再現性が高まる場合に限り、構造化資産を追加します。\
形式を揃えることだけを目的に既存資産を移行しません。

### 動作ケースの形式

Runner は、このリポジトリで現在使っている形式を受け付けます。

```json
{
  "schema_version": 1,
  "skill": "example-skill",
  "cases": [
    {
      "id": "bounded-change",
      "input": "Handle this request.",
      "assertions": ["bounded-output"]
    }
  ]
}
```

`evals.json` では、最小限の公式方式に沿った形式も受け付けます。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Handle this request.",
      "expected_output": "A bounded result.",
      "files": []
    }
  ]
}
```

文字列と整数の ID は文字列へ正規化します。\
この形式から現在の Runner が利用する項目は、`prompt`、任意の `expected_output`、任意の `files` です。\
期待する答えを executor へ知らせないように、executor の入力と assertion・期待出力を分けます。

このリポジトリの既存ケースについては、adapter が `input`、`turns`、conversation context、`assertion_ids`、inline `fixture.files` も受け付けます。\
複数 turn は 1 件の明示的な transcript へ直列化するため、ケースと条件の 1 組が消費する executor 呼び出しは 1 回のままですが、この結果は supplied context に対する最終応答だけを検査し、turn 間で生成されたはずの応答の証拠にはなりません。\
repository-relative な `files` は `inputs/` 配下へコピーし、inline fixture file は宣言された path を disposable fixture 内で保ちます。\
内容を持たない名前だけの fixture は安全に再構築できないため、実行前に拒否します。

`triggers.json` には、このリポジトリの現在の `{skill, cases}` 形式で routing ケースを記録します。\
routing 評価では、Codex の JSONL event が公開する path または command field だけを Skill 読み込みの証拠として数えます。\
読み込みを観測できない場合は `not_exposed` と記録し、最終応答の文言から選択を推測しません。

## トークンを使う前に計画する

リポジトリの root で一時ディレクトリを作り、計画を生成します。

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
base commit を解決し、変更された Skill file と選択したケース資産の hash を記録し、明示的に選んだケースと条件だけを展開して、モデル呼び出し回数の見積もりを表示します。\
一時 plan には呼び出し元が採点に使う選択済み assertion 定義、期待出力、追加の採点要件を残しますが、executor prompt には正規化したケース入力だけを含めます。

モデルを使う経路では、1 件以上の `--case` が必要です。\
全ケースを暗黙に選ぶ option はありません。

既定の条件は `candidate` です。\
`baseline-comparison` の既定条件は `candidate` と `baseline` であり、`without-skill` を含む `--condition` を明示することもできます。\
他の経路では比較条件を指定できません。

既定の model は `gpt-5.6-sol`、reasoning effort は `high`、sandbox は `read-only` です。\
評価上の問いに別の環境が必要な場合は明示的に上書きします。

## 承認した計画を実行する

明示的な予算を付けて計画を実行します。

```bash
python3 scripts/run_skill_evaluation.py run \
  --plan "$evaluation_tmp/plan.json" \
  --artifacts-dir "$evaluation_tmp/artifacts" \
  --execute \
  --max-model-calls 1
```

計画が `--max-model-calls` を超える場合、`run` は実行前に拒否します。\
以前の実行結果を黙って上書きしたり混在させたりしないように、artifact directory は未作成でなければなりません。

各 Codex 呼び出しでは、ephemeral session、JSONL 出力、計画した model・reasoning effort・sandbox、システムの一時ディレクトリに置いた disposable fixture を使います。\
candidate 条件では作業ツリーの Skill、baseline 条件では解決済み base commit の Skill を配置し、without-Skill 条件では対象 Skill を配置しません。\
hidden assertion と期待出力を executor から見えなくするため、candidate、baseline、companion のコピーから `evals/` を除外します。\
評価資産で宣言した companion Skill だけを一緒に配置します。

動作評価では、対象 Skill を使うよう executor に明示します。\
routing 評価では Skill の選択を強制せず、依頼だけを渡します。

Runner はモデル呼び出しの前に、機械的な repository checker を 1 回実行します。\
Skill の変更により以前の report が stale になることを考慮し、この検査中だけ、評価対象 Skill の以前の `report.json` を除外します。\
通常の repository validation では report を除外しません。

raw JSONL、stderr、完全な最終応答、disposable fixture、計画、実行記録は、システムの一時ディレクトリだけに残します。\
これらを commit しません。

## 計画した結果を採点する

Runner は、別の model を自動 grader として使いません。\
呼び出し元の Codex session または人間が、計画した出力をケースの assertion に照らして採点し、小さな一時 JSON file を作成します。

```json
{
  "schema_version": 1,
  "results": [
    {
      "case_id": "bounded-change",
      "condition": "candidate",
      "status": "pass",
      "requirements": [
        {
          "id": "bounded-output",
          "status": "pass",
          "evidence": "The result states the boundary and does not expand the task."
        }
      ],
      "evidence": "All selected requirements passed."
    }
  ]
}
```

使用できる status は `pass`、`fail`、`inconclusive`、`error` です。\
grade は完了したケースと条件の組に正確に対応する必要があり、欠落、重複、未計画の結果は拒否されます。\
ケースに assertion ID が割り当てられている場合、grade には割り当てられた各 assertion を 1 回ずつ含める必要があります。\
executor の失敗は、作り上げた採点証拠を要求せず `error` result になります。

evidence は短く、判断に関係する内容だけを記載します。\
完全な prompt、response、trace、stderr、JSONL event、credential、環境固有の絶対 path を grade へ貼り付けません。

## report を確認して書き込む

リポジトリを変更する前に、簡潔な report を preview します。

```bash
python3 scripts/run_skill_evaluation.py report \
  --plan "$evaluation_tmp/plan.json" \
  --run "$evaluation_tmp/artifacts/run.json" \
  --grades "$evaluation_tmp/grades.json" \
  --stopping-reason "The selected case answered the acceptance question." \
  --unverified "Unselected responsibilities"
```

preview を確認した後でのみ `--write` を追加します。\
この command は `skills/<skill-name>/evals/report.json` を置き換えます。

`report.json` には、次の内容を記録します。

- 評価目的と影響を受ける責務
- 選択した経路、ケース、条件
- 解決済み base commit と評価対象 candidate file の hash
- Codex client、model、reasoning effort、sandbox
- 機械的検査と採点結果
- 集約 status、停止理由、未検証の境界

集約 status には、`error`、`fail`、`inconclusive`、`pass` の優先順を使います。\
repository checker は、summary と結果の status が一致し、評価対象 file の hash が現在も有効であることを確認します。

report は、Skill 全体の品質ではなく、1 件の変更に対する評価を記述します。\
未選択ケースを stale または未実行として記録せず、report から省きます。\
次に評価する変更で同じ file を置き換え、以前に受け入れた記録は Git 履歴に残します。

`results.json` は、legacy の履歴証拠として引き続き有効です。\
repository checker は基本的な JSON の識別情報を検査しますが、candidate hash が現在の Skill と一致することは求めません。\
Skill の別の部分が変わっただけで、legacy result を更新または移行しません。

## 停止と評価の強化

選択した各 candidate ケースを 1 回観測した結果で受け入れ判断ができ、重要な選択要件をすべて採点し、残る未検証範囲を明示できたら停止します。

次のいずれかを解消する場合だけ、証拠を追加します。

- 選択した要件が採点されていない
- ケースまたは採点規則に欠陥がある
- candidate の証拠が曖昧、または別の観測と矛盾する
- 観測済みの不安定性により反復が判断へ影響する
- 以前の Skill または Skill なしの動作との比較が受け入れ判断に必要である
- 重要な環境固有の主張が未検証である

ケースまたは grader の欠陥を直すために Skill を編集しません。\
先に評価入力を修正します。

## 評価が十分かレビューする

選択した証拠が変更された責務を扱っているかは、レビュワーが判断します。\
checker は記録の整合性を確認できますが、意味上の十分性は判断できません。

評価不足の指摘では、次のすべてを特定する必要があります。

- 被覆されていない変更責務
- 受け入れ判断に関係する、具体的に起こり得る失敗
- 記録済みの検査でその失敗を露出できない理由
- 解消に必要な最小の追加ケース、条件、または機械的検査

未選択ケース、無関係な suite、legacy `results.json`、以前の report が更新されていないという理由だけで、評価不足を指摘しません。\
判断に関係する失敗へ結び付けずに、固定のケース数、baseline、反復、Skill なし条件、model matrix を要求しません。

## リポジトリの検査

report の書き込み後、または評価資産の変更後に、機械的検査をすべて実行します。

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests
```

checker は LLM を呼び出さずに、構造と記録の整合性を検査します。\
静的検査の合格は、実行時の品質、routing、未検証 client への対応を証明しません。
