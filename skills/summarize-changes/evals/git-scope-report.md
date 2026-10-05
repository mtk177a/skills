# Real Git scope evaluation — 2026-10-05

The three historical real-Git cases passed in the recorded Codex CLI environment after repository write permissions were removed.\
Each verdict combines the final response, completed command trace, and post-run integrity checks; it is not a verdict for the Runner text cases or other clients.

## Execution conditions

- Candidate `SKILL.md` SHA-256: `416336f4f3ab05920b128d942ade3d0428e2e3e150d90e85e7866b7e63056ac7`
- Codex CLI `0.155.1`, model `gpt-6-luna`, reasoning `max`, macOS, 2026-10-05
- The repositories used the historical Git data and prompts from `git-scope-fixtures.json`, with a repository-local copy of the candidate Skill.
- All write permission bits were removed recursively, including from `.git/`; a direct file-creation probe was denied before execution.
- The CLI used a read-only permission profile, `approval_policy=never`, `--ephemeral --json --ignore-rules`, disabled plugins, and a read guard plus disabled catalog entries for the personal same-name Skill.
- User configuration remained available for authentication; `mcp_servers.serena.enabled=false` was supplied, but Serena still started.
- Responses, JSONL, stderr, prompts, and manifests were saved outside `repo/` under the system-temporary directory named `summarize-changes-git-scope-73-v4`.
- Model fixtures were prepared using the helper at `3907d81` and manually made read-only.\
  The updated helper automates the same barrier and additionally records directories; its fresh-fixture checks were tested separately without rerunning the model.

## Cause and isolation evidence

The client configuration starts Serena with `--project-from-cwd`.\
Serena 1.7.0's startup log for the writable trial records automatic project detection, `serena.config.serena_config:autogenerate` saving `.serena/project.yml`, and `serena.project:__init__` creating `.serena/.gitignore`.\
The model's completed command trace contains no write command responsible for those files.

For the three read-only runs, Serena startup logs at 15:44:04, 15:45:52, and 15:46:52 JST record `PermissionError: [Errno 13] Permission denied` for the attempted `.serena` directory.\
The model completed each run, and no `.serena` directory or other repository mutation was found afterward.\
This is a verified containment of startup writes, not a fix for the client's startup behavior.

The reason Serena starts despite the disabled configuration entry remains unverified.\
Two preliminary `--ignore-user-config` attempts failed with HTTP 401 before obtaining a model response; they are not graded cases.\
The writable trial returned a response but failed integrity and is not counted as a pass.

## Verdicts

| Case | Response and scope evidence | Integrity | Verdict |
| --- | --- | --- | --- |
| staged-only-pr-description | Uses the cached diff; covers implementation and empty test addition; excludes unstaged operations and untracked experiment; states tests were not run | Passed | Passed |
| commit-range-public-release | Uses `release-base..HEAD`; covers CSV export and the `--output` to `--format` migration; omits internal rollout details | Passed | Passed |
| pr-range-operational-handoff | Uses `git diff main...feature`; covers API and migration, deployment order, reported CI, unverified smoke check, monitoring, and rollback | Passed | Passed |

The branch fixture has a linear base, so `git diff main..feature` would produce the same response inventory.\
The completed diff commands below explicitly use three dots, which makes this execution's operator distinguishable.\
`git log main..feature` would be valid history inspection and must not be confused with a two-dot diff.\
If a future client does not expose the diff command or its merge-base equivalent, the branch selection verdict is inconclusive; the response alone is insufficient.

## Recorded responses and completed commands

The following responses and command strings are copied from each saved `last-message.txt` and completed `command_execution` JSONL item.\
The full JSONL tool outputs remain in the temporary artifact directories.

### staged-only-pr-description

Recorded HEAD: `faed88fe91b4007a01afcbe11409a3e1f065e0fd`.

Final response:

```text
## Invoice export

### Summary
`ExportInvoice` now returns the invoice ID as `invoice:<id>` instead of an empty string.\
This gives callers a string that identifies the exported invoice.

### Changes
- Update `ExportInvoice` to prefix the supplied ID with `invoice:`.
- Add `TestInvoiceExport`, which is currently empty and does not assert behavior.

### Reviewer context
Confirm that `invoice:<id>` is the intended output format. The staged changes do not establish which callers consume this value or whether the format is part of a public contract.

### Verification
- Tests: Not run.
- `git diff --cached --check`: passed.
```

Completed commands:

```text
exit_code=0
/bin/zsh -lc "cat .agents/skills/summarize-changes/SKILL.md && printf '\\n--- status ---\\n' && git status --short && printf '\\n--- staged names ---\\n' && git diff --cached --name-status && printf '\\n--- staged diff ---\\n' && git diff --cached --"

exit_code=0
/bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'README*' -g 'CONTRIBUTING*' -g '.github/**' -g '*PULL_REQUEST_TEMPLATE*' -g '*pull_request_template*' | sort && git diff --cached --check && git diff --cached --stat"
```

Artifact SHA-256:

