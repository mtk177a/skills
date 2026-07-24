---
name: audit-agent-guidance
description: Audits durable agent guidance—including AGENTS.md, CLAUDE.md, SKILL.md, and agent-facing references—against intended behavior, observed usage, client semantics, and evaluation evidence. Use when diagnosing guidance scope, precedence, trigger conflicts, safety or third-party trust boundaries, context cost, or systemic failures before revision; not for ordinary code or script vulnerability review, new Skill authoring, or standalone Codex `.rules` policy review.
license: MIT
---

# Audit Agent Guidance

## Objective

- Diagnose whether durable agent guidance produces the intended behavior and explain why it succeeds or fails.
- Treat "agent guidance" as an umbrella term for durable instructions, reusable workflows, and agent-facing references.
- Audit either one existing Skill or a guidance system spanning multiple surfaces.
- State the expected behavior in one sentence before inspecting current artifacts, and do not assume the current artifact or document split is correct.

## Evidence and scope

- Define the intended behavior, failure signals, users, client, and model before naming target files.
- Distinguish observed evidence, reasonable inference, assumptions, and unknowns.
- Discover relevant instruction documents, Skills, references, policy files, client configuration, and distribution metadata. Record their authority, scope, loading order, precedence, triggers, coexistence, permissions, and delivery path when material.
- When third-party content or executable capabilities are involved, inventory every distributed and directly referenced file, provenance, actual remote destinations, scripts, dependencies, tools, filesystem and network access, and possible outbound data flow. Evaluate the combined capability chain rather than isolated permissions.
- Check current official client semantics when loading, precedence, approval, or Skill-discovery behavior is material and not established by local primary sources.
- Prefer traces, execution results, evaluations, and usage history over textual plausibility. When behavioral evidence is unavailable, label the work as a static audit and leave behavior unconfirmed.
- Before expanding evaluation, map each material guidance claim or proposed change to a plausible failure, a scenario or check that can expose it, and a grading method. Use scenario count and repetition only when they add decision-relevant evidence.

## Workflow

1. Write a one-sentence expected behavior, then define failure signals, affected users, and the relevant client and model before referring to an artifact name.
2. Restate the problem, surface hidden assumptions, and consider causes at other layers. Test counterfactuals that keep, remove, move, merge, or replace the current guidance.
3. Discover the relevant guidance surfaces, authority and permission boundaries, loading and precedence rules, triggers, coexistence behavior, and distribution paths. For third-party or executable Skills, trace provenance, external instructions and redirects, commands and tools, data access, outbound destinations, and the controls that constrain the full capability chain. Verify current official client semantics when they materially affect the diagnosis.
4. Gather behavioral evidence such as traces, outcomes, evaluations, and usage history. If none is available, state that the audit is static and that behavioral effects remain unverified.
5. Separate symptoms from root causes and report every material finding supported by the audit; do not impose an arbitrary finding limit.
6. Use a complete record for every material finding: evidence, impact, confidence, affected surfaces, and a way to verify or falsify it. Do not leave a field implicit or provide it only in an aggregate validation section. Keep importance and confidence as separate axes.
7. Compare local corrections with structural remedies. Preserve the required safety properties, and when replacing a guardrail, verify that the replacement provides equivalent or stronger protection. Keep diagnostic completeness separate from staged rollout.
8. Make the recommendation testable with evaluation proportional to the risk and uncertainty. Compare current guidance, no guidance, and the candidate in isolation or coexistence only when those conditions can distinguish a material failure.

## Evaluation dimensions

Use the dimensions that matter to the intended behavior; they have no fixed priority order.

- **Outcome alignment:** whether the guidance produces the desired behavior and failure handling
- **Authority / precedence:** whether authoritative sources, overrides, and conflicts resolve as intended
- **Surface fit:** whether each instruction lives on a surface that the target client and user will actually load and understand
- **Triggering / coexistence:** whether relevant Skills or instructions activate precisely and behave correctly together
- **Correctness / freshness:** whether claims and client semantics are accurate and current
- **Safety / integrity:** whether required protections survive ambiguity, conflict, replacement, bypass, untrusted external instructions, or combined data-access and outbound capabilities
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
- the recommendation and validation method, plus a staged rollout when a change is recommended

For a third-party or executable Skill finding, identify the trust boundary, relevant capability and data path, destination, and deterministic control or missing control. Do not reduce a combined risk to a list of individually acceptable permissions.

Do not force a change when the evidence shows that current guidance is adequate.

## Boundaries

- Diagnose existing durable guidance. Use `design-skill` for new or substantially rescoped Skill design, `design-agent-instructions` for a new instruction set or post-diagnosis reorganization, and `review-changes` for ordinary diff review.
- Include script and tool behavior when it forms part of the Skill's instruction, trust, or data-flow boundary. Route a standalone implementation vulnerability review to the appropriate code or security review workflow instead of expanding this audit into general code analysis.
- Exclude standalone Codex `.rules` command-policy review. Include `.rules` only when its approval behavior is a relevant surface in the wider guidance system.
- Keep the audit read-only by default. Edit only when the user's request authorizes changes and the target environment's applicable policy permits them; do not invent an additional universal approval gate.
- Do not treat the absence of a particular file, heading, or `Never` section as a defect without evidence that the intended behavior requires it.
- Do not assume a local patch is safer than a structural change. Evaluate both against the required safety properties and rollout risks.
- Do not treat a fixed number of findings, scenarios, or runs as proof of completeness. Stop when material claims and failure boundaries are covered and further evidence would not change the decision.
