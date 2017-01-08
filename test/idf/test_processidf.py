import StringIO
import unittest
import os

from transition.idf.processidf import IDFProcessor
from transition.exceptions import MalformedIDFException, ProcessingException


class TestIDFProcessingViaStream(unittest.TestCase):
    def test_proper_idf(self):
        idf_object = """
ObjectType,
 This Object Name,   !- Name
 Descriptive Field,  !- Field Name
 3.4,                !- Numeric Field
 ,                   !- Optional Blank Field
 Final Value;        !- With Semicolon
"""
        processor = IDFProcessor()
        ret_value = processor.process_file_via_stream(StringIO.StringIO(idf_object))
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
        processor = IDFProcessor()
        ret_value = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(ret_value))

    def test_missing_comma(self):
        idf_object = """
Objecttype,
object_name,
a line without a comma
something, !- with a comment
"""
        processor = IDFProcessor()
        with self.assertRaises(MalformedIDFException):
            processor.process_file_via_stream(StringIO.StringIO(idf_object))

    def test_missing_semicolon(self):
        idf_object = """
Objecttype,
object_name,
something without a semicolon !- with a comment
"""
        processor = IDFProcessor()
        with self.assertRaises(MalformedIDFException):
            processor.process_file_via_stream(StringIO.StringIO(idf_object))


class TestIDFProcessingViaFile(unittest.TestCase):

    def test_valid_idf_file_simple(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "1ZoneEvapCooler.idf")
        processor = IDFProcessor()
        ret_value = processor.process_file_given_file_path(idf_path)
        self.assertEquals(74, len(ret_value))

    def test_valid_idf_file_complex(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "RefBldgLargeHotelNew2004.idf")
        processor = IDFProcessor()
        ret_value = processor.process_file_given_file_path(idf_path)
        self.assertEquals(1078, len(ret_value))

    def test_missing_idf(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "NotReallyThere.idf")
        processor = IDFProcessor()
        with self.assertRaises(ProcessingException):
            processor.process_file_given_file_path(idf_path)

    def test_blank_idf(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "Blank.idf")
        processor = IDFProcessor()
        ret_value = processor.process_file_given_file_path(idf_path)
        self.assertEquals(0, len(ret_value))
