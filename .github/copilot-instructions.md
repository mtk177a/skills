# GitHub Copilot Instructions

This repository manages personally authored and maintained agent Skills.

- Read `README.md` and `docs/authoring.md` first
- The basic unit is `skills/<skill-name>/SKILL.md`
- Directory names and `name` values use kebab-case
- `SKILL.md` frontmatter must include at minimum `name`, `description`, and `license`
- Express agent-specific differences in Skill names or `description`; do not create `common/` or per-agent classification directories
- Add `evals/`, `references/`, `scripts/`, `assets/` only when needed
- Do not propose copying external Skills verbatim
- Do not include secrets, personal information, customer information, or internal URLs
- Do not hardcode OS-specific assumptions or local absolute paths
- Match the style of existing Skills and docs; keep content concise
- Changes to repository rule documents or Skill bodies require approval before proceeding
