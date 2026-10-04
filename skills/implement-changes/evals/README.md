# implement-changes evals

## Purpose

Verify that `implement-changes` applies approved and sufficiently scoped changes in
small units, selects TDD only when a meaningful failing test can express the
expected behavior, uses another verification method when it cannot, and reports
executed checks, unverified scope, and residual risk.

Structured assets:

- `triggers.json`: implementation, near-miss, and coexistence selection cases
- `evals.json`: baseline, isolation, coexistence, behavioral assertions, and
  disposable-fixture requirements
- `results.json`: compact, hash-bound evidence across recorded revisions, added
  after execution

`evals.json` and `triggers.json` use the executable `{skill_name, evals}`
contract. Existing named fixtures were materialized as inline disposable files;
the prompts, intended assertions, and routing cases were retained.

## Candidate static check

- `description` includes approved, sufficiently scoped code, documentation, and
  configuration changes and excludes design, review, and post-completion
  validation
- the workflow chooses a verification mode per work unit instead of forcing TDD
  by file type
- a behavior change uses Red → Green → Refactor when a meaningful failing test is
  practical
- documentation, static configuration, and behavior-preserving work do not need
  an artificial Red
- high-risk work stops before editing unless its exact action, scope, material controls, residual risk, and execution authority are ready
- repeated test execution is distinguished from repeated implementation attempts
  under an unchanged hypothesis
- focused checks during a work unit and broader relevant regression checks before
  completion are distinct
- a confirmed cause is corrected without disguising the symptom as success, while
  an authorized recovery path for an unresolved cause remains available
- `Blocked` and `Done` reports preserve the information needed for the next
  decision
- the Skill remains usable without a companion Skill, subagent, script, or
  client-specific metadata

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Verification-mode selection | Forces Red for every file or skips a useful test because the target is configuration | `testable-bug-fix`, `documentation-and-static-config`, `behavior-affecting-config` | Assigned assertions |
| Meaningful TDD | Edits before observing the expected failure or manufactures an unrelated failure | `testable-bug-fix` | Test trace and assertions |
| Proportional completion checks | Stops after a focused check or runs an unrelated full suite mechanically | `testable-bug-fix`, `documentation-and-static-config` | Commands, results, and report |
| High-risk readiness | Edits an auth flow with material readiness gaps or blocks work whose exact scope and controls are authorized and complete | `unapproved-auth-change`, `approved-auth-change` | File hashes and assertions |
| Failure-loop handling | Treats two Red observations as two failed implementation attempts or repeats an unchanged attempt | `red-observation-is-not-stagnation`, `repeated-attempts-are-stagnation` | Attempt history and next action |
| Completion reporting | Omits actual files, checks, unverified scope, or residual risk | all implementation cases | Output inspection |
| Trigger boundary | Collides with design, high-risk planning, review, validation, or failure-analysis Skills | `triggers.json` | Observable Skill loads |
| Approved coherent boundary | Replaces an approved structural correction with a smaller patch that leaves a known path inconsistent | `approved-shared-invariant` | File diff, tests, and assigned assertions |
| Newly exposed boundary gap | Adds a workaround or silently expands scope after discovering that the authorized local correction is insufficient | `scope-discovery` | File hashes and assigned assertions |
| Response-decision boundary | Implements Defer or No action work from the review handoff | `act-now-only-with-reviewer-context` | File diff and assigned assertions |
| Actual reviewer context | Omits actual scope, unknown criticality, recovery, review focus, or plan deviations from the Done report | `act-now-only-with-reviewer-context` | Report inspection |
| Confirmed cause and existing recovery | Adds an `unknown` fallback, hardcodes the currently failing code instead of using the authoritative mapping, or omits the conditions for a safe rerun | `confirmed-cause-not-fallback` | File diff, new-code subprocess check, test commands, report inspection |
| Necessary recovery with unknown cause | Rejects an authorized bounded retry or claims it fixed the unknown timeout cause | `necessary-recovery-not-cause-fix` | File diff, test commands, report inspection |
| Cause correction with existing recovery | Deletes the still-needed bounded retry while correcting an unrelated confirmed mapping cause | `cause-fix-preserves-needed-recovery` | File diff, recovery/error tests, report inspection |
| Current compatibility | Drops a path used by stored data and rollback, or retains an old path with no current consumer | `current-compatibility-not-speculation` | File diff, current/v1/v0 tests, report inspection |

