# Skill 評価

この文書では、このリポジトリで Skill の評価を選択、実行、記録、移行、レビューする方法を定めます。

目的は、変更を受け入れられるか判断するために必要な最小限の証拠を得ることです。\
編集のたびに自動で評価するものではなく、通常の Skill 変更で全ケース、baseline、反復実行、複数 client の組み合わせを要求するものでもありません。

## 評価の流れ

Skill を変更するときは、次の順序で進めます。

1. 変更した主張または責務を特定する。
2. その Skill の評価定義を移行する必要があるか判断する。
3. 必要十分な評価経路を選ぶ。
4. 変更した責務、既知の回帰、または影響し得る隣接境界を検出できるケースだけを選ぶ。
5. 計画を生成し、実行前にモデル呼び出し回数を確認する。
6. 承認した計画を 1 回実行する。
7. 計画した case-condition の結果だけを採点する。
8. 停止理由と未検証の境界を記録する。
9. 現在の結果だけでは判断できない場合に限り、証拠を追加する。

Runner を file watcher、編集後 hook、その他すべての変更を自動評価する仕組みへ接続しないでください。\
選択した経路で実行が必要な場合に、開発者またはレビュー担当の agent が明示的に呼び出します。

## 評価経路を選ぶ

| 変更の種類 | 経路 | 必要な証拠 |
| --- | --- | --- |
| 発見方法に影響しない文書、整形、意味を変えない表現、機械的な metadata | `static-only` | repository checker のみ |
| 局所的な指示、出力、安全性、その他の実行時責務 | `targeted-candidate` | 影響を受ける candidate ケースを、まず 1 回ずつ |
| `name`、`description`、呼び出し動作、隣接 Skill との責務境界 | `targeted-routing` | 関連する trigger、non-trigger、near-miss、曖昧、coexistence ケース |
| 既知の回帰、大規模な再設計、成功条件の変更、candidate だけでは判断できない結果 | `baseline-comparison` | 判断に必要なケースの candidate と、`baseline` または `without-skill` の対応する条件 |
| 明示的な環境対応の主張、または環境固有の失敗 | `target-environment` | 対象環境での直接実行 |

反復実行は既定の経路ではなく、追加調査です。\
観測された不安定さ、矛盾する証拠、または重大な失敗の影響により、もう一度の観測が判断に必要な場合だけ繰り返します。

package と配布の確認は、通常の Skill 動作評価とは分けて扱います。\
配布動作が変わる場合だけ実行します。

## Skill を初めて実質的に変更するときに定義を移行する

既存の評価 asset をリポジトリ全体で一斉移行しません。\
既存 Skill の `SKILL.md`、runtime resource、発見方法、責務、安全境界、または評価定義を PR で初めて実質的に変更するときに、その Skill の `evals.json` と `triggers.json` 全体を移行します。

README、参考訳の同期、意味を変えない文書や metadata、legacy result だけの変更では移行を要求しません。\
一つの Skill に `evals.json` と `triggers.json` の両方がある場合は、実行可能な契約が新旧混在しないよう、同じ PR で両方を移行します。

評価定義の移行は、移行したすべてのケースを実行することではありません。\
移行後も、その PR で変更した責務に必要なケースだけを実行します。

legacy の `{skill, cases}`、`scenarios`、および legacy `triggers.json` は、リポジトリの履歴として引き続き有効です。\
モデルを使う経路では Codex を呼び出す前にこれらを拒否し、Skill 単位で全評価定義の移行が必要だと示します。\
`static-only` は評価ケースを読み込まないため、未移行の Skill にも使用できます。

## 評価 asset と schema

再利用する asset は Skill と同じ場所に置きます。

```text
skills/<skill-name>/
└── evals/
    ├── README.md       # 人が読む評価契約
    ├── evals.json      # 任意の behavior ケース
    ├── triggers.json   # 任意の routing ケース
    ├── report.json     # 直近で評価した変更の任意の記録
    └── results.json    # 任意の legacy 履歴証拠
```

