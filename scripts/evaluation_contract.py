"""Validate and normalize executable Skill evaluation definitions."""

from __future__ import annotations

import re
from pathlib import Path, PureWindowsPath
from typing import Any


CONDITIONS = {"candidate", "baseline", "without-skill"}
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TRACKED_REPOSITORY_LOCAL_SKILLS = {"maintain-japanese-references"}
REPOSITORY_LOCAL_COMPANIONS = {"maintain-japanese-references": {"write-natural-japanese"}}
TURN_ROLES = {"assistant", "user"}
TOP_LEVEL_FIELDS = {"skill_name", "execution", "evals"}
EXECUTION_FIELDS = {"coexistence_skills"}
CASE_FIELDS = {
    "id",
    "title",
    "prompt",
    "turns",
    "request",
    "authoring_turns",
    "conversation",
    "expected_output",
    "files",
    "assertions",
    "fixture",
    "baseline_files",
    "coexistence_skills",
    "conditions",
    "expected_handlers",
}
INPUT_FIELDS = {"prompt", "turns", "request", "authoring_turns", "conversation"}
VALID_INPUT_SHAPES = (
    frozenset({"prompt"}),
    frozenset({"turns"}),
    frozenset({"request", "authoring_turns"}),
    frozenset({"conversation", "prompt"}),
)


class EvaluationContractError(ValueError):
    """An executable evaluation definition violates the shared contract."""


