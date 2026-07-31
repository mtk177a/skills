# Repository Document Kinds

Choose a document by the reader's question, not by a fixed repository template.
Create only the documents that have a maintained reader need.

## README

**Reader question:** What is this repository, can I use it, how do I start, and where is the detailed documentation?

Include the repository's purpose, audience, status when material, shortest supported start or verification path, common entry commands, and descriptive links to canonical detail.

Exclude complete API references, long architecture explanations, full runbooks, decision history, and duplicated generated information.

Use the current project entry points, executable tasks, CI configuration, and canonical detail pages as evidence.
Update the README when the initial user or contributor path changes.
Validate its commands, links, and stated status.

## How-to guide

**Reader question:** How do I accomplish one specific task?

Include the outcome, prerequisites, ordered actions, expected results, completion check, and only the troubleshooting or cleanup needed for that task.

Exclude a complete conceptual introduction, design history, unrelated alternatives, and exhaustive reference listings.

Use executable commands, configuration, tests, and an accepted operating method as evidence.
Human authority is required for business policy, permissions, and unsafe operational choices.
Update the guide when the task entry point, preconditions, commands, or success criteria change.
Validate the procedure in a representative environment when practical.

## Runbook

**Reader question:** How does an operator detect, contain, diagnose, recover from, and verify a known operational condition?

Include triggers, scope, prerequisites, safe checks, decision points, expected observations, escalation or ownership when established, recovery or compensation, completion criteria, and post-action verification.

Exclude speculative commands, invented owners, unsupported rollback, and general architecture education.

Use tested operational procedures, monitoring definitions, deployment configuration, incident evidence, and authorized operational policy.
Human authority is required for risk acceptance, destructive action, access, escalation, and recovery policy.
Update the runbook when alerts, controls, commands, dependencies, or recovery behavior change.
Validate in a safe environment or record why execution was not possible.

## Architecture

**Reader question:** What is the current system structure, responsibility, boundary, dependency, and important runtime behavior?

Include scope, system context, components and responsibilities, interfaces, important flows, external dependencies, trust boundaries, and relevant failure behavior.

Exclude historical debate, proposed future design presented as current, class-by-class narration, and full generated contracts.

Use deployed configuration, code, schemas, tests, and accepted current documentation as evidence.
Do not infer why the architecture was chosen.
Update the document when current boundaries, responsibilities, dependencies, or major flows change.
Validate each material element and relationship against its canonical source.

## Reference

**Reader question:** What exact value, option, contract, type, default, or constraint applies?

Include complete and consistently ordered facts needed for lookup, including units, defaults, allowed values, exceptions, and precise identifiers.

Exclude persuasive background, decision history, and manually copied data that can be generated reliably.

Prefer schemas, source definitions, command help, OpenAPI, database definitions, and generated artifacts as canonical evidence.
Update or regenerate the reference when its source changes.
Validate generation, schema consistency, and links.
Do not hand-edit a generated output unless its documented workflow requires it.

## Current behavior

**Reader question:** What does the system currently do, including undefined or conflicting behavior?

State that the document is descriptive, not normative.
Record the examined revision or commit when practical.
Include observed inputs, outputs, conditions, errors, edge behavior, and the implementation locations needed for maintenance.
Separate verified behavior, inference, and unknowns.

Exclude claims about intended behavior, business correctness, design rationale, or future guarantees unless an authorized source establishes them.

Use code, tests, schemas, reproducible execution, and production observations that are safe and authorized.
Update the document when the described behavior changes or a previously unknown condition is resolved.
Validate representative scenarios and preserve untested cases as unknown.

## ADR

**Reader question:** What significant decision was made, why was it made, what alternatives mattered, and what consequences were accepted?

Include status, context, decision drivers, considered alternatives, the decision, positive and negative consequences, and links to superseding decisions.

Exclude a broad feature design, current architecture catalog, reconstructed rationale based only on code, and later conclusions rewritten into an accepted record.

Use the authorized decision and the evidence available when it was made.
Accepted ADRs remain historical records.
Replace a changed decision with a new ADR and mark the old one superseded rather than rewriting its conclusion.
Validate status and cross-links.
A person with decision authority must confirm the decision and rationale.

## Design Doc or RFC

**Reader question:** What problem and decisions require review before implementation, and why is the proposed design preferable under the stated constraints?

Include the review decision requested, context, problem, goals, non-goals, constraints, assumptions, prioritized criteria, proposed design, important runtime and failure scenarios, alternatives, trade-offs, risks, rollout, verification, rollback or compensation, and open questions that are material to the proposal.

Include only sections that affect the actual design.
Do not copy full generated API, schema, or implementation definitions.

Use verified current-state evidence and explicit product, operational, security, and engineering decisions.
The document may propose choices, but an authorized review must decide them.
Keep it current through implementation when decisions change; after release, move current truth to Architecture or Reference documents and retain the Design Doc as decision context.

## Evidence basis

- [Diátaxis](https://diataxis.fr/)
- [AWS: Architectural decision records](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/)
- [arc42 template overview](https://arc42.org/overview)
- [C4 model diagram review checklist](https://c4model.com/diagrams/checklist)
