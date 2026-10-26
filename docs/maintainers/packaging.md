# Build the plugin ZIP

This guide is for maintainers and the agents working for them.\
It describes how to build a new plugin version as a ZIP, and how to confirm that the pushed commit installs through APM.\
It also describes what the ZIP contains.\
To install the ZIP in ChatGPT or Cursor, see the [installation guide](../users/installation.md).\
Publishing through GitHub Releases or elsewhere is outside this guide.

## Requirements

- Python 3.10 or later
- Git
- APM, for step 3

## Procedure

Follow these four steps to build the ZIP and confirm that the same commit installs through APM.

### 1. Prepare the source commit

Keep Skill bodies and resources only in `skills/`.\
The build copies them into the ZIP.

For an update, do both of the following before committing:

- Check the results and safety boundaries of the changed Skills, as their changes require.
- Increment the version in `plugin.json`.

Then commit the version and source changes.\
Give each change of content a new, higher version number.

To recover from a faulty version, restore the needed previous content in `skills/`.\
Then build it as a new version with these same steps.

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

In this repository, run `apm install` and `apm update` only with `--dry-run`.\
Doing so creates consumer manifests, lockfiles, and installed files in the source checkout.

These checks show whether installation and dependencies are intact.\
They do not show whether a client invokes the Skills or follows their instructions.

### 4. Keep the outputs

Keep the ZIP, hash, source commit, change summary, and verification results together, so that each traces to the others.

## ZIP specification

### Generated files

| File | Purpose |
| --- | --- |
| `<name>-<version>.zip` | Plugin ZIP to install |
| `<name>-<version>.sha256` | SHA-256 hash that identifies the ZIP's exact contents |
| `<name>-<version>.build.json` | Source commit, ZIP hash, Skill list, and each packaged file's hash and mode |

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
Keep these settings in the root `plugin.json`, without a separate compatibility `.codex-plugin/plugin.json`.\
When the root `plugin.json` contains an OpenAI extension, only those settings apply.\
They are not merged with the compatibility format.

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

When a Skill changes, review the following yourself, because the builder does not check them:

- References to other files written in generic examples or plain text, rather than as links or code spans
- Whether the tools that the Skill's instructions require are available in the target clients
- Instructions that apply only under certain conditions, and whether those conditions can occur
