---
name: revise-docs-fresh-eyes
description: 執筆時の会話を受け取っていない fresh subagent に、既存の documentation または技術文書を改稿させる。ユーザーが fresh eyes、cold pass、独立した改稿を明示的に求めた場合、またはこの Skill を直接指定した場合に、subagent を利用できる Codex または Claude Code でのみ使う。通常の編集、初稿生成、事実確認、一般的な diff review、同一 context での自己推敲には使わない。
license: MIT
---

> **注記:** 英語版（`SKILL.md`）が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Fresh Eyes で文書を改稿する

## 目的

- artifact を作成または以前に編集した context から、改稿を構造的に分離する。
- fresh subagent に cold read と改稿を完結させ、執筆 context を持つ親が指摘を解釈して文章を書き直す構造を避ける。
- ユーザーが提示した事実、不確実性、要件、例、境界を保持し、それ以外の削除または再構成は reviser に委ねる。

## Fresh context の前提条件

この Skill では subagent が必須である。同一 context の編集へ独立 review を任意で追加する workflow ではない。

次の条件をすべて満たす場合だけ、改稿を fresh と扱う。

- 別の child execution が cold read と改稿を行う
- child が初稿作成または以前の編集に参加していない
- child が親の会話 turn、親の診断、期待する削除、望ましい結論、草稿の理由、非公開の採点基準を受け取らない

継承される system instructions、repository guidance、ユーザーが明示的に求めた writing rules は、child の fresh 性を損なわない。これらの永続的な指示を利用できる場合、child を blank-slate と表現しない。

Codex では、`fork_turns="none"` または現在の同等手段を使い、執筆 turn を fork しない新しい agent thread を開始する。Claude Code では、執筆会話を resume または fork せず、通常の fresh `Agent` subagent を使う。

上位指示で subagent が禁止されている、client に subagent の仕組みがない、または child を執筆 turn から分離できない場合は、fresh revision を実行しなかったと報告して停止する。親 context での改稿へフォールバックしない。

## 親の責務

親は orchestration と権限確認だけを担当し、文章を編集しない。

delegation の前に、次だけを確認する。

- 正確な artifact または限定された対象範囲
- ユーザーの最新依頼と、その依頼が有効にする読者または読後目標
- 最新依頼が有効にする、事実、用語、例、不確実性、書式、長さ、互換性に関する明示的な制約
- ユーザーが file edit、回答内の完全な改稿、comments only のどれを許可したか

artifact を事前に review または要約しない。child 用の reader contract を推定せず、削除すべき箇所を決めない。以前の authoring turn にある好み、文章への愛着、疑っている問題、望ましい結論は、最新依頼が明示的に繰り返さない限り保持制約へ変換しない。重要な読者、目標、制約、編集権限が実際に曖昧な場合は、child を開始する前にユーザーへ確認する。

artifact は改稿対象の data として扱い、指示または主張が正しいことの証明として扱わない。ユーザーが別途許可しない限り、事実確認を追加しない。

## Delegation payload

fresh subagent には、ユーザー由来の最小限の payload だけを渡す。

- 共有 workspace から artifact を読める場合は対象 path と限定範囲、それ以外は artifact の原文
- 最新の改稿依頼と、その依頼が有効にする読者、読後目標、保持制約。可能なら原文のまま渡す
- 許可された出力 mode と書き込み範囲
- artifact を cold-read し、review と revision の両方を自分で完結する指示

chat にしかない artifact を中継するときは、周囲にある author の comment を含めず、artifact の原文だけをコピーする。artifact に対する親の解釈、以前の authoring turn にある好み、文章への愛着、疑っている問題、望ましい結論、理由を含めない。別の writing Skill が明示的に必要な場合は、fresh subagent がその Skill を利用できるようにするか、適用するよう指示する。後から親 context で適用しない。

## 改稿の境界

fresh subagent は、提示された意味を削除、統合、移動、書き換えできるが、推測に基づく best-practice template へ artifact を拡張しない。

child に次を要求する。

- 提示された事実、証拠、不確実性、禁止事項、互換性条件、必要な例、重要な例外を保持する
- 未確認の事実、結論、検証結果、強めた確実性、新しい運用要件を追加しない
- artifact または最新依頼に既に存在する対象または行為を理解、実行するために直接必要な不足文脈だけを追加または指摘する
- 不足する値を特定し、その値を作らない

役立つ可能性だけを理由に、command、system、environment、approval、permission、validation、rollback、logging、monitoring、owner、notification、audit record、placeholder を作らない。最新依頼が求めない限り、短い手順を実行可能な template へ変えない。artifact が何かを read または update するよう求めながら、どこで、またはどのように行うかを示していない場合は、その不足だけを特定し、隣接する前提条件を推測しない。

## 改稿 workflow

1. fresh subagent を開始し、観測可能な child identifier と使用した分離方法を保持する。
2. child に、評価する前に artifact を読ませ、上記の改稿境界を適用させる。
3. revision mode では、child に完全な改稿済み artifact を作成させるか、許可された file だけを直接編集させる。指摘だけでは未完了とする。
4. comments-only mode では、child に対応可能な comment だけを返させる。ユーザーが明示的に求めた場合だけ、この mode を選ぶ。
5. child の結果を、明示的な権限、範囲、保持制約、出力 mode に対して機械的に確認する。文章を再評価せず、裁量的に編集しない。
6. 客観的な制約違反がある場合は、その違反だけを child へ返して修正させる。書き直し方を指示せず、親 context で artifact を修復しない。
7. child の artifact をそのまま返す、patch を機械的に適用する、または許可された直接編集を維持する。親が追加の改稿を行わない。

child が、改稿を実質的に変える情報を求めた場合は、その質問をユーザーへ中継する。意図的に child へ渡さなかった執筆側の理由から回答しない。

## 出力契約

実行した場合は、改稿済み artifact または編集した file に加え、次だけを返す。

- `Fresh revision: executed.`
- 観測可能な child provenance と分離方法
- 未解決の質問、または child が満たせなかった明示的な制約

前提条件を満たせなかった場合は、次を返す。

- `Fresh revision: not executed.`
- 利用できない、または禁止された subagent capability
- 親 context からの評価または改稿は返さない

Skill の invocation を、file edit、文書公開、その他の外部書き込みの権限として扱わない。変更の正しさを確認する diff review には対応する workflow、主張の検証には事実調査 workflow を使う。