新しく実行可能にする定義は、[Agent Skills の評価形式](https://agentskills.io/skill-creation/evaluating-skills)に、明示的なリポジトリ固有拡張を加えた形にします。

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

Runner が扱う公式 field は `id`、`prompt`、`expected_output`、`files` です。\
文字列と整数の ID は文字列へ正規化します。\
文字列 assertion には `assertion-1` のような安定した位置ベースの ID を与え、既定では critical とします。

リポジトリ固有拡張は、`id`、`text`、`critical` を持つ assertion object、明示的な `conditions`、inline の `fixture.files`、case または top-level の `coexistence_skills`、transcript 入力、routing 用の `expected_handlers` です。\
期待する回答が executor に漏れないよう、executor 入力と assertions、`expected_output` を分離してください。

behavior ケースに assertion がなければ、Runner は `expected_output` から critical な `expected-output` requirement を一つ生成します。\
routing ケースは同じ top-level 形式の `triggers.json` に置き、選択する各ケースへ `expected_handlers` 配列を指定します。

routing 評価では、Codex が JSONL に公開した、配置済み Skill に対する成功した read または tool event だけを数えます。\
読み込みを観測できない場合は `not_exposed` を記録し、routing を `inconclusive` と判定します。最終応答の文面から handler を推測しません。

## token を使う前に計画する

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
base commit を解決し、明示的に選んだケースと条件だけを展開し、モデル呼び出し回数の見積もりを表示して、canonical JSON の digest を持つ schema version 2 の計画を書き出します。

計画には、executor へ渡し得る candidate の通常ファイルを、`evals/` を除いてすべて記録します。\
評価 asset、選択ケースが使うリポジトリ内の入力ファイル、coexistence Skill 全体の manifest は別々に記録します。\
symlink は拒否し、manifest にないファイルを fixture へコピーしません。

モデルを使う経路では、一つ以上の `--case` が必要です。全ケースを暗黙に選ぶ指定はありません。\
既定の条件は `candidate` です。\
`baseline-comparison` の既定は `candidate` と `baseline` で、`without-skill` を含む明示的な `--condition` も指定できます。\
それ以外の経路では比較条件を指定できません。

既定の model は `gpt-5.6-sol`、reasoning effort は `high`、sandbox は `read-only` です。\
別の環境が評価上必要な場合は、これらを明示的に上書きします。

## 承認した計画を実行する

明示的な予算を指定して計画を実行します。

```bash
python3 scripts/run_skill_evaluation.py run \
  --plan "$evaluation_tmp/plan.json" \
  --artifacts-dir "$evaluation_tmp/artifacts" \
  --execute \
  --max-model-calls 1
```

計画が `--max-model-calls` を超える場合、または記録済みの candidate、評価入力、case 入力、coexistence Skill の manifest が変わっている場合、`run` は開始しません。\
これらの検査は Codex の呼び出し前に行います。\
artifact directory がすでに存在する場合も拒否します。

各 Codex 呼び出しでは、ephemeral session、JSONL 出力、計画済みの model、reasoning effort、sandbox、system temporary directory 配下の disposable fixture を使用します。\
candidate 条件では manifest に固定した working tree の Skill、baseline 条件では解決済み base commit の Skill を配置し、without-Skill 条件では対象 Skill を配置しません。\
candidate と companion のコピーから `evals/` を除外します。

behavior 評価では対象 Skill の使用を executor に明示します。\
routing 評価では Skill の選択を強制せずに依頼を渡します。

schema version 2 の `run.json` は絶対 plan path を持たず、正規化済みの plan と digest を埋め込みます。\
実際の execution pair、environment、static check の結果、routing の観測、一時 artifact directory 内の raw artifact の場所も記録します。

raw JSONL、stderr、最終応答、disposable fixture、plan、run record は system temporary directory 配下だけに残します。\
これらを commit しないでください。

## 計画した結果を採点する

Runner は別のモデルを自動 grader として呼び出しません。\
呼び出し元の Codex session または人が、routing 以外の requirement に対する schema version 2 の grades を作成します。

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

case-level status は入力しません。\
Runner が requirement の status と、plan に固定した critical flag から次の順序で導出します。

1. executor または requirement の `error` は `error` とする。
2. critical な `fail` は `fail` とする。
3. non-critical な `fail` またはいずれかの `inconclusive` は `inconclusive` とする。
4. すべての requirement が pass なら `pass` とする。

Runner は直接観測から critical な `routing-handlers` requirement を追加して採点するため、grades ではこれを繰り返しません。\
grades は完了した case-condition pair と routing 以外の requirement に正確に一致する必要があり、不足、重複、計画外の結果は拒否します。

証拠は簡潔で、判断に必要な内容に限定してください。\
完全な prompt、response、trace、stderr、JSONL event、credential、環境固有の絶対 path を grades に貼り付けないでください。

## report を preview して書き込む

リポジトリを変更する前に compact report を preview します。

```bash
python3 scripts/run_skill_evaluation.py report \
  --run "$evaluation_tmp/artifacts/run.json" \
  --grades "$evaluation_tmp/grades.json" \
  --stopping-reason "The selected case answered the acceptance question." \
  --unverified "Unselected responsibilities"
```

`report` は別の plan を受け取りません。\
`run.json` に埋め込まれた plan snapshot だけを正本として、digest、environment、execution pair、candidate manifest、評価入力を再検証します。

preview を確認してから `--write` を付けてください。\
指定すると、`skills/<skill-name>/evals/report.json` を schema version 2 で置き換えます。

report には、評価目的、影響を受ける責務、選択した経路と pair、base commit、candidate manifest、選択した評価入力の hash、実行環境、導出した結果、停止理由、未検証の境界を記録します。\
plan snapshot、raw prompt、response、JSONL、絶対 path、credential、coexistence Skill の manifest は含めません。

checker は result と summary の status を再計算し、対象 Skill と選択した評価入力が現在も一致することを検査します。\
後から coexistence Skill だけが無関係に変わっても、承認済み report を stale にしません。

report は一つの変更に限定した評価を記述するもので、Skill 全体の品質を表すものではありません。\
未選択ケースは stale や未実行として記録せず、省略します。\
次に評価を伴う変更でこのファイルを置き換え、以前の記録は Git 履歴に残します。

`results.json` は legacy の履歴証拠として引き続き有効です。\
repository checker は JSON の基本的な identity を検査しますが、candidate hash が現在の Skill と一致することは要求しません。\
Skill の別の部分が変わっただけで legacy result を更新または移行しません。

## 停止と追加調査

選択した candidate ケースを 1 回ずつ観測し、結果が受け入れ判断に答え、重要な選択済み requirement がすべて採点され、未検証範囲が明示されていれば停止します。

次のいずれかを解消するために必要な証拠だけを追加します。

- 選択した requirement が未採点である
- case または採点規則に不備がある
- candidate の証拠が曖昧、または別の観測と矛盾する
- 観測された不安定さにより反復が判断に必要になった
- 以前の Skill または Skill なしの動作との比較が受け入れ判断に必要である
- 重要な環境固有の主張が未検証である

case や grader の不備を補うために Skill を変更しないでください。\
先に評価入力を修正します。

## 評価の十分性をレビューする

選択した証拠が変更した責務を覆っているかは、レビュワーが判断します。\
checker は記録の整合性を確認できますが、意味上の十分性は判断できません。

評価不足を指摘するには、次のすべてを特定する必要があります。

- 評価されていない変更責務
- 受け入れ判断に影響する、具体的で起こり得る失敗
- 記録済みの確認ではその失敗を検出できない理由
- 判断に必要な最小の追加 case、condition、または deterministic check

未選択ケース、無関係な suite、未移行 Skill、legacy `results.json`、以前の report が更新されていないという理由だけで、評価不足を指摘しません。\
判断に関係する失敗へ結び付けずに、固定のケース数、baseline、反復、Skill なし条件、model matrix を要求しません。

## リポジトリの検査

report の書き込み後または評価 asset の変更後に、deterministic な検証をすべて実行します。

```bash
python3 scripts/check_repository.py
python3 -m unittest discover -s tests
```

checker は LLM を呼び出さずに、構造、新旧形式の混在、manifest の鮮度、記録の整合性を検査します。\
静的検査の合格は、実行時の品質、routing、未検証 client への対応を証明しません。
