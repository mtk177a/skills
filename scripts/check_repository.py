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


KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
CATALOG_ROW = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|", re.MULTILINE)
APM_SKILL = re.compile(r"^\s*-\s+\S+/skills/([a-z0-9-]+)\s*$", re.MULTILINE)
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
COMPANION_ROW = re.compile(r"^\|\s*`([^`]+)`\s*→\s*`([^`]+)`\s*\|(.+)$", re.MULTILINE)
PERSONAL_PATHS = (
    re.compile(r"(?<![A-Za-z0-9_])/(?:home|Users)/[^/\s\"'`<>]+"),
    re.compile(r"(?<![A-Za-z0-9_])/mnt/[A-Za-z]/Users/[^/\s\"'`<>]+"),
    re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:\\Users\\[^\\\s\"'`<>]+"),
)
TEXT_SUFFIXES = {".json", ".md", ".sh", ".txt", ".yaml", ".yml"}


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

    apm = root / "apm.yml"
    if not apm.is_file():
        add(problems, root, apm, 1, "required APM manifest is missing")
        return names
    text = apm.read_text(encoding="utf-8")
    entries = [(match.group(1), line_number(text, match.start())) for match in APM_SKILL.finditer(text)]
    seen: set[str] = set()
    for entry, line in entries:
        if entry in seen:
            add(problems, root, apm, line, f"duplicate APM Skill dependency `{entry}`")
        seen.add(entry)
    apm_names = {entry for entry, _ in entries}
    for missing in sorted(names - apm_names):
        add(problems, root, apm, 1, f"APM manifest is missing Skill `{missing}`")
    for unexpected in sorted(apm_names - names):
        line = next(line for entry, line in entries if entry == unexpected)
        add(problems, root, apm, line, f"APM manifest references unknown Skill `{unexpected}`")
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
        for key in ("name", "description", "license"):
            if key not in fields or not fields[key][0]:
                add(problems, root, skill_file, 1, f"required frontmatter `{key}` is missing or empty")
        name = fields.get("name", ("", 1))[0]
        if not KEBAB_CASE.fullmatch(directory.name):
            add(problems, root, skill_file, 1, f"Skill directory `{directory.name}` is not kebab-case")
        if name and not KEBAB_CASE.fullmatch(name):
            add(problems, root, skill_file, fields["name"][1], f"frontmatter name `{name}` is not kebab-case")
        if name and name != directory.name:
            add(
                problems,
                root,
                skill_file,
                fields["name"][1],
                f"frontmatter name `{name}` does not match directory `{directory.name}`",
            )
        eval_readme = directory / "evals" / "README.md"
        if not eval_readme.is_file():
            add(problems, root, eval_readme, 1, "every Skill requires evals/README.md")


def markdown_without_code(text: str) -> str:
    result: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            marker = match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            result.append("\n" if line.endswith("\n") else "")
            continue
        if fence is not None:
            result.append("\n" if line.endswith("\n") else "")
            continue
        result.append(re.sub(r"`[^`\n]*`", "", line))
    return "".join(result)


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
    for path in sorted((root / "skills").glob("*/SKILL-ja.md")):
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


def check_json_assets(root: Path, problems: list[Problem]) -> None:
    for path in sorted((root / "skills").glob("*/evals/*.json")):
        text = path.read_text(encoding="utf-8")
        try:
            document = json.loads(text)
        except json.JSONDecodeError as error:
            add(problems, root, path, error.lineno, f"invalid JSON: {error.msg}")
            continue
        if not isinstance(document, dict):
            add(problems, root, path, 1, "evaluation JSON top level must be an object")
            continue
        version = document.get("schema_version", document.get("version"))
        if isinstance(version, bool) or not isinstance(version, int) or version < 1:
            add(problems, root, path, 1, "evaluation JSON requires a positive integer schema_version or version")
        expected_skill = path.parent.parent.name
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
                    if not isinstance(case_id, str) or not case_id.strip():
                        add(problems, root, path, 1, "every case requires a non-empty string id")
                    elif case_id in seen:
                        add(problems, root, path, 1, f"duplicate case id `{case_id}`")
                    else:
                        seen.add(case_id)
        if path.name == "results.json":
            check_candidate_hashes(root, path, document, problems)


