import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.run_skill_evaluation import direct_skill_load_observation


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
                "schema_version": 1,
                "skill": "alpha-skill",
                "cases": [
                    {"id": "selected", "input": "Run the selected case."},
                    {"id": "not-selected", "input": "Do not run this case."},
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
            {
                "schema_version": 1,
                "skill": "alpha-skill",
                "path": "targeted-candidate",
                "purpose": "Check grade matching.",
                "affected_responsibilities": ["grade matching"],
                "base": {"ref": "HEAD", "commit": commit},
                "environment": {"model": "test", "reasoning_effort": "test", "sandbox": "read-only"},
                "cases": [{"id": "selected", "prompt": "Run it.", "assertions": [], "files": []}],
                "executions": [{"case_id": "selected", "condition": "candidate"}],
                "estimated_model_calls": 1,
                "candidate": {"files": {}},
                "coexistence_skills": [],
            }
        )
        + "\n",
    )


class SkillEvaluationRunnerTests(unittest.TestCase):
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

    def test_plan_selects_only_requested_legacy_case(self) -> None:
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
            self.assertEqual("official", plan["source"]["format"])
            self.assertEqual("7", plan["cases"][0]["id"])
            self.assertEqual("A bounded answer.", plan["cases"][0]["expected_output"])

    def test_legacy_turns_and_inline_fixture_are_normalized_for_one_execution(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(
                root / "skills" / "alpha-skill" / "evals" / "evals.json",
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill": "alpha-skill",
                        "cases": [
                            {
                                "id": "turns",
                                "turns": ["Start the request.", "Use the repository convention."],
                                "assertions": ["uses-convention"],
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
                        "schema_version": 1,
                        "skill": "alpha-skill",
                        "cases": [{"id": "named", "input": "Run it.", "fixture": "missing-fixture"}],
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
            self.assertIn("invalid environment", result.stderr)
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
                        "schema_version": 1,
                        "results": [
                            {
                                "case_id": "selected",
                                "condition": "candidate",
                                "status": "pass",
                                "requirements": [
                                    {"id": "bounded", "status": "pass", "evidence": "The answer stayed bounded."}
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
                "--plan",
                str(plan_path),
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
                        "schema_version": 1,
                        "skill": "alpha-skill",
                        "cases": [{"id": "route", "input": "Choose the appropriate Skill."}],
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
            self.assertEqual("not_exposed", run["executions"][0]["skill_load"])

    def test_report_rejects_missing_and_extra_grades(self) -> None:
        for results, expected in (
            ([], "missing grades"),
            (
                [
                    {
                        "case_id": "selected",
                        "condition": "candidate",
                        "status": "pass",
                        "requirements": [],
                        "evidence": "Selected result.",
                    },
                    {
                        "case_id": "extra",
                        "condition": "candidate",
                        "status": "pass",
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
                write(
                    run_path,
                    json.dumps(
                        {
                            "schema_version": 1,
                            "skill": "alpha-skill",
                            "client": "codex-cli fake",
                            "environment": {},
                            "static_check": {"status": "pass", "exit_code": 0},
                            "executions": [
                                {"case_id": "selected", "condition": "candidate", "status": "completed"}
                            ],
                        }
                    )
                    + "\n",
                )
                grades = Path(output) / "grades.json"
                write(grades, json.dumps({"schema_version": 1, "results": results}) + "\n")

                result = subprocess.run(
                    [
                        sys.executable,
                        str(RUNNER),
                        "--root",
                        str(root),
                        "report",
                        "--plan",
                        str(plan_path),
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
            plan["cases"][0]["assertions"] = ["required-assertion"]
            write(plan_path, json.dumps(plan) + "\n")
            run_path = Path(output) / "run.json"
            write(
                run_path,
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill": "alpha-skill",
                        "client": "codex-cli fake",
                        "static_check": {"status": "pass"},
                        "executions": [
                            {"case_id": "selected", "condition": "candidate", "status": "completed"}
                        ],
                    }
                )
                + "\n",
            )
            grades = Path(output) / "grades.json"
            write(
                grades,
                json.dumps(
                    {
                        "schema_version": 1,
                        "results": [
                            {
                                "case_id": "selected",
                                "condition": "candidate",
                                "status": "pass",
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
                    "--plan",
                    str(plan_path),
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
                    "--plan",
                    str(plan_path),
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
