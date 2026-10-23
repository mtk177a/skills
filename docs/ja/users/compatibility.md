> この文書は [英語版 compatibility.md](../../users/compatibility.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# 実行条件とクライアントごとの違い

この手引きは、Skill をどこで使うかを選ぶ人に向けたものである。\
作業に必要な条件と、Skill の検出や実行についてクライアントごとに異なる点をまとめる。\
[インストール方法](installation.md#インストール方法を選ぶ) を選ぶ前に確認する。

Agent Skills の形式に沿った Skill でも、どのクライアントでも動くとは限らない。\
クライアントが Skill を検出、呼び出し、実行できることに加えて、作業に必要なツールと権限をエージェントが使えることも必要になる。

## すべての Skill に共通する条件

- エージェントが、Skill の本文と同梱の資料を読める。\
  どの資料を読むかは、各 Skill に書かれている。
- ツールを使う作業では、必要なリポジトリ、ファイル、ネットワーク、外部サービスにエージェントがアクセスできる。
- ファイルの書き込み、外部サービスへの操作、サブエージェントの実行が許可されている。\
  Skill や Plugin を導入しただけでは、これらは許可されない。

公開している Skill は、実行可能なスクリプトを同梱しておらず、Python ライブラリの追加も必要としない。\
ただし、作業そのものには、ツール、権限、外部の証拠が必要になる場合がある。

## 特定の Skill に必要な条件

Plugin には、すべての公開 Skill が、指示を変えずに入っている。\
使う環境を選ぶときは、特に次の条件を確認する。

| Skill または作業 | 必要な条件 |
| --- | --- |
| `define-referents` | エージェントが、Skill を適用する前に、必須の同梱資料を読む。 |
| `cognitive-rhythm-writing` | エージェントが `japanese-tech-writing/SKILL.md` を読むため、2 つの Skill を一緒に導入する。 |
| `write-natural-japanese` | エージェントが、表現の参照資料を全文読む。 |
| その他の執筆・設計用の Skill | エージェントが、各 Skill が選ぶか必須とする参照資料を読む。 |
| リポジトリの編集、調査、レビュー | エージェントが、実際のファイル、差分、証拠にアクセスでき、確認を実行する場合はそのためのツールも使える。 |
| `research-web-safely` | エージェントが Web を検索して内容を取得でき、確認できる出典を示せる。 |
| `revise-docs-fresh-eyes` | エージェントが Codex または Claude Code で動作し、執筆時の会話を引き継がない独立したサブエージェントを起動することが許可されている。 |

独立したサブエージェントを使えない場合や、使うことが禁止されている場合、`revise-docs-fresh-eyes` は作業を止める。

`cognitive-rhythm-writing` を除き、ほかの Skill を必要とする Skill はない。\
[次に使う Skill を選ぶ](workflows.md) に書いたつながりは、次の Skill を選ぶための案内であり、依存関係ではない。\
出力、不足している入力の扱い、作業を止める条件は、各 Skill を確認する。

## クライアントごとの違い

Skill の検出、呼び出し、制御の方法は、クライアントによって異なる。

- **Codex**:
  - CLI や IDE での `/skills` や `$` による明示的な呼び出しと、自動的な選択は、クライアントの機能である。
  - 任意の `agents/openai.yaml` には、OpenAI 固有の表示と依存関係の情報を書く。
  - サンドボックス、承認、ルール、ツールへのアクセスは、それぞれ別の仕組みで制御される。
- **Claude Code**: 検出、呼び出し、フロントマター、権限、フックの扱いは、クライアント固有である。\
  共通形式に適合していても、それらがどう動くかは分からない。
- **Cursor**: [Cursor での導入手順](installation.md#cursor-で使う) に従い、使っている Cursor のバージョンで、検出と明示的な呼び出しを確かめる。
- **GitHub Copilot、Gemini CLI などのその他のクライアント**: 検出、呼び出し、メタデータ、権限、実行時の動作を、最新の公式資料と使っているバージョンで確かめる。
- **APM**: `skills/` ディレクトリを導入するツールであり、Skill を実行するものではない。

## 使っているクライアントで Skill が動くか確かめる

次の点は、一つを確かめても他のことは分からないので、それぞれ別に確かめる。

- パッケージの形式が正しい。
- クライアントが Skill を導入し、一覧に表示する。
- Skill を呼び出せる。
- クライアント固有の拡張が想定どおりに動く。
- 前提にしている権限を、クライアントが実際に制御している。
- 作業に必要なものに、エージェントがアクセスできる。

クライアントの動作は、パッケージの形式とは関係なく変わる。\
作業に影響する点は、最新の公式資料で確認する。

- [Agent Skills 仕様](https://agentskills.io/specification)
- [OpenAI の Skill 作成ガイド](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code の Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude の Skill 作成ガイド](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude の企業向け Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Cursor の Plugins](https://cursor.com/docs/plugins)
