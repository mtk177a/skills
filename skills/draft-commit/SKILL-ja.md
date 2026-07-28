---
name: draft-commit
description: 明示的に対象化された Git の変更集合から、staged・unstaged・untracked の境界を保ちながら、原子的なコミット計画と Conventional Commits メッセージを作成する。コミットメッセージ、コミット分割、または明示的に承認された commit workflow の事前整理に使う。PR 要約、差分レビュー、実装、または Skill の呼び出し自体を stage・commit の権限として扱う用途には使わない。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Draft Commit（コミット案作成）

## 目的

- 明示的に対象化された Git の変更集合から、一つ以上の一貫したコミット計画と完全な Conventional Commits メッセージを作る。
- リポジトリの既存 index を保護し、staged、unstaged、untracked、提供された差分だけの変更を区別する。
- Skill の呼び出しを変更権限として扱わず、別途承認された commit workflow を支援できる read-only の handoff を返す。

## 対象と根拠

案を作る前に、effective change set を確定する。

1. 明示的に提供された diff、path 集合、commit range、または staged-only の範囲があれば、それを使う。
2. 元の workflow から明示的な範囲を引き継いでいる場合は、それを使う。
3. ローカルの「現在の変更」という指定だけの場合は、staged、unstaged、関連する untracked changes を確認し、含めた範囲を明示する。
4. 複数の妥当な解釈によってコミット内容が実質的に変わる場合だけ質問する。変更集合を取得できない場合は、案を作成できなかったと報告する。

対象リポジトリに明示された type、scope、message、summary の言語規約を先に読む。変更目的と、変更理由を示す利用可能な Issue、設計、実装 handoff、テスト、周辺証拠を確認する。diff は「何が変わったか」の根拠として扱い、「なぜ変わったか」を単独で証明するものとは扱わない。

関連する各変更を `Staged`、`Unstaged`、`Untracked`、`Partially staged`、`Provided diff only` のいずれかに分類する。リポジトリ状態を伴わない提供 diff からメッセージ案は作れるが、現在の index を確認済みとしたり、実行可能な staging command を正当化したりしない。

## 手順

1. Effective change set、リポジトリ規約、利用可能な意図の根拠、重要な除外範囲を明示する。
2. リポジトリ状態を確認できる場合は status と diff stat から始め、各コミット案を理解できるところまで staged、unstaged、untracked の内容を確認する。段階的な確認で context を節約できるが、目的やグループ分けが不明な path や hunk を確認せずに含めない。
3. 変更 inventory を作る。対象内の各 path または hunk を一度だけ、特定のコミットへ `Included` として割り当てるか、`Excluded` として明示的に外すか、`Unresolved` とする。変更を黙って省略・重複させない。
4. diff に secret または credential の疑いがある場合は、その値を再掲せず、その内容について通常のコミット計画を続けない。必要最小限の path と分類だけを示して対象から外し、必要な対処または不確実性を報告する。根拠なしに無害な placeholder と仮定しない。
5. 一つの一貫した目的、必要な依存関係、レビュー可能な振る舞いごとに変更をまとめる。同じファイルの変更が異なる関心事に属する場合は hunk 単位で分ける。rename と delete の対応を保ち、必要なコミット順を明示する。必要な数だけコミットを使い、数値上限のために関心事を統合・省略しない。
6. リポジトリ規約、確認済みの変更意図、observable な semantic effect、互換性への影響から type を選ぶ。不足している意図によって type が実質的に変わり得る場合は、構文だけから推測せず、質問するか `Unresolved` とする。
7. 完全なメッセージ案を作る。summary は対象リポジトリが指定する言語を使い、指定がなければユーザーの言語を使う。どちらからも判断できない場合は質問するか、言語を unresolved とする。scope はリポジトリ規約が対応しているか、その規約下で明らかに有用な場合だけ付ける。文脈、参照、release automation に必要なら body または footer を追加する。breaking change には必ず `!` または `BREAKING CHANGE:` footer を付ける。type、breaking change、body、footer の判断が自明でない場合は `references/commit-types.md` を読む。
8. 既存の staged content と除外した worktree changes を保護する staging plan を作る。partially staged file は、working tree のファイル全体で index を置き換えず、hunk 単位の操作として扱う。
9. リポジトリ状態を確認済みで、曖昧さなく計画を表現できる場合だけ候補 command を示す。安全で portable な表現ができない場合は command を省略し、理由を説明する。
10. 対象内の変更が一度ずつ割り当てられていること、各コミットの主目的が一つであること、メッセージが確認済みの意図とローカル規約に一致すること、除外した内容が除外されたままであること、Skill がリポジトリ状態を変更していないことを確認する。

## 安全な command の規則

- 意図した内容がすでに staged なら、不要な `git add` を付けない。
- 現在のファイル全体がそのコミットに属し、除外対象または unstaged の別関心事を含めない場合だけ、ファイル単位の `git add` を使う。
- hunk 単位の staging には `git add -p -- <path>` または同等の対話手順を使う。対話 command を、選択内容まで確定した run-as-is の command と表現しない。
- pathspec の前に `--` を置き、確認した shell に合わせて path を quote する。path または message を安全かつ portable に表現できない場合は、shell command を付けず semantic plan を示す。
- 複数行 message、body、footer は、安全な command 表現を確立できない限り message blockとして示す。不安定な一行の `git commit -m` へ強制しない。
- 現在のリポジトリ状態を確認できない `Provided diff only` には、staging または commit command を出さない。

## 報告契約

タスクに合わせて表現を調整し、空の節は省略する。次の意味情報を維持する。

- effective change set、関連するリポジトリ規約、意図の根拠
- 各コミット案の主目的、完全な message、現在の状態を付けた対象 path または hunk、依存順、staging plan
- 安全な command の規則を満たす場合だけ候補 command
- excluded changes と unresolved changes
- secret の疑いに対する扱い、その他の停止理由、未確認事項
- 実行していないリポジトリ変更と次の handoff

案の作成が blocked の場合は、不足している変更集合、重要な意図、リポジトリ規約、安全な staging 判断を明示し、影響する範囲を unresolved のまま残す。結果を完全な計画として示さない。

## 権限と workflow の境界

- この Skill の読み込みや明示呼び出しは、`git add`、`git commit`、`git push`、index の変更、実装、その他のリポジトリ書き込みを許可しない。
- 元の依頼がすでにコミットを明示的に許可している場合は、その workflow へ draft と staging handoff を返す。追加の普遍的な承認gateを捏造したり、権限を持つ caller の続行を妨げたりしない。
- `summarize-changes`、`review-changes`、実装 workflow を置き換えない。この Skill はコミット単位とメッセージを作り、PR descriptionを書いたり、レビュー指摘を発見したり、ファイルを変更したりしない。
- message、command、説明へ secret または credential を出力しない。
- ユーザーの無関係な変更を変更・破棄したり、黙ってコミット対象へ取り込んだりしない。
