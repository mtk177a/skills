---
name: design-agent-instructions
description: Designs a new or reorganized set of durable instruction documents for the agent clients that a repository actually uses. Decides the source of truth, the loading and precedence relations, the shared and client-specific guidance, and the necessary companion files. Use before editing such a set.
license: MIT
---

# Design Agent Instructions

Design the smallest set of instruction documents that reaches the intended clients with clear authority and little duplication.\
Base the role of each document on verified client semantics and on the needs of the repository.\
The output is a design, and the instruction files stay unchanged.

## Workflow

1. **Define the target**

   Define the intended behavior, the scope, the active users, clients, and models, and what must be shared or client-specific.\
   If the request starts from unexplained behavior, and the loading or the authority of the current guidance is uncertain, stop.\
   Report that a diagnosis is necessary first, and name the missing evidence.

2. **Review the current set**

   Review the existing instruction documents, client configuration, imports, rules, hooks, policy surfaces, and project documentation.\
   Collect the observed loading evidence, traces, corrections, or failures, and the local policy and authorization boundaries.\
   Separate observed evidence, inferences, assumptions, and unknowns.\
   Evaluate a missing standard filename against the needs of the active clients.

3. **Verify the client semantics**

   For each target client, verify and record its loading, discovery, precedence, import, and enforcement semantics.\
   Use the current official documentation of the client.\
   Record each client separately, because the hierarchy of one client can differ from another.\
   Treat instruction documents as context that guides behavior.\
   Treat them as enforcement only when the current client semantics state it.

4. **Choose the source of truth**

   Choose one source of truth for each shared fact or rule.\
   Use imports, references, or generated views only when the target client supports them, and they reduce drift without hiding authority.

5. **Separate guidance from enforcement**

   Separate durable behavioral guidance from enforced permissions and lifecycle automation.\
   When a guarantee is required and the client provides policy, settings, or hooks, put the guarantee there.

6. **Decide the content of always-loaded files**

   A file that the client loads in every session costs context in every session.\
   Put in it only content that meets both of these conditions:

   - The agent needs it in most tasks.
   - The agent cannot find it cheaply by itself.\
     Examples are an unwritten convention, the reason for a choice, and a hard guardrail.

   Point to the facts that the agent can look up, such as commands, the directory layout, and configuration.\
   Copy such a fact only when the lookup is expensive.\
   Write the content as positive instructions, and keep prohibitions for hard guardrails, each with the wanted behavior next to it.\
   Put guidance for one kind of task in a document that the agent reads for that task.

7. **Decide the documents**

   Decide which documents and configuration surfaces are necessary.\
   Add a client-specific companion only when that client is in active use and cannot read the source of truth directly.\
   Define what each surface contains and what it leaves to other surfaces.\
   Keep general project facts in ordinary documentation, unless they must be in the context of the agent.\
   Keep secrets, credentials, personal information, and private operational data out of templates and examples.

8. **Check the set**

   Check the set for duplication, contradictions, context cost, portability, ownership, and update paths.\
   When they apply, check the behavior after compaction or lazy loading.\
   Compare the proposed set with three alternatives: the current set, the current set without redundant guidance, and a smaller bridge document.

9. **Plan the verification**

   Define the verification from the material risks:

   - whether each client loads the intended documents
   - conflicts of precedence
   - adherence to the instructions
   - the boundaries of enforcement
   - coexistence across the active clients

10. **Prepare the handoff**

    Prepare a scoped handoff for implementation.\
    File changes belong to an authorized implementation workflow.

## Report

Use a structure that suits the decision, and include these items:

- the recommended set of documents, and why it is better than the alternatives
- the intended behavior, the scope, the active clients, and the open assumptions
- the verified loading, discovery, precedence, import, and enforcement semantics of each client
- the sources of truth, and the responsibility of each surface
- the content of each always-loaded file, and where the other content goes
- the documents or surfaces that the design leaves out, and why
- the risks of duplication, context cost, portability, maintenance, and migration
- the verification, and the units of change for implementation
- a handoff for diagnosis, with the missing evidence, when unresolved behavior prevents a sound design

Add a companion document, a fixed filename, or a fixed heading template only when the clients or repository need it.\
If the behavior is not confirmed, name the diagnostic evidence that is necessary, and present the design as a hypothesis.
