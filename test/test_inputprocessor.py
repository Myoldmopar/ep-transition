import unittest

from transition.exceptions import UnimplementedMethodException
from transition.inputprocessor import InputFileProcessor


class TestInputProcessor(unittest.TestCase):
    def test_it_crashes(self):
        with self.assertRaises(UnimplementedMethodException):
            i = InputFileProcessor()
            i.process_a_file(None)
