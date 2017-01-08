import StringIO
import unittest

from transition.idf.processidf import IDFProcessor
from transition.exceptions import MalformedIDFException


class TestIDFProcessing(unittest.TestCase):
    def test_proper_idf(self):
        idf_object = """
ObjectType,
 This Object Name,   !- Name
 Descriptive Field,  !- Field Name
 3.4,                !- Numeric Field
 ,                   !- Optional Blank Field
 Final Value;        !- With Semicolon
"""
        processor = IDFProcessor(StringIO.StringIO(idf_object))
        ret_value = processor.process_one_file()
        self.assertEquals(1, len(ret_value))

    def test_valid_goofy_idf(self):
        idf_object = """
Objecttype,
object_name,
something, !- with a comment

,
! here is a comment line
last field with space; ! and comment for fun
"""
        processor = IDFProcessor(StringIO.StringIO(idf_object))
        ret_value = processor.process_one_file()
        self.assertEquals(1, len(ret_value))

    def test_missing_comma(self):
        idf_object = """
Objecttype,
object_name,
a line without a comma
something, !- with a comment
"""
        processor = IDFProcessor(StringIO.StringIO(idf_object))
        with self.assertRaises(MalformedIDFException):
            processor.process_one_file()

    def test_missing_semicolon(self):
        idf_object = """
Objecttype,
object_name,
something without a semicolon !- with a comment
"""
        processor = IDFProcessor(StringIO.StringIO(idf_object))
        with self.assertRaises(MalformedIDFException):
            processor.process_one_file()
