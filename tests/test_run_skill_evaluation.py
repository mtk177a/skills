import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.run_skill_evaluation import (
    EvaluationError,
    attach_plan_digest,
    canonical_json,
    copy_baseline_skill,
    copy_case_files,
    copy_manifest,
    direct_skill_load_observation,
    observed_skill_handlers,
    isolated_skill_catalog_check,
    isolated_skill_config_args,
    execute_case,
    runtime_skill_read_check,
    runtime_skill_read_guard,
    skill_manifest,
    validate_plan,
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
if sys.argv[1:3] == ["debug", "prompt-input"]:
    skills_root = pathlib.Path.cwd() / ".agents" / "skills"
    catalog = "- `r0` = `" + str(skills_root) + "`"
    for local in sorted(skills_root.glob("*/SKILL.md")):
        description = next((line.removeprefix("description: ") for line in local.read_text().splitlines() if line.startswith("description: ")), "")
        catalog += "\\n- " + local.parent.name + ": " + description + " (file: r0/" + local.parent.name + "/SKILL.md)"
    if {mode!r} == "duplicate-catalog":
        catalog += "\\n- `r1` = `/tmp/personal-skills`\\n- maintain-japanese-references: Personal copy. (file: r1/maintain-japanese-references/SKILL.md)"
    if {mode!r} == "duplicate-public-catalog":
        catalog += "\\n- `r1` = `/tmp/personal-skills`\\n- alpha-skill: Personal copy. (file: r1/alpha-skill/SKILL.md)"
    if {mode!r} == "personal-companion":
        catalog += "\\n- `r2` = `/tmp/personal-skills`\\n- write-natural-japanese: Personal copy. (file: r2/write-natural-japanese/SKILL.md)"
    print(json.dumps([{{"role": "developer", "content": [{{"text": catalog}}]}}]))
    raise SystemExit(0)
output = pathlib.Path(sys.argv[sys.argv.index("--output-last-message") + 1])
skill = pathlib.Path.cwd() / ".agents" / "skills" / "alpha-skill" / "SKILL.md"
state = skill.read_text() if skill.exists() else "without-skill"
prompt = sys.stdin.read()
output.write_text("final: " + state, encoding="utf-8")
if {mode!r} == "timeout":
    print("partial event before timeout", flush=True)
    print("partial stderr before timeout", file=sys.stderr, flush=True)
    time.sleep(5)
elif {mode!r} == "invalid-jsonl":
    print("not-json")
elif {mode!r} == "unexposed":
    print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": "I used /skills/alpha-skill/SKILL.md"}}}}))
elif {mode!r} == "non-trigger":
    print(json.dumps({{"type": "item.completed", "item": {{"type": "agent_message", "text": "No Skill was needed."}}}}))
    print(json.dumps({{"type": "turn.completed", "usage": {{"input_tokens": 1, "output_tokens": 1}}}}))
else:
    observed_skill = skill
    if {mode!r} == "personal-runtime":
        observed_skill = pathlib.Path.home() / ".agents" / "skills" / "alpha-skill" / "SKILL.md"
    print(json.dumps({{"type": "item.completed", "item": {{"type": "command_execution", "command": "read " + str(observed_skill), "exit_code": 0}}}}))
    if {mode!r} == "beta-read":
        beta = pathlib.Path.cwd() / ".agents" / "skills" / "beta-skill" / "SKILL.md"
        print(json.dumps({{"type": "item.completed", "item": {{"type": "command_execution", "command": "read " + str(beta), "exit_code": 0}}}}))
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
                "schema_version": 3,
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
                "executions": [{"case_id": "selected", "condition": "candidate", "coexistence_skills": []}],
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
    def test_runtime_skill_read_guard_uses_one_profile_with_personal_denials(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            personal = home / ".agents" / "skills" / "alpha-skill" / "SKILL.md"
            write(personal, "personal copy\n")
            command, status, error = runtime_skill_read_guard(
                "codex",
                "alpha-skill",
                home=home,
                sandbox="workspace-write",
            )

            self.assertEqual("permission-profile", status)
            self.assertIsNone(error)
            self.assertEqual("codex", command[0])
            self.assertNotIn("sandbox-exec", command)
            self.assertIn('default_permissions="skill-evaluation"', command)
            self.assertTrue(any('extends=":workspace"' in arg for arg in command))
            self.assertTrue(any(json.dumps(str(personal.parent)) + '="deny"' in arg for arg in command))
            self.assertIn('approval_policy="never"', command)

    def test_runtime_skill_read_guard_refuses_unsandboxed_personal_reads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            write(home / ".codex" / "skills" / "alpha-skill" / "SKILL.md", "personal copy\n")

            command, status, error = runtime_skill_read_guard(
                "codex", "alpha-skill", home=home, sandbox="danger-full-access",
            )

            self.assertEqual([], command)
            self.assertEqual("unavailable", status)
            self.assertIn("cannot enforce read isolation", error or "")

    def test_read_only_profile_denies_both_personal_locations_and_symlink_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            canonical = home / "actual-skill" / "SKILL.md"
            write(canonical, "personal copy\n")
            alias = home / ".agents" / "skills" / "alpha-skill" / "SKILL.md"
            alias.parent.mkdir(parents=True)
            alias.symlink_to(canonical)
            other = home / ".codex" / "skills" / "alpha-skill" / "SKILL.md"
            write(other, "other copy\n")
            command, status, error = runtime_skill_read_guard("codex", "alpha-skill", home=home)
            self.assertIsNone(error)
            self.assertEqual("permission-profile", status)
            profile = next(arg for arg in command if arg.startswith("permissions.skill-evaluation="))
            self.assertIn('extends=":read-only"', profile)
            for path in (alias.parent, canonical.resolve().parent, other.parent):
                self.assertIn(json.dumps(str(path)) + '="deny"', profile)

    def test_native_read_check_rejects_unsupported_cli_before_a_model_call(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            with patch("scripts.run_skill_evaluation.subprocess.run", return_value=subprocess.CompletedProcess([], 2, "", "unsupported profile")) as run:
                error = runtime_skill_read_check(["codex"], fixture, "alpha-skill", "read-only", home=fixture)
            self.assertIn("native sandbox could not preserve", error or "")
            self.assertEqual(1, run.call_count)
            self.assertIn("sandbox", run.call_args.args[0])
            self.assertNotIn("exec", run.call_args.args[0])

    def test_failed_guard_preflight_stops_execution_before_model_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            create_manual_plan(root, plan_path)
            plan = json.loads(plan_path.read_text())
            fake = Path(output) / "fake-codex"
            create_fake_codex(fake)
            with (
                patch("scripts.run_skill_evaluation.runtime_skill_read_guard", return_value=([str(fake)], "permission-profile", None)),
                patch("scripts.run_skill_evaluation.runtime_skill_read_check", return_value="sandbox probe failed"),
            ):
                record = execute_case(root, Path(output) / "artifacts", plan, plan["cases"][0], plan["executions"][0], 1, str(fake), 30, None)
            self.assertEqual("error", record["status"])
            self.assertTrue(record["preflight_failed"])
            self.assertEqual("sandbox probe failed", record["error"])
            fixture = Path(output) / "artifacts" / record["artifact_directory"] / "fixture"
            self.assertFalse((fixture / "invocation.json").exists())
            self.assertFalse((fixture.parent / "events.jsonl").exists())

    def test_profile_execution_preserves_denials_without_legacy_sandbox_overrides(self) -> None:
        for source in ("public", "repository-local"):
            with self.subTest(source=source), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                write(root / ".agents" / "skills" / "alpha-skill" / "SKILL.md", (root / "skills" / "alpha-skill" / "SKILL.md").read_text())
                plan_path = Path(output) / "plan.json"
                create_manual_plan(root, plan_path)
                plan = json.loads(plan_path.read_text())
                plan["skill_source"] = source
                fake = Path(output) / "fake-codex"
                create_fake_codex(fake)
                home = Path(output) / "home"
                write(home / ".agents" / "skills" / "alpha-skill" / "SKILL.md", "personal copy\n")
                prefix, status, error = runtime_skill_read_guard(str(fake), "alpha-skill", home=home)
                with (
                    patch("scripts.run_skill_evaluation.TRACKED_REPOSITORY_LOCAL_SKILLS", {"alpha-skill"}),
                    patch("scripts.run_skill_evaluation.runtime_skill_read_guard", return_value=(prefix, status, error)),
                    patch("scripts.run_skill_evaluation.runtime_skill_read_check", return_value=None),
                ):
                    record = execute_case(root, Path(output) / "artifacts", plan, plan["cases"][0], plan["executions"][0], 1, str(fake), 30, "auto")
                self.assertEqual("completed", record["status"])
                self.assertEqual("pass", record["runtime_guard_preflight"])
                fixture = Path(output) / "artifacts" / record["artifact_directory"] / "fixture"
                argv = json.loads((fixture / "invocation.json").read_text())["argv"]
                self.assertNotIn("--sandbox", argv)
                self.assertIn("--ignore-user-config", argv)
                self.assertIn('default_permissions="skill-evaluation"', argv)
                self.assertIn('approval_policy="never"', argv)

    def test_repository_local_catalog_rejects_a_second_same_name_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            write(fixture / ".agents" / "skills" / "maintain-japanese-references" / "SKILL.md",
                  "---\nname: maintain-japanese-references\ndescription: Fixture candidate.\nlicense: MIT\n---\n")
            fake = Path(directory) / "codex"
            create_fake_codex(fake, "duplicate-catalog")
            result = isolated_skill_catalog_check(
                str(fake), fixture, "maintain-japanese-references", "candidate",
                isolated_skill_config_args("maintain-japanese-references", []),
            )
            self.assertIn("duplicated", result or "")

    def test_repository_local_catalog_rejects_personal_companion_when_fixture_omits_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / "fixture"
            write(fixture / ".agents" / "skills" / "maintain-japanese-references" / "SKILL.md",
                  "---\nname: maintain-japanese-references\ndescription: Fixture candidate.\nlicense: MIT\n---\n")
            fake = Path(directory) / "codex"
            create_fake_codex(fake, "personal-companion")
            args = isolated_skill_config_args("maintain-japanese-references", [])
            self.assertIn("write-natural-japanese", " ".join(args))
            result = isolated_skill_catalog_check(
                str(fake), fixture, "maintain-japanese-references", "candidate", args,
            )
            self.assertIn("without a fixture copy", result or "")

    def test_repository_local_run_preflights_catalog_and_copies_companion_to_repository_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repository"
            create_repository(root)
            local = root / ".agents" / "skills" / "maintain-japanese-references"
            write(local / "SKILL.md", "---\nname: maintain-japanese-references\ndescription: Maintain Japanese references.\nlicense: MIT\n---\n")
            write(local / "evals" / "evals.json", json.dumps({
                "skill_name": "maintain-japanese-references",
                "evals": [{"id": "H", "prompt": "Maintain the reference.",
                           "coexistence_skills": ["beta-skill"], "expected_output": "Updated."}],
            }) + "\n")
            write(root / "skills" / "beta-skill" / "SKILL.md", "---\nname: beta-skill\ndescription: Beta companion.\nlicense: MIT\n---\n")
            subprocess.run(["git", "-C", str(root), "add", ".agents/skills/maintain-japanese-references/SKILL.md"], check=True)
            fake = Path(directory) / "codex"
            create_fake_codex(fake)
            plan_path = Path(directory) / "plan.json"
            plan_command = [sys.executable, str(RUNNER), "--root", str(root), "plan",
                            "--skill", "maintain-japanese-references", "--skill-source", "repository-local",
                            "--path", "targeted-candidate", "--purpose", "Check local behavior.",
                            "--affected", "reference maintenance", "--case", "H",
                            "--base-ref", "HEAD", "--sandbox", "workspace-write", "--output", str(plan_path)]
            planned = subprocess.run(plan_command, text=True, capture_output=True)
            self.assertEqual(0, planned.returncode, planned.stderr)
            artifacts = Path(directory) / "artifacts"
            result = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root), "--codex-bin", str(fake),
                 "run", "--plan", str(plan_path), "--artifacts-dir", str(artifacts),
                 "--execute", "--max-model-calls", "1"],
                text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            fixture = artifacts / "executions" / "001-candidate-H" / "fixture"
            self.assertTrue((fixture / "skills" / "beta-skill" / "SKILL.md").is_file())
            invocation = json.loads((fixture / "invocation.json").read_text())
            self.assertNotIn("--ignore-user-config", invocation["argv"])
            self.assertFalse(any(arg.startswith("cli_auth_credentials_store=") for arg in invocation["argv"]))
            self.assertIn("features.plugins=false", invocation["argv"])

    def test_repository_local_plan_and_run_reject_companion_fixture_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repository"
            create_repository(root)
            local = root / ".agents" / "skills" / "maintain-japanese-references"
            write(local / "SKILL.md", "# Local Skill\n")
            definition = local / "evals" / "evals.json"
            document = {
                "skill_name": "maintain-japanese-references",
                "execution": {"coexistence_skills": ["alpha-skill"]},
                "evals": [{"id": "selected", "prompt": "Maintain it.", "expected_output": "Updated."}],
            }
            write(definition, json.dumps(document) + "\n")
            subprocess.run(["git", "-C", str(root), "add", ".agents/skills/maintain-japanese-references/SKILL.md"], check=True)
            plan_path = Path(directory) / "plan.json"
            plan_command = [
                sys.executable, str(RUNNER), "--root", str(root), "plan",
                "--skill", "maintain-japanese-references", "--skill-source", "repository-local",
                "--path", "targeted-candidate", "--purpose", "Check fixture safety.",
                "--affected", "companion integrity", "--case", "selected",
                "--base-ref", "HEAD", "--output", str(plan_path),
            ]

            document["evals"][0]["fixture"] = {"files": {"skills/alpha-skill/SKILL.md": "replacement"}}
            write(definition, json.dumps(document) + "\n")
            rejected = subprocess.run(plan_command, text=True, capture_output=True)
            self.assertEqual(2, rejected.returncode)
            self.assertIn("conflicts with companion Skill `alpha-skill`", rejected.stderr)
            self.assertFalse(plan_path.exists())

            del document["evals"][0]["fixture"]
            write(definition, json.dumps(document) + "\n")
            planned = subprocess.run(plan_command, text=True, capture_output=True)
            self.assertEqual(0, planned.returncode, planned.stderr)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["cases"][0]["inline_files"]["skills/alpha-skill/SKILL.md"] = "replacement"
            write(plan_path, canonical_json(attach_plan_digest(plan)) + "\n")
            artifacts = Path(directory) / "artifacts"
            run = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root), "--codex-bin", "/missing/codex",
                 "run", "--plan", str(plan_path), "--artifacts-dir", str(artifacts),
                 "--execute", "--max-model-calls", "1"],
                text=True, capture_output=True,
            )
            self.assertEqual(2, run.returncode)
            self.assertIn("conflicts with companion Skill `alpha-skill`", run.stderr)
            self.assertFalse(artifacts.exists())

    def test_plan_repository_local_skill_uses_tracked_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repository"
            create_repository(root)
            local = root / ".agents" / "skills" / "maintain-japanese-references"
            write(local / "SKILL.md", "# Local Skill\n")
            write(local / "evals" / "evals.json", json.dumps({
                "skill_name": "maintain-japanese-references",
                "evals": [{"id": "H", "prompt": "Maintain the reference.", "expected_output": "Updated."}],
            }) + "\n")
            subprocess.run(["git", "-C", str(root), "add", ".agents/skills/maintain-japanese-references/SKILL.md"], check=True)
            output = Path(directory) / "plan.json"
            result = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root), "plan",
                 "--skill", "maintain-japanese-references", "--skill-source", "repository-local",
                 "--path", "targeted-candidate", "--purpose", "Check local behavior.",
                 "--affected", "reference maintenance", "--case", "H",
                 "--base-ref", "HEAD", "--output", str(output)],
                text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("repository-local", plan["skill_source"])
            self.assertEqual(".agents/skills/maintain-japanese-references/evals/evals.json", plan["source"]["file"])
            write(local / "SKILL.md", "# Changed after planning\n")
            artifacts = Path(directory) / "artifacts"
            run = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root), "run",
                 "--plan", str(output), "--artifacts-dir", str(artifacts),
                 "--execute", "--max-model-calls", "1"],
                text=True, capture_output=True,
            )
            self.assertEqual(2, run.returncode)
            self.assertIn("candidate Skill manifest changed after planning", run.stderr)
            self.assertFalse(artifacts.exists())

    def test_plan_rejects_untracked_repository_local_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repository"
            create_repository(root)
            local = root / ".agents" / "skills" / "maintain-japanese-references"
            write(local / "SKILL.md", "# Untracked local Skill\n")
            result = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root), "plan",
                 "--skill", "maintain-japanese-references", "--skill-source", "repository-local",
                 "--path", "static-only", "--purpose", "Check source restriction.",
                 "--affected", "source restriction", "--base-ref", "HEAD",
                 "--output", str(Path(directory) / "plan.json")],
                text=True, capture_output=True,
            )
            self.assertEqual(2, result.returncode)
            self.assertIn("must be tracked by Git", result.stderr)

    def test_case_baseline_produces_only_the_planned_document_diff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repository"
            fixture = Path(directory) / "fixture"
            fixture.mkdir()
            create_repository(root)
            case = {
                "id": "H",
                "files": [],
                "inline_files": {"docs/authoring.md": "must update\n", "docs/ja/authoring.md": "may update\n"},
                "baseline_files": {"docs/authoring.md": "may update\n", "docs/ja/authoring.md": "may update\n"},
            }
            copy_case_files(root, case, fixture)
            diff = subprocess.run(
                ["git", "-C", str(fixture), "diff", "--", "docs/authoring.md", "docs/ja/authoring.md"],
                text=True, capture_output=True, check=True,
            ).stdout
            self.assertIn("+must update", diff)
            self.assertNotIn("diff --git a/docs/ja/authoring.md", diff)

    def test_plan_checks_references_in_full_definition_and_sibling(self) -> None:
        for location, expected in (
            ("selected-file", "case `selected` input file must be a regular repository file: missing.txt"),
            ("unselected-file", "case `not-selected` input file must be a regular repository file: missing.txt"),
            ("execution-skill", "execution coexistence Skill must have a regular SKILL.md: missing-skill"),
            ("unselected-skill", "case `not-selected` coexistence Skill must have a regular SKILL.md: missing-skill"),
            ("sibling-file", "case `routing` input file must be a regular repository file: missing.txt"),
        ):
            with self.subTest(location=location), tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
                root = Path(repository)
                create_repository(root)
                asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                document = json.loads(asset.read_text())
                if location == "selected-file":
                    document["evals"][0]["files"] = ["missing.txt"]
                elif location == "unselected-file":
                    document["evals"][1]["files"] = ["missing.txt"]
                elif location == "execution-skill":
                    document["execution"] = {"coexistence_skills": ["missing-skill"]}
                elif location == "unselected-skill":
                    document["evals"][1]["coexistence_skills"] = ["missing-skill"]
                else:
                    write(
                        asset.with_name("triggers.json"),
                        json.dumps({"skill_name": "alpha-skill", "evals": [
                            {"id": "routing", "prompt": "Route it.", "expected_handlers": [], "files": ["missing.txt"]}
                        ]}),
                    )
                write(asset, json.dumps(document))
                plan_path = Path(output) / "plan.json"

                result = subprocess.run(
                    [sys.executable, str(RUNNER), "--root", str(root), "plan",
                     "--skill", "alpha-skill", "--path", "targeted-candidate",
                     "--purpose", "Check static references.", "--affected", "definition references",
                     "--case", "selected", "--base-ref", "HEAD", "--output", str(plan_path)],
                    text=True, capture_output=True,
                )

                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(plan_path.exists())

    def test_plan_accepts_existing_references(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            write(root / "input.txt", "Input.\n")
            write(root / "skills" / "beta-skill" / "SKILL.md", "# Beta\n")
            asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(asset.read_text())
            document["execution"] = {"coexistence_skills": ["beta-skill"]}
            document["evals"][1]["files"] = ["input.txt"]
            document["evals"][1]["coexistence_skills"] = ["beta-skill"]
            write(asset, json.dumps(document))
            plan_path = Path(output) / "plan.json"

            result = subprocess.run(
                [sys.executable, str(RUNNER), "--root", str(root), "plan",
                 "--skill", "alpha-skill", "--path", "targeted-candidate",
                 "--purpose", "Check static references.", "--affected", "definition references",
                 "--case", "selected", "--base-ref", "HEAD", "--output", str(plan_path)],
                text=True, capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            plan = json.loads(plan_path.read_text())
            self.assertEqual(["selected"], [case["id"] for case in plan["cases"]])
            self.assertEqual(["beta-skill"], plan["coexistence_skills"])

    def test_case_file_copy_rejects_absolute_destination(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            fixture = Path(output) / "fixture"
            fixture.mkdir()
            input_file = root / "inputs" / "request.txt"
            write(input_file, "Original input.\n")
            original_timestamp = 1_600_000_000_000_000_000
            os.utime(input_file, ns=(original_timestamp, original_timestamp))

            with self.assertRaisesRegex(EvaluationError, "unsafe case input path"):
                copy_case_files(
                    root,
                    {"id": "absolute-input", "files": [str(input_file)], "inline_files": {}},
                    fixture,
                )

            self.assertFalse((fixture / "inputs" / "request.txt").exists())
            self.assertEqual("Original input.\n", input_file.read_text(encoding="utf-8"))
            self.assertEqual(original_timestamp, input_file.stat().st_mtime_ns)

    def test_case_file_copy_uses_disposable_inputs_directory(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            fixture = Path(output) / "fixture"
            fixture.mkdir()
            input_file = root / "inputs" / "request.txt"
            write(input_file, "Original input.\n")
            original_timestamp = 1_600_000_000_000_000_000
            os.utime(input_file, ns=(original_timestamp, original_timestamp))

            copy_case_files(
                root,
                {"id": "relative-input", "files": ["inputs/request.txt"], "inline_files": {}},
                fixture,
            )

            copied = fixture / "inputs" / "inputs" / "request.txt"
            self.assertEqual("Original input.\n", copied.read_text(encoding="utf-8"))
            self.assertEqual("Original input.\n", input_file.read_text(encoding="utf-8"))
            self.assertEqual(original_timestamp, input_file.stat().st_mtime_ns)

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
                    "model": "gpt-6-luna",
                    "reasoning_effort": "max",
                    "sandbox": "read-only",
                },
                plan["environment"],
            )
            self.assertEqual(1, plan["estimated_model_calls"])
            self.assertEqual(
                [{"case_id": "selected", "condition": "candidate", "coexistence_skills": []}],
                plan["executions"],
            )
            self.assertNotIn("not-selected", plan_path.read_text(encoding="utf-8"))

    def test_coexistence_skills_are_isolated_per_routing_execution(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            for skill in ("beta-skill", "gamma-skill"):
                write(
                    root / "skills" / skill / "SKILL.md",
                    f"---\nname: {skill}\ndescription: Exercises {skill} coexistence.\nlicense: MIT\n---\n",
                )
            write(
                root / "skills" / "alpha-skill" / "evals" / "triggers.json",
                json.dumps(
                    {
                        "skill_name": "alpha-skill",
                        "execution": {"coexistence_skills": ["gamma-skill"]},
                        "evals": [
                            {"id": "A", "prompt": "Route A.", "expected_handlers": ["alpha-skill"]},
                            {
                                "id": "B",
                                "prompt": "Route B.",
                                "expected_handlers": ["alpha-skill", "beta-skill"],
                                "coexistence_skills": ["gamma-skill", "beta-skill"],
                            },
                        ],
                    }
                ) + "\n",
            )
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex, "beta-read")
            plan_path = Path(output) / "plan.json"
            artifacts = Path(output) / "artifacts"
            result = subprocess.run(
                [
                    sys.executable, str(RUNNER), "--root", str(root), "plan",
                    "--skill", "alpha-skill", "--path", "targeted-routing",
                    "--purpose", "Check case isolation.", "--affected", "coexistence",
                    "--case", "A", "--case", "B", "--base-ref", "HEAD",
                    "--output", str(plan_path),
                ],
                text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            self.assertEqual(3, plan["schema_version"])
            self.assertEqual(["beta-skill", "gamma-skill"], plan["coexistence_skills"])
            self.assertEqual(
                [
                    {"case_id": "A", "condition": "candidate", "coexistence_skills": ["gamma-skill"]},
                    {"case_id": "B", "condition": "candidate", "coexistence_skills": ["beta-skill", "gamma-skill"]},
                ],
                plan["executions"],
            )
            result = subprocess.run(
                [
                    sys.executable, str(RUNNER), "--root", str(root),
                    "--codex-bin", str(fake_codex), "run", "--plan", str(plan_path),
                    "--artifacts-dir", str(artifacts), "--execute", "--max-model-calls", "2",
                ],
                text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(
                [["alpha-skill"], ["alpha-skill", "beta-skill"]],
                [entry["routing_observation"]["handlers"] for entry in run["executions"]],
            )
            for index, case_id, has_beta in ((1, "A", False), (2, "B", True)):
                fixture_skills = artifacts / "executions" / f"{index:03d}-candidate-{case_id}" / "fixture" / ".agents" / "skills"
                self.assertTrue((fixture_skills / "gamma-skill" / "SKILL.md").is_file())
                self.assertEqual(has_beta, (fixture_skills / "beta-skill" / "SKILL.md").is_file())

    def test_plan_validates_execution_coexistence_skills(self) -> None:
        mutations = (
            (lambda plan: plan["executions"][0].pop("coexistence_skills"), "plan execution coexistence_skills"),
            (lambda plan: plan["executions"][0].update(coexistence_skills=["Bad_Name"]), "plan execution coexistence_skills"),
            (lambda plan: plan["executions"][0].update(coexistence_skills=["beta-skill", "beta-skill"]), "plan execution coexistence_skills"),
            (lambda plan: plan["cases"][0].update(coexistence_skills=["beta-skill"]), "omits a case coexistence Skill"),
            (lambda plan: plan.update(coexistence_skills=["beta-skill"]), "do not match its executions"),
            (lambda plan: plan["inputs"]["companions"].update({"beta-skill": {"files": {}}}), "companion manifests do not match"),
            (lambda plan: plan.update(schema_version=2), "unsupported plan schema_version"),
        )
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            plan_path = Path(output) / "plan.json"
            create_manual_plan(root, plan_path)
            original = json.loads(plan_path.read_text(encoding="utf-8"))
            for mutate, expected in mutations:
                with self.subTest(expected=expected):
                    plan = json.loads(json.dumps(original))
                    mutate(plan)
                    with self.assertRaisesRegex(EvaluationError, expected):
                        validate_plan(attach_plan_digest(plan), root)

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
                                "title": "Official case metadata",
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
            self.assertEqual("Official case metadata", plan["cases"][0]["title"])
            self.assertEqual(
                "A bounded answer.",
                plan["cases"][0]["grading_requirements"][0]["text"],
            )

    def test_plan_rejects_unknown_case_fields(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(asset.read_text())
            document["evals"][0]["unused"] = "ignored before the executable contract"
            write(asset, json.dumps(document) + "\n")
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
                    "Check strict case loading.",
                    "--affected",
                    "case contract",
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
            self.assertIn("evaluation case contains unknown field(s): unused", result.stderr)
            self.assertFalse(plan_path.exists())

    def test_plan_rejects_invalid_turn_role_and_unexecutable_conditions(self) -> None:
        invalid_cases = (
            ({"prompt": None, "turns": [{"role": [], "content": "Hello."}]}, "role must be user or assistant"),
            ({"conditions": []}, "conditions must include candidate"),
            ({"conditions": ["baseline"]}, "conditions must include candidate"),
        )
        for changes, expected in invalid_cases:
            with (
                self.subTest(changes=changes),
                tempfile.TemporaryDirectory() as repository,
                tempfile.TemporaryDirectory() as output,
            ):
                root = Path(repository)
                create_repository(root)
                asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                document = json.loads(asset.read_text())
                case = document["evals"][0]
                case.update(changes)
                if case.get("prompt") is None:
                    case.pop("prompt")
                write(asset, json.dumps(document) + "\n")
                plan_path = Path(output) / "plan.json"
                result = subprocess.run(
                    [
                        sys.executable, str(RUNNER), "--root", str(root), "plan",
                        "--skill", "alpha-skill", "--path", "targeted-candidate",
                        "--purpose", "Reject an invalid definition.", "--affected", "contract",
                        "--case", "selected", "--base-ref", "HEAD", "--output", str(plan_path),
                    ],
                    text=True, capture_output=True,
                )
                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(plan_path.exists())

        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
            document = json.loads(asset.read_text())
            document["evals"][0]["conditions"] = ["candidate"]
            write(asset, json.dumps(document) + "\n")
            plan_path = Path(output) / "plan.json"
            result = subprocess.run(
                [
                    sys.executable, str(RUNNER), "--root", str(root), "plan",
                    "--skill", "alpha-skill", "--path", "targeted-candidate",
                    "--purpose", "Plan a valid condition.", "--affected", "contract",
                    "--case", "selected", "--base-ref", "HEAD", "--output", str(plan_path),
                ],
                text=True, capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(plan_path.is_file())

    def test_plan_rejects_absolute_case_input_path(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
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
                                "id": "absolute-input",
                                "prompt": "Use the input.",
                                "expected_output": "A bounded result.",
                                "files": [str(input_file)],
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
                    "Reject an unsafe case input.",
                    "--affected",
                    "case input isolation",
                    "--case",
                    "absolute-input",
                    "--base-ref",
                    "HEAD",
                    "--output",
                    str(plan_path),
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("unsafe case input path", result.stderr)
            self.assertFalse(plan_path.exists())

    def test_plan_rejects_non_repository_case_input_paths_and_duplicates(self) -> None:
        unsafe_values = (
            ([""], "unsafe case input path"),
            (["."], "unsafe case input path"),
            (["../outside.txt"], "unsafe case input path"),
            ([r"C:\\fixtures\\input.txt"], "unsafe case input path"),
            (["inputs/request.txt", "inputs//request.txt"], "repeats a file path"),
        )
        for files, expected in unsafe_values:
            with (
                self.subTest(files=files),
                tempfile.TemporaryDirectory() as repository,
                tempfile.TemporaryDirectory() as output,
            ):
                root = Path(repository)
                create_repository(root)
                write(root / "inputs" / "request.txt", "Original input.\n")
                asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                write(
                    asset,
                    json.dumps(
                        {
                            "skill_name": "alpha-skill",
                            "evals": [
                                {
                                    "id": "unsafe-input",
                                    "prompt": "Use the input.",
                                    "expected_output": "A bounded result.",
                                    "files": files,
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
                        "Reject an unsafe case input.",
                        "--affected",
                        "case input isolation",
                        "--case",
                        "unsafe-input",
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(plan_path),
                    ],
                    text=True,
                    capture_output=True,
                )

                self.assertEqual(2, result.returncode)
                self.assertIn(expected, result.stderr)
                self.assertFalse(plan_path.exists())

    def test_plan_rejects_paths_that_cannot_be_materialized(self) -> None:
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
            with (
                self.subTest(changes=changes),
                tempfile.TemporaryDirectory() as repository,
                tempfile.TemporaryDirectory() as output,
            ):
                root = Path(repository)
                create_repository(root)
                write(root / "source.txt", "Repository input.\n")
                asset = root / "skills" / "alpha-skill" / "evals" / "evals.json"
                document = json.loads(asset.read_text())
                document["evals"][0].update(changes)
                write(asset, json.dumps(document) + "\n")
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
                        "Reject a path that cannot be materialized.",
                        "--affected",
                        "fixture materialization",
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

                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn(expected, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(plan_path.exists())

    def test_plan_normalizes_safe_relative_case_input_path(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
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
                                "id": "relative-input",
                                "prompt": "Use the input.",
                                "expected_output": "A bounded result.",
                                "files": ["./inputs/request.txt"],
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
                    "Normalize a safe case input.",
                    "--affected",
                    "case input isolation",
                    "--case",
                    "relative-input",
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
            self.assertEqual(["inputs/request.txt"], plan["cases"][0]["files"])
            self.assertEqual(
                ["inputs/request.txt"],
                list(plan["inputs"]["case_files"]),
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

    def test_run_rejects_digest_valid_plan_with_absolute_case_input(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            input_file = root / "inputs" / "request.txt"
            write(input_file, "Original input.\n")
            original_timestamp = 1_600_000_000_000_000_000
            os.utime(input_file, ns=(original_timestamp, original_timestamp))
            plan_path = Path(output) / "plan.json"
            create_manual_plan(root, plan_path)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan.pop("plan_digest")
            plan["cases"][0]["files"] = [str(input_file)]
            plan["inputs"]["case_files"] = {
                "inputs/request.txt": "sha256:" + hashlib.sha256(input_file.read_bytes()).hexdigest()
            }
            write(plan_path, canonical_json(attach_plan_digest(plan)) + "\n")
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex)
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
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("unsafe case input path", result.stderr)
            self.assertFalse(artifacts.exists())
            self.assertEqual("Original input.\n", input_file.read_text(encoding="utf-8"))
            self.assertEqual(original_timestamp, input_file.stat().st_mtime_ns)

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
                    "--auth-credentials-store",
                    "auto",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            self.assertEqual("pass", run["static_check"]["status"])
            self.assertEqual("auto", run["auth_credentials_store"])
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
            self.assertTrue(all("--ignore-user-config" in invocation["argv"] for invocation in invocations))
            self.assertTrue(all("features.plugins=false" in invocation["argv"] for invocation in invocations))
            self.assertTrue(all("skills.config=[" in " ".join(invocation["argv"]) for invocation in invocations))
            self.assertTrue(all('cli_auth_credentials_store="auto"' in invocation["argv"] for invocation in invocations))
            self.assertTrue(all(execution["catalog_preflight"] == "pass" for execution in run["executions"]))
            self.assertTrue(
                all(
                    invocation["argv"][invocation["argv"].index("--model") + 1] == "gpt-6-luna"
                    for invocation in invocations
                )
            )
            self.assertTrue(
                all('model_reasoning_effort="max"' in invocation["argv"] for invocation in invocations)
            )
            self.assertTrue(
                all(
                    "use only the `alpha-skill` Skill at `.agents/skills/alpha-skill/SKILL.md`"
                    in invocation["prompt"]
                    for invocation in invocations
                )
            )
            self.assertTrue(
                all("Do not read or use a same-name Skill outside" in invocation["prompt"] for invocation in invocations)
            )
            self.assertTrue(all("Do not run this case." not in invocation["prompt"] for invocation in invocations))

    def test_public_run_rejects_personal_same_name_skill_read_during_execution(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex, "personal-runtime")
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
                    "Reject a personal same-name Skill read at runtime.",
                    "--affected",
                    "public Skill runtime isolation",
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
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(1, result.returncode, result.stderr)
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            execution = run["executions"][0]
            self.assertEqual("error", execution["status"])
            self.assertEqual("fail", execution["runtime_isolation"])
            self.assertIn("personal same-name Skill", execution["error"])

    def test_public_run_rejects_personal_same_name_skill_before_model_call(self) -> None:
        with tempfile.TemporaryDirectory() as repository, tempfile.TemporaryDirectory() as output:
            root = Path(repository)
            create_repository(root)
            fake_codex = Path(output) / "fake-codex"
            create_fake_codex(fake_codex, "duplicate-public-catalog")
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
                    "Reject a personal same-name Skill.",
                    "--affected",
                    "public Skill isolation",
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
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(1, result.returncode, result.stderr)
            run = json.loads((artifacts / "run.json").read_text(encoding="utf-8"))
            execution = run["executions"][0]
            self.assertEqual("error", execution["status"])
            self.assertTrue(execution["preflight_failed"])
            self.assertIn("duplicated", execution["error"])
            fixture = artifacts / execution["artifact_directory"] / "fixture"
            self.assertFalse((fixture / "invocation.json").exists())

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
                if mode == "timeout":
                    execution = artifacts / run["executions"][0]["artifact_directory"]
                    self.assertIn("partial event before timeout", (execution / "events.jsonl").read_text())
                    self.assertIn("partial stderr before timeout", (execution / "stderr.txt").read_text())

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
