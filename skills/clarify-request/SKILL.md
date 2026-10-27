---
name: clarify-request
description: Aligns with the user on the intent and meaning of a request, resolves the gaps that can change later work, and returns an agreed request or a handoff for the next step. Use when the user asks to clarify, scope, or organize a request, or to check that you understand it, and when a missing purpose, success criterion, constraint, environment, or authority can change the work.
license: MIT
---

# Clarify Request

Agree with the user on what the request means and what result it needs.\
Clarify over several turns, and ask only about what can change the next action.

## Clarification cycle

1. **Restate the request**

   State briefly how you understand the intent, the expected result, and the material uncertainty.\
   Identify what the user wants from the clarification:

   - only an agreed understanding
   - a handoff for a next step, such as design or implementation
   - a clarification inside a task that is already authorized

   Done when the user can correct your understanding, and you know which of the three results to return.\
   If the request is already clear, restate it and finish with the state `Ready`.

2. **Update the clarification record**

   Add the latest answer of the user to a record with these parts:

   - confirmed facts from the user or from authoritative sources
   - inferences, with their evidence
   - working assumptions
   - open questions and contradictions
   - missing authorization or risk acceptance

   Record only information from the user or from an authoritative source as confirmed.\
   Record a value that exists but is not known as `unknown`, and a choice that nobody made as `undecided`.\
   If a new answer clearly replaces an earlier condition, record it as a correction.\
   If a new answer conflicts with earlier information, show the conflict to the user.\
   Keep each open gap from earlier turns in the record until it is resolved.\
   Done when every answer is in the record.

3. **Find the gaps**

   Find the gaps that can change one of these:

   - the result, the completion criteria, the scope, or the exclusions
   - the constraints, the environment, or the external effects
   - the authority, the risk, or the verification

   Use safe, read-only inspection to find facts when the target and the scope of the inspection are clear.\
   A gap is material only when the next step must guess intent, authority, or risk acceptance to resolve it.\
   Give each gap one class:

   - **Blocking**: it can change the work, or it needs information, authorization, or risk acceptance that only the user can give.
   - **Assumable**: it is small, local, and reversible, and a convention or evidence supports one answer.
   - **Not relevant now**: it does not affect the next step.

   Done when each gap has a class.

4. **Resolve the gaps**

   For a blocking gap, first check if the next step can resolve it with evidence and user criteria.\
   If it can, keep the gap as an open input for that step.\
   If it cannot, ask the questions that resolve the gap, and say briefly why each answer matters.\
   For an assumable gap, state the assumption, its reason, the affected scope, and the condition to revisit it.\
   Continue safe work that does not depend on the answer.

5. **Repeat after each answer**

   After each answer, go back to step 2.\
   If an answer is partial, ask a narrower question about the part that is still open.\
   Done when another exchange cannot change the state of the request.

6. **Finish in one state**

   - `Ready`: the understanding is agreed, and a requested handoff has what the next step needs to start.\
     The next step can still have facts to investigate and decisions to make within its own authority.
   - `Proceed with assumptions`: only stated, small assumptions remain.
   - `Blocked`: a material gap remains, because the user cannot answer, does not decide, or the necessary authority is not available.

## What a handoff needs

- **For design**: the confirmed result, the success boundary, the scope, the exclusions, the constraints, and the authority to design.\
  Leave the structure, the files, the dependencies, the data mapping, and the verification design to the design step.\
  Do this only when the user gave the criteria for those decisions.
- **For implementation**: the approach, the authorized scope, the exclusions, the risk decisions, and a way to verify the result.\
  Send the request to design first if a design choice is still open.

Ask the user to reconcile requirements that conflict.\
If the request has several goals, keep them together.\
Propose to separate them only when together they change the scope, the order, the authorization, or the review.\
Offer options only when they show real choices.\
Give a recommendation only when evidence, an established default, or stated trade-offs support it.\
If the user asks to continue with open gaps, use assumptions only for assumable gaps.\
Report blocking gaps as `Blocked`.

## Report

- **Understanding check**: start with a short restatement of the request.\
  Show the understood intent separately from the uncertainty, and ask only what the clarification needs.\
  When the understanding is agreed, return the agreed request in a form that a reader can use alone.\
  Say that the clarification is complete.

- **Questions**: give the open point, its effect on the next action, the question, and useful options or trade-offs.\
  Say which next action waits for the answer when that is not clear.

- **Assumptions**: for each assumption, give its reason, the affected scope, and the condition to revisit it.

- **Handoff**: include these items, and omit empty items:

  - the confirmed result
  - the background or reasons that the next step needs to understand the request or to compare trade-offs
  - the success or completion criteria
  - the scope, the exclusions, and the constraints
  - the assumptions, the open items, and the missing authority
  - the next action

  After a clarification of several turns, restate all confirmed information in the handoff, not only the latest change.\
  Keep likely implementation results, general best practices, and design ideas as open inputs for the next step, not as requirements.\
  Show which information is confirmed and which is inferred.

- **Blocked**: give the open gap, the missing evidence or decision, the unchanged parts, and what can unblock the request.\
  Ask the same question again only with new information.

After a request for clarification only, finish with the agreed request, and wait for the next instruction of the user.\
When the clarification happens inside an authorized task, return to that task with its existing scope and authority.
