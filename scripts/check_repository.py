#!/usr/bin/env python3
"""Deterministic, read-only consistency checks for this repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

try:
    from evaluation_contract import EvaluationContractError, TRACKED_REPOSITORY_LOCAL_SKILLS, normalize_evaluation_document, validate_evaluation_references
except ModuleNotFoundError:  # Imported as scripts.check_repository in unit tests.
    from scripts.evaluation_contract import EvaluationContractError, TRACKED_REPOSITORY_LOCAL_SKILLS, normalize_evaluation_document, validate_evaluation_references


KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
FILE_MODES = {"100644", "100755"}
REPORT_STATUSES = {"pass", "fail", "inconclusive", "error"}
REPORT_CONDITIONS = {"candidate", "baseline", "without-skill"}
REPORT_DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
GIT_COMMIT = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
REPORT_PATHS = {
    "static-only",
    "targeted-candidate",
    "targeted-routing",
    "baseline-comparison",
    "target-environment",
}
RAW_REPORT_FIELDS = {
    "artifact_directory",
    "authentication",
    "credentials",
    "events",
    "jsonl",
    "prompt",
    "plan",
    "plan_snapshot",
    "raw_output",
    "raw_response",
    "response",
    "session_log",
    "stderr",
    "stdout",
}
REPORT_ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9:])(?:/[A-Za-z0-9._-][^\s\"'`<>]*|[A-Za-z]:\\[^\s\"'`<>]+)")
CATALOG_ROW = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|", re.MULTILINE)
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
COMPANION_ROW = re.compile(r"^\|\s*`([^`]+)`\s*→\s*`([^`]+)`\s*\|(.+)$", re.MULTILINE)
PERSONAL_PATHS = (
    re.compile(r"(?<![A-Za-z0-9_])/(?:home|Users)/[^/\s\"'`<>]+"),
    re.compile(r"(?<![A-Za-z0-9_])/mnt/[A-Za-z]/Users/[^/\s\"'`<>]+"),
    re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:\\Users\\[^\\\s\"'`<>]+"),
)
TEXT_SUFFIXES = {".json", ".md", ".py", ".sh", ".txt", ".yaml", ".yml"}
PERSONAL_PATH_EXCLUSIONS = {
    "scripts/check_repository.py",
    "tests/test_check_repository.py",
}
@dataclass(frozen=True, order=True)
class Problem:
    path: str
    line: int
    reason: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.reason}"


def relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def add(problems: list[Problem], root: Path, path: Path, line: int, reason: str) -> None:
    problems.append(Problem(relative_path(root, path), line, reason))


def parse_frontmatter(path: Path) -> tuple[dict[str, tuple[str, int]], list[tuple[int, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, []
    closing = next((index for index, value in enumerate(lines[1:], start=1) if value == "---"), None)
    if closing is None:
        return {}, []
    fields: dict[str, tuple[str, int]] = {}
    duplicates: list[tuple[int, str]] = []
    for index, value in enumerate(lines[1:closing], start=2):
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", value)
        if not match:
            continue
        key, field_value = match.groups()
        if key in fields:
            duplicates.append((index, key))
        else:
            fields[key] = (field_value.strip(), index)
    return fields, duplicates


def parse_double_quoted_yaml_scalar(value: str) -> tuple[str | None, int]:
    escapes = {
        "0": "\0",
        "a": "\a",
        "b": "\b",
        "t": "\t",
        "n": "\n",
        "v": "\v",
        "f": "\f",
        "r": "\r",
        "e": "\x1b",
        " ": " ",
        '"': '"',
        "/": "/",
        "\\": "\\",
        "N": "\x85",
        "_": "\xa0",
        "L": "\u2028",
        "P": "\u2029",
    }
    parsed: list[str] = []
    index = 1
    while index < len(value):
        character = value[index]
        if character == '"':
            return "".join(parsed), index + 1
        if character != "\\":
            parsed.append(character)
            index += 1
            continue
        index += 1
        if index >= len(value):
            return None, index
        escape = value[index]
        if escape in escapes:
            parsed.append(escapes[escape])
            index += 1
            continue
        digits = {"x": 2, "u": 4, "U": 8}.get(escape)
        if digits is None:
            return None, index
        encoded = value[index + 1 : index + 1 + digits]
        if len(encoded) != digits or re.fullmatch(r"[0-9A-Fa-f]+", encoded) is None:
            return None, index
        try:
            parsed.append(chr(int(encoded, 16)))
        except ValueError:
            return None, index
        index += digits + 1
    return None, index


def parse_frontmatter_scalar(raw: str) -> tuple[str | None, str | None]:
    value = raw.strip()
    guidance = "must use a supported single-line string scalar (plain, single-quoted, or double-quoted)"
    if not value:
        return "", None
    if value[0] == '"':
        parsed, end = parse_double_quoted_yaml_scalar(value)
        remainder = value[end:].strip()
        if parsed is None or (remainder and not remainder.startswith("#")):
            return None, guidance
        return parsed, None
    if value[0] == "'":
        parsed: list[str] = []
        index = 1
        while index < len(value):
            if value[index] != "'":
                parsed.append(value[index])
                index += 1
                continue
            if index + 1 < len(value) and value[index + 1] == "'":
                parsed.append("'")
                index += 2
                continue
            remainder = value[index + 1 :].strip()
            if remainder and not remainder.startswith("#"):
                return None, guidance
            return "".join(parsed), None
        return None, guidance
    if value[0] in "[{|>&*!":
        return None, guidance
    return re.split(r"\s+#", value, maxsplit=1)[0].rstrip(), None


def skill_directories(root: Path) -> list[Path]:
    skills = root / "skills"
    if not skills.is_dir():
        return []
    return sorted(path for path in skills.iterdir() if path.is_dir() and not path.name.startswith("."))


def parse_catalog(path: Path) -> tuple[list[tuple[str, int]], int | None]:
    text = path.read_text(encoding="utf-8")
    entries = [(match.group(1), line_number(text, match.start())) for match in CATALOG_ROW.finditer(text)]
    count_match = re.search(r"\b(\d+)\s+(?:の\s+)?Skills?\b", text, re.IGNORECASE)
    return entries, int(count_match.group(1)) if count_match else None


def check_catalogs(root: Path, problems: list[Problem]) -> set[str]:
    directories = skill_directories(root)
    names = {path.name for path in directories}
    if not directories:
        add(problems, root, root / "skills", 1, "no Skill directories found")

    for name in ("README.md", "README.ja.md"):
        path = root / name
        if not path.is_file():
            add(problems, root, path, 1, "required catalog is missing")
            continue
        entries, declared_count = parse_catalog(path)
        seen: set[str] = set()
        for entry, line in entries:
            if entry in seen:
                add(problems, root, path, line, f"duplicate catalog entry `{entry}`")
            seen.add(entry)
        entry_names = {entry for entry, _ in entries}
        for missing in sorted(names - entry_names):
            add(problems, root, path, 1, f"catalog is missing Skill `{missing}`")
        for unexpected in sorted(entry_names - names):
            line = next(line for entry, line in entries if entry == unexpected)
            add(problems, root, path, line, f"catalog references unknown Skill `{unexpected}`")
        if declared_count is None:
            add(problems, root, path, 1, "catalog does not declare its Skill count")
        elif declared_count != len(names):
            add(
                problems,
                root,
                path,
                1,
                f"declared Skill count {declared_count} does not match {len(names)} directories",
            )

    return names


def check_skill_packages(root: Path, problems: list[Problem]) -> None:
    for directory in skill_directories(root):
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            add(problems, root, skill_file, 1, "canonical Skill file is missing")
            continue
        fields, duplicates = parse_frontmatter(skill_file)
        if not fields:
            add(problems, root, skill_file, 1, "frontmatter must start at the first line and have a closing delimiter")
            continue
        for line, key in duplicates:
            add(problems, root, skill_file, line, f"duplicate frontmatter key `{key}`")
        normalized: dict[str, tuple[str, int]] = {}
        for key in ("name", "description", "license"):
            if key not in fields:
                add(problems, root, skill_file, 1, f"required frontmatter `{key}` is missing or empty")
                continue
            value, error = parse_frontmatter_scalar(fields[key][0])
            if error:
                add(problems, root, skill_file, fields[key][1], f"frontmatter `{key}` {error}")
            elif not value:
                add(problems, root, skill_file, fields[key][1], f"required frontmatter `{key}` is missing or empty")
            else:
                normalized[key] = (value, fields[key][1])
        name = normalized.get("name", ("", 1))[0]
        if not KEBAB_CASE.fullmatch(directory.name):
            add(problems, root, skill_file, 1, f"Skill directory `{directory.name}` is not kebab-case")
        if name and not KEBAB_CASE.fullmatch(name):
            add(problems, root, skill_file, normalized["name"][1], f"frontmatter name `{name}` is not kebab-case")
        if name and name != directory.name:
            add(
                problems,
                root,
                skill_file,
                normalized["name"][1],
                f"frontmatter name `{name}` does not match directory `{directory.name}`",
            )
        if name and len(name) > 64:
            add(problems, root, skill_file, normalized["name"][1], "frontmatter `name` exceeds 64 characters")
        description = normalized.get("description", ("", 1))[0]
        if description and len(description) > 1024:
            add(
                problems,
                root,
                skill_file,
                normalized["description"][1],
                "frontmatter `description` exceeds 1024 characters",
            )
        eval_readme = directory / "evals" / "README.md"
        if not eval_readme.is_file():
            add(problems, root, eval_readme, 1, "every Skill requires evals/README.md")


def markdown_without_code(text: str) -> str:
    visible = list(text)

    def mask(start: int, end: int) -> None:
        for index in range(start, end):
            if visible[index] not in "\r\n":
                visible[index] = " "

    fence_marker: str | None = None
    fence_length = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        if fence_marker is None:
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if opening and not (opening.group(1).startswith("`") and "`" in line[opening.end() :]):
                fence_marker = opening.group(1)[0]
                fence_length = len(opening.group(1))
                mask(offset, offset + len(line))
        else:
            closing = re.match(r"^ {0,3}(`+|~+)[ \t]*(?:\r?\n)?$", line)
            mask(offset, offset + len(line))
            if (
                closing
                and closing.group(1)[0] == fence_marker
                and len(closing.group(1)) >= fence_length
            ):
                fence_marker = None
                fence_length = 0
        offset += len(line)

    masked_fences = "".join(visible)
    index = 0
    while index < len(masked_fences):
        if masked_fences[index] != "`":
            index += 1
            continue
        opening_end = index + 1
        while opening_end < len(masked_fences) and masked_fences[opening_end] == "`":
            opening_end += 1
        delimiter_length = opening_end - index
        search = opening_end
        closing_end: int | None = None
        while search < len(masked_fences):
            if masked_fences[search] != "`":
                search += 1
                continue
            run_end = search + 1
            while run_end < len(masked_fences) and masked_fences[run_end] == "`":
                run_end += 1
            if run_end - search == delimiter_length:
                closing_end = run_end
                break
            search = run_end
        if closing_end is None:
            index = opening_end
            continue
        mask(index, closing_end)
        index = closing_end

    return "".join(visible)


def link_destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    return value.split(maxsplit=1)[0]


def is_external_link(destination: str) -> bool:
    return (
        not destination
        or destination.startswith(("#", "/", "//"))
        or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination) is not None
    )


def contained(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
        return True
    except ValueError:
        return False


def check_markdown_links(root: Path, problems: list[Problem]) -> None:
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        visible = markdown_without_code(text)
        matches = list(INLINE_LINK.finditer(visible)) + list(REFERENCE_LINK.finditer(visible))
        for match in sorted(matches, key=lambda item: item.start()):
            destination = link_destination(match.group(1))
            if is_external_link(destination):
                continue
            clean = unquote(destination.split("#", 1)[0].split("?", 1)[0])
            target = (path.parent / clean).resolve()
            line = line_number(visible, match.start())
            if not contained(root.resolve(), target):
                add(problems, root, path, line, f"relative Markdown link escapes repository: `{destination}`")
            elif not target.exists():
                add(problems, root, path, line, f"relative Markdown link target does not exist: `{destination}`")


def check_localization_notices(root: Path, problems: list[Problem]) -> None:
    paths = list((root / "skills").glob("*/SKILL-ja.md"))
    paths.extend(
        path
        for name in TRACKED_REPOSITORY_LOCAL_SKILLS
        if (path := root / ".agents" / "skills" / name / "SKILL-ja.md").is_file()
    )
    for path in sorted(paths):
        lines = path.read_text(encoding="utf-8").splitlines()
        start = 0
        if lines and lines[0] == "---":
            closing = next((index for index, value in enumerate(lines[1:], start=1) if value == "---"), None)
            if closing is None:
                add(problems, root, path, 1, "translation frontmatter has no closing delimiter")
                continue
            start = closing + 1
        notice_lines = [value.strip() for value in lines[start:] if value.strip()][:4]
        notice = " ".join(notice_lines)
        has_canonical = "SKILL.md" in notice and ("canonical source" in notice.lower() or "正本" in notice)
        has_reference = "reference" in notice.lower() or "参考" in notice
        if not (has_canonical and has_reference):
            add(
                problems,
                root,
                path,
                start + 1,
                "Japanese translation must begin with a notice that SKILL.md is canonical and this file is reference-only",
            )


def check_json_assets(root: Path, problems: list[Problem], ignored_report_skill: str | None = None) -> None:
    migration_states: dict[Path, dict[str, bool]] = {}
    public_assets = (root / "skills").glob("*/evals/*.json")
    local_assets = (
        path
        for skill in TRACKED_REPOSITORY_LOCAL_SKILLS
        for path in (root / ".agents" / "skills" / skill / "evals").glob("*.json")
    )
    for path in sorted([*public_assets, *local_assets]):
        if path.name == "report.json" and path.parent.parent.name == ignored_report_skill:
            continue
        text = path.read_text(encoding="utf-8")
        try:
            document = json.loads(text)
        except json.JSONDecodeError as error:
            add(problems, root, path, error.lineno, f"invalid JSON: {error.msg}")
            continue
        if not isinstance(document, dict):
            add(problems, root, path, 1, "evaluation JSON top level must be an object")
            continue
        if path.name == "report.json":
            check_evaluation_report(root, path, document, problems)
            continue
        if path.name in {"evals.json", "triggers.json"}:
            migrated = "skill_name" in document or "evals" in document
            migration_states.setdefault(path.parent.parent, {})[path.name] = migrated
        official = path.name == "evals.json" and ("skill_name" in document or "evals" in document)
        if path.name == "triggers.json" and ("skill_name" in document or "evals" in document):
            official = True
        expected_skill = path.parent.parent.name
        if official:
            try:
                normalized = normalize_evaluation_document(
                    document,
                    expected_skill=expected_skill,
                    definition_kind="routing" if path.name == "triggers.json" else "behavior",
                )
                validate_evaluation_references(normalized, root)
            except EvaluationContractError as error:
                add(problems, root, path, 1, str(error))
            continue
        version = document.get("schema_version", document.get("version"))
        if isinstance(version, bool) or not isinstance(version, int) or version < 1:
            add(problems, root, path, 1, "evaluation JSON requires a positive integer schema_version or version")
        if document.get("skill") != expected_skill:
            add(problems, root, path, 1, f"evaluation JSON skill must be `{expected_skill}`")
        cases = document.get("cases")
        if cases is not None:
            if not isinstance(cases, list):
                add(problems, root, path, 1, "cases must be an array")
            else:
                seen: set[str] = set()
                for case in cases:
                    case_id = case.get("id") if isinstance(case, dict) else None
                    if isinstance(case_id, bool) or not isinstance(case_id, (str, int)) or not str(case_id).strip():
                        add(problems, root, path, 1, "every case requires a non-empty string or integer id")
                    elif str(case_id) in seen:
                        add(problems, root, path, 1, f"duplicate case id `{case_id}`")
                    else:
                        seen.add(str(case_id))
    for skill_root, states in sorted(migration_states.items()):
        if len(states) > 1 and len(set(states.values())) > 1:
            path = skill_root / "evals" / sorted(states)[0]
            add(problems, root, path, 1, "must migrate evals.json and triggers.json together")


def report_case_assertions(path: Path) -> dict[str, dict[str, bool] | None]:
    if not path.is_file():
        return {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(document, dict):
        return {}
    migrated = "evals" in document and "skill_name" in document
    if migrated:
        try:
            normalized = normalize_evaluation_document(
                document,
                expected_skill=path.parent.parent.name,
                definition_kind="routing" if path.name == "triggers.json" else "behavior",
            )
        except EvaluationContractError:
            return {}
        return {
            case["id"]: {
                requirement["id"]: requirement["critical"]
                for requirement in case["grading_requirements"]
            }
            for case in normalized["cases"]
        }
    raw_cases = document.get("cases")
    if not isinstance(raw_cases, list):
        return {}
    cases: dict[str, dict[str, bool] | None] = {}
    for case in raw_cases:
        if not isinstance(case, dict):
            continue
        case_id = case.get("id")
        if isinstance(case_id, bool) or not isinstance(case_id, (str, int)):
            continue
        assertions = case.get("assertions", case.get("assertion_ids"))
        cases[str(case_id)] = (
            {value: True for value in assertions}
            if isinstance(assertions, list) and all(isinstance(value, str) for value in assertions)
            else None
        )
    return cases


def find_forbidden_report_field(value: object) -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in RAW_REPORT_FIELDS:
                return key
            found = find_forbidden_report_field(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_forbidden_report_field(child)
            if found is not None:
                return found
    return None


def find_report_absolute_path(value: object) -> str | None:
    if isinstance(value, dict):
        for child in value.values():
            found = find_report_absolute_path(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_report_absolute_path(child)
            if found is not None:
                return found
    elif isinstance(value, str):
        match = REPORT_ABSOLUTE_PATH.search(value)
        if match is not None:
            return match.group(0)
    return None


def expected_report_status(statuses: list[str], repository_status: str) -> str:
    if "error" in statuses:
        return "error"
    if repository_status == "fail" or "fail" in statuses:
        return "fail"
    if repository_status == "unavailable" or "inconclusive" in statuses:
        return "inconclusive"
    return "pass"


def derive_report_result_status(requirements: list[dict[str, object]]) -> str:
    if any(value.get("status") == "error" for value in requirements):
        return "error"
    if any(value.get("critical") is True and value.get("status") == "fail" for value in requirements):
        return "fail"
    if any(value.get("status") in {"fail", "inconclusive"} for value in requirements):
        return "inconclusive"
    return "pass"


def check_evaluation_report(
    root: Path,
    path: Path,
    document: dict[str, object],
    problems: list[Problem],
) -> None:
    expected_skill = path.parent.parent.name
    expected_source = "repository-local" if path.parent.parent.parent.parent == root / ".agents" else "public"
    if document.get("skill_source", "public") != expected_source:
        add(problems, root, path, 1, f"evaluation report skill_source must be `{expected_source}`")
    if document.get("schema_version") != 2:
        add(problems, root, path, 1, "report schema_version must be 2")
    if document.get("skill") != expected_skill:
        add(problems, root, path, 1, f"evaluation report skill must be `{expected_skill}`")
    if not isinstance(document.get("evaluated_on"), str) or REPORT_DATE.fullmatch(document["evaluated_on"]) is None:
        add(problems, root, path, 1, "report evaluated_on must use YYYY-MM-DD")
    for field in ("purpose", "stopping_reason"):
        if not isinstance(document.get(field), str) or not str(document[field]).strip():
            add(problems, root, path, 1, f"report requires a non-empty `{field}`")
    affected = document.get("affected_responsibilities")
    if (
        not isinstance(affected, list)
        or not affected
        or not all(isinstance(value, str) and value.strip() for value in affected)
    ):
        add(problems, root, path, 1, "report affected_responsibilities must be a non-empty string array")
    unverified = document.get("unverified")
    if not isinstance(unverified, list) or not all(isinstance(value, str) and value.strip() for value in unverified):
        add(problems, root, path, 1, "report unverified must be a string array")

    forbidden = find_forbidden_report_field(document)
    if forbidden is not None:
        add(problems, root, path, 1, f"report must not contain raw artifact field `{forbidden}`")
    absolute_path = find_report_absolute_path(document)
    if absolute_path is not None:
        add(problems, root, path, 1, f"report must not contain absolute path `{absolute_path}`")

    base = document.get("base")
    commit = base.get("commit") if isinstance(base, dict) else None
    if not isinstance(commit, str) or GIT_COMMIT.fullmatch(commit) is None:
        add(problems, root, path, 1, "report base.commit must be a full Git object id")
    candidate = document.get("candidate")
    if not isinstance(candidate, dict) or not isinstance(candidate.get("files"), dict):
        add(problems, root, path, 1, "report candidate.files must be an object")
    evaluation_inputs = document.get("evaluation_inputs")
    if not isinstance(evaluation_inputs, dict) or not all(
        isinstance(evaluation_inputs.get(field), dict) for field in ("evaluation_files", "case_files")
    ):
        add(problems, root, path, 1, "report evaluation_inputs manifests must be objects")
    environment = document.get("environment")
    environment_fields = ("client", "model", "reasoning_effort", "sandbox")
    if not isinstance(environment, dict) or not all(
        isinstance(environment.get(field), str) and environment[field].strip()
        for field in environment_fields
    ):
        add(problems, root, path, 1, "report environment fields must be non-empty strings")

    selection = document.get("selection")
    evaluation_path = selection.get("path") if isinstance(selection, dict) else None
    raw_selected = selection.get("cases") if isinstance(selection, dict) else None
    if evaluation_path not in REPORT_PATHS:
        add(problems, root, path, 1, "report selection.path is invalid")
    selected_pairs: set[tuple[str, str]] = set()
    selected_ids: set[str] = set()
    known_assertions: dict[str, dict[str, bool] | None] = {}
    if not isinstance(raw_selected, list):
        add(problems, root, path, 1, "report selection.cases must be an array")
    else:
        for selected in raw_selected:
            case_id = selected.get("id") if isinstance(selected, dict) else None
            conditions = selected.get("conditions") if isinstance(selected, dict) else None
            if not isinstance(case_id, str) or not case_id or case_id in selected_ids:
                add(problems, root, path, 1, "report selected case ids must be unique non-empty strings")
                continue
            selected_ids.add(case_id)
            if not isinstance(conditions, list) or not conditions:
                add(problems, root, path, 1, f"report selected case `{case_id}` requires conditions")
                continue
            for condition in conditions:
                pair = (case_id, condition)
                if condition not in REPORT_CONDITIONS or pair in selected_pairs:
                    add(
                        problems,
                        root,
                        path,
                        1,
                        f"report selected case `{case_id}` has invalid or duplicate conditions",
                    )
                else:
                    selected_pairs.add(pair)
    if evaluation_path == "static-only" and selected_pairs:
        add(problems, root, path, 1, "static-only report must not select model-backed cases")
    if evaluation_path not in {"static-only", "baseline-comparison"} and any(
        condition != "candidate" for _, condition in selected_pairs
    ):
        add(problems, root, path, 1, "comparison conditions require the baseline-comparison path")
    if evaluation_path == "baseline-comparison" and selected_pairs:
        conditions = {condition for _, condition in selected_pairs}
        if "candidate" not in conditions or not ({"baseline", "without-skill"} & conditions):
            add(problems, root, path, 1, "baseline-comparison requires candidate and a comparison condition")
    if evaluation_path in REPORT_PATHS - {"static-only"}:
        asset_name = "triggers.json" if evaluation_path == "targeted-routing" else "evals.json"
        known_assertions = report_case_assertions(path.parent / asset_name)
        for case_id in sorted(selected_ids - set(known_assertions)):
            add(problems, root, path, 1, f"report references unknown case id `{case_id}`")

    results = document.get("results")
    result_pairs: set[tuple[str, str]] = set()
    statuses: list[str] = []
    if not isinstance(results, list):
        add(problems, root, path, 1, "report results must be an array")
    else:
        for result in results:
            case_id = result.get("case_id") if isinstance(result, dict) else None
            condition = result.get("condition") if isinstance(result, dict) else None
            status = result.get("status") if isinstance(result, dict) else None
            pair = (case_id, condition)
            if not isinstance(case_id, str) or condition not in REPORT_CONDITIONS or pair in result_pairs:
                add(problems, root, path, 1, "report result pairs must be unique valid case-condition values")
            else:
                result_pairs.add(pair)
            if status not in REPORT_STATUSES:
                add(problems, root, path, 1, f"report result `{case_id}` has an invalid status")
            else:
                statuses.append(status)
            if (
                not isinstance(result, dict)
                or not isinstance(result.get("evidence"), str)
                or not result["evidence"].strip()
            ):
                add(problems, root, path, 1, f"report result `{case_id}` requires concise evidence")
            requirements = result.get("requirements") if isinstance(result, dict) else None
            if not isinstance(requirements, list):
                add(problems, root, path, 1, f"report result `{case_id}` requirements must be an array")
            else:
                requirement_ids: set[str] = set()
                normalized_requirements: list[dict[str, object]] = []
                for requirement in requirements:
                    requirement_id = requirement.get("id") if isinstance(requirement, dict) else None
                    requirement_status = requirement.get("status") if isinstance(requirement, dict) else None
                    requirement_evidence = requirement.get("evidence") if isinstance(requirement, dict) else None
                    requirement_critical = requirement.get("critical") if isinstance(requirement, dict) else None
                    if (
                        not isinstance(requirement_id, str)
                        or not requirement_id
                        or requirement_id in requirement_ids
                    ):
                        add(problems, root, path, 1, f"report result `{case_id}` has invalid requirement ids")
                    else:
                        requirement_ids.add(requirement_id)
                    if requirement_status not in REPORT_STATUSES:
                        add(problems, root, path, 1, f"report requirement `{requirement_id}` has an invalid status")
                    if not isinstance(requirement_evidence, str) or not requirement_evidence.strip():
                        add(problems, root, path, 1, f"report requirement `{requirement_id}` requires evidence")
                    if not isinstance(requirement_critical, bool):
                        add(problems, root, path, 1, f"report requirement `{requirement_id}` requires critical")
                    if isinstance(requirement_id, str) and requirement_status in REPORT_STATUSES and isinstance(
                        requirement_critical, bool
                    ):
                        normalized_requirements.append(
                            {"id": requirement_id, "status": requirement_status, "critical": requirement_critical}
                        )
                expected_assertions = known_assertions.get(case_id)
                if status != "error" and expected_assertions is not None and requirement_ids != set(expected_assertions):
                    add(problems, root, path, 1, f"report result `{case_id}` must grade every assigned assertion")
                if status != "error" and expected_assertions is not None:
                    for requirement in normalized_requirements:
                        expected_critical = expected_assertions.get(str(requirement["id"]))
                        if expected_critical is not None and requirement["critical"] != expected_critical:
                            add(
                                problems,
                                root,
                                path,
                                1,
                                f"report requirement `{requirement['id']}` critical does not match the evaluation asset",
                            )
                derived_status = derive_report_result_status(normalized_requirements)
                if status != "error" and status != derived_status:
                    add(
                        problems,
                        root,
                        path,
                        1,
                        f"report result `{case_id}` must derive status `{derived_status}` from requirement results",
                    )
    if result_pairs != selected_pairs:
        add(problems, root, path, 1, "report results must exactly match selected case-condition pairs")

    checks = document.get("checks")
    repository_status = checks.get("repository") if isinstance(checks, dict) else None
    if repository_status not in {"pass", "fail", "unavailable"}:
        add(problems, root, path, 1, "report checks.repository has an invalid status")
        repository_status = "unavailable"
    summary = document.get("summary")
    summary_status = summary.get("status") if isinstance(summary, dict) else None
    expected_status = expected_report_status(statuses, repository_status)
    if summary_status != expected_status:
        add(problems, root, path, 1, f"report summary.status must be `{expected_status}`")
    counts = summary.get("counts") if isinstance(summary, dict) else None
    expected_counts = {status: statuses.count(status) for status in sorted(REPORT_STATUSES)}
    if counts != expected_counts:
        add(problems, root, path, 1, "report summary.counts do not match results")
    check_candidate_manifest(root, path, document, problems)
    check_evaluation_input_hashes(root, path, document, problems)


def check_candidate_manifest(root: Path, path: Path, document: dict[str, object], problems: list[Problem]) -> None:
    candidate = document.get("candidate")
    files = candidate.get("files") if isinstance(candidate, dict) else None
    if files is None:
        return
    if not isinstance(files, dict):
        add(problems, root, path, 1, "candidate.files must be an object")
        return
    skill_root = path.parent.parent.resolve()
    skills_root = skill_root.parent.resolve()
    results_text = path.read_text(encoding="utf-8")
    current_files: set[str] = set()
    for target in skill_root.rglob("*"):
        relative = target.relative_to(skill_root)
        if relative.parts and relative.parts[0] == "evals":
            continue
        if target.is_symlink():
            add(
                problems,
                root,
                path,
                1,
                f"candidate Skill tree must not contain symlink `{relative.as_posix()}`",
            )
        elif target.is_file():
            current_files.add(relative.as_posix())
    if set(files) != current_files:
        add(problems, root, path, 1, "candidate manifest does not match the current Skill tree")
    for file_name, entry in sorted(files.items()):
        encoded_name = json.dumps(file_name)
        file_line = next(
            (index for index, value in enumerate(results_text.splitlines(), start=1) if encoded_name in value),
            1,
        )
        if not isinstance(file_name, str) or not isinstance(entry, dict) or set(entry) != {"sha256", "mode"}:
            add(problems, root, path, file_line, "candidate.files entries require sha256 and mode")
            continue
        expected = entry.get("sha256")
        expected_mode = entry.get("mode")
        if not isinstance(expected, str):
            add(problems, root, path, file_line, f"candidate hash for `{file_name}` must be a string")
            continue
        if not SHA256.fullmatch(expected):
            add(
                problems,
                root,
                path,
                file_line,
                f"candidate hash for `{file_name}` must use lowercase sha256:<64 hex>",
            )
            continue
        if expected_mode not in FILE_MODES:
            add(problems, root, path, file_line, f"candidate mode for `{file_name}` must be `100644` or `100755`")
            continue
        unresolved = skill_root / file_name
        target = unresolved.resolve()
        if not contained(skills_root, target):
            add(problems, root, path, file_line, f"candidate file escapes repository skills tree: `{file_name}`")
        elif unresolved.is_symlink():
            add(problems, root, path, file_line, f"candidate file must not be a symlink: `{file_name}`")
        elif not target.is_file():
            add(problems, root, path, file_line, f"candidate file does not exist: `{file_name}`")
        else:
            actual = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                add(
                    problems,
                    root,
                    path,
                    file_line,
                    f"candidate hash for `{file_name}` is stale: expected `{actual}`, found `{expected}`",
                )
            actual_mode = "100755" if target.stat().st_mode & 0o111 else "100644"
            if actual_mode != expected_mode:
                add(
                    problems,
                    root,
                    path,
                    file_line,
                    f"candidate mode for `{file_name}` is stale: expected `{actual_mode}`, found `{expected_mode}`",
                )


def check_evaluation_input_hashes(
    root: Path,
    path: Path,
    document: dict[str, object],
    problems: list[Problem],
) -> None:
    inputs = document.get("evaluation_inputs")
    if not isinstance(inputs, dict):
        return
    for field in ("evaluation_files", "case_files"):
        files = inputs.get(field)
        if not isinstance(files, dict):
            continue
        for file_name, expected in sorted(files.items()):
            if not isinstance(file_name, str) or not isinstance(expected, str) or not SHA256.fullmatch(expected):
                add(problems, root, path, 1, f"report {field} entries must map paths to sha256 hashes")
                continue
            target = (root / file_name).resolve()
            if not contained(root.resolve(), target) or not target.is_file():
                add(problems, root, path, 1, f"report evaluation input is missing: `{file_name}`")
                continue
            actual = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                add(problems, root, path, 1, f"report evaluation input hash is stale: `{file_name}`")


def check_companion_relationships(root: Path, problems: list[Problem], catalog: set[str]) -> None:
    registry = root / "docs" / "authoring.md"
    if not registry.is_file():
        return
    text = registry.read_text(encoding="utf-8")
    for match in COMPANION_ROW.finditer(text):
        dependent, companion, remainder = match.groups()
        line = line_number(text, match.start())
        for name in (dependent, companion):
            if name not in catalog and name not in TRACKED_REPOSITORY_LOCAL_SKILLS:
                add(problems, root, registry, line, f"companion relationship references uncataloged Skill `{name}`")
        dependent_skill = (
            root / ".agents" / "skills" / dependent / "SKILL.md"
            if dependent in TRACKED_REPOSITORY_LOCAL_SKILLS
            else root / "skills" / dependent / "SKILL.md"
        )
        if dependent_skill.is_file():
            body = dependent_skill.read_text(encoding="utf-8")
            local_dependent = dependent in TRACKED_REPOSITORY_LOCAL_SKILLS
            reference = f"skills/{companion}/SKILL.md" if local_dependent else f"../{companion}/SKILL.md"
            if reference not in body:
                add(problems, root, dependent_skill, 1, f"companion Skill reference `{reference}` is missing")
            if not local_dependent:
                command = f"apm install mtk177a/skills --skill {dependent} --skill {companion}"
                if command not in body:
                    add(problems, root, dependent_skill, 1, "supported companion installation command is missing")
        else:
            add(problems, root, dependent_skill, 1, "companion relationship dependent Skill is missing")
        if "UPSTREAM.md" not in remainder and not re.search(
            r"https://github\.com/mtk177a/skills/(?:pull|issues)/[0-9]+", remainder
        ):
            add(problems, root, registry, line, "companion registry row must reference provenance")
        if "evals/" not in remainder:
            add(problems, root, registry, line, "companion registry row must reference evaluation coverage")


def repository_text_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(root).as_posix()
        if ".git" in path.relative_to(root).parts or relative in PERSONAL_PATH_EXCLUSIONS:
            continue
        candidates.append(path)
    return sorted(candidates)


def check_personal_paths(root: Path, problems: list[Problem]) -> None:
    for path in repository_text_files(root):
        text = path.read_text(encoding="utf-8")
        for pattern in PERSONAL_PATHS:
            for match in pattern.finditer(text):
                add(
                    problems,
                    root,
                    path,
                    line_number(text, match.start()),
                    f"prohibited environment-specific absolute path `{match.group(0)}`",
                )


def check_deployment_artifacts(root: Path, problems: list[Problem]) -> None:
    for name in ("apm.yml", "apm.lock.yaml"):
        path = root / name
        if path.exists():
            add(problems, root, path, 1, f"source repository must not contain `{name}`; consumers own APM manifests and lockfiles")
    apm_modules = root / "apm_modules"
    if apm_modules.exists():
        add(problems, root, apm_modules, 1, "unexpected APM deployment artifact; remove it after approval")
    deployed = root / ".agents" / "skills"
    if deployed.is_dir():
        for child in sorted(deployed.iterdir()):
            if child.name not in TRACKED_REPOSITORY_LOCAL_SKILLS:
                add(problems, root, child, 1, "unexpected APM-deployed Skill; preserve only tracked repository-local exceptions")


def check_repository(root: Path, ignored_report_skill: str | None = None) -> list[Problem]:
    root = root.resolve()
    problems: list[Problem] = []
    catalog = check_catalogs(root, problems)
    check_skill_packages(root, problems)
    check_markdown_links(root, problems)
    check_localization_notices(root, problems)
    check_json_assets(root, problems, ignored_report_skill)
    check_companion_relationships(root, problems, catalog)
    check_personal_paths(root, problems)
    check_deployment_artifacts(root, problems)
    return sorted(set(problems))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root to inspect (defaults to the checker repository)",
    )
    parser.add_argument(
        "--ignore-report-for-skill",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root: Path = args.root
    if not root.is_dir():
        print(f"{root}:0: repository root is not a directory", file=sys.stderr)
        return 2
    try:
        problems = check_repository(root, args.ignore_report_for_skill)
    except (OSError, UnicodeError) as error:
        print(f"{root}:0: checker could not read repository: {error}", file=sys.stderr)
        return 2
    if problems:
        for problem in problems:
            print(problem.render(), file=sys.stderr)
        return 1
    print("Repository consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
