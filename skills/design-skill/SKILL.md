---
name: design-skill
description: Designs whether and how to create, merge, split, or substantially rescope an Agent Skill before implementation. Defines the responsibility, the trigger, and the reusable resources of the Skill. Use when a recurring gap in agent behavior may need a new or changed Skill.
license: MIT
---

# Design Skill

Decide whether a reusable Skill is the right intervention, before anyone drafts one.\
Produce a design, based on evidence, that an implementer can apply without new decisions about the responsibility, trigger, or resources.\
The output is the design, and the Skill files stay unchanged.\
An existing audit can supply evidence, and this Skill also works without one.

Read the sections of [references/authoring-guide.md](references/authoring-guide.md) that apply to the design:

- **Design the discovery metadata**: when you draft or revise `name` and `description`
- **Write the body**: when you plan the content of `SKILL.md`
- **Separate portable and client-specific layers**: when the design needs client metadata or controls
- **Review third-party and executable capabilities**: when the design adapts third-party material or includes executable resources

The local instructions that apply have authority within their scope.\
Use the bundled guide where the local instructions say nothing.

## Workflow

1. **Define the gap**

   Define the intended capability, and the recurring failure or knowledge gap.\
   Collect the intended outcome, the users, clients, and models, and the failure signals.\
   Treat a new Skill as one possible answer, not as the starting point.

2. **Examine the baseline**

   Examine representative tasks, corrections, traces, or outputs, and the behavior without a Skill or with the previous version.\
   Identify what the agent lacks, what it already does well, and which corrections can be reused.\
   Separate observed evidence, inferences, assumptions, and unknowns.\
   If only textual plausibility is available, label the design as a static hypothesis.\
   Done when you can state the gap with evidence, or state that the evidence is not available.

3. **Compare the interventions**

   Compare these interventions:

   - no durable guidance
   - a local instruction or a tool
   - an update or a merge of an existing Skill
   - a split of an existing Skill
   - a new Skill

   Apply these criteria:

   - Choose no Skill when the model already does the task reliably, and no reusable context or procedure is missing.
   - Choose an update or a merge when the trigger, the output, and the risk boundary stay coherent.
   - Choose a new Skill or a split when one Skill with both responsibilities would make triggering, loading, or execution ambiguous.

4. **Inspect the neighbors**

   Inspect the adjacent Skills, their descriptions, and how they work together.\
   Inspect the distribution surfaces and the local instructions.\
   Resolve overlap of responsibility, competing triggers, context cost, and coexistence risks.\
   For third-party or executable material, also resolve the provenance, the license, the complete file inventory, and the capability paths.\
   Done when the chosen intervention has no unresolved overlap or trust boundary.

5. **Define the responsibility**

   Choose one coherent responsibility.\
   Define its users, the tasks in scope, the inputs, the outputs, and the failure handling.

6. **Draft the metadata**

   Draft `name` and `description` with the guide.\
   Put the full trigger context in `description`.\
   Make the trigger specific enough that it does not compete with the triggers of the adjacent Skills.

7. **Allocate the content**

   Put only reusable content that the agent does not already have in `SKILL.md`, `references/`, `scripts/`, and `assets/`.\
   Bundle references or scripts only when they save repeated discovery, give domain evidence, or make a fragile operation verifiable.\
   Keep `SKILL.md` short enough that each loaded section is worth its context cost.\
   Plan each step with a completion criterion, and put each rule in the step that applies it.\
   Match the freedom of the instructions to the fragility of the task.\
   Keep the portable metadata to the common contract, and list the client-specific additions separately.

8. **Define the safety boundaries**

   Define safety or permission boundaries only where the workflow needs them.\
   When external instructions, scripts, tools, or file system or network access are involved, trace the combined path.\
   Move hard guarantees to client controls that can enforce them, when the client provides such controls.

9. **Prepare the handoff**

   Identify the surfaces that the design actually affects.\
   Prepare a handoff for implementation, with the checks for retained code, structure, and safety.

## Report

Use a structure that suits the decision, and include these items:

- the recommended intervention, and why it is better than the alternatives
- the evidence, the assumptions, and the open questions
- the responsibility and the trigger
- the metadata draft, when a Skill is recommended
- the allocation of content and resources
- the portable metadata and content, and the separate client-specific additions
- the provenance requirements for third-party material
- the safety, data-flow, and permission properties that the implementation must keep
- the checks for the result, and the rollout strategy
- the affected surfaces, and the handoff for implementation

When the evidence supports no durable guidance or a different intervention, recommend that instead of a Skill.\
File changes, new dependencies, and changes to repository policy belong to an authorized implementation workflow.
