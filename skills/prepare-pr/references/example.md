# Example pull request

This example shows a finished title and description for a fictional change.

- **Copy**: the order of the sections, the labels, one item for each group of changes, the three groups of checks, and the level of detail in each item.
- **Do not copy**: the wording, the number of items, or the length. Write each section from the change in front of you, and leave out what the rules let you leave out.

## The change

A command-line tool has an `upload` command. The command stops at the first failed request, and users on unstable networks must start long uploads again. The change adds retries for temporary network errors, and keeps the stop for other errors. The `download` command has the same problem, but it uses a different client.

## Title

```text
fix(upload): retry requests after temporary network errors
```

## Description

```markdown
## Summary

`upload` now retries a request after a temporary network error, so a short outage no longer stops a long upload. Errors that a retry cannot fix still stop the command at once.

## Why

- **Current state**: `upload` stops at the first failed request, and the user must start the whole upload again.
- **Problem**: On unstable networks, uploads of several hundred files often fail before they finish.
- **Chosen approach**: Retry each failed request a few times, with a longer wait each time. A resumable upload protocol would also avoid repeated work, but the server does not support it.

## What changes

- **Retries for temporary errors**: A timeout, a reset connection, or a `503` response causes up to three retries, with waits of 1, 2, and 4 seconds.
- **Stop for other errors**: An authentication error or another `4xx` response stops the command at once, with the same message as before.
- **Not included**: Retries for `download`. It uses a different client and needs its own change.

## How to review

- **Reading order**: Start with `retry.py`, then read where `upload.py` calls it.
- **Focus**: The list of errors that count as temporary. A wrong entry can hide a real failure.

## Evidence

- **Automated checks**

  - **`pytest`**: Passed, with new tests for each temporary error and for an authentication error.

- **Manual checks**

  - **Upload during a simulated outage**: Before the change, the upload stopped at the first failure. After the change, it finished after two retries.

## Risk

- **Irreversible effects**: None.
- **Blast radius**: People who run `upload`. A failing upload now takes up to 7 seconds longer before it stops.

## Related

- Closes #42
```
