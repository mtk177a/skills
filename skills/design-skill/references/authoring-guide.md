# Portable Skill Authoring Guide

Use this reference as a design baseline for any repository.\
Find the local instructions that apply, and let them govern their own scope.\
This guide fills the gaps that local instructions leave.

## Design the discovery metadata

The Agent Skills format requires a `SKILL.md` with `name` and `description`.\
Local policy can require more metadata.

- Keep `name` the same as the directory name, and within the syntax that the target clients support.
- Use a specific name, such as an action and an object.
- Put what the Skill does and when it applies in `description`.
- Write `description` in the third person, because the client adds it to the system prompt.
- Put the main use case and trigger terms first, so that a client that shortens the text keeps them.
- Write only when to use the Skill.\
  If two Skills trigger on the same requests, make the trigger of each Skill more specific.
- Keep execution details in the body, unless the trigger needs them.

The client normally selects a Skill from its metadata before it loads the body.\
For this reason, the body cannot repair a missing trigger.

## Write the body

- Keep only text that changes the behavior of the agent.\
  Delete a sentence that tells the model what it already does.
- Match the freedom of the instructions to the task.\
  Give goals and criteria when several approaches are valid, and exact steps when an operation is fragile.
- End each step with a completion criterion that the agent can check.
- State the behavior that you want.\
  Use a prohibition only for a hard guardrail that has no positive form.\
  Put the wanted behavior next to the prohibition.
- Put each rule in the step where the agent applies it.
- Use terms that the model already knows, and use one term for one concept.
- Point to facts that the agent can find in the repository, instead of copying them.

## Separate portable and client-specific layers

Keep the standard `name`, `description`, instructions, and bundled resources as the portable layer.\
Add the metadata or configuration of a client only when the target workflow needs one of these:

- explicit or implicit invocation control
- UI presentation
- declarations of tools or dependencies
- permission, sandbox, hook, or execution-context behavior

Add only the extensions that the workflow needs.\
List the extensions for each client separately in the implementation handoff, and keep the portable metadata to the common contract.\
If a client format requires an extension in the same `SKILL.md`, label the field with its target client.\
Then verify that the other intended clients accept it.\
Verify the current semantics of a client before you depend on an extension, and document the supported target.\
Keep the core responsibility usable without unrelated client metadata.

Make a portable Skill work alone, without unnamed external documents or companion Skills.\
For a Skill that is intentionally specific to one project, state the dependency and the environment.

## Review third-party and executable capabilities

When a design adopts or adapts third-party material, record these items:

- the upstream source and the pinned revision
- the license
- the complete set of files
- the local modifications
- the update path

Inspect each distributed file and each directly referenced file.\
The main Markdown file alone does not show that a Skill is safe.

When instructions can lead to scripts, tools, file system access, credentials, network access, or external content, trace the complete path.\
The path goes from the input, through data access, to a side effect or an outbound destination.\
Examine combined capabilities carefully, such as these:

- file reads together with network sends
- untrusted documents together with privileged tools
- automatic invocation together with destructive actions

Use the least authority and the smallest data scope that the responsibility needs.\
For a hard guarantee, use a permission, sandbox, hook, or CI control when the client provides it.\
If you cannot establish the provenance, the executable behavior, or the outbound data flow, reject the design.\
As an alternative, mark it as not verified.

## Sources

This guide summarizes these sources, and they remain the authority:

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices)
- [OpenAI Build skills guide](https://learn.chatgpt.com/docs/build-skills)
- [Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic enterprise Skill review guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise)
- [`writing-for-agents` by Matt Pocock](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
- [`authoring-a-skill` playbook in pstack](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md)