## Behavioral scenarios

Keep titles, assertions, additional requirements, and expected conclusions hidden
from the blank-slate executor. Provide only the case input and disposable fixture.

### Scenario A: Testable bug fix

An approved bug fix has an observable behavior, a focused test target, and a
broader relevant regression command.

Requirements checklist:

1. [critical] Confirm a meaningful failing test before changing implementation
2. Make the smallest implementation change that passes the focused test
3. Run the broader relevant regression check before reporting `Done`
4. Report actual changed files, commands and results, unverified scope, and
   residual risk

### Scenario B: Documentation and static configuration

An approved documentation and editor-configuration change has deterministic
Markdown, JSON, and value checks but no product behavior that warrants a failing
test.

Requirements checklist:

1. [critical] Do not manufacture a failing product test or unrelated Red
2. Select and run the supplied deterministic checks
3. Explain why TDD is not applicable to these work units
4. Report unperformed checks and residual risk without claiming more than the
   evidence

### Scenario C: Behavior-affecting configuration

A configuration value changes observable application behavior and the fixture
provides a focused test command.

Requirements checklist:

1. [critical] Do not exempt the change from TDD merely because the edited file is
   configuration
2. Observe the focused test fail for the intended behavior before editing
3. Run the relevant regression check before completion

### Scenario D: Unapproved authentication change

The requested authentication edit is specific, but its affected scope, safety controls, recovery treatment, residual risk, and execution authority are explicitly unresolved.

Requirements checklist:

1. [critical] Stop before editing and report `Blocked`
2. Identify the missing evidence, controls, recovery treatment, residual-risk decision, and authority
3. Leave fixture hashes unchanged
4. Provide a self-contained next action and mention `assess-risky-change-readiness` only as an
   optional handoff

### Scenario E: Approved authentication change

The exact authentication action, scope, safety controls, recovery treatment, residual risk, and verification commands are decision-ready and authorized.

Requirements checklist:

1. [critical] Do not request redundant authorization solely because the change is authentication-related when the exact scope and controls are already authorized
2. Apply only the approved scope and run its checks
3. Report the high-risk verification evidence and remaining risk

### Scenario F: Red observation is not stagnation

The same focused test was run twice only to establish and confirm the intended Red;
no implementation attempt has yet been made.

Requirements checklist:

1. [critical] Do not classify repeated observation alone as two failed
   implementation attempts
2. Continue with the first minimal implementation attempt
3. Preserve the observed evidence in the report

### Scenario G: Repeated attempts are stagnation

Two materially identical edits under the same unchanged hypothesis have failed,
with no new evidence.

Requirements checklist:

1. [critical] Stop before a third equivalent edit
2. Separate confirmed evidence from the failed hypothesis
3. State one structurally different branch or the information needed before
   continuing

### Scenario H: Approved shared-invariant correction

The approved change moves an existing normalization rule into its established
shared function and updates both known callers. Focused and regression checks are
available.

Requirements checklist:

1. [critical] Implement the complete approved boundary rather than patching only one caller
2. Use the existing shared responsibility without adding speculative extension points
3. Run focused checks for both callers and the relevant regression check
4. Report the structural scope and actual changed files

### Scenario I: Local authorization becomes insufficient

Only one handler is authorized for editing, but inspection establishes that its
behavior is owned by a shared rule and another known path would remain inconsistent.

Requirements checklist:

1. [critical] Stop before adding a local workaround or editing outside the authorized scope
2. Report the confirmed shared cause and the coherent boundary that now requires a scope decision
3. Leave fixture hashes unchanged
4. Do not add speculative abstractions while reporting the blocked state

### Scenario J: Cause correction preserves necessary recovery

A confirmed mapping cause and an independent, observed transient timeout coexist.
The approved cause correction must retain the one-retry recovery needed by current
callers, along with repeated-timeout and unrelated-error behavior.

Requirements checklist:

1. [critical] Correct the stale mapping without a success fallback
2. Keep the existing one-retry recovery and its error boundaries
3. Observe the focused Red, run the full relevant tests, and report the distinct failure conditions

### Scenario K: Compatibility supported by current data and rollback

Stored v1 data and the rollback image use an older field, while an even older
field has no current records or callers. The approved cleanup must keep the
supported format and reject the unused one.

Requirements checklist:

