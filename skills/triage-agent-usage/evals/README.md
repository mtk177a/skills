# triage-agent-usage evals

`triage-agent-usage` の単体運用を評価するためのメモです。作業前に、最も軽い選択肢で足りるかを見極め、重い agent や高性能モデルの必要性を説明できるかを見ます。

## Iter 0

- `description` と本文が「ツール/モデル選定の事前トリアージ」に揃っているか
- リポジトリを読む必要の有無が分かれているか
- 重い選択肢を選ぶ理由が残るか
- 学習目的か納期優先か、本人がレビュー可能かを判定できるか
- 単体で次の依頼先判断に使えるか

## Scenarios

### Scenario A: リポジトリを読まない文章整理

メールや設計メモの整理で、coding agent は不要。通常チャットを勧める。

Requirements checklist:

1. [critical] リポジトリを読む必要がない作業に重い coding agent を既定提案しない
2. 推奨ツールと理由が対応している
3. 渡すべき最小コンテキストが絞られている

### Scenario B: 複数ファイル変更と高リスク判断

実装とテストに加え、セキュリティや破壊的変更の懸念もある。高性能モデルを使う理由を明示する。

Requirements checklist:

1. [critical] 重い選択肢を選ぶ理由を 1 行で説明できる
2. 高リスク要素を軽量選択肢に押し込まない
3. 作業単位が過剰に広くならない
4. `推奨ツール` に具体的なツール名がある
5. `推奨モデル / profile` に具体的な model または profile がある
6. ツール選定と model / profile 選定の理由が対応している

### Scenario C: 学習目的の実装相談

未知領域の実装相談で、納期より理解を優先したい。AI に任せる調査と本人がレビュー・判断する範囲を分ける。

Requirements checklist:

1. [critical] 学習目的か納期優先かを判定軸に含める
2. 本人がレビュー可能な範囲と AI へ委任する範囲が分かれている
3. 理解・レビューに必要な前提が出力に残る

## Failure Ledger Seed

- `heavy agent recommended by default`
- `model choice lacks rationale`
- `context not minimized`
- `tool or profile selection remains generic`
- `learning goal ignored`
