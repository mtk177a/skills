> この文書は [英語版 workflows.md](../../users/workflows.md) の日本語参考訳です。\
> 内容が異なる場合は英語版を優先してください。

# 次に使う Skill を選ぶ

このガイドは、一つの作業で複数の Skill を使う人に向けたものである。\
作業の種類ごとに、通常どの Skill を次に使うかと、次へ進む前に前の Skill が何を報告している必要があるかを示す。\
最初に使う Skill は、[目的別の一覧](../../../README.ja.md#skill-一覧) から選ぶ。

ほとんどの Skill は、最後に `Ready for design` のような状態を報告する。\
次の手順は、その状態を見て選ぶ。

ここに書いたつながりは案内である。\
すべての手順を実行する必要はなく、つながりがあることで何かの操作が許可されるわけでもない。\
入力、出力、作業の範囲は、各 Skill に書かれている。

## 変更する

変更では、通常次の 4 つの Skill を順に使う。

1. **`clarify-request`**
   - 依頼の目的、範囲、成功条件が不明確な場合に使う。\
     すでに明確な場合は省く。
   - `define-referents`、`draft-issue`、`record-session-handoff` などの Skill が、依頼そのものが不明確だと報告した場合も、この Skill に戻る。
2. **`design-changes`**
   - 方針、影響範囲、変更の検証方法を決めるために使う。\
     これらがすでに明確で、変更が許可されている場合は省く。
3. **`implement-changes`**
4. **`review-changes`**
   - [変更をレビューして修正する](#変更をレビューして修正する) に進む。

これらの手順の前や途中で、特定の不足を補う Skill が 2 つある。

- 用語が曖昧な場合は `define-referents` を使い、合意した意味で元の手順に戻る。
- 重要な選択に実質的に異なる選択肢がある場合は `explore-decision-space` を使う。\
  `Selected for design` が報告されたら、`design-changes` に進む。

## 障害を調べる

1. **`investigate-failure`**
   - `Ready for implementation` が報告されたら、`implement-changes` に進む。
   - `Ready for design` が報告されたら、`design-changes` に進む。
   - `Diagnostic next` または `Blocked` が報告されたら、不足している情報を補うか、示された確認を実行してから、調査を続ける。
2. **`implement-changes`**（必要なら設計の後）
3. **`validate-fix`**
   - 修正を、元の障害に照らして確かめる。

調査に、現在の公開文書、注意喚起、提供元の挙動を証拠として使う必要がある場合は、`research-web-safely` で調べられる。\
その場合も、診断は `investigate-failure` が行う。

## 変更をレビューして修正する

レビューでは、通常次の Skill を順に使う。\
各 Skill は決まった情報を次の Skill に渡し、ほかの Skill が担う判断は行わない。

1. **`review-changes`**
   - 指摘を、分類、影響、確度とともに報告する。\
     これらだけでは、指摘に対応するかどうかは決まらない。
2. **`triage-review-feedback`**
   - 指摘ごとに、`Act now`、`Defer`、`No action` のいずれかの対応方針を決める。
   - 実装するのは、`Act now` の作業のうち、許可したものだけである。\
     懸念を認めても、指摘した人の解決案を採用する必要はない。
   - 指摘の確認に現在の公開文書が必要な場合は、`research-web-safely` で調べられる。
3. **`draft-review-comments`**（コメントが必要な場合だけ）
   - 各指摘の評価、状態、対応方針を渡す。\
     この Skill は、これらを判断せずにコメントを下書きする。
   - 指摘のないレビューでは、指摘の判断を省き、`review-changes` の結論、レビューした範囲、実施した確認、その限界を直接渡す。
   - 下書きを作っても、それを投稿することや、GitHub のレビュー操作を選ぶことは許可されない。
4. **`implement-changes`**
5. **`validate-fix`**
   - 修正が完了していなければ、`implement-changes` に戻る。
   - 検証対象の外で、修正が原因の問題が記録されたら、その問題を `review-changes` でレビューする。
   - 差分全体を `review-changes` でもう一度レビューするのは、全体の再レビューを求める場合だけである。

各手順で、証拠と不確実な点を引き継ぐ。\
情報がないことは、リスクが低いことの証拠にならない。

## 変更を説明する

変更を説明するだけで、問題を探さない Skill が 2 つある。

- `summarize-changes` は、PR の説明やリリースノートなどの変更の要約を書く。
- `draft-commit` は、コミットの分け方を決め、メッセージを下書きする。

## リスクのある作業や行き詰まった作業を止める

次の状況では、作業をいったん止めて、対応する Skill を使う。

1. **復旧、運用、セキュリティ、外部の状態に重大な影響がある操作をする: `assess-risky-change-readiness`**
   - 使うかどうかは、「移行」「本番」などの呼び名ではなく、実際の影響で判断する。
   - `design-changes` や `implement-changes` で、追加の重大リスク対策が必要と分かった場合にも使う。
   - `Ready for authorization` は、対策は揃っているが、責任者がまだ操作を承認していない状態である。\
     `Ready for execution handoff` は、操作がすでに許可されている状態であり、この Skill 自体は操作を実行しない。
2. **同じような試行が、新しい証拠を得られないまま失敗し続ける: `break-failure-loop`**
   - `Diagnostic next` が報告されたら、示された確認を実行してから作業に戻る。
   - `Diversify` が報告されたら、`explore-decision-space` に進む。
   - `Blocked` が報告されたら、不足している情報や判断が揃うまで作業を止めたままにする。
3. **重要な選択が、早い段階で一つの方針に絞られている: `explore-decision-space`**
   - `Selected for design` が報告されたら、`design-changes` に進む。
   - 簡単に元に戻せる作業や、十分な比較に基づいて選択済みの作業では使わなくてよい。

## 実行環境を選び、作業内容への理解を保つ

作業に使うチャット、エージェント、モデル、ツールを使える環境、エージェントの構成を選ぶには、`choose-ai-execution-setup` を使う。\
作業内容への理解も保ちたい場合は、選んだ環境の中で `calibrate-learning-support` を続けて使う。

## エージェント向けの指示や Skill を変更する

ここで扱う Skill は、`AGENTS.md` や Skill のように、エージェントが継続して使う指示を対象にする。

1. **`audit-agent-guidance`**
   - エージェントの予期しない挙動の原因が分からない場合に使う。\
     原因がすでに証拠で裏付けられている場合は省く。
2. **`design-skill` または `design-agent-instructions`**
   - Skill の責務と範囲には、`design-skill` を使う。
   - 指示文書の役割分担と、クライアントによる読み込み方には、`design-agent-instructions` を使う。
3. **`implement-changes`**
   - どちらの設計用の Skill も、最後に実装への引き継ぎを作る。\
     設計しただけでは、予期しない挙動が直ったことにはならない。
