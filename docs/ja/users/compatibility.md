> この文書は [英語版 compatibility.md](../../users/compatibility.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# 互換性と実行条件

Agent Skills の形式に適合していても、クライアントが Skill を検出・呼び出し・実行できるとは限らない。\
[導入方法](installation.md#導入方法を選ぶ) を選ぶ前に、利用先の機能と作業の実行条件を確認する。

## 共通の実行条件

- エージェントが Skill 本文と同梱資料を読めること。\
  読む資料は各 Skill の指示に従う。
- ツールを使う作業では、必要なリポジトリ、ファイル、ネットワーク、外部サービスにアクセスできること。
- 書き込み、外部への操作、サブエージェントの実行に必要な許可があること。\
  Plugin の導入だけでは許可は得られない。

現在の公開 Skill は、実行スクリプトを同梱せず、Python ライブラリの追加も要求しない。\
ただし、作業に必要なツール・権限・外部の証拠は別途必要となる。

## Plugin の実行条件

`mtk177a-skills` は、すべての公開 Skill を指示を変えずに同梱する。\
利用する環境を選ぶ際は、特に次の条件を確認する。

| 作業・Skill | 必要な条件 |
| --- | --- |
| `define-referents` | 適用前に、必須の同梱資料を読む |
| `cognitive-rhythm-writing` | 隣接する `japanese-tech-writing/SKILL.md` を読むため、両方を導入する |
| 執筆・設計用 Skill | 各 Skill が指定・選択する参照資料を読む。`write-natural-japanese` は表現の参照資料を全文読む |
| リポジトリの編集・調査・レビュー | 実際のファイル、差分、証拠にアクセスする。検証を実行する場合は対応するツールも必要 |
| `research-web-safely` | 実際の検索・取得手段と、確認できる引用元がある |
| `revise-docs-fresh-eyes` | Codex または Claude Code で、執筆時の会話を引き継がない独立したサブエージェントを使う許可がある。利用できない、または禁止されている場合は中止する |

別の作業手順への言及だけでは、その Skill を必須の併用先とはみなさない。\
出力、不足情報への対応、停止条件は各 Skill を確認する。\
指示や資料を変更するときは、該当する実行条件と同梱資料の参照関係を併せて見直す。

## クライアント固有の動作

| クライアント・ツール | 確認する違い |
| --- | --- |
| Codex | CLI・IDE での `/skills`・`$` による明示指定と暗黙の選択は、クライアント側の機能。任意の `agents/openai.yaml` は OpenAI 固有の表示・依存情報を指定する。サンドボックス、承認、ルール、ツールへのアクセスは別の制御となる |
| Claude Code | 検出、呼び出し、フロントマター、権限、フックはクライアント固有であり、共通形式への適合だけでは動作を確認できない |
| Cursor | [ローカル導入手順](installation.md#cursor) に従い、対象バージョンでの検出と明示的な実行を確認する |
| GitHub Copilot・Gemini CLI など | 検出、呼び出し、メタデータ、権限、実行時の動作を、最新の公式資料と対象バージョンで確認する |
| APM | ルートの `skills/` を導入するツールであり、実行クライアントではない |

クライアント固有のメタデータは、呼び出しの制御、画面表示、依存の宣言、権限の動作が必要な場合だけ追加する。\
それ以外では、`name`、`description`、指示、資料を共通形式に保つ。

## 必要な動作を確認する

形式、導入・検出、呼び出し、クライアント固有の拡張、強制される権限制御、実行環境へのアクセスを別々に確認する。

クライアントの動作は、パッケージ形式とは別に変わる。\
作業の判断に影響する場合は、最新の公式資料を確認する。

- [Agent Skills 仕様](https://agentskills.io/specification)
- [OpenAI の Skill 作成ガイド](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code の Skills](https://code.claude.com/docs/en/slash-commands)
- [Claude の Skill 作成ガイド](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude の企業向け Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [Cursor の Plugins](https://cursor.com/docs/plugins)

第三者の資料や実行機能を含む場合は、[セキュリティレビュー](../maintainers/security.md) も行う。
