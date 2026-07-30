---
name: choose-ai-execution-setup
description: 具体的な task の開始前に、必要な access、tool、model capability と reasoning、context、permission、verification、agent topology を導出し、利用可能な AI execution setup のどれを使うべきか助言する。ユーザーが chat、coding agent、model、tool-enabled surface、delegation setup のどれを使うべきか明示的に尋ねた場合に使う。active task の自動 orchestration・実行、implementation unit の設計、client 設定の変更、learning support の calibration には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Choose AI Execution Setup

## 目的

- access、model capability、reasoning effort、context、permission、verification、topology、cost、latency を 1 本の尺度へまとめず、具体的な task に利用可能な AI execution setup を推奨する。
- prerequisite、未確認の利用可能性、次の手順を所有する actor を特定し、推奨を実行可能にする。
- execution-setup advice を、task design、task execution、client configuration、authorization、learning calibration から分離する。

## 証拠

利用可能な情報を集める。

- 具体的な task、意図する outcome、定義済みの work unit
- setup が読むべき証拠と system、access すべき tool または environment、実行すべき action
- 利用可能な chat、coding agent、model、reasoning setting、tool、permission、execution environment
- 不確実性、必要な判断、context 量、verification needs、可逆性、誤りの影響
- ユーザーが提示した cost、latency、token、privacy の制約

確認済みの利用可能性と、必要な capability を区別する。利用可能な選択肢が不明な場合に、特定の product、model、profile、tool、permission、topology を捏造しない。

## 判断 workflow

1. 依頼が、具体的な task に対する execution-setup advice を求めているか確認する。task または関連する選択肢が不明確で比較できない場合は、推測せず不足する証拠を示す。
2. 読むべき証拠、実行すべき action、実行すべき check から、必要な access と tool capability を導出する。
3. 曖昧さ、必要な判断、影響、verification complexity から model capability を選ぶ。task の重要性や tool access を model capability の代用にしない。利用可能な setup が model capability を独立して示していない場合は、未確認または比較上の差がないとする。
4. reasoning effort を model や execution surface とは別に選ぶ。reasoning setting を model capability の証拠にしない。深い推論または検証が判断に影響する場合だけ reasoning を増やす。利用可能な reasoning setting を確認できない場合は、既定値を推奨せず、未確認または比較上の差がないとする。
5. 利用可能でなければならない context と、active context の外に置ける情報を決める。
6. setup が必要とする permission と side effect を特定する。authorization ではなく prerequisite として扱う。
7. outcome を確認するために必要な verification と review capability を選ぶ。
8. work unit が既に定義されている場合だけ、1 session、sequential handoff、independent review、parallel agent のどれを使うか決める。implementation unit の設計が必要な場合は、その作業を所有する design workflow へ返す。
9. unit が独立しており、mutable state または file の競合がなく、ownership と completion check が明確で、parent が統合でき、効果が coordination cost を上回る場合だけ parallel agent を使う。統合担当の parent は、その unit に対する capability と利用可能性を確認できない限り worker 数へ含めず、work unit を割り当てない。
10. ユーザーが提示した cost、latency、token、privacy の制約を、適格な選択肢へ適用する。比較する次元を示さずに setup を軽いまたは重いと呼ばない。
11. requirement を確認済みの利用可能な選択肢へ対応付ける。`Recommendation ready` を使う前に、必要な access、tool、environment、permission、verification capability をその選択肢で確認済みか検証する。それ以外の場合は、条件付き、setup 変更、証拠不足のうち該当する state を使う。
12. 推奨、重要な代替案、prerequisite、未知、次の actor を示す。

## 完了 state

次のいずれか 1 つを割り当てる。

- `Recommendation ready`: 確認済みの利用可能な setup が task requirement を満たし、責任を持つ actor が開始できる。
- `Conditional recommendation`: 推奨する setup を特定できるが、開始前に限定的な利用可能性または task 条件を 1 件確認する必要がある。
- `Setup change required`: 現在確認済みの setup では、必要な capability、permission、environment、verification need を満たせない。
- `Insufficient evidence`: task、利用可能な選択肢、または判断に必要な別の入力が不明確で、捏造せずに比較できない。

## Reporting contract

判断に合わせて応答を調整する。次を含める。

- 完了 state
- 推奨する利用可能な setup、または capability-level recommendation
- access と tool、model capability、reasoning effort、context、permission と side effect、verification と review、topology の独立した項目。判断を制約しない次元は、未確認または比較上の差がないと示す
- ユーザーが提示した重要な cost、latency、token、privacy の制約
- prerequisite、未確認の前提、次の手順を所有する actor
- setup 判断を妨げる場合だけ、task design、configuration、authorization への handoff

`Recommendation ready` の場合は、開始を妨げる prerequisite または判断に必要な未知が残っていないと示す。topology が重要な場合は、latency または specialization 上の効果が coordination・integration cost を上回るか、その比較を妨げる証拠を示す。

`Model capability` と `Reasoning effort` を別々に示す。reasoning effort に関する記述から model capability を推論したり、model 名から reasoning effort を推論したりしない。最終化する前に、各 model-capability claim が task で直接裏付けられているか確認し、それ以外は未確認または比較上の差がないとする。

ユーザーが task 固有の理解または learning support を明示的に求めた場合は、setup recommendation の後に任意の `calibrate-learning-support` handoff を追加し、その方法は設計しない。

特定の model、profile、複数 agent を強制したり、各独立次元が判断を制約するかの記録を超えた詳細比較を強制したりしない。

## 境界

- task の実行または orchestration、implementation work unit の作成、client setting の変更、model の切り替え、permission の付与を行わず、recommendation を authorization として扱わない。
- ユーザーの objective、scope、risk tolerance、実質的な implementation design、final adoption decision を選ばない。
- task 固有の learning・understanding calibration は `calibrate-learning-support` に残し、その Skill が利用できない場合も自己完結させる。
- 自動的な agent・tool orchestration は、この配布 Skill ではなく、active agent の durable instructions、client configuration、agent definitions に残す。
