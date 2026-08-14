---
name: design-changes
description: code または configuration を変更する前に、実装可能な変更方針、対象・対象外の scope、risk、decision point、verification coverage を設計する。request と採用方針が理解済みで、実装前に impact または trade-off を整理するときに使う。未定義 request の明確化、未確定な問題フレームまたは解決案の探索、Agent Skill の設計、変更の実装、高リスクな execution readiness と safety control の単独評価には使わない。
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
- 後続レビューの調整に影響する reviewer context: product または operational criticality、影響する user・data・contract、exposure、採用済み trade-off、detection・recovery control、review focus

重要な claim を `Observed`、`Reported`、`Inferred`、`Unknown`、`Conflicting` に分け、計画した verification と区別する。文脈不足から低い criticality または exposure を推論しない。成功条件と non-goals を定義できるほど request が理解されていない場合は、変更設計の前に `clarify-request` へ回す。

## Workflow

1. 期待する挙動、合意済み scope、non-goals、適用される制約を捉え直す。未解決の requirement を推測せずに設計を始められることを確認する。
2. 既存構造を確認し、変更が影響し得る entry point、主要 branch、ownership boundary、現在の verification path を特定する。
3. 差分を最小化する前に、確認済みの原因と現在の要件を完全に扱う、最小で一貫した boundary を特定する。影響する責務、invariant、contract、既知の実行経路から導出し、明示的な non-target と、影響する interface、module、data、configuration、dependency、consumer を示す。
   確認済みの現在の evidence が変更を必要としない限り、既存の公開 input、signature、受け入れる呼び出し形式を維持する。missing や omitted などの語が、既存の sentinel value と新しい呼び出し形式のどちらも意味し得る場合は、推測で interface を広げず、現在の contract と観測済み caller から区別する。
4. その boundary で局所修正が成立するか、構造的修正が必要かを判断する。確認済みの原因を残す、既存規則を重複させる、確立済みの責務 boundary を迂回する、既知の経路間で挙動を不整合にする、既知の追随修正を必要とする場合は、変更行数が少ないことだけを理由に局所 patch を選ばない。
5. 不確実性、coupling、手戻りコストのため判断に必要な場合だけ、選んだ変更と構造的に異なる代替案を比較する。構造的修正が必要な場合は、局所案が不十分な理由、回復する現在の責務または invariant、影響する contract、変更しないものを説明する。
6. abstraction、dependency、configuration surface、compatibility path、process、service、deployment unit を追加する場合は、それが解決する現在の問題、その問題が存在するか近い将来の要件として合意済みである evidence、検討した単純な代替案、その代替案が不十分な理由、継続的な maintenance または operational cost を記録する。現在必要な作業と任意の将来改善を分ける。
7. 各 material risk を、failure mode に適した prevention、mitigation、detection、recovery、compensation、containment strategy のいずれかと対応付ける。plan がどう扱うかを示さずに risk だけを列挙しない。
8. 変更する各責務、挙動、regression risk、failure boundary を、verification method と期待する evidence へ対応付ける。1つの check が複数 claim を明確に露出する場合は再利用し、固有 risk がある場合だけ追加する。
9. 実装へ進む条件、implementation scope、stop condition を定義する。dependency 追加、破壊的操作、未解決の authority、高リスクな execution readiness の必要性を実装前に明示する。追加の safety control が必要な場合は `assess-risky-change-readiness` への handoff を明記し、この workflow は通常の change design で止める。
10. behavior と ownership に沿った最小で review 可能な単位へ分ける。可読性変更では、孤立した空白や comment の差分ではなく、処理段階と読み手の理解単位で分ける。
11. acceptance、安全性、将来の maintenance に影響する場合、重要な trade-off とユーザーまたは reviewer が理解すべき概念を記録する。
12. 利用可能な evidence から planned reviewer context を作る。目的と期待結果、product または operational context と criticality、scope と non-goals、影響する user・data・contract・exposure、制約と採用済み trade-off、計画した verification と unknown、detection・recovery control、review focus を対象とする。関連する field だけを含め、gap を埋めずに重要な evidence state を保持する。
13. 実装可能な handoff を作る。計画した check と観測済み result を分け、変更を実装しない。

## 判断基準

- 確認済みの原因と現在の要件を完全に扱い、確立済みの boundary を保つ、最小で一貫した変更を優先する。十分な boundary を定めた後にだけ付随的な複雑性を最小化する。
- 実証済みの failure が構造変更を必要としない限り、既存 style と design を維持する。
- 推測上の将来の柔軟性を複雑性の根拠にせず、現在の evidence が必要性を示す構造的修正を差分量だけで退けない。
- downstream consumer が必要とする場合だけ厳密な output template を使い、それ以外は変更に適した構造で必要情報を報告する。
- impact と不確実性から、static check、targeted regression、反復的 empirical evaluation のいずれかを選ぶ。普遍的な test、scenario、alternative、run の件数を設けない。
- material な operational、data、security、external-state、irreversibility、recovery risk が通常の implementation handoff を超える execution-readiness control を必要とする場合は `assess-risky-change-readiness` を使う。

## 報告契約

変更に適した構成を使い、次を含める:

- 推奨方針と、その evidence、前提、未解決の問い
- 変更するものと維持するもの
- その選択が重要な場合、局所修正で十分な理由、または構造的修正が必要な理由
- 現在必要な作業と任意の将来改善
- dependency、影響する boundary、consumer、compatibility impact
- mitigation または control と対応付けた material risk
- verification coverage: 責務または risk → 起こり得る failure → check と期待する evidence
- review severity を宣言せず、実装と後続 review に十分な、重要な unknown と evidence state を含む planned reviewer context
- 実装へ進む条件、implementation scope、stop condition、review 可能な変更単位

代替設計、module map、migration detail、rollback、user explanation point は重要な場合だけ含める。計画した validation は未実行と明示し、観測済み evidence として報告しない。

## 境界

- objective または成功条件が未定義なら `clarify-request`、Agent Skill の責務と trigger 設計には `design-skill`、この handoff の採用後の実装には `implement-changes` を使う。
- 追加の safety、recovery、evidence、authorization-readiness control が必要な destructive、security-sensitive、migration、dependency、その他の consequential change では `assess-risky-change-readiness` と組み合わせる。重要な意思決定で実質的に異なる問題フレームまたは解決案がまだ必要な場合は、この Skill の前に `explore-decision-space` を使い、案が十分に選択済みなら使わない。
- high-risk boundary が該当する場合、implementation handoff で `assess-risky-change-readiness` と未解決の readiness need を明記し、通常の design を実行 authorization として扱わない。
- workflow を read-only に保つ。dependency を追加せず、破壊的変更を行わず、実装を始めない。
- 固定見出し、空の checklist section、alternative の最小件数、test の最小件数を強制しない。
- 別 agent または subagent を既定で使わない。利用できる evidence から設計判断を作り、未解決の高影響な選択はユーザーへ残す。
