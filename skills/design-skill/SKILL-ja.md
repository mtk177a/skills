---
name: design-skill
description: Agent Skillを新規作成・統合・分割・大幅な責務変更のどれで設計すべきか、実装前に判断する。Skillの責務、trigger境界、再利用資源、評価戦略を定義するときに使う。通常の文言修正、既存挙動の監査、実装自体には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Design Skill

## 目的

- 草案を書く前に、再利用可能なSkillが適切な介入かを判断する。
- 実装工程が責務、trigger、資源、評価の判断をやり直さずに適用できる、証拠に基づく設計を作る。
- 診断、設計、実装を分離する。既存の監査結果は証拠として利用できるが、このSkill単独でも機能させる。

## 証拠

設計判断の前に `references/authoring-guide.md` を完全に読む。

利用できる範囲で以下を集める。

- 期待する結果、利用者、client、model、失敗の兆候
- 再利用可能なgapを示す実タスク例、修正履歴、trace、出力
- Skillなし、または旧版のbaseline
- 適用可能なローカル指示と配布上の制約
- 隣接Skill、そのdescription、共存時の挙動

適用可能なローカル指示は、そのscope内で権威ある情報として扱う。同梱guideは、ローカル指示が規定していない部分のポータブルなbaselineとして使う。観測事実、推論、前提、不明点を分ける。文章上もっともらしいことしか確認できない場合は、改善が実証済みであるかのように扱わず、静的な仮説と明記する。

## Workflow

1. 新しいSkillが必要だと仮定せず、期待する能力と、繰り返し発生する失敗または知識gapを定義する。
2. 代表的な実タスクとbaseline挙動を確認する。agentに不足するもの、既に処理できるもの、再利用すべき修正を分ける。
3. 永続的なguidanceなし、ローカル指示やtool、既存Skillの更新・統合、分割、新規Skillを比較する。
4. 隣接Skillと配布surfaceを確認する。artifactを選ぶ前に、責務重複、trigger競合、context cost、共存riskを解消する。
5. 一貫した責務単位を1つ選ぶ。対象利用者、scope内のtask、除外、入力、出力、failure handlingを定義する。
6. `name` と `description` の案を作る。暗黙triggerに必要なcontextを`description`へ入れ、衝突を防ぐ場合はnegative boundaryも含める。
7. agentが知らない再利用可能な内容だけを、`SKILL.md`、`references/`、`scripts/`、`assets/`、eval資産へ割り当てる。すべてを同じ詳細度に固定せず、taskの壊れやすさに指示の自由度を合わせる。
8. workflowに必要な場合だけ、安全性やpermissionの境界を定義する。特定の見出しtemplateを強制せず、必要な安全特性を保持する。
9. 大量の本文を書く前に評価を設計する。対象client・modelに関係するtrigger、non-trigger、near-miss、baseline、isolation、coexistence、instruction-following、output-qualityを扱う。
10. 実際に影響するtarget surfaceだけを特定し、実装handoffを作る。このworkflowではSkillを編集・実装しない。

## 判断基準

- modelが既に安定してtaskを実行でき、再利用可能な専門contextや手順が不足していない場合は、Skillを作らない。
- trigger、出力契約、risk境界を一貫したまま保てる場合は、既存Skillの更新・統合を優先する。
- 責務をまとめるとtrigger、loading、実行が曖昧になる場合は、新規Skillまたは分割を優先する。
- referenceやscriptは、繰り返す再調査を減らす、domain evidenceを提供する、壊れやすい操作を検証可能にする場合だけ同梱する。
- main instructionは簡潔に保ち、読み込まれる各sectionがcontext costに見合うようにする。

## 報告契約

固定の提案templateではなく、判断に合う構成を使う。以下の情報を含める。

- 推奨する介入と、代替案より適切な理由
- 証拠、前提、未解決の問い
- 責務とtrigger境界の案
- Skillを推奨する場合のmetadata案
- 本文とresourceの配置
- 実装後も保持すべき安全性・permission特性
- 評価・rollout戦略
- 影響するtarget surfaceと、実装可能なhandoff

証拠が永続的guidance不要、または別の介入を支持する場合は、Skill案を強制しない。ファイル編集、依存追加、repository policy変更は行わず、権限を持つ実装workflowへ引き渡す。
