import StringIO
import os
import unittest

from eptransition.epexceptions import MalformedIDFException, ProcessingException
from eptransition.idf.processidf import IDFProcessor


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
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(idf_structure.objects))

    def test_indented_idf(self):
        idf_object = """
    ObjectType,
    This Object Name,   !- Name
          Descriptive Field,  !- Field Name
\t3.4,                !- Numeric Field
 ,                   !- Optional Blank Field
 Final Value;        !- With Semicolon
"""
        processor = IDFProcessor()
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(idf_structure.objects))

    def test_one_line_idf(self):
        idf_object = """ObjectType,This Object Name,Descriptive Field,3.4,,Final Value;"""
        processor = IDFProcessor()
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(idf_structure.objects))

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
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(1, len(idf_structure.objects))

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
        idf_structure = processor.process_file_given_file_path(idf_path)
        self.assertEquals(75, len(idf_structure.objects))

    def test_valid_idf_file_complex(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "RefBldgLargeHotelNew2004.idf")
        processor = IDFProcessor()
        idf_structure = processor.process_file_given_file_path(idf_path)
        self.assertEquals(1078, len(idf_structure.objects))

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
        idf_structure = processor.process_file_given_file_path(idf_path)
        self.assertEquals(0, len(idf_structure.objects))
