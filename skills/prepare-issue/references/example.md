# Example Issues

This file shows a finished title and body for two fictional Issues: an enhancement and a defect.

- **Copy**: the order of the sections, the labels, the Background items for each type of work, the separation of observations and speculation, and completion criteria that someone can observe.
- **Do not copy**: the wording, the number of items, or the length. Write each section from the request in front of you, and leave out what the rules let you leave out.

## Enhancement

### Request

Users of a command-line tool report that long uploads fail on unstable networks, because `upload` stops at the first failed request.

### Title

```text
Retry uploads after temporary network errors
```

### Body

```markdown
## Summary

`upload` should continue after a temporary network error, so that a short outage does not stop a long upload.

## Background

- **Current state**: `upload` stops at the first failed request, and the user must start the whole upload again.
- **Problem**: On unstable networks, uploads of several hundred files often fail before they finish. Three users reported this in the last month.

## Goal

A short network outage no longer stops an upload. This includes deciding which errors count as temporary, and keeping the current stop for the other errors.

## Requirements

- **Clear failures**: Authentication errors still stop the command at once, with the current message.

## Completion criteria

- [ ] An upload during a simulated outage of a few seconds finishes.
- [ ] An upload with wrong credentials stops at once, with the current message.

## Related

- #38: The same problem in `download`, which uses a different client.
```

## Defect

### Request

A user reports that `upload` printed `Done` although some files are missing on the server.

### Title

```text
upload reports success when the server storage is full
```

### Body

```markdown
## Summary

`upload` prints `Done` and exits with code 0 when the server rejects files because its storage is full, so users believe that the upload worked.

## Background

- **Steps to reproduce**

  1. Fill the storage of a test server.
  2. Run `upload ./photos`.

- **Expected behavior**

  - `upload` reports the rejected files and exits with a non-zero code.

- **Actual behavior**

  - `upload` prints `Done` and exits with code 0. The server log shows `507 Insufficient Storage` for each file.

- **Environment**

  - Version 2.3.1 on Linux. The user reported the same result on macOS.

- **Suspected cause**

  - Speculation: the client checks only for `4xx` responses, so it treats `507` as a success.

## Goal

`upload` reports every file that the server does not store, and the exit code shows the failure.

## Completion criteria

- [ ] With a full test server, `upload` lists the rejected files.
- [ ] With a full test server, `upload` exits with a non-zero code.
```
