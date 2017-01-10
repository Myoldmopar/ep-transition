# import StringIO
import os
import unittest

from transition.idd.processidd import IDDProcessor


class TestIDDProcessingViaFile(unittest.TestCase):
    def test_valid_idd(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idd_path = os.path.join(cur_dir, "..", "..", "support", "transition_files", "Energy+.idd")
        processor = IDDProcessor()
        ret_value = processor.process_file_given_file_path(idd_path)
        self.assertEquals(57, len(ret_value.groups))
