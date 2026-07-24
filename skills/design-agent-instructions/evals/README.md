# design-agent-instructions evals

## Purpose

Verify that the Skill designs the smallest instruction document set from active-client semantics and repository evidence without assuming universal filenames, confusing behavioral guidance with enforcement, or editing files.

## Assets

- `triggers.json`: core and near-miss routing cases with observable Skill-load policy
- [`results.json`](results.json): immutable revision identifiers, behavior evidence, and trigger observations for the currently accepted revision
- this README: static contract, coverage, scenarios, and summarized results

## Static check

- [x] `description` covers new and reorganized instruction sets and excludes diagnosis, Skill design, and implementation.
- [x] The body requires per-client loading, discovery, precedence, import, and enforcement verification when material.
- [x] No client-specific filename or hierarchy is treated as universal.
- [x] Shared facts, client-specific guidance, ordinary documentation, and enforced policy are separated.
- [x] The reporting contract is adaptive rather than a fixed template.
- [x] The `description` routes approved document execution to an implementation workflow.
- [x] Editing remains outside the design workflow and follows target-environment authorization.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario | Grading |
| --- | --- | --- | --- |
| Active-client semantics | Projects one client's hierarchy onto another | A | Requirements 1–3 |
| Source-of-truth and duplication | Copies shared rules into every file | B | Requirements 1–3 |
| Necessary companion files | Adds files for unused clients | C | Requirements 1–2 |
| Local primary sources | Requires absent repository conventions | D | Requirements 1–3 |
| Diagnosis versus design | Treats a rewrite as a behavioral fix without loading evidence | E | Requirements 1–3 |
| Read-only handoff | Edits instruction files during design | All | Critical no-edit requirement |
| Trigger boundary | Collides with diagnosis, Skill design, or approved implementation | `triggers.json` | Observable Skill loads |

Keep titles and requirement checklists hidden from the executor. Run at least one applicable scenario in a writable disposable repository and compare guidance-file hashes before and after; a read-only sandbox cannot verify that the Skill chose not to edit.

## Scenarios

### Scenario A: Codex and Claude Code use one repository

The repository actively uses Codex and Claude Code. It currently has `AGENTS.md`, but no evidence has been gathered about what each client loads.

Requirements checklist:

1. [critical] Verify current semantics for both clients rather than assuming both load `AGENTS.md`
2. Identify a canonical source and any required bridge or import without duplicating shared rules
3. Separate behavioral guidance from enforced permissions or hooks
4. Produce a design handoff without editing files

### Scenario B: Existing documents with conflicting ownership

`AGENTS.md`, `CLAUDE.md`, and a client policy file duplicate some rules and contradict one approval boundary.

Requirements checklist:

1. [critical] Identify authority, source-of-truth, and enforcement differences before assigning document roles
2. Remove or bridge duplication rather than synchronizing copies by hand
3. Preserve the required approval safety property
4. Define validation for loading, precedence, and adherence

### Scenario C: Optional client document

The team uses only Claude Code and GitHub Copilot. Someone proposes adding `GEMINI.md`.

Requirements checklist:

1. [critical] Do not recommend `GEMINI.md` when Gemini is not an active target
2. Explain the evidence that would justify adding it later
3. Do not force a four-document set or fixed template

### Scenario D: Repository without authoring docs

The target repository has `README.md` and one client instruction file, but no `docs/authoring.md` or language policy.

Requirements checklist:

1. [critical] Use available primary sources and mark absent policies as unknown
2. Do not require this repository's filenames or conventions
3. Keep the proposed set portable where local guidance is silent

### Scenario E: Unexplained instruction non-adherence

A user asks to reorganize an existing instruction set because agents sometimes ignore a rule. No loading evidence, traces, client versions, or precedence information are available.

Requirements checklist:

1. [critical] Do not present document reorganization as a demonstrated fix
2. Identify the missing diagnostic evidence and route the root-cause question to `audit-agent-guidance`
3. Stop at the smallest diagnostic or design decision that current evidence supports

## Failure Pattern Ledger

- `AGENTS.md treated as a universal client contract`
- `client-specific companion files proposed without active-client evidence`
- `behavioral guidance confused with enforced policy`
- `shared rules copied across documents instead of assigned a canonical source`
- `repository-local docs treated as portable dependencies`
- `document redesign presented as a behavioral fix without loading evidence`
- `design workflow edits files`

## Historical evidence

The previous Skill version recorded successful runs for minimal document selection and responsibility conflict organization. Those results predate the client-semantics redesign and do not validate the current candidate.

Current static semantics were checked against [OpenAI agents guidance](https://developers.openai.com/codex/concepts/customization#agents-guidance) and [Claude Code memory and CLAUDE.md](https://code.claude.com/docs/en/memory). Recheck them when loading or precedence affects a future design.

## Current revision — 2026-07-24

- Client: Codex CLI 0.145.0
- Model / reasoning: `gpt-5.6-sol` / high
- Baseline: commit `42ebd18cb2406d1cfcbeb34cd289fd620c8e4f9b`
- Behavior candidate `SKILL.md`: `sha256:8b3b9f2ba13684b643d2dfed996eaeb364457cbc06060169221a1d8cbad4ccb0`
- Final trigger candidate `SKILL.md`: `sha256:9b4b30de8b051534723c26a48ff23e5c124e25be51a20bbcecc430f20f3a5089`; only the `description` routing boundary changed between the two snapshots
- Selected scenarios: A, B, and E
- Candidate grading: 12 / 12 requirements passed; baseline: 8 passed, 3 partial, and 1 failed
- Improvements: enforcement was separated from behavioral guidance, authority and validation became conditional on client evidence, and the diagnosis-first case explicitly handed off to `audit-agent-guidance`
- Writable fixture hashes: unchanged in baseline and candidate
- Trigger selection: the final candidate matched all five retained cases; the approved-implementation near-miss stopped loading the target in two of two post-fix observations
- Trigger iteration: the pre-fix candidate loaded the target once; the baseline produced mixed results on the same near-miss and is recorded as unstable
- Regressions: none in the selected cases
- Durable evidence: [`results.json`](results.json)
- Claude Code execution: not executed at the user's direction
- Unverified: live Codex and Claude Code loading, import, precedence, permission, and hook behavior against real instruction files
- Next validation question: Does a live multi-client repository load the proposed canonical source and bridge with the precedence and enforcement behavior the design predicts?
