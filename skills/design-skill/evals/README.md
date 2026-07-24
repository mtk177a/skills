# design-skill evals

## Purpose

Verify that `design-skill` decides whether durable Skill guidance is warranted, produces a coherent and portable design when it is, and stops at an implementation handoff.

Structured assets:

- `triggers.json`: should-trigger, should-not-trigger, and near-miss selection cases
- `evals.json`: baseline, isolation, coexistence, and behavioral assertions
- [`results.json`](results.json): immutable revision identifiers and the durable case-by-requirement evidence matrix for the currently accepted revision

## Candidate static check

- `description` carries the complete trigger and negative boundary
- the body starts from outcome and evidence rather than a requested artifact
- the bundled guide requires discovery of applicable local instructions without assuming a root filename
- no fixed proposal template, universal approval sequence, or mandatory boundary headings remain
- the Skill compares no guidance, existing-Skill revision, split or merge, and new Skill interventions
- evaluation precedes extensive authoring
- evaluation scope follows material responsibility and failure coverage rather than a fixed scenario or run count
- client-specific metadata is added only for a demonstrated invocation, UI, tool, or permission need
- portable metadata is reported separately from target-labeled client extensions, even when a client requires fields in the same file
- third-party and executable designs preserve provenance and trace combined data and capability paths
- executor inputs do not include hidden assertions or expected conclusions
- the Skill ends at an implementation handoff
- every candidate assertion in `evals.json` is exercised by at least one case, and only fail-gating requirements are marked critical

## Scenarios

### Scenario A: Requested Skill with a healthy baseline

The user asks for a Skill, but repeated no-Skill runs already meet the intended outcome without specialized knowledge or corrections.

Requirements checklist:

1. [critical] Do not force a new Skill when evidence supports no durable guidance
2. Compare the relevant non-Skill interventions
3. Define what evidence would justify revisiting the decision
4. Stop without implementation

### Scenario B: Extract a proven recurring workflow

Several real executions expose the same domain mapping, deterministic validator, and recurring correction.

Requirements checklist:

1. [critical] Ground the design in the supplied artifacts and corrections
2. Define a coherent responsibility and trigger boundary
3. Allocate instructions, references, scripts, and evals by demonstrated need
4. Exclude private task data from the portable design
5. Produce an implementation-ready handoff without editing files

### Scenario C: Overlap and coexistence

The proposed Skill overlaps separate planning and execution Skills.

Requirements checklist:

1. [critical] Compare add, merge, split, and retain-current options
2. Keep trigger, output, and risk boundaries coherent
3. Design coexistence and near-miss evaluation
4. Do not collapse planning and execution solely to reduce file count

### Scenario D: Mixed task fragility

One part of a workflow requires contextual judgment while another requires an exact verified sequence.

Requirements checklist:

1. [critical] Use different degrees of control for the contextual and fragile parts
2. Preserve material safety and permission properties
3. Prefer a tested script for deterministic fragile operations when justified
4. Define executable verification

### Scenario E: Unknown repository layout

The target repository can be inspected, but its local guidance filenames and directory conventions are unknown.

Requirements checklist:

1. [critical] Discover applicable local instructions instead of requesting a standard root file
2. Treat discovered local instructions as authoritative in their scope
3. Avoid importing this repository's distribution assumptions
4. Keep the design portable where local constraints are silent

### Scenario F: Diagnosis required before redesign

The user requests a redesign based only on the current text and provides no behavioral or loading evidence.

Requirements checklist:

1. [critical] Do not claim that a textual rewrite is a demonstrated behavioral fix
2. Identify missing trigger, loading, client, trace, and baseline evidence
3. Design the smallest evaluation or diagnostic step that can resolve the uncertainty
4. Keep behavior unconfirmed until evidence exists

### Scenario G: Evaluation design without a target count

The Skill responsibility and changed behavior are known. Some trigger, coexistence, and output risks are material, while other standard evaluation dimensions cannot affect the decision.

Requirements checklist:

1. [critical] Map each material claim or change to a plausible failure, scenario or check, and grader
2. Include only evaluation dimensions that address a distinct risk
3. Do not add scenarios or repeated runs to reach a target number
4. Distinguish static validation, targeted regression, and empirical tuning

### Scenario H: Adapt a third-party executable Skill

An external Skill bundles a script, follows mutable remote instructions, reads workspace data, and uploads results. The target clients have different invocation and permission controls.

Requirements checklist:

1. [critical] Establish provenance, license, pinned source, complete file scope, and local modifications before recommending adoption
2. Trace input, filesystem access, script and tool execution, outbound data, destination, and enforceable controls as one capability chain
3. Keep portable instructions separate from client-specific invocation, UI, tool, and permission metadata
4. Reject or leave the design unverified when provenance or outbound data flow cannot be established
5. Define only the security and client evaluation needed for the identified risks

## Failure Pattern Ledger

