# Core Skill Workflows

A minimal reference for how the core Skills connect into common workflows.

## Basic workflow

`scope-request` → `design-changes` → `implement-changes` → `review-changes` → `validate-fix`

- `scope-request`: Clarify purpose, completion criteria, constraints, assumptions, and open questions
- `design-changes`: Define what changes, what is out of scope, risks, test strategy, and stop conditions
- `implement-changes`: Build incrementally with TDD, leave a clear handoff for verification
- `review-changes`: Review the diff and categorize findings as `must` / `should` / `suggestion` / `nit`
- `validate-fix`: Summarize what was verified, what was not, and what risks remain

## Review feedback workflow

`triage-review-feedback` → `implement-changes` → `validate-fix`

- `triage-review-feedback`: Sort existing review comments into accepted, deferred, and rejected; decide on approach
- `implement-changes`: Apply only the accepted changes
- `validate-fix`: Document verification results and remaining open items

## Stagnation recovery workflow

`break-failure-loop` → `diversify-agent-search` → `design-changes` → `implement-changes`

- `break-failure-loop`: Stop repeated same-hypothesis attempts and organize the evidence
- `diversify-agent-search`: When available, widen the search with candidate archives, diversity axes, and case-level evaluation
- `design-changes`: Turn the selected branch into an implementable plan
- `implement-changes`: Resume implementation only after the branch and stop conditions are clear

Each Skill should still work on its own. `diversify-agent-search` is a companion for deeper search design, not a required dependency for the other Skills.

## Stop conditions

Stop and request approval or clarification when:

- Editing docs, Skills, or AGENTS files
- Adding dependencies or making significant design changes
- Performing destructive or high-risk changes
- Specifications are unresolved and proceeding would require guessing
