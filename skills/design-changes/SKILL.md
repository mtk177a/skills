---
name: design-changes
description: Designs how to make a code or configuration change before implementation, including the change boundary, the parts that stay unchanged, the risks, the decision points, and the verification. Use when the request is understood and the impact or trade-offs of the change need a plan.
license: MIT
---

# Design Changes

Make a plan that an implementer can follow without new decisions about scope, risk, or verification.\
The output is the plan, and the target files stay unchanged.

## Workflow

1. **Restate the target**

   State the expected behavior, the scope, the exclusions, and the constraints.\
   Done when the success condition and the exclusions are clear without a guess.\
   If they are not clear, stop and report what the user must clarify.

2. **Map the affected structure**

   Find the entry points, main branches, responsibility boundaries, and current checks that the change can affect.\
   Done when you can list each part that the change can affect.

3. **Set the change boundary**

   Find the smallest boundary that fully fixes the confirmed cause and meets the current requirements.\
   Derive it from the affected responsibilities, invariants, contracts, and known execution paths.\
   Then list the parts that stay unchanged, and the affected interfaces, modules, data, configuration, dependencies, and users of the code.\
   Done when each affected part is inside or outside the boundary, with a reason.

   Apply these rules to the boundary:

   - Keep the current public inputs, signatures, and call forms, unless current evidence requires a change.\
     A word such as "missing" can mean an existing value or a new call form.\
     Decide its meaning from the current contract and the callers.
   - Make code shared only when the evidence shows the same knowledge, responsibility, invariant, or contract.\
     Code that only looks similar can stay duplicated.

4. **Choose a local or a structural correction**

   Choose a local correction when it fixes the confirmed cause.\
   Choose a structural correction when a local correction does one of these:

   - leaves the confirmed cause
   - copies an existing rule
   - goes around an established responsibility boundary
   - makes known paths behave differently
   - needs a known follow-up correction

   For a structural correction, state these items:

   - why a local correction is not sufficient
   - what the structural correction restores
   - which contracts change, and what stays the same

   Compare with a structurally different alternative when uncertainty, coupling, or the cost of rework makes the comparison useful.\
   Done when the choice has a reason that the evidence supports.

5. **Justify new structure**

   For each new abstraction, dependency, configuration option, compatibility path, process, service, or deployment unit, record these items:

   - the current problem that it solves, and the evidence for the problem or for an agreed near-term requirement
   - the simpler alternative that you considered, and why it is not sufficient
   - the cost to maintain and operate it

   Keep the existing style and design unless a known failure needs a structural change.\
   Use a design principle only to solve a current problem with a responsibility, contract, interface, or dependency.\
   Put optional future improvements in a separate list.\
   Done when each new item has a current reason.

6. **Plan the risk handling**

   For each material risk, give a way to prevent, reduce, detect, recover from, compensate for, or contain it.\
   Some risks need controls before execution, beyond an ordinary implementation plan.\
   Examples are destructive operations, data migrations, security changes, changes to external state, and changes that cannot be undone.\
   For these risks, state that a separate readiness assessment is necessary, and list what it must settle.\
   Done when each material risk has a handling method or a readiness need.

7. **Plan the verification**

   For each changed responsibility, behavior, regression risk, and failure boundary, give a check and its expected evidence.\
   Select the depth of each check from its impact and uncertainty.\
   Examples are a static check, a focused regression test, and repeated measurement.\
   Use one check for several claims when it shows each claim clearly.\
   Done when each item has a check.

8. **Split the work**

   Split the work into small units that a person can review, aligned with behavior and responsibility.\
   For a readability change, split by processing stage and by what a reader understands together.\
   State the conditions to start, the scope of the implementation, and the conditions to stop.\
   List dependency additions, destructive operations, and open authority before implementation starts.\
   Done when each unit has a scope and an expected result.

9. **Prepare the reviewer context**

   Prepare these items for the implementer and the reviewer, and include only the items that apply:

   - the objective and the expected result
   - the product or operational context, and its criticality
   - the scope and the exclusions
   - the affected users, data, and contracts, and who can see the change
   - the constraints and the accepted trade-offs
   - the planned verification and the unknowns
   - the detection and recovery controls
   - the parts that the reviewer must examine carefully

   Mark missing criticality or exposure as `Unknown`, not as low risk.\
   Done when each applicable item has a value or `Unknown`.

## Report

Use a structure that suits the change, and include these items:

- the recommended approach, with its evidence, assumptions, and open questions
- what changes and what stays the same
- the reason for a local or a structural correction, when the choice matters
- the necessary current work, and the optional future improvements
- the dependencies, the affected boundaries and users, and the compatibility impact
- the material risks, each with its handling method
- the verification: each responsibility or risk, its possible failure, and the check with its expected evidence
- the reviewer context
- the conditions to start and to stop, the implementation scope, and the units of work

Add alternative designs, module maps, migration details, rollback, or explanation points for the user only when they matter.\
Label each planned check as not run.\
Leave open high-impact choices to the user.
