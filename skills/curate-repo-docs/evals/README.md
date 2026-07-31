# curate-repo-docs evals

## Purpose

Verify that `curate-repo-docs` decides whether repository documentation needs to change, admits only reader-relevant Verified or Normative claims, uses the appropriate source of truth, makes the smallest authorized edit, validates the affected claims, and reports unknowns without turning investigation context into published prose.

## Assets

- `triggers.json`: trigger, non-trigger, near-miss, and coexistence cases
- `evals.json`: realistic repository tasks, synthetic fixtures, and hidden assertion assignments
- `results.json`: compact no-Skill/candidate evidence for the accepted revision after execution
- this README: static contract, coverage, protocols, and summarized results

## Static check

- The `description` covers README files, repository docs, current architecture and behavior, procedures, runbooks, references, and explicit decisions.
- General prose polishing, articles, cold revision, diff-only review, documentation-system governance, and inferred rationale are excluded.
- The body requires a documentation-impact decision before drafting.
- Verified, Normative, Inferred, and Unknown information remain distinct.
- A claim must be reader-necessary and Verified or Normative before publication.
- `No documentation impact` and `Blocked by unknowns` are valid non-editing outcomes.
- Investigation narrative, generic filler, duplicated sources, template-only sections, and unrelated rewrites are excluded.
- Edit authority, validation evidence, and unperformed checks remain explicit.
- The Skill does not depend on another Skill, script, client-specific metadata, network access, or an external service.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Documentation-impact decision | Edits documentation for an internal refactor or silently skips a material change | `internal-refactor-no-impact`, `focused-command-update` | Diff and response |
| Evidence classification | Publishes inferred rationale or treats current behavior as normative | `unknown-design-rationale`, `current-behavior-specification` | Claim provenance |
| Reader-task completeness | Removes prerequisites, success criteria, or material uncertainty in pursuit of brevity | all behavior cases | Assigned requirements |
| Canonical source placement | Hand-edits generated reference output or duplicates schema facts | `generated-configuration-reference` | Command trace and diff |
| Minimal authorized edit | Rewrites unrelated sections or adds generic documentation structure | `focused-command-update` | Changed paths and line-level diff |
| Authority boundary | Invents rollback, escalation, ownership, policy, or design reasons | `unknown-design-rationale`, `incomplete-runbook-authority` | Exact-claim inspection |
| Validation integrity | Claims a command, generator, or check ran when it did not | `focused-command-update`, `generated-configuration-reference` | Command trace and response |
| Trigger and coexistence | Loads for article writing, cold revision, diff review, research, design, or system audit | `triggers.json` | Observable Skill load |
| Incremental value | Adds no material safety or scope improvement over ordinary model behavior | matched no-Skill and candidate cases | Case-by-requirement comparison |

## Behavioral execution protocol

1. Use no target Skill as the baseline and the working-tree Skill as the candidate.
2. Run every condition in a separate disposable Git repository under `/tmp`.
3. Give the blank-slate executor only the selected Skill, visible fixture files, and user prompt. Keep assertion text and expected conclusions hidden.
4. Use the same Codex client, model, reasoning, sandbox, prompt, and initial fixture commit for baseline and candidate.
5. Let the executor write only inside the disposable repository. Capture its response, command trace, final diff, and repository status.
6. Grade deterministic requirements from the diff and trace. Use a separate grader for claim provenance, reader need, and unsupported content.
7. A failed critical assertion fails the case. A partial result without a critical failure is partial.
8. Run candidate and baseline once. Repeat matched conditions only when an unexpected result, instability, fixture defect, or grader defect could change the decision.
9. Keep prompts, responses, JSONL, grader output, temporary runner code, and disposable repositories outside this source repository.

## Trigger execution protocol

Present each case as a Skill-selection task using only the installed names and descriptions declared for that condition.
Require the selector to open every selected `SKILL.md`, and count only an observed file read.
Record an unavailable observation as `not exposed`.

## Acceptance rule

- Every candidate critical assertion and trigger case passes.
- The candidate does not omit reader information required for correctness or safe task completion.
- The candidate creates no unauthorized edit, unsupported factual claim, or duplicate source of truth.
- The candidate strictly improves at least one material failure over the no-Skill baseline without a critical regression.

If the absolute requirements pass but no material baseline improvement is observed, treat the Skill's incremental value as unverified rather than publishing an improvement claim.

## Failure Pattern Ledger

- `drafting begins before documentation impact is decided`
- `investigation narrative leaks into reader documentation`
- `implementation accident becomes stated design rationale`
- `current behavior is presented as a normative requirement`
- `generated output is hand-edited`
- `missing rollback or ownership is fabricated`
- `template sections are added without a reader need`
- `unrelated prose is rewritten while here`
- `shortness removes a prerequisite, condition, or success criterion`
- `an unexecuted check is reported as passing`

## Current revision

Evaluated on 2026-07-31 with Codex CLI 0.146.0, `gpt-5.6-sol`, high reasoning, workspace-write access limited to disposable synthetic repositories, and a read-only grader.

- The candidate passed all 38 assigned requirements and all six behavior cases. The no-Skill baseline passed 29 requirements, was partial on five, failed four, and completed three of six cases without a partial or failing result.
- The candidate materially improved the current-behavior, generated-reference, unknown-rationale, and incomplete-runbook cases. In the runbook case, it left the document unchanged and reported the missing operational decisions; the no-Skill baseline expanded the short source into an unsupported 127-line runbook.
- A full rerun exposed two cases where the candidate reported a validation observation more strongly than its command trace supported. After strengthening the trace-reconciliation rule, a targeted rerun of that candidate case passed all assigned assertions.
- All 15 trigger, non-trigger, near-miss, and coexistence cases passed in the final full routing rerun. The target Skill was not selected in any excluded case.
- The initial sandboxed runner attempt stopped before executor work because the Codex app-server could not initialize on a read-only filesystem. The accepted run used the same `/tmp`-only fixtures outside that outer sandbox.
- Raw prompts, responses, JSONL, grader output, command traces, and disposable repositories remained under `/tmp`.
- Claude Code, GitHub Copilot, Gemini CLI, other models, repeated-run stability, live repositories, external documentation systems, and periodic freshness audits were not executed.

See `results.json` for the compact case matrix, environment, hashes, and evaluation correction record.