def check_candidate_hashes(root: Path, path: Path, document: dict[str, object], problems: list[Problem]) -> None:
    candidate = document.get("candidate")
    files = candidate.get("files") if isinstance(candidate, dict) else None
    if files is None:
        return
    if not isinstance(files, dict):
        add(problems, root, path, 1, "candidate.files must be an object")
        return
    skill_root = path.parent.parent.resolve()
    skills_root = (root / "skills").resolve()
    results_text = path.read_text(encoding="utf-8")
    for file_name, expected in sorted(files.items()):
        encoded_name = json.dumps(file_name)
        file_line = next(
            (index for index, value in enumerate(results_text.splitlines(), start=1) if encoded_name in value),
            1,
        )
        if not isinstance(file_name, str) or not isinstance(expected, str):
            add(problems, root, path, file_line, "candidate.files keys and hashes must be strings")
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
        target = (skill_root / file_name).resolve()
        if not contained(skills_root, target):
            add(problems, root, path, file_line, f"candidate file escapes repository skills tree: `{file_name}`")
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


def check_companion_relationships(root: Path, problems: list[Problem], catalog: set[str]) -> None:
    registry = root / "docs" / "authoring.md"
    if not registry.is_file():
        return
    text = registry.read_text(encoding="utf-8")
    for match in COMPANION_ROW.finditer(text):
        dependent, companion, remainder = match.groups()
        line = line_number(text, match.start())
        for name in (dependent, companion):
            if name not in catalog:
                add(problems, root, registry, line, f"companion relationship references uncataloged Skill `{name}`")
        dependent_skill = root / "skills" / dependent / "SKILL.md"
        if dependent_skill.is_file():
            body = dependent_skill.read_text(encoding="utf-8")
            reference = f"../{companion}/SKILL.md"
            command = f"apm install mtk177a/skills --skill {dependent} --skill {companion}"
            if reference not in body:
                add(problems, root, dependent_skill, 1, f"companion Skill reference `{reference}` is missing")
            if command not in body:
                add(problems, root, dependent_skill, 1, "supported companion installation command is missing")
        if "UPSTREAM.md" not in remainder:
            add(problems, root, registry, line, "companion registry row must reference provenance")
        if "evals/" not in remainder:
            add(problems, root, registry, line, "companion registry row must reference evaluation coverage")


def repository_text_files(root: Path) -> list[Path]:
    candidates: set[Path] = set()
    for pattern in ("README*", "AGENTS*", "CLAUDE*", "THIRD_PARTY_NOTICES.md", "apm.yml"):
        candidates.update(path for path in root.glob(pattern) if path.is_file())
    for directory in ("docs", "skills", ".github", ".agents"):
        base = root / directory
        if base.exists():
            candidates.update(
                path for path in base.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
            )
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
    apm_modules = root / "apm_modules"
    if apm_modules.exists():
        add(problems, root, apm_modules, 1, "unexpected APM deployment artifact; remove it after approval")
    deployed = root / ".agents" / "skills"
    if deployed.is_dir():
        for child in sorted(deployed.iterdir()):
            if child.name != "refresh-apm-lockfile":
                add(problems, root, child, 1, "unexpected APM-deployed Skill; preserve only the tracked repository-local exception")


def check_repository(root: Path) -> list[Problem]:
    root = root.resolve()
    problems: list[Problem] = []
    catalog = check_catalogs(root, problems)
    check_skill_packages(root, problems)
    check_markdown_links(root, problems)
    check_localization_notices(root, problems)
    check_json_assets(root, problems)
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root: Path = args.root
    if not root.is_dir():
        print(f"{root}:0: repository root is not a directory", file=sys.stderr)
        return 2
    try:
        problems = check_repository(root)
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
