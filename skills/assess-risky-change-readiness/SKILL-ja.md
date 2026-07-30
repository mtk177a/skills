---
name: assess-risky-change-readiness
description: 重大または復旧困難な変更が実行へ移る前に、安全 control、recovery strategy、evidence、authorization state を評価して準備する。material な operational、data、security、external-state、irreversibility、recovery risk が通常の implementation handoff を超える control を必要とする場合、または別 workflow が不足する high-risk control を特定した場合に使う。通常の change design、control が揃った承認済み implementation、完了済み diff の review、failure investigation、一般的な security review、変更の実行には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Assess Risky Change Readiness

## 目的

- 重大または復旧困難な変更について、実行へ移れるだけの evidence、安全 control、recovery preparation、authority があるかを判断する。
- 具体的な action、target、environment、execution boundary、material risk、責任ある handoff を decision-ready にする。
- read-only な readiness または authorization handoff で止まり、変更を承認または実行しない。

## Evidence と入力

利用できる範囲で次を集める:

- objective、選択済み approach、具体的な action、target、environment、revision、data scope、execution boundary
- 影響を受ける user、system、data、external state、credential、依存 operation
- precondition、backup または restore evidence、monitoring、validation、operational ownership
- 提案済みの prevention、mitigation、detection、abort、recovery、compensation、containment control
- 適用 policy、既存 authorization、必要な decision owner、risk tolerance、accepted loss
- assumption、未解決 decision、unknown、現在の authority 内では取得できない evidence

各 material input を `Confirmed`、`Reported`、`Inferred`、`Assumed`、`Unknown` のいずれかに分類する。
報告された control、提案コマンド、予定された backup を confirmed evidence に変換しない。

## Risk assessment

category label だけで判断せず、追加 control が必要になる次の性質を評価する:

- reversibility と reversal が不可能になる point
- recovery time、cost、completeness、evidence を含む recoverability
- user、system、region、tenant、record、external party にわたる blast radius
- production、shared、persistent、externally controlled state の mutation
- data loss、corruption、confidentiality、integrity、security、privacy、compliance impact
- detectability、monitoring delay、abort signal の信頼性
- action authority、separation of duties、responsible owner、escalation path
- target、plan、dependency、control、expected outcome の uncertainty

これらの性質が追加の execution control を必要としない場合は、通常の change design を使う。

## Workflow

1. 具体的な action、target、environment、revision または data scope、execution boundary、intended outcome、non-goals を確定する。
2. risk property が通常の implementation handoff を超える control を必要とするか判断する。
3. confirmed evidence を、reported claim、inference、assumption、unknown から分離する。
4. 各 material risk を、それを防止または軽減する control、検知する evidence、中止する signal と threshold、責任を持つ人または workflow へ対応付ける。
5. 各 material failure mode に対して、rollback、roll-forward、restore、compensation、containment、partial または manual recovery、irreversible loss の明示的受容から現実的な recovery treatment を選ぶ。
6. precondition、go/no-go criteria、monitoring、abort authority、point of no return、recovery ownership、post-action verification が decision-ready か確認する。
7. authority を付与したり重複承認を求めたりせず、具体的な scope と control の authorization state を判断する。
8. completion state を一つだけ割り当て、handoff を作る。

target または execution boundary を特定できない場合は、plan を捏造せず `Blocked` とする。
実行済みであることを supplied evidence が示さない限り、command は提案済みの未実行 action として扱う。

## Completion states

次の順序で状態を一つだけ選ぶ:

1. `Not applicable`: 通常の design または implementation handoff を超える safety control が不要である。
2. `Blocked`: Skill は適用されるが、material な target、evidence、control、recovery、ownership、risk acceptance、authority の不足により、責任ある authorization または execution handoff ができない。
3. `Ready for authorization`: material な control と evidence は decision-ready だが、責任ある authority が具体的な action、scope、residual risk を承認していない。
4. `Ready for execution handoff`: material な control は decision-ready で、具体的な action と scope が特定された execution owner に対して承認済みである。

material な readiness gap が残る場合、authorization status より `Blocked` を優先する。
この Skill は authorization を記録するが、作り出さない。

## Control と recovery の規則

- reversal が不可能、または別 treatment より危険な場合に rollback を必須にしない。
- prerequisite、procedure、owner、expected limit が credible である evidence なしに、recovery が利用可能だと記述しない。
- failure mode に rollback より適する場合は、roll-forward、restore、compensation、containment、explicit loss acceptance を使う。
- material な irreversible loss に承認済み acceptance decision がない場合、または必要な recovery evidence が得られない場合は `Blocked` とする。
- 具体的な scope と control が承認済みの場合は、一般的な再確認を求めない。
- action、target、scope、control set、residual risk、適用 authority が承認内容から実質的に変わる場合だけ、新しい decision を必要とする。

## 報告契約

変更に合わせた構成で、次を含める:

- completion state とその理由
- 具体的な action、target、environment、revision または data scope、execution boundary
- material input と unknown の evidence state
- applicability basis と material risk property
- prevention または mitigation、detection、abort condition、recovery treatment、owner、residual risk を含む risk-to-control mapping
- precondition、go/no-go criteria、monitoring、point of no return、post-action verification
- authorization state、responsible decision owner、accepted loss
- 次の handoff と、それを無効にする条件

空の section と固定の step 数を強制しない。
command が有用な場合は、確認した evidence に基づいて具体化し、未実行と明記する。

## 境界

- objective、target、environment、authority、success criteria が評価できないほど未定義な場合は `clarify-request` を使う。
- 実質的に異なる safety または rollout strategy が未確定な場合は `explore-decision-space` を使い、approach を選択してからここへ戻る。
- 通常の implementation design には `design-changes` を使い、追加の high-risk control が必要な場合はその handoff を受け取る。
- 承認済み implementation は `implement-changes` または元の authorized operator へ渡し、その実行責務を吸収しない。
- 完了済み diff の review、failure investigation、一般的な security assessment、file modification、提案 operation の実行、変更の承認、変更の実行を行わない。
- 隣接 Skill がなくても self-contained に動作し、別 agent または subagent を既定で導入しない。
