# Plugin distribution

`mtk177a-skills` packages the public `skills/` catalog as one portable Agent Plugin, starting at `0.1.0`.
Keep Skill bodies and resources in `skills/`; do not maintain distribution copies.
Standalone Skills and the native APM bundle remain available.

## Package contents

The root `plugin.json` is the only maintained plugin manifest and declares the Agent Plugins 1.0.0 schema.
OpenAI-specific settings, when needed, belong under `extensions["com.openai"]` in that file.
Do not maintain a second `.codex-plugin/plugin.json`: OpenAI supports that compatibility format, but an inline OpenAI extension replaces its settings rather than merging them.
See [OpenAI packaging](https://developers.openai.com/plugins/build/plugins).

The builder includes `plugin.json`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, and tracked files under public `skills/`, excluding `evals/` and filenames ending in `-ja.md` or `.ja.md`.
It retains references, runtime resources and metadata, and both mirrors' `UPSTREAM.md` files byte for byte.
It excludes repository maintenance Skills under `.agents/`, repository instructions, tests, and repository documentation.
New tracked files under `skills/` are distribution candidates: review them before committing, including scripts, external references, credentials, and generated output.

The initial catalog contains 29 Skills, 14 reference files, and two provenance files; with the three root files, the ZIP has 48 entries.
All Skills are included, but execution still depends on the [runtime requirements](compatibility.md#plugin-runtime-requirements).
The archive has no extra enclosing directory.

## Build a candidate

Use Python 3.10 or later and Git; the builder adds no Python dependencies and performs no network requests, installation, or upload.
Run the builder from the same checkout revision that supplies the release source.
The reference is resolved once to a commit; uncommitted and untracked files never enter the package.
Commit the manifest version before building.

```bash
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests
git diff --check
python3 -B scripts/build_plugin.py --ref <commit> --output-dir <outside-repository-output-directory>
```

The output consists of `<name>-<version>.zip`, `.sha256`, and `.build.json`.
The build record identifies the source commit, archive hash, Skill list, and every packaged file's hash and mode.
Sorted entries, fixed timestamps, and uncompressed ZIP storage make repeated builds byte-identical without depending on a compression-library version.
The builder rejects existing output files instead of replacing them.

Validation checks the supported manifest identity fields, required package files, Skill entrypoints, mirror hashes, relative Markdown links, and explicit `references/` or `../` code-span references against the selected package.
It rejects symlinks and submodules in included paths and verifies every ZIP entry against the original blob and mode.
This is a focused release check, not a complete JSON Schema or Markdown parser and not a behavioral evaluation.
Generic examples, plain-text references, tool availability, and conditional instructions still require review when a Skill changes.

Before distribution, push the candidate branch and verify that exact commit from disposable consumer directories outside this repository.
Follow the [APM checks](compatibility.md#validation) for the full bundle, affected selections, individual paths, frozen install, and audit.
Do not run non-dry-run APM installation in the source checkout.
Keep the ZIP, hash, source commit, change summary, and verification results together; distributing them through GitHub Releases requires separate authorization.

## Install and update

### ChatGPT and Codex

1. In ChatGPT Plugins, use the personal plugin archive upload to install the ZIP.
2. For later versions, open the existing plugin's menu and select **Upload new version**, rather than creating another plugin.
3. Check the displayed version and Skill list, then start a new conversation for an explicit-use check.
4. Select the plugin with the available UI and name the intended Skill in the request, for example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”
5. Check discovery, body/reference reading when observable, and output separately in each target surface.

Do not assume that the same invocation syntax or runtime capabilities exist in Chat, Work, dots, and Codex.
Do not infer loading from a plausible answer or assume automatic selection without a recorded test.
Installing the plugin does not grant shell access, repository access, external connections, subagents, or write permissions.
The user performs uploads; the builder does not change account settings.

### Cursor

[Cursor documents](https://cursor.com/docs/plugins) portable Agent Plugins support and local testing under `~/.cursor/plugins/local/<plugin-name>/`.
Extract the same ZIP into that plugin directory so `plugin.json` is directly inside it, then restart Cursor or use **Developer: Reload Window** and verify Skill discovery and explicit use.
For local updates, replace the old extracted directory as a whole after preserving any needed backup; overlaying files can leave removed Skills behind.
No `.cursor-plugin/plugin.json` is needed for this Skills-only package.
This is the documented local route; actual Cursor behavior remains unverified until tested.
Marketplace submission is outside this workflow.

### Avoid duplicate installations

Choose Plugin or standalone/APM delivery for the same Skills in each runtime.
Before enabling the formal plugin, identify and disable or remove the probe plugin and overlapping standalone installations using the client's supported controls.
Do not remove unrelated Skills or credentials, and do not rely on undocumented precedence or namespaces to resolve duplicates.
Verify the formal plugin in a new conversation; retain the prior archive for recovery.
APM remains the existing Claude Code route; a Claude-specific plugin manifest is not introduced.

## Release and recovery

Update Skill sources, run the checks relevant to their changed responsibilities, increment `plugin.json` version, and commit before generating the next archive.
Repeat package and consumer checks, retain the release evidence, then have the user upload and verify the update.
Never replace a distributed version with different content.
For recovery, restore the needed previous source content and issue it under a new version after the same checks; direct downgrade has not been verified.
Do not mix runtime tests with static or consumer-install evidence.
A formal release is not behavior-verified until the user-uploaded package has been checked on the intended surfaces.
