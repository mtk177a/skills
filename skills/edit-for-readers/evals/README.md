# edit-for-readers evals

## Purpose

Verify that `edit-for-readers` compresses an existing draft against an explicit
reader contract, preserves necessary meaning and uncertainty, identifies
missing context, and does not turn a reader-focused pass into first-draft
generation, factual verification, diff review, or an exhaustive edit log.

Structured assets:

- `triggers.json`: core, near-miss, and coexistence selection cases
- `evals.json`: no-Skill baseline and candidate behavior cases
- `results.json`: added only after executed evidence is accepted

## Iter 0 — Static check

- `description` includes over-written drafts, author-context bias, fresh-reader
  passes, and reader-centered revision and excludes first drafts, general diff
  review, factual verification, and language-specific style
- the body requires an existing artifact, reader contract, preservation
  constraints, and explicit edit authority
- deletion depends on the reading goal rather than length alone
- necessary facts, evidence, uncertainty, examples, and exceptions survive
- missing reader context is identified rather than hidden by compression
- independent reading is supplied by orchestration rather than started or
  awaited inside the Skill
- a supplied independent result is separated from the author's expected
  diagnosis or hidden grading criteria, and an absent result is not reported as
  fresh
- an explicitly required independent pass stops before assessment or revision
  when no provenance-bearing result was supplied
- review-only output contains actionable labels and omits exhaustive `KEEP`,
  reader-contract, and routine process-status reporting
- the Skill is portable and does not require a client-specific agent, model,
  script, reference, or companion Skill

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Reader-goal compression | Rephrases repetition without removing it | `overwritten-operations-guide` | Required meaning and repeated meaning comparison |
| Preservation | Deletes a compatibility condition or strengthens uncertainty | `overwritten-operations-guide` | Critical assertion rubric |
| Missing context | Only shortens and leaves an unusable prerequisite gap | `missing-prerequisite` | Required `MISSING` item |
| Review authority | Edits a file or returns a full rewrite when comments only were requested | `review-only-comments` | Output and repository-state inspection |
| Concise reporting | Enumerates every unchanged passage | `review-only-comments` | Output rubric |
| Independent context | Calls an unobserved pass fresh or silently falls back to the main context | `explicit-fresh-reader` | Result provenance, status, and stop behavior |
| Trigger boundary | Activates for first drafts, factual verification, or diff review | `triggers.json` | Observable Skill loads |
| Coexistence | Replaces Japanese prose rules or diff review | `triggers.json` | Observable selected handlers |

## Execution protocol

1. Use a no-Skill executor as the baseline and the working-tree Skill as the
   candidate.
2. Give both executors the same case input and fixture. Keep assertions,
   expected deletions, and grading notes hidden.
3. Use the same client, model, reasoning effort, sandbox, and grader for both
   conditions.
4. Start each executor without repository conversation history. For the
   independent-reader case, confirm that the Skill does not attempt delegation
   and does not claim execution without a supplied distinct-reader result.
5. Run each case once per condition. Repeat only when an unexpected result,
   instability, model difference, or failure consequence could change the
   decision.
6. Record unavailable orchestration evidence as `not exposed` and skipped
   client coverage as `not executed`; neither is a pass.
7. Keep raw responses, JSONL, grader output, and disposable artifacts outside
   this repository.

## Acceptance

- every assigned critical assertion passes for the candidate
- no candidate case strengthens uncertainty, loses a required condition, or
  invents a fact
- every trigger case selects the expected handler or handlers from observable
  Skill loads
- the candidate is no worse than the baseline on any assigned assertion and
  improves reader-goal compression, missing-context detection, or reporting
  concision in at least one case

## Current result

On 2026-07-30, Codex CLI 0.146.0 with `gpt-5.6-sol` and high reasoning
produced:

- baseline: 11/21 assertions and 1/4 cases passed
- candidate: 21/21 assertions and 4/4 cases passed
- trigger selection: 8/8 core, near-miss, and coexistence cases passed

The candidate removed repeated meaning while preserving material constraints,
kept review-only output action-focused, and identified only artifact-grounded
missing context. When no provenance-bearing independent result was supplied, it
returned the not-executed status and stopped without silently substituting a
main-session pass. The missing-context case passed two additional observations
after an earlier variable output exposed an adjacent-prerequisite failure.

Claude Code, GitHub Copilot, Gemini CLI, and a configured reader-agent
orchestration path were not executed. Detailed case and trigger evidence is in
`results.json`; raw traces are intentionally not retained.
