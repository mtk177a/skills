# format-markdown evals

## Purpose

Determine whether the current `format-markdown` Skill adds reproducible value over blank-slate Codex and configured static tools, without treating CommonMark as a writing style guide or forcing judgment-heavy document organization into a formatter.

## Assets

- [`evals.json`](evals.json): matched behavior fixtures, hidden assertions, applicability, and verdict policy
- [`triggers.json`](triggers.json): trigger, non-trigger, near-miss, coexistence, and unclaimed-requirement cases
- `results.json`: compact evidence from the executed comparison
- this file: evaluation contract, execution protocol, and summarized decision record

## Static findings before execution

- The current Skill describes CommonMark as the basis for recommended, context-dependent, and discouraged style judgments, although CommonMark specifies syntax and parsing rather than a universal writing style.
- The current body does not state the content-preservation, heading-repair, table-normalization, or rewrite-refusal requirements claimed by the previous evaluation README.
- The current Skill mixes rule selection, formatting, approval, reporting, rollback, and delegation to `plan-risky-change`.
- No prior behavior result, no-Skill baseline, or current-Skill requirement matrix exists.
- A routing observation in `define-referents` shows that Codex can select `format-markdown` for a mechanical Markdown request, but it does not establish output quality.

## Coverage map

| Responsibility or boundary | Plausible failure | Scenario or check | Grading |
| --- | --- | --- | --- |
| Safe mechanical normalization | Rewrites wording, changes item order, damages code, or only describes an edit | `deterministic-surface-normalization` | File invariants and hidden grader |
| No implicit hard wrapping | Introduces physical line breaks from an unstated 80-column rule | deterministic and Japanese cases | Physical-line comparison |
| Japanese and ASCII spacing | Misses requested boundaries or corrupts protected token internals | `japanese-ascii-boundaries` | Expected boundaries and protected substrings |
| Semantic heading boundary | Silently promotes or demotes a heading without knowing its relationship | `ambiguous-heading-relation` | File hash and response inspection |
| Explicit mixed authority | Refuses an authorized wording edit or invents retry behavior | `authorized-format-and-wording` | Fact containment and unsupported-claim check |
| Review versus mutation | Edits during a review-only request or treats reorganization as mechanical formatting | `markdown-structure-review-only` | Fixture hash and categorized observations |
| CommonMark authority | Presents parser behavior as universal style recommendation | all agent cases | Requirement-level grader |
| Trigger boundary | Absorbs prose rewriting, review, implementation, toolchain design, or unclaimed Japanese rules | `triggers.json` | Observable Skill load |

## Behavior execution protocol

1. Use Codex CLI 0.145.0 with `gpt-5.6-sol`, high reasoning, ephemeral sessions, ignored user instructions, and disposable fixture directories.
2. Give every agent condition the same prompt, file, and local execution authority.
3. For `no_skill`, expose no `format-markdown` Skill. For `current_skill`, copy the current `SKILL.md` into the disposable catalog and require it to be read before solving the task.
4. Run the static condition on an identical fixture with pinned packages in a temporary npm project:
   - `prettier@3.9.6` with Markdown parsing and `proseWrap: preserve`
   - `textlint@15.7.1` with `textlint-rule-ja-space-between-half-and-full-width@3.0.2`, using `space: ["alphabets", "numbers"]` and `lintStyledNode: false`
   - `markdownlint-cli2@0.23.2` in check-only mode with an explicit default-off configuration and `MD013` disabled
5. Apply the static stages in this order: Prettier, textlint fix, markdownlint check. Do not run them against repository files.
6. For format-only fixtures, render before and after with the pinned `markdown-it@14.3.0` transitively installed by the toolchain. A changed rendered-structure hash overrides a prose grader's content-preservation pass.
7. Keep assertions and expected conclusions hidden from agent executors. Grade objective file properties deterministically and judgment-heavy outputs with a separate Codex grader that is not told the condition name.
8. Record a static responsibility outside the declared tool scope as `not_applicable`, not pass or fail.
9. Run one matched observation per agent condition and one deterministic static run. Repeat both agent conditions for an affected case only when a partial result, unexpected difference, or instability could change the decision.
10. Keep prompts, responses, JSONL, grader output, npm contents, and fixture copies under `/tmp`. Commit no raw traces.

## Trigger execution protocol

Present each routing prompt with only the descriptions named in `triggers.json`. Require the selector to open every selected Skill so loading is observable. Count only observed file reads. The no-Skill and static-tool conditions have no trigger behavior and are not assigned artificial routing passes.

## Decision rule

- Recommend retirement when static tools cover the deterministic responsibilities and no-Skill Codex is equal or better on judgment-heavy responsibilities without a critical regression.
- Keep the current Skill as a candidate only if it reproducibly improves at least one material, non-deterministic requirement, introduces no critical regression, and owns a precise trigger boundary.
- If deterministic work belongs to tools but a repeatable structure-review gap remains, recommend a separately designed, narrower review Skill rather than preserving the current mixed responsibility.
- Treat a missing static capability as a tool or custom-checker decision, not by itself as evidence that a Skill is required.
- Do not collapse the case-by-requirement matrix into a single score.

## Failure Pattern Ledger

- `CommonMark treated as a universal style authority`
- `format-only request changes wording or meaning`
- `80-column hard wrap introduced without an authoritative rule`
- `URL, link destination, code, command, or identifier corrupted`
- `heading relationship invented to satisfy a lint rule`
- `authorized wording change refused as categorically out of scope`
- `review-only request edits the fixture`
- `static not-applicable responsibility reported as passed`
- `Skill activation treated as evidence of output quality`

## Current revision

Evaluated on 2026-07-29 with Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, and a temporary pinned static toolchain.

- Skill-less and current-Skill Codex were equal on heading ambiguity, explicitly authorized wording, and review-only structure judgment.
- Both agent conditions changed two separately rendered lists into one list during mechanical normalization. The static condition preserved the rendered structure and reported the marker conflict.
- The current Skill condition completed Japanese spacing outside styled nodes in two of two observations; Skill-less Codex missed those boundaries in both runs. The tested textlint configuration also covered only part of that rule.
- The current Skill loaded incorrectly for Markdown toolchain design and for the unclaimed Japanese-spacing request in both initial and repeated routing observations.
- The evidence therefore recommends retiring the current mixed Skill and evaluating deterministic Markdown and Japanese spacing rules separately. It does not yet recommend a specific repository dependency or replacement Skill.
- The maintainer accepted retirement on 2026-07-29 and deferred any replacement Skill or static-tool design to a separate future decision.
- Claude, other clients and models, additional textlint rules, context-sensitive punctuation, MDX, and the complete GFM extension set were not executed.

See [`results.json`](results.json) for package integrity, requirement-level evidence, the rendered-structure grader correction, routing observations, and unverified scope.

### Deferred replacement question

- If a distributed replacement is reconsidered, which deterministic rules belong in a bundled checker, which should defer to each consumer repository's configured tools, and which remain outside the Skill?
