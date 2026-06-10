# Core Skill Workflows

A minimal reference for how the core Skills connect into common workflows.

## Basic workflow

`scope-request` → `design-changes` → `implement-changes` → `review-changes` → `validate-fix`

- `scope-request`: Clarify purpose, completion criteria, constraints, assumptions, and open questions
- `design-changes`: Define what changes, what is out of scope, risks, test strategy, and stop conditions
- `implement-changes`: Build incrementally with TDD, leave a clear handoff for verification
- `review-changes`: Review the diff and categorize findings as Must-fix / Should-fix / Nice-to-have
- `validate-fix`: Summarize what was verified, what was not, and what risks remain

## Review feedback workflow

`triage-review-feedback` → `implement-changes` → `validate-fix`

- `triage-review-feedback`: Sort existing review comments into accepted, deferred, and rejected; decide on approach
- `implement-changes`: Apply only the accepted changes
- `validate-fix`: Document verification results and remaining open items

## Stop conditions

Stop and request approval or clarification when:

- Editing docs, Skills, or AGENTS files
- Adding dependencies or making significant design changes
- Performing destructive or high-risk changes
- Specifications are unresolved and proceeding would require guessing
