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

    def test_broken_relative_markdown_link_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "README.md"
            path.write_text(path.read_text() + "\n[Missing](docs/missing.md)\n")

        self.assert_fixture_failure(mutate, "relative Markdown link target does not exist: `docs/missing.md`")

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
