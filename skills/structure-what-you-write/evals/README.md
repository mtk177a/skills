# structure-what-you-write evaluations

## Purpose

This guide evaluates whether the Skill adds useful writing behavior when used on its own, compared with the same model without the Skill.
Evaluate whether the result helps readers find, understand, compare, or use evidence-backed information while preserving meaning and authority.
Passing assertions establishes task adequacy; it does not by itself establish an effect attributable to the Skill.
Judge both outputs against the reader's task rather than rewarding a preferred Markdown layout.

## Evaluation definitions

- [evals.json](evals.json): 15 behavior cases with inline input files and case-specific assertions.
- [triggers.json](triggers.json): 8 routing cases covering explicit and implicit writing requests and non-writing controls.
- [report.json](report.json): the latest executed behavior results, with candidate hashes and per-assertion grades; comparative judgments are recorded below.

Fixtures are fictional and self-contained; no case requires an external service, publication, installation, or live-system operation.

## Choose the evaluation method

For the question "Does this Skill produce its intended effect?", use `baseline-comparison` with explicit `candidate` and `without-skill` conditions.
Give the candidate only this Skill and give the control no Skills; keep the model, reasoning effort, request, fixture, tool access and sandbox identical.
Verify the entire visible Skill catalog, not only the absence of a personal same-name copy.
Disable unrelated personal Skills only for the evaluation invocation; stop if the required isolation cannot be confirmed.
No other Skill's selection, installation or cooperation is an individual acceptance requirement.

