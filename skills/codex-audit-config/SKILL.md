---
name: codex-audit-config
description: Codex config リポジトリの AGENTS.md / skills / docs を監査し、改善提案したいときに使う。
---

# Codex Config Audit (AGENTS/Skills改善モード)

## 目的

このリポジトリの **AGENTS.md / Skills / docs** を、実運用ベースで継続改善する。
「理想論の大改造」より、**小さく安全でレビュー可能な改善**を優先する。

## 使う場面

- AGENTS.md / skills/*/SKILL.md / docs の改善提案を行うとき

## 前提 (重要)

- AGENTS.md と Skills は **設定契約 (configuration contract)** であり、通常のコード変更より慎重に扱う。
- **ユーザーの明示承認なしに、AGENTS.md / Skills を直接書き換えない。**
  - 例外：誤字修正などの超軽微な変更でも、まず提案を出す。

## 実行手順

1. 対象 (AGENTS.md / skills/*/SKILL.md / docs) を確認する。
2. 次の観点で問題と改善余地を洗い出す (最大5件)。
   - Safety: secrets, destructive actions, approvals, sandbox assumptions
   - Cost / Context: 常時読み込みの長文化、skill へ分離できる内容、重い model / reasoning / MCP / subagent の既定、失敗ループ停止ルールの有無
   - Consistency: 同じルールの重複・矛盾・散在
   - Clarity: 曖昧さ (例：いつ承認が必要か不明、境界が曖昧)
   - Maintainability: 長文化、責務過多、更新しづらさ
   - Triggerability (Skills): description が呼び出し条件として弱い/短すぎる/言葉がズレている
3. 「最小で安全な first change」を1つ選び、提案する。

## 出力フォーマット (固定)

以下を必ず出す：

### 1. Summary

- 何をどう改善するか (1〜2文)

### 2. Motivation

- なぜ必要か (事故防止、手戻り削減、読みやすさなど)

### 3. Proposed changes

- 変更するファイル一覧
- 差分 (diff) または変更後全文 (短い場合)

### 4. Risk / Compatibility

- 既存運用への影響、誤作動リスク

### 5. Next step

- 「この変更で進めてよいですか？」と承認を求める

## 優先順位

1. Safety (最優先)
2. Cost / Context
3. Consistency
4. Clarity
5. Maintainability
6. Expressiveness (nice-to-have)

## 禁止事項

- 大規模なリファクタや全面書き換えをいきなりしない
- ガードレールを弱める方向の変更を提案しない
- “完璧な一般化” を目指して肥大化させない
- 依存関係追加や運用フロー破壊を無断で提案しない (必ず事前相談)

## 境界

### Always:

- ユーザーの明示承認なしに AGENTS.md / Skills を直接書き換えない
- 最小で安全な変更から提案する

### Ask first:

- AGENTS.md / skills/*/SKILL.md / docs の実編集

### Never:

- 承認なしで編集を実行する

## よくある改善パターン (参考)

- AGENTS.md が長い → 詳細はSkillへ移す (AGENTSは入口と契約のみ)
- 常時読み込みファイルが長い → 契約だけ残し、判断手順やチェックリストは Skill へ分離する
- Skills が増えすぎ → 役割重複を統合、description を整理してトリガー精度を上げる
- 重い model / reasoning / MCP / subagent が既定 → 軽い既定へ寄せ、重い選択は条件付きにする
- 失敗ループ対策がない → 停止条件、仮説更新、次の一手の固定を追加する
- docs が散らかる → `docs/` に索引 (index) を作る
