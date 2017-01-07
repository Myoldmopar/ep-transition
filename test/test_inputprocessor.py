import unittest
from transition.inputprocessor import InputFileProcessor
from transition.exceptions import UnimplementedMethodException


class TestInputProcessor(unittest.TestCase):

    def test_it_crashes(self):
        with self.assertRaises(UnimplementedMethodException):
            i = InputFileProcessor()
            i.process_a_file(None)
