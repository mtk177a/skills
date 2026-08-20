import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "check_repository.py"


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
        """---
name: alpha-skill
description: fixture の Skill を確認する。
license: MIT
---

> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳です。

# Alpha Skill
""",
    )
    write(skill / "evals" / "README.md", "# alpha-skill evals\n")
    write(
        skill / "evals" / "evals.json",
        json.dumps(
            {
                "skill": "alpha-skill",
                "version": 1,
                "cases": [{"id": "alpha-case"}],
            },
            indent=2,
        )
        + "\n",
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
    write(
        root / "apm.yml",
        """dependencies:
  apm:
    - example/skills/skills/alpha-skill
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

    def test_stale_candidate_hash_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            write(
                root / "skills" / "alpha-skill" / "evals" / "results.json",
                json.dumps(
                    {
                        "schema_version": 3,
                        "skill": "alpha-skill",
                        "candidate": {"files": {"SKILL.md": "sha256:" + "0" * 64}},
                    }
                ),
            )

        self.assert_fixture_failure(mutate, "candidate hash for `SKILL.md` is stale")

    def test_candidate_file_may_bind_an_adjacent_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            source = root / "skills" / "alpha-skill" / "SKILL.md"
            expected = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            write(
                root / "skills" / "alpha-skill" / "evals" / "results.json",
                json.dumps(
                    {
                        "schema_version": 3,
                        "skill": "alpha-skill",
                        "candidate": {"files": {"../alpha-skill/SKILL.md": expected}},
                    }
                ),
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_candidate_file_may_not_escape_skills_tree(self) -> None:
        def mutate(root: Path) -> None:
            source = root / "README.md"
            expected = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
            write(
                root / "skills" / "alpha-skill" / "evals" / "results.json",
                json.dumps(
                    {
                        "schema_version": 3,
                        "skill": "alpha-skill",
                        "candidate": {"files": {"../../README.md": expected}},
                    }
                ),
            )

        self.assert_fixture_failure(mutate, "candidate file escapes repository skills tree")

    def test_missing_canonical_source_notice_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "SKILL-ja.md"
            path.write_text(path.read_text().replace(
                "> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳です。\n\n",
                "",
            ))

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

    def test_invalid_json_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "skills" / "alpha-skill" / "evals" / "broken.json", "{\n")

        self.assert_fixture_failure(mutate, "invalid JSON")

    def test_duplicate_case_id_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["cases"].append({"id": "alpha-case"})
            path.write_text(json.dumps(document))

        self.assert_fixture_failure(mutate, "duplicate case id `alpha-case`")

    def test_companion_relationship_requires_skill_reference(self) -> None:
        def mutate(root: Path) -> None:
            write(
                root / "docs" / "authoring.md",
                """# Authoring

| Relationship | Rationale | Installation | Provenance | Evaluation |
| --- | --- | --- | --- | --- |
| `alpha-skill` → `alpha-skill` | test | install | [UPSTREAM.md](../skills/alpha-skill/UPSTREAM.md) | [evals/README.md](../skills/alpha-skill/evals/README.md) |
""",
            )

        self.assert_fixture_failure(mutate, "companion Skill reference `../alpha-skill/SKILL.md` is missing")

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
