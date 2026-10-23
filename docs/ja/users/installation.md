> この文書は [英語版 installation.md](../../users/installation.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# 導入と更新

`mtk177a-skills` は、公開している `skills/` を 1 つの Agent Plugin として配布する。\
Plugin と単体・APM 導入で同じ原本を使い、配布用のコピーは別管理しない。

- **利用する**: [導入方法を選ぶ](#導入方法を選ぶ) → [実行条件を確認する](compatibility.md#plugin-の実行条件)。
- **ZIP を作る**: [Plugin の ZIP を作る](../maintainers/packaging.md)。

## 導入方法を選ぶ

同じ実行環境で Skill が重複しないよう、導入方法を一つに揃える。

| 利用先 | 導入方法 |
| --- | --- |
| ChatGPT と Codex | ZIP を ChatGPT の個人用 Plugin としてアップロードし、利用する画面や環境ごとに使えるか確認する |
| Cursor | 同じ ZIP を Cursor のローカル Plugin ディレクトリに展開する |
| Claude Code | [APM による導入](#apm-で導入する) を使う。このパッケージでは Claude 固有の Plugin マニフェストを追加しない |

**有効化する前に、重複する導入を整理する。**

- **対象**: 別の Plugin や単体・APM 導入との重複を特定し、クライアントが提供する操作で無効化または削除する。
- **保護するもの**: 無関係な Skill や認証情報は削除しない。\
  文書化されていない優先順位や名前空間に依存しない。
- **復旧と確認**: 前のアーカイブを保管し、新しい会話で Plugin を確認する。

導入で利用可能になるのは同梱された指示であり、シェル・リポジトリ・外部接続・サブエージェント・書き込み権限は別途必要となる。\
導入できても、作業に必要な機能や権限が不足する場合がある。

## Plugin を導入・更新する

### ChatGPT と Codex

アーカイブはユーザーが手動でアップロードする。\
生成スクリプトは、アップロードやアカウント設定の変更を行わない。

1. **ZIP をアップロードする。**
   - 初回: ChatGPT の個人用 Plugin のアーカイブアップロードを使う。
   - 更新: 別の Plugin を作らず、既存 Plugin のメニューで「新しいバージョンをアップロード」を選ぶ。

2. **バージョンと Skill 一覧を確認する。**\
   確認後、新しい会話を開始する。

3. **Plugin と Skill を指定する。**\
   利用可能な UI で Plugin を選び、依頼文で使う Skill を指定する。\
   たとえば、「`mtk177a-skills` の `define-referents` を使い、参照資料を読んでから命名案を出してください」と依頼する。

4. **利用先ごとに結果を確認する。**
   - 検出: Skill が一覧に現れるか。
   - 読み込み: 本文・参照資料を読めたか。\
     実際に観測できる場合に確認する。
   - 出力: どのような回答が得られたか。\
     回答の妥当性だけで読み込み済みと判断しない。

Chat、Work、dots、Codex では、呼び出し方や使える機能が異なる場合がある。

### Cursor

[Cursor の公式資料](https://cursor.com/docs/plugins) では、共通形式の Agent Plugin への対応と、`~/.cursor/plugins/local/<plugin-name>/` でのローカル検証が案内されている。

1. **ZIP を展開する。**\
   `~/.cursor/plugins/local/mtk177a-skills/` の直下に `plugin.json` を置く。\
   更新時は必要なバックアップを確保し、展開先の古いディレクトリを丸ごと入れ替える。\
   ファイルを上書きするだけでは、新版で削除された Skill が残る可能性がある。
2. **再読み込みする。**\
   Cursor を再起動するか、**Developer: Reload Window** を実行する。
3. **動作を確認する。**\
   Skill が認識され、明示的に指定して使えることを確認する。

この Skill のみを含むパッケージでは、`.cursor-plugin/plugin.json` は不要である。\
マーケットプレイスへの申請は、この手順の対象外とする。

## APM で導入する

Claude Code など、APM が対象とするクライアントで使用する。

| 対象 | コマンド |
| --- | --- |
| 全 Skill | `apm install mtk177a/skills` |
| 選んだ Skill | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| 個別パス | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` は隣接する `japanese-tech-writing` を読むため、上表の選択導入で両方を導入する。

利用側の `apm.yml` で全体を依存として宣言することもできる。

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

導入後は、利用先での配置場所と Skill の検出・明示的な実行を確認する。\
APM の導入成功だけでは、そのクライアントでの動作を確認したことにはならない。
