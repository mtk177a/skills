---
name: design-agent-instructions
description: Designs new or reorganized durable instruction document sets for the agent clients a repository actually uses. Use before editing when deciding source-of-truth roles, loading and precedence relationships, shared versus client-specific guidance, and necessary companion files; not for diagnosing unexplained behavior, ordinary Skill design, or executing an approved document change, which belongs to an implementation workflow.
license: MIT
---

# Design Agent Instructions

## Objective

- Design the smallest instruction document set that reaches the intended clients with clear authority and minimal duplication.
- Base document roles on verified client semantics and repository needs rather than assuming that one filename or hierarchy is universal.
- Produce an implementation-ready handoff without editing the instruction set.

## Evidence

Gather what is available:

- intended behavior, scope, active users, clients, and models
- existing instruction documents, client configuration, imports, rules, hooks, policy surfaces, and general project documentation
- current official client documentation when loading, discovery, precedence, enforcement, or supported filenames are material
- observed loading evidence, traces, corrections, or failures
- applicable local policy and authorization boundaries

Distinguish observed evidence, inference, assumptions, and unknowns. If the request begins from unexplained behavior and loading or authority is uncertain, diagnose it with `audit-agent-guidance` before treating a document redesign as the fix.

## Workflow

1. Define the intended behavior, scope, active clients, and what must be shared or client-specific. If unexplained non-adherence is the primary question and loading or authority remains uncertain, stop document design and explicitly hand off to `audit-agent-guidance` with the missing evidence.
2. Review the existing instruction set and project-local primary sources. Do not assume that an absent standard filename is itself a defect.
3. For each target client, verify and record the relevant loading, discovery, precedence, import, and enforcement semantics. Do not project one client's hierarchy onto another.
4. Identify the canonical source for each shared fact or rule. Use imports, references, or generated views only when the target client supports them and they reduce drift without hiding authority.
5. Separate durable behavioral guidance from enforced permissions or lifecycle automation. Use client policy, settings, or hooks when a guarantee is required and the client provides that mechanism.
6. Decide which documents and configuration surfaces are necessary. Include a client-specific companion only when that client is actively used and cannot consume the canonical guidance directly.
7. Define what belongs in each surface and what is explicitly excluded. Keep general project facts in ordinary documentation unless they must be present in agent context.
8. Check duplication, contradictions, context cost, portability, ownership, update paths, and behavior after compaction or lazy loading when relevant.
9. Compare the proposed set with keeping the current set, removing redundant guidance, or using a smaller bridge document.
10. Define validation from the material risks: loading observability, precedence conflicts, instruction adherence, enforcement boundaries, and coexistence across active clients.
11. Produce a scoped implementation handoff. Do not create or edit files as part of this design workflow.

## Reporting contract

Use a structure suited to the decision. Include:

- the recommended document set and why it is preferable to the alternatives
- intended behavior, scope, active clients, and unresolved assumptions
- verified loading, discovery, precedence, import, and enforcement semantics by client
- canonical sources and per-surface responsibilities
- documents or surfaces intentionally omitted
- duplication, context, portability, maintenance, and migration risks
- validation coverage and implementation-ready change units
- an explicit diagnostic handoff to `audit-agent-guidance` when unresolved behavior prevents a sound document design

Do not force a companion document, a fixed filename, or a fixed heading template. If behavior is unconfirmed, identify the diagnostic evidence needed instead of presenting the design as a demonstrated fix.

## Boundaries

- Use `audit-agent-guidance` when the primary need is diagnosing why existing guidance behaves inconsistently. Use `design-skill` for reusable Skill responsibility and trigger design.
- Treat instruction documents as behavioral context, not hard enforcement, unless current client semantics establish otherwise.
- Do not assume `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or `GEMINI.md` is loaded by a client without verification.
- Do not duplicate shared facts across files merely to make the set look complete.
- Keep the workflow read-only. Editing requires user authorization and the target environment's applicable policy; do not invent an additional universal approval gate.
- Keep secrets, credentials, personal information, and non-public operational data out of templates and examples.
