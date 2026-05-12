---
name: draft-commit
description: 差分をもとに、コミットメッセージ案やコミット分割案を作りたいときに使う。
---

# Draft Commit (コミット案作成)

## 目的

- 差分をもとに、日本語の Conventional Commits 形式でコミット案を作る。

## 使う場面

- コミットメッセージを考えたいとき
- 変更をどの単位でコミット分割するか整理したいとき
- `releaser` に渡す前にコミット単位を整えたいとき

## 入力

- `git diff`
- `git diff --staged`
- 未追跡ファイルの差分

## 手順

1. 変更内容を把握するために、可能なら `git diff` と `git diff --staged` を確認する。
2. 未追跡ファイルがある場合は `git status -sb` で検知し、必要なら `git add -N <path>` または `git diff --no-index /dev/null <path>` で差分を確認する。
3. 関心事が複数ある場合は、ファイル単位または機能単位でコミット分割案を考える。
4. 各コミットの主目的を 1 つに絞る。
5. Conventional Commits 形式で各コミット案を作る。
6. `summary` が日本語で短く具体的になっているか確認する。
7. scope は明示的な規約がある場合のみ従い、規約が不明な場合は無理に付けない。
8. 必要なら `committer` を使って提案を安定化させる。
9. タイプ選定の詳細が必要なら `references/commit-types.md` を参照する。

## 出力フォーマット

```text
<commit 1>
<type>(<optional-scope>): <summary>
files: <file1>, <file2>

<commit 2>
<type>(<optional-scope>): <summary>
files: <file1>, <file2>
```

```text
<commit 1>
docs: summary の日本語必須ルールを追記
files: skills/draft-commit/SKILL.md
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
- summary は日本語で書く
- 関心事が複数なら分割して提案する
- 各コミット案に `files:` を付ける

### Ask first:

- 差分が取得できない場合
- diff から主目的が特定できない場合

### Never:

- 実際にコミットを実行する
- 差分を見ずに推測で提案する
