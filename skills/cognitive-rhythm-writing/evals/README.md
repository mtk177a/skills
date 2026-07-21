# cognitive-rhythm-writing evals

## Iter 0 — Static check

- the description and body consistently target pacing in explanatory Japanese
  writing
- the required `japanese-tech-writing` companion is named before the main
  procedure
- the missing-companion path stops application and provides one exact install
  command for both Skills
- the body distinguishes situation-updating prose from document-updating meta
  prose
- [critical] the executor must read the companion Skill before applying this
  Skill

## Scenarios

### Scenario A: Read the companion before revising

Both Skills are installed. The user asks the executor to revise a flat Japanese
technical chapter so that it has cognitive rhythm without losing necessary
context.

Requirements checklist:
1. [critical] Read `../japanese-tech-writing/SKILL.md` before applying this Skill
2. Preserve the companion Skill's Japanese technical-writing constraints
3. Add pacing only where the source situation provides material
4. Do not shorten away scope, comparison axes, or unresolved facts

### Scenario B: Stop when the companion is missing

Only `cognitive-rhythm-writing` is installed. The user asks for a rewrite.

Requirements checklist:
1. [critical] Stop without applying the writing rules
2. State that `japanese-tech-writing` is required
3. Provide exactly this installation command:
   `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing`
4. Do not produce a partial rewrite

### Scenario C: Avoid meta prose and leaked device names

The source is a flat Japanese explanation with enough data and conflicting
expectations to create pacing. The executor must revise it without narrating
the writing process.

Requirements checklist:
1. [critical] Do not add document-progress narration such as “next we examine”
   or “this section explains”
2. Do not expose device names such as “tension,” “recovery,” or “half the
   answer” in the resulting prose
3. Build changes from facts, data, reader inference, or the narrator's judgment
   state
4. Apply the topic test to newly introduced short sentences

## Failure Pattern Ledger

- `companion Skill not read before application`
- `partial rewrite produced when companion is missing`
- `exact pair-install command omitted or altered`
- `writing process narrated in the resulting prose`
- `device vocabulary leaked into the resulting prose`

## Iter 1 — not yet executed

Scenarios have not been executed. Execution results will be recorded here once
run.
