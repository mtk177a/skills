> この文書は [英語版 installation.md](../../users/installation.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# Skill を導入・更新する

この手引きは、このリポジトリの Skill を使いたい人に向けたものである。\
クライアントごとの導入と更新の方法、Skill が使えることの確かめ方を説明する。

Skill の導入方法は、APM で導入する方法と、Plugin の ZIP で導入する方法の 2 つがある。\
どちらの方法でも、このリポジトリの `skills/` にある同じ Skill が導入される。\
APM は、このリポジトリから直接導入する。\
Plugin の ZIP は公開していないので、使う場合は [Plugin の ZIP を作る](../maintainers/packaging.md) に従って自分で作る必要がある。

## 導入方法を選ぶ

| クライアント | 導入方法 |
| --- | --- |
| Claude Code、その他 APM が対応するクライアント | [APM で導入する](#apm-で導入する) |
| ChatGPT と Codex | [Plugin の ZIP を ChatGPT にアップロードする](#plugin-の-zip-を-chatgpt-にアップロードする) |
| Cursor | [Plugin の ZIP を Cursor 用に展開する](#plugin-の-zip-を-cursor-用に展開する) |

このパッケージには Claude 専用の Plugin マニフェストがないため、Claude Code では APM を使う。

Skill を導入すると、その指示をクライアントが使えるようになる。\
ただし、シェル、リポジトリ、外部サービス、サブエージェント、書き込みのアクセス権がエージェントに与えられるわけではない。\
クライアントを選ぶ前に、予定している作業の [実行条件](compatibility.md) を確認する。

## 重複して導入しない

一つの環境では、各 Skill を一つの方法だけで導入する。\
同じ Skill を別の Plugin、単体の導入、APM のいずれかですでに導入している場合は、Plugin を有効にする前に、重複している方を無効にするか削除する。

- 無効化や削除は、クライアントが提供する操作で行う。
- 関係のない Skill や認証情報は削除しない。
- 重複したときにどちらが使われるかを、文書化されていない優先順位や名前空間に頼って決めない。

元に戻せるように前の ZIP を保管し、新しい会話で Plugin を確かめる。

## APM で導入する

導入したい範囲に合わせてコマンドを選ぶ。

| 導入する範囲 | コマンド |
| --- | --- |
| すべての Skill | `apm install mtk177a/skills` |
| 選んだ Skill | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| パスを指定した一つの Skill | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` は `japanese-tech-writing` を読み込むので、上の「選んだ Skill」の例のように 2 つを一緒に導入する。

すべての Skill を依存関係として宣言する場合は、利用側の `apm.yml` にこのリポジトリを追加する。

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

導入したら、クライアントで Skill の配置場所、Skill が一覧に表示されること、Skill を明示的に呼び出せることを確かめる。\
`apm install` が成功しても、クライアントで Skill を使えることまでは分からない。

## Plugin の ZIP を ChatGPT にアップロードする

ZIP を個人用 Plugin として ChatGPT にアップロードし、Codex を含め、使う予定の各画面で確かめる。

1. ZIP をアップロードする。\
   初めて導入するときは、ChatGPT の Plugin 画面にある個人用 Plugin のアーカイブアップロードを使う。\
   更新するときは、別の Plugin を作らず、既存の Plugin のメニューから **Upload new version** を選ぶ。
2. Plugin に新しいバージョンと想定どおりの Skill が表示されることを確かめてから、新しい会話を始める。
3. 画面で Plugin を選び、依頼文で使う Skill を指定する。\
   たとえば、「`mtk177a-skills` の `define-referents` を使い、参照資料を読んでから命名案を出してください」と依頼する。
4. 使う予定の各画面で、次の点を確かめる。
   - 検出: Skill が一覧に表示される。
   - 読み込み: Skill の本文と参照資料を読んだことが、クライアントの表示で分かる（表示できる場合）。
   - 出力: 得られた回答。\
     回答がもっともらしいだけでは、Skill を読み込んだとは言えない。

Chat、Work、dots、Codex などの画面によって、呼び出し方や使える機能が異なる場合がある。

## Plugin の ZIP を Cursor 用に展開する

[Cursor の公式資料](https://cursor.com/docs/plugins) では、共通形式の Agent Plugin に対応していることと、`~/.cursor/plugins/local/<plugin-name>/` でのローカル検証の方法が説明されている。

1. `plugin.json` が `~/.cursor/plugins/local/mtk177a-skills/` の直下に来るように ZIP を展開する。\
   更新するときは、必要なら古いディレクトリをバックアップしてから、ディレクトリごと入れ替える。\
   古いファイルの上に新しいファイルをコピーすると、新しい版で削除された Skill が残ることがある。
2. Cursor を再起動するか、**Developer: Reload Window** を実行する。
3. Cursor が Skill を一覧に表示し、Skill を明示的に呼び出せることを確かめる。

このパッケージは Skill だけで構成されているため、`.cursor-plugin/plugin.json` は不要である。\
Cursor のマーケットプレイスへの申請は、この手引きの対象外とする。
