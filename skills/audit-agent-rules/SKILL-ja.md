---
name: audit-agent-rules
description: AGENTS.md / skills / docs の運用ルールを監査し、命名、境界、承認ルール、重い既定を含めて小さく安全な改善提案を出したいときに使う。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Audit Agent Rules

## 目的

- `AGENTS.md`、`skills/*/SKILL.md`、`docs` の運用ルールを実運用ベースで見直す。
- 理想論の全面改造ではなく、小さく安全でレビュー可能な改善提案を優先する。

## 使う場面

- `AGENTS.md` / `skills/*/SKILL.md` / `docs` の改善提案を行うとき
- Skill 名、`description`、境界、承認ルール、責務分担のズレを点検したいとき
- Safety、Cost / Context、Consistency、Clarity の観点で小さな改善提案を返したいとき

## 前提 (重要)

- リポジトリの指示文書と Skills は設定契約であり、通常のコード変更より慎重に扱う。
- 承認境界の最終判断は対象リポジトリの適用可能な指示文書またはポリシー文書に従う。`AGENTS.md` が存在する場合はそれを使う。
- ユーザーの明示承認なしに、リポジトリの指示文書 / Skills / docs を直接書き換えない。
- 誤字修正レベルでも、まず提案を出してから編集する。

## 実行手順

1. 対象 (`AGENTS.md` / `skills/*/SKILL.md` / `docs`) を確認する。
2. 次の観点で問題と改善余地を洗い出す (最大5件)。
   - Safety: secrets、破壊的操作、承認境界、sandbox 前提
   - Cost / Context: 常時読み込みの長文化、Skill に分離できる内容、重い model / reasoning / MCP / subagent の既定、失敗ループ停止ルールの有無
   - Consistency: 同じルールの重複、矛盾、散在
   - Clarity: 承認条件、対象範囲、境界の曖昧さ
   - Maintainability: 長文化、責務過多、更新しづらさ
   - Triggerability: Skill 名や `description` が呼び出し条件として弱い、または言葉がずれている
   - Rule layering: 見出し・タイトルの命名と、本文・運用契約の規約を分けて評価し、許容された表現差を drift として扱わない
3. 最小で安全な first change を 1 つ選び、提案する。

## 出力フォーマット (固定)

以下を必ず出す。

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
- 「完璧な一般化」を目指して肥大化させない
- 依存関係追加や運用フロー破壊を無断で提案しない (必ず事前相談)

## 境界

### Always:

- ユーザーの明示承認なしにリポジトリの指示文書 / Skills / docs を直接書き換えない
- 最小で安全な変更から提案する

### Ask first:

- リポジトリの指示文書 / `skills/*/SKILL.md` / `docs` の実編集
- 命名変更や責務再編で利用側への影響が出る場合

### Never:

- 承認なしで編集を実行する

## よくある改善パターン (参考)

- `AGENTS.md` が長い → 詳細は Skill へ移す (`AGENTS.md` は入口と契約のみ)
- 常時読み込みファイルが長い → 契約だけ残し、判断手順やチェックリストは Skill へ分離する
- Skills が増えすぎ → 役割重複を統合し、Skill 名と `description` を整理してトリガー精度を上げる
- 重い model / reasoning / MCP / subagent が既定 → 軽い既定へ寄せ、重い選択は条件付きにする
- 失敗ループ対策がない → 停止条件、仮説更新、次の一手の固定を追加する
- docs が散らかる → `docs/` に索引 (index) を作る
