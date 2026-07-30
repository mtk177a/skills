---
name: triage-agent-usage
description: 作業開始前に、適切な agent、tool、model capability、work-unit size を選ぶ。chat、completion、coding agent、より強い reasoning の選択、または運用上の委任分割を判断するときに使う。作業中の学習・理解の calibration、実質的な実装設計の選択、task 自体の実行には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Triage Agent Usage

## 目的

- 許容できる正しさと手戻りリスクで task を実行できる、最も軽い execution surface と model capability を選ぶ。
- 運用上の委任を review 可能な work unit へ分け、各 unit に必要な context だけを渡す。
- tool・capability 選択を、task の実質的な判断や learning calibration から分離する。

## 証拠

利用可能な情報を集める。

- task type と期待する outcome
- repository、external system、execution への access が必要か
- 影響範囲、verification needs、不確実性、可逆性、失敗コスト
- 利用可能な tool、model、profile、permission、environment constraints
- 独立した context、specialist analysis、parallel work に具体的な効果があるか

task が重要という理由だけで、より重い agent が適切と推測しない。利用可能性や capability を確認できない tool・profile を利用可能なものとして推奨しない。

## 選択 workflow

1. text organization、repository implementation、investigation、review、external-system interaction など、必要な operational work を分類する。
2. 証拠を読み、承認済み scope 内で行動し、結果を検証するために必要な capability を特定する。
3. 必要な capability を満たす最も軽い execution surface から検討する。不確実性、影響、context 量、verification complexity に具体的な理由がある場合に model または agent の重さを上げる。
4. 1 session、独立 context、specialist review、parallel unit のどれが必要か判断する。別 agent を既定で導入しない。
5. 委任する作業を、一貫した outcome、ownership、verification boundary で分ける。証拠や変更を review できないほど広い work unit を避ける。
6. 各 unit の objective、constraints、relevant evidence、authority、completion check を失わない範囲で context を最小化する。
7. 推奨と、より重い capability、追加 agent、広い context が必要な理由を示す。
8. 選択した execution setup を引き継ぐ。実装設計、調査結論、採否判断は、それを所有する workflow に残す。

## 判断基準

次は固定的な tool mapping ではなく heuristic として使う。

- repository や execution access が不要なら ordinary chat を使う
- 小さく既存 pattern に沿う edit で、出力を局所 review できる場合は completion または lightweight coding surface を使う
- repository discovery、multi-file change、test execution が必要なら coding agent を使う
- 重要な未解決の不確実性、手戻りコスト、security・authorization 上の影響、曖昧な証拠がある場合は、より強い reasoning を使う
- context isolation、specialist judgment、latency reduction が coordination・review cost を上回る場合だけ、独立または parallel agent を使う

選択した workflow を進めながら理解を保持または回復したい場合は、`calibrate-learning-support` への任意 handoff を返す。この Skill で teaching method、comprehension checkpoint、ユーザーの learning depth を決めない。

## Reporting contract

判断に合わせて応答を調整する。次を含める。

- 推奨する execution surface または tool
- 選択が重要な場合の model capability または profile
- 最も軽い適切な選択肢より強いものへ上げる理由
- work unit と ownership
- 各 unit に必要な最小 context、permission、期待する verification
- 利用可能性または capability に関する未確認の前提
- ユーザーが求めた場合の任意の learning-calibration handoff

利用可能な証拠が要求しない場合は、特定の model、profile、複数 agent、固定 template を強制しない。

## 境界

- task を実行せず、実質的な実装方式を選ばず、tool 選択を authorization として扱わない。
- 高影響な requirement、scope、risk tolerance、adoption decision をユーザーに代わって決めない。
- repository または execution capability が不要な作業に heavy coding agent を推奨しない。
- 別 agent または subagent を既定で使わず、context、specialization、verification、latency 上の具体的な効果を要求する。
- 学習・理解の calibration は `calibrate-learning-support` に残し、その Skill がない場合も自己完結させる。
