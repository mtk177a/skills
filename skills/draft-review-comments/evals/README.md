# draft-review-comments evals

`draft-review-comments` の単体運用を評価するためのメモです。新しい指摘を発見したり採否を決めたりせず、発見済み・整理済みの指摘を GitHub PR 向けコメント案へ落とせるかを見ます。

## Iter 0

- `description` と本文が「レビューコメント文面の提案」に揃っているか
- 新規指摘発見や採否判断に責務が漏れていないか
- 行コメントでは位置とコメント本文がセットで返るか
- 行コメント位置で `path:line` と `path:start-end` を適切に使い分けるか
- `must` / `should` / `nit` の強さが文面に反映されるか
- 断定の強さが根拠の強さに揃っているか
- 行コメント / review summary / 全体コメント相当を使い分けられるか
- review summary / 全体コメント相当で位置を強制しないか
- まとめるべき関連指摘を過不足なく集約できるか
- `Approve with comments` の文面が hidden blocker になっていないか
- `Nice-to-have` 相当が blocker 扱いになっていないか
- トーン未指定時でも既定で圧迫的でない文面になるか

## Scenarios

### Scenario A: 初回レビューのコメント案作成

2-3 件の指摘、対象位置、重要度を受け取り、強い根拠の `must` と静的読解ベースの `should`、`Nice-to-have` 相当の軽微提案を含めて返す。

Requirements checklist:

1. [critical] 各コメントが 1 論点になっている
2. 位置と本文が対応している
3. 期待アクションが分かる
4. 静的読解ベースの指摘で断定しすぎない
5. `Nice-to-have` 相当が `nit` 相当の非 blocker トーンで返る

### Scenario B: 再レビューの整理

前回指摘と今回差分の要約があり、`resolved` / `remaining` / `new` を分けてコメント案と summary を返す。Approve しつつ補足コメントだけ残す論点も含む。

Requirements checklist:

1. [critical] `remaining` を `new` と混同しない
2. resolved を無理に再指摘しない
3. summary に状態差分がある
4. Approve 時の補足コメントが blocker と読めない
5. summary や補足コメントで位置を無理に要求しない

### Scenario C: stacked PR の後続許容

この PR 起点だが、後続 PR での修正でもよい論点を含む。全体コメント相当に寄せた方が自然なケースも含む。

Requirements checklist:

1. [critical] 今回必須か後続許容かが分かる
2. blocker でない論点を過剰に強くしない
3. 後続 PR へ送れる理由が書かれる
4. 全体コメント相当として返す場合は位置なしでも自然に読める

### Scenario D: 同じ根本原因の集約

2 つの症状が同じ原因から生じており、別々にコメントするとノイズが増える。

Requirements checklist:

1. [critical] 根本原因ベースで 1 論点にまとめられる
2. まとめても次のアクションが曖昧にならない
3. コメント位置が結果の行ではなく直接原因の行に寄る

### Scenario E: 具体条件の明示

条件分岐や null 判定が原因の指摘をコメント化する。`この条件` のような抽象語ではなく、対象の識別子や条件式を文面に含められるかを見る。

Requirements checklist:

1. [critical] コメントが期待結果、現状挙動、具体条件の順で読める
2. 識別子や条件式が必要な範囲で明示されている
3. 具体化しても文面が冗長になりすぎない

### Scenario F: 指定 diff に固定したコメント位置

stacked PR や実質 diff 指定があり、current working tree や後続 PR では行番号や原因箇所がずれている。コメント位置、型名、原因説明を指定された commit range に固定して返せるかを見る。

Requirements checklist:

1. [critical] `path:line` または `path:start-end` が指定 diff 上の位置に一致する
2. current working tree や後続 PR の状態を根拠に混ぜない
3. 直接原因の行を優先する
4. コメント本文中の型名や差分説明も指定 range と整合している

### Scenario G: 複数行にまたがるコメント位置

複数行の条件式、関数呼び出し、追加 / 削除ブロック全体が原因の指摘をコメント化する。単一行だけに固定せず、GitHub で範囲選択して貼れる位置を返せるかを見る。

Requirements checklist:

1. [critical] 複数行全体が論点なら `path:start-end` で返る
2. 単一行で十分な論点まで不要に範囲指定しない
3. 範囲指定しても 1 コメント 1 論点が保たれている
4. 指摘の本文が範囲内の式、条件、ブロックと対応している

### Scenario H: 既定トーンが柔らかめ

トーン指定なしで、`must` / `should` / `nit` が混在する指摘をコメント化する。正しさと期待アクションを保ちつつ、既定で柔らかめの文面になっているかを見る。

Requirements checklist:

1. [critical] トーン未指定でも詰問調や圧迫的な語尾にならない
2. `must` でも期待アクションが曖昧にならない
3. 作者ではなくコードに向いた文面になっている
4. 非 blocker の論点が hidden blocker に見えない
5. 必要なら短い理由や影響が添えられている

## Failure Ledger Seed

- `comment mixes multiple issues`
- `tone stronger than severity`
- `assertiveness stronger than evidence`
- `location and comment do not match`
- `root-cause comments split into noisy fragments`
- `summary loses actionability`
- `approve-with-comments reads like hidden blocker`
- `summary wrongly forced into path:line`
- `multi-line comment collapsed to single line`
- `single-line comment widened unnecessarily`
- `nice-to-have escalated into blocker wording`
- `stacked-pr deferral phrasing unclear`
- `comment anchored to current tree instead of requested diff`
- `default tone sounds harsher than requested`
- `soft-tone request still sounds interrogative`
- `comment targets author not code`
- `non-blocker phrasing reads as hidden blocker`
