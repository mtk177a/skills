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

## Plugin の実行条件

`mtk177a-skills` 0.1.0 は、公開する 29 個の Skill の指示を変更せずに同梱する。\
パッケージには指示と参照資料が揃っているが、それを実行するためのツールや権限まで含まれるわけではない。\
次の一覧で目的の作業に必要な条件を確認し、実際に確認できた動作は [検証記録](#plugin-の検証結果と残る確認) を参照する。

実行するエージェントは、同梱資料をすべて読める必要がある。\
作業中にどの資料を読むかは、各 Skill の指示に従う。\
現在の Skill に実行スクリプトの同梱や Python ライブラリの追加要件はないが、ツールを使う作業には、対象環境のツールと操作権限が必要となる。

| 作業と Skill | 必要な入力・機能 |
| --- | --- |
| 依頼や判断を整理する: `clarify-request`、`define-referents`、`explore-decision-space`、`calibrate-learning-support` | 会話と依頼の文脈。外部の事実が判断に影響する場合は、それを取得する手段。`define-referents` では同梱の参照資料も必ず読む |
| 執筆・説明する: `make-it-click`、`structure-what-you-write`、`write-natural-japanese` | 文章と文脈、および各 Skill が必須とする、または必要に応じて選ぶ同梱資料。結果を保存する場合は、許可された書き込み手段も必要 |
| 日本語の技術文書を書く: `japanese-tech-writing`、`cognitive-rhythm-writing` | 執筆・推敲する文章。`cognitive-rhythm-writing` では、隣接する `japanese-tech-writing/SKILL.md` を必ず読む |
| 実行条件を評価する: `choose-ai-execution-setup`、`assess-risky-change-readiness` | 利用可能な環境、機能、制御、権限についての証拠。助言を得ても、それらの機能が使えるようになったり、実行が許可されたりするわけではない |
| 変更を設計する: `design-changes`、`design-agent-instructions`、`design-skill` | 関係する既存実装、指示、制約へのアクセス。成果は設計であり、変更の実装ではない |
| 指示や障害を調査する: `audit-agent-guidance`、`investigate-failure`、`break-failure-loop` | 対象範囲の指示、障害・試行の証拠、必要な読み取り用の調査手段。動作の証拠がなければ未確認とする |
| リポジトリ内のファイルを編集する: `curate-repo-docs`、`implement-changes` | 対象ファイル、適用されるリポジトリ規則、許可された書き込み手段、必要な検証ツール。実行に必要な機能が足りない場合、実装に成功したとは扱わない |
| 変更や指摘をレビューする: `review-changes`、`validate-fix`、`triage-review-feedback` | 実際の差分・修正・指摘と、関連する原本・仕様の証拠。コマンド実行や実環境の確認には、それに対応するツールが必要。未検証の主張は未確認のまま扱う |
| 変更概要や課題管理用の文面を下書きする: `draft-commit`、`draft-issue`、`draft-review-comments`、`summarize-changes` | 各 Skill が要求する、範囲の定まった変更、根拠のある依頼、提供された指摘。証拠の取得に必要な場合は、リポジトリや課題管理システムへのアクセスも必要。下書きの作成では投稿しない |
| 引き継ぎを記録する: `record-session-handoff` | 現在の作業の証拠と、利用可能な場合は許可された保存手段。保存できない場合は、Skill が定める下書きや未保存の結果を返す |
| Web で調査する: `research-web-safely` | 実際の検索・取得手段と、確認できる引用元。資料やツールを利用できなかった場合は、検証済みとする根拠にはできない |
| 別のエージェントで改稿する: `revise-docs-fresh-eyes` | Codex または Claude Code、成果物へのアクセス、執筆時の会話を引き継がない独立したサブエージェントの利用許可。子実行が利用できない、または禁止されている場合は中止し、同じ文脈内での改稿で代用しない |

パッケージには、`design-skill` の作成ガイド、編集用 Skill が使う文書判断・TDD の参照資料、未改変の Gist ミラー 2 個と来歴文書を含める。\
ミラーを隣接して配置することで、一方がもう一方の本文を必ず読むという関係を保つ。\
別の作業手順への言及があるだけでは、その Skill を必須の併用先とはみなさない。

リポジトリ保守専用の `maintain-japanese-references` は、公開配布の対象外とする。\
公開 Skill の `write-natural-japanese` を必要とすることは、保守用 Skill 自体を公開する理由にはならない。\
指示や関連ファイルを変更した場合は、上記の該当する実行条件と、パッケージ内の参照関係を一緒に見直す。

## Plugin の検証結果と残る確認

29 個の Skill を含む正式版は、アップロードと動作検証が未完了である。\
次の記録は、[Issue #100](https://github.com/mtk177a/skills/issues/100) にある、3 個の Skill を含む検証用 Plugin `mtk177a-skills-probe` の 0.1.0 から 0.1.1 への更新に関するものである。\
確認できた範囲は表に記載した内容に限られ、正式版の検証結果としては扱わない。

| 利用先 | 検証用 Plugin で得た証拠 | 未確認の範囲 |
| --- | --- | --- |
| ChatGPT 個人用 Plugin | ユーザーからアーカイブの導入・更新の報告があり、UI でもバージョン変更と Skill 数の 2 個から 3 個への増加を確認した | 自動同期と直接のダウングレード。正式版のアップロードもユーザーが行う |
| Codex | `explore-decision-space` が利用可能な一覧に現れ、本文を読めた。アップロードした原本 7 ファイルは、以前バイト単位での一致を確認した | 配置された全ファイルがアップロード内容と一致するか。2026-10-23 のキャッシュには `.codex-plugin/plugin.json` もあったが、どの段階で追加されたかは観測していない |
| Chat | 提供された会話 PDF に、`define-referents` と `explore-decision-space` を明示的に指定した依頼と、それに沿った出力がある | 本文の読み込み。読み込んだことを証明する独立したツール実行記録はない |
| dots | `clarify-request` と `define-referents` を読んだという dot の応答を、ユーザーから報告された | 独立した確認。証拠は自己申告であり、実行記録を直接観測したものではない |
| Work | 個別の動作検証記録なし | 実行時の動作。検証は未実行 |

これらの検証では、クライアント・モデルのバージョンと権限モードを完全には記録していないため、結果を別の環境へ一般化できない。\
Cursor では、ルートの `plugin.json` とローカル Plugin の読み込みが公式資料に記載されているが、このパッケージでは試していない。

正式版をユーザーがアップロードした後、対象となる画面や環境で次を確認する。

| 確認項目 | 使用する Skill | 確認する内容 |
| --- | --- | --- |
| ツールに依存しない作業 | `explore-decision-space` | 主な作業にツールを必要としない Skill を、明示的に指定して使えるか |
| 同梱資料の読み込み | `define-referents` | Skill に付属する参照資料を読めるか |
| 必須の併用先の読み込み | `cognitive-rhythm-writing` と `japanese-tech-writing` | 一方のミラーがもう一方を必ず読むという関係を保てるか |
| 必要な実行機能がない場合 | `revise-docs-fresh-eyes` | 独立したサブエージェントを使えない場合に中止するか |

バージョン、日付、導入経路、明示的に指定した依頼、観測できた読み込み、出力、不足する機能を記録する。\
観測手段がない動作（`not exposed`）と、実行していない検証（`not executed`）を区別し、どちらも成功とは扱わない。\
成功という結果を得るためだけに、許可なくアカウント設定を変更したり、サブエージェントを作成したりしない。

生成、導入、更新、重複回避、不具合のある版からの復旧は [Plugin の配布手順](distribution.md) を参照する。

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
