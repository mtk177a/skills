import unittest


class TemporaryCiFailureCheck(unittest.TestCase):
    def test_fails_on_purpose(self):
        self.fail('temporary failure to check CI')