- `requested artifact accepted without testing whether a Skill adds value`
- `generic authoring advice substituted for real task evidence`
- `repository-root document name treated as a portable dependency`
- `local instructions demoted below a bundled generic guide`
- `body-only trigger guidance cannot affect implicit selection`
- `overlapping Skills retained or merged without coexistence analysis`
- `fixed proposal template consumes attention without improving the decision`
- `Always / Ask first / Never treated as mandatory quality criteria`
- `implementation performed by the design workflow`
- `candidate declared improved without baseline or behavioral evidence`
- `evaluation checklist expanded mechanically without distinct failure coverage`
- `executor shown the expected conclusion or grading criteria`
- `client-specific metadata added without a client behavior that requires it`
- `third-party Markdown reviewed without tracing scripts, remote instructions, or outbound data`

## Historical baseline — Iter 1, date unknown

### Changes

- Initial run. Skill body unchanged from Iter 0.
- Pattern applied: `(baseline)`

### Execution results

| Scenario | Result | steps | duration | retries | Weak phase |
| --- | --- | --- | --- | --- | --- |
| A | × | N/A | N/A | 0 | Understanding |
| B | ○ | N/A | N/A | 0 | — |

Note: `spawn_agent` / `wait_agent` could not retrieve `tool_uses` or `duration_ms`; steps/duration are unrecorded for this iteration. Accuracy was 87.5% for Scenario A, 100% for Scenario B.

### Structured reflection

- Scenario A:
  - Issue: When the usage context is abstract, the Skill's logic for stopping at a provisional name rather than confirming it is not easily read from the first half of the body.
  - Cause: The overlap check and primary source reference are clear, but the stop condition for abstract inputs appears after the naming step in the procedure.
  - General Fix Rule: Authoring Skills that handle abstract inputs should explicitly surface the step of fixing the usage context in one sentence before the naming step.
- Scenario B:
  - Issue: Overlap candidate organization worked, but the judgment axis for absorbing into an existing Skill relied partially on supplementary reasoning.
  - Cause: The body requires an overlap check but does not provide examples for when to absorb into an existing Skill versus creating a new one.
  - General Fix Rule: Skills that handle overlap decisions should briefly exemplify the judgment axis for absorbing into an existing Skill.

### Ledger updates

- Re-seen: `metadata proposed without trigger-oriented description` — a provisional description was used, but could not be finalized for abstract inputs
- Added: `abstract request reaches naming step too early`

### Next fix proposal

- In "When to use" and "Steps," move forward the rule that abstract inputs require fixing the usage context in one sentence and stopping at a provisional name if responsibility boundaries are not yet confirmed

## Iter 2 — 2026-07-24

### Changes

- Reframed the Skill from proposal assembly to evidence-first intervention design
- Replaced named repository-root dependencies with local-guidance discovery
- Removed the fixed proposal, approval, formatting, and boundary-heading requirements
- Added baseline, trigger, isolation, coexistence, and output-quality assets

### Execution results

- Client / model: Codex validator / `gpt-5.6-terra`, medium reasoning
- Date: 2026-07-24
- Configuration: candidate and historical version tested separately with only their directly bundled guide; no eval files or expected answers exposed
- Static checks: passed
- Selected behavior cases:
  - A, healthy baseline: candidate passed; historical version reached the same no-Skill decision but emitted unnecessary fixed boundary and approval sections
  - B, overlap and coexistence: candidate passed with phase-specific triggers, coexistence checks, baseline comparison, and a design-only handoff; historical version chose the correct split but retained the fixed proposal contract
  - E, unknown repository layout: candidate passed by discovering local authority without assuming filenames or drafting premature metadata; historical version treated local guidance as supplemental and continued into fixed boundary and approval steps
- Candidate selected-case result: 3 / 3 passed
- Historical selected-case judgment: 3 / 3 reached a viable intervention, with contract and portability regressions described above
- Steps, duration, and token counts: not exposed
- Trigger runs: not executed
- Full six-case behavioral suite: not executed
- Coexistence with adjacent loaded Skills: not executed

### Next validation question

- Does the candidate's narrower description avoid trigger collisions with audit and implementation Skills across repeated observable runs?

## Current revision — 2026-07-24

- Client: Codex CLI 0.145.0
- Model / reasoning: `gpt-5.6-sol` / high
- Baseline: commit `42ebd18cb2406d1cfcbeb34cd289fd620c8e4f9b`
- Candidate `SKILL.md`: `sha256:ec5d29bd278ad1812e074a4134c4b06897d3a71e3ffc4923fd0eb2a2e2cdac19`
- Candidate `references/authoring-guide.md`: `sha256:0929fdd5208f9acd313629273f52aaffc7c21ac2845ebd0ba0da2eb12e62074e`
- Selected scenarios: D, G, and H
- Candidate grading: 13 / 13 requirements passed; baseline: 11 passed and 2 partial
- Improvements: material claims map directly to failure/check/grader paths, evaluation depth and escalation are explicit, and portable metadata is separated from target-labeled client extensions
- Writable fixture hashes: unchanged in baseline and candidate
- Regressions: an initial portable-metadata partial was corrected and the affected case rerun; final regression count is zero
- Durable evidence: [`results.json`](results.json)
- Trigger suite: not executed because the `description` did not change in this revision
- Claude Code and other clients: not executed
- Unverified: proposed scripts and validators, third-party provenance and endpoints, actual client metadata support, permission prompts, and UI behavior
- Next validation question: Do the target clients tolerate the separately identified extensions and enforce the designed data-flow controls in an isolated executable fixture?
