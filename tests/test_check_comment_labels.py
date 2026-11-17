import subprocess
import sys
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / 'skills' / 'give-pr-review' / 'scripts' / 'check_comment_labels.py'


def run(text):
    return subprocess.run([sys.executable, '-B', str(CHECKER)], input=text, capture_output=True, text=True, check=False)


class CommentLabelTests(unittest.TestCase):
    def test_accepts_valid_lines(self):
        result = run(
            'issue (blocking): The retry hides authentication errors\n'
            'suggestion (non-blocking, if-minor): Name the wait list `RETRY_WAITS`\n'
            'nitpick: Prefer a full stop at the end of the message\n'
            '\n'
            'praise: The tests cover each temporary error\n'
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout, '')

    def test_rejects_missing_merge_decoration(self):
        result = run('issue: The retry hides authentication errors\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('needs exactly one of', result.stdout)

    def test_rejects_both_merge_decorations(self):
        result = run('question (blocking, non-blocking): Is the 503 retry safe?\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('needs exactly one of', result.stdout)

    def test_rejects_if_minor_alone(self):
        result = run('polish (if-minor): Shorten the log message\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('needs exactly one of', result.stdout)

    def test_rejects_decoration_on_note(self):
        result = run('note (non-blocking): The client also has a timeout\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn("'note' takes no decoration", result.stdout)

    def test_rejects_unknown_label_and_decoration(self):
        result = run('must: Fix the retry\ntypo (optional): Fix the spelling\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 1: unknown label 'must'", result.stdout)
        self.assertIn("line 2: unknown decoration 'optional'", result.stdout)

    def test_rejects_line_without_format(self):
        result = run('The retry hides authentication errors\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('does not match', result.stdout)


if __name__ == '__main__':
    unittest.main()