def _reject_unknown_fields(value: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise EvaluationContractError(f"{label} contains unknown field(s): {', '.join(unknown)}")


def _non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationContractError(f"{label} must be a non-empty string")
    return value


def _unique(values: list[str], label: str) -> list[str]:
    if len(set(values)) != len(values):
        raise EvaluationContractError(f"{label} must not contain duplicates")
    return values


def _skill_names(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and SKILL_NAME.fullmatch(item) for item in value
    ):
        raise EvaluationContractError(f"{label} must be an array of Skill names")
    return _unique(value, label)


def normalize_case_input_path(value: str, case_id: str) -> str:
    relative = Path(value)
    windows_path = PureWindowsPath(value)
    if (
        not value
        or value == "."
        or "\0" in value
        or relative.is_absolute()
        or bool(windows_path.drive)
        or "\\" in value
        or ".." in relative.parts
    ):
        raise EvaluationContractError(
            f"evaluation case `{case_id}` has an unsafe case input path: `{value}`"
        )
    normalized = relative.as_posix()
    if normalized == ".":
        raise EvaluationContractError(
            f"evaluation case `{case_id}` has an unsafe case input path: `{value}`"
        )
    return normalized


def normalize_case_input_paths(values: Any, case_id: str) -> list[str]:
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise EvaluationContractError(
            f"evaluation case `{case_id}` files must be an array of strings"
        )
    normalized = [normalize_case_input_path(value, case_id) for value in values]
    if len(set(normalized)) != len(normalized):
        raise EvaluationContractError(f"evaluation case `{case_id}` repeats a file path")
    return normalized


def _regular_repository_file(root: Path, relative: Path) -> bool:
    target = root / relative
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return False
    try:
        target.resolve().relative_to(root.resolve())
        return target.is_file()
    except (OSError, RuntimeError, ValueError):
        return False


def validate_evaluation_references(definition: dict[str, Any], root: Path) -> None:
    """Check every static file and Skill reference in a normalized definition."""
    for skill in definition["execution"]["coexistence_skills"]:
        if not _regular_repository_file(root, Path("skills") / skill / "SKILL.md"):
            raise EvaluationContractError(
                f"evaluation execution coexistence Skill must have a regular SKILL.md: {skill}"
            )
    for case in definition["cases"]:
        for name in case["files"]:
            if not _regular_repository_file(root, Path(name)):
                raise EvaluationContractError(
                    f"evaluation case `{case['id']}` input file must be a regular repository file: {name}"
                )
        for skill in case["coexistence_skills"]:
            if not _regular_repository_file(root, Path("skills") / skill / "SKILL.md"):
                raise EvaluationContractError(
                    f"evaluation case `{case['id']}` coexistence Skill must have a regular SKILL.md: {skill}"
                )


def _reject_fixture_path_conflicts(paths: list[str], case_id: str) -> None:
    ordered = sorted(paths)
    for index, left in enumerate(ordered):
        left_parts = Path(left).parts
        for right in ordered[index + 1 :]:
            right_parts = Path(right).parts
            if right_parts[: len(left_parts)] == left_parts:
                raise EvaluationContractError(
                    f"evaluation case `{case_id}` fixture file paths conflict: "
                    f"`{left}` and `{right}`"
                )
            if left_parts[: len(right_parts)] == right_parts:
                raise EvaluationContractError(
                    f"evaluation case `{case_id}` fixture file paths conflict: "
                    f"`{right}` and `{left}`"
                )


def _reject_case_fixture_path_conflicts(
    case_paths: list[str], fixture_paths: list[str], case_id: str
) -> None:
    case_destinations = sorted(
        ((Path("inputs") / path).as_posix(), path) for path in case_paths
    )
    for case_destination, case_path in case_destinations:
        case_parts = Path(case_destination).parts
        for fixture_path in sorted(fixture_paths):
            fixture_parts = Path(fixture_path).parts
            if (
                fixture_parts[: len(case_parts)] == case_parts
                or case_parts[: len(fixture_parts)] == fixture_parts
            ):
                raise EvaluationContractError(
                    f"evaluation case `{case_id}` case file `{case_path}` and fixture file "
                    f"`{fixture_path}` conflict after materialization"
                )


def _format_turns(values: Any, label: str) -> str:
    if not isinstance(values, list) or not values:
        raise EvaluationContractError(f"{label} must be a non-empty array")
    rendered: list[str] = []
    for index, value in enumerate(values, start=1):
        if isinstance(value, str):
            content = _non_empty_string(value, f"{label} entry {index}")
            role = "user"
        elif isinstance(value, dict):
            _reject_unknown_fields(value, {"role", "content"}, f"{label} entry {index}")
            if set(value) != {"role", "content"}:
                raise EvaluationContractError(f"{label} entry {index} requires role and content")
            role = value["role"]
            if not isinstance(role, str) or role not in TURN_ROLES:
                raise EvaluationContractError(
                    f"{label} entry {index} role must be user or assistant"
                )
            content = _non_empty_string(value["content"], f"{label} entry {index} content")
        else:
            raise EvaluationContractError(
                f"{label} entries must be strings or role-content objects"
            )
        rendered.append(f"{role.capitalize()} turn {index}:\n{content}")
    return "\n\n".join(rendered)


def _normalize_assertions(
    case: dict[str, Any], case_id: str, definition_kind: str
) -> list[dict[str, Any]]:
    raw_assertions = case.get("assertions", [])
    if not isinstance(raw_assertions, list):
        raise EvaluationContractError(f"evaluation case `{case_id}` assertions must be an array")
    requirements: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, assertion in enumerate(raw_assertions, start=1):
        if isinstance(assertion, str):
            text = _non_empty_string(
                assertion, f"evaluation case `{case_id}` assertion {index}"
            )
            requirement = {"id": f"assertion-{index}", "text": text, "critical": True}
        elif isinstance(assertion, dict):
            label = f"evaluation case `{case_id}` assertion {index}"
            _reject_unknown_fields(assertion, {"id", "text", "critical"}, label)
            if set(assertion) != {"id", "text", "critical"}:
                raise EvaluationContractError(f"{label} requires id, text, and critical")
            requirement_id = _non_empty_string(assertion["id"], f"{label} id")
            text = _non_empty_string(assertion["text"], f"{label} text")
            critical = assertion["critical"]
            if not isinstance(critical, bool):
                raise EvaluationContractError(f"{label} critical must be boolean")
            requirement = {"id": requirement_id, "text": text, "critical": critical}
        else:
            raise EvaluationContractError(
                f"evaluation case `{case_id}` assertions must be strings or objects"
            )
        if requirement["id"] in seen:
            raise EvaluationContractError(
                f"evaluation case `{case_id}` assertion ids must be unique"
            )
        seen.add(requirement["id"])
        requirements.append(requirement)

    expected_output = None
    if "expected_output" in case:
        expected_output = _non_empty_string(
            case["expected_output"], f"evaluation case `{case_id}` expected_output"
        )
    if not requirements and expected_output is not None:
        requirements.append({"id": "expected-output", "text": expected_output, "critical": True})

    if definition_kind == "routing":
        if "expected_handlers" not in case:
            raise EvaluationContractError(
                f"routing case `{case_id}` requires expected_handlers as an array of Skill names"
            )
        expected_handlers = _skill_names(
            case["expected_handlers"], f"routing case `{case_id}` expected_handlers"
        )
        if "routing-handlers" in seen:
            raise EvaluationContractError(
                f"routing case `{case_id}` reserves the assertion id `routing-handlers`"
            )
        requirements.append(
            {
                "id": "routing-handlers",
                "text": "Directly observed Skill handlers match the expected handlers.",
                "critical": True,
                "expected_handlers": expected_handlers,
            }
        )
    elif "expected_handlers" in case:
        raise EvaluationContractError(
            f"behavior case `{case_id}` must not define expected_handlers"
        )

    if not requirements:
        raise EvaluationContractError(
            f"behavior case `{case_id}` requires assertions or expected_output"
        )
    return requirements


def _normalize_fixture(case: dict[str, Any], case_id: str) -> dict[str, str]:
    if "fixture" not in case:
        return {}
    fixture = case["fixture"]
    if isinstance(fixture, str):
        raise EvaluationContractError(
            f"evaluation case `{case_id}` names fixture `{fixture}` without inline files; "
            "materialize the fixture before using the common Runner"
        )
    if not isinstance(fixture, dict):
        raise EvaluationContractError(f"evaluation case `{case_id}` fixture must be an object")
    _reject_unknown_fields(fixture, {"files"}, f"evaluation case `{case_id}` fixture")
    if set(fixture) != {"files"}:
        raise EvaluationContractError(f"evaluation case `{case_id}` fixture requires files")
    raw_files = fixture["files"]
    if not isinstance(raw_files, dict) or not all(
        isinstance(name, str) and isinstance(content, str) for name, content in raw_files.items()
    ):
        raise EvaluationContractError(
            f"evaluation case `{case_id}` fixture.files must map paths to strings"
        )
    normalized: dict[str, str] = {}
    for name, content in raw_files.items():
        path = normalize_case_input_path(name, case_id)
        if Path(path).parts[0] in {".agents", ".git"}:
            raise EvaluationContractError(
                f"evaluation case `{case_id}` has an unsafe fixture path: {name}"
            )
        if path in normalized:
            raise EvaluationContractError(
                f"evaluation case `{case_id}` repeats a fixture file path"
            )
        normalized[path] = content
    _reject_fixture_path_conflicts(list(normalized), case_id)
    return normalized


def _normalize_baseline_files(case: dict[str, Any], case_id: str, current_paths: set[str]) -> dict[str, str]:
    if "baseline_files" not in case:
        return {}
    files = case["baseline_files"]
    if not isinstance(files, dict) or not files or not all(
        isinstance(name, str) and isinstance(content, str) for name, content in files.items()
    ):
        raise EvaluationContractError(f"evaluation case `{case_id}` baseline_files must map paths to strings")
    normalized: dict[str, str] = {}
    for name, content in files.items():
        path = normalize_case_input_path(name, case_id)
        if path not in current_paths:
            raise EvaluationContractError(
                f"evaluation case `{case_id}` baseline file has no current counterpart: {path}"
            )
        normalized[path] = content
    _reject_fixture_path_conflicts(list(normalized), case_id)
    return normalized


def _normalize_case(case: Any, definition_kind: str) -> dict[str, Any]:
    if not isinstance(case, dict):
        raise EvaluationContractError("every evaluation case must be an object")
    _reject_unknown_fields(case, CASE_FIELDS, "evaluation case")
    case_id = case.get("id")
    if isinstance(case_id, bool) or not isinstance(case_id, (str, int)):
        raise EvaluationContractError("every evaluation case requires a string or integer id")
    normalized_id = str(case_id).strip()
    if not normalized_id:
        raise EvaluationContractError("every evaluation case requires a non-empty id")

    present_inputs = frozenset(set(case) & INPUT_FIELDS)
    if present_inputs not in VALID_INPUT_SHAPES:
        raise EvaluationContractError(
            f"evaluation case `{normalized_id}` must use exactly one supported input form: "
            "prompt; turns; authoring_turns with request; or conversation with prompt"
        )
    if present_inputs == {"prompt"}:
        prompt = _non_empty_string(case["prompt"], f"evaluation case `{normalized_id}` prompt")
        input_mode = "single-turn"
    elif present_inputs == {"turns"}:
        prompt = _format_turns(case["turns"], f"evaluation case `{normalized_id}` turns")
        input_mode = "transcript"
    elif present_inputs == {"request", "authoring_turns"}:
        request = _non_empty_string(
            case["request"], f"evaluation case `{normalized_id}` request"
        )
        authoring = _format_turns(
            case["authoring_turns"], f"evaluation case `{normalized_id}` authoring_turns"
        )
        prompt = f"Prior authoring conversation:\n\n{authoring}\n\nCurrent request:\n{request}"
        input_mode = "authoring-transcript"
    else:
        current = _non_empty_string(
            case["prompt"], f"evaluation case `{normalized_id}` prompt"
        )
        history = _format_turns(
            case["conversation"], f"evaluation case `{normalized_id}` conversation"
        )
        prompt = f"Conversation so far:\n\n{history}\n\nCurrent user request:\n{current}"
        input_mode = "conversation"

    files = normalize_case_input_paths(case.get("files", []), normalized_id)
    inline_files = _normalize_fixture(case, normalized_id)
    _reject_case_fixture_path_conflicts(files, list(inline_files), normalized_id)
    baseline_files = _normalize_baseline_files(case, normalized_id, set(inline_files))

    normalized: dict[str, Any] = {
        "id": normalized_id,
        "prompt": prompt,
        "input_mode": input_mode,
        "grading_requirements": _normalize_assertions(case, normalized_id, definition_kind),
        "files": files,
        "inline_files": inline_files,
        "baseline_files": baseline_files,
        "coexistence_skills": _skill_names(
            case.get("coexistence_skills", []),
            f"evaluation case `{normalized_id}` coexistence_skills",
        ),
    }
    if "title" in case:
        normalized["title"] = _non_empty_string(
            case["title"], f"evaluation case `{normalized_id}` title"
        )
    if "conditions" in case:
        conditions = case["conditions"]
        if not isinstance(conditions, list) or not all(
            isinstance(value, str) and value in CONDITIONS for value in conditions
        ):
            raise EvaluationContractError(
                f"evaluation case `{normalized_id}` has unsupported conditions"
            )
        if "candidate" not in conditions:
            raise EvaluationContractError(
                f"evaluation case `{normalized_id}` conditions must include candidate"
            )
        normalized["allowed_conditions"] = sorted(
            _unique(conditions, f"evaluation case `{normalized_id}` conditions")
        )
    return normalized


def normalize_evaluation_document(
    document: Any, *, expected_skill: str, definition_kind: str
) -> dict[str, Any]:
    """Return the normalized executable definition or raise a contract error."""

    if definition_kind not in {"behavior", "routing"}:
        raise ValueError(f"unsupported definition kind: {definition_kind}")
    if not isinstance(document, dict):
        raise EvaluationContractError("evaluation JSON top level must be an object")
    _reject_unknown_fields(document, TOP_LEVEL_FIELDS, "evaluation definition")
    skill_name = document.get("skill_name")
    if (
        skill_name != expected_skill
        or not isinstance(skill_name, str)
        or SKILL_NAME.fullmatch(skill_name) is None
    ):
        raise EvaluationContractError(
            f"evaluation JSON skill_name must be `{expected_skill}`"
        )
    execution = document.get("execution", {})
    if not isinstance(execution, dict):
        raise EvaluationContractError("evaluation execution settings must be an object")
    _reject_unknown_fields(execution, EXECUTION_FIELDS, "evaluation execution settings")
    coexistence_skills = _skill_names(
        execution.get("coexistence_skills", []),
        "evaluation execution coexistence_skills",
    )
    raw_cases = document.get("evals")
    if not isinstance(raw_cases, list):
        raise EvaluationContractError("evaluation cases must be an array")
    cases = [_normalize_case(case, definition_kind) for case in raw_cases]
    ids = [case["id"] for case in cases]
    if len(set(ids)) != len(ids):
        duplicate = next(case_id for case_id in ids if ids.count(case_id) > 1)
        raise EvaluationContractError(f"duplicate case id `{duplicate}`")
    return {
        "skill_name": skill_name,
        "execution": {"coexistence_skills": coexistence_skills},
        "cases": cases,
    }
