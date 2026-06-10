# review-changes evals

## Iter 0 — Static check

- description and body are internally consistent around "new review"
- `must` / `should` / `suggestion` / `question` / `nit` / `note` canonical labels are applied per finding
- criteria for each label are clearly defined
- `Must-fix` / `Should-fix` / `Nice-to-have` are accepted as legacy input and normalized to canonical labels
- each finding includes evidence
- each finding explains why it is a problem and how to detect it
- output is sufficient to proceed to the next decision without external context
- at least one `[critical]` assertion is identified

## Scenarios

### Scenario A: Small diff new review

A diff and related spec are provided, with a mix of `must` and `should` findings. No approval decision is made; only decision material is returned.

Requirements checklist:
1. [critical] Each finding has specific evidence
2. Each finding carries exactly one canonical label
3. `must` and `should` criteria match the definitions in the body
4. Test steps or verification points are present

### Scenario B: Review including unconfirmed spec

Part of the diff depends on unclear spec and cannot be asserted definitively. Do not force a `must` — leave it as a `question`.

Requirements checklist:
1. [critical] Do not create a critical finding based on speculation alone
2. Separate unconfirmed spec as a `question`
3. Output contains enough information to pass to triage as-is

### Scenario C: Separating API contract from internal constraints

A case where OpenAPI marks a field non-nullable but the internal storage column is nullable. Should organize findings around the external contract violation, not be pulled toward DB implementation details.

Requirements checklist:
1. [critical] Findings are anchored to external contracts such as API or schema
2. DB nullability is treated as a separate concern
3. Contract violation and implementation detail are not mixed in the explanation
4. A clear contract violation is classified as `must`

### Scenario D: Singular-field change vs. existing cardinality

A new diff uses a singular field or single-record fetch in an area that already has a relation table, multi-record sibling endpoints, and bulk update SQL. Can cross-cutting cardinality assumptions be surfaced?

Requirements checklist:
1. [critical] Existing cardinality is confirmed by inspecting relations and sibling endpoints
2. The impact of singularization on backward compatibility and neighboring API consistency is explained
3. Conclusion is not drawn from a single code fragment alone

### Scenario E: Grounding consistency comments in repo precedents

No definite bug, but compared to handlers/wrappers/types with the same responsibility, this diff alone deviates in timezone or conversion policy. Can in-repo precedents be used to set the strength of the consistency comment?

Requirements checklist:
1. [critical] Cross-cutting in-repo precedents are used as evidence for findings about the same responsibility
2. When precedents are weak, the finding strength is reduced rather than overstated
3. The finding is framed as a consistency gap, not a personal preference
4. Recommended fixes use `should`; optional improvements use `suggestion`

### Scenario F: Review findings useful for learning

A problem is found in a diff review, but the finding alone would not help detect the same problem next time. A thorough explanation of why it is a problem and how to detect it is included.

Requirements checklist:
1. [critical] Each finding retains matched evidence, why-it-is-a-problem, how-to-detect, and verification point
2. The why-it-is-a-problem connects to spec, accident risk, maintainability, test gaps, or similar concerns
3. The how-to-detect generalizes beyond the current diff into a reusable verification approach
4. Approval decision is not finalized; findings are left as decision material

### Scenario G: Separating minor suggestions from reference notes

The diff contains minor naming variations, optional readability improvements, and future-watch notes. Non-blocking concerns should not be over-escalated.

Requirements checklist:
1. [critical] Minor naming or wording findings are not classified as `must` or `should`
2. Optional improvement proposals are classified as `suggestion`
3. Trivial findings are classified as `nit`
4. Background information requiring no action is classified as `note`

### Scenario H: Normalizing legacy label input

Receive `Must-fix` / `Should-fix` / `Nice-to-have` from existing notes and align them to canonical labels in the normal output of `review-changes`.

Requirements checklist:
1. [critical] `Must-fix` / `Should-fix` / `Nice-to-have` are not used as primary headings in the output
2. `Must-fix` is normalized to `must`
3. `Should-fix` is normalized to `should`
4. `Nice-to-have` is normalized to `suggestion` or `nit` based on content

### Scenario I: State reconciliation in re-review

Previous findings and current diff are provided; resolved, remaining, and newly found items are mixed. States and labels must not be conflated; output is organized as a re-review result.

Requirements checklist:
1. [critical] State labels are unified as `Resolved` / `Remaining` / `New`
2. State and canonical label are treated as separate axes
3. When a `Remaining` `must` exists, there is enough evidence to use it for an approval decision

### Scenario J: Boundary — approve without reading

A request to rubber-stamp a PR without providing a diff. Should produce a finding or explicit "no issues found with reasoning", not a bare LGTM.

Requirements checklist:
1. [critical] Does not output a bare LGTM or Approved without evidence
2. Requests the diff or explains that review cannot proceed

## Failure Pattern Ledger

- `findings lack evidence`
- `severity mixed with decision`
- `review only meaningful inside triage flow`
- `review not reusable for learning`
- `learning note detached from finding`
- `legacy labels used as primary output`
- `uncertain premise classified as must`
- `non-blocking suggestion escalated to should or must`
- `status mixed with label`
