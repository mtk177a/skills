---
name: define-referents
description: Defines what new or ambiguous terms refer to, with their semantic roles, relationships, and naming constraints, before a term merges distinct concepts in a design, investigation, explanation, or identifier. Returns a referent table and a naming table to the work that continues. Use when terminology can distort later reasoning, or when the user asks for a referent table.
license: MIT
---

# Define Referents

Connect each material term to a concrete referent, its role, and its relationships, and only then propose a name.\
This keeps a fluent label from hiding different conditions, states, events, values, records, purposes, means, or entities.\
The output is two tables and a state.\
The originating work continues the design, investigation, writing, or implementation.

Read [references/referents-before-labels.md](references/referents-before-labels.md) completely each time you use this Skill.\
Use it for the semantic decisions, and use `SKILL.md` for the steps and the output.

## Workflow

1. **Select the terms**

   Select only the terms that are new, or that are reused with a broader or ambiguous meaning.\
   Select a term only when its meaning can change later reasoning.\
   Reuse an established term with its established meaning.

2. **Check the source**

   Collect the source requirement, observation, evidence, or reasoning, and the document, design, or identifier that will use the terms.\
   Collect the established domain terms and their authoritative sources.\
   Use safe, read-only inspection to find facts when the target and the scope are clear.\
   Done when the source can distinguish the referents and their relationships.\
   If a material fact is missing, ask a focused question, or stop with the state `Blocked`.

3. **Create the grounding table**

   Create the [grounding table](#grounding-table) with concrete wording only.\
   Write candidate terms only in the naming table, after step 4.\
   Done when each relevant referent has a row.

4. **Check the grounding table**

   Check each row without its label:

   - The row names a concrete referent.
   - The row states the current semantic role of the referent.
   - The row shows the place of the referent in the reasoning.
   - The row records the uncertainty.

   Done when each row passes these checks.

5. **Create the naming table**

   Create the [naming table](#naming-table).\
   Use an established term or a term from the user first.\
   If no precise term makes the concrete wording shorter without a change to its boundary, use `concrete wording`.\
   Then hide the naming table, and check that the grounding table is still clear alone.

6. **Choose the state**

   - `Ready`: the mapping and the naming constraints are clear enough for the originating work to continue.\
     When only a small, local, reversible naming choice remains, choose `Ready` without asking the user.
   - `Decision required`: different mappings or terms lead to different public contracts or domain boundaries.\
     Show the grounded alternatives, and ask the question that decides between them.
   - `Blocked`: the evidence, information, or authority to ground a referent is not available.

7. **Return the result**

   For a direct naming request, return the tables and the state as the result.\
   For a larger task, return them as a handoff, so that the originating work can continue.

8. **Handle corrections**

   If a row of the grounding table changes, mark each dependent row of the naming table as invalid.\
   Revise the grounding, and create the naming proposal again only for the affected rows.\
   Keep the content that the user or a later step wrote.

## Grounding table

Use this column order:

| ID | Source | Purpose | Concrete referent | Semantic role | Sequence / relationship | Uncertainty |
| --- | --- | --- | --- | --- | --- | --- |

- Use stable IDs, such as `R1`.\
  An ID only connects the two tables, and it is not a domain term.
- State what the referent is, not a proposed label.
- Describe the semantic role in the current explanation or design.\
  The roles in the reference are examples, so use a more precise role when the context needs it.
- Use separate rows when one label would hide different referents or different roles.\
  Keep one row for one referent, even when it has several relationships.
- Keep the order of reasoning and the uncertainty that the user supplied.
- Record the uncertainty as `confirmed`, `inferred`, `assumed`, or `unknown`, with a short reason when it is not obvious.
- Split the table only when the purposes or reasoning stages are separate, or when the table is too large to review.

## Naming table

| ID | Candidate term | Status | First-use definition |
| --- | --- | --- | --- |

- Use the ID from the grounding table, so that each name maps to one referent.
- Use `established`, `proposed`, `concrete wording`, or `decision required` for `Status`.
- Define each proposed term as "X means ...".\
  For an established term, mark it as established, and keep its authoritative mapping.
- Give several alternatives for one ID only in the state `Decision required`, and state the semantic trade-off of each one.
- Read each candidate term alone.\
  It must not also be a true name for another row whose difference matters.

## Report

- Start with `State: Ready`, `State: Decision required`, or `State: Blocked`.
- Include the grounding table when the grounding is complete enough.\
  Include the naming table only after the grounding table passes its checks.
- For `Decision required`, give the open semantic choice, its effect on the public contract or domain boundary, and the question for the user.
- For `Blocked`, give the missing evidence or information, the open mapping, and what can unblock it.
- Return the tables in the response.\
  Create a separate file for the tables only when the user asks for that file.\
  Permission to write the target document does not include this extra file.
- The order of the two tables shows that the grounding came first.
