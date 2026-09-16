#!/usr/bin/env python3
"""Plan, run, and summarize cost-bounded Skill evaluations with Codex."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLAN_VERSION = 1
RUN_VERSION = 1
REPORT_VERSION = 1
MODEL_PATHS = {
    "targeted-candidate",
    "targeted-routing",
    "baseline-comparison",
    "target-environment",
}
PATHS = {"static-only", *MODEL_PATHS}
CONDITIONS = {"candidate", "baseline", "without-skill"}
STATUSES = {"pass", "fail", "inconclusive", "error"}
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class EvaluationError(Exception):
    """A user-facing evaluation configuration or execution error."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise EvaluationError(f"could not read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise EvaluationError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(document, dict):
        raise EvaluationError(f"JSON top level must be an object: {path}")
    return document


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def contained(parent: Path, child: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def require_temporary_path(root: Path, path: Path, label: str) -> None:
    if contained(root, path):
        raise EvaluationError(f"{label} must be outside the repository: {path}")
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if not contained(temporary_root, path):
        raise EvaluationError(f"{label} must be under the system temporary directory: {temporary_root}")


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise EvaluationError(detail)
    return result.stdout.strip()


def resolve_base(root: Path, base_ref: str) -> str:
    return git(root, "rev-parse", "--verify", "--end-of-options", f"{base_ref}^{{commit}}")


def validate_skill_name(skill: str) -> None:
    if SKILL_NAME.fullmatch(skill) is None:
        raise EvaluationError(f"invalid Skill name: {skill}")


def format_turns(values: Any, label: str) -> str:
    if not isinstance(values, list) or not values:
        raise EvaluationError(f"{label} must be a non-empty array")
    rendered = []
    for index, value in enumerate(values, start=1):
        if isinstance(value, str) and value.strip():
            rendered.append(f"User turn {index}:\n{value}")
        elif (
            isinstance(value, dict)
            and isinstance(value.get("role"), str)
            and isinstance(value.get("content"), str)
            and value["content"].strip()
        ):
            rendered.append(f"{value['role'].capitalize()} turn {index}:\n{value['content']}")
        else:
            raise EvaluationError(f"{label} entries must be strings or role-content objects")
    return "\n\n".join(rendered)


def normalize_case(case: Any, official: bool) -> dict[str, Any]:
    if not isinstance(case, dict):
        raise EvaluationError("every evaluation case must be an object")
    case_id = case.get("id")
    if isinstance(case_id, bool) or not isinstance(case_id, (str, int)):
        raise EvaluationError("every evaluation case requires a string or integer id")
    normalized_id = str(case_id).strip()
    if not normalized_id:
        raise EvaluationError("every evaluation case requires a non-empty id")
    input_mode = "single-turn"
    if isinstance(case.get("prompt"), str) and case["prompt"].strip():
        prompt = case["prompt"]
    elif isinstance(case.get("input"), str) and case["input"].strip():
        prompt = case["input"]
    elif "turns" in case:
        prompt = format_turns(case["turns"], f"evaluation case `{normalized_id}` turns")
        input_mode = "transcript"
    elif isinstance(case.get("request"), str) and case["request"].strip() and "authoring_turns" in case:
        authoring = format_turns(
            case["authoring_turns"],
            f"evaluation case `{normalized_id}` authoring_turns",
        )
        prompt = f"Prior authoring conversation:\n\n{authoring}\n\nCurrent request:\n{case['request']}"
        input_mode = "authoring-transcript"
    else:
        expected = "prompt" if official else "prompt, input, turns, or request with authoring_turns"
        raise EvaluationError(f"evaluation case `{normalized_id}` requires {expected}")
    conversation = case.get("conversation")
    if conversation is not None:
        history = format_turns(conversation, f"evaluation case `{normalized_id}` conversation")
        prompt = f"Conversation so far:\n\n{history}\n\nCurrent user request:\n{prompt}"
        input_mode = "conversation"
    assertions = case.get("assertions", case.get("assertion_ids", []))
    if not isinstance(assertions, list) or not all(isinstance(value, str) for value in assertions):
        raise EvaluationError(f"evaluation case `{normalized_id}` assertions must be strings")
    additional = case.get("additional_requirement", case.get("additional_requirements", []))
    if isinstance(additional, str):
        additional_requirements = [additional]
    elif isinstance(additional, list) and all(isinstance(value, str) for value in additional):
        additional_requirements = additional
    else:
        raise EvaluationError(f"evaluation case `{normalized_id}` additional requirements must be strings")
    files = case.get("files", [])
    if not isinstance(files, list) or not all(isinstance(value, str) for value in files):
        raise EvaluationError(f"evaluation case `{normalized_id}` files must be strings")
    inline_files: dict[str, str] = {}
    fixture = case.get("fixture")
    if isinstance(fixture, dict):
        raw_inline_files = fixture.get("files", {})
        if not isinstance(raw_inline_files, dict) or not all(
            isinstance(name, str) and isinstance(content, str)
            for name, content in raw_inline_files.items()
        ):
            raise EvaluationError(f"evaluation case `{normalized_id}` fixture.files must map paths to strings")
        for name in raw_inline_files:
            relative = Path(name)
            if not name or relative == Path(".") or relative.is_absolute() or ".." in relative.parts or (
                relative.parts and relative.parts[0] in {".agents", ".git"}
            ):
                raise EvaluationError(f"evaluation case `{normalized_id}` has an unsafe fixture path: {name}")
        inline_files = raw_inline_files
    elif fixture is not None and not isinstance(fixture, str):
        raise EvaluationError(f"evaluation case `{normalized_id}` fixture must be an object or name")
    if isinstance(fixture, str):
        raise EvaluationError(
            f"evaluation case `{normalized_id}` names fixture `{fixture}` without inline files; "
            "materialize the fixture before using the common Runner"
        )
    coexistence_skills = case.get("coexistence_skills", [])
    if not isinstance(coexistence_skills, list) or not all(
        isinstance(value, str) for value in coexistence_skills
    ):
        raise EvaluationError(f"evaluation case `{normalized_id}` coexistence_skills must be strings")
    raw_conditions = case.get("conditions")
    condition_aliases = {
        "candidate": "candidate",
        "candidate_isolation": "candidate",
        "baseline": "baseline",
        "current": "baseline",
        "no_skill": "without-skill",
    }
    allowed_conditions = None
    if raw_conditions is not None:
        if not isinstance(raw_conditions, list) or not all(
            isinstance(value, str) and value in condition_aliases for value in raw_conditions
        ):
            raise EvaluationError(f"evaluation case `{normalized_id}` has unsupported conditions")
        allowed_conditions = sorted({condition_aliases[value] for value in raw_conditions})
    normalized = {
        "id": normalized_id,
        "prompt": prompt,
        "input_mode": input_mode,
        "assertions": assertions,
        "additional_requirements": additional_requirements,
        "files": files,
        "inline_files": inline_files,
        "coexistence_skills": coexistence_skills,
    }
    if allowed_conditions is not None:
        normalized["allowed_conditions"] = allowed_conditions
    expected = case.get("expected_output")
    if expected is not None:
        if not isinstance(expected, str):
            raise EvaluationError(f"evaluation case `{normalized_id}` expected_output must be a string")
        normalized["expected_output"] = expected
    return normalized


def load_case_asset(root: Path, skill: str, evaluation_path: str) -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    asset_name = "triggers.json" if evaluation_path == "targeted-routing" else "evals.json"
    asset = root / "skills" / skill / "evals" / asset_name
    if not asset.is_file():
        raise EvaluationError(f"evaluation asset does not exist: {asset.relative_to(root)}")
    document = read_json(asset)
    if "evals" in document or "skill_name" in document:
        if document.get("skill_name") != skill:
            raise EvaluationError(f"evaluation asset skill_name must be `{skill}`")
        raw_cases = document.get("evals")
        official = True
    else:
        if document.get("skill") != skill:
            raise EvaluationError(f"evaluation asset skill must be `{skill}`")
        raw_cases = document.get("cases")
        official = False
    if not isinstance(raw_cases, list):
        raise EvaluationError(f"evaluation cases must be an array: {asset.relative_to(root)}")
    cases = [normalize_case(case, official) for case in raw_cases]
    raw_assertions = document.get("assertions", document.get("candidate_assertions", []))
    assertion_definitions: dict[str, dict[str, Any]] = {}
    if isinstance(raw_assertions, list):
        for assertion in raw_assertions:
            if not isinstance(assertion, dict) or not isinstance(assertion.get("id"), str):
                continue
            requirement = assertion.get("requirement", assertion.get("statement"))
            if not isinstance(requirement, str):
                continue
            assertion_definitions[assertion["id"]] = {
                "id": assertion["id"],
                "requirement": requirement,
                "critical": assertion.get("critical") is True,
            }
    for case in cases:
        case["grading_requirements"] = [
            assertion_definitions.get(assertion_id, {"id": assertion_id})
            for assertion_id in case["assertions"]
        ]
    ids = [case["id"] for case in cases]
    if len(set(ids)) != len(ids):
        raise EvaluationError(f"evaluation case ids must be unique: {asset.relative_to(root)}")
    return asset, document, cases


def default_conditions(evaluation_path: str) -> list[str]:
    if evaluation_path == "static-only":
        return []
    if evaluation_path == "baseline-comparison":
        return ["candidate", "baseline"]
    return ["candidate"]


def candidate_files(root: Path, skill: str, base_commit: str, asset: Path | None) -> dict[str, str]:
    skill_root = root / "skills" / skill
    prefix = skill_root.relative_to(root).as_posix()
    changed = set(filter(None, git(root, "diff", "--name-only", base_commit, "--", prefix).splitlines()))
    changed.update(
        filter(None, git(root, "ls-files", "--others", "--exclude-standard", "--", prefix).splitlines())
    )
    excluded = {
        f"{prefix}/evals/report.json",
        f"{prefix}/evals/results.json",
    }
    selected = {value for value in changed if value not in excluded}
    if asset is not None:
        selected.add(asset.relative_to(root).as_posix())
    bindings: dict[str, str] = {}
    for relative in sorted(selected):
        target = root / relative
        if target.is_file():
            bindings[target.relative_to(skill_root).as_posix()] = sha256(target)
    return bindings


def make_plan(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    validate_skill_name(args.skill)
    skill_root = root / "skills" / args.skill
    if not (skill_root / "SKILL.md").is_file():
        raise EvaluationError(f"Skill does not exist: {args.skill}")
    base_commit = resolve_base(root, args.base_ref)
    conditions = args.condition or default_conditions(args.path)
    if len(set(conditions)) != len(conditions):
        raise EvaluationError("conditions must not be repeated")
    if any(condition not in CONDITIONS for condition in conditions):
        raise EvaluationError("unsupported condition")
    if args.path != "baseline-comparison" and any(value != "candidate" for value in conditions):
        raise EvaluationError("comparison conditions require the baseline-comparison path")
    if args.path == "baseline-comparison" and (
        "candidate" not in conditions or not ({"baseline", "without-skill"} & set(conditions))
    ):
        raise EvaluationError("baseline-comparison requires candidate and baseline or without-skill")

    selected_cases: list[dict[str, Any]] = []
    asset: Path | None = None
    source = None
    coexistence_skills: list[str] = []
    if args.path in MODEL_PATHS:
        if not args.case:
            raise EvaluationError("model-backed evaluation requires at least one --case")
        asset, document, available = load_case_asset(root, args.skill, args.path)
        by_id = {case["id"]: case for case in available}
        missing = [case_id for case_id in args.case if case_id not in by_id]
        if missing:
            raise EvaluationError("unknown evaluation case(s): " + ", ".join(missing))
        if len(set(args.case)) != len(args.case):
            raise EvaluationError("cases must not be repeated")
        selected_cases = [by_id[case_id] for case_id in args.case]
        for case in selected_cases:
            allowed = case.get("allowed_conditions")
            if allowed is not None:
                unsupported = [condition for condition in conditions if condition not in allowed]
                if unsupported:
                    raise EvaluationError(
                        f"evaluation case `{case['id']}` does not support condition(s): "
                        + ", ".join(unsupported)
                    )
        source = {
            "file": asset.relative_to(skill_root).as_posix(),
            "format": "official" if "evals" in document or "skill_name" in document else "legacy",
        }
        execution_settings = document.get("execution", {})
        if isinstance(execution_settings, dict):
            coexistence = execution_settings.get("coexistence_skills", [])
            if isinstance(coexistence, list) and all(isinstance(value, str) for value in coexistence):
                coexistence_skills = coexistence
        coexistence_skills = sorted(
            {
                *coexistence_skills,
                *(value for case in selected_cases for value in case["coexistence_skills"]),
            }
        )
    elif args.case or args.condition:
        raise EvaluationError("static-only does not accept cases or conditions")

    executions = [
        {"case_id": case["id"], "condition": condition}
        for case in selected_cases
        for condition in conditions
    ]
    plan: dict[str, Any] = {
        "schema_version": PLAN_VERSION,
        "skill": args.skill,
        "path": args.path,
        "purpose": args.purpose,
        "affected_responsibilities": args.affected,
        "base": {"ref": args.base_ref, "commit": base_commit},
        "environment": {
            "model": args.model,
            "reasoning_effort": args.reasoning_effort,
            "sandbox": args.sandbox,
        },
        "cases": selected_cases,
        "executions": executions,
        "estimated_model_calls": len(executions),
        "candidate": {"files": candidate_files(root, args.skill, base_commit, asset)},
        "coexistence_skills": coexistence_skills,
    }
    if source is not None:
        plan["source"] = source
    return plan


def command_plan(args: argparse.Namespace, root: Path) -> int:
    output = args.output.resolve()
    require_temporary_path(root, output, "plan output")
    plan = make_plan(args, root)
    write_json(output, plan)
    print(f"Plan written to {output}")
    print(f"Estimated model calls: {plan['estimated_model_calls']}")
    return 0


def load_plan(path: Path, root: Path) -> dict[str, Any]:
    require_temporary_path(root, path, "plan")
    plan = read_json(path)
    if plan.get("schema_version") != PLAN_VERSION:
        raise EvaluationError(f"unsupported plan schema_version: {plan.get('schema_version')}")
    skill = plan.get("skill")
    if not isinstance(skill, str):
        raise EvaluationError("plan references an unknown Skill")
    validate_skill_name(skill)
    if not (root / "skills" / skill / "SKILL.md").is_file():
        raise EvaluationError("plan references an unknown Skill")
    if plan.get("path") not in PATHS:
        raise EvaluationError("plan has an invalid evaluation path")
    if not isinstance(plan.get("purpose"), str) or not plan["purpose"].strip():
        raise EvaluationError("plan requires a non-empty purpose")
    affected = plan.get("affected_responsibilities")
    if not isinstance(affected, list) or not affected or not all(
        isinstance(value, str) and value.strip() for value in affected
    ):
        raise EvaluationError("plan requires affected responsibilities")
    environment = plan.get("environment")
    if not isinstance(environment, dict) or environment.get("sandbox") not in {
        "read-only",
        "workspace-write",
    }:
        raise EvaluationError("plan has an invalid environment")
    if not all(
        isinstance(environment.get(field), str) and environment[field].strip()
        for field in ("model", "reasoning_effort")
    ):
        raise EvaluationError("plan model and reasoning effort must be non-empty strings")
    cases = plan.get("cases")
    if not isinstance(cases, list) or not all(
        isinstance(case, dict)
        and isinstance(case.get("id"), str)
        and isinstance(case.get("prompt"), str)
        for case in cases
    ):
        raise EvaluationError("plan cases are invalid")
    case_ids = [case["id"] for case in cases]
    if len(set(case_ids)) != len(case_ids):
        raise EvaluationError("plan case ids must be unique")
    executions = plan.get("executions")
    if not isinstance(executions, list):
        raise EvaluationError("plan executions must be an array")
    execution_pairs: list[tuple[str, str]] = []
    for execution in executions:
        case_id = execution.get("case_id") if isinstance(execution, dict) else None
        condition = execution.get("condition") if isinstance(execution, dict) else None
        if case_id not in case_ids or condition not in CONDITIONS:
            raise EvaluationError("plan execution references an invalid case or condition")
        execution_pairs.append((case_id, condition))
    if len(set(execution_pairs)) != len(execution_pairs):
        raise EvaluationError("plan executions must be unique")
    conditions = {condition for _, condition in execution_pairs}
    if plan["path"] == "static-only" and execution_pairs:
        raise EvaluationError("static-only plan must not include model executions")
    if plan["path"] not in {"static-only", "baseline-comparison"} and any(
        condition != "candidate" for condition in conditions
    ):
        raise EvaluationError("comparison conditions require the baseline-comparison path")
    if plan["path"] == "baseline-comparison" and (
        "candidate" not in conditions or not ({"baseline", "without-skill"} & conditions)
    ):
        raise EvaluationError("baseline-comparison plan lacks a comparison condition")
    coexistence = plan.get("coexistence_skills", [])
    if not isinstance(coexistence, list) or not all(isinstance(value, str) for value in coexistence):
        raise EvaluationError("plan coexistence_skills must be an array of Skill names")
    for coexistence_skill in coexistence:
        validate_skill_name(coexistence_skill)
    if plan.get("estimated_model_calls") != len(executions):
        raise EvaluationError("plan model-call estimate does not match executions")
    return plan


def verify_candidate_bindings(root: Path, plan: dict[str, Any]) -> None:
    skill_root = root / "skills" / plan["skill"]
    candidate = plan.get("candidate")
    files = candidate.get("files") if isinstance(candidate, dict) else None
    if not isinstance(files, dict):
        raise EvaluationError("plan candidate.files must be an object")
    for relative, expected in files.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise EvaluationError("plan candidate file bindings must be strings")
        target = (skill_root / relative).resolve()
        if not contained(skill_root, target) or not target.is_file():
            raise EvaluationError(f"bound candidate file is missing or outside the Skill: {relative}")
        actual = sha256(target)
        if actual != expected:
            raise EvaluationError(f"bound candidate file changed after planning: {relative}")


def copy_working_skill(root: Path, skill: str, destination: Path) -> None:
    validate_skill_name(skill)
    source = root / "skills" / skill
    if not (source / "SKILL.md").is_file():
        raise EvaluationError(f"coexistence Skill does not exist: {skill}")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("evals"))


def copy_baseline_skill(root: Path, skill: str, commit: str, destination: Path) -> None:
    prefix = f"skills/{skill}"
    listing = git(root, "ls-tree", "-r", "--name-only", commit, "--", prefix)
    files = [value for value in listing.splitlines() if value]
    if f"{prefix}/SKILL.md" not in files:
        raise EvaluationError(f"baseline commit does not contain Skill `{skill}`")
    for relative in files:
        suffix = Path(relative).relative_to(prefix)
        if suffix.parts and suffix.parts[0] == "evals":
            continue
        target = destination / suffix
        target.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"{commit}:{relative}"],
            capture_output=True,
        )
        if result.returncode != 0:
            raise EvaluationError(f"could not materialize baseline file: {relative}")
        target.write_bytes(result.stdout)


