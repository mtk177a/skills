---
name: scope-implementation
description: Before implementing, narrow the target files, off-limits scope, completion criteria, and verification commands.
license: Apache-2.0
---

# Scope Implementation

## Purpose

- Fix the implementation scope before starting to reduce exploration cost and rework.
- Break a broad request into small, reviewable units.

## When to use

- When a request is broad, like "do this whole Issue"
- When you want to separate files to read from files not to touch before implementing
- When you want to minimize the agent's exploration scope

## Input (optional)

- Request text
- Issue / PR / review comment
- Potentially related files and directories
- Candidate verification commands

## Steps

1. Compress the request into one Goal.
2. Explicitly state Non-goals for this session.
3. Narrow the files to read first.
4. Explicitly state the files that may be edited.
5. Explicitly state the files that must not be edited. In particular, exclude docs, configuration, dependencies, and generated files until they are actually needed.
6. Organize constraints, completion criteria, and verification commands.
7. If the verification command is unknown, stop and record it as unconfirmed rather than guessing.
8. Write in Stop conditions the conditions under which the scope would expand beyond the initial assumption.

## Output format

- Goal: ...
- Non-goals: ...
- Files to read:
  - ...
- Files that may be edited:
  - ...
- Files that must not be edited:
  - ...
- Constraints:
  - ...
- Completion criteria:
  - ...
- Verification commands:
  - ...
- Stop conditions:
  - ...

## Boundaries

### Always:

- State "files that must not be edited" explicitly
- State "stop conditions" explicitly
- Separate goal from non-goals
- Do not fill in unknown verification commands with guesses

### Ask first:

- When the edit scope expands beyond the initial assumption
- When dependency additions, configuration changes, or docs updates are needed
- When work equivalent to a separate Issue is mixed into the completion criteria

### Never:

- Start implementation ambiguously under the assumption of expanding "if needed"
- Start broad exploration with off-limits files undefined
