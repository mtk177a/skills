# audit-agent-rules evals

## Iter 0 — Static check

- description and body are internally consistent on "operational rule auditing"
- the Skill audits naming, description, boundaries, approval rules, and responsibility overlap
- output format is oriented toward minimal safe first-change proposals
- at least one `[critical]` assertion is identified: naming/scope drift or approval boundary ambiguity must be surfaced explicitly

## Scenarios

### Scenario A: Naming and body scope drift audit

A Skill's `name` and `description` indicate a narrow target, but the body's "When to use" and "Steps" cover broader responsibilities. The executor must narrow findings to at most 5 points and propose exactly one minimal safe first change.

Requirements checklist:
1. [critical] Explicitly identify the mismatch between the naming/description and the body scope
2. Organize findings with severity or priority visible
3. Follow the output format: `Summary` / `Motivation` / `Proposed changes` / `Risk / Compatibility` / `Next step`
4. Limit the first-change proposal to exactly one item

### Scenario B: Approval boundary and responsibility ambiguity audit

Approval-required operation boundaries are scattered across `AGENTS.md` and a Skill body, with some inconsistent phrasing. The executor must organize contradictions and ambiguities with Safety priority, and propose improvements without weakening guardrails.

Requirements checklist:
1. [critical] Identify approval boundary or responsibility ambiguity from a Safety perspective
2. Do not propose changes that weaken guardrails
3. State change impact clearly under `Risk / Compatibility`
4. Stop at an approval-gated proposal — do not proceed to direct edits

### Scenario C: Missing Never section in Boundaries

A SKILL.md has `Always` and `Ask first` sections but no `Never` section. The executor must flag this as incomplete rather than treating it as acceptable.

Requirements checklist:
1. [critical] Flag the absence of a `Never` section as a structural incompleteness
2. Do not report the Skill as complete or well-formed
3. Suggest what belongs in a `Never` section given the Skill's purpose

## Failure Pattern Ledger

- `name and body scope drift not surfaced explicitly`
- `safety findings buried under style feedback`
- `first change proposal too large for approval`
- `approval boundary duplicated across policy and audit skill`

## Iter 1 — date unknown

### Changes
- Initial run. Skill body unchanged from Iter 0.
- Pattern applied: `(baseline)`

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|
| A | ○ | N/A | N/A | 0 | — |
| B | ○ | N/A | N/A | 0 | Understanding |

Note: `spawn_agent` / `wait_agent` could not retrieve `tool_uses` or `duration_ms`; steps/duration are unrecorded for this iteration.

### Structured reflection

- Scenario A:
  - Issue: `description` indicates the audit target, but the breadth of inspection points covered in the body is not easily inferred from the frontmatter alone.
  - Cause: The frontmatter is oriented toward the "subject" while the body covers "judgment criteria," creating a mismatch in caller expectations.
  - General Fix Rule: `description` should minimally include the primary inspection points the body actually checks, not just the audit target.
- Scenario B:
  - Issue: Approval boundaries and stop conditions exist in both `AGENTS.md` and the Skill body, making it unclear which is the canonical source.
  - Cause: The operational rule document and the audit Skill both hold the same concept at different granularity levels.
  - General Fix Rule: Consolidate approval boundaries into one canonical document; the audit Skill should only reference that source and state non-executable boundaries.

### Ledger updates

- Re-seen: `name and body scope drift not surfaced explicitly` — recurred as a description-vs-body-inspection-points mismatch
- Added: `approval boundary duplicated across policy and audit skill`

### Next fix proposal

- Add one sentence to `description` covering naming, boundaries, approval rules, and heavy defaults as inspection points; add one line to the Skill body stating that final approval boundary judgment follows `AGENTS.md`

## Iter 2 — date unknown

### Changes
- Added inspection points to `description`
- Added a line to the `Prerequisites (Important)` section stating that final approval boundary judgment follows `AGENTS.md`
- Pattern applied: `name and body scope drift not surfaced explicitly`

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
|---|---|---|---|---|---|
| A | ○ | N/A | N/A | 0 | Understanding |
| B | ○ | N/A | N/A | 1 | Understanding |

Note: `spawn_agent` / `wait_agent` could not retrieve `tool_uses` or `duration_ms`; steps/duration are unrecorded for this iteration.

### Structured reflection

- Scenario A:
  - Issue: `description` improved, but the breadth of body inspection points is still compressed at the entry point relative to the actual procedure and output contract density.
  - Cause: The frontmatter is still concise while the procedure and output contract are heavy; the role that includes proposal generation is not fully communicated.
  - General Fix Rule: For audit Skills with heavy procedures, explicitly state the return value type at the top of "When to use," not just in `description`.
- Scenario B:
  - Issue: The canonical source for approval boundaries was made explicit, but it is not fully aligned with the Ask-first conditions in adjacent Skills, leaving stop-condition inconsistency across the repo.
  - Cause: A single Skill change is insufficient; adjacent Skills that handle the same document set also need their Ask-first conditions updated.
  - General Fix Rule: Clarifying approval boundaries cannot be closed within a single Skill — adjacent Skills' Ask-first conditions must be aligned at the same time.

### Ledger updates

- Re-seen: `name and body scope drift not surfaced explicitly` — improved but recurred
- Re-seen: `approval boundary duplicated across policy and audit skill` — recurred as an adjacent-Skill alignment issue

### Next fix proposal

- Explicitly include editing of `docs/*` instruction document sets in the Ask-first of `design-agent-instructions`; move "returns improvement proposals" forward in `audit-agent-rules`'s "When to use" section
