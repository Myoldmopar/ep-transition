import StringIO
import os
from unittest import TestCase, skip

from transition.idd.processidd import IDDProcessor


class TestIDDProcessingViaStream(TestCase):
    def test_proper_idd(self):
        idd_object = """
\\group Simulation Parameters

Version,
      \\memo Specifies the EnergyPlus version of the IDF file.
      \\unique-object
      \format singleLine
  A1 ; \\field Version Identifier
      \\default 8.6

"""
        processor = IDDProcessor()
        ret_value = processor.process_file_via_stream(StringIO.StringIO(idd_object))
        self.assertEquals(1, len(ret_value.groups))
        self.assertEquals(1, len(ret_value.groups[0].objects))

    def test_repeated_object_meta_idd(self):
        idd_object = """
\\group Simulation Parameters

Version,
      \\memo Specifies the EnergyPlus version of the IDF file.
      \\memo Some additional memo line
      \\unique-object
      \format singleLine
  A1 ; \\field Version Identifier
      \\default 8.6

"""
        processor = IDDProcessor()
        ret_value = processor.process_file_via_stream(StringIO.StringIO(idd_object))
        self.assertEquals(1, len(ret_value.groups))
        self.assertEquals(1, len(ret_value.groups[0].objects))
        version_obj = ret_value.get_object_by_type("version")
        self.assertEquals(1, len(version_obj.fields))

    def test_invalid_idd_obj_lookup(self):
        idd_object = """
\\group Stuff
Version,A1;
"""
        processor = IDDProcessor()
        ret_value = processor.process_file_via_stream(StringIO.StringIO(idd_object))
        bad_obj = ret_value.get_object_by_type("noObjecT")
        self.assertIsNone(bad_obj)

class TestIDDProcessingViaFile(TestCase):

    @skip("Big test")
    def test_valid_idd(self):  # pragma: no cover
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idd_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "Energy+.idd")
        processor = IDDProcessor()
        ret_value = processor.process_file_given_file_path(idd_path)
        self.assertEquals(57, len(ret_value.groups))
