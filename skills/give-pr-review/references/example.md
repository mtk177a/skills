# Example review

This example shows a finished first review and a re-review reply for a fictional pull request.

- **Copy**: the first line of each comment, the reason and next step in the discussion, the placement of each comment at its cause, the summary structure, and the reply that starts with its result.
- **Do not copy**: the wording, the number of comments, or the length. Write each comment from the findings in front of you.

## The pull request

The pull request adds retries to the `upload` command of a command-line tool. It retries a request after a timeout, a reset connection, or any `5xx` response, up to three times.

## First review

### Inline comments

On `retry.py`, at the list of errors that count as temporary:

```markdown
issue (blocking): A `501` response is retried, but it never succeeds on a retry

`501 Not Implemented` means that the server does not support the request, so each retry repeats the same failure and adds 7 seconds before the error. Limit the retry to `502`, `503`, and `504`.
```

On `upload.py`, at the call to the retry function:

```markdown
question (non-blocking): Does the server accept the same file twice?

If a request reaches the server and only the response is lost, the retry uploads the file again. If the server rejects duplicates, the retry turns a success into an error. If the server accepts them, no change is needed.
```

On `test_retry.py`:

```markdown
praise: The tests cover each temporary error separately

A failure in one error type now points directly at its cause.
```

### Summary

```markdown
One comment blocks the merge: `501` responses are retried although a retry cannot fix them.

- **Scope**: Head `4f2a9c1`. I read `retry.py`, `upload.py`, and the tests, and ran `pytest`, which passed.
- **Blocking**: 1. `retry.py`: a `501` response is retried.
- **Non-blocking**: `question` 1.
- **Not checked**: The behavior of the real server for duplicate uploads.
- **Strengths**: Each temporary error has its own test.
```

## Re-review reply

In the thread of the blocking comment, after the author changed the list:

```markdown
Partially resolved. `501` is no longer retried in `retry.py` at `9b3e7d0`, and the new test passes. `505` is still in the list and has the same problem. Remove `505` as well, and I will resolve this thread.
```

The thread stays open, because the result is not `Resolved`.
