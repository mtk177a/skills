#!/usr/bin/env python3
"""Plan, run, and summarize cost-bounded Skill evaluations with Codex."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from evaluation_contract import (
        CONDITIONS,
        SKILL_NAME,
        TRACKED_REPOSITORY_LOCAL_SKILLS,
        REPOSITORY_LOCAL_COMPANIONS,
        EvaluationContractError,
        normalize_case_input_paths as _normalize_case_input_paths,
        normalize_evaluation_document,
        reject_repository_local_companion_fixture_paths,
        validate_evaluation_references,
    )
except ModuleNotFoundError:  # Imported as scripts.run_skill_evaluation in unit tests.
    from scripts.evaluation_contract import (
        CONDITIONS,
        SKILL_NAME,
        TRACKED_REPOSITORY_LOCAL_SKILLS,
        REPOSITORY_LOCAL_COMPANIONS,
        EvaluationContractError,
        normalize_case_input_paths as _normalize_case_input_paths,
        normalize_evaluation_document,
        reject_repository_local_companion_fixture_paths,
        validate_evaluation_references,
    )


PLAN_VERSION = 3
RUN_VERSION = 2
GRADES_VERSION = 2
REPORT_VERSION = 2
MODEL_PATHS = {
    "targeted-candidate",
    "targeted-routing",
    "baseline-comparison",
    "target-environment",
}
PATHS = {"static-only", *MODEL_PATHS}
STATUSES = {"pass", "fail", "inconclusive", "error"}
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
FILE_MODES = {"100644": 0o644, "100755": 0o755}
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9:])(?:/[A-Za-z0-9._-][^\s\"'`<>]*|[A-Za-z]:\\[^\s\"'`<>]+)")


class EvaluationError(Exception):
    """A user-facing evaluation configuration or execution error."""


def normalize_case_input_paths(values: Any, case_id: str) -> list[str]:
    try:
        return _normalize_case_input_paths(values, case_id)
    except EvaluationContractError as error:
        raise EvaluationError(str(error)) from error


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


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def document_digest(value: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def attach_plan_digest(plan: dict[str, Any]) -> dict[str, Any]:
    unsigned = {key: value for key, value in plan.items() if key != "plan_digest"}
    return {**unsigned, "plan_digest": document_digest(unsigned)}


def verify_plan_digest(plan: dict[str, Any]) -> None:
    expected = plan.get("plan_digest")
    unsigned = {key: value for key, value in plan.items() if key != "plan_digest"}
    if not isinstance(expected, str) or expected != document_digest(unsigned):
        raise EvaluationError("plan digest does not match the normalized plan")


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


def candidate_prefix(skill: str, skill_source: str = "public") -> Path:
    validate_skill_name(skill)
    if skill_source == "public":
        return Path("skills") / skill
    if skill_source == "repository-local" and skill in TRACKED_REPOSITORY_LOCAL_SKILLS:
        return Path(".agents") / "skills" / skill
    raise EvaluationError(f"unsupported Skill source or untracked repository-local Skill: {skill_source}/{skill}")


def require_tracked_repository_local_skill(root: Path, skill: str, skill_source: str) -> None:
    if skill_source != "repository-local":
        return
    source = candidate_prefix(skill, skill_source) / "SKILL.md"
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", source.as_posix()],
        text=True, capture_output=True,
    )
    if result.returncode != 0:
        raise EvaluationError(f"repository-local Skill must be tracked by Git: {source}")


def reject_absolute_path(value: str, label: str) -> None:
    match = ABSOLUTE_PATH.search(value)
    if match is not None:
        raise EvaluationError(f"{label} must not contain an absolute path: {match.group(0)}")


def load_case_asset(root: Path, skill: str, evaluation_path: str, skill_source: str = "public") -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    asset_name = "triggers.json" if evaluation_path == "targeted-routing" else "evals.json"
    asset = root / candidate_prefix(skill, skill_source) / "evals" / asset_name
    if not asset.is_file():
        raise EvaluationError(f"evaluation asset does not exist: {asset.relative_to(root)}")
    document = read_json(asset)
    if "skill_name" not in document and "evals" not in document:
        shape = "scenarios" if "scenarios" in document else "legacy {skill, cases}"
        raise EvaluationError(
            f"{asset.relative_to(root)} uses the unsupported {shape} evaluation format; "
            "migrate the Skill's complete evals.json and triggers.json set to {skill_name, evals} "
            "before using a model-backed path"
        )
    for sibling_name in ("evals.json", "triggers.json"):
        sibling = asset.parent / sibling_name
        if sibling == asset or not sibling.is_file():
            continue
        sibling_document = read_json(sibling)
        if "skill_name" not in sibling_document and "evals" not in sibling_document:
            shape = "scenarios" if "scenarios" in sibling_document else "legacy {skill, cases}"
            raise EvaluationError(
                f"{sibling.relative_to(root)} uses the unsupported {shape} evaluation format; "
                "migrate the Skill's complete evals.json and triggers.json set to {skill_name, evals} "
                "before using a model-backed path"
            )
        try:
            sibling_normalized = normalize_evaluation_document(
                sibling_document,
                expected_skill=skill,
                definition_kind="routing" if sibling_name == "triggers.json" else "behavior",
            )
            validate_evaluation_references(sibling_normalized, root, repository_local=skill_source == "repository-local")
        except EvaluationContractError as error:
            raise EvaluationError(str(error)) from error
    try:
        normalized = normalize_evaluation_document(
            document,
            expected_skill=skill,
            definition_kind="routing" if evaluation_path == "targeted-routing" else "behavior",
        )
        validate_evaluation_references(normalized, root, repository_local=skill_source == "repository-local")
    except EvaluationContractError as error:
        raise EvaluationError(str(error)) from error
    return asset, normalized, normalized["cases"]


def default_conditions(evaluation_path: str) -> list[str]:
    if evaluation_path == "static-only":
        return []
    if evaluation_path == "baseline-comparison":
        return ["candidate", "baseline"]
    return ["candidate"]


def regular_file_manifest_entry(path: Path) -> dict[str, str]:
    mode = "100755" if path.stat().st_mode & 0o111 else "100644"
    return {"sha256": sha256(path), "mode": mode}


def validate_skill_manifest(files: Any, label: str) -> dict[str, dict[str, str]]:
    if not isinstance(files, dict):
        raise EvaluationError(f"{label} manifest must be an object")
    for name, entry in files.items():
        if (
            not isinstance(name, str)
            or not isinstance(entry, dict)
            or set(entry) != {"sha256", "mode"}
            or not isinstance(entry.get("sha256"), str)
            or SHA256.fullmatch(entry["sha256"]) is None
            or entry.get("mode") not in FILE_MODES
        ):
            raise EvaluationError(
                f"{label} manifest entries must contain a sha256 hash and mode 100644 or 100755"
            )
    return files


def skill_manifest(root: Path, skill: str, skill_source: str = "public") -> dict[str, dict[str, str]]:
    skill_root = root / candidate_prefix(skill, skill_source)
    if not (skill_root / "SKILL.md").is_file():
        raise EvaluationError(f"Skill does not exist: {skill}")
    bindings: dict[str, dict[str, str]] = {}
    for target in sorted(skill_root.rglob("*")):
        relative = target.relative_to(skill_root)
        if relative.parts and relative.parts[0] == "evals":
            continue
        if target.is_symlink():
            raise EvaluationError(f"Skill execution trees must not contain symlinks: {target.relative_to(root)}")
        if target.is_file():
            bindings[relative.as_posix()] = regular_file_manifest_entry(target)
    return bindings


def case_file_manifest(root: Path, cases: list[dict[str, Any]]) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for case in cases:
        for name in normalize_case_input_paths(case.get("files"), case["id"]):
            unresolved = root / name
            source = unresolved.resolve()
            if not contained(root, source) or not unresolved.is_file() or unresolved.is_symlink():
                raise EvaluationError(f"case input file must be a regular repository file: {name}")
            bindings[name] = sha256(source)
    return dict(sorted(bindings.items()))


def verify_file_manifest(base: Path, files: Any, label: str) -> None:
    validated = validate_skill_manifest(files, label)
    current: dict[str, dict[str, str]] = {}
    if base.is_dir():
        for target in sorted(base.rglob("*")):
            relative = target.relative_to(base)
            if relative.parts and relative.parts[0] == "evals" and label.endswith("Skill"):
                continue
            if target.is_symlink():
                raise EvaluationError(f"{label} manifest changed after planning: {relative.as_posix()}")
            if target.is_file():
                current[relative.as_posix()] = regular_file_manifest_entry(target)
    if current != validated:
        raise EvaluationError(f"{label} manifest changed after planning")


def verify_root_file_manifest(root: Path, files: Any, label: str) -> None:
    if not isinstance(files, dict):
        raise EvaluationError(f"{label} manifest must be an object")
    for name, expected in files.items():
        if not isinstance(name, str) or not isinstance(expected, str):
            raise EvaluationError(f"{label} manifest must map paths to hashes")
        target = (root / name).resolve()
        if not contained(root, target) or not target.is_file() or target.is_symlink() or sha256(target) != expected:
            raise EvaluationError(f"{label} changed after planning: {name}")


def make_plan(args: argparse.Namespace, root: Path) -> dict[str, Any]:
    skill_source = args.skill_source
    skill_root = root / candidate_prefix(args.skill, skill_source)
    require_tracked_repository_local_skill(root, args.skill, skill_source)
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
    global_coexistence_skills: list[str] = []
    if args.path in MODEL_PATHS:
        if not args.case:
            raise EvaluationError("model-backed evaluation requires at least one --case")
        asset, document, available = load_case_asset(root, args.skill, args.path, skill_source)
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
        source = {"file": asset.relative_to(root).as_posix(), "format": "agent-skills"}
        global_coexistence_skills = document["execution"]["coexistence_skills"]
    elif args.case or args.condition:
        raise EvaluationError("static-only does not accept cases or conditions")

    executions = [
        {
            "case_id": case["id"],
            "condition": condition,
            "coexistence_skills": sorted({*global_coexistence_skills, *case["coexistence_skills"]}),
        }
        for case in selected_cases
        for condition in conditions
    ]
    coexistence_skills = sorted(
        {skill for execution in executions for skill in execution["coexistence_skills"]}
    )
    companion_manifests = {skill: {"files": skill_manifest(root, skill)} for skill in coexistence_skills}
    evaluation_files = {} if asset is None else {asset.relative_to(root).as_posix(): sha256(asset)}
    plan: dict[str, Any] = {
        "schema_version": PLAN_VERSION,
        "skill": args.skill,
        "skill_source": skill_source,
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
        "candidate": {"files": skill_manifest(root, args.skill, skill_source)},
        "inputs": {
            "evaluation_files": evaluation_files,
            "case_files": case_file_manifest(root, selected_cases),
            "companions": companion_manifests,
        },
        "coexistence_skills": coexistence_skills,
    }
    if source is not None:
        plan["source"] = source
    return attach_plan_digest(plan)


def command_plan(args: argparse.Namespace, root: Path) -> int:
    output = args.output.resolve()
    require_temporary_path(root, output, "plan output")
    plan = make_plan(args, root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical_json(plan) + "\n", encoding="utf-8")
    print(f"Plan written to {output}")
    print(f"Estimated model calls: {plan['estimated_model_calls']}")
    return 0


def load_plan(path: Path, root: Path) -> dict[str, Any]:
    require_temporary_path(root, path, "plan")
    plan = read_json(path)
    return validate_plan(plan, root)


def validate_plan(plan: dict[str, Any], root: Path) -> dict[str, Any]:
    if plan.get("schema_version") != PLAN_VERSION:
        raise EvaluationError(f"unsupported plan schema_version: {plan.get('schema_version')}")
    verify_plan_digest(plan)
    skill = plan.get("skill")
    if not isinstance(skill, str):
        raise EvaluationError("plan references an unknown Skill")
    skill_source = plan.get("skill_source", "public")
    skill_root = root / candidate_prefix(skill, skill_source)
    require_tracked_repository_local_skill(root, skill, skill_source)
    if not (skill_root / "SKILL.md").is_file():
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
    base = plan.get("base")
    if (
        not isinstance(base, dict)
        or not isinstance(base.get("ref"), str)
        or not base["ref"].strip()
        or not isinstance(base.get("commit"), str)
        or re.fullmatch(r"[0-9a-f]{40,64}", base["commit"]) is None
    ):
        raise EvaluationError("plan base requires a ref and full commit id")
    cases = plan.get("cases")
    if not isinstance(cases, list) or not all(
        isinstance(case, dict)
        and isinstance(case.get("id"), str)
        and isinstance(case.get("prompt"), str)
        and isinstance(case.get("grading_requirements"), list)
        for case in cases
    ):
        raise EvaluationError("plan cases are invalid")
    case_ids = [case["id"] for case in cases]
    if len(set(case_ids)) != len(case_ids):
        raise EvaluationError("plan case ids must be unique")
    for case in cases:
        files = case.get("files")
        normalized_files = normalize_case_input_paths(files, case["id"])
        if files != normalized_files:
            raise EvaluationError(f"plan case `{case['id']}` input paths must be normalized")
        inline_files = case.get("inline_files")
        baseline_files = case.get("baseline_files", {})
        if not isinstance(inline_files, dict) or not all(
            isinstance(name, str) and isinstance(content, str) for name, content in inline_files.items()
        ):
            raise EvaluationError(f"plan case `{case['id']}` inline files are invalid")
        if not isinstance(baseline_files, dict) or not all(
            isinstance(name, str) and isinstance(content, str) for name, content in baseline_files.items()
        ):
            raise EvaluationError(f"plan case `{case['id']}` baseline files are invalid")
        for name in {*inline_files, *baseline_files}:
            if name.split("/")[0] in {".agents", ".git"} or normalize_case_input_paths([name], case["id"]) != [name]:
                raise EvaluationError(f"plan case `{case['id']}` has an unsafe fixture path: {name}")
        if not set(baseline_files).issubset(inline_files):
            raise EvaluationError(f"plan case `{case['id']}` baseline files lack current counterparts")
        skills = case.get("coexistence_skills")
        if not isinstance(skills, list) or not all(
            isinstance(skill, str) and SKILL_NAME.fullmatch(skill) for skill in skills
        ) or len(skills) != len(set(skills)):
            raise EvaluationError("plan case coexistence_skills must be unique Skill names")
    cases_by_id = {case["id"]: case for case in cases}
    executions = plan.get("executions")
    if not isinstance(executions, list):
        raise EvaluationError("plan executions must be an array")
    execution_pairs: list[tuple[str, str]] = []
    execution_coexistence: set[str] = set()
    for execution in executions:
        case_id = execution.get("case_id") if isinstance(execution, dict) else None
        condition = execution.get("condition") if isinstance(execution, dict) else None
        if case_id not in case_ids or condition not in CONDITIONS:
            raise EvaluationError("plan execution references an invalid case or condition")
        skills = execution.get("coexistence_skills")
        if not isinstance(skills, list) or not all(
            isinstance(skill, str) and SKILL_NAME.fullmatch(skill) for skill in skills
        ) or skills != sorted(set(skills)):
            raise EvaluationError("plan execution coexistence_skills must be sorted unique Skill names")
        if not set(cases_by_id[case_id]["coexistence_skills"]).issubset(skills):
            raise EvaluationError("plan execution omits a case coexistence Skill")
        if skill_source == "repository-local":
            try:
                reject_repository_local_companion_fixture_paths(cases_by_id[case_id], set(skills))
            except EvaluationContractError as error:
                raise EvaluationError(str(error)) from error
        execution_coexistence.update(skills)
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
    if coexistence != sorted(execution_coexistence):
        raise EvaluationError("plan coexistence_skills do not match its executions")
    if plan.get("estimated_model_calls") != len(executions):
        raise EvaluationError("plan model-call estimate does not match executions")
    candidate = plan.get("candidate")
    inputs = plan.get("inputs")
    if not isinstance(candidate, dict) or not isinstance(candidate.get("files"), dict):
        raise EvaluationError("plan candidate.files must be an object")
    validate_skill_manifest(candidate["files"], "candidate Skill")
    if not isinstance(inputs, dict) or not all(
        isinstance(inputs.get(field), dict) for field in ("evaluation_files", "case_files", "companions")
    ):
        raise EvaluationError("plan inputs manifests are invalid")
    companions = inputs["companions"]
    if set(companions) != set(coexistence):
        raise EvaluationError("companion manifests do not match planned coexistence Skills")
    for companion_skill, manifest in companions.items():
        files = manifest.get("files") if isinstance(manifest, dict) else None
        validate_skill_manifest(files, f"companion {companion_skill} Skill")
    return plan


def verify_candidate_bindings(root: Path, plan: dict[str, Any]) -> None:
    candidate = plan["candidate"]["files"]
    verify_file_manifest(root / candidate_prefix(plan["skill"], plan.get("skill_source", "public")), candidate, "candidate Skill")
    inputs = plan["inputs"]
    verify_root_file_manifest(root, inputs["evaluation_files"], "evaluation input")
    verify_root_file_manifest(root, inputs["case_files"], "case input")
    companions = inputs["companions"]
    if set(companions) != set(plan["coexistence_skills"]):
        raise EvaluationError("companion manifests do not match planned coexistence Skills")
    for skill, manifest in companions.items():
        files = manifest.get("files") if isinstance(manifest, dict) else None
        verify_file_manifest(root / "skills" / skill, files, f"companion {skill} Skill")


def copy_manifest(base: Path, files: dict[str, dict[str, str]], destination: Path) -> None:
    validated = validate_skill_manifest(files, "copy source")
    for relative, entry in sorted(validated.items()):
        source = (base / relative).resolve()
        if not contained(base, source) or not source.is_file() or source.is_symlink():
            raise EvaluationError(f"manifest source is missing or unsafe: {relative}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        target.chmod(FILE_MODES[entry["mode"]])


def copy_baseline_skill(root: Path, skill: str, commit: str, destination: Path, skill_source: str = "public") -> None:
    prefix = candidate_prefix(skill, skill_source).as_posix()
    listing = git(root, "ls-tree", "-r", commit, "--", prefix)
    entries: list[tuple[str, str, str]] = []
    for line in listing.splitlines():
        metadata, separator, relative = line.partition("\t")
        fields = metadata.split()
        if not separator or len(fields) != 3:
            raise EvaluationError("could not parse baseline Skill tree")
        mode, object_type, _object_id = fields
        entries.append((mode, object_type, relative))
    if not any(relative == f"{prefix}/SKILL.md" for _, _, relative in entries):
        raise EvaluationError(f"baseline commit does not contain Skill `{skill}`")
    for mode, object_type, relative in entries:
        suffix = Path(relative).relative_to(prefix)
        if suffix.parts and suffix.parts[0] == "evals":
            continue
        if object_type != "blob" or mode not in FILE_MODES:
            raise EvaluationError(f"baseline Skill contains an unsupported entry: {relative} ({mode} {object_type})")
        target = destination / suffix
        target.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"{commit}:{relative}"],
            capture_output=True,
        )
        if result.returncode != 0:
            raise EvaluationError(f"could not materialize baseline file: {relative}")
        target.write_bytes(result.stdout)
        target.chmod(FILE_MODES[mode])


def copy_case_files(root: Path, case: dict[str, Any], fixture: Path) -> None:
    case_id = case.get("id") if isinstance(case.get("id"), str) else "unknown"
    inputs = fixture / "inputs"
    baseline_files = case.get("baseline_files", {})
    if baseline_files:
        for value, content in baseline_files.items():
            destination = fixture / value
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        for arguments in (
            ["git", "init", "-q", str(fixture)],
            ["git", "-C", str(fixture), "config", "user.name", "Evaluation Fixture"],
            ["git", "-C", str(fixture), "config", "user.email", "evaluation@example.invalid"],
            ["git", "-C", str(fixture), "add", "--", *baseline_files],
            ["git", "-C", str(fixture), "commit", "-qm", "baseline fixture"],
        ):
            result = subprocess.run(arguments, text=True, capture_output=True)
            if result.returncode != 0:
                raise EvaluationError(f"could not prepare Git baseline for case `{case_id}`: {result.stderr.strip()}")
    for value in normalize_case_input_paths(case.get("files", []), case_id):
        unresolved = root / value
        source = unresolved.resolve()
        if not contained(root, source) or not unresolved.is_file() or unresolved.is_symlink():
            raise EvaluationError(f"case file is missing or outside the repository: {value}")
        destination = (inputs / value).resolve()
        if not contained(inputs, destination) or destination == source:
            raise EvaluationError(f"evaluation case `{case_id}` has an unsafe case input path: {value}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
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
        if (
            item.get("type") in {"file_read", "tool_call"}
            and item.get("status") not in {"error", "failed"}
            and not item.get("error")
            and visit(item)
        ):
            return "observed"
    return "not_exposed"


def observed_skill_handlers(events: list[dict[str, Any]], skills: list[str]) -> dict[str, Any]:
    if not any(event.get("type") == "turn.completed" for event in events):
        return {"status": "not_exposed", "handlers": []}
    observed = sorted(skill for skill in skills if direct_skill_load_observation(events, skill) == "observed")
    return {"status": "observed", "handlers": observed}


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


def repository_local_config_args(skill: str, companions: list[str]) -> list[str]:
    names = sorted({skill, *companions, *REPOSITORY_LOCAL_COMPANIONS.get(skill, set())})
    disabled = [
        f'{{path={json.dumps(str(Path.home() / directory / name / "SKILL.md"))},enabled=false}}'
        for directory in (".agents/skills", ".codex/skills")
        for name in names
    ]
    return [
        "-c", "features.plugins=false",
        "-c", "skills.max_context_tokens=10000",
        "-c", "skills.config=[" + ",".join(disabled) + "]",
    ]


def repository_local_catalog_check(
    codex_bin: str,
    fixture: Path,
    skill: str,
    condition: str,
    config_args: list[str],
    companions: list[str] | None = None,
) -> str | None:
    try:
        result = subprocess.run(
            [codex_bin, "debug", "prompt-input", *config_args],
            cwd=fixture, text=True, capture_output=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "could not inspect the model-visible Skill catalog"
    if result.returncode != 0:
        return "could not inspect the model-visible Skill catalog"
    try:
        entries = json.loads(result.stdout)
    except json.JSONDecodeError:
        return "model-visible Skill catalog was not JSON"
    if not isinstance(entries, list):
        return "model-visible Skill catalog was not a list"
    developer_text = "\n".join(
        content.get("text", "")
        for entry in entries if isinstance(entry, dict) and entry.get("role") == "developer"
        for content in entry.get("content", []) if isinstance(content, dict)
    )
    roots = dict(re.findall(r"^- `(?P<alias>r\d+)` = `(?P<path>[^`]+)`$", developer_text, re.MULTILINE))
    for name in sorted({skill, *REPOSITORY_LOCAL_COMPANIONS.get(skill, set()), *(companions or [])}):
        pattern = rf"^- {re.escape(name)}: (?P<description>.+) \(file: (?P<alias>r\d+)/{re.escape(name)}/SKILL\.md\)$"
        matches = list(re.finditer(pattern, developer_text, re.MULTILINE))
        source = fixture / ".agents" / "skills" / name / "SKILL.md"
        if not source.is_file() or (name == skill and condition == "without-skill"):
            if matches:
                return f"personal or same-name {name} Skill was visible without a fixture copy"
            continue
        descriptions = [
            line.removeprefix("description: ")
            for line in source.read_text(encoding="utf-8").splitlines()
            if line.startswith("description: ")
        ]
        if len(descriptions) != 1 or len(matches) != 1:
            return f"{name} Skill description was absent, duplicated, or shortened in the catalog"
        match = matches[0]
        if match.group("description") != descriptions[0]:
            return f"{name} Skill description was shortened or changed in the catalog"
        catalog_root = roots.get(match.group("alias"))
        if catalog_root is None or Path(catalog_root).resolve() != source.parent.parent.resolve():
            return f"same-name {name} Skill in the catalog was not the fixture copy"
    return None


def execute_case(
    root: Path,
    artifacts: Path,
    plan: dict[str, Any],
    case: dict[str, Any],
    execution: dict[str, Any],
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
        copy_manifest(root / candidate_prefix(plan["skill"], plan.get("skill_source", "public")), plan["candidate"]["files"], target)
    elif condition == "baseline":
        copy_baseline_skill(root, plan["skill"], plan["base"]["commit"], target, plan.get("skill_source", "public"))
    elif condition != "without-skill":
        raise EvaluationError(f"unsupported execution condition: {condition}")
    for coexistence_skill in execution["coexistence_skills"]:
        if coexistence_skill != plan["skill"]:
            copy_manifest(
                root / "skills" / coexistence_skill,
                plan["inputs"]["companions"][coexistence_skill]["files"],
                skills_directory / coexistence_skill,
            )
            if plan.get("skill_source", "public") == "repository-local":
                copy_manifest(
                    root / "skills" / coexistence_skill,
                    plan["inputs"]["companions"][coexistence_skill]["files"],
                    fixture / "skills" / coexistence_skill,
                )
    copy_case_files(root, case, fixture)
    prompt = build_executor_prompt(plan, case)
    final_output = directory / "last-message.txt"
    local_source = plan.get("skill_source", "public") == "repository-local"
    config_args = repository_local_config_args(plan["skill"], execution["coexistence_skills"]) if local_source else []
    command = [
        codex_bin,
        "exec",
        "--ephemeral",
        "--json",
        *([] if local_source else ["--ignore-user-config"]),
        "--ignore-rules",
        "--skip-git-repo-check",
        "--sandbox",
        plan["environment"]["sandbox"],
        "--model",
        plan["environment"]["model"],
        *config_args,
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
    if local_source:
        preflight_error = repository_local_catalog_check(
            codex_bin, fixture, plan["skill"], condition, config_args,
            execution["coexistence_skills"],
        )
        if preflight_error is not None:
            record.update({"status": "error", "error": preflight_error, "preflight_failed": True})
            return record
        record["catalog_preflight"] = "pass"
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
        installed = sorted({plan["skill"], *execution["coexistence_skills"]})
        record["routing_observation"] = observed_skill_handlers(events, installed)
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
        "skill_source": plan.get("skill_source", "public"),
        "plan_digest": plan["plan_digest"],
        "plan": plan,
        "client": codex_version(codex_bin),
        "environment": plan["environment"],
        "static_check": run_static_check(root, artifacts, plan["skill"]),
        "executions": [],
    }
    cases = {case["id"]: case for case in plan["cases"]}
    for index, execution in enumerate(plan["executions"], start=1):
        execution_record = execute_case(
            root,
            artifacts,
            plan,
            cases[execution["case_id"]],
            execution,
            index,
            codex_bin,
            args.timeout_seconds,
        )
        run["executions"].append(execution_record)
        if execution_record.get("preflight_failed"):
            break
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
    evidence = value.get("evidence")
    if not isinstance(case_id, str) or not case_id:
        raise EvaluationError("every grade result requires a non-empty case_id")
    if condition not in CONDITIONS:
        raise EvaluationError(f"grade result `{case_id}` has an invalid condition")
    if "status" in value:
        raise EvaluationError(f"grade result `{case_id}` must not provide a case-level status")
    if not isinstance(evidence, str) or not evidence.strip():
        raise EvaluationError(f"grade result `{case_id}` requires concise evidence")
    reject_absolute_path(evidence, f"grade result `{case_id}` evidence")
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
        reject_absolute_path(
            requirement_evidence,
            f"grade result `{case_id}` requirement `{requirement_id}` evidence",
        )
        seen.add(requirement_id)
        normalized_requirements.append(
            {"id": requirement_id, "status": requirement_status, "evidence": requirement_evidence}
        )
    return {
        "case_id": case_id,
        "condition": condition,
        "requirements": normalized_requirements,
        "evidence": evidence,
    }


def derive_case_status(requirements: list[dict[str, Any]]) -> str:
    if any(value["status"] == "error" for value in requirements):
        return "error"
    if any(value["critical"] and value["status"] == "fail" for value in requirements):
        return "fail"
    if any(value["status"] in {"fail", "inconclusive"} for value in requirements):
        return "inconclusive"
    return "pass"


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
    run: dict[str, Any],
    grades: dict[str, Any] | None,
    stopping_reason: str,
    unverified: list[str],
) -> dict[str, Any]:
    if not stopping_reason.strip():
        raise EvaluationError("report requires a non-empty stopping reason")
    reject_absolute_path(stopping_reason, "stopping reason")
    for boundary in unverified:
        if not boundary.strip():
            raise EvaluationError("unverified boundaries must be non-empty")
        reject_absolute_path(boundary, "unverified boundary")
    if run.get("schema_version") != RUN_VERSION:
        raise EvaluationError("run record has an unsupported schema")
    raw_plan = run.get("plan")
    if not isinstance(raw_plan, dict):
        raise EvaluationError("run record requires an embedded plan")
    plan = validate_plan(raw_plan, root)
    if run.get("plan_digest") != plan["plan_digest"]:
        raise EvaluationError("run plan digest does not match the embedded plan")
    if run.get("skill") != plan["skill"] or run.get("environment") != plan["environment"]:
        raise EvaluationError("run record does not match the embedded plan environment")
    verify_candidate_bindings(root, plan)
    run_executions = run.get("executions")
    if not isinstance(run_executions, list):
        raise EvaluationError("run executions must be an array")
    completed: set[tuple[str, str]] = set()
    execution_errors: list[dict[str, Any]] = []
    run_pairs: list[tuple[str, str]] = []
    for execution in run_executions:
        if not isinstance(execution, dict):
            raise EvaluationError("run executions must be objects")
        pair = (execution.get("case_id"), execution.get("condition"))
        if not all(isinstance(value, str) for value in pair):
            raise EvaluationError("run execution requires case_id and condition")
        run_pairs.append(pair)
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
    planned_pairs = [(value["case_id"], value["condition"]) for value in plan["executions"]]
    if run_pairs != planned_pairs:
        raise EvaluationError("run executions do not match the embedded plan")
    grade_results: list[dict[str, Any]] = []
    if grades is not None:
        if grades.get("schema_version") != GRADES_VERSION or not isinstance(grades.get("results"), list):
            raise EvaluationError(f"grades require schema_version {GRADES_VERSION} and a results array")
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
        case = cases_by_id[result["case_id"]]
        definitions = {
            requirement["id"]: requirement
            for requirement in case["grading_requirements"]
            if requirement["id"] != "routing-handlers"
        }
        expected_assertions = set(definitions)
        graded_assertions = {requirement["id"] for requirement in result["requirements"]}
        if graded_assertions != expected_assertions:
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
        normalized_requirements = []
        for requirement in result["requirements"]:
            definition = definitions[requirement["id"]]
            normalized_requirements.append({**requirement, "critical": definition["critical"]})
        if plan["path"] == "targeted-routing":
            execution = next(
                value
                for value in run_executions
                if value["case_id"] == result["case_id"] and value["condition"] == result["condition"]
            )
            observation = execution.get("routing_observation")
            routing_definition = next(
                value for value in case["grading_requirements"] if value["id"] == "routing-handlers"
            )
            expected_handlers = routing_definition["expected_handlers"]
            if not isinstance(observation, dict) or observation.get("status") not in {"observed", "not_exposed"}:
                raise EvaluationError("run routing observation is invalid")
            if observation["status"] == "not_exposed":
                if observation.get("handlers") != []:
                    raise EvaluationError("run routing observation is invalid")
                routing_status = "inconclusive"
                routing_evidence = "Codex did not expose a completed Skill read."
            else:
                handlers = observation.get("handlers")
                if not isinstance(handlers, list) or not all(isinstance(value, str) for value in handlers):
                    raise EvaluationError("run routing observation is invalid")
                routing_status = "pass" if sorted(handlers) == sorted(expected_handlers) else "fail"
                routing_evidence = f"Observed handlers: {', '.join(handlers) if handlers else 'none'}."
            normalized_requirements.append(
                {
                    "id": "routing-handlers",
                    "status": routing_status,
                    "evidence": routing_evidence,
                    "critical": True,
                }
            )
            result["routing_observation"] = observation
        result["requirements"] = normalized_requirements
        result["status"] = derive_case_status(normalized_requirements)
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
        "skill_source": plan.get("skill_source", "public"),
        "evaluated_on": datetime.now(timezone.utc).date().isoformat(),
        "purpose": plan["purpose"],
        "affected_responsibilities": plan["affected_responsibilities"],
        "selection": {"path": plan["path"], "cases": selected_cases},
        "base": {"commit": plan["base"]["commit"]},
        "candidate": plan["candidate"],
        "evaluation_inputs": {
            "evaluation_files": plan["inputs"]["evaluation_files"],
            "case_files": plan["inputs"]["case_files"],
        },
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
    run_path = args.run.resolve()
    require_temporary_path(root, run_path, "run record")
    run = read_json(run_path)
    grades = None
    if args.grades is not None:
        grades_path = args.grades.resolve()
        require_temporary_path(root, grades_path, "grades")
        grades = read_json(grades_path)
    report = make_report(root, run, grades, args.stopping_reason, args.unverified or [])
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.write:
        destination = root / candidate_prefix(report["skill"], report.get("skill_source", "public")) / "evals" / "report.json"
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
    plan.add_argument("--skill-source", choices=("public", "repository-local"), default="public")
    plan.add_argument("--path", required=True, choices=sorted(PATHS))
    plan.add_argument("--purpose", required=True)
    plan.add_argument("--affected", action="append", required=True)
    plan.add_argument("--case", action="append")
    plan.add_argument("--condition", action="append", choices=sorted(CONDITIONS))
    plan.add_argument("--base-ref", default="origin/main")
    plan.add_argument("--model", default="gpt-5.6-luna")
    plan.add_argument("--reasoning-effort", default="max")
    plan.add_argument("--sandbox", choices=("read-only", "workspace-write"), default="read-only")
    plan.add_argument("--output", type=Path, required=True)

    run = subparsers.add_parser("run", help="execute an approved evaluation plan")
    run.add_argument("--plan", type=Path, required=True)
    run.add_argument("--artifacts-dir", type=Path, required=True)
    run.add_argument("--execute", action="store_true")
    run.add_argument("--max-model-calls", type=int, required=True)
    run.add_argument("--timeout-seconds", type=int, default=300)

    report = subparsers.add_parser("report", help="preview or write a compact evaluation report")
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
