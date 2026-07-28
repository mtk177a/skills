---
name: draft-commit
description: Drafts atomic commit plans and Conventional Commits messages from an explicitly scoped Git change set while preserving staged, unstaged, and untracked boundaries. Use for commit-message drafting, commit splitting, or preflight within an explicitly authorized commit workflow; not for PR summaries, diff review, implementation, or treating Skill invocation alone as permission to stage or commit.
license: MIT
---

# Draft Commit

## Objective

- Turn an explicitly scoped Git change set into one or more coherent commit plans and complete Conventional Commits messages.
- Preserve the repository's existing index and distinguish staged, unstaged, untracked, and supplied-only changes.
- Return a read-only handoff that can support a separately authorized commit workflow without treating Skill invocation as mutation authority.

## Scope and evidence

Establish the effective change set before drafting:

1. Use an explicitly supplied diff, path set, commit range, or staged-only scope when present.
2. Use the scope inherited from an originating workflow when it is explicit.
3. For an unspecified local "current changes" request, inspect staged, unstaged, and relevant untracked changes and state what is included.
4. Ask only when multiple plausible scopes would materially change a commit. If the change set cannot be obtained, report that drafting did not run.

Read the target repository's explicit type, scope, message, and summary-language convention first. Gather the stated change purpose and any available issue, design, implementation handoff, tests, or surrounding evidence that explains why the change exists. Treat the diff as evidence of what changed, not sufficient proof of why it changed.

Classify each relevant change as `Staged`, `Unstaged`, `Untracked`, `Partially staged`, or `Provided diff only`. A supplied diff without repository state can support message drafting but cannot prove the current index or justify executable staging commands.

## Workflow

1. State the effective change set, repository convention, available intent evidence, and material exclusions.
2. Start with status and diff statistics when repository state is available, then inspect enough staged, unstaged, and untracked content to understand every proposed commit. Progressive inspection may save context, but do not leave an included path or hunk unexamined when its purpose or grouping remains uncertain.
3. Build a change inventory. Assign every in-scope path or hunk exactly once to a proposed commit as `Included`, leave it out explicitly as `Excluded`, or mark it `Unresolved`. Do not silently omit or duplicate a change.
4. If a diff contains a suspected secret or credential, do not reproduce its value or continue with a normal commit plan for that material. Identify only the minimum path and category needed, exclude the material, and state the required remediation or uncertainty. Do not assume that a value is a harmless placeholder without evidence.
5. Group changes by one coherent purpose, required dependency, and reviewable behavior. Split a file by hunk when its changes belong to different concerns. Preserve rename and deletion pairs and state any required commit order. Use as many commits as the material requires; do not merge or omit concerns to satisfy a numeric limit.
6. Select each commit type from the repository convention, confirmed change intent, observable semantic effect, and compatibility impact. If missing intent could materially change the type, ask or mark the decision `Unresolved` instead of guessing from syntax alone.
7. Draft the complete message. Use the target repository's required summary language; otherwise use the user's language. If neither is available, ask or leave the language unresolved. Include an optional scope only when supported by repository convention or clearly useful under that convention. Add a body or footer when context, references, or release automation need them. Mark every breaking change with `!` or a `BREAKING CHANGE:` footer. Read `references/commit-types.md` when type, breaking-change, body, or footer selection is non-obvious.
8. Produce a staging plan that preserves existing staged content and excluded worktree changes. Treat a partially staged file as a hunk-level operation rather than replacing the index with the full working-tree file.
9. Provide candidate commands only when repository state was inspected and the commands can represent the plan without ambiguity. Omit commands and explain why when safe, portable representation is not possible.
10. Verify that every in-scope change is accounted for once, every commit has one primary purpose, messages match confirmed intent and local rules, excluded material remains excluded, and the Skill has not changed repository state.

## Safe command rules

- If the intended content is already staged, do not add a redundant `git add`.
- Use file-level `git add` only when the whole current file belongs in that commit and doing so cannot include an excluded or unstaged concern.
- Use `git add -p -- <path>` or an equivalent interactive instruction for hunk-level staging. Do not describe an interactive command as an exact run-as-is selection.
- Put `--` before pathspecs and quote paths for the identified shell. If a path or message cannot be represented safely and portably, provide the semantic plan without a shell command.
- Keep multiline messages, bodies, and footers in a message block unless a safe command representation is established. Do not force them into a fragile one-line `git commit -m` command.
- Do not emit staging or commit commands for `Provided diff only` input because the current repository state is unverified.

## Reporting contract

Adapt the presentation to the task and omit empty sections. Preserve these semantics:

- effective change set, relevant repository rules, and intent evidence
- for each proposed commit: primary purpose, complete message, included paths or hunks with current state, dependency order, and staging plan
- candidate commands only when they satisfy the safe command rules
- excluded and unresolved changes
- suspected secret handling, other stop reasons, and unconfirmed items
- repository mutations not performed and the next handoff

For a blocked draft, identify the missing change set, material intent, repository rule, or safe staging decision and leave the affected scope unresolved. Do not present the result as a complete plan.

## Authority and workflow boundaries

- Loading or explicitly invoking this Skill does not authorize `git add`, `git commit`, `git push`, index mutation, implementation, or any other repository write.
- When the originating request already explicitly authorizes a commit, return the draft and staging handoff to that workflow; do not invent another universal approval gate or prevent the authorized caller from continuing.
- Do not replace `summarize-changes`, `review-changes`, or an implementation workflow. This Skill drafts commit units and messages; it does not write PR descriptions, discover review findings, or change files.
- Do not expose secrets or credentials in messages, commands, or explanations.
- Do not alter, discard, or silently absorb unrelated user changes.
