---
name: draft-commit
description: Drafts commit plans and Conventional Commits messages for a scoped Git change set, and keeps the staged, unstaged, and untracked boundaries. Use when the user asks for commit messages, a split of changes into commits, or a check before an authorized commit.
license: MIT
---

# Draft Commit

Turn a scoped Git change set into coherent commit plans and complete Conventional Commits messages.\
Keep the current index, and distinguish staged, unstaged, untracked, and supplied-only changes.\
The output is a plan and messages.\
Staging, committing, and pushing belong to a separately authorized commit workflow.\
When the request already authorizes a commit, return the plan to that workflow so that it can continue.

## Workflow

1. **Identify the change set**

   Use the first source that applies:

   - a diff, a path set, a commit range, or a staged-only scope that the user supplied
   - an explicit scope from the originating workflow
   - for local changes, the staged, unstaged, and related untracked changes

   If two possible scopes give different commits, ask the user.\
   If you cannot get the change set, report that drafting did not run.\
   Done when you can state which changes the plan covers.

2. **Read the rules and the intent**

   Read the type, scope, message, and summary-language rules of the repository first.\
   Collect the stated purpose of the change, and the related Issue, design, handoff, tests, or other evidence.\
   The diff shows what changed.\
   The intent comes from the user and this evidence.

3. **Inspect the changes**

   Start with the status and the diff statistics when the repository is available.\
   Then read enough of each change to understand every proposed commit.\
   Read each included path or hunk whose purpose or group is not clear.\
   Classify each change as `Staged`, `Unstaged`, `Untracked`, `Partially staged`, or `Provided diff only`.

4. **Make the inventory**

   Assign each path or hunk in scope exactly once:

   - `Included`, in one proposed commit
   - `Excluded`, with the reason
   - `Unresolved`, with the open question

   Done when each change in scope has one entry.

5. **Handle suspected secrets**

   If a change contains a suspected secret or credential, exclude that material from the plan.\
   Report only the path and the category, and keep the value out of the output.\
   State the remediation or the uncertainty.\
   Treat a value as a harmless placeholder only when evidence shows it.

6. **Group the changes into commits**

   Make each commit one coherent purpose, with its required dependencies and a behavior that a person can review.\
   Split a file by hunk when its changes belong to different purposes.\
   Keep a rename and its deletion together, and state any required order of the commits.\
   Use as many commits as the changes need.

7. **Select the types**

   Select each type from the repository rules, the confirmed intent, the observable effect, and the compatibility impact.\
   If missing intent can change the type, ask the user, or mark the type `Unresolved`.\
   Read `references/commit-types.md` when the type, a breaking change, the body, or a footer is not obvious.

8. **Write the messages**

   Write each complete message:

   - Use the summary language of the repository, or else the language of the user.\
     If neither is known, ask the user or mark the language `Unresolved`.
   - Add a scope only when the repository rules support it, or when it is clearly useful under them.
   - Add a body or a footer when the context, references, or release automation need it.
   - Mark each breaking change with `!` or a `BREAKING CHANGE:` footer.

9. **Plan the staging**

   Plan the staging so that the existing staged content and the excluded changes stay as they are.\
   Stage a partially staged file by hunk, not as a full file from the working tree.\
   Give commands only when they follow [Command rules](#command-rules).\
   Otherwise, give the plan in words, and state why no command is given.

10. **Check the plan**

    Check these items:

    - Each change in scope appears once.
    - Each commit has one main purpose.
    - Each message matches the confirmed intent and the repository rules.
    - Excluded material stays excluded.
    - The repository state is unchanged.

## Command rules

- Give commands only when you inspected the repository state, and the commands show the plan exactly.\
  For `Provided diff only` input, give the plan without commands.
- When the content is already staged, leave it staged and give no `git add` for it.
- Use a file-level `git add` only when the whole file belongs to that commit.\
  Check that it adds no excluded or unstaged change to the commit.
- Use `git add -p -- <path>`, or an equivalent instruction, for staging by hunk.\
  Label it as interactive, because the user selects the hunks.
- Put `--` before paths, and quote paths for the identified shell.\
  If a path or a message cannot be written safely in a command, give the plan without the command.
- Put a message with several lines, a body, or footers in a separate message block.\
  Use `git commit -m` only for a message that it can show safely.

## Report

Include these items, and leave out empty sections:

- the change set, the repository rules, and the evidence of intent
- for each commit: its main purpose, its complete message, its included paths or hunks with their current state, its order, and its staging plan
- the commands, only when they follow the command rules
- the excluded and unresolved changes
- the handling of suspected secrets, other reasons to stop, and the items that are not confirmed
- the statement that the repository was not changed, and the next step

If the draft is blocked, name the missing change set, intent, repository rule, or staging decision.\
Mark the affected scope as `Unresolved`, and report the plan as incomplete.
