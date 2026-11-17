"""Mechanical checks for the Markdown source conventions of this repository.

The checks cover only rules that need no judgment.
`docs/maintainers/authoring.md` describes the conventions, including the ones that need judgment.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^(?P<indent> *)(?P<marker>[-*+]|\d+[.)])\s+(?P<text>.*)$")
LABEL_ONLY = re.compile(r"^\*\*[^*]+\*\*\s*$")
LABEL_VALUE = re.compile(r"^\*\*[^*]+\*\*:\s*\S")
NUMBERED_STEP = re.compile(r"^\d+[.)]$")
BOLD_NAME = re.compile(r"^\*\*[^*]+\*\*\s*$")


@dataclass
class Line:
    number: int
    text: str
    in_code: bool

    @property
    def blank(self) -> bool:
        return not self.text.strip()

    @property
    def indent(self) -> int:
        return len(self.text) - len(self.text.lstrip(" "))


@dataclass
class Item:
    index: int
    indent: int
    marker: str
    text: str
    end: int = 0
    has_children: bool = False


def source_lines(text: str) -> list[Line]:
    """Split text into lines, mark code-block lines, and blank out frontmatter."""
    raw = text.split("\n")
    lines: list[Line] = []
    fence: str | None = None
    in_frontmatter = bool(raw) and raw[0] == "---"
    for number, value in enumerate(raw, start=1):
        if in_frontmatter:
            if number > 1 and value == "---":
                in_frontmatter = False
            lines.append(Line(number, "", True))
            continue
        match = FENCE.match(value)
        if fence is None and match:
            fence = match.group(1)
            lines.append(Line(number, value, True))
        elif fence is not None:
            closing = FENCE.match(value)
            if closing and closing.group(1)[0] == fence[0] and len(closing.group(1)) >= len(fence) and not value.strip()[len(closing.group(1)):].strip():
                fence = None
            lines.append(Line(number, value, True))
        else:
            lines.append(Line(number, value, False))
    return lines


def list_items(lines: list[Line]) -> list[Item]:
    items: list[Item] = []
    for index, line in enumerate(lines):
        if line.in_code:
            continue
        match = LIST_ITEM.match(line.text)
        if match:
            items.append(Item(index, len(match.group("indent")), match.group("marker"), match.group("text").strip()))
    for item in items:
        end = len(lines)
        for index in range(item.index + 1, len(lines)):
            line = lines[index]
            if line.blank:
                continue
            if line.indent <= item.indent:
                end = index
                break
            item.has_children = True
        while end - 1 > item.index and lines[end - 1].blank:
            end -= 1
        item.end = end
    return items


def sibling_groups(items: list[Item], lines: list[Line]) -> list[list[Item]]:
    """Group items that share a parent and an indent, and are not separated by other content."""
    groups: list[list[Item]] = []
    for item in items:
        group = next((candidate for candidate in groups if candidate[-1].indent == item.indent and candidate[-1].end <= item.index
                      and all(lines[index].blank for index in range(candidate[-1].end, item.index))), None)
        if group is not None:
            group.append(item)
        else:
            groups.append([item])
    return groups


def check_line_breaks(lines: list[Line]) -> list[tuple[int, str]]:
    return [(line.number, "hard line break with a trailing backslash; write the sentences of one paragraph or item on one line")
            for line in lines if not line.in_code and line.text.rstrip(" ").endswith("\\")]


def check_blank_lines(lines: list[Line], items: list[Item], groups: list[list[Item]]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for item in items:
        if item.has_children and item.index + 1 < len(lines) and not lines[item.index + 1].blank:
            found.append((lines[item.index].number, "put a blank line between the text of an item and its first child"))
    for group in groups:
        for previous, current in zip(group, group[1:]):
            gap = current.index - previous.end
            if previous.has_children or current.has_children:
                if gap < 1:
                    found.append((lines[current.index].number, "put a blank line before and after an item that has children"))
            elif gap > 0:
                found.append((lines[current.index].number, "write sibling items without children on consecutive lines"))
    return found


def check_label_forms(lines: list[Line], groups: list[list[Item]]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for group in groups:
        if not any(LABEL_ONLY.match(item.text) and item.has_children for item in group):
            continue
        for item in group:
            if LABEL_VALUE.match(item.text):
                found.append((lines[item.index].number, "give every sibling a label and child items when one sibling has child items"))
    return found


def check_headings(lines: list[Line]) -> list[tuple[int, str]]:
    headings = []
    for index, line in enumerate(lines):
        if line.in_code:
            continue
        match = HEADING.match(line.text)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))
    found: list[tuple[int, str]] = []
    for position, (index, level, name) in enumerate(headings):
        parent = next((candidate for candidate in reversed(headings[:position]) if candidate[1] < level), None)
        if parent is not None and parent[2].casefold() == name.casefold():
            found.append((lines[index].number, "give a child heading a name that differs from its parent heading"))
        following = headings[position + 1:]
        section_end = next((candidate[0] for candidate in following if candidate[1] <= level), len(lines))
        children = [candidate for candidate in following if candidate[0] < section_end and candidate[1] == level + 1]
        own_end = following[0][0] if following else len(lines)
        own_content = any(not lines[i].blank for i in range(index + 1, own_end))
        if len(children) == 1 and not own_content and not any(candidate[1] > level + 1 for candidate in following if candidate[0] < children[0][0]):
            found.append((lines[index].number, "put the only subsection directly in its parent, or give the heading more than one item of content"))
    return found


def check_skill_steps(lines: list[Line], items: list[Item]) -> list[tuple[int, str]]:
    return [(lines[item.index].number, "write a workflow step as a heading such as `### 1. Name`, not as a numbered list item with a bold name")
            for item in items if item.indent == 0 and NUMBERED_STEP.match(item.marker) and BOLD_NAME.match(item.text) and item.has_children]


def markdown_style_problems(text: str, skill_file: bool = False) -> list[tuple[int, str]]:
    """Return (line number, reason) for each convention that the text breaks."""
    lines = source_lines(text)
    items = list_items(lines)
    groups = sibling_groups(items, lines)
    found = check_line_breaks(lines) + check_blank_lines(lines, items, groups) + check_label_forms(lines, groups) + check_headings(lines)
    if skill_file:
        found += check_skill_steps(lines, items)
    return sorted(set(found))
