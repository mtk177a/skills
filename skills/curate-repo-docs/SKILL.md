---
name: curate-repo-docs
description: Curates repository-managed documentation by deciding whether a documentation change is needed, selecting only reader-relevant and evidence-backed content, placing it in the appropriate source of truth, making the smallest authorized edit, and validating the result. Use for README files, repository docs, current architecture or behavior, how-to guides, runbooks, references, and records of explicit design decisions. Not for general prose polishing, articles or book chapters, cold revision, diff-only review, documentation-system governance, or inferring requirements or rationale from code alone.
license: MIT
---

# Curate Repository Documentation

## Objective

- Decide whether repository documentation needs to change before drafting text.
- Publish only information that the intended reader needs and that available evidence or an authorized decision supports.
- Put information in its canonical location, make the smallest authorized change, and validate the result without turning investigation context into documentation.

## Evidence and authority

Inspect the applicable repository instructions, target document, implementation, tests, schemas, generated sources, accepted decisions, and relevant history.
Use only the evidence needed to resolve the documentation change.

Classify candidate information internally:

- **Verified:** confirmed by code, tests, schemas, execution results, or accepted documentation
- **Normative:** explicitly decided by a person or source with authority over the requirement
- **Inferred:** plausible but not explicitly established
- **Unknown:** unavailable, conflicting, or impossible to determine from the accessible sources

Publish Verified and Normative information as fact.
Do not publish Inferred information as fact.
Report material Unknowns instead of filling them with plausible content.

Code can establish current behavior.
It does not by itself establish business requirements, design rationale, policy, intended permanence, ownership, SLOs, or acceptable risk.

## Workflow

1. Confirm the requested outcome, edit authority, target scope, and applicable repository instructions. Treat a request to explain, assess, or review as read-only unless it also authorizes editing.
2. Determine the reader, the task the reader must complete, and the document's role. When selecting or creating a document kind, read [document-kinds.md](references/document-kinds.md).
3. Identify the canonical sources for the claims under consideration. Prefer a generated or executable source over a manually duplicated reference.
4. Decide exactly one documentation-impact state:
   - `Update required`
   - `No documentation impact`
   - `Blocked by unknowns`
5. Before drafting, form a temporary document contract containing: `Audience`, `Reader task`, `Document role`, `Canonical sources`, `Claims to publish`, `Explicit decisions`, `Excluded context`, `Unknowns`, `Validation`, and `Update triggers`. Do not persist this contract unless the user asks for it or the repository defines it as document metadata.
6. Admit a claim only when both conditions hold:
   - it is necessary for the reader's task, accuracy, or safety
   - it is Verified or Normative
7. For an authorized update, read [repository-writing.md](references/repository-writing.md), preserve the existing language and useful structure, and edit the smallest coherent section. Link to the canonical source instead of duplicating it.
8. Remove investigation narrative, discarded hypotheses, generic best-practice filler, template-only sections, redundant examples, and unrelated rewrites. Delete a heading, paragraph, or example when removing it does not reduce task completion, correctness, or safety.
9. Run the repository-provided checks relevant to the changed content. Do not install a new documentation tool merely to complete this workflow. Record an unavailable check as unperformed, not passing.
10. Before reporting, reconcile every claimed check with the observed command or execution trace. Do not name a check as run when the trace does not show it, and do not present a conclusion derived from inspection as an observed execution result.

## Decision handling

Return `No documentation impact` without editing when the change does not alter reader-visible behavior, contracts, operations, architecture, configuration, or other documented facts.

Return `Blocked by unknowns` without inventing content when a required claim depends on missing authority or evidence.
Identify the exact unknown and the source or decision needed to continue.

When reverse-engineering current behavior, label it as descriptive rather than normative and record the revision or commit examined when practical.
Preserve undefined or conflicting behavior as an explicit unknown.

## Validation and reporting

Validate the affected claims rather than only the Markdown syntax.
Depending on the repository, use:

- documentation lint, link checks, or a strict documentation build
- execution of changed commands or examples
- comparison with API, configuration, database, or generated schemas
- regeneration followed by a clean-diff check
- inspection of relative links, identifiers, terminology, and success criteria

Report:

- the documentation-impact state
- changed documents and their reader-facing purpose, or why no edit was made
- canonical sources used
- checks actually run and their results
- material unknowns, unperformed checks, and residual documentation impact

Keep the report shorter than the investigation unless the user requests the evidence record.

## Boundaries

- Do not treat Skill invocation as authority to edit files, publish content, or make another external write.
- Do not redesign a documentation system, perform a repository-wide freshness audit, or create policy merely because a local document needs work.
- Do not use `japanese-tech-writing` or `cognitive-rhythm-writing` automatically. If the user explicitly combines writing Skills, keep content selection, evidence, source-of-truth placement, and edit scope under this Skill; let the other Skill adjust expression only within the admitted content.
- Use a design workflow to make unresolved design decisions. Record only decisions that an authorized source has made.
- Use a diff-review workflow to review a completed change and a fresh-revision workflow only when the user explicitly requests a cold or independent pass.
