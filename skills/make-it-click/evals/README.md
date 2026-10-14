# make-it-click evaluation

The executable cases test whether the Skill produces complete, reader-facing explanations across Japanese and English, technical and everyday topics, and new writing and revision. They cover a missing case-specific premise, an eligibility condition, excess internal history, unsupported causation, and multiple possible contributors. The prompts are separate from `references/explanation-examples.md`; repeating that reference is not an acceptance criterion.

Run selected cases with the existing `scripts/run_skill_evaluation.py` Runner. For this new Skill, compare `candidate` with `without-skill` under the same case, model, reasoning effort, and sandbox. The Runner hides assertions from the executor. Grade each actual response against the case assertions; distinguish the observations from a manual source review. Keep raw artifacts under a temporary directory, and record only a compact report in `report.json` if execution completes.

## Current result (2026-10-14)

The earlier `write-clear-explanations` candidate had a plan for all five cases under both `candidate` and `without-skill`: 10 planned calls with Codex CLI 0.159.0-alpha.3, `gpt-6-luna`, `max` reasoning, and a read-only sandbox, against `origin/main` at `cea5c19`. That candidate's `SKILL.md` SHA-256 was `c8520cc1e7a4ae75b70df4221ccc52cc5b605c3798ca3a691c31faffcb475ff2`. The first run stopped before model execution because the environment's default `CODEX_HOME` is read-only. A one-case candidate retry with a writable temporary home passed the Skill catalog check, then timed out because the network proxy returned HTTP CONNECT 403 for the model service. Actual completed responses: 0. No requirement was graded, and no improvement or regression relative to the no-Skill condition is established. No `report.json` was written.

The renamed `make-it-click` candidate has `SKILL.md` SHA-256 `f795475565c9201cfb34385c7506946ff5866cc785d2ffd17785a0e6f7c2230e`. It has not been run against a model. Repository checker and unit-test results for this version are recorded in the pull request.

This attempt does not establish behavior for any selected case, other models, clients, subjects, or live source verification. The reference examples are illustrations, not evaluation inputs. Retry the planned matched comparison only when model access is available; the static checks are not behavioral evidence.
