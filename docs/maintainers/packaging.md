# Build a plugin archive

This document is for maintainers.\
It describes how to build a new plugin version as a ZIP, confirm that the pushed commit installs through APM, and what the ZIP contains.\
To install the ZIP in ChatGPT or Cursor, see the [installation guide](../users/installation.md).\
Publishing through GitHub Releases or elsewhere is outside this document's scope.

## Requirements

- Python 3.10 or later
- Git

## Procedure

Follow these four steps to build the ZIP and confirm that the same commit installs through APM.

### 1. Prepare the source commit

Keep Skill bodies and resources in `skills/` only; do not maintain separate distribution copies.

For an update, do both of the following before committing:

- Run the checks relevant to the changed Skill responsibilities.
- Increment the version in `plugin.json`.

Then commit the version and source changes.\
Never reuse a version number; whenever the content changes, increment the version.

To recover from a faulty version, restore the needed previous content in `skills/` and build it as a new version with these same steps.

### 2. Check the repository and build the ZIP

From a checkout of the step 1 commit, run the following commands in order.

```bash
# Check the repository
python3 -B scripts/check_repository.py
python3 -B -m unittest discover -s tests
git diff --check

# Build the ZIP
python3 -B scripts/build_plugin.py --ref <commit> --output-dir <outside-repository-output-directory>
```

- `<commit>`: the commit from step 1.
- `<outside-repository-output-directory>`: where to write the outputs.\
  Use a directory outside the repository.

The builder resolves `--ref` to a commit once and reads only the files in that commit.\
Uncommitted changes and untracked files are therefore not included.\
If an output file with the same name already exists, the builder exits with an error instead of overwriting it.\
The builder makes no network requests and performs no installation or upload.

### 3. Verify APM installation from the pushed commit

Push the candidate branch and install its commit with APM.\
Use a separate disposable consumer directory outside this repository for each of the following installations.

| Installation | Target | Why this target |
| --- | --- | --- |
| Full bundle | All public Skills | Covers the whole catalog |
| Selection | `cognitive-rhythm-writing` and `japanese-tech-writing` | The first Skill requires the second |
| Individual path | `define-referents` | Has a bundled reference file |

Install with the command for each directory.

```bash
# Full bundle
apm install 'mtk177a/skills#<commit>' --target agent-skills --no-policy

# Selection
apm install 'mtk177a/skills#<commit>' --skill cognitive-rhythm-writing --skill japanese-tech-writing --target agent-skills --no-policy

# Individual path
apm install 'mtk177a/skills/skills/define-referents#<commit>' --target agent-skills --no-policy
```

Replace `<commit>` with the full ID of the pushed commit.

Then, in each directory, verify the installation against the generated lockfile.

```bash
apm install --frozen --dry-run --no-policy
apm audit --ci --no-policy
```

Do not run non-dry-run `apm install` or `apm update` in this repository.\
Doing so creates consumer manifests, lockfiles, and installed files in the source checkout.

These checks show whether installation and dependencies are intact.\
They do not show whether a client invokes the Skills or follows their instructions.

### 4. Keep the outputs

Keep the ZIP, hash, source commit, change summary, and verification results together so that each can be traced to the others.

## Archive specification

### Generated files

| File | Purpose |
| --- | --- |
| `<name>-<version>.zip` | Plugin archive to install |
| `<name>-<version>.sha256` | SHA-256 hash that identifies the archive's exact contents |
| `<name>-<version>.build.json` | Source commit, archive hash, Skill list, and each packaged file's hash and mode |

Building the same commit again produces a byte-identical ZIP.\
Entries are sorted, timestamps are fixed, and files are stored uncompressed, so the result does not depend on the compression-library version.

### Included files

The builder selects the following files from the requested commit:

- Root `plugin.json`, `LICENSE`, and `THIRD_PARTY_NOTICES.md`
- Tracked files under `skills/`.\
  These include references, runtime resources, metadata, both upstream mirrors, and their `UPSTREAM.md` provenance files.

The following files are excluded:

- Files under `skills/` whose names end in `-ja.md` or `.ja.md`
- Repository instructions, tests, and documentation
- Repository maintenance Skills under `.agents/`

Included files keep their original bytes.\
`plugin.json` and `skills/` sit at the top level of the ZIP, with no enclosing directory.

Any new tracked file under `skills/` goes into the ZIP.\
Before committing, review additions for scripts, external references, credentials, and generated output.

### Manifest

The root `plugin.json` is the only manifest source.\
It declares the Agent Plugins 1.0.0 schema.

Put OpenAI-specific settings in `extensions["com.openai"]` of `plugin.json` when needed.\
Do not maintain a separate compatibility `.codex-plugin/plugin.json`.\
When the root `plugin.json` contains an OpenAI extension, only those settings apply; they are not merged with the compatibility format.

See [OpenAI packaging](https://developers.openai.com/plugins/build/plugins) for the format rules.

### Build-time checks

When building the ZIP, the builder checks the following:

- The manifest identity fields that the builder supports
- The required root files exist
- Each Skill has a `SKILL.md`
- Upstream mirror hashes match the hashes recorded in their provenance files
- Relative Markdown links, and code-span references starting with `references/` or `../`, point to files included in the ZIP
- Included paths contain no symlinks or submodules
- Each ZIP entry's contents and file mode match the original file recorded in Git

These checks catch specific packaging failures only.\
They do not validate every JSON Schema field, fully parse Markdown, or verify runtime behavior.

When a Skill changes, separately review the following:

- References given in generic examples or plain text
- Whether required tools are available
- Conditional instructions
