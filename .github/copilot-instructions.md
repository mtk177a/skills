# GitHub Copilot Instructions

`AGENTS.md` is the canonical source for shared repository instructions.
Read and follow the repository-root `AGENTS.md` before working in this repository.

This file is only a bridge for GitHub Copilot surfaces that load
`.github/copilot-instructions.md` but do not automatically load `AGENTS.md`.

Because those surfaces may not receive `AGENTS.md`, always apply this minimum
safety and approval fallback:

- Do not include secrets, personal information, customer information, or internal URLs.
- Do not hardcode OS-specific assumptions or local absolute paths.
- Obtain approval before changing repository rule documents, Skill bodies, or other operational guidance.

If `AGENTS.md` cannot be accessed, do not modify files, run commands, or make
external changes. Stop and report that the shared instructions are unavailable.

Keep shared instructions in `AGENTS.md`.
Add guidance here only when GitHub Copilot requires client-specific loading or behavior.
