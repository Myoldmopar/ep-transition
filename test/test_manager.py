import unittest

from transition.manager import TransitionFile


class TestManager(unittest.TestCase):
    def test_dummy(self):
        TransitionFile(None)
        self.assertTrue(True)
