---
name: design-agent-instructions
description: Use when you want to design the instruction document set for AGENTS.md / CLAUDE.md / .github/copilot-instructions.md / GEMINI.md.
license: MIT
---

# Design Agent Instructions

## Purpose

- Provide a safe process for designing and creating agent instruction document sets.
- When multiple documents exist, determine the structure without breaking role separation and consistency.

## When to use

- When you want to create a new `AGENTS.md`
- When you want to reorganize the full instruction set including `AGENTS.md` / `CLAUDE.md` / `.github/copilot-instructions.md` / `GEMINI.md`
- When you need to decide which documents to create and what goes where
- When you want to judge whether adding companion documents is necessary or whether `AGENTS.md` alone is sufficient

## Input (optional)

- Purpose / scope / constraints (e.g., global / repository / subdirectory)
- Key rules to add
- Existing related documents (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`, README, docs)

## Steps

1. Confirm the purpose and scope (global / repository / subdirectory).
2. Review the existing instruction document set and project-local primary sources when present.
3. Document the loading order:
   - `~/.codex/AGENTS.md` → repository root `AGENTS.md` → per-subdirectory `AGENTS.md`
4. Fix the source documents to rely on:
   - e.g., existing `README.md`, `docs/*`, language policy docs, or other repository-local instructions
5. Define the role of each document:
   - `AGENTS.md`: formal contract
   - `CLAUDE.md`: supplementary instructions for Claude Code
   - `.github/copilot-instructions.md`: condensed / supplementary instructions for GitHub Copilot
   - `GEMINI.md`: supplementary instructions for Gemini
6. Decide which documents are needed. Do not add unnecessary documents. Include a companion document as a candidate only when that agent is actively used and `AGENTS.md` alone is insufficient for repo-specific guidance.
7. Separate shared facts from what each document should and should not contain.
8. Present a minimal template or document set proposal.
9. List candidates for repo-specific rules and how to divide them without duplication.
10. Note impact (on operations / reviews / sharing).
11. Obtain approval before creating or editing.

## Output format

- Summary of changes: ...
- Purpose / scope: ...
- Target documents: ...
- Loading order: ...
- Primary sources: ...
- Role of each document: ...
- Template or document set proposal:

  ```markdown
  # AGENTS.md

  ## Purpose
  - ...

  ## Guidelines
  - ...

  ## Avoid
  - ...

  ## How to work
  - ...
  ```

- Role notes when related documents exist:
  - `AGENTS.md`: ...
  - `CLAUDE.md`: ...
  - `.github/copilot-instructions.md`: ...
  - `GEMINI.md`: ...
- Impact / risk: ...
- Approval: Is it OK to proceed with this approach?

## Boundaries

### Always:

- Document the loading order
- When related instruction documents exist, evaluate consistency as a document set rather than optimizing a single document in isolation
- Fix available source documents before drafting content
- Propose only the documents needed; do not add unnecessary ones
- Propose in minimal, reviewable units

### Ask first:

- When editing an existing `AGENTS.md`
- When simultaneously creating or revising `CLAUDE.md`, `.github/copilot-instructions.md`, or `GEMINI.md`
- When editing or adding to instruction document groups that include `docs/*`
- When changing responsibility boundaries between documents
- When adding organization policy or security items to a template

### Never:

- Edit or create instruction documents or Skills without approval
- Include secrets or confidential information in templates

## Notes (optional)

- The `AGENTS.md` specification may change; confirm when uncertain
- Avoid repeating the same fact in multiple documents; divide content by role
- Do not contradict existing language (Japanese/English) rules or repository-local documentation when present
- Treat `GEMINI.md` as optional; include it as a candidate only when the target repository requires it
