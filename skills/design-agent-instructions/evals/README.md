# design-agent-instructions evals

## Iter 0 — Static check

- description and body are internally consistent on "designing and creating an instruction document set"
- roles of `AGENTS.md` / `CLAUDE.md` / `.github/copilot-instructions.md` / `GEMINI.md` are distinguishable
- only necessary documents are proposed — unnecessary documents are not assumed
- repository-local docs such as `docs/authoring.md` are used only when present, not assumed as portable dependencies
- at least one `[critical]` assertion is identified: no unnecessary documents proposed by default

## Scenarios

### Scenario A: Minimal instruction document set design

A new repository needs `AGENTS.md` and `.github/copilot-instructions.md`, but it is unclear whether `CLAUDE.md` and `GEMINI.md` are needed. The executor must organize the primary source, loading order, and per-document roles, and propose only the documents that are actually needed.

Requirements checklist:
1. [critical] Propose only needed documents — do not assume all four are required
2. State the loading order explicitly
3. Separate per-document roles
4. Do not proceed to create or edit before approval

### Scenario B: Redesign with responsibility conflicts in existing documents

Existing `AGENTS.md` and `CLAUDE.md` duplicate the same rules; `.github/copilot-instructions.md` is under-specified; `GEMINI.md` appears unnecessary. The executor must organize responsibility conflicts and return a document-set proposal stating what goes where and what is omitted.

Requirements checklist:
1. [critical] Identify document-level responsibility conflicts and overlaps
2. Treat `GEMINI.md` as optional — do not include it unnecessarily
3. Separate shared facts from document-specific content
4. Retain impact and risks for an approval decision

### Scenario C: Optional document not forced when agent not in use

The team uses only Claude Code and GitHub Copilot. Someone suggests adding `GEMINI.md`. The executor must treat it as optional and not recommend it when Gemini is not being used.

Requirements checklist:
1. [critical] Do not recommend adding `GEMINI.md` when Gemini is not part of the workflow
2. Explicitly state the document is optional

### Scenario D: Repository without authoring docs

The target repository has `README.md` and `AGENTS.md`, but no `docs/authoring.md` or language policy document. The executor must design the instruction document set from the available sources and must not require repository-local docs that do not exist.

Requirements checklist:
1. [critical] Does not require `docs/authoring.md` or any absent repo-local docs
2. Uses existing `README.md` / instruction documents as the available source set
3. Clearly marks missing local policies as absent rather than inventing them

## Failure Pattern Ledger

- `all documents proposed by default`
- `document roles overlap without exclusion rules`
- `agent-specific optional document treated as mandatory`
- `optional document criteria inferred, not surfaced early`
- `repository-local docs treated as portable dependencies`

## Iter 1 — date unknown

### Changes
- Initial run. Skill body unchanged from Iter 0.
- Pattern applied: `(baseline)`

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|
| A | ○ | N/A | N/A | 0 | — |
| B | ○ | N/A | N/A | 0 | — |

Note: `spawn_agent` / `wait_agent` could not retrieve `tool_uses` or `duration_ms`; steps/duration are unrecorded for this iteration.

### Structured reflection

- Scenario A:
  - Issue: The judgment on whether supplementary documents are needed depends on which agents are actually in use — a runtime assumption.
  - Cause: The body says "propose only needed documents" but the criteria for including supplementary documents could be stated more upfront.
  - General Fix Rule: Skills with optional supplementary documents should state adoption criteria early in "When to use" or "Steps."
- Scenario B:
  - Issue: Responsibility conflict reorganization works, but the canonical destination for shared facts partially depends on reader judgment due to limited examples.
  - Cause: While `AGENTS.md` is stated as the formal contract, the boundary for what stays in README/docs lacks concrete examples.
  - General Fix Rule: Document-set design Skills should provide at least one-line examples for the contract / supplementary-instruction / general-documentation split.

### Ledger updates

- Re-seen: `all documents proposed by default` — did not recur; only necessary documents were proposed
- Re-seen: `agent-specific optional document treated as mandatory` — did not recur; `GEMINI.md` was kept optional
- Added: `optional document criteria inferred, not surfaced early`

### Next fix proposal

- Add one line to "When to use" or "Steps" stating that supplementary documents are only candidates when the target agent is actively used