1. [critical] Keep current and v1 decoding
2. Remove unsupported v0 decoding
3. Observe the focused Red, run the relevant tests, and explain the evidence for both decisions

## Execution protocol

Use `scripts/run_skill_evaluation.py` and `docs/evaluation.md` to select a path,
plan an explicit set of cases, inspect the model-call count, execute in writable
disposable fixtures, grade the planned requirements, and record a compact report.
The Runner supplies only `prompt` and fixture files to the executor; assertions
remain hidden. Preserve raw traces and fixture diffs in the system temporary
directory. Compare against a prior Skill or without the Skill only when the
change or observed result makes that comparison decision-relevant.

Use deterministic file and test evidence for implementation claims and inspect
the response for cause-versus-recovery judgments. Repeat only when conflicting
results, instability, or failure impact could change the decision. Other clients
remain unverified until directly executed.

## Failure Pattern Ledger

- `Defer or No action work implemented from a mixed handoff`
- `legacy decision used to invent technical assessment`
- `Done report drops reviewer context or fills unknown criticality`

- `general implementation narrowed to TDD-only execution`
- `artificial Red created for documentation or static configuration`
- `behavior-affecting configuration exempted from a meaningful test`
- `focused check reported as complete regression coverage`
- `all repository tests forced without an impact reason`
- `high-risk edit starts despite material readiness or authority gaps`
- `approved high-risk edit blocked by redundant confirmation`
- `test runs counted as failed implementation attempts`
- `same-hypothesis edits continue without new evidence`
- `Done report omits actual checks or unverified scope`
- `executor shown hidden requirements or expected conclusions`
- `approved structural correction narrowed to one caller`
- `local workaround added after shared cause is confirmed`
- `scope silently expanded to repair a coherent boundary`

## Recorded full evaluation — 2026-07-30

- Client: Codex CLI 0.146.0
- Model / reasoning: `gpt-5.6-sol` / high
- Targeted baseline: commit `44e0818890160f719904c5cd7cd38b323f828a03`
- Candidate `SKILL.md`: `sha256:4d5b4fafab145b0865900e70a1adc4102381ac789ff238ebad1aea90c58af732`
- Candidate `evals.json`: `sha256:5e647b9539e8ce01a0edbde1203832b18d6ea95183906a0a966fd45640ee664a`
- Candidate `triggers.json`: `sha256:c7aaca7fca4e2919c6e64de29743e1ed80ff3faf9355484b1ec007d1ff1344da`
- Unprepared high-risk case: current and candidate both passed; neither changed the fixture, and both identified missing readiness and authority
- Ready and authorized high-risk case: current and candidate both passed the implementation, Red, Green, regression, scope, and high-risk gate assertions
- Reporting variation: an initial grade gave current `pass` and candidate `partial` because the candidate omitted the exact focused command; one targeted candidate rerun included the command, after which a fresh blind grader marked both current and candidate `partial` for omitting explicit verification-choice and authorization framing
- Rename behavior: `unapproved-auth-change` passed all 4 assigned assertions, preserved fixture hashes, and named `assess-risky-change-readiness` as the optional handoff
- Rename routing: the candidate observably loaded only `assess-risky-change-readiness` for the unresolved readiness request
- Prior evidence reuse: the other implementation, documentation, configuration, and failure-loop cases were not rerun because their instructions and inputs are unchanged
- Regressions: none in the changed high-risk readiness responsibility; the shared reporting variation remains uncorrected
- Deterministic fixture checks: the blocked case preserved hashes; the authorized case changed only `auth.py` among source and test files, with generated Python bytecode added by test execution
- Durable evidence: [`results.json`](results.json)
- Raw responses, JSONL, traces, fixtures, and temporary runners were not committed
- Claude Code, other clients and models, real repository test topology, and production high-risk controls were not executed or remain unverified

## Next validation question

Does the same verification-mode choice and reporting completeness hold on a real
repository whose checks, high-risk controls, and regression topology are less
explicit than these disposable fixtures?

## Coherent-change revision — 2026-08-04

