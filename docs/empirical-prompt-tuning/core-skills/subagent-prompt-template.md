This template is for running the methodology from mizchi's external `empirical-prompt-tuning` skill against local skills in this repo.

You are an executor reading a target skill set with a blank slate.

## Target prompt

Read the following skills in order:

1. `<path to first SKILL.md>`
2. `<path to second SKILL.md>`
3. `<path to third SKILL.md>`

## Scenario

`<one paragraph scenario>`

## Requirements checklist

1. [critical] `<minimum bar item>`
2. `<normal item>`
3. `<normal item>`
4. `<normal item>`

## Task

1. Follow the target skills to execute the scenario and produce the deliverable.
2. Do not assume undocumented policy unless the skill text forces you to.
3. On completion, respond with the report structure below.

## Report structure

- Deliverable: `<artifact or execution summary>`
- Requirement achievement:
  - `1. ○ | × | partial: <reason>`
  - `2. ○ | × | partial: <reason>`
  - `3. ○ | × | partial: <reason>`
  - `4. ○ | × | partial: <reason>`
- Trace:
  - Understanding: `OK | stuck | skipped` - `<reason if not OK>`
  - Planning: `OK | stuck | skipped` - `<reason if not OK>`
  - Execution: `OK | stuck | skipped` - `<reason if not OK>`
  - Formatting: `OK | stuck | skipped` - `<reason if not OK>`
- Unclear points (structured):
  - Issue: `<what observably happened>`
  - Cause: `<why, diagnosed at the instruction level>`
  - General Fix Rule: `<class-level rule>`
- Discretionary fill-ins:
  - `<decision you had to invent>`
- Retries: `<count and reason>`
