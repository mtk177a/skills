# Glossary

This guide is for maintainers and the agents working for them.\
It records which terms this repository uses for its own concepts, and which referents must not share one word.\
Use it when you write about these concepts in documentation or Skill bodies, or when you translate them into Japanese.

This is not a fixed translation table.\
Use the same term when the text points to the same thing, and choose the term from what the text points to, not from the English word alone.\
A word listed here can still carry its ordinary meaning in other contexts.

## Repository concepts

### Plugin ZIP

- **English**: plugin ZIP
- **Japanese**: Plugin の ZIP
- **Refers to**: the ZIP file that `scripts/build_plugin.py` builds, containing `plugin.json` and `skills/`.

Write “plugin ZIP” rather than “archive” or “package”, so that readers can tell the file apart from the plugin it contains.

### Plugin

- **English**: plugin
- **Japanese**: Plugin
- **Refers to**: the Agent Plugin that a client enables, regardless of the file it arrives in.

### All public Skills

- **English**: all public Skills
- **Japanese**: 公開 Skill 全体
- **Refers to**: every Skill under `skills/`, which APM can install with one command.

Use “bundle” only for APM's `SKILL_BUNDLE` format.

### Bundled resources

- **English**: bundled resources
- **Japanese**: 同梱資料
- **Refers to**: the files in a Skill's directory other than `SKILL.md`, such as `references/`, `scripts/`, and `assets/`.

### Install

- **English**: install
- **Japanese**: インストール
- **Refers to**: making Skills usable in a client, whether through APM, by uploading the plugin ZIP, or by extracting it.

Keep command names such as `apm install` as they are.\
“Extract” (展開) names the specific action of unpacking the ZIP.\
In Japanese, keep 導入 for its ordinary meaning of introducing something, such as a new term or feature, rather than for installing Skills.

### Publish and distribute

- **English**: publish
- **Japanese**: 公開
- **Refers to**: making Skills available to people other than the maintainer.\
  The Skills are currently published through this public GitHub repository.\
  Publishing the plugin ZIP requires approval.

Use “distribute” (配布) only for passing on third-party material, as in a license's redistribution terms.\
The plugin ZIP is built locally and handed to no one, so calling it “distributed” misstates what happens.

### Build

- **English**: build
- **Japanese**: 作る
- **Refers to**: producing the plugin ZIP with the build script.

Use 生成 when describing what the script itself does.

### Maintainer

- **English**: maintainer
- **Japanese**: 保守者
- **Refers to**: the person who maintains this repository, together with the agents working for that person.

### People who use the Skills

- **English**: people who use the Skills
- **Japanese**: 利用者
- **Refers to**: anyone who installs and uses the Skills, including the maintainer.

In repository documentation, do not write “user” (ユーザー) for this person.\
Agents and people both read these documents, and “user” points to different people depending on who reads it.

### User in Skill bodies

- **English**: user
- **Japanese**: ユーザー
- **Refers to**: the person directing the agent in the current session.

Inside a Skill body, the reader is always the agent, so “user” has only this meaning.

### Client and ChatGPT surfaces

- **English**: client
- **Japanese**: クライアント
- **Refers to**: the software in which an agent runs Skills, such as Codex, Claude Code, Cursor, and ChatGPT.

Chat, Work, and dots are separate surfaces within ChatGPT.\
Refer to them by name, such as “ChatGPT's Chat, Work, and dots”, instead of with a general term.

### Consumer repository

- **English**: consumer repository
- **Japanese**: 利用側のリポジトリ
- **Refers to**: a repository or directory that installs the Skills through APM and owns its own `apm.yml` and lockfile.

### English source

- **English**: English source
- **Japanese**: 英語版
- **Refers to**: the English file that defines requirements, from which a Japanese reference translation is made.

Avoid 原本 and 正本 for this file.\
They suggest a legal or archival original, while the actual relationship is that of a translation and its source.

### Upstream

- **English**: upstream
- **Japanese**: 上流
- **Refers to**: the external Gist from which an upstream mirror is copied.

### Guide

- **English**: guide
- **Japanese**: ガイド
- **Refers to**: a document under `docs/` written for a stated reader.

## Words that can point to different things

### Evidence and reason

These two are easy to mix up in Japanese, because 根拠 can mean either.

- Material that supports or refutes a claim, such as observations, logs, test results, and documents: evidence, 証拠.
- The reason a decision or conclusion was reached: reason or basis, 理由 or 根拠.

Both 証拠で裏付けられている and 根拠がある can be natural.\
Choose the wording so that material does not read as a rationale, and a rationale does not read as observed material.

### Authority and permission

- The power of a person or party to decide or to allow an action: authority, 権限.\
  Example: 設計する権限, 実行の権限.
- Technical access granted by a client or system setting, such as tool access, sandbox settings, or write access: permission, アクセス権 or 許可設定.\
  Example: 書き込みのアクセス権.

Translating both as 権限 hides whether a person's decision or a system setting is missing.

### Authorized and approved

- A specific action or scope that a person with authority has allowed: authorized, 許可された.
- A responsible party's explicit acceptance of a proposal or result, including GitHub's `Approve`: approved, 承認された.

Do not translate “authorized” as 承認済み.\
承認 suggests a formal acceptance event that may not have happened.

### Check and verification

- A single test, command, or inspection that was run: check, 確認.\
  Keep the name of a specific check, such as `check_repository.py`, as it is.
- Establishing with evidence whether a result meets what was expected, such as deciding whether a fix resolves its original finding: verify, validate, or verification, 検証.

In ordinary prose that does not need this distinction, 確認 is fine.

## Add or change an entry

Add an entry only for one of these:

- a concept specific to this repository
- a word that currently points to two things that need to be distinguished

Do not add general words just because their wording varies, as long as their meanings do not mix.\
For each entry, write what it refers to and why the distinction matters.\
Update the English source and its Japanese reference translation together.
