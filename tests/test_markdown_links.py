import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from markdown_links import (  # noqa: E402
    heading_anchors,
    is_external_link,
    link_fragment,
    link_path,
    markdown_links,
    markdown_without_code,
)


class MarkdownLinkTests(unittest.TestCase):
    def test_links_are_returned_in_document_order(self) -> None:
        text = "[ref]: docs/b.md\n[inline](docs/a.md \"Title\")\n![image](<docs/c d.png>)\n"

        self.assertEqual(
            [(0, "docs/b.md"), (17, "docs/a.md"), (45, "docs/c d.png")],
            markdown_links(text),
        )

    def test_links_inside_code_are_ignored(self) -> None:
        text = "`[a](a.md)`\n\n```\n[b](b.md)\n```\n\n[c](c.md)\n"

        self.assertEqual(["c.md"], [destination for _, destination in markdown_links(text)])

    def test_code_is_masked_without_moving_offsets(self) -> None:
        text = "a `b` c\n```\nd\n```\n"

        masked = markdown_without_code(text)

        self.assertEqual(len(text), len(masked))
        self.assertEqual(text.count("\n"), masked.count("\n"))
        self.assertEqual("a     c", masked.splitlines()[0])

    def test_link_path_and_fragment_are_decoded(self) -> None:
        self.assertEqual("docs/a b.md", link_path("docs/a%20b.md?x=1#Some%20Part"))
        self.assertEqual("Some Part", link_fragment("docs/a%20b.md?x=1#Some%20Part"))
        self.assertIsNone(link_fragment("docs/a.md"))

    def test_external_links_are_recognized(self) -> None:
        for destination in ("", "#part", "/root.md", "//host/x", "https://example.com", "mailto:a@example.com"):
            with self.subTest(destination=destination):
                self.assertTrue(is_external_link(destination))
        self.assertFalse(is_external_link("docs/a.md"))

    def test_heading_anchors_follow_github_rules(self) -> None:
        text = "# Hello `code` World\n## Hello code World\n```\n# Not a heading\n```\n<a id=\"custom\"></a>\n"

        self.assertEqual({"hello-code-world", "hello-code-world-1", "custom"}, heading_anchors(text))


if __name__ == "__main__":
    unittest.main()
