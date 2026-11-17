"""Parse Markdown links and heading anchors the way GitHub renders them."""

from __future__ import annotations

import re
from urllib.parse import unquote

INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HEADING_START = re.compile(r"^ {0,3}#{1,6}[ \t]")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
HTML_ID = re.compile(r"""<[^>]+\b(?:id|name)=["']([^"']+)["']""")
INLINE_CODE = re.compile(r"`+([^`]*)`+")
MARKDOWN_LINK_TEXT = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")


def markdown_without_code(text: str) -> str:
    """Return the text with fenced code blocks and code spans replaced by spaces, keeping offsets and line breaks."""
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
    """Return the destination of a link target, without angle brackets or a title."""
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    return value.split(maxsplit=1)[0]


def markdown_links(text: str) -> list[tuple[int, str]]:
    """Return the offset and destination of each Markdown link outside code, in document order."""
    visible = markdown_without_code(text)
    matches = sorted(
        [*INLINE_LINK.finditer(visible), *REFERENCE_LINK.finditer(visible)],
        key=lambda match: match.start(),
    )
    return [(match.start(), link_destination(match.group(1))) for match in matches]


def link_path(destination: str) -> str:
    """Return the decoded path of a relative link, without its fragment or query."""
    return unquote(destination.split("#", 1)[0].split("?", 1)[0])


def link_fragment(destination: str) -> str | None:
    """Return the decoded fragment of a link, or None if it has none."""
    if "#" not in destination:
        return None
    return unquote(destination.split("#", 1)[1])


def is_external_link(destination: str) -> bool:
    """Return whether a link leaves the repository's relative paths: empty, a fragment only, absolute, or with a scheme."""
    return (
        not destination
        or destination.startswith(("#", "/", "//"))
        or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", destination) is not None
    )


def heading_anchors(text: str) -> set[str]:
    """Return the anchors that GitHub generates for the headings and HTML ids of a Markdown document."""
    anchors: set[str] = set(HTML_ID.findall(text))
    counts: dict[str, int] = {}
    for original, visible in zip(text.splitlines(), markdown_without_code(text).splitlines()):
        if not HEADING_START.match(visible):
            continue
        heading = HEADING.match(original)
        if heading is None:
            continue
        label = INLINE_CODE.sub(r"\1", heading.group(1))
        label = MARKDOWN_LINK_TEXT.sub(r"\1", label)
        slug = re.sub(r"[^\w\- ]", "", label.strip().lower()).replace(" ", "-")
        suffix = counts.get(slug, 0)
        counts[slug] = suffix + 1
        anchors.add(slug if suffix == 0 else f"{slug}-{suffix}")
    return anchors
