> **注記:** 英語版 (`docs/authoring.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Skill 作成ガイド

この文書は、このリポジトリで管理する Skills の作成ガイドです。個別の Skill と一緒に運ぶべきポータブルな Skill 設計ガイドは、その Skill 自身の `references/` ディレクトリに置きます。

## 良い Skill の条件

良い Skill は、エージェントが迷わずいつ使うかを判断でき、必要十分な詳細量を持ちます。

本文は英語を原則とします。日本語の執筆・推敲そのものを目的とする Skill は、日本語の `SKILL.md` を正本とし、重複する日本語訳を省略できます。この例外と Skill の出典は文書化します。固有名詞、設定キー、技術用語はそのままにします。

優先すべき内容:

- Skill の目的を短く明確に述べる
- いつ使い、いつ使わないかを示す
- 前提条件、入力、期待する出力を読みやすく書く
- エージェント固有の表現を最小化する
- ヘルパースクリプトや参照資料の範囲を明示する
- 高い判断を要する workflow は、あらかじめ決めた成果物ではなく、期待する結果と evidence から設計する
- 指示の自由度をタスクの壊れやすさと文脈依存性に合わせる。複数の進め方が妥当なら目的と制約を示し、順序や完全性が正しさに影響するなら簡潔な番号付き手順と検証方法を示す
- 完全な診断と、段階的な実装または rollout を分ける
- discovery や findings に根拠のない件数上限を設けない

既存の Skill と比較する場合は、責務の重複を解消し、判断が収束するまで必要な例を確認します。目的を満たしたら止め、根拠のない件数上限を設けたり、理由なく catalog 全体を読んだりしません。

## 見出しテンプレートではなく意味上の契約を使う

Skills の見出しを統一する必要はありません。一方で、blank-slate agent が欠けた policy を推測せずに workflow を選択、実行、検証できるだけの情報は必要です。

次の意味上の責務を確認します:

- objective と一貫した単一の責務
- `description` に含まれる完全な trigger context と重要な除外境界
- 行動前に必要な evidence、inputs、preconditions
- workflow または decision logic
- 必要な出力情報。downstream consumer が必要とする場合は厳密な output format
- 重要な場合の authority、failure handling、安全性または permission の境界
- 失敗し得る挙動に対する verification または evaluation
- 同梱 resource と、それを読むまたは実行する条件

これらの責務を表せる最小の構成を使います。代表的な archetype は次の2つです:

| Archetype | 典型的な意味構成 |
| --- | --- |
| 判断型 | Objective、Evidence、Workflow、必要に応じた decision criteria または dimensions、Reporting contract、Boundaries |
| 操作型 | Objective、Inputs または Preconditions、順序付き Steps、Output format、Verification、Boundaries |

これらは review model であり、必須の見出しではありません。文脈に応じた判断で方法を選び、その後に壊れやすい操作を厳密な順序で行う Skill では、両方を組み合わせられます。

`description` の繰り返しとして本文へ `When to use` を追加しません。Skill が選択された後にも agent が分岐判断へ使う条件がある場合だけ残します。同様に、厳密な output template、`Always` / `Ask first` / `Never`、companion Skill section、self-review checklist は、その区別が実行を実質的に変える場合だけ使います。

## Companion Skill

Skill は原則として自己完結させます。companion 関係は、一方の Skill が規範を正しく適用するために、他方の Skill を意図的に必要とする限定的な承認例外です。利便性、関連する主題、任意の依存グラフを表すために使いません。偶発的な Skill 間結合は、引き続き設計上の問題として扱います。

承認する関係には、次を記録します。

- 関係の方向と対象 Skill
- companion が必要な理由
- サポートする導入方法
- companion が利用できない場合の動作。作業を停止するかどうかを含む
- 関係を導入または維持する provenance とローカル改変
- 関係を正しく保つための評価範囲と更新契機

いずれかの Skill、関係、導入方法、または companion 不在時の動作を変更する場合は、この記録と影響を受ける評価資産をまとめて確認します。

### 承認済みの関係

| 関係 | 理由 | 導入と companion 不在時の動作 | Provenance | 評価 |
| --- | --- | --- | --- | --- |
| `cognitive-rhythm-writing` → `japanese-tech-writing` | 緩急の規範は、日本語技術文書の規範を置き換えず、その制約を前提に拡張する。 | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` で両方を導入する。companion がない場合、`cognitive-rhythm-writing` は規範を適用せず停止する。 | [`skills/cognitive-rhythm-writing/UPSTREAM.md`](../../skills/cognitive-rhythm-writing/UPSTREAM.md)、[`skills/japanese-tech-writing/UPSTREAM.md`](../../skills/japanese-tech-writing/UPSTREAM.md)、[`THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md) が Unlicense の出典とローカル改変を保持する。 | [`skills/cognitive-rhythm-writing/evals/README.md`](../../skills/cognitive-rhythm-writing/evals/README.md) が必須の読込順と companion 不在時の経路を扱う。 |

## description の書き方

`description` は、一般的な説明ではなく利用判断の入口です。次を含めます:

- どのような状況でこの Skill を呼び出すか
- どのような作業を支援するか
- 特定のエージェントへの依存があれば、その依存内容
- 実行機構より利用場面に重点を置く
- implicit selection に必要な情報をすべて `description` に置き、読み込み後の役割、オーケストレーション、実行機構は本文へ移す

避けること:

- 利用場面が不明瞭な曖昧な説明
- 「便利な Skill」のような主観的な表現
- 明示せず Codex を前提にした説明
- 内部実装の詳細を frontmatter に詰め込むこと

## 運用境界の書き方

`Always`、`Ask first`、`Never` は、その区分が workflow 上の意味を持つ場合だけ使います。空の section を追加したり、3つの見出しがすべて存在することを普遍的な品質要件として扱ったりしません。

境界テンプレートを機械的に写すのではなく、必要な挙動と安全特性を表します。既存の guardrail を置き換える場合は、置換後も同等以上の保護が維持されることを検証する方法を定義します。

## Skill の命名

一目で責務と利用場面が分かる名前を選びます。
このリポジトリでは `動作 + 対象` のケバブケースを標準パターンとして使います。

- Skill が何をするかを説明する短い動詞から始める
- Skill が対象とするオブジェクトを追加する
- 利用場面と責務境界が明確になる名前を優先する
- 迷ったら簡潔さより明確さを優先する

例:

- `clarify-request`
- `design-changes`
- `implement-changes`
- `review-changes`
- `triage-review-feedback`
- `summarize-changes`

避けること:

- `build`、`design`、`release` のような単語だけの名前
- 実際のスコープより広く読める名前
- 責務境界が推測しにくい名前

Skill の責務が十分に狭く、名前を誤読できない場合に限り単語名も許容されます。

## 共有 Skill とエージェント固有 Skill

まず、エージェント依存なしに Skill を表現できないかを検討します。

- 共有 Skill: 同じ目的・同じ手順で複数のエージェントが使用できる
- エージェント固有 Skill: 手順、ツール、入出力形式が特定のエージェントに強く結びついている

このリポジトリでは分類ディレクトリを使いません。違いは Skill 名や `description` で表します。
エージェント固有性が重要な場合は、名前か説明にその文脈を含めます。

## 外部 Skill のフォーク・コピーについて

外部 Skill はそのままコピーしません。外部 Skill のインストールは、dotfiles の `apm.yml` / `apm.lock.yaml` で管理します。

次の条件を満たす場合のみ、このリポジトリに取り込みます:

- 自分で継続的に変更・維持する必要がある
- そのまま使うより最初から再設計した方が良い
- 自分のワークフロー向けに明確に再構成したい

取り込む場合でも、`frontmatter` と `description` をこのリポジトリの規約に合わせて見直します。そのままインポートしません。

第三者 Skill を採用または改変する前に、provenance、license、全ファイル、外部参照、scripts、tool と network の利用、複合 capability を確認します。Markdown の指示を本質的に安全な文章ではなく、実行に影響する入力として扱います。リポジトリの checklist は [セキュリティレビュー](security.md) に従います。

## 秘密情報・個人情報の除外

Skill 本文、ヘルパースクリプト、参照資料、アセットには次を含めないでください:

- API キー、トークン、パスワード
- 顧客名、個人情報
- 内部 URL、内部手順、非公開の運用情報
- ローカル環境にしか存在しない秘密ファイルへの参照

Skill は他の環境やエージェントから参照される可能性があると想定して書きます。
環境固有の情報には変数名やプレースホルダーを使います。

## スクリプトを含む Skill の注意点

`scripts/` ディレクトリは便利ですが脆弱です。丁寧に扱います。

- シェル、OS、アーキテクチャへの依存を最小化する
- 追加の依存があれば文書化する
- リポジトリ外の絶対パスに依存しない
- スクリプトが破壊的な操作を行う場合、Skill 本文で安全確認を促す
- 生成物やキャッシュをリポジトリに混在させない

macOS M1 と Windows WSL の両方との互換性を明示した理由なしに崩すスクリプトは避けます。

## references/ の注意点

`references/` ディレクトリには、Skill が判断時に必要とする資料 (フォーマット、仕様、判断基準) を置きます。

- blank-slate エージェントが Skill を適用するために必要なものだけを含める
- 外部文書はそのままコピーせず、正規ソースへリンクする
- 一時メモや顧客固有情報を置かない
- 含める資料のライセンスを確認し、互換性のないライセンスの資料を同梱しない

## assets/ の注意点

`assets/` ディレクトリには、配布可能な補助資料 (画像、再利用可能なテンプレート、小さな構造化データ) を置きます。

- 出典が明確でライセンスが互換なものだけを含める
- 生成物、キャッシュ、一時ファイルを `assets/` に混在させない
- 本当に必要でない限り、大きなバイナリファイルはリポジトリに入れない

## 評価資産

Skill を繰り返し改善するとき、評価資産をコンテンツと一緒に管理します。

- Skill 単位のシナリオとチェックリストは `skills/<skill-name>/evals/` に置く
- 複数 Skill をまたぐフロー評価は `docs/` を参照 (`evaluation.md`)
- 最初に、影響を受ける責務と、実行時動作、発見方法、責務境界のどれが変わるかを特定し、`evaluation.md` の選択方針に従う
- まず Iter 0 から始める: `description` と本文が一致しているか、出力フォーマットが定義されているか、Skill が自己完結しているか、または承認済みの companion 関係を持つかを静的に確認する
- 実行時動作と責務境界へ影響しない場合は、機械的なリポジトリ検証を実行し、動作シナリオを追加せずに終了する
- 実行時動作が変わる場合は、影響を受ける claim または責務だけを、起こり得る失敗、それを露出できる既存または新規の候補版ケース、採点方法へ対応付ける
- 発見方法または隣接 Skill との責務境界が変わる場合だけ、routing、near-miss、coexistence ケースを追加する。無関係な core、routing、coexistence の被覆を自動的に追加しない
- `evaluation.md` の強化条件により追加証拠が判断に関係する場合だけ、baseline 比較または反復を追加する
- blank-slate の executor が実行できるシナリオと要件チェックリストを整備する
- 期待解と採点基準を executor の入力へ含めない
- 違反時にシナリオを fail とすべき要件だけを `[critical]` とし、すべての観察項目を既定で critical にしない
- Skill 本文の中で別のエージェントやサブエージェントをデフォルトの動作にしない
- 追加エージェントは、ユーザーが明示的に求めた場合か、高リスク・高不確実性のケースへの任意の拡張としてのみ提案する

評価の目的は、作者の主観的な判断ではなく、別のエージェントが混乱なく意図した動作を再現できることを検証することです。
非公式なメモより、再利用可能なシナリオ、判断基準、失敗パターンを優先します。反復的な empirical prompt tuning は、観測済みの失敗、高い影響、不安定性、大幅な再設計が追加コストを正当化する場合にだけ使います。

## 新規 Skill チェックリスト

プルリクエストを開く前に:

- [ ] ディレクトリ名がケバブケースで frontmatter の `name` と一致している
- [ ] `name`、`description`、`license` の frontmatter が揃った `SKILL.md` が存在する
- [ ] `description` が本文を読まなくても利用場面を明確に伝えている
- [ ] 見出しテンプレートを機械的に写さず、本文が意味上の契約を満たしている
- [ ] 本文が英語で書かれているか、日本語の執筆・推敲用 Skill の例外が文書化されている
- [ ] `SKILL.md` が日本語正本であると文書化されている場合を除き、`SKILL-ja.md` 日本語参考訳が存在する
- [ ] 秘密情報、個人情報、内部 URL が含まれていない
- [ ] 外部素材を含む場合、第三者 provenance と capability risk を確認している
- [ ] `scripts/`、`references/`、`assets/` に必要なものだけが含まれている (空のディレクトリは削除済み)
- [ ] `evals/README.md` の Iter 0 静的チェックが完了している
- [ ] 評価選択記録に、影響を受ける責務、選択した経路と検査、未検証境界が記載され、選択した経路が必要とする場合だけ動作ケースが完了している

## Codex 専用 Skill を複数エージェントで動作させる

Codex 固有の Skill を Claude Code や GitHub Copilot 向けに改変するとき、Codex 固有の表現を残すべきかを見直します。

互換 client が同じ instruction filename を発見し、同じ precedence rule を適用すると仮定しません。リンク先の現行公式文書では、Codex は durable repository guidance に `AGENTS.md` を使い、Claude Code は `CLAUDE.md` を読み、import または bridge により `AGENTS.md` を再利用できます。GitHub Copilot における `AGENTS.md` の対応状況は surface によって異なるため、このリポジトリでは、`.github/copilot-instructions.md` を、そのファイルを読み込む一方で `AGENTS.md` を自動では読み込まない surface 向けの最小限の bridge として維持します。この挙動が設計に影響する場合は、最新 client documentation を再確認します。

このリポジトリでは、`AGENTS.md` を共有 repository instructions の正本とします。GitHub Copilot 用の bridge は、その正本を読むよう Copilot に指示し、正本を参照できない場合は、file の変更、command の実行、外部状態の変更を行わずに停止するよう指示します。一部の Copilot surface は bridge を読み込んでも `AGENTS.md` を自動では読み込まないため、bridge には、その境界を維持するために必要最小限の安全性・承認ルールだけを重複して記載します。この限定的な fallback は delivery layer の例外であり、2 つ目の正本ではありません。`AGENTS.md` の関連ルールを変更するときは、fallback の整合性を同時に確認して更新します。それ以外の共有ルールを client 固有の bridge file に重複して記載しません。

確認すること:

- 特定のツール名への過度な依存
- リクエスト・出力フォーマットが他のエージェントでも意味をなすか
- Codex 固有の機能を前提にしているステップ
- エージェント固有の差異が `description` や本文で十分に説明されているか
- 共通 guidance が 1 つの canonical source を持ち、client 固有 bridge file が文書化された必要最小限の安全性・承認 fallback だけを重複しているか
- 維持している安全性・承認 fallback が正本のルールと整合しているか
- requirement に behavioral guidance が必要なのか、client が強制する policy、permission、hook が必要なのか

その固有性が Skill の核心的な価値である場合のみ、Codex 固有の表現を残します。
そうでなければ、目的と判断基準を中心に書き直し、実行機構を差し替え可能にします。

情報源: [OpenAI agents guidance](https://developers.openai.com/codex/concepts/customization#agents-guidance)、[Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory)、[GitHub Copilot custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support)。
