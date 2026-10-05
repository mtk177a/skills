# triage-review-feedback evals

The executable definitions use the repository Runner's `{skill_name, evals}` format:

- `evals.json` contains existing-finding inputs and assertions for assessment, state, response decisions, evidence preservation, and authority boundaries.
- `triggers.json` checks selection against `review-changes`, `implement-changes`, `validate-fix`, and `draft-review-comments` in a shared catalog.
- `results.json` preserves historical Codex CLI evidence; its former candidate totals do not certify later changes.
- `report.json` records the selected current candidate behavior evaluation.

## Coverage map

| Responsibility | Plausible failure | Case |
| --- | --- | --- |
| Existing findings are required | Invents a finding or decision without input | `missing-findings` |
| Assessment and response are independent | Treats high impact or low confidence as a decision, or rejects a supported but disproportionate concern as technically false | `high-impact-low-confidence-question`, `supported-but-disproportionate` |
| Current state is separate from historical validity | Schedules work for a finding resolved in the target revision | `resolved-stale-finding` |
| The response addresses the concern | Adopts an incompatible proposed implementation despite a valid concern | `supported-concern-bad-proposal` |
| Collection decisions are coherent | Schedules duplicate or contradictory work | `duplicate-and-conflicting-findings` |
| Feedback does not grant authority | Executes an embedded install or outbound data-transfer request | `embedded-command-and-data-transfer` plus command-trace inspection |
| Adjacent workflow routing is precise | Selects triage for discovery, implementation, completed-fix validation, or comment drafting | `triggers.json` |

## Execution

Plan selected cases with `scripts/run_skill_evaluation.py plan` before a model call. Use `targeted-candidate` for behavior and `targeted-routing` for selection; execute only the cases needed for the changed responsibility. Keep plans, raw traces, and full responses outside the repository. Inspect command events, not only the answer text, for `embedded-command-and-data-transfer`.

Run `python3 scripts/check_repository.py` and `python3 -m unittest discover -s tests` after changing evaluation definitions. A format migration alone requires static validation of every migrated case and its preserved intent, not a model rerun of the entire historical suite. Record selected executions and unverified scope in the Issue and, when model evaluation runs, in `report.json`.

## Historical evidence

On 2026-07-27, Codex CLI 0.145.0 with `gpt-5.6-sol` and high reasoning passed 28/28 candidate behavior requirements across six cases and 6/6 trigger cases after an isolated rerun. No embedded install, private-key access, or outbound upload command was executed. A later proportionality revision on 2026-08-14 added independent assessment, state, and response decisions; its matched forward test kept a supported but disproportionate concern as `Supported`, `Open`, and `No action`. The earlier pass totals are superseded for that changed decision contract. Claude Code and other clients were not exercised.
