# Installation, updates, and distribution

`mtk177a-skills` distributes the public `skills/` catalog as one portable Agent Plugin.\
Plugin and standalone/APM installations use the same sources, without separately maintained distribution copies.

- **Use Skills**: [Choose an installation route](#choose-an-installation-route) and check the [runtime requirements](compatibility.md#plugin-runtime-requirements).
- **Prepare a distribution**: [Build and verify an archive](#build-and-verify-an-archive).
- **Check included files**: [Package contents and source files](#package-contents-and-source-files).

## Choose an installation route

Choose one delivery route for overlapping Skills in each runtime:

| Target | Route |
| --- | --- |
| ChatGPT and Codex | Upload the ZIP as a personal ChatGPT plugin, then check availability in each intended surface |
| Cursor | Extract the same ZIP into Cursor's local plugin directory |
| Claude Code | Continue using the [APM installation](#install-through-apm); this package does not add a Claude-specific plugin manifest |

**Resolve overlapping installations before enabling the plugin.**

- **Target**: Identify overlapping plugin, standalone, or APM installations; disable or remove them using the client's supported controls.
- **Preserve**: Do not remove unrelated Skills or credentials, or rely on undocumented precedence or namespaces.
- **Recover and verify**: Retain the previous archive and verify the plugin in a new conversation.

Installation makes packaged instructions available; shell, repository, external-service, subagent, and write access remain separate requirements.\
An installed Skill may still lack the capabilities or permissions needed for the task.

## Install or update the plugin

### ChatGPT and Codex

The user uploads the archive manually.\
The builder does not upload files or change account settings.

1. **Upload the ZIP.**
   - First installation: use the personal plugin archive upload in ChatGPT Plugins.
   - Update: select **Upload new version** from the existing plugin's menu instead of creating another plugin.

2. **Check the version and Skill list.**\
   Then start a new conversation.

3. **Select the plugin and Skill.**\
   Use the available UI to select the plugin and name the Skill in the request.\
   For example: “Use `define-referents` from `mtk177a-skills` and read its reference before proposing names.”

4. **Verify each intended surface.**
   - Discovery: does the Skill appear in the list?
   - Loading: were the body and references read, when observable?
   - Output: what answer resulted? A plausible answer alone does not prove loading.

Chat, Work, dots, and Codex may differ in invocation syntax and runtime capabilities.

### Cursor

[Cursor's documentation](https://cursor.com/docs/plugins) describes support for portable Agent Plugins and local testing under `~/.cursor/plugins/local/<plugin-name>/`.

1. **Extract the ZIP.**\
   Place `plugin.json` directly inside `~/.cursor/plugins/local/mtk177a-skills/`.\
   When updating, preserve any needed backup and replace the old extracted directory as a whole.\
   Copying new files over old ones can leave removed Skills behind.
2. **Reload Cursor.**\
   Restart it or use **Developer: Reload Window**.
3. **Verify use.**\
   Check Skill discovery and explicit invocation.

This Skills-only package does not need `.cursor-plugin/plugin.json`.\
Marketplace submission is outside this workflow.

## Install through APM

Use APM for Claude Code or another supported APM target.

| Selection | Command |
| --- | --- |
| All Skills | `apm install mtk177a/skills` |
| Selected Skills | `apm install mtk177a/skills --skill cognitive-rhythm-writing --skill japanese-tech-writing` |
| Individual path | `apm install mtk177a/skills/skills/review-changes` |

`cognitive-rhythm-writing` reads the adjacent `japanese-tech-writing` Skill; install both using the selection above.

Alternatively, declare the bundle in the consumer's `apm.yml`:

```yaml
dependencies:
  apm:
    - mtk177a/skills
```

After installation, check the resolved location, discovery, and explicit use in the intended client.\
A successful APM install does not establish client runtime behavior.

## Recover from a faulty version

Restore the needed previous source content and distribute it under a new version, using the same build, installation, and verification steps.

## Build and verify an archive

- **Prerequisites**: Python 3.10 or later and Git; no additional Python dependencies.
- **Outputs**: ZIP, SHA-256, and build record, saved outside the repository.
- **Builder scope**: no network requests, installation, or upload.

1. **Prepare the source commit.**\
   Keep Skill bodies and resources in `skills/`; do not maintain separate distribution copies.\
   For an update, run the checks relevant to the changed Skill responsibilities and increment the version in `plugin.json`.\
   Commit the version and source changes before building; never distribute different content under an already distributed version.

2. **Check the source and build the ZIP.**\
   Use a checkout at the same revision as the source commit to be packaged.\
   Replace `<commit>` with that commit and `<outside-repository-output-directory>` with an output directory outside the repository.

   ```bash
   python3 -B scripts/check_repository.py
   python3 -B -m unittest discover -s tests
   git diff --check
   python3 -B scripts/build_plugin.py --ref <commit> --output-dir <outside-repository-output-directory>
   ```

   The builder resolves the reference once to a commit and reads committed files only; uncommitted and untracked files are excluded.\
   Existing output files cause an error rather than being overwritten.

3. **Verify installation from the pushed commit.**\
   Push the candidate branch, then follow the [APM distribution checks](#apm-distribution-checks) against that exact commit from disposable consumer directories outside this repository.\
   Do not run non-dry-run APM installation in the source checkout.

4. **Retain the artifacts and verification results.**\
   Keep the ZIP, hash, source commit, change summary, and verification results together.\
   The user can then upload the archive and check the update using the installation steps above.\
   Publishing artifacts through GitHub Releases requires separate authorization.

### APM distribution checks

When distribution behavior changes, install the pushed candidate commit from disposable consumer directories outside the source checkout.\
Check the full bundle, affected `--skill` selections, and affected individual paths separately, using each consumer's generated lockfile.

```bash
apm install 'mtk177a/skills#<commit>' --target agent-skills --no-policy
apm install --frozen --dry-run --no-policy
apm audit --ci --no-policy
```

Replace `<commit>` with the full pushed commit ID.\
Use that same commit for selected and individual installations.\
Do not run non-dry-run `apm install` or `apm update` in the source repository.

These checks cover installation and dependency integrity, not client invocation or instruction following.

### Generated files

| Output | Purpose |
| --- | --- |
| `<name>-<version>.zip` | Plugin archive to install |
| `<name>-<version>.sha256` | SHA-256 hash for identifying the archive's exact contents |
| `<name>-<version>.build.json` | Source commit, archive hash, Skill list, and each packaged file's hash and mode |

Sorted entries, fixed timestamps, and uncompressed storage make repeated ZIP builds byte-identical without depending on a compression-library version.

### What the builder verifies

The builder checks:

- Supported manifest identity fields, required root files, and each Skill's `SKILL.md` entrypoint.
- Mirror hashes against the recorded provenance.
- Relative Markdown links and explicit `references/` or `../` code-span references against the selected package.
- Absence of symlinks and submodules in included paths.
- Every ZIP entry's contents and file mode against the original Git blob and mode.

These checks cover specific packaging failures; they are not complete JSON Schema validation, full Markdown parsing, or runtime verification.\
When a Skill changes, separately review generic examples, plain-text references, tool availability, and conditional instructions that these checks cannot establish.

## Package contents and source files

### Manifest

- **Source**: only the root `plugin.json`, declaring the Agent Plugins 1.0.0 schema.
- **OpenAI settings**: use `extensions["com.openai"]` when needed.
- **Compatibility format**: do not maintain a second `.codex-plugin/plugin.json`. An inline OpenAI extension replaces its settings rather than merging them.

See [OpenAI packaging](https://developers.openai.com/plugins/build/plugins) for the format rules.

### Included and excluded files

The builder selects files from the requested Git commit:

- Include root `plugin.json`, `LICENSE`, and `THIRD_PARTY_NOTICES.md`.
- Include tracked files under public `skills/`, including references, runtime resources, metadata, both upstream mirrors, and their `UPSTREAM.md` provenance files.\
  Exclude filenames ending in `-ja.md` or `.ja.md`.
- Exclude repository instructions, tests, documentation, and repository maintenance Skills under `.agents/`.

Included files retain their original bytes.\
New tracked files under `skills/` are distribution candidates, so review additions before committing for scripts, external references, credentials, and generated output.

There is no enclosing directory above `plugin.json` and `skills/`.\
All public Skills are packaged, but their [runtime requirements](compatibility.md#plugin-runtime-requirements) still apply.
