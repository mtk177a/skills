> この文書は [英語版 installation.md](../../users/installation.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# Skill のインストールと更新

このガイドは、このリポジトリの Skill を使いたい人に向けたものである。\
インストール方法の選び方、それぞれの方法での Skill のインストールと更新、Skill が使えることの確かめ方を説明する。

インストール方法は、APM と Plugin の ZIP の 2 つである。\
どちらの方法でも、このリポジトリの `skills/` にある同じ Skill がインストールされる。

## インストール方法を選ぶ

### 方法ごとに使えるクライアント

| 方法 | クライアント |
| --- | --- |
| APM | Claude Code、Codex、Cursor、その他の [APM が対応しているクライアント](https://microsoft.github.io/apm/reference/targets-matrix/) |
| Plugin の ZIP | ChatGPT（Chat、Work、dots）、Codex、Cursor |

APM は、このリポジトリから直接 Skill をインストールする。\
Plugin の ZIP は公開していないので、インストールする前に自分で作る必要がある。

ChatGPT にアップロードした Plugin は、Codex でも使える。\
このことは、Codex App の Codex と dots、ブラウザの ChatGPT の Chat と dots で確認している。

### Skill を使う場所に合わせて選ぶ

1. **ChatGPT（Chat、Work、dots）でも使う**
   - Plugin の ZIP を使う。\
     ChatGPT が対応しているのは、この方法だけである。
   - Codex 用に APM でもインストールすることはしない。\
     Plugin がすでに Codex でも使えるからである。
2. **Codex は使うが、ChatGPT は使わない**
   - APM を使う。\
     Plugin の ZIP を作る必要がない。
3. **Claude Code で使う**
   - APM を使う。\
     この Plugin には Claude 専用のマニフェストがない。
4. **Cursor で使う**
   - ChatGPT のためにすでに Plugin の ZIP を使っている場合を除き、APM を使う。
   - Plugin の ZIP を Cursor のローカルの Plugin ディレクトリに展開することもできる。

### 同じ Skill を重複してインストールしない

一つの環境では、各 Skill を一つの方法だけでインストールする。\
Plugin を有効にする前に、別の Plugin や APM（パスを指定した個別の Skill のインストールを含む）でインストールした同じ Skill を、無効にするか削除する。

- APM は、Codex 用と Cursor 用の Skill を、同じ `.agents/skills/` ディレクトリにインストールする。\
  そのため、Cursor 用に APM でインストールすると、そのプロジェクトの Codex からも Skill が見えるようになる。
- 重複している Skill の無効化や削除は、クライアントが提供している操作で行う。
- 関係のない Skill や認証情報は削除しない。
- 重複したときにクライアントがどちらを使うかを、文書化されていない優先順位や名前空間に頼って決めない。

Skill をインストールすると、その指示をクライアントが使えるようになる。\
ただし、シェル、リポジトリ、外部サービス、サブエージェント、書き込みのアクセス権が、エージェントに与えられるわけではない。\
予定している作業の [実行条件](compatibility.md) を確認する。

## APM でインストールする

### インストールする範囲を選ぶ

| インストールする範囲 | コマンド |
| --- | --- |
| 公開 Skill 全体 | `apm install mtk177a/skills` |
| 選んだ Skill | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| パスを指定した一つの Skill | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` は `japanese-tech-writing` を読み込むので、上の「選んだ Skill」の例のように、2 つを一緒にインストールする。

インストールした Skill を最新のバージョンに更新するには、利用側のリポジトリで `apm update` を実行する。

### 依存関係として宣言する

公開 Skill 全体を依存関係として宣言する場合は、利用側のリポジトリの `apm.yml` に、このリポジトリを追加する。

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

### インストールできたことを確かめる

インストールしたら、クライアントで次の点を確かめる。

1. **Skill が、クライアントの読み込む場所にある**
   - クライアントごとのディレクトリは、[APM の Targets matrix](https://microsoft.github.io/apm/reference/targets-matrix/) を参照する。
2. **クライアントが Skill を一覧に表示する**
3. **Skill を明示的に呼び出せる**

`apm install` が成功しても、クライアントで Skill を使えることまでは分からない。

## Plugin の ZIP でインストールする

### Plugin の ZIP を作る

Plugin の ZIP は公開していない。\
[Plugin の ZIP を作る](../maintainers/packaging.md) に従って作る。

### ChatGPT と Codex で使う

1. **Plugin の ZIP を ChatGPT にアップロードする**
   - 初めてインストールするときは、ChatGPT Plugins で個人用の Plugin としてアップロードする。
   - 更新するときは、元に戻せるように、まず前の ZIP を保管しておく。\
     そのうえで、別の Plugin を作らずに、既存の Plugin のメニューから **Upload new version** を選ぶ。
2. **バージョンと Skill を確かめる**
   - Plugin に新しいバージョンと想定どおりの Skill が表示されることを確かめる。
   - そのうえで、新しい会話を始める。
3. **依頼文で Skill を指定する**
   - 画面で Plugin を選び、依頼文で使う Skill を指定する。
   - たとえば、「`mtk177a-skills` の `define-referents` を使い、参照資料を読んでから命名案を出してください」と依頼する。
4. **Plugin を使う場所ごとに確かめる**
   - Skill の呼び出し方や使える機能は場所によって異なる場合があるので、ChatGPT の Chat、Work、dots と Codex を、それぞれ確かめる。
   - 検出: Skill が一覧に表示される。
   - 読み込み: Skill の本文と参照資料を読んだことが、クライアントの表示で分かる（表示できる場合）。
   - 出力: 得られた回答。\
     回答がもっともらしいだけでは、Skill を読み込んだとは言えない。

### Cursor で使う

[Cursor の公式資料](https://cursor.com/docs/plugins) には、共通形式の Agent Plugin に対応していることと、`~/.cursor/plugins/local/<plugin-name>/` でのローカルでの検証方法が書かれている。

1. **Plugin の ZIP を展開する**
   - `plugin.json` が `~/.cursor/plugins/local/mtk177a-skills/` の直下に来るように展開する。
   - 更新するときは、必要なら古いディレクトリをバックアップしてから、ディレクトリごと入れ替える。\
     古いファイルの上に新しいファイルをコピーすると、新しいバージョンで削除された Skill が残ることがある。
2. **Cursor を再読み込みする**
   - Cursor を再起動するか、**Developer: Reload Window** を実行する。
3. **Skill を確かめる**
   - Cursor が Skill を一覧に表示し、Skill を明示的に呼び出せることを確かめる。
   - Skill が表示されない場合は、ローカルの Plugin の取り込みが許可されているかを確認する。\
     Cursor は、許可されている場合にだけ、このディレクトリの Plugin を検出する。

この Plugin は Skill だけで構成されているため、`.cursor-plugin/plugin.json` は不要である。\
Cursor のマーケットプレイスへの申請は、このガイドの対象外とする。
