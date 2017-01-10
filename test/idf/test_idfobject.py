import StringIO
import unittest

from transition.idf.idfobject import IDFObject


class TestIDFObject(unittest.TestCase):
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
