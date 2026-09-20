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


def candidate_entry(path: Path, sha256_value: str | None = None, mode: str | None = None) -> dict[str, str]:
    return {
        "sha256": sha256_value or "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
        "mode": mode or ("100755" if path.stat().st_mode & 0o111 else "100644"),
    }


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
                "skill_name": "alpha-skill",
                "evals": [
                    {
                        "id": "alpha-case",
                        "prompt": "Run the alpha case.",
                        "expected_output": "A bounded result.",
                    }
                ],
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
    write(root / "docs" / "authoring.md", "# Authoring\n")


def create_valid_report(root: Path) -> dict[str, object]:
    skill = root / "skills" / "alpha-skill"
    source = skill / "SKILL.md"
    return {
        "schema_version": 2,
        "skill": "alpha-skill",
        "evaluated_on": "2026-09-16",
        "purpose": "Check the selected responsibility.",
        "affected_responsibilities": ["selected responsibility"],
        "selection": {
            "path": "targeted-candidate",
            "cases": [{"id": "alpha-case", "conditions": ["candidate"]}],
        },
        "base": {"commit": "a" * 40},
        "candidate": {
            "files": {
                "SKILL-ja.md": candidate_entry(skill / "SKILL-ja.md"),
                "SKILL.md": candidate_entry(source),
            }
        },
        "evaluation_inputs": {
            "evaluation_files": {
                "skills/alpha-skill/evals/evals.json": "sha256:"
                + hashlib.sha256((skill / "evals" / "evals.json").read_bytes()).hexdigest()
            },
            "case_files": {},
        },
        "environment": {
            "client": "codex-cli test",
            "model": "test-model",
            "reasoning_effort": "test",
            "sandbox": "read-only",
        },
        "checks": {"repository": "pass"},
        "results": [
            {
                "case_id": "alpha-case",
                "condition": "candidate",
                "status": "pass",
                "requirements": [
                    {
                        "id": "expected-output",
                        "status": "pass",
                        "evidence": "The bounded result was present.",
                        "critical": True,
                    }
                ],
                "evidence": "The selected behavior passed.",
            }
        ],
        "summary": {
            "status": "pass",
            "counts": {"error": 0, "fail": 0, "inconclusive": 0, "pass": 1},
        },
        "stopping_reason": "The selected result answered the acceptance question.",
        "unverified": ["Unselected responsibilities"],
    }


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
            report = create_valid_report(root)
            source = root / "skills" / "alpha-skill" / "SKILL.md"
            report["candidate"] = {"files": {"SKILL.md": candidate_entry(source, "sha256:" + "0" * 64)}}
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
            )

        self.assert_fixture_failure(mutate, "candidate hash for `SKILL.md` is stale")

    def test_stale_candidate_mode_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            report = create_valid_report(root)
            source = root / "skills" / "alpha-skill" / "SKILL.md"
            source.chmod(0o755)
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
            )

        self.assert_fixture_failure(mutate, "candidate mode for `SKILL.md` is stale")

    def test_candidate_manifest_entry_requires_valid_hash_and_mode(self) -> None:
        for field, value, expected in (
            ("sha256", "invalid", "must use lowercase sha256"),
            ("mode", "100777", "must be `100644` or `100755`"),
        ):
            def mutate(root: Path) -> None:
                report = create_valid_report(root)
                report["candidate"]["files"]["SKILL.md"][field] = value
                write(
                    root / "skills" / "alpha-skill" / "evals" / "report.json",
                    json.dumps(report),
                )

            with self.subTest(field=field):
                self.assert_fixture_failure(mutate, expected)

    def test_stale_legacy_result_hash_is_not_current_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
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

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_runner_may_ignore_only_the_report_it_is_replacing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            report = create_valid_report(root)
            source = root / "skills" / "alpha-skill" / "SKILL.md"
            report["candidate"] = {"files": {"SKILL.md": candidate_entry(source, "sha256:" + "0" * 64)}}
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(CHECKER),
                    "--root",
                    str(root),
                    "--ignore-report-for-skill",
                    "alpha-skill",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)

    def test_valid_change_scoped_report_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(create_valid_report(root)),
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_repository_local_evaluation_definitions_are_checked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            local = root / ".agents" / "skills" / "maintain-japanese-references"
            write(local / "SKILL.md", "# Local Skill\n")
            definition = local / "evals" / "evals.json"
            write(definition, json.dumps({
                "skill_name": "wrong-name",
                "evals": [{"id": "H", "prompt": "Maintain it.", "expected_output": "Updated."}],
            }))
            result = run_checker(root)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("maintain-japanese-references/evals/evals.json", result.stderr)
            self.assertIn("skill_name", result.stderr)

    def test_migrated_and_legacy_assets_may_not_coexist_for_one_skill(self) -> None:
        def mutate(root: Path) -> None:
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill": "alpha-skill",
                        "version": 1,
                        "cases": [{"id": "route", "prompt": "Route."}],
                    }
                ),
            )

        self.assert_fixture_failure(mutate, "must migrate evals.json and triggers.json together")

    def test_migrated_behavior_and_routing_definitions_may_coexist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": "route",
                                "prompt": "Route this request.",
                                "expected_handlers": ["alpha-skill"],
                            }
                        ],
                    }
                ),
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_migrated_routing_definition_does_not_require_behavior_definition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            (root / "skills" / "alpha-skill" / "evals" / "evals.json").unlink()
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": "route",
                                "prompt": "Route this request.",
                                "expected_handlers": ["alpha-skill"],
                            }
                        ],
                    }
                ),
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_skill_without_executable_definitions_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            (root / "skills" / "alpha-skill" / "evals" / "evals.json").unlink()

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_legacy_assets_remain_valid_until_the_skill_is_migrated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "evals.json",
                json.dumps(
                    {
                        "skill": "alpha-skill",
                        "version": 1,
                        "cases": [{"id": "legacy-case", "input": "Run it."}],
                    }
                ),
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_report_rejects_case_status_that_ignores_critical_failure(self) -> None:
        def mutate(root: Path) -> None:
            report = create_valid_report(root)
            report["results"][0]["requirements"][0]["status"] = "fail"
            report["results"][0]["status"] = "pass"
            write(root / "skills" / "alpha-skill" / "evals" / "report.json", json.dumps(report))

        self.assert_fixture_failure(mutate, "must derive status `fail` from requirement results")

    def test_executor_error_report_does_not_require_fabricated_requirement_grades(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            report = create_valid_report(root)
            report["results"][0].update(
                {
                    "status": "error",
                    "requirements": [],
                    "evidence": "The executor timed out.",
                }
            )
            report["summary"] = {
                "status": "error",
                "counts": {"error": 1, "fail": 0, "inconclusive": 0, "pass": 0},
            }
            write(root / "skills" / "alpha-skill" / "evals" / "report.json", json.dumps(report))

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_report_candidate_manifest_detects_unrecorded_file(self) -> None:
        def mutate(root: Path) -> None:
            report = create_valid_report(root)
            write(root / "skills" / "alpha-skill" / "NEW.md", "Unrecorded.\n")
            write(root / "skills" / "alpha-skill" / "evals" / "report.json", json.dumps(report))

        self.assert_fixture_failure(mutate, "candidate manifest does not match the current Skill tree")

    def test_report_candidate_manifest_rejects_symlinks(self) -> None:
        for kind, target in (
            ("file", "SKILL.md"),
            ("broken", "missing.md"),
            ("directory", "evals"),
        ):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                create_valid_repository(root)
                report = create_valid_report(root)
                (root / "skills" / "alpha-skill" / f"{kind}-link").symlink_to(target)
                write(
                    root / "skills" / "alpha-skill" / "evals" / "report.json",
                    json.dumps(report),
                )

                result = run_checker(root)

                self.assertNotEqual(0, result.returncode)
                self.assertIn("candidate Skill tree must not contain symlink", result.stderr)

    def test_report_result_must_match_selected_case_condition(self) -> None:
        def mutate(root: Path) -> None:
            report = create_valid_report(root)
            report["results"][0]["condition"] = "baseline"
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
            )

        self.assert_fixture_failure(mutate, "report results must exactly match selected case-condition pairs")

    def test_report_rejects_raw_response_field(self) -> None:
        def mutate(root: Path) -> None:
            report = create_valid_report(root)
            report["response"] = "full model response"
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
            )

        self.assert_fixture_failure(mutate, "report must not contain raw artifact field `response`")

    def test_report_rejects_plan_snapshot_and_absolute_path(self) -> None:
        def add_plan(root: Path) -> None:
            report = create_valid_report(root)
            report["plan"] = {"schema_version": 2}
            write(root / "skills" / "alpha-skill" / "evals" / "report.json", json.dumps(report))

        def add_path(root: Path) -> None:
            report = create_valid_report(root)
            report["unverified"] = ["Inspect /tmp/evaluation later."]
            write(root / "skills" / "alpha-skill" / "evals" / "report.json", json.dumps(report))

        self.assert_fixture_failure(add_plan, "raw artifact field `plan`")
        self.assert_fixture_failure(add_path, "report must not contain absolute path `/tmp/evaluation`")

    def test_report_requires_execution_environment(self) -> None:
        def mutate(root: Path) -> None:
            report = create_valid_report(root)
            report["environment"] = {"client": "codex-cli test"}
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
            )

        self.assert_fixture_failure(mutate, "report environment fields must be non-empty strings")

    def test_report_must_grade_every_assertion_assigned_to_selected_case(self) -> None:
        def mutate(root: Path) -> None:
            evals = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(evals.read_text())
            document["evals"][0]["assertions"] = [
                {"id": "required-assertion", "text": "Required.", "critical": True}
            ]
            write(evals, json.dumps(document))
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(create_valid_report(root)),
            )

        self.assert_fixture_failure(mutate, "must grade every assigned assertion")

    def test_candidate_manifest_may_not_use_adjacent_skill_paths(self) -> None:
        def mutate(root: Path) -> None:
            source = root / "skills" / "alpha-skill" / "SKILL.md"
            report = create_valid_report(root)
            report["candidate"] = {"files": {"../alpha-skill/SKILL.md": candidate_entry(source)}}
            write(root / "skills" / "alpha-skill" / "evals" / "report.json", json.dumps(report))

        self.assert_fixture_failure(mutate, "candidate manifest does not match the current Skill tree")

    def test_candidate_file_may_not_escape_skills_tree(self) -> None:
        def mutate(root: Path) -> None:
            source = root / "README.md"
            report = create_valid_report(root)
            report["candidate"] = {"files": {"../../README.md": candidate_entry(source)}}
            write(
                root / "skills" / "alpha-skill" / "evals" / "report.json",
                json.dumps(report),
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

    def test_tracked_repository_local_skills_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            name = "maintain-japanese-references"
            write(root / ".agents" / "skills" / name / "SKILL.md", f"# {name}\n")
            write(
                root / ".agents" / "skills" / name / "SKILL-ja.md",
                "> **注記:** 英語版 (`SKILL.md`) が正本です。このファイルは参考訳です。\n",
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

    def test_invalid_json_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            write(root / "skills" / "alpha-skill" / "evals" / "broken.json", "{\n")

        self.assert_fixture_failure(mutate, "invalid JSON")

    def test_duplicate_case_id_is_detected(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["evals"].append(
                {
                    "id": "alpha-case",
                    "prompt": "Duplicate.",
                    "expected_output": "Duplicate.",
                }
            )
            path.write_text(json.dumps(document))

        self.assert_fixture_failure(mutate, "duplicate case id `alpha-case`")

    def test_official_eval_shape_accepts_numeric_case_id_without_schema_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "evals.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": 1,
                                "prompt": "Run the official-shaped case.",
                                "expected_output": "A bounded result.",
                                "files": [],
                            }
                        ],
                    }
                ),
            )

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_official_eval_shape_accepts_transcript_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            case = document["evals"][0]
            case.pop("prompt")
            case["turns"] = [
                {"role": "user", "content": "Start the task."},
                {"role": "assistant", "content": "What should I preserve?"},
                "Preserve the existing boundary.",
            ]
            write(path, json.dumps(document))

            result = run_checker(root)

            self.assertEqual(0, result.returncode, result.stderr)

    def test_official_eval_shape_rejects_unhashable_turn_role(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            case = document["evals"][0]
            case.pop("prompt")
            case["turns"] = [{"role": [], "content": "Hello."}]
            write(path, json.dumps(document))

        stderr = self.assert_fixture_failure(mutate, "role must be user or assistant")
        self.assertNotIn("Traceback", stderr)

    def test_official_eval_shape_requires_candidate_in_explicit_conditions(self) -> None:
        for conditions in ([], ["baseline"], ["without-skill"]):
            with self.subTest(conditions=conditions):
                def mutate(root: Path) -> None:
                    path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                    document = json.loads(path.read_text())
                    document["evals"][0]["conditions"] = conditions
                    write(path, json.dumps(document))

                self.assert_fixture_failure(mutate, "conditions must include candidate")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["evals"][0]["conditions"] = ["candidate", "without-skill"]
            write(path, json.dumps(document))
            result = run_checker(root)
            self.assertEqual(0, result.returncode, result.stderr)

    def test_official_eval_rejects_missing_file_in_unselected_case(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["evals"].append(
                {"id": "unselected", "prompt": "Run it.", "expected_output": "Result.", "files": ["missing.txt"]}
            )
            write(path, json.dumps(document))

        self.assert_fixture_failure(mutate, "evaluation case `unselected` input file must be a regular repository file: missing.txt")

    def test_official_routing_definition_rejects_missing_file(self) -> None:
        def mutate(root: Path) -> None:
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps({"skill_name": "alpha-skill", "evals": [
                    {"id": "routing", "prompt": "Route it.", "expected_handlers": [], "files": ["missing.txt"]}
                ]}),
            )

        self.assert_fixture_failure(mutate, "evaluation case `routing` input file must be a regular repository file: missing.txt")

    def test_official_eval_rejects_missing_coexistence_skills(self) -> None:
        for location, expected in (
            ("execution", "evaluation execution coexistence Skill must have a regular SKILL.md: missing-skill"),
            ("case", "evaluation case `alpha-case` coexistence Skill must have a regular SKILL.md: missing-skill"),
        ):
            with self.subTest(location=location):
                def mutate(root: Path) -> None:
                    path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                    document = json.loads(path.read_text())
                    if location == "execution":
                        document["execution"] = {"coexistence_skills": ["missing-skill"]}
                    else:
                        document["evals"][0]["coexistence_skills"] = ["missing-skill"]
                    write(path, json.dumps(document))

                self.assert_fixture_failure(mutate, expected)

    def test_official_eval_accepts_existing_file_and_coexistence_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["execution"] = {"coexistence_skills": ["alpha-skill"]}
            document["evals"][0]["files"] = ["README.md"]
            document["evals"][0]["coexistence_skills"] = ["alpha-skill"]
            write(path, json.dumps(document))

            result = run_checker(root)
            self.assertEqual(0, result.returncode, result.stderr)

    def test_official_eval_shape_rejects_unknown_case_fields(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["evals"][0]["unused"] = "ignored before the executable contract"
            write(path, json.dumps(document))

        self.assert_fixture_failure(mutate, "evaluation case contains unknown field(s): unused")

    def test_official_eval_files_require_safe_repository_relative_paths(self) -> None:
        for value in ("/tmp/input.txt", "../outside.txt", r"C:\fixtures\input.txt"):
            with self.subTest(value=value):
                def mutate(root: Path) -> None:
                    path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                    document = json.loads(path.read_text())
                    document["evals"][0]["files"] = [value]
                    path.write_text(json.dumps(document))

                self.assert_fixture_failure(
                    mutate,
                    "evaluation case `alpha-case` has an unsafe case input path",
                )

    def test_official_eval_files_reject_duplicates_after_normalization(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(path.read_text())
            document["evals"][0]["files"] = ["inputs/request.txt", "inputs//request.txt"]
            path.write_text(json.dumps(document))

        self.assert_fixture_failure(mutate, "evaluation case `alpha-case` repeats a file path")

    def test_official_eval_shape_rejects_paths_that_cannot_be_materialized(self) -> None:
        invalid_cases = (
            ({"files": ["inputs/bad\0name.txt"]}, "unsafe case input path"),
            (
                {"fixture": {"files": {"a": "file", "a/b": "nested"}}},
                "fixture file paths conflict: `a` and `a/b`",
            ),
            (
                {
                    "files": ["source.txt"],
                    "fixture": {"files": {"inputs/source.txt": "inline"}},
                },
                "case file `source.txt` and fixture file `inputs/source.txt` conflict",
            ),
            (
                {
                    "files": ["source.txt"],
                    "fixture": {"files": {"inputs": "inline"}},
                },
                "case file `source.txt` and fixture file `inputs` conflict",
            ),
        )
        for changes, expected in invalid_cases:
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                create_valid_repository(root)
                path = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                document = json.loads(path.read_text())
                document["evals"][0].update(changes)
                write(path, json.dumps(document))

                result = run_checker(root)

                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

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

    def test_repository_local_companion_relationship(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_repository(root)
            local_skill = root / ".agents" / "skills" / "maintain-japanese-references" / "SKILL.md"
            write(local_skill, "Read skills/alpha-skill/SKILL.md before deciding.\n")
            write(
                root / "docs" / "authoring.md",
                """# Authoring

| Relationship | Rationale | Installation | Provenance | Evaluation |
| --- | --- | --- | --- | --- |
| `maintain-japanese-references` → `alpha-skill` | test | Read both repository files | [#42](https://github.com/mtk177a/skills/pull/42) | `evals/README.md` |
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
