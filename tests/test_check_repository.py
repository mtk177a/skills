import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_repository.py"
REFERENCE_NOTICE = (
    "> **注記:** この Skill の内容は英語版 (`SKILL.md`) を基準とします。\n"
    "> このファイルは参考訳です。\n"
    "> 内容に差異がある場合は英語版を優先してください。\n"
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def create_valid_repository(root: Path) -> None:
    skill = root / "skills" / "alpha-skill"
    write(
        skill / "SKILL.md",
        """---
name: alpha-skill
description: Checks a fixture Skill.
license: MIT
---

# Alpha Skill
""",
    )
    write(
        skill / "SKILL-ja.md",
        f"""---
name: alpha-skill
description: fixture の Skill を確認する。
license: MIT
---

{REFERENCE_NOTICE}
# Alpha Skill
""",
    )
    write(
        root / "README.md",
        """# Fixture

1 Skills.

| Skill | Description |
| --- | --- |
| `alpha-skill` | Fixture |
""",
    )
    write(
        root / "README.ja.md",
        """# Fixture

1 の Skill。

| Skill | 説明 |
| --- | --- |
| `alpha-skill` | Fixture |
""",
    )
    write(root / "docs" / "authoring.md", "# Authoring\n")


def rename_fixture_skill(root: Path, name: str) -> None:
    source = root / "skills" / "alpha-skill"
    target = root / "skills" / name
    source.rename(target)
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        path.write_text(path.read_text().replace("alpha-skill", name), encoding="utf-8")


def run_checker(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


class CheckerCliTests(unittest.TestCase):
    def test_valid_repository_passes_without_modification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            before = tree_hash(root)

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(before, tree_hash(root))

    def test_catalogs_can_omit_declared_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            english = root / "README.md"
            japanese = root / "README.ja.md"
            english.write_text(english.read_text().replace("1 Skills.", "This repository includes the following Skills."))
            japanese.write_text(japanese.read_text().replace("1 の Skill。", "以下の Skill を収録しています。"))

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def assert_fixture_failure(self, mutate, expected: str) -> str:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            mutate(root)
            result = run_checker(root)
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn(expected, result.stderr)
            return result.stderr

    def test_catalog_mismatch_is_file_specific(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "README.md"
            path.write_text(path.read_text().replace("| `alpha-skill` | Fixture |\n", ""))

        self.assert_fixture_failure(mutate, "README.md:1: catalog is missing Skill `alpha-skill`")

    def test_frontmatter_name_must_match_directory(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL.md"
            path.write_text(path.read_text().replace("name: alpha-skill", "name: other-skill"))

        self.assert_fixture_failure(mutate, "frontmatter name `other-skill` does not match directory `alpha-skill`")

    def test_upstream_mirrors_can_omit_local_license(self) -> None:
        for name in ("japanese-tech-writing", "cognitive-rhythm-writing"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                create_valid_repository(root)
                rename_fixture_skill(root, name)
                skill = root / "skills" / name
                source = skill / "SKILL.md"
                source.write_text(source.read_text().replace("license: MIT\n", ""))
                digest = hashlib.sha256(source.read_bytes()).hexdigest()
                write(
                    skill / "UPSTREAM.md",
                    f"# Upstream provenance\n\n"
                    f"- Source: <https://gist.github.com/k16shikano/{'fd287c3133457c4fd8f5601d34aa817d' if name == 'japanese-tech-writing' else 'eb2929f13ed19c97188393d297be8432'}>\n"
                    f"- Mirrored revision: `{'a' * 40}`\n"
                    "- Retrieved: `2026-10-05`\n"
                    f"- SKILL.md SHA-256: `sha256:{digest}`\n"
                    "- License: Unlicense\n"
                    "- License declaration: <https://gist.github.com/k16shikano/67625f2a7d96e3bbdfae8d571a936063>\n",
                )

                result = run_checker(root)

                self.assertEqual(0, result.returncode, result.stderr)

    def test_upstream_mirror_detects_changed_source(self) -> None:
        def mutate(root: Path) -> None:
            rename_fixture_skill(root, "japanese-tech-writing")
            skill = root / "skills" / "japanese-tech-writing"
            write(
                skill / "UPSTREAM.md",
                "# Upstream provenance\n\n"
                "- Source: <https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d>\n"
                f"- Mirrored revision: `{'a' * 40}`\n"
                "- Retrieved: `2026-10-05`\n"
                f"- SKILL.md SHA-256: `sha256:{'0' * 64}`\n"
                "- License: Unlicense\n"
                "- License declaration: <https://gist.github.com/k16shikano/67625f2a7d96e3bbdfae8d571a936063>\n",
            )

        self.assert_fixture_failure(mutate, "mirrored SKILL.md differs from recorded SHA-256")

    def test_non_mirrored_skill_still_requires_license(self) -> None:
        def mutate(root: Path) -> None:
            source = root / "skills" / "alpha-skill" / "SKILL.md"
            source.write_text(source.read_text().replace("license: MIT\n", ""))

        self.assert_fixture_failure(mutate, "required frontmatter `license` is missing or empty")

    def test_quoted_frontmatter_name_is_normalized(self) -> None:
        for quoted_name in ('"alpha-skill"', "'alpha-skill'", r'"alpha\x2dskill"'):
            with self.subTest(quoted_name=quoted_name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                create_valid_repository(root)
                path = root / "skills" / "alpha-skill" / "SKILL.md"
                path.write_text(path.read_text().replace("name: alpha-skill", f"name: {quoted_name}"))

                result = run_checker(root)

                self.assertEqual(0, result.returncode, result.stderr)

    def test_frontmatter_name_length_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            rename_fixture_skill(root, "a" * 64)

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_frontmatter_name_over_64_characters_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            rename_fixture_skill(root, "a" * 65)

        self.assert_fixture_failure(mutate, "frontmatter `name` exceeds 64 characters")

    def test_frontmatter_description_length_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            path = root / "skills" / "alpha-skill" / "SKILL.md"
            path.write_text(path.read_text().replace(
                "description: Checks a fixture Skill.",
                f'description: {"a" * 1024}',
            ))

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_frontmatter_description_over_1024_characters_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL.md"
            path.write_text(path.read_text().replace(
                "description: Checks a fixture Skill.",
                f'description: {"a" * 1025}',
            ))

        self.assert_fixture_failure(mutate, "frontmatter `description` exceeds 1024 characters")

    def test_unsupported_frontmatter_scalar_is_rejected(self) -> None:
        for replacement in ("description: >\n  Checks a fixture Skill.", "description: [fixture]"):
            with self.subTest(replacement=replacement):
                def mutate(root: Path) -> None:
                    path = root / "skills" / "alpha-skill" / "SKILL.md"
                    path.write_text(path.read_text().replace(
                        "description: Checks a fixture Skill.",
                        replacement,
                    ))

                self.assert_fixture_failure(
                    mutate,
                    "frontmatter `description` must use a supported single-line string scalar",
                )

    def test_broken_relative_markdown_link_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "README.md"
            path.write_text(path.read_text() + "\n[Missing](docs/missing.md)\n")

        self.assert_fixture_failure(mutate, "relative Markdown link target does not exist: `docs/missing.md`")

    def test_link_inside_multi_backtick_code_span_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            path = root / "README.md"
            path.write_text(path.read_text() + "\n``[Example](docs/missing.md)``\n")

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_unequal_backtick_runs_do_not_close_code_span(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "README.md"
            path.write_text(path.read_text() + "\n``[Missing](docs/missing.md)```\n")

        self.assert_fixture_failure(mutate, "relative Markdown link target does not exist: `docs/missing.md`")

    def test_shorter_fence_does_not_close_longer_fenced_block(self) -> None:
        for marker in ("`", "~"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                create_valid_repository(root)
                path = root / "README.md"
                path.write_text(
                    path.read_text()
                    + f"\n{marker * 4}text\n[First](docs/first-missing.md)\n{marker * 3}\n"
                    + f"[Second](docs/second-missing.md)\n{marker * 4}\n"
                )

                result = run_checker(root)

                self.assertEqual(0, result.returncode, result.stderr)

    def test_missing_reference_notice_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL-ja.md"
            path.write_text(path.read_text().replace(REFERENCE_NOTICE, ""))

        self.assert_fixture_failure(mutate, "Japanese translation must begin with a notice")

    def test_reference_notice_accepts_equivalent_wording(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            path = root / "skills" / "alpha-skill" / "SKILL-ja.md"
            path.write_text(path.read_text().replace(
                REFERENCE_NOTICE,
                "> **注記:** このファイルは英語版 (`SKILL.md`) の参考訳です。\n"
                "> 内容が異なる場合は英語版に従ってください。\n",
            ))

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_notice_without_reference_status_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL-ja.md"
            path.write_text(path.read_text().replace(
                "> このファイルは参考訳です。\n",
                "",
            ))

        self.assert_fixture_failure(mutate, "Japanese translation must begin with a notice")

    def test_notice_without_english_skill_source_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL-ja.md"
            path.write_text(path.read_text().replace("`SKILL.md`", "`別ファイル.md`"))

        self.assert_fixture_failure(mutate, "Japanese translation must begin with a notice")

    def test_notice_after_heading_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL-ja.md"
            path.write_text(path.read_text().replace(
                REFERENCE_NOTICE,
                "# Alpha Skill\n" + REFERENCE_NOTICE,
            ))

        self.assert_fixture_failure(mutate, "Japanese translation must begin with a notice")

    def test_tracked_repository_local_skills_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            name = "maintain-japanese-references"
            write(root / ".agents" / "skills" / name / "SKILL.md", f"# {name}\n")
            write(
                root / ".agents" / "skills" / name / "SKILL-ja.md",
                REFERENCE_NOTICE,
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_source_apm_manifest_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "apm.yml", "name: fixture\n")

        self.assert_fixture_failure(mutate, "source repository must not contain `apm.yml`")

    def test_source_apm_lockfile_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "apm.lock.yaml", "lockfile_version: '1'\n")

        self.assert_fixture_failure(mutate, "source repository must not contain `apm.lock.yaml`")

    def test_retired_refresh_skill_is_rejected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / ".agents" / "skills" / "refresh-apm-lockfile" / "SKILL.md", "# retired\n")

        self.assert_fixture_failure(mutate, "unexpected APM-deployed Skill")

    def test_repository_local_translation_notice_is_required(self) -> None:
        def mutate(root: Path) -> None:
            write(
                root / ".agents" / "skills" / "maintain-japanese-references" / "SKILL-ja.md",
                "# 訳\n",
            )

        self.assert_fixture_failure(mutate, "Japanese translation must begin with a notice")

    def test_personal_absolute_path_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "docs" / "local.md", "Use `/home/alice/private/config`.\n")

        self.assert_fixture_failure(mutate, "prohibited environment-specific absolute path `/home/alice`")

    def test_personal_absolute_path_in_python_source_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "scripts" / "local-path.py", 'CONFIG = "/Users/alice/private/config"\n')

        self.assert_fixture_failure(
            mutate,
            "scripts/local-path.py:1: prohibited environment-specific absolute path `/Users/alice`",
        )

    def test_intentional_personal_path_in_checker_test_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            write(
                root / "tests" / "test_check_repository.py",
                'EXAMPLE = "/Users/alice/private/config"\n',
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_unexpected_deployment_artifact_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / ".agents" / "skills" / "deployed-skill" / "SKILL.md", "# generated\n")

        self.assert_fixture_failure(mutate, "unexpected APM-deployed Skill")

    def test_companion_relationship_requires_skill_reference(self) -> None:
        def mutate(root: Path) -> None:
            write(
                root / "docs" / "authoring.md",
                """# Authoring

| Relationship | Rationale | Installation | Provenance |
| --- | --- | --- | --- |
| `alpha-skill` → `alpha-skill` | test | install | [UPSTREAM.md](../skills/alpha-skill/UPSTREAM.md) |
""",
            )

        self.assert_fixture_failure(mutate, "companion Skill reference `../alpha-skill/SKILL.md` is missing")

    def test_repository_local_companion_relationship(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            local_skill = root / ".agents" / "skills" / "maintain-japanese-references" / "SKILL.md"
            write(local_skill, "Read skills/alpha-skill/SKILL.md before deciding.\n")
            write(
                root / "docs" / "authoring.md",
                """# Authoring

| Relationship | Rationale | Installation | Provenance |
| --- | --- | --- | --- |
| `maintain-japanese-references` → `alpha-skill` | test | Read both repository files | [#42](https://github.com/mtk177a/skills/pull/42) |
""",
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)
            write(local_skill, "Do the work without the companion.\n")
            result = run_checker(root)
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn("companion Skill reference `skills/alpha-skill/SKILL.md` is missing", result.stderr)

    def test_diagnostics_have_stable_path_order(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "docs" / "z.md", "Use `/home/z/private`.\n")
            write(root / "docs" / "a.md", "Use `/home/a/private`.\n")

        stderr = self.assert_fixture_failure(mutate, "prohibited environment-specific absolute path")
        diagnostic_paths = [line.split(":", 1)[0] for line in stderr.splitlines()]
        self.assertEqual(sorted(diagnostic_paths), diagnostic_paths)

    def test_invalid_root_returns_usage_error(self) -> None:
        missing = REPOSITORY_ROOT / "tests" / "does-not-exist"
        result = run_checker(missing)
        self.assertEqual(2, result.returncode)
        self.assertIn("repository root is not a directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
