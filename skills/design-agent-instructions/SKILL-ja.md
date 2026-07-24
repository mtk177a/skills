---
name: design-agent-instructions
description: リポジトリが実際に使う agent client 向けに、新規または再編する durable instruction 文書セットを設計する。編集前に source of truth の役割、loading と precedence の関係、共通 guidance と client 固有 guidance、必要な companion file を決めるときに使う。未解明な挙動の診断、通常の Skill 設計、承認済み文書変更の実行には使わず、実行は implementation workflow へ回す。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Design Agent Instructions

## 目的

- 明確な authority と最小限の重複で、期待する client に届く最小の instruction 文書セットを設計する。
- 1つの filename や hierarchy が普遍的だと仮定せず、確認済みの client semantics と repository の必要性から文書の役割を決める。
- instruction set を編集せず、実装可能な handoff を作る。

## 証拠

利用できる範囲で以下を集める。

- 期待する挙動、scope、実際の利用者、client、model
- 既存の instruction 文書、client 設定、import、rules、hooks、policy surface、一般 project documentation
- loading、discovery、precedence、enforcement、対応 filename が重要な場合の最新公式 client documentation
- 観測済みの loading evidence、trace、修正履歴、失敗
- 適用可能な local policy と authorization boundary

観測事実、推論、前提、不明点を分ける。依頼が未解明な挙動から始まり、loading または authority が不確かな場合は、文書再設計を修正と扱う前に `audit-agent-guidance` で診断する。

## Workflow

1. 期待する挙動、scope、実際に使う client、共通化すべき内容と client 固有にすべき内容を定義する。説明できない non-adherence が主題で、loading または authority が未確定なら、document design を止め、不足 evidence とともに `audit-agent-guidance` へ明示的に引き渡す。
2. 既存の instruction set と project-local の一次情報を確認する。標準的な filename がないことだけを欠陥と扱わない。
3. 各 target client について、関連する loading、discovery、precedence、import、enforcement semantics を確認して記録する。ある client の hierarchy を別 client に投影しない。
4. 共通の事実または rule ごとに canonical source を特定する。import、reference、generated view は、target client が対応し、authority を隠さず drift を減らす場合だけ使う。
5. durable behavioral guidance と、強制される permission または lifecycle automation を分離する。保証が必要で client に該当 mechanism がある場合は、client policy、settings、hooks を使う。
6. 必要な文書と設定 surface を決める。client 固有 companion は、その client が実際に使われ、canonical guidance を直接利用できない場合だけ含める。
7. 各 surface に置く内容と明示的に置かない内容を定義する。一般 project facts は、agent context に必要でなければ通常の documentation に置く。
8. 必要に応じて、重複、矛盾、context cost、portability、ownership、更新経路、compaction または lazy loading 後の挙動を確認する。
9. 提案 set を、現状維持、冗長 guidance の削除、より小さい bridge document と比較する。
10. 重要な risk から validation を定義する。loading observability、precedence conflict、instruction adherence、enforcement boundary、active client 間の coexistence を扱う。
11. scope のある implementation handoff を作る。この design workflow では file を作成・編集しない。

## 報告契約

判断に合う構成を使い、以下を含める。

- 推奨する文書セットと、代替案より適切な理由
- 期待する挙動、scope、active client、未解決の前提
- client ごとに確認した loading、discovery、precedence、import、enforcement semantics
- canonical source と surface ごとの責務
- 意図的に省く文書または surface
- 重複、context、portability、maintenance、migration の risk
- validation coverage と実装可能な change unit
- 未解決の挙動により妥当な document design ができない場合の、`audit-agent-guidance` への明示的な diagnostic handoff

companion document、固定 filename、固定 heading template を強制しない。挙動が未確認の場合は、design を実証済みの修正として示さず、必要な diagnostic evidence を特定する。

## 境界

- 主目的が既存 guidance の不整合な挙動の原因診断なら `audit-agent-guidance` を使う。再利用可能な Skill の責務と trigger 設計には `design-skill` を使う。
- 現行 client semantics が別の性質を示さない限り、instruction document は hard enforcement ではなく behavioral context として扱う。
- `AGENTS.md`、`CLAUDE.md`、`.github/copilot-instructions.md`、`GEMINI.md` が client に読み込まれると、確認なしに仮定しない。
- 文書セットを完全に見せるためだけに、共通事実を複数 file へ複製しない。
- workflow は read-only に保つ。編集には user authorization と対象環境の applicable policy が必要であり、普遍的な追加 approval gate を作らない。
- template と例に secret、credential、personal information、非公開の operational data を含めない。
