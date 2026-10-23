> **注記:** 英語版 (`docs/compatibility.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# 互換性

この文書では、portable な Agent Skills format の互換性と、client 固有の discovery、invocation、permission、実行挙動を分けます。Skill の構造が有効でも、特定の client で意図どおり読み込まれ、発火し、実行されるとは限りません。

このリポジトリでは、証拠を次の 4 状態に分けます。
各状態は記録した範囲にだけ適用し、記録していない client behavior まで裏付けるものではありません。

| 状態 | 意味 |
| --- | --- |
| Format-compatible | Skill package が Agent Skills specification に準拠している。client が Skill を発見または実行できることまでは示さない |
| Documented | 現行の client 公式文書に、対象の discovery、invocation、extension、runtime behavior が記載されている。このリポジトリで実行済みとは限らない |
| Locally verified | client version、日付、観測した discovery または invocation の結果を、記録している。観測していない invocation path は未検証のままとする |
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

| Client または層 | 文書上の位置付け |
| --- | --- |
| Codex | 公式文書には、暗黙選択と、Codex CLI または IDE extension で `/skills` か `$` による Skill mention を使う明示的 invocation が記載されている。任意の `agents/openai.yaml` は OpenAI 固有の表示と dependency metadata を提供する。sandbox、approval、rules、tools、runtime access は Skill 本文とは別の制御面である |
| Claude Code | 公式文書には、Claude Code 固有の Skill discovery、invocation、frontmatter、permission、hook behavior が記載されている。これらの client 固有 control は、portable Skill の format 互換性からは導けない |
| GitHub Copilot / `gh skill` | client 固有の discovery、invocation、metadata、permission、runtime behavior は、現行公式文書と対象 version に照らして確認する必要がある |
| Gemini CLI | client 固有の discovery、invocation、metadata、permission、runtime behavior は、現行公式文書と対象 version に照らして確認する必要がある |
| その他の client | 標準 package を扱える可能性はあるが、format 互換性だけでは discovery または実行を確認できない |
| APM | root の `skills/` directory を native `SKILL_BUNDLE` として配布するが、実行 client ではない。target 選択と installation layout は、downstream の invocation または behavior を示さない |

client が対応しているという理由だけで、client 固有 metadata を全 Skills に追加しません。その client の invocation control、UI 表示、tool dependency declaration、permission behavior が必要な場合だけ追加します。portable な `name`、`description`、instructions、resources を共通層として維持します。

## Plugin の実行条件

`mtk177a-skills` は、公開する Skill の指示を変更せずに同梱する。\
パッケージには指示と参照資料が揃っているが、それを実行するためのツールや権限まで含まれるわけではない。\
次の一覧で、目的の作業に必要な条件を確認する。

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