Use `targeted-candidate` for a localized regression question after effectiveness has been assessed.
Use `static-only` for meaning-preserving documentation edits.
`targeted-routing` is an optional, separate discovery evaluation; it does not measure writing benefit and is not a prerequisite for accepting standalone behavior.
Coexistence studies require their own concrete deployment question and scope.
See [evaluation-path selection](../../../docs/evaluation.md#select-an-evaluation-path) for shared rules.

Behavior cases use `workspace-write` even when the expected result is no edit, so an unauthorized edit can be observed.
Prompts describe reader goals and authorized edits rather than prescribing a split, merge, table, or heading pattern.
The field pair uses domain labels and multiplicities different from the Skill's worked examples.
These are synthetic transfer tasks, not evidence of performance on all real-world writing.

## Evaluation cases

### Behavior cases — evals.json

Each row identifies one case in [evals.json](evals.json), the responsibility it checks, and the evidence needed for grading.
Select cases for the changed responsibility; the assertions in the definition supply the full acceptance criteria.

| Case ID | Responsibility | Failure to detect | Grading evidence |
| --- | --- | --- | --- |
| `views-and-checks` | Semantic units and containment | Keeps arbitrary bundles or treats a checking instruction as a peer view record | Edited task and preserved name/filter associations |
| `state-and-completion` | Related but distinct information functions | Obscures state definitions, progress evidence, or qualified completion rules | Edited assessment and all preserved conditions |
| `field-lookup` | Independent field lookup | Makes one field's complete definition hard to retrieve or confuses unset and explicit None | Definition locality and exact field semantics |
| `field-comparison` | Reader-dependent presentation | Mechanically splits a useful side-by-side comparison because an example used separate tables | Comparable dimensions, with independent schemas preserved |
| `ordered-procedure` | Executable order and exceptions | Performs a write before its prerequisite or detaches no-retry/result checks | Edited sequence and every stop/verification condition |
| `split-reader-tasks` | Independent reader tasks | Makes onboarding or configuration lookup hard to access, or creates conflicting copies | Entry paths for both readers, completeness, reference authority and links; no prescribed file count |
| `merge-fragmented-guide` | One coherent reader task | Requires a chain of file jumps or loses instructions/links | Complete procedure and necessary navigation from README; no prescribed filename |
| `standalone-task` | Standalone execution, placement, and preserved behavior | Extracts essential rules, retains maintainer duties as execution steps, or invents runtime rules while restructuring | Task body compared with supplied operational requirements, maintainer document, and created-file list |
| `short-message` | Short-form creation | Adds report scaffolding or invents commitments in a short message | Final message and absence of sends/file writes |
| `no-documentation-impact` | No-change judgment | Manufactures edits after an internal refactor with no reader impact | Original fixture comparison and explanation |
| `review-only-scope` | Structural review and edit authority | Only proofreads local wording or edits related sources during a review-only request | Findings, proposed placements, and unchanged fixture files |
| `focused-readme-update` | Focused update and verification | Rewrites unrelated sections or claims command verification without execution | README delta, command trace/output, preserved other files |
| `pr-description` | Evidence-based PR writing | Publishes drafting history, rejected behavior, or an unverified release claim | Final description compared with change, diff, and attributed verification record |
| `unknown-design-rationale` | Current behavior versus rationale | Invents an accepted design reason from implementation evidence, or refuses independently supported work | Current-behavior document and explicit rationale uncertainty |
| `faithful-restructure` | Faithful editing versus content selection | Deletes supplied claims, changes their certainty, or turns a proposal into approval | Full claim/condition comparison with the supplied original |

The paired `field-lookup` and `field-comparison` cases use the same source for different reader tasks.
Select both when changing how field definitions are presented: success requires choosing a structure for the requested lookup or comparison, not copying a fixed table pattern.
The independent-reader, coherent-procedure and standalone cases test distinct placement decisions; neither splitting nor merging is inherently better.

### Routing cases — triggers.json

Each row identifies one case in [triggers.json](triggers.json).
Expected selection corresponds to `expected_handlers`: the target Skill for writing requests and an empty array for non-writing controls.
These cases test selection, not the quality of the resulting writing.
They are retained for optional discovery investigations and are excluded from the standalone-effectiveness comparison.

| Case ID | Request type | Expected selection | Failure to detect |
| --- | --- | --- | --- |
| `explicit-structure` | Explicit Skill invocation | `structure-what-you-write` | Ignores explicit invocation |
| `implicit-readme` | README drafting | `structure-what-you-write` | Misses an implicit documentation-writing request |
| `implicit-email` | Short email drafting | `structure-what-you-write` | Excludes short messages from writing support |
| `implicit-structural-review` | Read-only structural review | `structure-what-you-write` | Misses review of information organization |
| `implicit-no-change-assessment` | Documentation-impact assessment | `structure-what-you-write` | Misses writing work that can conclude no change is needed |
| `arithmetic` | Arithmetic | No Skill (`[]`) | Invokes writing support for a numerical calculation |
| `literal-copy` | Exact string copying | No Skill (`[]`) | Invokes writing support when rewriting is prohibited |
| `lookup-only` | Direct numeric lookup | No Skill (`[]`) | Invokes writing support for simple value retrieval |

## Run the selected evaluation

Run commands from the repository root.

1. **Check the definitions and inputs.**
   - Keep prompts and fixtures separate from assertions and expected answers.
   - Check fixture paths for safety.
   - Confirm that the supplied facts are sufficient for the requested task.
   - Check assertions against the current Skill's requirements.
   - Run the repository checker; it validates package metadata, evaluation definitions, and referenced assets.

   ```bash
   python3 scripts/check_repository.py
   ```

2. **Create a plan for the selected cases.**
   Use the path, conditions, and sandbox chosen above.\
   The initial standalone-effectiveness comparison selects the nine cases listed below:

   ```bash
   evaluation_tmp="$(mktemp -d)"
   python3 scripts/run_skill_evaluation.py plan \
     --skill structure-what-you-write \
     --path baseline-comparison \
     --purpose "Assess the incremental effect of the standalone Skill." \
     --affected "reader access, placement, creation, review and preserved meaning" \
     --condition candidate \
     --condition without-skill \
     --case views-and-checks \
     --case field-lookup \
     --case field-comparison \
     --case split-reader-tasks \
     --case merge-fragmented-guide \
     --case standalone-task \
     --case short-message \
     --case review-only-scope \
     --case pr-description \
     --base-ref HEAD \
     --sandbox workspace-write \
     --output "$evaluation_tmp/plan.json"
   ```

3. **Inspect and execute the plan.**
   Confirm the selected cases, conditions, sandbox, and estimated model-call count before execution.\
   Follow [the shared execution procedure](../../../docs/evaluation.md#execute-the-approved-plan).\
   The nine paired cases require 18 model calls, with no additional model grader.\
   Planning alone does not execute a case.

4. **Grade the observed results.**
   Use the evidence requirements below and [the shared grading procedure](../../../docs/evaluation.md#grade-planned-results).\
   The invoking agent or a human grades behavior assertions; the Runner grades routing selection from its trace.\
   Apply the same assertions to both conditions, then compare reader-task outcomes using the probes below.\
   No additional model grader is required.

5. **Record the result and decide whether more evidence is needed.**
   After actual execution, follow [the shared report procedure](../../../docs/evaluation.md#preview-and-write-the-report).\
   Keep raw plans, traces, fixture snapshots, and grades outside the repository.\
   Stop when the selected cases resolve the acceptance question; add evaluation only for a changed responsibility, uncovered failure, unstable result, or conflicting evidence that affects the decision.

## Grade the results

### Behavior: writing quality and authorized changes

Grade each behavior case against its assertions in `evals.json`; all are marked critical.
For structural judgments, inspect whether the result serves the requested reader task and preserves every required relationship and qualification.
A view inventory can pass as a list or a table when its associations, checking instructions, and scope are clear.
The field cases require the requested access pattern rather than a prescribed column arrangement.

Use all applicable checks below for the selected case; these are grading dimensions, not mutually exclusive case types.

| Grading dimension | Evidence to inspect | What to establish |
| --- | --- | --- |
| Writing quality and completeness | Final artifact or response, compared with the request and supplied sources | The requested information and relationships are accurate, complete, and useful to the reader |
| Edit authority and preservation | Changed, added, or removed fixture files, compared with their original contents | Changes stayed within authority; no-edit and review-only cases left content unchanged |
| Reference integrity | Relative links affected by the edit and their destinations | Required information remains reachable after moves or deletions |
| Verification claims | Execution trace and actual command output, compared with the final report | Observed verification is distinguished from supplied reports and unperformed checks |

Do not infer a completed edit from the final response alone.
Inspect no-edit cases for actual content changes even though their sandbox permits writes.
For `standalone-task`, check additions as well as omissions: new processing order, validation, stop/continue behavior, access restrictions, or mandatory output constraints require a supplied basis.
Headings, bullets, and other presentation choices are allowed when they do not change required execution behavior.
Record insufficient evidence as `inconclusive`.

### Routing: expected versus observed selection

Use `expected_handlers` in `triggers.json` as the expected selection and the completed event trace as the observation.
Successful Skill-read events establish which installed Skills were read.
Only a completed trace with neither a target read nor an ambiguous read attempt supports non-selection.
A missing or incomplete trace, or an unresolved read attempt in a failed shell command, is `inconclusive`, not proof of non-selection.
The Runner grades this routing requirement from the trace according to [the shared evaluation rules](../../../docs/evaluation.md#grade-planned-results).

## Compare the reader-task outcomes

The selected cases cover distinct intended effects and a control against harmful overstructuring.
Other cases remain available for their specific regression questions; there is no required universal case count.
The probes are for the grader and must not be added to executor inputs.

| Case | Reader probe and comparative evidence |
| --- | --- |
| `views-and-checks` | Locate the Unowned filter and the common before-use checks; inspect whether names, filters and checks are grouped by meaning without reconstructing arbitrary bundles |
| `field-lookup` | Find all Request checks values, its selection/clearing rules and blank/None behavior as one coherent lookup; count necessary jumps or unrelated scans, not headings |
| `field-comparison` | Compare the two multiplicities and special states directly; check whether both lookup and comparison outputs adapt to the different reader tasks |
| `split-reader-tasks` | Trace a default first run and a maintainer's WIDTH lookup from README; inspect direct access, one authoritative definition and any avoidable navigation |
| `merge-fragmented-guide` | Trace prerequisites through failure reporting from README; compare mandatory file jumps while preserving every instruction |
| `standalone-task` | Give the executing reader only task.md; inspect whether all required rules remain local and no new runtime decisions are imposed |
| `short-message` | Read the message as a colleague; inspect whether all four facts/request are conveyed without report scaffolding or invented commitments |
| `review-only-scope` | Determine where configuration and issue-reporting guidance should live and why; compare actionable diagnosis, maintained-source reasoning and unsupported findings, with no edits |
| `pr-description` | Determine the actual behavior change and verification limits; compare grounded synthesis and the effort to distinguish delivered behavior from drafting notes |

1. Grade every assertion for each condition from the artifact/response and actual trace, not executor self-report.
2. Hide condition labels before comparing the outputs against these probes; record source locations and concrete retrieval or comprehension differences before revealing the labels.
3. Record the candidate's effect as `better`, `equivalent`, `worse`, `mixed`, or `inconclusive` for each pair.\
   A material gain must help complete the reader task; an alternate table style, additional headings, shorter text, or more files alone is not a gain.\
   Use `mixed` when gains and losses matter, and `inconclusive` when evidence is insufficient.\
   Do not average away lost meaning, unauthorized edits, or invented requirements.
4. State the supported benefit and its limits.\
   A candidate critical failure prevents an unqualified acceptance recommendation, even if the control also fails.\
   If both conditions meet the requirements and the probes show no material difference, record no demonstrated incremental benefit; do not infer effectiveness from the candidate passing.\
   Mixed or sparse gains support only the specific observed tasks, not the entire advertised scope.

The invoking agent performs the grading; masked labels reduce expectation bias but do not make this an independent or statistically blinded study.
Record ties and regressions honestly rather than adding easier cases or tuning to obtain a favorable comparison.
Repeat only for a decision-relevant instability or ambiguity and keep rejected candidates separate.

## Recorded verification

The revised definitions were evaluated on 2026-10-16 against the working-tree Skill based on commit `e43f40af06030cf8148f195deb8be42a4b964e75`.
[report.json](report.json) binds the exact Skill and evaluation-definition hashes and records all 18 case-condition grades.
The comparison used Codex CLI `0.162.0-alpha.17.2`, `gpt-6-luna`, reasoning effort `max`, and `workspace-write` in both conditions.
Each of the nine preselected cases ran once per condition in a fresh ephemeral session, with identical request and fixture data and no coexistence Skills.
A temporary per-invocation adapter disabled personal Skills and required the visible catalog to contain only the candidate or to be empty in the control.
All candidate body reads and copied manifests were verified, and controls contained no target Skill.
Three independent six-call Runner batches were combined by matching their actual execution pairs to the approved 18-call plan; original batch records, traces, masked outputs and grades remain outside the repository.

### Comparative findings

No case demonstrated an unqualified incremental benefit from the Skill.
Eight pairs were materially equivalent; one had important gains and losses and failed critical requirements in both conditions.
The invoking agent graded artifacts with condition labels hidden, recorded the judgments, then revealed the labels.
This does not establish that the Skill has no effect in all environments; it establishes that this sample does not support the intended general benefit.

| Case | Candidate / without-Skill requirement result | Comparative effect and evidence |
| --- | --- | --- |
| `views-and-checks` | Pass / pass | Equivalent: both expose each filter in a table and common checks in a separate scoped section |
| `field-lookup` | Pass / pass | Equivalent: both provide field-specific value/clearing tables and clearly shared blank/None rules |
| `field-comparison` | Pass / pass | Equivalent: both directly expose different multiplicities and common exceptional states; a longer supporting reference adds no material gain |
| `split-reader-tasks` | Pass / pass | Equivalent: both put the default startup in README and complete settings in one reference a single link away |
| `merge-fragmented-guide` | Pass / pass | Equivalent: both place the whole procedure in README, eliminating mandatory file jumps and retaining instructions |
| `standalone-task` | Fail / fail | Mixed: candidate avoids unsupported operational design but omits reporting partial missing input after item entries; control preserves that requirement but invents processing order, validation and output rules |
| `short-message` | Pass / pass | Equivalent: both convey the same facts and request naturally without added commitments or report scaffolding |
| `review-only-scope` | Pass / pass | Equivalent: both identify the mixed reader tasks and duplicated configuration, propose maintained-source links, and make no edits |
| `pr-description` | Pass / pass | Equivalent: both synthesize the delivered flag/default/scope and accurately attribute limited verification, without drafting history |

The standalone candidate's `Report` section lists titles/statuses but lacks the supplied instruction to append any missing input.
Its absent-snapshot rule does not retain the broader reporting requirement.
The control adds mandatory snapshot ordering, missing/invalid-record handling, placeholders and exact output rules that were not supplied.
Neither result is an acceptable standalone-task revision.
Do not recommend merging on the claim that the Skill has demonstrated its intended writing benefit on this evidence.

### Check results and limits

The Runner report contains 16 passing and 2 failing case-condition results; these are adequacy grades, not counts of beneficial comparisons.
All three batches passed the repository checker before execution.
Repository unit tests passed (157 tests); current report consistency, relative file links, mirrored command examples and whitespace were checked separately.
The Skill body and other Skills were not tuned after observing this comparison.
Unselected regression cases and optional routing cases were not executed in this assessment.

## Further evaluation decisions

Address the concrete missing-input preservation failure before accepting the standalone behavior.
If a revised design proposes a specific benefit beyond these results, compare the relevant matched tasks rather than accumulating favorable cases.
Additional clients, repeated-run stability, live readers, multi-turn work, unavailable external evidence, scale and rendered accessibility require separate concrete questions; they are not automatic prerequisites.
Discovery and multi-Skill composition remain outside individual standalone-effectiveness acceptance.
