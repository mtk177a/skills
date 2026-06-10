---
name: draft-commit
description: 差分をもとに、コミットメッセージ案やコミット分割案を作りたいときに使う。
license: Apache-2.0
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Draft Commit (コミット案作成)

## 目的

- 差分をもとに、日本語の Conventional Commits 形式でコミット案を作る。

## 使う場面

- コミットメッセージを考えたいとき
- 変更をどの単位でコミット分割するか整理したいとき
- コミット前に変更を論点ごとに分けたいとき

## 入力

- 現在作業中の対象リポジトリに明示されたコミット規約
- `git status -sb`
- `git diff --stat`
- 必要なファイルだけの `git diff -- <path>`
- 必要なファイルだけの `git diff --staged -- <path>`
- 未追跡ファイルの内容

## 手順

1. まず現在作業中の対象リポジトリに明示されたコミット規約を確認し、コミット type や scope のローカル規約があればそれを優先する。
2. 次に `git status -sb` で変更ファイルの種類と件数を把握する。
3. 次に `git diff --stat` と、必要なら `git diff --staged --stat` で差分規模を把握する。
4. いきなり diff 全文を読むのではなく、必要なファイルだけ `git diff -- <path>` または `git diff --staged -- <path>` で確認する。
5. 未追跡ファイルがある場合は、内容確認が必要なものだけ差分相当を確認する。
6. 関心事が複数ある場合は、ファイル単位または機能単位でコミット分割案を考える。
7. 各コミットの主目的を 1 つに絞る。
8. Conventional Commits 形式で各コミット案を作る。
9. `summary` が日本語で短く具体的になっているか確認する。
10. scope は明示的な規約がある場合のみ従い、規約が不明な場合は無理に付けない。
11. rename / move を含む差分では、新 path だけでなく旧 path 側の delete も確認し、`git add` に rename 前後の path を含める。無関係な既存差分は含めない。
12. 各コミット案について、`git add ...` と `git commit -m "..."` をそのまま実行できる形で並べる。
13. 提案は最大 3 案までに絞る。
14. タイプ選定の詳細が必要なら `references/commit-types.md` を参照する。
15. 差分が複数関心事に分かれ、かつユーザーが追加確認を求めた場合だけ、別 agent の利用を検討する。

## 出力フォーマット

```text
<commit 1>
<type>(<optional-scope>): <summary>
files: <file1>, <file2>
git add <file1> <file2>
git commit -m "<type>(<optional-scope>): <summary>"
```

## タイプ選定ガイド (例)

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント更新
- `style`: 仕様に影響しないコードの整形
- `refactor`: 振る舞いを変えない構造改善
- `perf`: 性能改善
- `test`: テスト追加・修正
- `build`: ビルドや依存関係
- `ci`: CI 関連
- `chore`: 雑務や補助的変更

## 境界

### Always:

- 差分に基づいて提案する
- 対象リポジトリに明示されたコミット規約を先に確認する
- summary は日本語で書く
- 関心事が複数なら分割して提案する
- `git status -sb` と `git diff --stat` から確認を始める
- 必要なファイルだけ個別 diff を読む
- 提案は最大 3 案までに絞る
- rename / move を含む差分では、旧 path / 新 path と無関係な既存差分の扱いを staging 方針として明示する
- 各コミット案に `files:` を付ける
- 各コミット案に `git add ...` と `git commit -m "..."` を付ける

### Ask first:

- 差分が取得できない場合
- diff から主目的が特定できない場合
- 差分が複数関心事に分かれ、追加確認のために別 agent を使いたい場合

### Never:

- 実際にコミットを実行する
- 差分を見ずに推測で提案する
