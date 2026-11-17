#!/usr/bin/env python3
"""Deterministic, read-only consistency checks for this repository."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from markdown_links import heading_anchors, is_external_link, link_fragment, link_path, markdown_links
from upstream_mirrors import UPSTREAM_LICENSE_DECLARATION, UPSTREAM_MIRRORS, recorded_mirror_hash

TRACKED_REPOSITORY_LOCAL_SKILLS = {"maintain-japanese-references"}


KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATALOG_ROW = re.compile(
    r"^\|\s*`(?P<plain>[a-z0-9-]+)`\s*\|"
    r"|^\|[^|\n]+\|\s*\[`(?P<linked>[a-z0-9-]+)`\]\(skills/[^)\s]+/SKILL(?:-ja)?\.md\)\s*\|[ \t]*$",
    re.MULTILINE,
)
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
COMPANION_REGISTRY = Path("docs") / "maintainers" / "authoring.md"


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


def frontmatter_closing(lines: list[str]) -> int | None:
    """Return the index of the closing `---` of frontmatter that opens on the first line."""
    return next((index for index, value in enumerate(lines[1:], start=1) if value == "---"), None)


def parse_frontmatter(path: Path) -> tuple[dict[str, tuple[str, int]], list[tuple[int, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, []
    closing = frontmatter_closing(lines)
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


def parse_single_quoted_yaml_scalar(value: str) -> tuple[str | None, int]:
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
        return "".join(parsed), index + 1
    return None, index


def parse_frontmatter_scalar(raw: str) -> tuple[str | None, str | None]:
    value = raw.strip()
    guidance = "must use a supported single-line string scalar (plain, single-quoted, or double-quoted)"
    if not value:
        return "", None
    if value[0] in "\"'":
        parse_quoted = parse_double_quoted_yaml_scalar if value[0] == '"' else parse_single_quoted_yaml_scalar
        parsed, end = parse_quoted(value)
        remainder = value[end:].strip()
        if parsed is None or (remainder and not remainder.startswith("#")):
            return None, guidance
        return parsed, None
    if value[0] in "[{|>&*!":
        return None, guidance
    return re.split(r"\s+#", value, maxsplit=1)[0].rstrip(), None


def repository_files(root: Path) -> list[Path]:
    """Return every file in the repository, without entering `.git` directories."""
    files: list[Path] = []
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories[:] = [name for name in subdirectories if name != ".git"]
        files.extend(path for name in filenames if (path := Path(directory, name)).is_file())
    return sorted(files)


def skill_file(root: Path, name: str, filename: str = "SKILL.md") -> Path:
    """Return a file of a tracked repository-local Skill or a public Skill."""
    if name in TRACKED_REPOSITORY_LOCAL_SKILLS:
        return root / ".agents" / "skills" / name / filename
    return root / "skills" / name / filename


def companion_rows(root: Path) -> list[tuple[str, str, str, int]] | None:
    """Return each companion registry row as (dependent, companion, remainder, line), or None if the registry is missing."""
    registry = root / COMPANION_REGISTRY
    if not registry.is_file():
        return None
    text = registry.read_text(encoding="utf-8")
    return [(*match.groups(), line_number(text, match.start())) for match in COMPANION_ROW.finditer(text)]


def skill_directories(root: Path) -> list[Path]:
    skills = root / "skills"
    if not skills.is_dir():
        return []
    return sorted(path for path in skills.iterdir() if path.is_dir() and not path.name.startswith("."))


def parse_catalog(path: Path) -> tuple[list[tuple[str, int]], int | None]:
    text = path.read_text(encoding="utf-8")
    entries = [
        (match.group("plain") or match.group("linked"), line_number(text, match.start()))
        for match in CATALOG_ROW.finditer(text)
    ]
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
        if declared_count is not None and declared_count != len(names):
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
        required_keys = (
            ("name", "description")
            if directory.name in UPSTREAM_MIRRORS
            else ("name", "description", "license")
        )
        for key in required_keys:
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


def check_upstream_mirrors(root: Path, problems: list[Problem]) -> None:
    for name, source in UPSTREAM_MIRRORS.items():
        directory = root / "skills" / name
        if not directory.is_dir():
            continue
        note = directory / "UPSTREAM.md"
        skill = directory / "SKILL.md"
        if not note.is_file():
            add(problems, root, note, 1, "upstream mirror provenance is missing")
            continue
        body = note.read_text(encoding="utf-8")
        if f"- Source: <{source}>" not in body:
            add(problems, root, note, 1, "upstream mirror source is missing or incorrect")
        if not re.search(r"^- Mirrored revision: `[0-9a-f]{40}`$", body, re.MULTILINE):
            add(problems, root, note, 1, "upstream mirror revision is missing or invalid")
        if not re.search(r"^- Retrieved: `[0-9]{4}-[0-9]{2}-[0-9]{2}`$", body, re.MULTILINE):
            add(problems, root, note, 1, "upstream mirror retrieval date is missing or invalid")
        license_recorded = re.search(r"^- License: Unlicense$", body, re.MULTILINE)
        declaration_recorded = re.search(
            rf"^- License declaration: <{re.escape(UPSTREAM_LICENSE_DECLARATION)}>$",
            body,
            re.MULTILINE,
        )
        if not license_recorded or not declaration_recorded:
            add(problems, root, note, 1, "upstream mirror license evidence is missing")
        recorded_hash = recorded_mirror_hash(body)
        if recorded_hash is None:
            add(problems, root, note, 1, "upstream mirror SHA-256 is missing or invalid")
        elif skill.is_file() and hashlib.sha256(skill.read_bytes()).hexdigest() != recorded_hash:
            add(problems, root, skill, 1, "mirrored SKILL.md differs from recorded SHA-256")


def contained(root: Path, target: Path) -> bool:
    try:
        target.relative_to(root)
        return True
    except ValueError:
        return False


def check_markdown_links(root: Path, problems: list[Problem]) -> None:
    anchor_cache: dict[Path, set[str]] = {}
    for path in repository_files(root):
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for offset, destination in markdown_links(text):
            line = line_number(text, offset)
            if destination.startswith("#"):
                target = path.resolve()
            elif is_external_link(destination):
                continue
            else:
                target = (path.parent / link_path(destination)).resolve()
                if not contained(root, target):
                    add(problems, root, path, line, f"relative Markdown link escapes repository: `{destination}`")
                    continue
                if not target.exists():
                    add(problems, root, path, line, f"relative Markdown link target does not exist: `{destination}`")
                    continue
            fragment = link_fragment(destination)
            if fragment is None or target.suffix.lower() != ".md" or not target.is_file():
                continue
            if target not in anchor_cache:
                anchor_cache[target] = heading_anchors(target.read_text(encoding="utf-8"))
            if fragment not in anchor_cache[target]:
                add(problems, root, path, line, f"Markdown link fragment does not match a heading in the target: `{destination}`")


def check_localization_notices(root: Path, problems: list[Problem]) -> None:
    paths = list((root / "skills").glob("*/SKILL-ja.md"))
    paths.extend(
        path
        for name in TRACKED_REPOSITORY_LOCAL_SKILLS
        if (path := skill_file(root, name, "SKILL-ja.md")).is_file()
    )
    for path in sorted(paths):
        lines = path.read_text(encoding="utf-8").splitlines()
        start = 0
        if lines and lines[0] == "---":
            closing = frontmatter_closing(lines)
            if closing is None:
                add(problems, root, path, 1, "translation frontmatter has no closing delimiter")
                continue
            start = closing + 1
        notice_start = next((index for index in range(start, len(lines)) if lines[index].strip()), len(lines))
        notice_lines = []
        for value in lines[notice_start:]:
            if not value.strip():
                break
            notice_lines.append(value.strip())
        notice = " ".join(notice_lines)
        starts_with_heading = bool(notice_lines) and notice_lines[0].startswith("#")
        has_english_source = "SKILL.md" in notice and (
            "英語版" in notice or "english" in notice.lower()
        )
        has_reference = "reference" in notice.lower() or "参考" in notice
        if starts_with_heading or not (has_english_source and has_reference):
            add(
                problems,
                root,
                path,
                notice_start + 1,
                "Japanese translation must begin with a notice identifying English SKILL.md and this file as a reference translation",
            )


def check_companion_relationships(
    root: Path,
    problems: list[Problem],
    catalog: set[str],
    rows: list[tuple[str, str, str, int]] | None,
) -> None:
    registry = root / COMPANION_REGISTRY
    if rows is None:
        add(problems, root, registry, 1, "companion relationship registry is missing")
        return
    for dependent, companion, remainder, line in rows:
        for name in (dependent, companion):
            if name not in catalog and name not in TRACKED_REPOSITORY_LOCAL_SKILLS:
                add(problems, root, registry, line, f"companion relationship references uncataloged Skill `{name}`")
        dependent_skill = skill_file(root, dependent)
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


def check_skill_name_references(
    root: Path,
    problems: list[Problem],
    catalog: set[str],
    rows: list[tuple[str, str, str, int]] | None,
) -> None:
    # Skills must work alone; relationships between Skills belong in docs/users/workflows.md.
    allowed = {(dependent, companion) for dependent, companion, _, _ in rows or []}
    for name in sorted(catalog - set(UPSTREAM_MIRRORS)):
        for filename in ("SKILL.md", "SKILL-ja.md"):
            path = root / "skills" / name / filename
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for other in sorted(catalog - {name}):
                if (name, other) in allowed:
                    continue
                for match in re.finditer(rf"(?<![\w-]){re.escape(other)}(?![\w-])", text):
                    add(
                        problems,
                        root,
                        path,
                        line_number(text, match.start()),
                        f"Skill instructions must not name another Skill `{other}`; describe the needed input or boundary instead",
                    )


def check_personal_paths(root: Path, problems: list[Problem]) -> None:
    for path in repository_files(root):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.relative_to(root).as_posix() in PERSONAL_PATH_EXCLUSIONS:
            continue
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


def check_repository(root: Path) -> list[Problem]:
    root = root.resolve()
    problems: list[Problem] = []
    catalog = check_catalogs(root, problems)
    check_skill_packages(root, problems)
    check_upstream_mirrors(root, problems)
    check_markdown_links(root, problems)
    check_localization_notices(root, problems)
    rows = companion_rows(root)
    check_companion_relationships(root, problems, catalog, rows)
    check_skill_name_references(root, problems, catalog, rows)
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
