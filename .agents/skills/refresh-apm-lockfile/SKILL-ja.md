---
name: refresh-apm-lockfile
description: mtk177a/skills リポジトリで public Skill または apm.yml の変更を commit / push した後、作業リポジトリへ APM package を展開せず disposable copy で apm.lock.yaml を生成・検証するときだけ使う。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳であり、内容に差異がある場合は英語版を優先してください。

# Refresh APM Lockfile

## 目的

- public Skill または `apm.yml` の変更後、このリポジトリの `apm.lock.yaml` を更新する。
- non-dry-run の APM 操作を作業リポジトリで実行せず、disposable copy に閉じ込める。
- 生成した lockfile を frozen install と audit で検証してから作業リポジトリへ戻す。
- 生成された `apm.lock.yaml` だけを戻し、lockfile commit はユーザーまたは呼び出し元 agent に残す。

## 使うとき

- `mtk177a/skills` リポジトリで作業している。
- 現在の lockfile に記録された commit 以降に、`skills/` 配下の public Skill または `apm.yml` の追加、削除、rename、変更があった。
- public source の変更はすでに commit / push 済み。
- 次の作業が `apm.lock.yaml` を別 commit で更新すること。
- ユーザーが APM lockfile refresh、disposable copy、このリポジトリの自己参照 APM dependency workflow に言及している。

repository guidance、repo-local Skill、無関係な docs、または `apm.lock.yaml` だけの変更後には、この Skill を使わない。script はこの場合を検出し、package source へ接続せず正常終了する。

## 前提条件

- 開始前の working tree が clean。
- 作業リポジトリに tracked、staged、untracked、ignored APM deployment artifact が残っていない。
- `.agents/skills/` には tracked repo-local Skill である `refresh-apm-lockfile` 以外の entry がない。
- `apm_modules/` が存在しない。
- 現在の branch に upstream がある。
- `HEAD` が upstream branch と一致している。
- repository root に `apm.yml` と `apm.lock.yaml` がある。
- インストール済みの APM CLI が `apm lock` をサポートしている。
- 作業リポジトリでは non-dry-run の `apm install` / `apm update` を実行しない。

## 手順

1. 前提条件を確認する。
2. repository root から `scripts/refresh-apm-lockfile.sh` を使う。
3. sandbox により network、SSH、credential access が塞がれる場合は、必要な承認を得て同じ script を再実行する。
4. public source に変更がないと script が報告した場合は、disposable copy や commit を作らず停止する。
5. それ以外の場合は、disposable copy での lock 生成、frozen install、audit が通ったことを確認する。
6. 作業リポジトリの差分が空、または `apm.lock.yaml` だけであることを確認する。
7. 作業リポジトリでの frozen dry-run と `git diff --check` が通ったことを確認する。
8. 差分が残らない場合は、commit を作らず停止する。
9. それ以外の場合は `apm.lock.yaml` だけを別 commit にする。通常は `fix: refresh APM lockfile after <change>` を使う。
10. diff を確認してから lockfile commit を push する。

## Script contract

実行:

```bash
bash .agents/skills/refresh-apm-lockfile/scripts/refresh-apm-lockfile.sh
```

script が行うこと:

- `skills/` 配下と `apm.yml` の public source を、現在の lockfile に記録された commit と比較する
- public source に変更がなければ正常終了する
- refresh が必要な場合は `/tmp` 配下に disposable copy を作る
- disposable copy で `apm lock --update --no-policy` を実行する
- dependency 数と、全 dependency が push 済み `HEAD` を指すことを確認する
- disposable copy で `apm install --frozen --no-policy` と `apm audit --ci --no-policy` を実行する
- 検証済みの `apm.lock.yaml` だけを作業リポジトリに戻す
- 作業リポジトリで `apm install --frozen --dry-run --no-policy` を実行する
- `git diff --check` で空白を確認する
- `apm.lock.yaml` が既に最新の場合は commit instruction を出さず正常終了する

script が行わないこと:

- `apm.yml` を編集しない
- 作業リポジトリで non-dry-run APM command を実行しない
- lock 生成または検証に失敗したとき、update や install command へ fallback しない
- disposable copy の `.agents/skills/` output を戻さない
- commit や push をしない

## 出力フォーマット

- Preconditions: ...
- Public source delta: refresh required | no refresh required
- Disposable copy: ... | not created
- APM command used: ... | not run
- Resolved commit in lockfile: ...
- Working repository diff: ...
- Verification:
  - disposable `apm install --frozen --no-policy`: ...
  - disposable `apm audit --ci --no-policy`: ...
  - `apm install --frozen --dry-run --no-policy`: ...
  - `git diff --check`: ...
- Next action:
  - `git add apm.lock.yaml`
  - `git commit -m "fix: refresh APM lockfile after <change>"`
  - または lockfile が既に最新なら "no commit needed"

## 境界

### Always:

- この Skill は repository-local に保つ。
- non-dry-run APM 操作には disposable copy を使う。
- 作業リポジトリへ戻すのは `apm.lock.yaml` だけにする。
- refresh 前に working tree が dirty なら停止する。untracked file も含める。
- `apm_modules/` や例外外の `.agents/skills/*` entry など、ignored APM deployment artifact がある場合は停止する。
- `HEAD` が upstream branch に push されていない場合は停止する。
- lock 生成、dependency、install、audit、認証、network、policy の error は hard failure とし、調査用に disposable copy を保持する。
- commit と push は明示的な follow-up action として残す。

### Ask first:

- lockfile refresh に `apm.yml` の変更が必要な場合。
- `apm.lock.yaml` 以外のファイルを上書きする必要がある場合。
- failure の解消に別の APM command または distribution workflow が必要と思われる場合。

### Never:

- 作業リポジトリで non-dry-run の `apm install` や `apm update` を実行しない。
- lock 生成を `apm update` や `apm install --update` で代替しない。
- APM integration が生成した `.agents/skills/` output を commit しない。
- commit や push を自動実行しない。
- この repo-local Skill を public Skill catalog や `apm.yml` に追加しない。