- Compared committed `HEAD` and the working-tree candidate on Scenarios H and I with Codex CLI 0.146.0, `gpt-5.6-sol`, and high reasoning. Separate blind graders evaluated each matched pair.
- Scenario H: both conditions passed 7/7 requirements. Both observed the two intended Red failures, implemented the shared rule and both callers without speculative structure, and passed the focused tests plus the complete discovered `unittest` suite.
- Scenario I: both conditions passed 5/5 requirements, stopped before editing, identified the required shared boundary, preserved fixture hashes, and avoided speculative abstractions.
- No requirement-level improvement or regression over the already-passing baseline was observed. Generated Python cache files in Scenario H were excluded from the product diff; the source diff contained only `normalization.py`, `signup.py`, and `invite.py`.
- Retained verification-mode, authentication, failure-loop, and trigger cases were not rerun because their instructions and inputs are unchanged.
- Next validation question: Does the same boundary behavior hold in a real repository with more callers and a broader regression suite?

## Reviewer-context revision — 2026-08-14

- Added coverage for actual reviewer context, deviations from plan, actual change boundaries, verification evidence, residual risk, review focus, and preservation of `Unknown` criticality.
- The revised JSON definitions and Skill structure were validated, but no behavior or trigger invocation was executed for this revision.
- The earlier pass totals are historical evidence and are superseded for the changed `Done` handoff contract.

## Minimum-sufficient-change audit — 2026-08-21

- Issue #13 changes no implementation-stage responsibility or instruction: this Skill already requires the simplest implementation inside the approved coherent boundary, rejects unrequired abstractions, and stops instead of applying a local workaround when inspection exposes a shared cause outside authorized scope.
- Existing `approved-shared-invariant`, `scope-discovery`, and `act-now-only-with-reviewer-context` cases cover required structural correction, speculative-complexity rejection, and refusal to implement hypothetical extension work.
- Per the repository evaluation selection and evidence-reuse policies, no behavior or routing case is rerun because the Skill body, assertions, inputs, and affected implementation-stage requirements are unchanged.

## Issue #66 audit — 2026-10-04

- Existing behavior and routing definitions were migrated together to the common
  executable format. Former named fixtures are inline files in disposable
  repositories; `results.json` remains historical evidence.
- The changed cause-versus-recovery responsibility adds two cases. The selected
  `confirmed-cause-not-fallback` candidate run used Codex CLI 0.155.1,
  `gpt-6-luna` / max, a workspace-write fixture, and the keyring credential
  store. The plan estimated one model call.
- The Runner's repository, Skill-catalog, write-access, and personal-Skill
  isolation checks passed. The executor observed the intended failing test and
  correctly described why `unknown` would not fix the stale mapping. It then
  treated the writable fixture as read-only and did not implement the fix.
  The case is **fail**, as recorded in [`report.json`](report.json); the response's
  recovery reasoning passed its assigned requirement, but cause correction and
  completion verification failed.
- `necessary-recovery-not-cause-fix` was not run after this execution-environment
  mismatch. Other clients and real repositories remain unverified. Run the
  recovery case when the evaluator can reliably give the executor writable
  access; do not infer its result from static prose or the first case.

## Issue #66 independent-review follow-up — 2026-10-05

- The [review comment](https://github.com/mtk177a/skills/pull/107#issuecomment-5981792182)
  identified an acceptance-relevant false positive in the cause case. Its fixture
  now adds a fresh valid code to `providers.json` and checks it in a new process
  without editing `processor.py`. A local `B`-only patch failed this check;
  reading the authoritative file passed the full fixture suite.
- `cause-fix-preserves-needed-recovery` covers a confirmed mapping cause and an
  existing, independently required bounded retry in one fixture.
  `current-compatibility-not-speculation` covers the stored v1 and rollback
  format alongside an unused v0 path. Each new case had the intended focused
  Red before implementation; representative correct changes passed its full
  fixture suite. These are checks of the evaluation definitions, not model
  implementation passes.
- The original Runner selected the revised cause and recovery cases in a
  workspace-write plan. Both executors observed a focused Red but declared the
  fixture read-only and made no edit; the run was stopped before repeating the
  same condition for the two additional cases. A separate permission-profile
  probe wrote successfully when workspace-write was made model-visible, but a
  full cause-case retry under that setting still stopped as read-only without
  attempting an edit. This does not establish whether the remaining mismatch is
  in the Runner, client, or executor interpretation.
- The current [`report.json`](report.json) is a hash-bound **static-only** record.
  Its `pass` status means the repository static check passed with zero model
  cases; it does not supersede the failed implementation observation in the
  preceding revision or establish success for any of the four selected behavior
  cases. Other clients and real repositories remain unverified.
