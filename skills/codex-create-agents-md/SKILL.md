---
name: codex-create-agents-md
description: Codex 向けに AGENTS.md を新規作成したいときや、関連する指示文書セットを含めて大きく作り直したいときに使う。
---

# AGENTS.md Authoring

## 目的

- AGENTS.md を安全に作成するための手順とテンプレートを提供する
- 関連する指示文書セットがある場合に、役割分担と整合を崩さず設計する

## 使う場面

- 新規に AGENTS.md を作成したい
- リポジトリ固有の AGENTS.md を作成したい
- `CLAUDE.md` や `.github/copilot-instructions.md` を含めて指示文書全体を整理したい

## 入力 (任意)

- 目的/範囲/制約 (例: 全体/リポジトリ/サブディレクトリ)
- 追加したいルールの要点
- 既存の関連文書 (`CLAUDE.md`, `.github/copilot-instructions.md`, README, docs) の有無

## 手順

1. 目的・適用範囲 (全体/リポジトリ/サブディレクトリ) を確認する
2. 読み込み順を明記する
   - `~/.codex/AGENTS.md` → リポジトリルートの `AGENTS.md` → サブディレクトリごとの `AGENTS.md`
3. 関連する指示文書 (`CLAUDE.md`, `.github/copilot-instructions.md` など) の有無を確認する
4. 一次情報として依拠する文書を固定する
   - 例: `README.md`, `skills/README.md`, `docs/skill-authoring.md`
5. 文書ごとの役割分担を整理する
   - `AGENTS.md`: 正式な契約
   - `CLAUDE.md`: 補助文書
   - `.github/copilot-instructions.md`: Copilot 向け短縮版
6. 共通事実と、各文書に書く内容 / 書かない内容を切り分ける
7. 最小構成のテンプレートまたは文書セット案を提示する
8. リポジトリ固有ルールの追加候補を整理する
9. 影響 (運用・レビュー・共有) を記載する
10. 承認を得てから作成/編集を行う

## 出力フォーマット

- 変更点の要約: ...
- 目的・範囲: ...
- 読み込み順: ...
- 一次情報: ...
- 文書ごとの役割分担: ...
- テンプレート案:

  ```markdown
  # AGENTS.md

  ## 目的
  - ...

  ## 基本方針
  - ...

  ## 禁止事項
  - ...

  ## 進め方
  - ...
  ```

- 関連文書がある場合の分担メモ:
  - `CLAUDE.md`: ...
  - `.github/copilot-instructions.md`: ...
- 影響/リスク: ...
- 承認: この方針で進めてよいですか？

## 境界

### Always:

- 読み込み順を明記する
- 関連指示文書がある場合は、単体最適化せず文書セットとして整合を見る
- 一次情報を先に固定してから文案を作る
- 最小差分・レビュー可能な単位で提案する

### Ask first:

- 既存の AGENTS.md を編集する場合
- `CLAUDE.md` や `.github/copilot-instructions.md` も同時に新規作成・改稿する場合
- 文書間の責務分担を変更する場合
- テンプレートに組織ポリシー/セキュリティ項目を追加する場合

### Never:

- AGENTS.md や Skill を無断で編集・作成する
- 秘密情報や社外秘情報をテンプレートに含める

## 注意点 (任意)

- AGENTS.md の仕様が変更される可能性があるため、曖昧な場合は確認する
- 同じ事実を複数文書に重複記載しすぎず、役割ごとに内容を分担する
- 文書本文の日本語/英語ルールは、`docs/skill-authoring.md` や既存文書と矛盾させない
