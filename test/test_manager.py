import logging
import os
import shutil
import tempfile
import unittest

from eptransition.manager import TransitionManager
from eptransition.exceptions import FileAccessException, FileTypeException, ManagerProcessingException

logging.basicConfig(filename=tempfile.mktemp(), level=logging.DEBUG)


class TestManager(unittest.TestCase):
    def test_valid_transition_results(self):
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

    def test_permission_creating_working_dir(self):
        pretend_root_idf = os.path.join(os.path.abspath(os.sep), "in.idf")
        with self.assertRaises(OSError):
            TransitionManager(pretend_root_idf)

    def test_idf_doesnt_exist(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        working_dir = tempfile.mkdtemp()
        # shutil.copy(idf_path, working_dir)  # "forgot" to copy the idf in
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        tm = TransitionManager(final_idf_path)
        with self.assertRaises(FileAccessException):
            tm.perform_transition()

    def test_folder_already_exists(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copy(idf_path, working_dir)  # "forgot" to copy the idf in
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        tm = TransitionManager(final_idf_path)
        tm.perform_transition()
        TransitionManager(final_idf_path)

    def test_idf_bad_extension(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copyfile(idf_path, os.path.join(working_dir, "bad_extension.idq"))  # "forgot" to copy the idf in
        final_idf_path = os.path.join(working_dir, "bad_extension.idq")
        tm = TransitionManager(final_idf_path)
        with self.assertRaises(FileTypeException):
            tm.perform_transition()

    def test_cant_process_idf(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "other", "Invalid.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copy(idf_path, working_dir)  # "forgot" to copy the idf in
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        tm = TransitionManager(final_idf_path)
        with self.assertRaises(ManagerProcessingException):
            tm.perform_transition()

    def test_process_idf_no_version(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "other", "ValidNoVersion.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copy(idf_path, working_dir)  # "forgot" to copy the idf in
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        tm = TransitionManager(final_idf_path)
        with self.assertRaises(ManagerProcessingException):
            tm.perform_transition()

    def test_process_idf_unincluded_version(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "other", "InvalidVersion.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copy(idf_path, working_dir)  # "forgot" to copy the idf in
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        tm = TransitionManager(final_idf_path)
        with self.assertRaises(ManagerProcessingException):
            tm.perform_transition()
