---
name: calibrate-ai-learning
description: 作業を進めながら、ユーザーが task 固有の理解、decision ownership、verification を保持または回復できるよう、AI の支援方法を調整する。ユーザーが学習を明示的に優先する場合、AI 生成物を説明・評価できないと述べた場合、理解を保ちながら委任したい場合、または理解確認後も calibration を継続する場合に使う。通常の tool・model 選択、実作業と無関係な一般教育、未知領域という理由だけで明確な依頼を止める用途には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Calibrate AI Learning

## 目的

- active task に対する AI の支援方法を調整し、ユーザーが自ら所有する判断を行い、説明責任を持つ部分を説明・検証できるようにする。
- calibration を元の workflow を包む反復的な layer として扱い、1 回限りの学習計画や、実装、調査、設計、レビューの代替にしない。
- 誤解が判断、検証、成果へ影響する部分だけに学習コストを使い、依頼された作業の進行を維持する。

## 証拠と calibration state

利用可能な情報を集める。

- active task、元の workflow、次の判断または行動
- ユーザーが明示した学習目的、時間制約、希望する支援、説明責任
- ユーザーが明示的に説明・選択・質問したこと、または不明としたこと
- 理解・評価する必要がある変更、提案、証拠、AI 生成物
- 適用される権限、リスク、検証上の制約

次を分けて扱う。

- 確認済みの task facts と authoritative decisions
- ユーザーが明示した理解と未知
- 理解状態に関する合理的な推論と、その根拠
- 証拠による確認が必要な AI 生成の主張
- ユーザー所有の判断と委任可能な作業

沈黙から理解や混乱を推測しない。理解確認への回答は、その回答が扱った点の証拠として扱い、一般的な習熟の証明にはしない。

## Calibration cycle

1. active task からユーザーが今必要としているものと、自ら理解・説明・検証・判断する必要があるものを特定する。
2. 誤解が次の行動、受容するリスク、検証、後の説明責任へ重要な影響を与えるか判断する。現在の作業を変えない一般論へ広げない。
3. decision ownership を分ける。
   - ユーザーは目的、優先順位、accepted scope、risk tolerance、authorization、説明責任を持つ場合の final adoption を所有する
   - AI は証拠収集、選択肢作成、変更案作成、承認済み check の実行、reasoning の説明を行える
   - AI は影響の大きい技術判断を分析できるが、証拠、trade-off、未知、採否判断を責任を持つユーザーへ返す
4. ユーザーの目的と制約に合う支援方法を選ぶ。文脈に応じて、実行前に説明する、判断を共同で行う、承認済み作業の後に証拠を説明する、既存の AI 生成物を再構成する、またはユーザーが重要な手順を行って AI がレビューする。
5. 選択した calibration の下で、元の workflow を継続または引き継ぐ。次の承認済み行動へ進める場合に、学習計画を出力するためだけに停止しない。
6. 回答が次の行動を変えるか、重要な gap を明らかにできる場合だけ understanding checkpoint を使う。一般的な記憶を試すのではなく、限定された説明、選択、予測、または検証手順を求める。
7. ユーザーの回答と新しい証拠を取り込む。解決済みの点を保持し、残る重要な gap だけを再評価し、必要なら支援方法を調整する。
8. calibration のやり取りによって判断、検証、説明責任が改善する間だけ反復する。それ以外は元の workflow へ戻るか、依頼された作業を完了する。

## 判断基準

学習と進行を二者択一にせず、連続的な軸で調整する。次を考慮する。

- ユーザーが今回の task で求める理解の深さ
- 誤判断の影響と可逆性
- ユーザーが結果を review、operate、maintain、approve、explain する必要性
- 利用可能な時間と、実行前・実行中・実行後のどこで説明できるか
- 利用可能な証拠の強さ

依頼が明確、承認済み、可逆的である場合は、短い説明とともに実行を継続することを優先する。ユーザーが学習を明示的に優先する場合、重要な出力を評価できない場合、または影響の大きい判断を所有する場合は、共同作業または checkpoint を増やす。

主張に適した証拠を使う。例として、公式 documentation・standard、repository の source・history、既存 implementation、direct observation、reproduction、log、test、measurement、または権限を持つ domain owner の決定がある。AI の結論は証拠そのものではなく、証拠からの推論として扱う。

## State と handoff contract

次の行動を表す state を使う。

- `Ready`: 元の workflow が進められ、重要な decision ownership と verification が明確
- `Proceed with checkpoints`: 特定した判断または理解の checkpoint を挟みながら作業を継続できる
- `Continue calibration`: 影響を受ける行動の前に、重要な理解不足について限定的な説明、質問、または共同作業が必要
- `Blocked`: 必要なユーザー所有の判断、authorization、または risk acceptance を取得できない

応答を task に合わせる。次の行動を変える情報だけを含める。

- 保護する理解または判断
- 選択した支援方法と理由
- AI が進められる作業と、ユーザーが所有する判断
- 次の checkpoint または元の workflow の行動
- supporting evidence、未確認の主張、残る未知

固定 template、概念数、確認問題、自習課題を要求しない。練習や後日の自習は、ユーザーが求めた場合、または明示された学習目的に重要な効果がある場合だけ提案する。

## 境界

- 未知領域という理由だけで、直接回答や承認済み実装を出し惜しみしない。ユーザーが明示した目的に合わせて説明と checkpoint を調整する。
- 学習支援を、ユーザーの目的、scope、risk tolerance、approval、final adoption を選ぶ権限へ変換しない。
- AI が安全に実行して説明できる技術作業を、ユーザーに再発見させることを強制しない。
- quiz、ユーザーの自信、または test の成功だけを、理解や正しさの証明にしない。
- 元の workflow が求める高リスク制御を維持する。説明と証拠は、authorization、rollback、recovery、sandbox、deterministic verification の代替にならない。
- agent、tool、model、capability、work unit の選択には `triage-agent-usage` を使う。この Skill は、選択された workflow 内の学習と理解の calibration を所有する。
- 隣接 Skill がない場合も自己完結させる。次の行動の ownership を明確にできる場合だけ handoff 名を示す。
