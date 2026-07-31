# Repository Documentation Writing

Use these rules when drafting or editing documentation that is versioned with a codebase.
Optimize for task completion, factual accuracy, safe operation, and future maintenance rather than literary completeness.

## Define the reader and task

Write for one primary audience and one primary reading task per document.
Identify what the reader already knows, what they need to do or understand, and what the document deliberately excludes.

Do not add background merely because it was useful during investigation.
Include background only when the reader needs it to choose, perform, verify, or safely undo an action.

## Lead with orientation or action

- For an entry document, state what the repository provides before its history.
- For a procedure, state the result and prerequisites before the steps.
- For a decision record, state the decision before its detailed rationale.
- For an explanation, establish the system boundary and overview before details.

Keep causal links, conditions, exceptions, and constraints even when shortening.
A shorter document is not better if the reader must reconstruct the logic.

## Make structure discoverable

Use one page title and a valid heading hierarchy.
Make headings predict the information below them.

Prefer:

- `Start the local API`
- `Retry a failed customer job`
- `Configuration precedence`

Avoid headings that provide little information on their own, such as `Details`, `Other`, or repeated `Overview` sections without a subject.

Use descriptive link text.
Prefer repository-relative links for repository content unless local policy requires another form.

## Write operationally

- Put a condition before the action it governs.
- Make the actor explicit when the system performs the action.
- Use one term for one concept and define necessary abbreviations on first use.
- Replace vague conditions such as "as needed", "normally", or "after a while" with observable criteria.
- Keep each procedural step focused on one operation.
- State the working directory, required permissions, destructive effects, and relevant environment when the reader could otherwise choose incorrectly.

Do not use confidence-reducing fillers such as "simply", "obviously", or "easy".

## Make examples verifiable

Prefer commands and examples that can be copied without removing prompt characters or guessing placeholders.
Give placeholders meaningful names and explain them near the example.

For a procedure, pair actions with evidence of success:

- expected status, output, response, or state
- a command or observation that checks completion
- the next action for a known failure
- cleanup or recovery when the operation changes state

Do not invent validation, rollback, ownership, or escalation steps to make a procedure appear complete.
Report the missing requirement instead.

## Keep related information together

Place a code example next to its explanation and a diagram next to the text that interprets it.
Avoid making readers hold values from distant sections in working memory.

Use a diagram only when it communicates a relationship more efficiently than short prose, such as a boundary, sequence, dependency, data flow, state change, comparison, or hierarchy.
Label direction and meaning.
Keep essential information available in text and provide useful alternative text.

Use:

- numbered lists for ordered procedures
- bullets for unordered parallel items
- tables for short comparisons on stable shared dimensions

Replace a table with headings or lists when cells require paragraphs, complex code, or several independent conditions.

## Control scope and duplication

Treat README files as entry points, not containers for every detail.
Link to the canonical Architecture, How-to, Runbook, Reference, ADR, or generated contract.

Do not:

- narrate the investigation
- preserve rejected hypotheses
- copy generated API or configuration listings into prose
- add a generic best-practice section unrelated to the reader's task
- fill every possible template section
- rewrite unaffected prose for stylistic consistency
- add multiple examples that establish the same fact

After drafting, remove any heading, paragraph, or example whose deletion does not reduce task completion, correctness, or safety.

## Scope of these rules

These rules apply to utilitarian repository documentation.
They do not define book, article, tutorial-essay, or publication prose.
Narrative pacing, rhetorical tension, density waves, and other literary techniques are outside this reference.

## Evidence basis

- [GitHub: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [Google: Documentation best practices](https://developers.google.com/style)
- [Google: Technical Writing One](https://developers.google.com/tech-writing/one)
- [Diátaxis](https://diataxis.fr/)
