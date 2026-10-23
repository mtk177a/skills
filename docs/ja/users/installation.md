> この文書は [英語版 installation.md](../../users/installation.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# Skill のインストールと更新

このガイドは、このリポジトリの Skill を使いたい人に向けたものである。\
クライアントごとの Skill のインストールと更新の方法、Skill が使えることの確かめ方を説明する。

Skill をインストールする方法は、APM を使う方法と、Plugin の ZIP を使う方法の 2 つがある。\
どちらの方法でも、このリポジトリの `skills/` にある同じ Skill がインストールされる。\
APM は、このリポジトリから直接インストールする。\
Plugin の ZIP は公開していないので、[Plugin の ZIP を作る](../maintainers/packaging.md) に従って自分で作る必要がある。

## インストール方法を選ぶ

使っているクライアントに合わせて方法を選ぶ。

| クライアント | 方法 |
| --- | --- |
| Claude Code、その他 APM が対応しているクライアント | [APM でインストールする](#apm-でインストールする) |
| ChatGPT と Codex | [Plugin の ZIP を ChatGPT にアップロードする](#plugin-の-zip-を-chatgpt-にアップロードする) |
| Cursor | [Plugin の ZIP を Cursor 用に展開する](#plugin-の-zip-を-cursor-用に展開する) |

この Plugin には Claude 専用のマニフェストがないため、Claude Code では APM を使う。

Skill をインストールすると、その指示をクライアントが使えるようになる。\
ただし、シェル、リポジトリ、外部サービス、サブエージェント、書き込みのアクセス権が、エージェントに与えられるわけではない。\
クライアントを選ぶ前に、予定している作業の [実行条件](compatibility.md) を確認する。

## 重複してインストールしない

一つの環境では、各 Skill を一つの方法だけでインストールする。\
同じ Skill を、別の Plugin、単体のインストール、APM のいずれかですでにインストールしている場合は、Plugin を有効にする前に、重複している方を無効にするか削除する。

- 無効化や削除は、クライアントが提供している操作で行う。
- 関係のない Skill や認証情報は削除しない。
- 重複したときにクライアントがどちらを使うかを、文書化されていない優先順位や名前空間に頼って決めない。

## APM でインストールする

インストールしたい範囲に合わせて、コマンドを実行する。

| インストールする範囲 | コマンド |
| --- | --- |
| 公開 Skill 全体 | `apm install mtk177a/skills` |
| 選んだ Skill | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| パスを指定した一つの Skill | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` は `japanese-tech-writing` を読み込むので、上の「選んだ Skill」の例のように、2 つを一緒にインストールする。

公開 Skill 全体を依存関係として宣言する場合は、利用側のリポジトリの `apm.yml` に、このリポジトリを追加する。

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

インストールしたら、クライアントで次の点を確かめる。

- Skill が、クライアントの読み込む場所にある。
- クライアントが Skill を一覧に表示する。
- Skill を明示的に呼び出せる。

`apm install` が成功しても、クライアントで Skill を使えることまでは分からない。

## Plugin の ZIP を ChatGPT にアップロードする

Plugin の ZIP を、個人用の Plugin として ChatGPT にアップロードする。\
Codex は同じ個人用の Plugin を使うので、Codex 用に別にアップロードする必要はない。

1. Plugin の ZIP をアップロードする。\
   初めてインストールするときは、ChatGPT Plugins で個人用の Plugin としてアップロードする。\
   更新するときは、元に戻せるように、まず前の ZIP を保管しておく。\
   そのうえで、別の Plugin を作らずに、既存の Plugin のメニューから **Upload new version** を選ぶ。
2. Plugin に新しいバージョンと想定どおりの Skill が表示されることを確かめてから、新しい会話を始める。
3. 画面で Plugin を選び、依頼文で使う Skill を指定する。\
   たとえば、「`mtk177a-skills` の `define-referents` を使い、参照資料を読んでから命名案を出してください」と依頼する。
4. ChatGPT の Chat、Work、dots や Codex など、Plugin を使う予定の場所ごとに、次の点を確かめる。
   - 検出: Skill が一覧に表示される。
   - 読み込み: Skill の本文と参照資料を読んだことが、クライアントの表示で分かる（表示できる場合）。
   - 出力: 得られた回答。\
     回答がもっともらしいだけでは、Skill を読み込んだとは言えない。

Skill の呼び出し方や使える機能は、ChatGPT の Chat、Work、dots と Codex とで異なる場合がある。

## Plugin の ZIP を Cursor 用に展開する

Plugin の ZIP を、Cursor のローカルの Plugin ディレクトリに展開する。\
[Cursor の公式資料](https://cursor.com/docs/plugins) には、共通形式の Agent Plugin に対応していることと、`~/.cursor/plugins/local/<plugin-name>/` でのローカルでの検証方法が書かれている。

1. `plugin.json` が `~/.cursor/plugins/local/mtk177a-skills/` の直下に来るように、ZIP を展開する。\
   更新するときは、必要なら古いディレクトリをバックアップしてから、ディレクトリごと入れ替える。\
   古いファイルの上に新しいファイルをコピーすると、新しいバージョンで削除された Skill が残ることがある。
2. Cursor を再起動するか、**Developer: Reload Window** を実行する。
3. Cursor が Skill を一覧に表示し、Skill を明示的に呼び出せることを確かめる。

この Plugin は Skill だけで構成されているため、`.cursor-plugin/plugin.json` は不要である。\
Cursor のマーケットプレイスへの申請は、このガイドの対象外とする。
