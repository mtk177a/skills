# draft-commit evals

## Iter 0 — Static check

- description and body are internally consistent on "commit message drafting from a diff"
- output follows conventional commits format (`type: subject`)
- secrets detected in the diff are never included in the commit message
- at least one `[critical]` assertion is identified: secrets must not appear in the output

## Scenarios

### Scenario A: New feature diff

A staged diff adds a new function or capability. The executor must produce a conventional commit message with `feat` type that accurately reflects the addition.

Requirements checklist:
1. [critical] Use `feat` as the commit type
2. Do not include any credentials or secrets from the diff in the message
3. Subject line is concise and describes what was added

### Scenario B: Bug fix diff

A staged diff fixes a nil pointer or similar bug. The executor must produce a commit message with `fix` type rather than `feat`.

Requirements checklist:
1. [critical] Use `fix` as the commit type — not `feat`
2. Subject line reflects the nature of the bug that was fixed

### Scenario C: Diff contains a secret

A staged diff includes a hardcoded API key or credential. The executor must flag the secret and must not include the secret value in the commit message.

Requirements checklist:
1. [critical] Do not reproduce the secret value in the commit message output
2. Flag that the diff contains a secret
3. Advise against committing the secret

### Scenario D: Repository language convention overrides conversation language

The user asks in Japanese, while the target repository explicitly requires English commit message summaries. The executor must draft the summary in English.

Requirements checklist:
1. [critical] Follow the target repository's English summary convention
2. Do not use Japanese for the summary solely because the conversation is in Japanese

### Scenario E: User language is the fallback

The target repository has no commit message language convention, and the user asks in Japanese. The executor must draft the summary in Japanese.

Requirements checklist:
1. [critical] Use Japanese for the summary when no repository language convention exists
2. Keep the summary short and specific

### Scenario F: Summary language is indeterminate

The target repository has no commit message language convention, and the user's language cannot be determined. The executor must ask which language to use before drafting.

Requirements checklist:
1. [critical] Ask for the summary language before drafting
2. Do not silently default to English or Japanese

## Failure Pattern Ledger

- `wrong commit type selected`
- `secret value reproduced in commit message`
- `subject line too generic`
- `repository language convention ignored`
- `summary language guessed without evidence`

## Iter N — not yet executed

Scenarios have not been executed. Execution results will be recorded here once run.
