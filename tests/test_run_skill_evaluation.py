import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.run_skill_evaluation import (
    EvaluationError,
    attach_plan_digest,
    canonical_json,
    copy_baseline_skill,
    copy_manifest,
    direct_skill_load_observation,
    observed_skill_handlers,
    skill_manifest,
    verify_file_manifest,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPOSITORY_ROOT / "scripts" / "run_skill_evaluation.py"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_repository(root: Path) -> None:
    write(
        root / "skills" / "alpha-skill" / "SKILL.md",
        """---
name: alpha-skill
description: Exercises an evaluation fixture.
license: MIT
---

# Alpha Skill
""",
    )
    write(
        root / "skills" / "alpha-skill" / "evals" / "evals.json",
        json.dumps(
            {
                "skill_name": "alpha-skill",
                "evals": [
                    {
                        "id": "selected",
                        "prompt": "Run the selected case.",
                        "expected_output": "A bounded result.",
                    },
                    {
                        "id": "not-selected",
                        "prompt": "Do not run this case.",
                        "expected_output": "No execution.",
                    },
                ],
            }
        )
        + "\n",
    )
    write(root / "scripts" / "check_repository.py", "raise SystemExit(0)\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)


def create_fake_codex(path: Path, mode: str = "success") -> None:
    write(
        path,
        f"""#!/usr/bin/env python3
import json
import pathlib
import sys
import time

if "--version" in sys.argv:
    print("codex-cli fake")
    raise SystemExit(0)
output = pathlib.Path(sys.argv[sys.argv.index("--output-last-message") + 1])
skill = pathlib.Path.cwd() / ".agents" / "skills" / "alpha-skill" / "SKILL.md"
state = skill.read_text() if skill.exists() else "without-skill"
prompt = sys.stdin.read()
output.write_text("final: " + state, encoding="utf-8")
if {mode!r} == "timeout":
    time.sleep(5)
elif {mode!r} == "invalid-jsonl":
    print("not-json")
elif {mode!r} == "unexposed":
    print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": "I used /skills/alpha-skill/SKILL.md"}}}}))
elif {mode!r} == "non-trigger":
    print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": "No Skill was needed."}}}}))
    print(json.dumps({{"type": "turn.completed", "usage": {{"input_tokens": 1, "output_tokens": 1}}}}))
else:
    print(json.dumps({{"type": "item.completed", "item": {{"type": "command_execution", "command": "read " + str(skill), "exit_code": 0}}}}))
    print(json.dumps({{"type": "turn.completed", "usage": {{"input_tokens": 1, "output_tokens": 1}}}}))
log = pathlib.Path(sys.argv[sys.argv.index("-C") + 1]) / "invocation.json"
log.write_text(json.dumps({{"argv": sys.argv[1:], "prompt": prompt, "state": state}}), encoding="utf-8")
""",
    )
    path.chmod(0o755)


def create_manual_plan(root: Path, path: Path) -> None:
    commit = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    write(
        path,
        json.dumps(
            attach_plan_digest({
                "schema_version": 2,
                "skill": "alpha-skill",
                "path": "targeted-candidate",
                "purpose": "Check grade matching.",
                "affected_responsibilities": ["grade matching"],
                "base": {"ref": "HEAD", "commit": commit},
                "environment": {"model": "test", "reasoning_effort": "test", "sandbox": "read-only"},
                "cases": [
                    {
                        "id": "selected",
                        "prompt": "Run it.",
                        "grading_requirements": [
                            {"id": "expected-output", "text": "A bounded result.", "critical": True}
                        ],
                        "files": [],
                        "inline_files": {},
                        "coexistence_skills": [],
                        "input_mode": "single-turn",
                    }
                ],
                "executions": [{"case_id": "selected", "condition": "candidate"}],
                "estimated_model_calls": 1,
                "candidate": {
                    "files": {
                        "SKILL.md": {
                            "sha256": "sha256:"
                            + hashlib.sha256(
                                (root / "skills" / "alpha-skill" / "SKILL.md").read_bytes()
                            ).hexdigest(),
                            "mode": "100644",
                        }
                    }
                },
                "inputs": {"evaluation_files": {}, "case_files": {}, "companions": {}},
                "coexistence_skills": [],
            })
        )
        + "\n",
    )


def create_manual_run(plan_path: Path, run_path: Path) -> None:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    write(
        run_path,
        json.dumps(
            {
                "schema_version": 2,
                "skill": plan["skill"],
                "plan_digest": plan["plan_digest"],
                "plan": plan,
                "client": "codex-cli fake",
                "environment": plan["environment"],
                "static_check": {"status": "pass", "exit_code": 0},
                "executions": [
                    {"case_id": "selected", "condition": "candidate", "status": "completed"}
                ],
            }
        )
        + "\n",
    )


class SkillEvaluationRunnerTests(unittest.TestCase):
    def test_candidate_manifest_detects_changed_and_deleted_files(self) -> None:
        for mutation in ("change", "delete"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as repository:
                root = Path(repository)
                create_repository(root)
                skill_root = root / "skills" / "alpha-skill"
                manifest = skill_manifest(root, "alpha-skill")
                if mutation == "change":
                    write(skill_root / "SKILL.md", "Changed after planning.\n")
                else:
                    (skill_root / "SKILL.md").unlink()

                with self.assertRaisesRegex(EvaluationError, "manifest changed after planning"):
                    verify_file_manifest(skill_root, manifest, "candidate Skill")

    def test_candidate_manifest_preserves_and_verifies_executable_mode(self) -> None:
        with tempfile.TemporaryDirectory() as repository:
            root = Path(repository)
            create_repository(root)
            skill_root = root / "skills" / "alpha-skill"
            helper = skill_root / "scripts" / "tool.sh"
            write(helper, "#!/bin/sh\nexit 0\n")
            helper.chmod(0o755)

            manifest = skill_manifest(root, "alpha-skill")

            self.assertEqual(
                {"sha256": "sha256:" + hashlib.sha256(helper.read_bytes()).hexdigest(), "mode": "100755"},
                manifest["scripts/tool.sh"],
            )
            helper.chmod(0o644)
            with self.assertRaisesRegex(EvaluationError, "manifest changed after planning"):
                verify_file_manifest(skill_root, manifest, "candidate Skill")

            helper.chmod(0o755)
            destination = root / "fixture" / "alpha-skill"
            copy_manifest(skill_root, manifest, destination)
            self.assertEqual(0o755, (destination / "scripts" / "tool.sh").stat().st_mode & 0o777)

    def test_baseline_copy_preserves_git_executable_mode(self) -> None:
        with tempfile.TemporaryDirectory() as repository:
            root = Path(repository)
            create_repository(root)
            helper = root / "skills" / "alpha-skill" / "scripts" / "tool.sh"
            write(helper, "#!/bin/sh\nexit 0\n")
            helper.chmod(0o755)
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "add executable helper"], check=True)
            commit = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip()
            destination = root / "baseline" / "alpha-skill"

            copy_baseline_skill(root, "alpha-skill", commit, destination)

            self.assertEqual(0o755, (destination / "scripts" / "tool.sh").stat().st_mode & 0o777)
            self.assertEqual(0o644, (destination / "SKILL.md").stat().st_mode & 0o777)

    def test_baseline_copy_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as repository:
            root = Path(repository)
            create_repository(root)
            link = root / "skills" / "alpha-skill" / "linked-skill.md"
            link.symlink_to("SKILL.md")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "add symlink"], check=True)
            commit = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip()

            with self.assertRaisesRegex(EvaluationError, "unsupported entry"):
                copy_baseline_skill(root, "alpha-skill", commit, root / "baseline" / "alpha-skill")

    def test_run_rejects_candidate_tree_changed_after_planning(self) -> None:
        for mutation in ("add", "mode"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                plan_path = Path(output) / "plan.json"
                subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "plan",
                        "--skill",
                        "alpha-skill",
                        "--path",
                        "targeted-candidate",
                        "--purpose",
                        "Bind the candidate tree.",
                        "--affected",
                        "candidate integrity",
                        "--case",
                        "selected",
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(plan_path),
                    ],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                if mutation == "add":
                    write(root / "skills" / "alpha-skill" / "NEW.md", "Unplanned file.\n")
                else:
                    (root / "skills" / "alpha-skill" / "SKILL.md").chmod(0o755)

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "--codex-bin",
                        "/bin/false",
                        "run",
                        "--plan",
                        str(plan_path),
                        "--artifacts-dir",
                        str(Path(output) / "artifacts"),
                        "--execute",
                        "--max-model-calls",
                        "1",
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(2, result.returncode)
                self.assertIn("candidate Skill manifest changed after planning", result.stderr)
                self.assertFalse((Path(output) / "artifacts").exists())

    def test_run_rejects_changed_evaluation_and_case_inputs(self) -> None:
        for changed_input, expected in (
            ("evaluation", "evaluation input changed after planning"),
            ("case", "case input changed after planning"),
        ):
            with self.subTest(changed_input=changed_input), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                input_file = root / "inputs" / "request.txt"
                write(input_file, "Original input.\n")
                asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                write(
                    asset,
                    json.dumps(
                        {
                            "skill_name": "alpha-skill",
                            "evals": [
                                {
                                    "id": "selected",
                                    "prompt": "Use the input.",
                                    "expected_output": "A bounded result.",
                                    "files": ["inputs/request.txt"],
                                }
                            ],
                        }
                    )
                    + "\n",
                )
                plan_path = Path(output) / "plan.json"
                subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "plan",
                        "--skill",
                        "alpha-skill",
                        "--path",
                        "targeted-candidate",
                        "--purpose",
                        "Bind evaluation inputs.",
                        "--affected",
                        "input integrity",
                        "--case",
                        "selected",
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(plan_path),
                    ],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                if changed_input == "evaluation":
                    write(asset, asset.read_text(encoding="utf-8") + "\n")
                else:
                    write(input_file, "Changed input.\n")

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "--codex-bin",
                        "/bin/false",
                        "run",
                        "--plan",
                        str(plan_path),
                        "--artifacts-dir",
                        str(Path(output) / "artifacts"),
                        "--execute",
                        "--max-model-calls",
                        "1",
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stderr)
                self.assertFalse((Path(output) / "artifacts").exists())

    def test_run_rejects_changed_companion_skill(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(root / "skills" / "beta-skill" / "SKILL.md", "# Beta Skill\n")
            asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            write(
                asset,
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "execution": {"coexistence_skills": ["beta-skill"]},
                        "evals": [
                            {
                                "id": "selected",
                                "prompt": "Run with the companion.",
                                "expected_output": "A bounded result.",
                            }
                        ],
                    }
                )
                + "\n",
            )
            plan_path = Path(output) / "plan.json"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Bind the companion.",
                    "--affected",
                    "coexistence",
                    "--case",
                    "selected",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            write(root / "skills" / "beta-skill" / "SKILL.md", "# Changed Beta Skill\n")

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    "/bin/false",
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(Path(output) / "artifacts"),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("companion beta-skill Skill manifest changed after planning", result.stderr)
            self.assertFalse((Path(output) / "artifacts").exists())

    def test_routing_observation_requires_completed_successful_read(self) -> None:
        skill_path = "/tmp/fixture/.agents/skills/alpha-skill/SKILL.md"
        events = [
            {
                "type": "item.started",
                "item": {"type": "command_execution", "command": f"cat {skill_path}", "exit_code": None},
            },
            {
                "type": "item.completed",
                "item": {"type": "command_execution", "command": f"cat {skill_path}", "exit_code": 1},
            },
        ]
        self.assertEqual("not_exposed", direct_skill_load_observation(events, "alpha-skill"))
        events[-1]["item"]["exit_code"] = 0
        self.assertEqual("observed", direct_skill_load_observation(events, "alpha-skill"))

    def test_routing_observation_distinguishes_completed_empty_stream(self) -> None:
        completed = [
            {"type": "item.completed", "item": {"type": "agent_message", "text": "No Skill needed."}},
            {"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}},
        ]
        incomplete = [
            {"type": "item.completed", "item": {"type": "agent_message", "text": "No Skill needed."}},
        ]

        self.assertEqual(
            {"status": "observed", "handlers": []},
            observed_skill_handlers(completed, ["alpha-skill"]),
        )
        self.assertEqual(
            {"status": "not_exposed", "handlers": []},
            observed_skill_handlers(incomplete, ["alpha-skill"]),
        )

    def test_plan_selects_only_requested_migrated_case(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Check the changed decision boundary.",
                    "--affected",
                    "decision boundary",
                    "--case",
                    "selected",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual(canonical_json(plan) + "\n", plan_path.read_text(encoding="utf-8"))
            self.assertEqual(
                {
                    "model": "gpt-5.6-luna",
                    "reasoning_effort": "max",
                    "sandbox": "read-only",
                },
                plan["environment"],
            )
            self.assertEqual(1, plan["estimated_model_calls"])
            self.assertEqual(
                [{"case_id": "selected", "condition": "candidate"}],
                plan["executions"],
            )
            self.assertNotIn("not-selected", plan_path.read_text(encoding="utf-8"))

    def test_plan_accepts_official_case_shape_and_normalizes_numeric_id(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            write(
                asset,
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": 7,
                                "prompt": "Use the official-shaped case.",
                                "expected_output": "A bounded answer.",
                                "files": [],
                            }
                        ],
                    }
                )
                + "\n",
            )
            plan_path = Path(output) / "plan.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Check official input compatibility.",
                    "--affected",
                    "official case loading",
                    "--case",
                    "7",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual("agent-skills", plan["source"]["format"])
            self.assertEqual("7", plan["cases"][0]["id"])
            self.assertEqual(
                "A bounded answer.",
                plan["cases"][0]["grading_requirements"][0]["text"],
            )

    def test_plan_allows_explicit_model_and_reasoning_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Check explicit environment overrides.",
                    "--affected",
                    "execution environment",
                    "--case",
                    "selected",
                    "--base-ref",
                    "HEAD",
                    "--model",
                    "override-model",
                    "--reasoning-effort",
                    "low",
                    "--output",
                    str(plan_path),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual("override-model", plan["environment"]["model"])
            self.assertEqual("low", plan["environment"]["reasoning_effort"])

    def test_migrated_turns_and_inline_fixture_are_normalized_for_one_execution(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "evals.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": "turns",
                                "turns": ["Start the request.", "Use the repository convention."],
                                "assertions": ["Uses the repository convention."],
                                "fixture": {"files": {"README.md": "Use the established convention.\n"}},
                            }
                        ],
                    }
                )
                + "\n",
            )
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex)
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Check transcript normalization.",
                    "--affected",
                    "transcript input",
                    "--case",
                    "turns",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    str(fake_codex),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            invocation = json.loads(
                (artifacts / "executions" / "001-candidate-turns" / "fixture" / "invocation.json").read_text()
            )
            self.assertIn("User turn 1", invocation["prompt"])
            self.assertIn("Use the repository convention.", invocation["prompt"])
            fixture = artifacts / "executions" / "001-candidate-turns" / "fixture" / "README.md"
            self.assertEqual("Use the established convention.\n", fixture.read_text())

    def test_plan_rejects_named_fixture_that_cannot_be_materialized(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "evals.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": "named",
                                "prompt": "Run it.",
                                "expected_output": "A bounded result.",
                                "fixture": "missing-fixture",
                            }
                        ],
                    }
                )
                + "\n",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Reject an unavailable fixture.",
                    "--affected",
                    "fixture materialization",
                    "--case",
                    "named",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(Path(output) / "plan.json"),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("materialize the fixture", result.stderr)

    def test_run_refuses_plan_that_exceeds_model_call_budget(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Check the budget.",
                    "--affected",
                    "budget enforcement",
                    "--case",
                    "selected",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(Path(output) / "artifacts"),
                    "--execute",
                    "--max-model-calls",
                    "0",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("exceeds --max-model-calls", result.stderr)
            self.assertFalse((Path(output) / "artifacts").exists())

    def test_run_rejects_tampered_plan_sandbox(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            create_manual_plan(root, plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["environment"]["sandbox"] = "danger-full-access"
            write(plan_path, json.dumps(plan) + "\n")

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(Path(output) / "artifacts"),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("plan digest does not match", result.stderr)
            self.assertFalse((Path(output) / "artifacts").exists())

    def test_run_rejects_invalid_candidate_manifest_entry(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            create_manual_plan(root, plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan.pop("plan_digest")
            plan["candidate"]["files"]["SKILL.md"]["mode"] = "100777"
            write(plan_path, canonical_json(attach_plan_digest(plan)) + "\n")

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    "/bin/false",
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(Path(output) / "artifacts"),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("sha256 hash and mode 100644 or 100755", result.stderr)
            self.assertFalse((Path(output) / "artifacts").exists())

    def test_run_isolates_candidate_baseline_and_without_skill(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            skill = root / "skills" / "alpha-skill" / "SKILL.md"
            skill.write_text(skill.read_text(encoding="utf-8") + "\nCandidate marker.\n", encoding="utf-8")
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex)
            plan_path = Path(output) / "plan.json"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "baseline-comparison",
                    "--purpose",
                    "Compare the three explicit conditions.",
                    "--affected",
                    "condition isolation",
                    "--case",
                    "selected",
                    "--condition",
                    "candidate",
                    "--condition",
                    "baseline",
                    "--condition",
                    "without-skill",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            artifacts = Path(output) / "artifacts"

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    str(fake_codex),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "3",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            self.assertEqual("pass", run["static_check"]["status"])
            self.assertEqual(
                ["candidate", "baseline", "without-skill"],
                [execution["condition"] for execution in run["executions"]],
            )
            states = [
                json.loads(
                    (artifacts / execution["artifact_directory"] / "fixture" / "invocation.json").read_text()
                )["state"]
                for execution in run["executions"]
            ]
            invocations = [
                json.loads(
                    (artifacts / execution["artifact_directory"] / "fixture" / "invocation.json").read_text()
                )
                for execution in run["executions"]
            ]
            self.assertIn("Candidate marker.", states[0])
            self.assertNotIn("Candidate marker.", states[1])
            self.assertEqual("without-skill", states[2])
            self.assertTrue(all(execution["status"] == "completed" for execution in run["executions"]))
            self.assertTrue(
                all(
                    not (
                        artifacts
                        / execution["artifact_directory"]
                        / "fixture"
                        / ".agents"
                        / "skills"
                        / "alpha-skill"
                        / "evals"
                    ).exists()
                    for execution in run["executions"][:2]
                )
            )
            self.assertTrue(all("--ephemeral" in invocation["argv"] for invocation in invocations))
            self.assertTrue(all("--json" in invocation["argv"] for invocation in invocations))
            self.assertTrue(
                all(
                    invocation["argv"][invocation["argv"].index("--model") + 1] == "gpt-5.6-luna"
                    for invocation in invocations
                )
            )
            self.assertTrue(
                all('model_reasoning_effort="max"' in invocation["argv"] for invocation in invocations)
            )
            self.assertTrue(all("Use the `alpha-skill` Skill" in invocation["prompt"] for invocation in invocations))
            self.assertTrue(all("Do not run this case." not in invocation["prompt"] for invocation in invocations))

    def test_report_previews_then_writes_compact_change_scoped_record(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex)
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Check the selected responsibility.",
                    "--affected",
                    "selected responsibility",
                    "--case",
                    "selected",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    str(fake_codex),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            grades = Path(output) / "grades.json"
            write(
                grades,
                json.dumps(
                    {
                        "schema_version": 2,
                        "results": [
                            {
                                "case_id": "selected",
                                "condition": "candidate",
                                "requirements": [
                                    {
                                        "id": "expected-output",
                                        "status": "pass",
                                        "evidence": "The answer stayed bounded.",
                                    }
                                ],
                                "evidence": "All selected requirements passed.",
                            }
                        ],
                    }
                )
                + "\n",
            )
            report_path = root / "skills" / "alpha-skill" / "evals" / "report.json"
            common = [
                sys.executable,
                str(RUNNER),
                "--root",
                str(root),
                "report",
                "--run",
                str(artifacts / "run.json"),
                "--grades",
                str(grades),
                "--stopping-reason",
                "The selected case answered the acceptance question.",
                "--unverified",
                "Unselected responsibilities",
            ]

            preview = subprocess.run(common, text=True, capture_output=True)

            self.assertEqual(0, preview.returncode, preview.stderr)
            self.assertFalse(report_path.exists())
            preview_document = json.loads(preview.stdout)
            self.assertEqual("pass", preview_document["summary"]["status"])
            self.assertEqual(["selected responsibility"], preview_document["affected_responsibilities"])
            self.assertNotIn(str(artifacts), preview.stdout)
            self.assertNotIn("final:", preview.stdout)

            written = subprocess.run([*common, "--write"], text=True, capture_output=True)

            self.assertEqual(0, written.returncode, written.stderr)
            self.assertEqual(preview_document, json.loads(report_path.read_text(encoding="utf-8")))

    def test_run_records_invalid_jsonl_and_timeout_as_errors(self) -> None:
        for mode, expected_error in (("invalid-jsonl", "invalid JSONL"), ("timeout", "timeout")):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                fake_codex = Path(output) / "fake-codex"
                create_fake_codex(fake_codex, mode)
                plan_path = Path(output) / "plan.json"
                subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "plan",
                        "--skill",
                        "alpha-skill",
                        "--path",
                        "targeted-candidate",
                        "--purpose",
                        "Exercise an executor failure.",
                        "--affected",
                        "executor failure handling",
                        "--case",
                        "selected",
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(plan_path),
                    ],
                    check=True,
                    text=True,
                    capture_output=True,
                )
                artifacts = Path(output) / "artifacts"

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "--codex-bin",
                        str(fake_codex),
                        "run",
                        "--plan",
                        str(plan_path),
                        "--artifacts-dir",
                        str(artifacts),
                        "--execute",
                        "--max-model-calls",
                        "1",
                        "--timeout-seconds",
                        "1",
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(1, result.returncode, result.stderr)
                run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
                self.assertEqual("error", run["executions"][0]["status"])
                self.assertIn(expected_error, run["executions"][0]["error"])

    def test_routing_does_not_infer_skill_load_from_output_wording(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": "route",
                                "prompt": "Choose the appropriate Skill.",
                                "expected_handlers": ["alpha-skill"],
                            }
                        ],
                    }
                )
                + "\n",
            )
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex, "unexposed")
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-routing",
                    "--purpose",
                    "Check observable routing.",
                    "--affected",
                    "Skill selection",
                    "--case",
                    "route",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    str(fake_codex),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {"status": "not_exposed", "handlers": []},
                run["executions"][0]["routing_observation"],
            )

    def test_routing_completed_empty_observation_passes_non_trigger_case(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "evals": [
                            {
                                "id": "non-trigger",
                                "prompt": "Handle this without a Skill.",
                                "expected_handlers": [],
                            },
                            {
                                "id": "missing-trigger",
                                "prompt": "Handle this with the Alpha Skill.",
                                "expected_handlers": ["alpha-skill"],
                            }
                        ],
                    }
                )
                + "\n",
            )
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex, "non-trigger")
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-routing",
                    "--purpose",
                    "Check non-trigger routing.",
                    "--affected",
                    "Skill selection",
                    "--case",
                    "non-trigger",
                    "--case",
                    "missing-trigger",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    str(fake_codex),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "2",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(2, len(run["executions"]))
            for execution in run["executions"]:
                self.assertEqual(
                    {"status": "observed", "handlers": []},
                    execution["routing_observation"],
                )
            grades = Path(output) / "grades.json"
            write(
                grades,
                json.dumps(
                    {
                        "schema_version": 2,
                        "results": [
                            {
                                "case_id": "non-trigger",
                                "condition": "candidate",
                                "requirements": [],
                                "evidence": "No Skill handler was observed.",
                            },
                            {
                                "case_id": "missing-trigger",
                                "condition": "candidate",
                                "requirements": [],
                                "evidence": "The expected Skill handler was not observed.",
                            }
                        ],
                    }
                )
                + "\n",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "report",
                    "--run",
                    str(artifacts / "run.json"),
                    "--grades",
                    str(grades),
                    "--stopping-reason",
                    "The completed observation answered the routing question.",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            report = json.loads(result.stdout)
            statuses = {result["case_id"]: result["status"] for result in report["results"]}
            self.assertEqual({"non-trigger": "pass", "missing-trigger": "fail"}, statuses)

    def test_routing_preserves_companions_and_derives_observed_handler_grade(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "beta-skill" / "SKILL.md",
                "---\nname: beta-skill\ndescription: Companion fixture.\nlicense: MIT\n---\n",
            )
            companion_helper = root / "skills" / "beta-skill" / "scripts" / "tool.sh"
            write(companion_helper, "#!/bin/sh\nexit 0\n")
            companion_helper.chmod(0o755)
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "execution": {"coexistence_skills": ["beta-skill"]},
                        "evals": [
                            {
                                "id": "route",
                                "prompt": "Choose the appropriate Skill.",
                                "expected_handlers": ["alpha-skill"],
                            }
                        ],
                    }
                )
                + "\n",
            )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "routing fixture"], check=True)
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex)
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-routing",
                    "--purpose",
                    "Check direct routing evidence.",
                    "--affected",
                    "Skill selection",
                    "--case",
                    "route",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual(["beta-skill"], plan["coexistence_skills"])
            self.assertIn("beta-skill", plan["inputs"]["companions"])
            self.assertEqual(
                "100755",
                plan["inputs"]["companions"]["beta-skill"]["files"]["scripts/tool.sh"]["mode"],
            )
            self.assertEqual(
                ["alpha-skill"],
                plan["cases"][0]["grading_requirements"][0]["expected_handlers"],
            )
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "--codex-bin",
                    str(fake_codex),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "1",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            copied_helper = (
                artifacts
                / "executions"
                / "001-candidate-route"
                / "fixture"
                / ".agents"
                / "skills"
                / "beta-skill"
                / "scripts"
                / "tool.sh"
            )
            self.assertEqual(0o755, copied_helper.stat().st_mode & 0o777)
            grades = Path(output) / "grades.json"
            write(
                grades,
                json.dumps(
                    {
                        "schema_version": 2,
                        "results": [
                            {
                                "case_id": "route",
                                "condition": "candidate",
                                "requirements": [],
                                "evidence": "Routing was observed directly.",
                            }
                        ],
                    }
                )
                + "\n",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "report",
                    "--run",
                    str(artifacts / "run.json"),
                    "--grades",
                    str(grades),
                    "--stopping-reason",
                    "The direct observation answered the routing question.",
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual("pass", report["results"][0]["status"])
            self.assertEqual(
                {
                    "id": "routing-handlers",
                    "status": "pass",
                    "evidence": "Observed handlers: alpha-skill.",
                    "critical": True,
                },
                report["results"][0]["requirements"][0],
            )

    def test_report_rejects_missing_and_extra_grades(self) -> None:
        for results, expected in (
            ([], "missing grades"),
            (
                [
                    {
                        "case_id": "selected",
                        "condition": "candidate",
                        "requirements": [
                            {"id": "expected-output", "status": "pass", "evidence": "Selected."}
                        ],
                        "evidence": "Selected result.",
                    },
                    {
                        "case_id": "extra",
                        "condition": "candidate",
                        "requirements": [],
                        "evidence": "Unplanned result.",
                    },
                ],
                "extra grades",
            ),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                plan_path = Path(output) / "plan.json"
                create_manual_plan(root, plan_path)
                run_path = Path(output) / "run.json"
                create_manual_run(plan_path, run_path)
                grades = Path(output) / "grades.json"
                write(grades, json.dumps({"schema_version": 2, "results": results}) + "\n")

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "report",
                        "--run",
                        str(run_path),
                        "--grades",
                        str(grades),
                        "--stopping-reason",
                        "Stop.",
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stderr)

    def test_report_requires_every_assertion_assigned_to_the_case(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            create_manual_plan(root, plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["cases"][0]["grading_requirements"] = [
                {"id": "required-assertion", "text": "Required.", "critical": True}
            ]
            write(plan_path, json.dumps(attach_plan_digest(plan)) + "\n")
            run_path = Path(output) / "run.json"
            create_manual_run(plan_path, run_path)
            grades = Path(output) / "grades.json"
            write(
                grades,
                json.dumps(
                    {
                        "schema_version": 2,
                        "results": [
                            {
                                "case_id": "selected",
                                "condition": "candidate",
                                "requirements": [],
                                "evidence": "The case was graded incompletely.",
                            }
                        ],
                    }
                )
                + "\n",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "report",
                    "--run",
                    str(run_path),
                    "--grades",
                    str(grades),
                    "--stopping-reason",
                    "Stop.",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("missing requirement grades", result.stderr)

    def test_report_rejects_tampered_embedded_plan_and_environment(self) -> None:
        for mutation, expected in (
            (
                lambda run: run["plan"]["environment"].update({"model": "claimed-model"}),
                "plan digest does not match",
            ),
            (
                lambda run: run["environment"].update({"model": "claimed-model"}),
                "does not match the embedded plan environment",
            ),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                plan_path = Path(output) / "plan.json"
                create_manual_plan(root, plan_path)
                run_path = Path(output) / "run.json"
                create_manual_run(plan_path, run_path)
                run = json.loads(run_path.read_text(encoding="utf-8"))
                mutation(run)
                write(run_path, json.dumps(run) + "\n")
                grades = Path(output) / "grades.json"
                write(
                    grades,
                    json.dumps(
                        {
                            "schema_version": 2,
                            "results": [
                                {
                                    "case_id": "selected",
                                    "condition": "candidate",
                                    "requirements": [
                                        {
                                            "id": "expected-output",
                                            "status": "pass",
                                            "evidence": "Passed.",
                                        }
                                    ],
                                    "evidence": "Passed.",
                                }
                            ],
                        }
                    )
                    + "\n",
                )

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "report",
                        "--run",
                        str(run_path),
                        "--grades",
                        str(grades),
                        "--stopping-reason",
                        "Stop.",
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stderr)

    def test_report_derives_case_status_from_requirement_criticality(self) -> None:
        for critical, requirement_status, expected_status in (
            (True, "fail", "fail"),
            (False, "fail", "inconclusive"),
            (True, "inconclusive", "inconclusive"),
            (True, "error", "error"),
            (True, "pass", "pass"),
        ):
            with self.subTest(status=requirement_status, critical=critical), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                plan_path = Path(output) / "plan.json"
                create_manual_plan(root, plan_path)
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                plan["cases"][0]["grading_requirements"] = [
                    {"id": "graded", "text": "Grade this.", "critical": critical}
                ]
                write(plan_path, json.dumps(attach_plan_digest(plan)) + "\n")
                run_path = Path(output) / "run.json"
                create_manual_run(plan_path, run_path)
                grades = Path(output) / "grades.json"
                write(
                    grades,
                    json.dumps(
                        {
                            "schema_version": 2,
                            "results": [
                                {
                                    "case_id": "selected",
                                    "condition": "candidate",
                                    "requirements": [
                                        {"id": "graded", "status": requirement_status, "evidence": "Observed."}
                                    ],
                                    "evidence": "Graded.",
                                }
                            ],
                        }
                    )
                    + "\n",
                )

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "report",
                        "--run",
                        str(run_path),
                        "--grades",
                        str(grades),
                        "--stopping-reason",
                        "Stop.",
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(0, result.returncode, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(expected_status, report["results"][0]["status"])
                self.assertEqual(expected_status, report["summary"]["status"])

    def test_model_backed_plan_rejects_legacy_case_shapes(self) -> None:
        for asset_name, document, evaluation_path, case_id, shape in (
            (
                "triggers.json",
                {
                    "skill": "alpha-skill",
                    "version": 1,
                    "run_policy": {},
                    "coexistence_skills": ["beta-skill"],
                    "cases": [{"id": "route", "prompt": "Route.", "expected_handler": "alpha-skill"}],
                },
                "targeted-routing",
                "route",
                "legacy {skill, cases}",
            ),
            (
                "evals.json",
                {
                    "skill": "alpha-skill",
                    "schema_version": 1,
                    "scenarios": [{"id": "A", "prompt": "Write.", "requirements": []}],
                },
                "targeted-candidate",
                "A",
                "scenarios",
            ),
        ):
            with self.subTest(shape=shape), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                write(root / "skills" / "alpha-skill" / "evals" / asset_name, json.dumps(document) + "\n")
                plan_path = Path(output) / "plan.json"

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "plan",
                        "--skill",
                        "alpha-skill",
                        "--path",
                        evaluation_path,
                        "--purpose",
                        "Reject legacy input.",
                        "--affected",
                        "migration boundary",
                        "--case",
                        case_id,
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(plan_path),
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(2, result.returncode)
                self.assertIn(f"unsupported {shape} evaluation format", result.stderr)
                self.assertIn("migrate the Skill's complete", result.stderr)
                self.assertFalse(plan_path.exists())

    def test_model_backed_plan_rejects_a_legacy_sibling_asset(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill": "alpha-skill",
                        "version": 1,
                        "cases": [{"id": "route", "prompt": "Route."}],
                    }
                )
                + "\n",
            )
            plan_path = Path(output) / "plan.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "targeted-candidate",
                    "--purpose",
                    "Reject partial migration.",
                    "--affected",
                    "migration boundary",
                    "--case",
                    "selected",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("complete evals.json and triggers.json set", result.stderr)
            self.assertFalse(plan_path.exists())

    def test_static_only_path_uses_no_model_and_needs_no_grades(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "plan",
                    "--skill",
                    "alpha-skill",
                    "--path",
                    "static-only",
                    "--purpose",
                    "Check a non-behavioral change.",
                    "--affected",
                    "static metadata",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual(0, plan["estimated_model_calls"])
            self.assertEqual([], plan["executions"])
            run = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "run",
                    "--plan",
                    str(plan_path),
                    "--artifacts-dir",
                    str(artifacts),
                    "--execute",
                    "--max-model-calls",
                    "0",
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, run.returncode, run.stderr)

            report = subprocess.run(
                [
                    sys.executable,
                    str(RUNNER),
                    "--root",
                    str(root),
                    "report",
                    "--run",
                    str(artifacts / "run.json"),
                    "--stopping-reason",
                    "Static validation was sufficient.",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, report.returncode, report.stderr)
            self.assertEqual("pass", json.loads(report.stdout)["summary"]["status"])


if __name__ == "__main__":
    unittest.main()
