# Example commits

This example shows a finished commit plan and its messages for a fictional change set.

- **Copy**: one purpose for each commit, the subject as a name for the change, the body order of the problem and then the solution with its reason, and footers only where the rules ask for them.
- **Do not copy**: the wording, the number of commits, or the length. Write each message from the changes in front of you.

## The change set

The working tree of a command-line tool has two unstaged changes. `retry.py` and `upload.py` add retries after temporary network errors, with tests in `test_retry.py`. `README.md` fixes a spelling error in an unrelated section. The repository uses Conventional Commits, and its rules set no line length for the body.

## Plan

| Commit | Purpose | Included changes |
| --- | --- | --- |
| 1 | Retry uploads after temporary errors | `retry.py`, `upload.py`, `test_retry.py` (unstaged) |
| 2 | Fix a spelling error in the README | `README.md` (unstaged) |

The two changes have different purposes, so they go in separate commits. The order does not matter, because neither commit depends on the other.

## Messages

Commit 1:

```text
fix(upload): retry requests after temporary network errors

upload stops at the first failed request, so a short network outage makes the user start a long upload again.

Retry a request after a timeout, a reset connection, or a 502, 503, or 504 response, up to three times with a longer wait each time. Other errors still stop the command at once, because a retry cannot fix them. A resumable upload would also avoid repeated work, but the server does not support it.

Closes #42
```

Commit 2:

```text
docs(readme): fix the spelling of "authentication"
```

Commit 2 has no body, because the subject already states what changes and why.
