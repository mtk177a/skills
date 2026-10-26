---
name: explore-decision-space
description: Expands the options for a consequential, hard-to-reverse choice that has converged too early on one problem frame or one solution. Develops materially different problem frames or structurally different solutions, and narrows them only with explicit constraints and evidence. Use before such a choice, or when the current approach is exhausted.
license: MIT
---

# Explore Decision Space

Keep a consequential decision from closing too early on one problem frame or one solution.\
Expand the part of the decision that is still open, and narrow it only when evidence supports it.\
The output is the exploration, and the files stay unchanged.

## Workflow

1. **Restate the decision**

   State the objective, the confirmed constraints, the current anchor, and the decision criteria.\
   The anchor is the problem frame or the solution that the work currently assumes.\
   Collect the affected users or systems, the success criteria, the exclusions, the authority, and the reversibility.\
   Collect the alternatives already considered, and why they were kept or rejected.\
   Treat a supplied frame, favorite option, score, or earlier conclusion as one candidate, even when it is detailed.\
   Keep confirmed constraints, and keep disputed assumptions open.

2. **Find the open layer**

   Choose the layer of the decision that is still open:

   - `Problem space`: the problem, its causes, its boundary, the needs of the stakeholders, or the definition of success is not settled.
   - `Solution space`: the problem frame is settled, but the approaches depend on one mechanism or one design area.
   - `Both`: the current solution depends on a problem frame that is not settled.\
     Explore the problem frames first.
   - `No expansion needed`: the decision is small, easy to reverse, or already has sufficient alternatives and evidence.

   If missing intent, authority, terms, evidence, or a diagnosis prevents a valid exploration, stop with the state `Blocked`.\
   Name what is missing.\
   Done when the open layer has a reason.

3. **Develop the problem frames**

   For `Problem space` or `Both`, find the axes that can change the meaning or the boundary of the problem.\
   Develop frames that differ in substance, not only in wording.\
   For each frame, state these items:

   - what it treats as the problem
   - the evidence for and against it
   - what it keeps and what it excludes
   - the observation that can distinguish it from the other frames

   Then mark each frame as supported, conditionally selected, needs evidence, or needs a user judgment.\
   Expand solutions only after one frame is supported or selected.

4. **Develop the solutions**

   For `Solution space`, find the axes that change the structure of the solution.\
   Examples are the mechanism, responsibility boundary, state representation, processing order, tool boundary, and operational model.\
   Develop structurally different options until the material axes and trade-offs of the decision are covered.

5. **Compare**

   Compare the frames or options against explicit criteria.\
   Keep observed performance separate from predicted properties.\
   Mark a comparison that is not available as `unknown`.

6. **Narrow or stop**

   Narrow the options when evidence, constraints, or a preference that the user authorized supports one.\
   Otherwise, return the evidence, decision, or experiment that can distinguish them.\
   Select a winner only when the evidence supports it.\
   Done when you choose one state from [States](#states).

## States

- `No expansion needed`: more options would not improve the decision.\
  State why.
- `Problem frames ready`: different problem frames and the conditions that distinguish them are clear, but the selection needs evidence or a judgment of the user.
- `Options ready`: the problem frame and structurally different solutions are clear, but the selection needs evidence or a judgment of the user.
- `Evidence needed`: a specific observation or comparison can distinguish the frames or options.
- `Selected for design`: one frame and one option have enough support to go to implementation design.\
  Keep the reason for the selection and the rejected alternatives.
- `Blocked`: missing intent, authority, safety margin, or necessary context prevents a valid exploration.

## Report

Include these items:

- the state, and the open layer: problem space, solution space, both, or neither
- the objective, the confirmed constraints, the current anchor, and the decision criteria
- the observed facts, reported results, assumptions, inferences, and unknowns that affect the choice
- the axes, and the different problem frames or solutions
- for each frame or option, its structural difference, the evidence for and against it, its conditions, its trade-offs, and the status of its evidence
- the basis of the comparison, the rejected alternatives worth keeping, and the open value judgments
- the next step: the supported selection, the distinguishing evidence, or the decision of the user
