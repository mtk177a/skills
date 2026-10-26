> この文書は [英語版 packaging.md](../../maintainers/packaging.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# Plugin の ZIP を作る

このガイドは、保守者と、保守者の代わりに作業するエージェントに向けたものである。\
新しいバージョンの Plugin の ZIP を作り、push したコミットを APM でインストールできることを確かめる手順と、ZIP の仕様を説明する。\
ZIP を ChatGPT や Cursor にインストールする方法は、[Skill のインストールと更新](../users/installation.md) を参照する。\
GitHub Releases などでの公開は、このガイドの対象外とする。

## 必要な環境

- Python 3.10 以降
- Git
- APM（手順 3 で使う）

## 手順

次の 4 つの手順で ZIP を生成し、同じコミットを APM でインストールできることを確かめる。

### 1. 元になるコミットを作る

Skill の本文と関連ファイルは、`skills/` だけで管理する。\
ZIP へのコピーは、生成の処理が行う。

更新する場合は、コミットする前に次の 2 つを行う。

- 変更した Skill の作業結果と安全上の範囲を、変更の内容に応じて確かめる。
- `plugin.json` のバージョンを上げる。

そのうえで、バージョンと Skill の変更をコミットする。\
内容を変えるたびに、新しい、より大きいバージョン番号を付ける。

不具合のある版から戻す場合も、必要な旧版の内容を `skills/` に戻し、新しいバージョンとして同じ手順で作り直す。

### 2. リポジトリを検査し、ZIP を生成する

手順 1 のコミットをチェックアウトした状態で、次のコマンドを順に実行する。

```bash
# リポジトリを検査する
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests
git diff --check

# ZIP を生成する
python3 -B scripts/build_plugin.py --ref <commit> --output-dir <outside-repository-output-directory>
```

- `<commit>`: 手順 1 で作ったコミット。
- `<outside-repository-output-directory>`: 生成物の保存先。\
  リポジトリの外にあるディレクトリを指定する。

生成スクリプトは、`--ref` に渡した参照を最初に一度だけコミットへ解決し、そのコミットに含まれるファイルだけを読む。\
そのため、コミットしていない変更や Git で管理していないファイルは ZIP に入らない。\
保存先に同じ名前のファイルがある場合は、上書きせずにエラーで終了する。\
なお、生成スクリプトは通信、インストール、アップロードを行わない。

### 3. push したコミットを APM でインストールできることを確かめる

候補ブランチを push し、そのコミットを APM でインストールする。\
次の 3 通りのインストールを、このリポジトリの外に作った使い捨てのディレクトリで、それぞれ別に行う。

| インストール | 対象 | この対象を選ぶ理由 |
| --- | --- | --- |
| 全 Skill | すべての公開 Skill | カタログ全体を確かめる |
| 選んだ Skill | `cognitive-rhythm-writing` と `japanese-tech-writing` | 前者が後者を必要とする |
| 個別パス | `define-referents` | 同梱の参照資料を持つ |

各ディレクトリで、対応するコマンドを実行してインストールする。

```bash
# 全 Skill
apm install 'mtk177a/skills#<commit>' --target agent-skills --no-policy

# 選んだ Skill
apm install 'mtk177a/skills#<commit>' --skill cognitive-rhythm-writing --skill japanese-tech-writing --target agent-skills --no-policy

# 個別パス
apm install 'mtk177a/skills/skills/define-referents#<commit>' --target agent-skills --no-policy
```

`<commit>` には、push 済みのコミットの完全な ID を指定する。

インストールしたら、各ディレクトリで、生成されたロックファイルとインストールの結果を検証する。

```bash
apm install --frozen --dry-run --no-policy
apm audit --ci --no-policy
```

このリポジトリの中では、`apm install` と `apm update` は `--dry-run` を付けた場合だけ実行する。\
実行すると、利用側のマニフェスト、ロックファイル、インストールされたファイルがこのリポジトリ内に作られてしまう。

これらの確認で分かるのは、インストールと依存関係に問題がないかどうかまでである。\
クライアントが Skill を呼び出せるか、指示どおりに動くかは確かめられない。

### 4. 生成物を保管する

ZIP、ハッシュ、元のコミット、変更の概要、確認結果を、互いの対応が分かるようにまとめて保管する。

## ZIP の仕様

### 生成されるファイル

| ファイル | 用途 |
| --- | --- |
| `<name>-<version>.zip` | インストールする Plugin の ZIP |
| `<name>-<version>.sha256` | ZIP の内容を識別するための SHA-256 ハッシュ |
| `<name>-<version>.build.json` | 元のコミット、ZIP のハッシュ、Skill の一覧、同梱した各ファイルのハッシュとファイルモードの記録 |

同じコミットから何度生成しても、バイト単位で同じ ZIP ができる。\
ZIP 内のファイルを並べ替え、時刻を固定し、圧縮せずに格納しているため、圧縮ライブラリのバージョンにも左右されない。

### 同梱するファイル

生成スクリプトは、指定したコミットから次のファイルを選んで ZIP に入れる。

- ルートの `plugin.json`、`LICENSE`、`THIRD_PARTY_NOTICES.md`
- `skills/` の下にある、Git で管理しているファイル。\
  参照資料、実行に必要なファイル、メタデータ、2 つの上流ミラーとその出典の記録 `UPSTREAM.md` も含む。

次のファイルは ZIP に入れない。

- `skills/` の下にあっても、ファイル名が `-ja.md` または `.ja.md` で終わるファイル
- リポジトリ向けの指示、テスト、文書
- `.agents/` の下にある、リポジトリ保守専用の Skill

ZIP に入れるファイルは、元のファイルとバイト単位で同じ内容のまま格納する。\
ZIP の最上位には `plugin.json` と `skills/` を直接置き、それらを囲む親ディレクトリは作らない。

`skills/` に追加して Git で管理したファイルは、そのまま ZIP に入る。\
そのため、コミットする前に、スクリプト、外部への参照、認証情報、生成物が紛れ込んでいないかを確認する。

### マニフェスト

Plugin のマニフェストは、ルートの `plugin.json` だけで管理する。\
このファイルは、Agent Plugins 1.0.0 のスキーマを宣言している。

OpenAI 固有の設定が必要な場合は、`plugin.json` の `extensions["com.openai"]` に書く。\
これらの設定はルートの `plugin.json` に置き、互換形式の `.codex-plugin/plugin.json` は別に設けない。\
ルートの `plugin.json` に OpenAI の拡張を書いた場合、その設定だけが採用され、互換形式の設定とは結合されない。

形式の詳細は、[OpenAI の Plugin の作成ガイド](https://developers.openai.com/plugins/build/plugins) を参照する。

### 生成時の検査

生成スクリプトは、ZIP を作るときに次の点を検査する。

- マニフェストの識別情報のうち、スクリプトが対応している項目
- ルートに必須のファイルがあること
- 各 Skill に `SKILL.md` があること
- 上流ミラーのハッシュが、出典の記録に書かれたハッシュと一致すること
- 相対 Markdown リンクと、コードスパンに書いた `references/` や `../` で始まる参照が、ZIP に含まれるファイルを指していること
- ZIP に含める範囲に、シンボリックリンクやサブモジュールがないこと
- ZIP 内の各ファイルの内容とファイルモードが、Git に記録された元のファイルと一致すること

これらの検査で見つかるのは、ZIP を作るときに起きる特定の不備だけである。\
JSON Schema の全項目の検証、Markdown の完全な構文解析、実際に使ったときの動作の確認は行わない。

生成スクリプトはこれらを検査しないので、Skill を変更したときは、次の点を自分で見直す。

- リンクやコードスパンではなく、一般的な例や通常の文章の中で示した、ほかのファイルへの参照
- Skill の指示が必要とするツールを、対象のクライアントで使えるかどうか
- 特定の条件でだけ適用する指示と、その条件が実際に起こり得るかどうか
