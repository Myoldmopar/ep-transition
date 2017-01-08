import StringIO
import unittest

from transition.idf.processidf import IDFProcessor


class TestIDFProcessing(unittest.TestCase):
    def test_valid_idf(self):
        idf_object = """
Objecttype,
object_name,
something, !- with a comment

,
! here is a comment line
last field with space; ! and comment for fun
"""
        processor = IDFProcessor()
        ret_value = processor.process_one_file(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(ret_value))
