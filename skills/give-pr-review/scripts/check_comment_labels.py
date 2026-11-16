#!/usr/bin/env python3
"""Check the first line of each review comment against the labels of give-pr-review.

Read standard input. Treat each non-empty line as the first line of one comment.
Print one message for each line that does not follow the rules.

Exit codes:
  0  every line follows the rules
  1  at least one line does not follow the rules
  2  the input could not be read
"""

import re
import sys

NEEDS_DECORATION = {"issue", "suggestion", "polish", "question", "typo"}
NO_DECORATION = {"nitpick", "note", "praise"}
MERGE_DECORATIONS = {"blocking", "non-blocking"}
DECORATIONS = MERGE_DECORATIONS | {"if-minor"}

LINE = re.compile(r"^(?P<label>[a-z-]+)(?: \((?P<decorations>[^)]*)\))?: (?P<subject>\S.*)$")


def problems(line):
    """Return the problems in one first line, or an empty list."""
    match = LINE.match(line)
    if not match:
        return ["does not match '<label> (<decorations>): <subject>'"]

    label = match.group("label")
    if label not in NEEDS_DECORATION | NO_DECORATION:
        return [f"unknown label '{label}'"]

    raw = match.group("decorations")
    decorations = [item.strip() for item in raw.split(",")] if raw is not None else []
    found = []
    for decoration in decorations:
        if decoration not in DECORATIONS:
            found.append(f"unknown decoration '{decoration}'")
    if len(set(decorations)) != len(decorations):
        found.append("repeated decoration")

    merge = [item for item in decorations if item in MERGE_DECORATIONS]
    if label in NO_DECORATION and decorations:
        found.append(f"'{label}' takes no decoration")
    if label in NEEDS_DECORATION and len(merge) != 1:
        found.append(f"'{label}' needs exactly one of (blocking) or (non-blocking)")
    return found


def main():
    try:
        text = sys.stdin.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"cannot read input: {error}", file=sys.stderr)
        return 2

    failed = False
    for number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        for problem in problems(line):
            failed = True
            print(f"line {number}: {problem}: {line}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
