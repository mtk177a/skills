# draft-issue evals

Evaluates `draft-issue` in standalone operation. Checks whether it can turn a problem description into a well-structured GitHub issue — without fabricating information or including personal data.

## Iter 0

- `description` and body are aligned on "GitHub issue drafting"
- Output includes: Title, Background, Expected / Actual, Steps to reproduce (for bugs), Purpose (for features)
- No personal information (names, emails, internal URLs) in the output
- Vague input triggers clarifying questions rather than fabricated details

## Open items

- Balance between asking for more info vs producing a usable draft has not been tested
