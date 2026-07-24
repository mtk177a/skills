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

- `scope-request`
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
- まず Iter 0 から始める: `description` と本文が一致しているか、出力フォーマットが定義されているか、Skill が自己完結しているかを静的に確認する
- シナリオを追加する前に、重要な Skill の claim または変更を、起こり得る失敗、それを露出できるシナリオ、採点方法へ対応付ける
- 固有の責務、境界、共存リスク、既知の regression を担う場合だけシナリオを追加し、普遍的な件数目標を設けない
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

## Codex 専用 Skill を複数エージェントで動作させる

Codex 固有の Skill を Claude Code や GitHub Copilot 向けに改変するとき、Codex 固有の表現を残すべきかを見直します。

互換 client が同じ instruction filename を発見し、同じ precedence rule を適用すると仮定しません。リンク先の現行公式文書では、Codex は durable repository guidance に `AGENTS.md` を使い、Claude Code は `CLAUDE.md` を読み、import または bridge により `AGENTS.md` を再利用できます。この挙動が設計に影響する場合は、最新 client documentation を再確認します。

確認すること:

- 特定のツール名への過度な依存
- リクエスト・出力フォーマットが他のエージェントでも意味をなすか
- Codex 固有の機能を前提にしているステップ
- エージェント固有の差異が `description` や本文で十分に説明されているか
- 共通 guidance が1つの canonical source を持ち、client 固有 bridge file が重複を避けているか
- requirement に behavioral guidance が必要なのか、client が強制する policy、permission、hook が必要なのか

その固有性が Skill の核心的な価値である場合のみ、Codex 固有の表現を残します。
そうでなければ、目的と判断基準を中心に書き直し、実行機構を差し替え可能にします。

情報源: [OpenAI agents guidance](https://developers.openai.com/codex/concepts/customization#agents-guidance)、[Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory)。
