---
name: audit-agent-guidance
description: Audits durable agent guidance—including AGENTS.md, CLAUDE.md, SKILL.md, and agent-facing references—against intended behavior, observed usage, client semantics, and evaluation evidence. Use when diagnosing guidance scope, precedence, trigger conflicts, safety boundaries, context cost, or systemic failures before revision; not for ordinary code review, new Skill authoring, or standalone Codex `.rules` policy review.
license: MIT
---

# Audit Agent Guidance

## Objective

- Diagnose whether durable agent guidance produces the intended behavior and explain why it succeeds or fails.
- Treat "agent guidance" as an umbrella term for durable instructions, reusable workflows, and agent-facing references.
- Audit either one existing Skill or a guidance system spanning multiple surfaces.
- Start from the expected outcome rather than assuming the current artifact or document split is correct.

## Evidence and scope

- Define the intended behavior, failure signals, users, client, and model before naming target files.
- Distinguish observed evidence, reasonable inference, assumptions, and unknowns.
- Discover relevant instruction documents, Skills, references, policy files, client configuration, and distribution metadata. Record their authority, scope, loading order, precedence, triggers, coexistence, permissions, and delivery path when material.
- Check current official client semantics when loading, precedence, approval, or Skill-discovery behavior is material and not established by local primary sources.
- Prefer traces, execution results, evaluations, and usage history over textual plausibility. When behavioral evidence is unavailable, label the work as a static audit and leave behavior unconfirmed.

## Workflow

1. Define the intended behavior, failure signals, affected users, and relevant client and model before referring to an artifact name.
2. Restate the problem, surface hidden assumptions, and consider causes at other layers. Test counterfactuals that keep, remove, move, merge, or replace the current guidance.
3. Discover the relevant guidance surfaces, authority and permission boundaries, loading and precedence rules, triggers, coexistence behavior, and distribution paths. Verify current official client semantics when they materially affect the diagnosis.
4. Gather behavioral evidence such as traces, outcomes, evaluations, and usage history. If none is available, state that the audit is static and that behavioral effects remain unverified.
5. Separate symptoms from root causes and report every material finding supported by the audit; do not impose an arbitrary finding limit.
6. For each finding, include evidence, impact, confidence, affected surfaces, and a way to verify or falsify it. Keep importance and confidence as separate axes.
7. Compare local corrections with structural remedies. Preserve the required safety properties, and when replacing a guardrail, verify that the replacement provides equivalent or stronger protection. Keep diagnostic completeness separate from staged rollout.
8. Make the recommendation testable by comparing current guidance, no guidance, and the candidate in isolation and in coexistence with adjacent surfaces when relevant.

## Evaluation dimensions

Use the dimensions that matter to the intended behavior; they have no fixed priority order.

- **Outcome alignment:** whether the guidance produces the desired behavior and failure handling
- **Authority / precedence:** whether authoritative sources, overrides, and conflicts resolve as intended
- **Surface fit:** whether each instruction lives on a surface that the target client and user will actually load and understand
- **Triggering / coexistence:** whether relevant Skills or instructions activate precisely and behave correctly together
- **Correctness / freshness:** whether claims and client semantics are accurate and current
- **Safety / integrity:** whether required protections survive ambiguity, conflict, replacement, or bypass
- **Context cost:** whether always-loaded or triggered content earns its attention and token cost
- **Portability:** whether unsupported client, model, environment, or path assumptions are explicit
- **Maintainability:** whether ownership, duplication, coupling, and change paths remain understandable
- **Observability / evalability:** whether behavior can be traced, compared, and falsified with realistic evidence

## Reporting contract

Choose a structure appropriate to the audit instead of forcing fixed headings. Include:

- the conclusion and audit scope
- confirmed evidence and unconfirmed items
- findings and their root causes
- alternatives and trade-offs, including maintaining or removing guidance when plausible
- the recommendation, staged rollout, and validation method

Do not force a change when the evidence shows that current guidance is adequate.

## Boundaries

- Diagnose existing durable guidance. Use `design-skill` for new Skill design, `design-agent-instructions` for a new instruction document set, and `review-changes` for ordinary diff review.
- Exclude standalone Codex `.rules` command-policy review. Include `.rules` only when its approval behavior is a relevant surface in the wider guidance system.
- Keep the audit read-only by default. Edit only when the user's request authorizes changes and the target environment's applicable policy permits them; do not invent an additional universal approval gate.
- Do not treat the absence of a particular file, heading, or `Never` section as a defect without evidence that the intended behavior requires it.
- Do not assume a local patch is safer than a structural change. Evaluate both against the required safety properties and rollout risks.