def copy_case_files(root: Path, case: dict[str, Any], fixture: Path) -> None:
    for value in case.get("files", []):
        source = (root / value).resolve()
        if not contained(root, source) or not source.is_file():
            raise EvaluationError(f"case file is missing or outside the repository: {value}")
        destination = fixture / "inputs" / value
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    for value, content in case.get("inline_files", {}).items():
        relative = Path(value)
        if relative.parts and relative.parts[0] in {".agents", ".git"}:
            raise EvaluationError(f"inline fixture file may not replace agent or Git state: {value}")
        destination = (fixture / value).resolve()
        if not contained(fixture, destination):
            raise EvaluationError(f"inline fixture file escapes the disposable fixture: {value}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def direct_skill_load_observation(events: list[dict[str, Any]], skill: str) -> str:
    needles = (f"/skills/{skill}/SKILL.md", f"\\skills\\{skill}\\SKILL.md")

    def visit(value: Any, key: str = "") -> bool:
        if isinstance(value, dict):
            return any(visit(child, str(child_key)) for child_key, child in value.items())
        if isinstance(value, list):
            return any(visit(child, key) for child in value)
        if isinstance(value, str) and key in {"command", "path", "file_path"}:
            normalized = value.replace("\\", "/")
            return any(needle.replace("\\", "/") in normalized for needle in needles)
        return False

    for event in events:
        if event.get("type") != "item.completed" or not isinstance(event.get("item"), dict):
            continue
        item = event["item"]
        if item.get("type") == "command_execution" and item.get("exit_code") == 0 and visit(item):
            return "observed"
        if item.get("type") in {"file_read", "tool_call"} and visit(item):
            return "observed"
    return "not_exposed"


def build_executor_prompt(plan: dict[str, Any], case: dict[str, Any]) -> str:
    prompt = case["prompt"]
    if case.get("input_mode") in {"transcript", "authoring-transcript", "conversation"}:
        prompt = (
            "Treat the supplied turns as conversation context and produce the assistant response "
            "to the final user request.\n\n"
            + prompt
        )
    if plan["path"] == "targeted-routing":
        return prompt
    return (
        f"Use the `{plan['skill']}` Skill available in this environment to handle the request below. "
        "Return only the task result; do not discuss the evaluation.\n\n"
        + prompt
    )


def parse_jsonl(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise EvaluationError(f"Codex emitted invalid JSONL on line {line_number}: {error.msg}") from error
        if not isinstance(event, dict):
            raise EvaluationError(f"Codex emitted a non-object JSONL event on line {line_number}")
        events.append(event)
    return events


def run_static_check(root: Path, artifacts: Path, skill: str) -> dict[str, Any]:
    checker = root / "scripts" / "check_repository.py"
    if not checker.is_file():
        return {"status": "unavailable", "reason": "scripts/check_repository.py is missing"}
    result = subprocess.run(
        [
            sys.executable,
            str(checker),
            "--root",
            str(root),
            "--ignore-report-for-skill",
            skill,
        ],
        text=True,
        capture_output=True,
    )
    (artifacts / "static-check.stdout.txt").write_text(result.stdout, encoding="utf-8")
    (artifacts / "static-check.stderr.txt").write_text(result.stderr, encoding="utf-8")
    return {"status": "pass" if result.returncode == 0 else "fail", "exit_code": result.returncode}


def codex_version(codex_bin: str) -> str:
    try:
        result = subprocess.run([codex_bin, "--version"], text=True, capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"
    return (result.stdout.strip() or result.stderr.strip() or "unavailable").splitlines()[0]


def execute_case(
    root: Path,
    artifacts: Path,
    plan: dict[str, Any],
    case: dict[str, Any],
    execution: dict[str, str],
    index: int,
    codex_bin: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    condition = execution["condition"]
    safe_case_id = "".join(character if character.isalnum() or character in "-_" else "_" for character in case["id"])
    relative_directory = Path("executions") / f"{index:03d}-{condition}-{safe_case_id}"
    directory = artifacts / relative_directory
    fixture = directory / "fixture"
    skills_directory = fixture / ".agents" / "skills"
    skills_directory.mkdir(parents=True)
    target = skills_directory / plan["skill"]
    if condition == "candidate":
        copy_working_skill(root, plan["skill"], target)
    elif condition == "baseline":
        copy_baseline_skill(root, plan["skill"], plan["base"]["commit"], target)
    elif condition != "without-skill":
        raise EvaluationError(f"unsupported execution condition: {condition}")
    for coexistence_skill in plan.get("coexistence_skills", []):
        if coexistence_skill != plan["skill"]:
            copy_working_skill(root, coexistence_skill, skills_directory / coexistence_skill)
    copy_case_files(root, case, fixture)
    prompt = build_executor_prompt(plan, case)
    final_output = directory / "last-message.txt"
    command = [
        codex_bin,
        "exec",
        "--ephemeral",
        "--json",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
        "--sandbox",
        plan["environment"]["sandbox"],
        "--model",
        plan["environment"]["model"],
        "-c",
        f'model_reasoning_effort="{plan["environment"]["reasoning_effort"]}"',
        "-C",
        str(fixture),
        "--output-last-message",
        str(final_output),
        "-",
    ]
    record: dict[str, Any] = {
        "case_id": case["id"],
        "condition": condition,
        "artifact_directory": relative_directory.as_posix(),
    }
    try:
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            cwd=fixture,
        )
    except subprocess.TimeoutExpired as error:
        (directory / "events.jsonl").write_text(error.stdout or "", encoding="utf-8")
        (directory / "stderr.txt").write_text(error.stderr or "", encoding="utf-8")
        record.update({"status": "error", "error": "timeout"})
        return record
    except OSError as error:
        record.update({"status": "error", "error": f"could not start Codex: {error}"})
        return record
    (directory / "events.jsonl").write_text(result.stdout, encoding="utf-8")
    (directory / "stderr.txt").write_text(result.stderr, encoding="utf-8")
    if result.returncode != 0:
        record.update({"status": "error", "error": f"Codex exited with status {result.returncode}"})
        return record
    try:
        events = parse_jsonl(result.stdout)
    except EvaluationError as error:
        record.update({"status": "error", "error": str(error)})
        return record
    record["status"] = "completed"
    if plan["path"] == "targeted-routing":
        record["skill_load"] = direct_skill_load_observation(events, plan["skill"])
    return record


def command_run(args: argparse.Namespace, root: Path, codex_bin: str) -> int:
    if not args.execute:
        raise EvaluationError("run requires --execute")
    plan = load_plan(args.plan.resolve(), root)
    estimated = plan["estimated_model_calls"]
    if estimated > args.max_model_calls:
        raise EvaluationError(
            f"plan requires {estimated} model call(s), which exceeds --max-model-calls={args.max_model_calls}"
        )
    if args.max_model_calls < 0:
        raise EvaluationError("--max-model-calls must be non-negative")
    if args.timeout_seconds < 1:
        raise EvaluationError("--timeout-seconds must be positive")
    verify_candidate_bindings(root, plan)
    artifacts = args.artifacts_dir.resolve()
    require_temporary_path(root, artifacts, "artifacts directory")
    try:
        artifacts.mkdir(parents=True, exist_ok=False)
    except FileExistsError as error:
        raise EvaluationError(f"artifacts directory already exists: {artifacts}") from error
    run: dict[str, Any] = {
        "schema_version": RUN_VERSION,
        "skill": plan["skill"],
        "plan": str(args.plan.resolve()),
        "client": codex_version(codex_bin),
        "environment": plan["environment"],
        "static_check": run_static_check(root, artifacts, plan["skill"]),
        "executions": [],
    }
    cases = {case["id"]: case for case in plan["cases"]}
    for index, execution in enumerate(plan["executions"], start=1):
        run["executions"].append(
            execute_case(
                root,
                artifacts,
                plan,
                cases[execution["case_id"]],
                execution,
                index,
                codex_bin,
                args.timeout_seconds,
            )
        )
    write_json(artifacts / "run.json", run)
    print(f"Run record written to {artifacts / 'run.json'}")
    failed = run["static_check"]["status"] == "fail" or any(
        execution["status"] == "error" for execution in run["executions"]
    )
    return 1 if failed else 0


def validate_grade_result(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvaluationError("every grade result must be an object")
    case_id = value.get("case_id")
    condition = value.get("condition")
    status = value.get("status")
    evidence = value.get("evidence")
    if not isinstance(case_id, str) or not case_id:
        raise EvaluationError("every grade result requires a non-empty case_id")
    if condition not in CONDITIONS:
        raise EvaluationError(f"grade result `{case_id}` has an invalid condition")
    if status not in STATUSES:
        raise EvaluationError(f"grade result `{case_id}` has an invalid status")
    if not isinstance(evidence, str) or not evidence.strip():
        raise EvaluationError(f"grade result `{case_id}` requires concise evidence")
    requirements = value.get("requirements", [])
    if not isinstance(requirements, list):
        raise EvaluationError(f"grade result `{case_id}` requirements must be an array")
    normalized_requirements = []
    seen: set[str] = set()
    for requirement in requirements:
        if not isinstance(requirement, dict):
            raise EvaluationError(f"grade result `{case_id}` requirements must be objects")
        requirement_id = requirement.get("id")
        requirement_status = requirement.get("status")
        requirement_evidence = requirement.get("evidence")
        if not isinstance(requirement_id, str) or not requirement_id or requirement_id in seen:
            raise EvaluationError(f"grade result `{case_id}` requirement ids must be unique non-empty strings")
        if requirement_status not in STATUSES:
            raise EvaluationError(f"grade result `{case_id}` requirement `{requirement_id}` has an invalid status")
        if not isinstance(requirement_evidence, str) or not requirement_evidence.strip():
            raise EvaluationError(f"grade result `{case_id}` requirement `{requirement_id}` requires evidence")
        seen.add(requirement_id)
        normalized_requirements.append(
            {"id": requirement_id, "status": requirement_status, "evidence": requirement_evidence}
        )
    return {
        "case_id": case_id,
        "condition": condition,
        "status": status,
        "requirements": normalized_requirements,
        "evidence": evidence,
    }


def aggregate_status(results: list[dict[str, Any]], static_status: str) -> str:
    statuses = [result["status"] for result in results]
    if "error" in statuses:
        return "error"
    if static_status == "fail" or "fail" in statuses:
        return "fail"
    if static_status == "unavailable" or "inconclusive" in statuses:
        return "inconclusive"
    return "pass"


def make_report(
    root: Path,
    plan: dict[str, Any],
    run: dict[str, Any],
    grades: dict[str, Any] | None,
    stopping_reason: str,
    unverified: list[str],
) -> dict[str, Any]:
    if run.get("schema_version") != RUN_VERSION or run.get("skill") != plan["skill"]:
        raise EvaluationError("run record does not match the plan Skill or schema")
    run_executions = run.get("executions")
    if not isinstance(run_executions, list):
        raise EvaluationError("run executions must be an array")
    completed: set[tuple[str, str]] = set()
    execution_errors: list[dict[str, Any]] = []
    for execution in run_executions:
        if not isinstance(execution, dict):
            raise EvaluationError("run executions must be objects")
        pair = (execution.get("case_id"), execution.get("condition"))
        if not all(isinstance(value, str) for value in pair):
            raise EvaluationError("run execution requires case_id and condition")
        if execution.get("status") == "completed":
            completed.add(pair)
        elif execution.get("status") == "error":
            execution_errors.append(
                {
                    "case_id": pair[0],
                    "condition": pair[1],
                    "status": "error",
                    "requirements": [],
                    "evidence": execution.get("error", "executor error"),
                }
            )
        else:
            raise EvaluationError(f"run execution `{pair[0]}` has an invalid status")
    grade_results: list[dict[str, Any]] = []
    if grades is not None:
        if grades.get("schema_version") != 1 or not isinstance(grades.get("results"), list):
            raise EvaluationError("grades require schema_version 1 and a results array")
        grade_results = [validate_grade_result(value) for value in grades["results"]]
    grade_pairs = [(value["case_id"], value["condition"]) for value in grade_results]
    if len(set(grade_pairs)) != len(grade_pairs):
        raise EvaluationError("grades contain duplicate case-condition results")
    if set(grade_pairs) != completed:
        missing = sorted(completed - set(grade_pairs))
        extra = sorted(set(grade_pairs) - completed)
        details = []
        if missing:
            details.append(f"missing grades: {missing}")
        if extra:
            details.append(f"extra grades: {extra}")
        raise EvaluationError("grades do not match completed executions; " + "; ".join(details))
    cases_by_id = {case["id"]: case for case in plan["cases"]}
    for result in grade_results:
        expected_assertions = set(cases_by_id[result["case_id"]].get("assertions", []))
        graded_assertions = {requirement["id"] for requirement in result["requirements"]}
        if expected_assertions and graded_assertions != expected_assertions:
            missing = sorted(expected_assertions - graded_assertions)
            extra = sorted(graded_assertions - expected_assertions)
            details = []
            if missing:
                details.append(f"missing requirement grades: {missing}")
            if extra:
                details.append(f"extra requirement grades: {extra}")
            raise EvaluationError(
                f"grades for case `{result['case_id']}` do not match assigned assertions; "
                + "; ".join(details)
            )
    execution_by_pair = {
        (execution["case_id"], execution["condition"]): execution for execution in run_executions
    }
    if plan["path"] == "targeted-routing":
        for result in grade_results:
            execution = execution_by_pair[(result["case_id"], result["condition"])]
            result["skill_load"] = execution.get("skill_load", "not_exposed")
    results = grade_results + execution_errors
    static_check = run.get("static_check")
    static_status = static_check.get("status") if isinstance(static_check, dict) else None
    if static_status not in {"pass", "fail", "unavailable"}:
        raise EvaluationError("run static_check has an invalid status")
    selected_cases = []
    for case in plan["cases"]:
        selected_cases.append(
            {
                "id": case["id"],
                "conditions": [
                    execution["condition"]
                    for execution in plan["executions"]
                    if execution["case_id"] == case["id"]
                ],
            }
        )
    summary_status = aggregate_status(results, static_status)
    return {
        "schema_version": REPORT_VERSION,
        "skill": plan["skill"],
        "evaluated_on": datetime.now(timezone.utc).date().isoformat(),
        "purpose": plan["purpose"],
        "affected_responsibilities": plan["affected_responsibilities"],
        "selection": {"path": plan["path"], "cases": selected_cases},
        "base": {"commit": plan["base"]["commit"]},
        "candidate": plan["candidate"],
        "environment": {
            "client": run.get("client", "unavailable"),
            "model": plan["environment"]["model"],
            "reasoning_effort": plan["environment"]["reasoning_effort"],
            "sandbox": plan["environment"]["sandbox"],
        },
        "checks": {"repository": static_status},
        "results": results,
        "summary": {
            "status": summary_status,
            "counts": {status: sum(result["status"] == status for result in results) for status in sorted(STATUSES)},
        },
        "stopping_reason": stopping_reason,
        "unverified": unverified,
    }


def command_report(args: argparse.Namespace, root: Path) -> int:
    plan = load_plan(args.plan.resolve(), root)
    verify_candidate_bindings(root, plan)
    run_path = args.run.resolve()
    require_temporary_path(root, run_path, "run record")
    run = read_json(run_path)
    grades = None
    if args.grades is not None:
        grades_path = args.grades.resolve()
        require_temporary_path(root, grades_path, "grades")
        grades = read_json(grades_path)
    report = make_report(root, plan, run, grades, args.stopping_reason, args.unverified or [])
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        destination = root / "skills" / plan["skill"] / "evals" / "report.json"
        destination.write_text(rendered, encoding="utf-8")
        print(f"Report written to {destination.relative_to(root)}")
    else:
        sys.stdout.write(rendered)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--codex-bin", default="codex")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan", help="create a zero-model-call evaluation plan")
    plan.add_argument("--skill", required=True)
    plan.add_argument("--path", required=True, choices=sorted(PATHS))
    plan.add_argument("--purpose", required=True)
    plan.add_argument("--affected", action="append", required=True)
    plan.add_argument("--case", action="append")
    plan.add_argument("--condition", action="append", choices=sorted(CONDITIONS))
    plan.add_argument("--base-ref", default="origin/main")
    plan.add_argument("--model", default="gpt-5.6-sol")
    plan.add_argument("--reasoning-effort", default="high")
    plan.add_argument("--sandbox", choices=("read-only", "workspace-write"), default="read-only")
    plan.add_argument("--output", type=Path, required=True)

    run = subparsers.add_parser("run", help="execute an approved evaluation plan")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--artifacts-dir", type=Path, required=True)
    run.add_argument("--execute", action="store_true")
    run.add_argument("--max-model-calls", type=int, required=True)
    run.add_argument("--timeout-seconds", type=int, default=300)

    report = subparsers.add_parser("report", help="preview or write a compact evaluation report")
    report.add_argument("--plan", type=Path, required=True)
    report.add_argument("--run", type=Path, required=True)
    report.add_argument("--grades", type=Path)
    report.add_argument("--stopping-reason", required=True)
    report.add_argument("--unverified", action="append")
    report.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"repository root is not a directory: {root}")
    try:
        if args.command == "plan":
            return command_plan(args, root)
        if args.command == "run":
            return command_run(args, root, args.codex_bin)
        if args.command == "report":
            return command_report(args, root)
        raise EvaluationError(f"unsupported command: {args.command}")
    except EvaluationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
