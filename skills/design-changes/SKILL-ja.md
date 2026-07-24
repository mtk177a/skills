---
name: design-changes
description: code または configuration を変更する前に、実装可能な変更方針、対象・対象外の scope、risk、decision point、verification coverage を設計する。request が理解済みで、実装前に impact または trade-off を整理するときに使う。未定義 request の明確化、Agent Skill の設計、変更の実装、高リスクな approval / rollback planning の単独処理には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Design Changes

## 目的

- 実装 workflow が scope、risk、verification の判断をやり直さずに使える、最小で decision-complete な方針を作る。
- 変更するものと維持するものを分け、impact boundary を review 可能にする。
- 実装 handoff で止まり、対象ファイルを編集しない。

## 証拠と入力

利用できる範囲で次を集める:

- 期待する挙動、合意済み scope、制約、non-goals
- 関連する entry point、module、interface、data flow、configuration、tests
- 既存仕様、repository guidance、確立済みの implementation pattern
- 観測済み failure、trace、過去の試行、design decision
- dependency、migration、compatibility、security、rollout の制約

確認済み evidence、推論、前提、不明点、計画した verification を区別する。成功条件と non-goals を定義できるほど request が理解されていない場合は、変更設計の前に request scoping へ回す。

## Workflow

1. 期待する挙動、合意済み scope、non-goals、適用される制約を捉え直す。未解決の requirement を推測せずに設計を始められることを確認する。
2. 既存構造を確認し、変更が影響し得る entry point、主要 branch、ownership boundary、現在の verification path を特定する。
3. 最小で一貫した変更と、明示的な non-target を定義する。影響する interface、module、data、configuration、dependency、consumer を特定する。
4. 不確実性、coupling、手戻りコストのため判断に必要な場合だけ、最小変更と構造的に異なる代替案を比較する。
5. 各 material risk を、prevention、mitigation、rollback、detection strategy のいずれかと対応付ける。plan がどう扱うかを示さずに risk だけを列挙しない。
6. 変更する各責務、挙動、regression risk、failure boundary を、verification method と期待する evidence へ対応付ける。1つの check が複数 claim を明確に露出する場合は再利用し、固有 risk がある場合だけ追加する。
7. 実装へ進む条件、implementation scope、stop condition を定義する。dependency 追加、破壊的操作、未解決の authority、高リスクな approval / rollback の必要性を実装前に明示する。高リスク control が必要な場合は `plan-risky-change` への handoff を明記し、この workflow は通常の change design で止める。
8. behavior と ownership に沿った最小で review 可能な単位へ分ける。可読性変更では、孤立した空白や comment の差分ではなく、処理段階と読み手の理解単位で分ける。
9. acceptance、安全性、将来の maintenance に影響する場合、重要な trade-off とユーザーまたは reviewer が理解すべき概念を記録する。
10. 実装可能な handoff を作る。計画した check と観測済み result を分け、変更を実装しない。

## 判断基準

- 確立済みの boundary を保ち、期待する挙動を満たす最小変更を優先する。
- 実証済みの failure が構造変更を必要としない限り、既存 style と design を維持する。
- downstream consumer が必要とする場合だけ厳密な output template を使い、それ以外は変更に適した構造で必要情報を報告する。
- impact と不確実性から、static check、targeted regression、反復的 empirical evaluation のいずれかを選ぶ。普遍的な test、scenario、alternative、run の件数を設けない。
- 通常の implementation handoff を超える明示 approval、rollback、recovery control が必要な場合は `plan-risky-change` を使う。

## 報告契約

変更に適した構成を使い、次を含める:

- 推奨方針と、その evidence、前提、未解決の問い
- 変更するものと維持するもの
- dependency、影響する boundary、consumer、compatibility impact
- mitigation または control と対応付けた material risk
- verification coverage: 責務または risk → 起こり得る failure → check と期待する evidence
- 実装へ進む条件、implementation scope、stop condition、review 可能な変更単位

代替設計、module map、migration detail、rollback、user explanation point は重要な場合だけ含める。計画した validation は未実行と明示し、観測済み evidence として報告しない。

## 境界

- objective または成功条件が未定義なら `scope-request`、Agent Skill の責務と trigger 設計には `design-skill`、この handoff の採用後の実装には `implement-changes` を使う。
- 明示 control が必要な destructive、security-sensitive、migration、dependency、その他の高リスク作業では `plan-risky-change` と組み合わせる。設計が同じ近傍で停滞した場合だけ `diversify-agent-search` を使う。
- high-risk boundary が該当する場合、追加 approval または rollback work を説明するだけでなく、implementation handoff で `plan-risky-change` を明記する。
- workflow を read-only に保つ。dependency を追加せず、破壊的変更を行わず、実装を始めない。
- 固定見出し、空の checklist section、alternative の最小件数、test の最小件数を強制しない。
- 別 agent または subagent を既定で使わない。利用できる evidence から設計判断を作り、未解決の高影響な選択はユーザーへ残す。
