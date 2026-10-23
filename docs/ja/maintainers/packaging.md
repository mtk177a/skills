> この文書は [英語版 packaging.md](../../maintainers/packaging.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# Plugin の ZIP を作る

この文書は保守者向けに、新しいバージョンの Plugin の ZIP を作り、push したコミットを APM で導入できることを確かめる手順と、ZIP の仕様を説明する。\
ZIP を ChatGPT や Cursor に導入する方法は、[導入ガイド](../users/installation.md) を参照する。\
GitHub Releases などでの公開は、この文書の対象に含めない。

## 必要な環境

- Python 3.10 以降
- Git

## 手順

次の 4 つの手順で ZIP を生成し、同じコミットを APM で導入できることを確かめる。

### 1. 元になるコミットを作る

Skill の本文と関連ファイルは `skills/` だけで管理し、配布用のコピーを別に作らない。

更新する場合は、コミットする前に次の 2 つを行う。

- 変更した Skill について、その責務に関係する確認を行う。
- `plugin.json` のバージョンを上げる。

そのうえで、バージョンと Skill の変更をコミットする。\
バージョン番号は使い回さない。\
内容を変えたら、必ずバージョンを上げる。

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

### 3. push したコミットを APM で導入できることを確かめる

候補ブランチを push し、そのコミットを APM で導入する。\
次の 3 通りの導入を、このリポジトリの外に作った使い捨てのディレクトリで、それぞれ別に行う。

| 導入方法 | 対象 | この対象を選ぶ理由 |
| --- | --- | --- |
| 全 Skill | すべての公開 Skill | カタログ全体を確かめる |
| 選択導入 | `cognitive-rhythm-writing` と `japanese-tech-writing` | 前者が後者を必要とする |
| 個別パス | `define-referents` | 同梱の参照資料を持つ |

各ディレクトリで、対応するコマンドを実行して導入する。

```bash
# 全 Skill
apm install 'mtk177a/skills#<commit>' --target agent-skills --no-policy

# 選択導入
apm install 'mtk177a/skills#<commit>' --skill cognitive-rhythm-writing --skill japanese-tech-writing --target agent-skills --no-policy

# 個別パス
apm install 'mtk177a/skills/skills/define-referents#<commit>' --target agent-skills --no-policy
```

`<commit>` には、push 済みのコミットの完全な ID を指定する。

導入したら、各ディレクトリで、生成されたロックファイルと導入結果を検証する。

```bash
apm install --frozen --dry-run --no-policy
apm audit --ci --no-policy
```

このリポジトリの中では、dry-run 以外の `apm install` や `apm update` を実行しない。\
実行すると、利用側のマニフェスト、ロックファイル、導入されたファイルがこのリポジトリ内に作られてしまう。

これらの確認で分かるのは、導入と依存関係に問題がないかどうかまでである。\
クライアントが Skill を呼び出せるか、指示どおりに動くかは確かめられない。

### 4. 生成物を保管する

ZIP、ハッシュ、元のコミット、変更の概要、確認結果を、互いの対応が分かるようにまとめて保管する。

## ZIP の仕様

### 生成されるファイル

| ファイル | 用途 |
| --- | --- |
| `<name>-<version>.zip` | 導入する Plugin の ZIP |
| `<name>-<version>.sha256` | ZIP の内容を識別するための SHA-256 ハッシュ |
| `<name>-<version>.build.json` | 元のコミット、ZIP のハッシュ、Skill の一覧、同梱した各ファイルのハッシュとファイルモードの記録 |

同じコミットから何度生成しても、バイト単位で同じ ZIP ができる。\
ZIP 内のファイルを並べ替え、時刻を固定し、圧縮せずに格納しているため、圧縮ライブラリのバージョンにも左右されない。

### 同梱するファイル

生成スクリプトは、指定したコミットから次のファイルを選んで ZIP に入れる。

- ルートの `plugin.json`、`LICENSE`、`THIRD_PARTY_NOTICES.md`
- `skills/` の下にある、Git で管理しているファイル。\
  参照資料、実行に必要なファイル、メタデータ、2 つの上流ミラーとその来歴文書 `UPSTREAM.md` も含む。

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
互換形式の `.codex-plugin/plugin.json` は、別に管理しない。\
ルートの `plugin.json` に OpenAI の拡張を書いた場合、その設定だけが採用され、互換形式の設定とは結合されない。

形式の詳細は、[OpenAI の配布仕様](https://developers.openai.com/plugins/build/plugins) を参照する。

### 生成時の検査

生成スクリプトは、ZIP を作るときに次の点を検査する。

- マニフェストの識別情報のうち、スクリプトが対応している項目
- ルートに必須のファイルがあること
- 各 Skill に `SKILL.md` があること
- 上流ミラーのハッシュが、来歴文書に記録されたハッシュと一致すること
- 相対 Markdown リンクと、コードスパンに書いた `references/` や `../` で始まる参照が、ZIP に含まれるファイルを指していること
- ZIP に含める範囲に、シンボリックリンクやサブモジュールがないこと
- ZIP 内の各ファイルの内容とファイルモードが、Git に記録された元のファイルと一致すること

これらの検査で見つかるのは、ZIP を作るときに起きる特定の不備だけである。\
JSON Schema の全項目の検証、Markdown の完全な構文解析、実際に使ったときの動作の確認は行わない。

そのため、Skill を変更したときは、次の点を別に見直す。

- 一般的な例や通常の文章の中で示した参照
- 必要なツールを使えるかどうか
- 条件付きの指示
