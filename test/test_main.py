import sys
import unittest
from transition.filetype import TypeEnum
from transition.idf.process import process_one_file
import StringIO


class TestIDFProcessing(unittest.TestCase):
    def test_valid_idf(self):
        idf_object = """
Objecttype,
object_name,
something, !- with a comment

,
last field with space; ! and comment for fun
"""
        ret_value = process_one_file(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(ret_value))


class TestA(unittest.TestCase):
    def setUp(self):
        """
        Does test setup
        """
        self.a = 1
        self.b = 2

    def test_it(self):
        self.assertEqual(3, self.a+self.b)
        self.assertEqual(0, TypeEnum.IDF)

# allow execution directly as python tests/test_main.py
if __name__ == '__main__':
    unittest.main()
