# draft-commit evals

Evaluates `draft-commit` in standalone operation. Checks whether it can produce a conventional-commit-format message from a staged diff — and refuse to include secrets.

## Iter 0

- `description` and body are aligned on "commit message drafting from a diff"
- Output follows conventional commits (type: subject)
- Summary is in the author's working language (Japanese for this repo)
- Secrets are never included in the message

## Open items

- Language detection (Japanese vs English summary) has not been empirically tested
