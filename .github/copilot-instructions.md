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
- Inspect the existing Skills needed to resolve responsibility overlap and converge on a judgment; stop when that purpose is met, do not impose an arbitrary count, and keep content concise
- Use concise ordered steps and verification when sequence or completeness materially affects correctness
- Changes to repository rule documents or Skill bodies require approval before proceeding
