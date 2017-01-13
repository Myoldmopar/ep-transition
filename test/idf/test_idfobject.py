import StringIO
from unittest import TestCase

from eptransition.idd.processidd import IDDProcessor
from eptransition.idf.idfobject import IDFObject
from eptransition.idf.processidf import IDFProcessor


class TestIDFObject(TestCase):
    def test_valid_object(self):
        tokens = ["Objecttype", "object_name", "something", "", "last field with space"]
        obj = IDFObject(tokens)
        self.assertEquals("Objecttype", obj.object_name)
        self.assertEquals(4, len(obj.fields))
        obj.object_string()
        s = StringIO.StringIO()
        obj.write_object(s)
        expected_string = """Objecttype,
  object_name,             !-%20
  something,               !-%20
  ,                        !-%20
  last field with space;   !-%20
"""
        self.assertEqual(expected_string.replace('%20', ' '), s.getvalue())
        tokens = ["Objecttypenofields"]
        obj = IDFObject(tokens)
        self.assertEquals("Objecttypenofields", obj.object_name)
        obj.object_string()
        obj.write_object(s)


class TestSingleLineIDFValidation(TestCase):
    def test_valid_single_token_object_no_idd(self):
        tokens = ["SingleLineObject"]
        obj = IDFObject(tokens)
        self.assertEquals("SingleLineObject", obj.object_name)
        self.assertEquals(0, len(obj.fields))
        s = obj.object_string()
        self.assertEquals("SingleLineObject;\n", s)

    def test_valid_single_token_object_with_idd(self):
        idd_string = """
        \group MyGroup
        SingleLineObject;"""
        idd_object = IDDProcessor().process_file_via_string(idd_string).get_object_by_type('SingleLineObject')
        tokens = ["SingleLineObject"]
        obj = IDFObject(tokens)
        self.assertEquals("SingleLineObject", obj.object_name)
        self.assertEquals(0, len(obj.fields))
        s = obj.object_string(idd_object)
        self.assertEquals("SingleLineObject;\n", s)


class TestIDFValidation(TestCase):
    def setUp(self):
        idd_string = """
\group MyGroup
MyObject,
  N1,  \\field NumericFieldA
       \\minimum 0
       \\maximum 2
       \\required-field
  N2;  \\field NumericFieldB
       \\minimum> 0
       \\maximum< 2
       \\autosizable
        """
        self.idd_structure = IDDProcessor().process_file_via_string(idd_string)
        self.idd_object = self.idd_structure.get_object_by_type('MyObject')

    def test_valid_idf_object(self):
        idf_string = "MyObject,1,1;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 0)

    def test_non_numeric(self):
        idf_string = "MyObject,A,1;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_non_numeric_but_autosize(self):
        idf_string = "MyObject,1,AutoSize;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 0)

    def test_non_numeric_autosize_but_not_allowed(self):
        idf_string = "MyObject,AutoSize,1;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_numeric_too_high_a(self):
        idf_string = "MyObject,3,1;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_numeric_too_high_b(self):
        idf_string = "MyObject,1,2;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_numeric_too_low_a(self):
        idf_string = "MyObject,-1,1;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_numeric_too_low_b(self):
        idf_string = "MyObject,1,0;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_missing_required_field(self):
        idf_string = "MyObject,,1;"
        idf_object = IDFProcessor().process_file_via_string(idf_string).get_idf_objects_by_type('MyObject')[0]
        issues = idf_object.validate(self.idd_object)
        self.assertEqual(len(issues), 1)

    def test_whole_idf_valid(self):
        idf_string = "MyObject,1,1;MyObject,1,1;"
        idf_structure = IDFProcessor().process_file_via_string(idf_string)
        issues = idf_structure.validate(self.idd_structure)
        self.assertEqual(len(issues), 0)

    def test_whole_idf_one_invalid(self):
        idf_string = "MyObject,-1,1;MyObject,1,1;"
        idf_structure = IDFProcessor().process_file_via_string(idf_string)
        issues = idf_structure.validate(self.idd_structure)
        self.assertEqual(len(issues), 1)

    def test_whole_idf_two_invalid(self):
        idf_string = "MyObject,-1,1;MyObject,-1,1;"
        idf_structure = IDFProcessor().process_file_via_string(idf_string)
        issues = idf_structure.validate(self.idd_structure)
        self.assertEqual(len(issues), 2)
