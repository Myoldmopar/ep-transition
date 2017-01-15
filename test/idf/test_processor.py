import StringIO
import os
import unittest

from eptransition.exceptions import MalformedIDFException, ProcessingException
from eptransition.idf.processor import IDFProcessor


class TestIDFProcessingViaStream(unittest.TestCase):
    def test_proper_idf(self):
        idf_object = """
Version,1.1;
ObjectType,
 This Object Name,   !- Name
 Descriptive Field,  !- Field Name
 3.4,                !- Numeric Field
 ,                   !- Optional Blank Field
 Final Value;        !- With Semicolon
"""
        processor = IDFProcessor()
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(2, len(idf_structure.objects))

    def test_indented_idf(self):
        idf_object = """
    Version,1.1;
    ObjectType,
    This Object Name,   !- Name
          Descriptive Field,  !- Field Name
\t3.4,                !- Numeric Field
 ,                   !- Optional Blank Field
 Final Value;        !- With Semicolon
"""
        processor = IDFProcessor()
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(2, len(idf_structure.objects))

    def test_one_line_idf(self):
        idf_object = """Version,1.1;ObjectType,This Object Name,Descriptive Field,3.4,,Final Value;"""
        processor = IDFProcessor()
        idf_structure = processor.process_file_via_stream(StringIO.StringIO(idf_object))
        self.assertEquals(2, len(idf_structure.objects))

    def test_invalid_goofy_idf(self):
        idf_object = """
Version,1.1;
Objecttype,
object_name,
something, !- with a comment

,
! here is a comment line
last field with space; ! and comment for fun
"""
        processor = IDFProcessor()
        with self.assertRaises(MalformedIDFException):
            processor.process_file_via_stream(StringIO.StringIO(idf_object))

    def test_nonnumerc_version(self):
        idf_object = """
Version,A.Q;
"""
        processor = IDFProcessor()
        with self.assertRaises(ProcessingException):
            processor.process_file_via_stream(StringIO.StringIO(idf_object))

    def test_missing_comma(self):
        idf_object = """
Version,1.1;
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
Version,1.1;
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
        self.assertEquals(78, len(idf_structure.objects))

    def test_valid_idf_file_complex(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "RefBldgLargeHotelNew2004.idf")
        processor = IDFProcessor()
        idf_structure = processor.process_file_given_file_path(idf_path)
        self.assertEquals(1136, len(idf_structure.objects))

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
        with self.assertRaises(ProcessingException) as e:  # should fail because needs version object at least
            processor.process_file_given_file_path(idf_path)

    def test_minimal_idf(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "Minimal.idf")
        processor = IDFProcessor()
        idf_structure = processor.process_file_given_file_path(idf_path)
        self.assertEquals(1, len(idf_structure.objects))
        self.assertAlmostEqual(idf_structure.version_float, 1.1, 1)
