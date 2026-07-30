# revise-docs-fresh-eyes evals

## Purpose

Verify that `revise-docs-fresh-eyes` responds only to explicit fresh-context
revision requests, starts a distinct subagent without authoring turns, and has
that subagent complete the cold read and revision. The parent must not leak its
diagnosis, rewrite the child's prose, or fall back to same-context editing.

Structured assets:

- `triggers.json`: explicit triggers, near misses, and coexistence cases
- `evals.json`: author-context, authority, and fail-closed behavior cases
- `results.json`: added only after accepted Codex and Claude Code evidence exists

## Iter 0 — Static check

- `description` requires an explicit fresh-eyes request or direct invocation and
  excludes ordinary editing, first drafts, fact checking, and diff review
- a distinct subagent is a prerequisite rather than an optional enhancement
- Codex delegation excludes authoring turns and Claude Code uses a normal fresh
  `Agent` subagent
- the parent neither creates a reader contract nor pre-reviews the artifact
- the child payload contains only the target, user-derived request and
  constraints, output mode, and authority
- earlier author preferences, attachment, suspected defects, and desired
  conclusions never become child constraints unless the latest request repeats
  them
- missing context stays grounded in supplied entities and actions; the child
  does not invent adjacent operational requirements or expand a short procedure
  into a speculative template
- the child owns both cold review and revision
- the parent performs only provenance, scope, authority, preservation, and
  output-mode checks and does not rewrite prose
- comments-only mode requires an explicit user request
- unavailable or prohibited subagents stop the workflow without a same-context
  assessment or revision
- the Skill needs no custom agent configuration, script, reference, or external
  dependency

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Explicit trigger | Activates for ordinary trimming or proofreading | `triggers.json` | Observable Skill loads |
| Fresh child | Reuses or forks the authoring conversation | `author-context-file-revision` | Child identity and spawn trace |
| Payload integrity | Sends parent diagnosis or expected deletions | `author-context-file-revision` | Child payload inspection |
| Revision ownership | Child reviews, then parent rewrites | `author-context-file-revision` | Child output and parent trace |
| Chat artifact relay | Parent summarizes text before delegation | `chat-artifact-revision` | Payload comparison |
| Comments authority | Rewrites when comments only were requested | `comments-only` | Child and final output inspection |
| Fail closed | Self-edits when delegation is prohibited | `subagents-prohibited` | No child, assessment, or revision |
| Preservation | Compression removes a hard constraint or uncertainty | revision cases | Artifact assertions |
| Dual-client support | Behavior works on only one target client | all runnable cases | Separate Codex and Claude records |

## Execution protocol

1. Compare the candidate with commit `2f57393` as the previous behavior and
   with no Skill when trigger selection needs a control.
2. Use an isolated disposable workspace and client home. Install only the target
   Skill and the adjacent Skills named by the case.
3. For author-context cases, create an actual parent conversation containing the
   supplied authoring turns, then issue the latest request as a later turn. Do
   not flatten the turns into the child payload.
4. Capture observable parent and child identifiers, spawn arguments, child
   payload, child result, file hashes, and final response. Keep raw traces
   outside the repository.
5. Run the same fixture with Codex CLI and Claude Code. In Codex, confirm that
   authoring turns were not forked. In Claude Code, confirm that a normal
   `Agent` subagent, not a resumed or forked parent conversation, performed the
   work.
6. Grade output quality separately from orchestration. A fluent revision cannot
   compensate for failed context isolation.
7. Record an unavailable observation as `not exposed` and an unrun client as
   `not executed`. Neither is a pass.

## Acceptance

- every assigned critical assertion passes
- every trigger case selects exactly the expected handler or handlers from
  observable Skill loads
- both Codex and Claude Code expose a distinct child that performs the revision
- no child payload contains parent-only diagnosis, expected deletions, draft
  rationale, or hidden grading criteria
- no parent trace contains discretionary prose repair after the child result
- required facts, prohibitions, uncertainty, and output authority survive
- the candidate improves author-context separation over the previous behavior
  without regressing any assigned preservation assertion

## Current result

On 2026-07-30, Codex CLI 0.146.0 with `gpt-5.6-sol` and high reasoning
produced:

- trigger selection: 10/10 core, near-miss, and coexistence cases passed
- a distinct file-edit child created with `fork_turns="none"` revised only the
  authorized file; the parent performed mechanical inspection and no prose edit
- the prohibited-subagent case stopped without a child call or file change
- the first chat-artifact run expanded four supplied steps into an invented
  operational template, and the first comments-only run leaked an earlier
  author preference into the child result
- after strengthening payload and revision boundaries, both affected cases
  passed: the chat revision stayed grounded in the four supplied actions, and
  comments-only removed the leaked author preference

The exact Codex child task body was encrypted in retained client traces, so its
payload content is `not exposed`; child identity, `fork_turns="none"`, child
workspace actions, parent actions, final output, and file hashes were
observable. Claude Code 2.1.204 was installed but not authenticated, so its
trigger and behavior suites are `not executed`. Blind human comparison is also
not executed.

Because dual-client evidence is incomplete, there is no accepted
`results.json`. The previous `edit-for-readers` result evaluated a different
responsibility and remains available in Git history at commit `2f57393`; it is
not evidence for this Skill.
