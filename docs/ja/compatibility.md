> **注記:** 英語版 (`docs/compatibility.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# 互換性

この文書では、portable な Agent Skills format の互換性と、client 固有の discovery、invocation、permission、実行挙動を分けます。Skill の構造が有効でも、特定の client で意図どおり読み込まれ、発火し、実行されるとは限りません。

このリポジトリでは、証拠を次の 4 状態に分けます。
各状態は記録した範囲にだけ適用し、記録していない client behavior まで裏付けるものではありません。

| 状態 | 意味 |
| --- | --- |
| Format-compatible | Skill package が Agent Skills specification に準拠している。client が Skill を発見または実行できることまでは示さない |
| Documented | 現行の client 公式文書に、対象の discovery、invocation、extension、runtime behavior が記載されている。このリポジトリで実行済みとは限らない |
| Locally verified | client version、日付、観測した discovery または invocation の結果を、このリポジトリに記録している。観測していない invocation path は未検証のままとする |
| Behavior-tested | 定義済みの scenario set について、Skill が選択され、指示に従ったかを targeted evaluation evidence に記録している。特定範囲の証拠であり、一般的な support guarantee ではない |

## 互換性の層

| 層 | 確認する問い |
| --- | --- |
| Format | 有効な `SKILL.md` と、直接発見できる resources があるか |
| Discovery と installation | client はどこを探索し、Skill はどのように配布されるか |
| Invocation | ユーザーが明示実行できるか、model が暗黙選択できるか、それぞれを無効化できるか |
| Client extensions | client 固有 metadata、UI、tools、lifecycle 機能に依存するか |
| Enforcement | どの permission、sandbox、policy、hook が実行を実際に制約するか |
| Runtime | scripts、dependencies、filesystem access、network access が対象環境で利用できるか |
| Verification | 以上のうち、version と日付を記録してローカルで観測したものは何か |

Format 互換性は、client の discovery、invocation、behavioral compatibility の証拠ではありません。
公式文書は Documented の根拠になりますが、Locally verified または Behavior-tested とするには、記録されたローカル実行結果が必要です。

## Client matrix

| Client または層 | 文書上の位置付け | リポジトリ内の証拠 | 現在の状態 |
| --- | --- | --- | --- |
| Codex | 公式文書には、暗黙選択と、Codex CLI または IDE extension で `/skills` か `$` による Skill mention を使う明示的 invocation が記載されている。任意の `agents/openai.yaml` は OpenAI 固有の表示と dependency metadata を提供する。sandbox、approval、rules、tools、runtime access は Skill 本文とは別の制御面である | repository-local discovery と、対象を限定した暗黙選択および behavior を観測済み。明示的な `/skills` と `$` invocation、UI behavior、live permission behavior は、このリポジトリについて未実行 | Documented。記録済み scenario について Locally verified かつ Behavior-tested。明示的 invocation はローカルで未検証 |
| Claude Code | 公式文書には、Claude Code 固有の Skill discovery、invocation、frontmatter、permission、hook behavior が記載されている。これらの client 固有 control は、portable Skill の format 互換性からは導けない | repository installation、discovery、明示・暗黙 invocation、permission、behavior の実行記録なし | Format-compatible。runtime behavior は未検証 |
| GitHub Copilot / `gh skill` | client 固有の discovery、invocation、metadata、permission、runtime behavior は、現行公式文書と対象 version に照らして確認する必要がある | repository installation、discovery、invocation、permission、behavior の実行記録なし | Format-compatible。runtime behavior は未検証 |
| Gemini CLI | client 固有の discovery、invocation、metadata、permission、runtime behavior は、現行公式文書と対象 version に照らして確認する必要がある | repository installation、discovery、invocation、permission、behavior の実行記録なし | Format-compatible。runtime behavior は未検証 |
| その他の client | 標準 package を扱える可能性はあるが、format 互換性だけでは discovery または実行を確認できない | repository-level または Skill-level の version 付き記録がない client は、ローカルで未検証 | version 付き記録がない場合は未検証 |
| APM | root の `skills/` directory を native `SKILL_BUNDLE` として配布するが、実行 client ではない。target 選択と installation layout は、downstream の invocation または behavior を示さない | 下記の bundle check を実行済み | 記録した範囲の distribution のみ検証済み |

client が対応しているという理由だけで、client 固有 metadata を全 Skills に追加しません。その client の invocation control、UI 表示、tool dependency declaration、permission behavior が必要な場合だけ追加します。portable な `name`、`description`、instructions、resources を共通層として維持します。

## 代表的な検証スナップショット

次の表は、文書から推測した support claim ではなく、記録済みの repository check から選んだ観測結果を残すスナップショットです。
後続の Skill 単位の評価について、最新状態または全件を示す一覧ではありません。
後続の Skill-level behavior result は、[evaluation.md](evaluation.md) の選択経路に応じた証拠責務に従い、関係する Skill の評価 asset に記録します。
その証拠を client 固有の compatibility state の根拠に使う場合は、関係する client version、日付、scenario scope を含めます。

| 対象 | Version | 検証日 | 観測した範囲 |
| --- | --- | --- | --- |
| Claude Code | — | — | 未実行。installation、discovery、明示・暗黙 invocation、permission、behavior は未検証 |
| Codex | 0.145.0 | 2026-07-24 | repository-local discovery、baseline/candidate 16 selection run での target Skill open 観測、影響 case の 5 回の再実行を含む candidate/baseline 29 behavior run。明示的な `/skills` と `$` invocation、UI、live permission behavior は未実行 |
| GitHub Copilot / `gh skill` | — | — | 未実行。installation、discovery、invocation、permission、behavior は未検証 |
| Gemini CLI | — | — | 未実行。installation、discovery、invocation、permission、behavior は未検証 |
| APM | 0.26.0 | 2026-09-15 | native bundle の導入、`--skill` の選択導入、個別 Skill path の導入、consumer 側の frozen install、audit |
| `npx skills add` の利用先を含むその他の client | — | — | 個別の記録がない限り未実行 |

このスナップショットに client-level の結果を追加するときは、client と version、日付、installation path、観測できる場合は明示・暗黙 invocation の結果、隣接 Skills、model、permission mode、観測できなかった挙動を含めます。
Skill-level の behavior result は、その Skill の評価資産に記録します。
`not exposed` と `not executed` は pass ではありません。

## Installation paths

### APM 経由の Claude Code

```bash
apm install mtk177a/skills
```

または `apm.yml` で package を宣言します:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### 個別 Skill

```bash
apm install mtk177a/skills/skills/review-changes
```

APM は複数 client を対象にできます。installation command を実行証拠として扱わず、対象ごとの解決 path と discovery behavior を検証します。

## 検証

利用可能な場合は `skills-ref` で Agent Skills format への適合を確認します:

```bash
skills-ref validate
```

配布を変更する場合は、push 済みの candidate commit が必要です。このリポジトリ外の disposable consumer directory から、その完全な commit について、bundle 全体、影響を受ける `--skill` の選択、影響を受ける個別 Skill path、consumer が生成した lockfile を検証します。

```bash
apm install 'mtk177a/skills#<commit>' --target agent-skills --no-policy
apm install --frozen --dry-run --no-policy
apm audit --ci --no-policy
```

これらの command は、triggering、instruction following、permission behavior、output quality を証明しません。それらの claim には [evaluation.md](evaluation.md) の targeted evaluation procedure を使い、第三者と executable capability の review には [security.md](security.md) を使います。

## 現行情報源

- [Agent Skills specification](https://agentskills.io/specification)
- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Skills for enterprise](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)

client extension と runtime behavior は core package format より頻繁に変わります。設計または監査に影響する場合は、現行公式情報を再確認します。

## Plugin の実行条件

`mtk177a-skills` 0.1.0 は、公開 29 Skill の本文を変更せずに同梱する。
次の一覧は必要な証拠と能力を示すもので、各クライアントで無条件に動くことを示すものではない。
同梱する参照資料は、実行するエージェントが読める必要がある。
現在の Skill に実行スクリプトの同梱や Python 依存のインストール要件はない。
ツールを使う作業では、対象環境のツールと操作権限が別途必要になる。

| Skill | 必要な入力・実行条件 |
| --- | --- |
| `clarify-request`、`define-referents`、`explore-decision-space`、`calibrate-learning-support` | 会話・依頼の証拠。`define-referents` は同梱の参照資料も必ず読む。外部の事実が判断に影響する場合は、その取得手段が必要 |
| `make-it-click`、`structure-what-you-write`、`write-natural-japanese` | 提供された文章と文脈、各 Skill が選択または必須とする同梱資料。保存には許可された書込手段が必要 |
| `japanese-tech-writing`、`cognitive-rhythm-writing` | 執筆・推敲する文章。後者は隣接する `japanese-tech-writing/SKILL.md` を必ず読む。未改変の両ミラーと来歴文書を同梱する |
| `choose-ai-execution-setup`、`assess-risky-change-readiness` | 利用可能な環境、能力、制御、権限の証拠。助言によってそれらが提供されたり、実行が許可されたりするわけではない |
| `design-changes`、`design-agent-instructions`、`design-skill` | 関係する既存実装・指示と制約へのアクセス。`design-skill` には作成ガイドを同梱する。設計では変更を実行しない |
| `audit-agent-guidance`、`investigate-failure`、`break-failure-loop` | 対象範囲の指示、障害・試行の証拠、必要な読み取り用の調査手段。動作の証拠がなければ未確認とする |
| `curate-repo-docs`、`implement-changes` | 対象ファイル、適用されるリポジトリ規則、許可された書込手段、必要な検証ツール。文書判断や TDD の参照資料を同梱する。実行能力の不足を実装成功と扱わない |
| `review-changes`、`validate-fix`、`triage-review-feedback` | 実際の差分・修正・指摘と、関連する原本・仕様の証拠。コマンドや実環境の確認には対応するツールが必要。未検証の主張は未確認のまま扱う |
| `draft-commit`、`draft-issue`、`draft-review-comments`、`summarize-changes` | 各 Skill が要求する範囲確定済みの変更、根拠のある依頼、または提供された指摘。必要な証拠に応じてリポジトリ・課題管理へのアクセスが必要。下書き作成では投稿しない |
| `record-session-handoff` | 現在の作業の証拠。許可された保存手段があれば記録し、なければ Skill が定める下書き・未保存の結果を返す |
| `research-web-safely` | Web 検証には実際の検索・取得手段と観測可能な引用が必要。資料やツールが利用できない場合は検証済みとしない |
| `revise-docs-fresh-eyes` | 許可された独立した新規サブエージェントと、成果物へのアクセスを持つ Codex または Claude Code。子実行が利用できない、または禁止されている場合は中止する。同じ文脈内での改稿では代用しない |

リポジトリ保守専用の `maintain-japanese-references` は除外する。
この Skill が `write-natural-japanese` を必要とすることは、公開配布する理由にはならない。
別の作業手順への言及だけで、その Skill を必須併用先とはみなさない。
資源や指示が変わる場合は、該当する行と配布物の参照関係を一緒に見直す。

## Plugin の検証結果と残る確認

[Issue #100](https://github.com/mtk177a/skills/issues/100) には、個人用の検証 Plugin `mtk177a-skills-probe` を 0.1.0 から 0.1.1 へ更新した記録がある。
この証拠は 3 Skill に関するもので、29 Skill を含む正式版の検証結果として扱わない。

| 利用先 | 証拠 | 限界 |
| --- | --- | --- |
| ChatGPT 個人用 Plugin | ユーザーによるアーカイブ導入・更新の報告と、バージョン・Skill 数が 2 個から 3 個へ変わった UI | 正式版もユーザーがアップロードする。自動同期・ダウングレードの証拠はない |
| Codex | probe の `explore-decision-space` が利用可能な一覧に現れ、本文を読めた。アップロードした原本 7 ファイルは以前バイト一致を確認した | 2026-10-23 の配置済みキャッシュには `.codex-plugin/plugin.json` も存在した。配置済みの全ファイル集合の一致は確認しておらず、互換ファイルが追加された段階も未観測 |
| Chat | 提供された会話 PDF に、`define-referents` と `explore-decision-space` の明示依頼と、それに沿う出力がある | 本文の読み込みを証明する独立したツール実行記録はない |
| dots | `clarify-request` と `define-referents` を読んだという dot の応答を、ユーザーから報告された | 自己申告であり、独立して観測した実行記録ではない |
| Work | 個別の動作検証記録なし | 未実行 |
| Cursor | 公式資料にルート `plugin.json` とローカル Plugin 読み込みの対応がある | このパッケージでは未実行 |

probe のクライアント・モデルのバージョンと権限モードは完全には記録されていないため、別の環境へ一般化しない。
正式版の検証はアップロード待ちであり、影響する利用先で、ツール非依存の `explore-decision-space`、参照資料を持つ `define-referents`、ミラーの組、サブエージェントがない場合の `revise-docs-fresh-eyes` を確認する。
バージョン、日付、導入経路、明示依頼、観測できた読み込み、出力、不足する能力、`not exposed`・`not executed` を分けて記録する。
検証を成功扱いにするためだけに、許可なくアカウント設定を変えたりサブエージェントを作ったりしない。
生成、導入、更新、重複回避、復旧は [配布手順](distribution.md) を参照する。
