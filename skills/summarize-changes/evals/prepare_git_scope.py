#!/usr/bin/env python3
"""Prepare or verify the three historical real-Git scope evaluation fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path, PurePosixPath


HERE = Path(__file__).resolve().parent
SOURCE_SKILL = HERE.parent / "SKILL.md"
CASES = HERE / "git-scope-fixtures.json"
EXPECTED_IDS = {
    "staged-only-pr-description",
    "commit-range-public-release",
    "pr-range-operational-handoff",
}


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def write_files(repo: Path, files: dict[str, str]) -> None:
    for name, content in files.items():
        path = PurePosixPath(name)
        if path.is_absolute() or not path.parts or any(part in {".", "..", ".git", ".agents"} for part in path.parts):
            raise ValueError(f"unsafe fixture path: {name}")
        target = repo.joinpath(*path.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def snapshot(repo: Path) -> dict[str, str]:
    return {
        path.relative_to(repo).as_posix(): (
            "symlink" if path.is_symlink() else hashlib.sha256(path.read_bytes()).hexdigest()
        )
        for path in sorted(repo.rglob("*"))
        if (path.is_file() or path.is_symlink()) and ".git" not in path.relative_to(repo).parts
    }


def verify_scope(case_id: str, repo: Path) -> None:
    if case_id == "staged-only-pr-description":
        checks = [
            (git(repo, "diff", "--cached", "--name-only").splitlines(), ["src/export.go", "tests/export_test.go"]),
            (git(repo, "diff", "--name-only").splitlines(), ["docs/operations.md"]),
        ]
        checks.append((
            "?? notes/experiment.md" in git(repo, "status", "--porcelain", "--untracked-files=all").splitlines(), True
        ))
    elif case_id == "commit-range-public-release":
        checks = [
            (git(repo, "rev-list", "--count", "release-base..HEAD"), "2"),
            (git(repo, "log", "--reverse", "--format=%s", "release-base..HEAD").splitlines(), [
                "feat: add customer CSV export", "feat!: rename output flag"
            ]),
            (git(repo, "diff", "--name-only", "release-base..HEAD").splitlines(), [
                "README.md", "cmd/options.go", "src/export.go"
            ]),
        ]
    elif case_id == "pr-range-operational-handoff":
        checks = [
            (git(repo, "branch", "--show-current"), "feature"),
            (git(repo, "merge-base", "main", "feature"), git(repo, "rev-parse", "main")),
            (git(repo, "rev-list", "--count", "main..feature"), "2"),
            (git(repo, "diff", "--name-only", "main...feature").splitlines(), [
                "api/region.go", "migrations/20260729_add_region.sql"
            ]),
        ]
    else:
        raise ValueError(f"unknown case: {case_id}")
    if any(actual != expected for actual, expected in checks):
        raise RuntimeError(f"real-Git scope is incorrect: {case_id}")


def prepare(case: dict[str, object], destination: Path) -> None:
    case_id = case["id"]
    if not isinstance(case_id, str):
        raise ValueError("case id must be a string")
    case_dir = destination / case_id
    repo = case_dir / "repo"
    repo.mkdir(parents=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Evaluation Fixture")
    git(repo, "config", "user.email", "evaluation@example.invalid")
    data = case["git"]
    if not isinstance(data, dict):
        raise ValueError(f"Git fixture must be an object: {case_id}")
    write_files(repo, data["head"])
    git(repo, "add", "--all")
    history = data.get("history")
    git(repo, "commit", "-qm", history[0]["message"] if history else "baseline fixture")
    git(repo, "branch", "-M", "main")
    if history:
        first_ref = history[0]["ref"]
        if first_ref == "release-base":
            git(repo, "branch", "release-base")
        elif first_ref == "main":
            git(repo, "switch", "-q", "-c", "feature")
        else:
            raise ValueError(f"unexpected base ref: {first_ref}")
        for commit in history[1:]:
            write_files(repo, commit["files"])
            git(repo, "add", "--all")
            git(repo, "commit", "-qm", commit["message"])
    else:
        write_files(repo, data["staged"])
        git(repo, "add", "--", *data["staged"])
        write_files(repo, data["unstaged"])
        write_files(repo, data["untracked"])
    skill_target = repo / ".agents" / "skills" / "summarize-changes" / "SKILL.md"
    skill_target.parent.mkdir(parents=True)
    shutil.copyfile(SOURCE_SKILL, skill_target)
    prompt = case["prompt"]
    if not isinstance(prompt, str):
        raise ValueError(f"prompt must be a string: {case_id}")
    prompt_path = case_dir / "prompt.txt"
    prompt_path.write_text(
        "For this evaluation, use the `summarize-changes` Skill at "
        "`.agents/skills/summarize-changes/SKILL.md` in this repository. "
        "Do not read or use a same-name Skill outside this repository. "
        "Return only the task result; do not discuss the evaluation.\n\n" + prompt + "\n",
        encoding="utf-8",
    )
    verify_scope(case_id, repo)
    (case_dir / "manifest.json").write_text(json.dumps({
        "case_id": case_id,
        "prompt_sha256": hashlib.sha256(prompt_path.read_bytes()).hexdigest(),
        "head": git(repo, "rev-parse", "HEAD"),
        "status": git(repo, "status", "--porcelain", "--untracked-files=all"),
        "files": snapshot(repo),
    }, indent=2) + "\n", encoding="utf-8")


def verify(destination: Path) -> None:
    for case_id in sorted(EXPECTED_IDS):
        case_dir = destination / case_id
        repo = case_dir / "repo"
        manifest = json.loads((case_dir / "manifest.json").read_text(encoding="utf-8"))
        verify_scope(case_id, repo)
        current_prompt = hashlib.sha256((case_dir / "prompt.txt").read_bytes()).hexdigest()
        current_head = git(repo, "rev-parse", "HEAD")
        current_status = git(repo, "status", "--porcelain", "--untracked-files=all")
        current_files = snapshot(repo)
        recorded_files = manifest["files"]
        changes = [
            *(f"added {name}" for name in current_files.keys() - recorded_files.keys()),
            *(f"removed {name}" for name in recorded_files.keys() - current_files.keys()),
            *(f"modified {name}" for name in current_files.keys() & recorded_files.keys()
              if current_files[name] != recorded_files[name]),
        ]
        if current_prompt != manifest["prompt_sha256"]:
            changes.append("prompt changed")
        if current_head != manifest["head"]:
            changes.append("head changed")
        if current_status != manifest["status"]:
            changes.append("index or worktree status changed")
        if changes:
            raise RuntimeError(f"fixture changed during execution: {case_id}: {', '.join(sorted(changes))}")
    print("All three real-Git scope fixtures match their recorded state.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new directory under the system temporary directory")
    parser.add_argument("--verify", action="store_true", help="check an existing fixture after execution")
    args = parser.parse_args()
    destination = args.output.resolve()
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if destination == temporary_root or temporary_root not in destination.parents:
        parser.error(f"output must be below {temporary_root}")
    if args.verify:
        verify(destination)
        return
    if destination.exists():
        parser.error(f"output already exists: {destination}")
    document = json.loads(CASES.read_text(encoding="utf-8"))
    cases = document["cases"]
    if document["schema_version"] != 1 or document["skill"] != "summarize-changes" or {case["id"] for case in cases} != EXPECTED_IDS:
        raise ValueError("fixture definitions must contain the three scope cases exactly once")
    destination.mkdir(parents=True)
    for case in cases:
        prepare(case, destination)
    verify(destination)


if __name__ == "__main__":
    main()
