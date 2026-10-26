> この文書は [英語版 AGENTS.md](AGENTS.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# AGENTS.md（日本語参考訳）

このリポジトリで作業するエージェント向けの共通指示は、英語版の `AGENTS.md` で定める。\
より深い階層に `AGENTS.md` があれば、そちらを優先する。

## 目的

- 自作したエージェント向けの Skill、継続的に改変して保守している Skill、指定した 2 つの上流 Gist のミラーを管理する
- Codex、Claude Code、GitHub Copilot など、複数のエージェントから参照しやすい単純な構成を保つ
- macOS M1 と Windows WSL の両方に対応するため、OS 固有の前提を持ち込まない

## 最初に読むもの

- [README.md](README.ja.md)
- Issue、検証、コミットメッセージ、PR については [CONTRIBUTING.md](CONTRIBUTING-ja.md)
- Skill を作成または編集する場合は [docs/maintainers/authoring.md](docs/ja/maintainers/authoring.md)
- 文書や Skill の本文で、このリポジトリの概念について書く場合は [docs/maintainers/glossary.md](docs/ja/maintainers/glossary.md)

Skill を作成または編集する場合は、責務の重複を解消し、判断を固めるのに必要な範囲で、既存の `skills/*/SKILL.md` を確認する。\
その目的を満たしたら止め、根拠のない件数の上限は設けない。

## このリポジトリに入れるもの

- 自作した Skill
- 外部の Skill をレビューして取り込み、継続的に改変して保守している Skill
- 指定した 2 つの上流 Gist の無改変コピーである `japanese-tech-writing` と `cognitive-rhythm-writing`
- Skill の運用規則、作成のガイド、移行のメモ

## このリポジトリに入れないもの

- 指定した 2 つの上流 Gist のミラーを除く、外部の Skill をそのままコピーしたもの
- 試しているだけの、実験的で未完成の Skill
- 顧客名、社内 URL、秘密情報、API キー、個人情報を含む内容
- チームの Skill リポジトリに置くべき、チームで共有する運用規則

## 構成の規則

- 基本の単位は `skills/<skill-name>/SKILL.md` とする
- `<skill-name>` はケバブケースにする
- `SKILL.md` のフロントマターには、少なくとも `name`、`description`、`license` を入れる。\
  ただし、2 つの上流 Gist のミラーは元のフロントマターを保つ
- `references/`、`scripts/`、`assets/` は任意で、必要な場合だけ追加する
- `common/`、`codex/`、`claude-code/` のような、エージェント別に分類するディレクトリは作らない
- エージェント固有の違いは、ディレクトリ構成ではなく、Skill の名前や `description` で表す

## 上流 Gist のミラー

- `skills/japanese-tech-writing/SKILL.md` と `skills/cognitive-rhythm-writing/SKILL.md` は、それぞれの `UPSTREAM.md` に記録した上流 Gist の版と、バイト単位で一致させる。\
  これらのファイルに、独自の指示、メタデータ、訂正、翻訳を加えない。
- どちらかのミラーを更新する前に、上流での変更全体をレビューする。\
  無改変のコピーとして受け入れられない場合は、Skill を独自に修正せず、その違いを報告する。
- 記録する内容とミラーの更新手順は、[上流 Gist のミラー](docs/ja/maintainers/authoring.md#上流-gist-のミラー) に従う。

## リポジトリ内の運用 Skill

- このリポジトリ自体の保守だけに使い、公開 Skill の一覧に含めて公開すべきでない運用 Skill に限り、`.agents/skills/<skill-name>/` に置いてよい。
- これらのリポジトリ内の Skill は、Git で明示的に追跡している場合、APM が配置した出力ではなく、ソースファイルとして扱う。
- リポジトリ内の Skill を、公開 Skill の一覧や Plugin の ZIP に加えない。
- リポジトリ内の Skill の名前はケバブケースにし、`SKILL.md` を置く。\
  `SKILL-ja.md` は、[Skill のファイル](docs/ja/maintainers/localization.md#skill-のファイル) に従って置く。\
  補助ファイルは必要な場合だけ追加する。
- 現在追跡している、リポジトリ内の運用 Skill の例外は次のとおりである。
  - `.agents/skills/maintain-japanese-references/`

## 作業の規則

- 変更は、小さくレビューしやすい単位に保つ
- 自作または改変する Skill の本文は、原則として英語で書く。\
  日本語の例外は、[Skill のファイル](docs/ja/maintainers/localization.md#skill-のファイル) を参照する。
- ローカルの絶対パスや、環境に依存する前提を埋め込まない
- Skill の本文は、このリポジトリについての前提知識がないエージェントでも使えるように、[Skill を設計する](docs/ja/maintainers/authoring.md#skill-を設計する) に従って書く
- 英語版を追加または変更した場合は、`.agents/skills/maintain-japanese-references/` を使って日本語参考訳を確認し、英語版の意味が変わる場合だけ更新する

## APM の Skill バンドルの作業手順

- このリポジトリは、ルートの `skills/` にある Skill を APM で公開する。\
  ルートに `apm.yml` や `apm.lock.yaml` を追加しない。\
  マニフェストとロックファイルは、利用側のリポジトリが持つ。
- 公開 Skill の変更をコミットする前に、リポジトリの検査スクリプトと、残しているコードの単体テストを実行する。\
  作業の結果と安全上の境界は、作業の内容に応じて検証する。
- インストールの動作が変わる場合や、Plugin の新しいバージョンを作る場合は、候補のソースをコミットして push する。\
  そのうえで、[docs/maintainers/packaging.md](docs/ja/maintainers/packaging.md) に従い、このリポジトリの外に作った使い捨ての利用側ディレクトリから、push したコミットそのものを検証する。
- このリポジトリでは、dry-run ではない `apm install` や `apm update` を実行しない。\
  ソースの作業ディレクトリに、利用側のマニフェスト、ロックファイル、APM が配置するファイルが作られるからである。
- エージェントのツールが作ることがあるので、空の `.agents/` ディレクトリはあってよい。
- `.agents/` の下に、レビューのメモ、一時ファイル、その他の作業用のファイルを保存しない。\
  代わりに、このリポジトリの外の一時ディレクトリを使う。
- ルートの APM マニフェスト、APM が配置した `.agents/skills/*`、`apm_modules/` のいずれかがある場合は、作業を止めて報告する。\
  削除するのは、生成されたファイルであることを確かめ、承認を得た後に限る。\
  上に挙げた、明示的に追跡しているリポジトリ内の運用 Skill は残す。

## 承認が必要な変更

- `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` の編集
- `skills/*/SKILL.md`、`docs/*`、その他の運用規則の文書の編集
- 外部の Skill の取り込み、依存関係の追加、Skill の公開元の変更
- GitHub Releases などでの Plugin の ZIP の公開
- リポジトリの目的やディレクトリ構成の方針を変える変更

## 避けること

- 指定した 2 つの上流 Gist のミラーを除き、外部の Skill を改変せずにこのリポジトリへコピーすること
- 秘密情報や非公開の情報を、Skill、文書、スクリプト、アセットに含めること
- OS やエージェントに依存する前提を、明示的に文書化せずに持ち込むこと
- リポジトリの規則を変える変更を、承認を得ずに進めること
