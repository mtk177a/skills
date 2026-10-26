---
name: review-changes
description: Reviews a code, documentation, or configuration diff for problems in correctness, safety, verification, compatibility, maintainability, and performance, and reports each finding with evidence, impact, and confidence. Use when the user asks to review a diff, or asks for a full re-review of a diff.
license: MIT
---

# Review Changes

Find the problems that a diff causes or exposes.\
Report each problem with the evidence that another person needs to evaluate it.

## Before you review

1. **Identify the diff**

   Use the first source that applies:

   - a diff, a commit range, or a PR range that the user supplied
   - in a PR, the base and head of the PR
   - for local changes, the staged, unstaged, and related untracked files

   Done when you can state exactly which changes you review.\
   If two possible scopes give different reviews, ask the user.\
   If you cannot get the diff, report that the review did not run, and name the missing input.

2. **Collect the reviewer context**

   Collect these items from the request, the PR, and the repository:

   - the objective and the expected result
   - the product or operational context, and its criticality
   - the scope and the exclusions
   - the affected users, data, and contracts, and who can see the change
   - the constraints and the accepted trade-offs
   - the verification and the unknowns
   - the detection and recovery controls
   - the parts that the user wants you to examine

   Done when each item has a value or is marked `Unknown`.\
   Missing criticality or exposure is `Unknown`, not low risk.

## Review

3. **Review the design**

   Start with the purpose, the design, the contracts, the responsibility boundaries, and the code that uses the changed code.\
   Then select the review areas in [Review areas](#review-areas) that apply to this change.\
   Done when you can state the risks of the change and the areas that you will review.

4. **Inspect the diff**

   Read the diff and the surrounding evidence that you need to test its assumptions.\
   This evidence can include specifications, tests, callers, schemas, and similar implementations.\
   Check claims in the request, the comments, and the specifications against the code and the checks.\
   Report problems that the change causes or that relate to the change.

5. **Run checks**

   Run safe, read-only checks when their result can confirm or reject a finding.\
   Keep the working tree, the dependencies, and external systems unchanged.\
   Record each check that you ran, with its command and result, separately from the checks that you suggest.

6. **Write the findings**

   Write each finding that the evidence supports and that matters for this change, with the fields in [Finding fields](#finding-fields).\
   State only the impact that the evidence supports.\
   If a possible consequence is useful but not verified, state it as a condition, and add it to `Unconfirmed premises`.\
   Done when each finding has a label, a confidence, and all applicable fields.

7. **For a full re-review, compare with the previous findings**

   Do this step only when the user asked for a full re-review.\
   Mark each previous finding as `Resolved` or `Remaining`, and mark each other finding as `New`.\
   Give each `New` finding one origin:

   - `Fix-induced`: the fix caused it.
   - `Newly observable`: the fix made it visible.
   - `Late-discovered`: it was visible before, and the previous review did not report it.

   Report a `Late-discovered` finding that does not block the change as a `note`, or leave it out.\
   This keeps it from starting another fix round.

8. **Report the review**

   Report these items:

   - the conclusion and the diff that you reviewed
   - the scope that you reviewed, and the material exclusions
   - the findings, ordered by label and impact
   - the checks that you ran, with the commands and the results
   - the suggested verification, the parts that you did not check, and the risks that remain

   If there are no material findings, say so, and report the same scope, checks, and risks.\
   If a specification question is open, review the rest of the diff, and report the question as a `question` finding.\
   If a review area is not complete, say that the review is not complete.\
   Leave the fixes and the decisions about the findings to the user.

## Review areas

Use only the areas that matter for the change.

**Code and behavior**

- correctness, edge cases, order, time, rounding, concurrency, error handling, and data integrity
- external contracts, such as APIs and schemas
- authorization, authentication, input validation, injection, exposure of secrets or personal data, and unsafe side effects
- backward compatibility, migrations, rollout, and consistency with callers and similar implementations
- fallbacks, retries, and paths that catch an error and continue: each one handles a current failure, and its result is observable
- compatibility paths: do current users, published behavior, stored data, migration, or rollback need them?
- test coverage and test quality, including tests that depend on the implementation or use too many mocks
- maintainability and performance, when the effect is concrete

**Structure**

Report a structural problem when the evidence shows a concrete result.\
Examples are duplicated rules, inconsistent behavior, unreachable branches, and more operational work.\
This applies to both directions:

- too much structure: an abstraction, extension point, configuration option, dependency, or layer that no current requirement needs
- too little structure: a local patch that leaves the confirmed cause, copies a shared rule, or differs from other known paths

When the evidence shows a shared responsibility or rule, accept the shared abstraction even if duplicated local code is shorter.

**Documentation**

- facts that agree with the implementation or the source
- commands, examples, links, identifiers, terms, and missing information
- render, lint, or content checks, when they are available

**Configuration**

- schema and parser validity, precedence, defaults, environment interaction, and compatibility
- values that change behavior, and the behavior checks that they need
- rollout, recovery, secret handling, and operational results

## Finding fields

Give each finding one label:

| Label | Meaning |
| --- | --- |
| `must` | Fix before merge. The evidence shows a material risk, and a smaller response is not sufficient. |
| `should` | Fix is recommended. An alternative or a constraint can change the decision. |
| `suggestion` | An improvement that does not block the change |
| `question` | The next action is to clarify or verify a premise. |
| `nit` | A small, optional correction |
| `note` | Information that needs no action |

Use `must` and `should` only for problems with evidence, not for preferences.\
A `question` keeps its potential impact, even when its premise is not confirmed.

Write these fields for each finding:

- `Confidence`: `high`, `medium`, or `low`
- `Finding`: the problem, proposal, question, or note
- `Evidence`: the locations, contracts, behavior, check output, or repository examples that support it
- `Impact`: the result that the evidence supports, or the result if an unconfirmed premise is true
- `Verification`: how to confirm, reproduce, or reject the finding
- `Unconfirmed premises`: the assumptions or unknowns that the finding, its impact, or its label depends on, or `none identified`

Add these fields when they can change the label:

- `Exposure and preconditions`: the conditions, paths, frequency, or affected people, or `Unknown`
- `Criticality and blast radius`: the importance of the affected part, and the extent of the harm
- `Detectability, recovery, and workaround`: how the problem is detected, contained, or recovered from
- `Remediation cost and trade-offs`: the cost of the fix in work, verification, complexity, regression risk, and delay

For a full re-review, add `Re-review state` and, for a `New` finding, `New finding origin`.\
Add `Generalizable check` only when the check is useful outside this diff.

Compare risks in order, such as higher or lower, with evidence.\
Select the smallest response that is sufficient for the risk that the evidence supports.