- `last-message.txt`: `830dcfc637dffb07a9837f6906e4e8eda1137c1d636d48e6878f651ec8b8658a`
- `events.jsonl`: `db23722690f79e6b18615f852458b3e0aa492f27132fd98dc785f8250aebfb8d`
- `manifest.json`: `d245774a1342cee541e2eb1d1ff3f205606a3cae20cad128cac8f4df2bab9cb9`

### commit-range-public-release

Recorded HEAD: `24c6a76686766cad21298fde803ebaf2f9f746fe`.

Final response:

```text
## Release notes

- Added CSV export.
- Renamed the command flag from `--output` to `--format`. Update commands that use `--output` to use `--format` instead.
```

Completed commands:

```text
exit_code=0
/bin/zsh -lc 'cat .agents/skills/summarize-changes/SKILL.md && git status --short && git diff --stat release-base..HEAD && git log --oneline --decorate release-base..HEAD'

exit_code=0
/bin/zsh -lc "git diff --find-renames --format=fuller release-base..HEAD -- README.md cmd/options.go src/export.go && git show --stat --oneline --decorate release-base..HEAD && rg --files -g 'CHANGELOG*' -g 'RELEASE*' -g 'docs/**' -g '*release*' -g 'README*'"
```

Artifact SHA-256:

- `last-message.txt`: `8f0d1d9dabaa71eb4dabac89e02bd0c569ecfed2e563d8c5ea00fbc56e2d8ad8`
- `events.jsonl`: `a871a2a013e116db339e77886f7b9f26748c8541732452ce374240f86e669362`
- `manifest.json`: `4d1f17fc494f3d973bbaec0236362df6196f6fce4f74457ade68340d38f7f1d0`

### pr-range-operational-handoff

Recorded HEAD: `7e9a090c51b5bc4d51c23712eaeb6c56d4dcf54f`.

Final response:

```text
## 運用リリース引き継ぎ: `main...feature`

### リリース内容

対象の差分は `api/region.go` と `migrations/20260729_add_region.sql` です。

API の `Region()` は空文字列ではなく `ap-northeast-1` を返すようになります。

マイグレーションの `regions` テーブル定義に `name text` が加わります。
依頼者の説明では additive migration ですが、適用先での実行状況は未確認です。

### 適用順序

1. `20260729_add_region` を適用し、完了を確認します。
2. その後、API の変更をデプロイします。

### 確認状況

- CI の unit test は通過したとの報告がありますが、CI を参照できないため未確認です。
- 本番 smoke check は未確認です。
- この引き継ぎ作成時にローカルテストは実行していません。

### 監視と切り戻し

`region_lookup_errors` を監視します。
監視閾値と判定時間は指定されていません。

切り戻す場合は API を `api-2026.07.28` に戻し、additive migration は残します。

### 未確認事項

本番 smoke check の結果と、適用先でのマイグレーション完了状況は未確認です。
```

Completed commands:

```text
exit_code=0
/bin/zsh -lc 'cat .agents/skills/summarize-changes/SKILL.md && git status --short && git diff --stat main...feature && git diff --name-status main...feature'

exit_code=0
/bin/zsh -lc 'git diff --no-ext-diff --unified=80 main...feature -- api/region.go migrations/20260729_add_region.sql'

exit_code=1
/bin/zsh -lc "rg -n \"region_lookup_errors|region_lookup|20260729_add_region|api-2026\\.07\\.28|smoke check|smoke test|release handoff\" --glob '"'!/.git/**'"' ."

exit_code=1
/bin/zsh -lc "rg --files -g 'AGENTS.md' -g '*release*' -g '*deploy*' -g '*runbook*' -g 'README*' -g '*CHANGELOG*'"
```

Artifact SHA-256:

- `last-message.txt`: `ada3186addb199118dc9058a06afb8ceafa6fa279d1ad227141265e4fb43c5b7`
- `events.jsonl`: `cf5a34790343e4bf3463062e36ea582becaffe34f1069490ebeb9d983439863e`
- `manifest.json`: `ca488d5b91ffb432849dfc620a7d4f0d04a2b39137a9627189937ddf496eec4b`

## Integrity and helper validation

After each model run, the original helper's `--verify` passed for all three repositories.\
A final read-only cross-check using the updated helper's scope and permission checks also confirmed unchanged HEAD, named scopes, status, file hashes, directories, prompt hashes, and write barriers for all three.\
For the earlier manifest format, expected directories were derived from the recorded file parents without modifying the saved manifests.

The updated helper generated and verified a fresh set of three sealed fixtures.\
Adding an empty directory after generation failed verification with `added .empty-generated-directory`, and restoring a write permission failed the barrier check.\
Repository consistency checks, all 151 repository unit tests, Python syntax parsing, and `git diff --check` passed.\
A preliminary `py_compile` check could not create `__pycache__` in the source worktree sandbox; syntax parsing provided the non-writing check instead.

The English Skill body and Japanese reference translation were not changed by this correction.\
Model stability across repeated runs, other models or clients, the Runner text cases, and the underlying client disable-flag behavior were not tested.
