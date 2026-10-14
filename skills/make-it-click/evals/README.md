# make-it-click evaluation

The executable cases test whether the Skill produces complete, reader-facing explanations across Japanese and English, technical and everyday topics, and new writing and revision. They cover a missing case-specific premise, an eligibility condition, excess internal history, unsupported causation, and multiple possible contributors. The prompts are separate from `references/explanation-examples.md`; repeating that reference is not an acceptance criterion.

Run selected cases with the existing `scripts/run_skill_evaluation.py` Runner. For this new Skill, compare `candidate` with `without-skill` under the same case, model, reasoning effort, and sandbox. The Runner hides assertions from the executor. Grade each actual response against the case assertions; distinguish the observations from a manual source review. Keep raw artifacts under a temporary directory, and record only a compact report in `report.json` if execution completes.

## Current result (2026-10-14)

The current `SKILL.md` SHA-256 is `f9902f6ab90d0d04c6113f6f4eeab5ad4678c0406ab4665b3540e9609c7d0b26`. A matched plan for all five cases under `candidate` and `without-skill` was generated for this version: 10 planned calls, none executed. The repository checker and 154 unit tests passed; these static checks do not establish explanation quality.

A previous candidate had a matched plan for all five cases under both `candidate` and `without-skill` with Codex CLI 0.159.0-alpha.3, `gpt-6-luna`, `max` reasoning, and a read-only sandbox. Its first run stopped at preflight because the default `CODEX_HOME` was read-only. A one-case candidate retry passed Skill catalog inspection but timed out after the network proxy returned HTTP CONNECT 403 for the model service. Completed responses: 0; graded requirements: 0. Improvement or regression relative to no Skill, other models and clients, and live source verification remain unconfirmed. No `report.json` was written. Retry the matched comparison when model access is available; the reference examples are not evaluation inputs.
