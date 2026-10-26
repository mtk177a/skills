> この文書は [英語版 AGENTS.md](AGENTS.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# AGENTS.md（日本語参考訳）

このファイルは、このリポジトリでのエージェント向けの共通の指示の基準となる場所である。\
サブディレクトリにある `AGENTS.md` は、そのサブディレクトリで優先される。

## 目的

このリポジトリは、次のものを管理する。

- 所有者が書いたエージェント向けの Skill
- 所有者がレビューして取り入れ、改変して保守している外部の Skill
- 2 つの上流 Gist の無改変コピー: `japanese-tech-writing` と `cognitive-rhythm-writing`
- これらの Skill の運用規則、作成のガイド、移行のメモ

実験的な Skill、ほかの外部の Skill をそのままコピーしたもの、チームの規則は、別のリポジトリに置く。\
Codex、Claude Code、GitHub Copilot などのエージェントが使えるように、構成を単純に保つ。\
macOS（Apple シリコン）と Windows WSL で動くように、内容を OS に依存しないものに保つ。\
顧客名、社内の URL、秘密情報、API キー、個人情報は、どのファイルにも入れない。

## 最初に読むもの

- [README.md](README.ja.md)
- [CONTRIBUTING.md](CONTRIBUTING-ja.md): Issue、検証、コミットメッセージ、プルリクエスト
- [docs/maintainers/authoring.md](docs/ja/maintainers/authoring.md): Skill を作成または編集する場合
- [docs/maintainers/glossary.md](docs/ja/maintainers/glossary.md): 文書や Skill の本文で、このリポジトリの概念について書く場合

## 構成

- 各 Skill は、ケバブケースの名前で `skills/<skill-name>/SKILL.md` に置く。
- フロントマターには、少なくとも `name`、`description`、`license` を入れる。\
  2 つの上流 Gist のミラーは、元のフロントマターを保つ。
- `references/`、`scripts/`、`assets/` は、Skill が必要とする場合だけ加える。
- すべてのエージェントで、一つのディレクトリ構成を使う。\
  エージェントごとの違いは、Skill の名前か `description` で示す。

## 上流 Gist のミラー

- `skills/japanese-tech-writing/SKILL.md` と `skills/cognitive-rhythm-writing/SKILL.md` は、それぞれの `UPSTREAM.md` にある上流の版と、バイト単位で同じに保つ。\
  独自の指示、メタデータ、訂正、翻訳は、これらのファイルの外に置く。
- ミラーを更新する前に、上流での変更の全体をレビューする。\
  無改変のコピーとして受け入れられない場合は、その違いを報告し、今のコピーを保つ。
- 記録する内容とミラーの更新方法は、[上流 Gist のミラー](docs/ja/maintainers/authoring.md#上流-gist-のミラー) に従う。

## リポジトリ内の運用 Skill

- このリポジトリの保守だけに使う Skill は、`.agents/skills/<skill-name>/` に置いてよい。\
  その Skill は、公開 Skill の一覧と Plugin の ZIP には含めない。
- git が追跡しているリポジトリ内の Skill は、APM が配置した出力ではなく、ソースファイルである。
- リポジトリ内の Skill には、ケバブケースの名前と `SKILL.md` を付ける。\
  `SKILL-ja.md` は [Skill のファイル](docs/ja/maintainers/localization.md#skill-のファイル) に従って加え、ほかのファイルは必要な場合だけ加える。
- 追跡しているリポジトリ内の Skill は、`.agents/skills/maintain-japanese-references/` だけである。

## 作業の規則

- 各変更は、小さくレビューしやすく保つ。
- Skill の本文は英語で書く。\
  日本語の例外は、[Skill のファイル](docs/ja/maintainers/localization.md#skill-のファイル) を参照する。
- 相対パスを使い、環境についての前提はそれぞれ明示する。
- Skill の本文は、[Skill を設計する](docs/ja/maintainers/authoring.md#skill-を設計する) に従って書く。\
  そうすれば、このリポジトリについての文脈を持たないエージェントでも使える。
- 英語版を追加または変更した場合は、`.agents/skills/maintain-japanese-references/` を使って、日本語参考訳を確かめる。\
  参考訳を更新するのは、英語版の意味が変わる場合だけにする。

## APM

- このリポジトリは、`skills/` にある Skill を APM で公開する。\
  `apm.yml` と `apm.lock.yaml` は利用側のリポジトリが持つので、このリポジトリのルートには置かない。
- 公開 Skill の変更をコミットする前に、リポジトリの検査スクリプトと単体テストを実行する。\
  作業の結果と安全上の範囲は、作業が必要とするとおりに検証する。
- インストールの動作が変わる場合や、Plugin の新しいバージョンを作る場合は、候補をコミットして push する。\
  そのうえで、[docs/maintainers/packaging.md](docs/ja/maintainers/packaging.md) に従い、このリポジトリの外の使い捨ての利用側ディレクトリから、push したコミットを検証する。
- このリポジトリでは、`apm install` と `apm update` は `--dry-run` を付けた場合だけ実行する。\
  付けないと、ソースの作業ディレクトリに、利用側のマニフェスト、ロックファイル、配置されたファイルが作られる。
- レビューのメモ、一時ファイル、その他の作業用のファイルは、このリポジトリの外の一時ディレクトリに保存する。\
  それらを `.agents/` に置かない。\
  エージェントのツールが作ることがあるので、空の `.agents/` ディレクトリはあってよい。
- ルートの APM マニフェスト、APM が配置した `.agents/skills/*`、`apm_modules/` のいずれかがある場合は、止まって報告する。\
  削除するのは、生成されたものであることを確かめ、承認を得た後だけにする。\
  追跡しているリポジトリ内の Skill は残す。

## 承認が必要な変更

次のいずれかを行う前に、承認を得る。

- `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md` の編集
- `skills/*/SKILL.md`、`docs/*`、その他の運用規則の文書の編集
- 外部の Skill の取り込み、依存関係の追加、Skill の公開元の変更
- GitHub Releases などでの Plugin の ZIP の公開
- リポジトリの目的や、ディレクトリ構成の方針の変更
