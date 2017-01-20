import os
import shutil
import tempfile
import unittest

from eptransition.manager import TransitionManager


class TestManager(unittest.TestCase):
    def test_transition(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copy(idf_path, working_dir)
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        tm = TransitionManager(final_idf_path)
        original_structure, final_structure = tm.perform_transition()

        # do some assertions on the original structure
        self.assertEqual(62, len(original_structure.objects))
        self.assertEqual(8.5, original_structure.version_float)

        # and do some assertions on the final structure
        self.assertEqual(62, len(final_structure.objects))
        self.assertEqual(8.7, final_structure.version_float)

        # do an actual object comparison, first find the first branch object in the file
        first_original_branch_object = original_structure.get_idf_objects_by_type("Branch")[0]
        # then try to find the same branch in the final structure
        same_branch_final = None
        for b in final_structure.get_idf_objects_by_type("Branch"):
            if b.fields[0].upper() == first_original_branch_object.fields[0].upper():
                same_branch_final = b
        if same_branch_final:
            self.assertNotEqual(len(first_original_branch_object.fields), len(same_branch_final.fields))
