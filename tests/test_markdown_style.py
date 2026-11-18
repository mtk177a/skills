import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from markdown_style import markdown_style_problems  # noqa: E402

CHECKER = REPOSITORY_ROOT / "scripts" / "check_repository.py"


def reasons(text, skill_file=False):
    return [reason for _, reason in markdown_style_problems(text, skill_file)]


class LineBreakTests(unittest.TestCase):
    def test_rejects_trailing_backslash(self):
        self.assertIn("hard line break", reasons("# Title\n\nOne sentence.\\\nTwo sentences.\n")[0])

    def test_ignores_backslash_in_code_block(self):
        self.assertEqual(reasons("# Title\n\n```text\nline \\\n```\n"), [])

    def test_ignores_frontmatter(self):
        self.assertEqual(reasons("---\nname: x\\\n---\n\n# Title\n"), [])


class BlankLineTests(unittest.TestCase):
    def test_accepts_conventional_list(self):
        text = (
            "# Title\n\n"
            "- **Scope**\n\n"
            "  - The files under docs.\n\n"
            "- **Exceptions**\n\n"
            "  - The generated files.\n"
            "  - The files that a tool owns.\n"
        )
        self.assertEqual(reasons(text), [])

    def test_rejects_missing_blank_line_before_first_child(self):
        text = "# Title\n\n- **Scope**\n  - The files under docs.\n"
        self.assertTrue(any("between the text of an item" in reason for reason in reasons(text)))

    def test_rejects_missing_blank_line_around_item_with_children(self):
        text = "# Title\n\n- One item.\n- **Group**\n\n  - A child.\n"
        self.assertTrue(any("before and after an item that has children" in reason for reason in reasons(text)))

    def test_rejects_blank_line_between_items_without_children(self):
        text = "# Title\n\n- One item.\n\n- Another item.\n"
        self.assertTrue(any("consecutive lines" in reason for reason in reasons(text)))


class LabelFormTests(unittest.TestCase):
    def test_rejects_value_label_beside_label_with_children(self):
        text = (
            "# Title\n\n"
            "- **Scope**: the files under docs.\n\n"
            "- **Exceptions**\n\n"
            "  - The generated files.\n"
        )
        self.assertTrue(any("every sibling a label" in reason for reason in reasons(text)))

    def test_accepts_value_labels_alone(self):
        self.assertEqual(reasons("# Title\n\n- **Scope**: docs.\n- **Owner**: maintainers.\n"), [])


class HeadingTests(unittest.TestCase):
    def test_rejects_child_with_parent_name(self):
        text = "# Title\n\n## Checks\n\nIntro.\n\n### Checks\n\nText.\n\n### Other\n\nText.\n"
        self.assertTrue(any("differs from its parent" in reason for reason in reasons(text)))

    def test_rejects_heading_with_only_one_subsection(self):
        text = "# Title\n\nIntro.\n\n## Checks\n\n### Line breaks\n\nText.\n"
        self.assertTrue(any("only subsection" in reason for reason in reasons(text)))

    def test_accepts_heading_with_two_subsections(self):
        text = "# Title\n\nIntro.\n\n## Checks\n\n### Line breaks\n\nText.\n\n### Headings\n\nText.\n"
        self.assertEqual(reasons(text), [])


class SkillStepTests(unittest.TestCase):
    def test_rejects_numbered_bold_step_in_skill_file(self):
        text = "# Skill\n\nIntro.\n\n## Workflow\n\n1. **Identify the target**\n\n   - Read the request.\n"
        self.assertTrue(any("as a heading" in reason for reason in reasons(text, skill_file=True)))

    def test_ignores_numbered_bold_step_outside_skill_files(self):
        text = "# Guide\n\nIntro.\n\n## Steps\n\n1. **Identify the target**\n\n   - Read the request.\n"
        self.assertEqual(reasons(text, skill_file=False), [])

    def test_accepts_step_headings(self):
        text = "# Skill\n\nIntro.\n\n## Workflow\n\n### 1. Identify the target\n\n- Read the request.\n\n### 2. Write\n\n- Write it.\n"
        self.assertEqual(reasons(text, skill_file=True), [])


class ScopeTests(unittest.TestCase):
    def run_checker(self, root):
        return subprocess.run([sys.executable, "-B", str(CHECKER), "--root", str(root)], capture_output=True, text=True, check=False)

    def test_checks_only_listed_files_and_reports_missing_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "scripts").mkdir()
            (root / "docs").mkdir()
            (root / "docs" / "listed.md").write_text("# Listed\n\nOne.\\\nTwo.\n", encoding="utf-8")
            (root / "docs" / "unlisted.md").write_text("# Unlisted\n\nOne.\\\nTwo.\n", encoding="utf-8")
            (root / "scripts" / "markdown-style-files.txt").write_text("# comment\ndocs/listed.md\ndocs/missing.md\n", encoding="utf-8")
            result = self.run_checker(root)
            self.assertIn("docs/listed.md:3: hard line break", result.stderr)
            self.assertNotIn("docs/unlisted.md", result.stderr)
            self.assertIn("listed file does not exist: docs/missing.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
