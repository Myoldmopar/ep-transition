import os
import shutil
import subprocess
import tempfile
import unittest

from eptransition import settings, transition
from eptransition.exceptions import FileAccessException


class TestDriver(unittest.TestCase):
    @unittest.skipIf(not settings.run_large_tests, "This is a large test that reads the entire idd")
    def test_driver(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path_85 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        idf_path_86 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.6", "1ZoneEvapCooler.idf")
        working_dir = tempfile.mkdtemp()
        shutil.copy(idf_path_85, working_dir)
        final_idf_path_85 = os.path.join(working_dir, os.path.basename(idf_path_85))
        shutil.copy(idf_path_86, working_dir)
        final_idf_path_86 = os.path.join(working_dir, os.path.basename(idf_path_86))
        r = transition.main([final_idf_path_85])
        self.assertEqual(0, r)
        r = transition.main([final_idf_path_86])
        self.assertEqual(0, r)

    def test_driver_cant_instantiate(self):
        idf_path = os.path.join(os.path.abspath(os.sep), "in.idf")
        with self.assertRaises(OSError):
            transition.main([idf_path])

    def test_driver_cant_transition(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        working_dir = tempfile.mkdtemp()
        # shutil.copy(idf_path, working_dir)  # "forgot" to copy the idf in
        os.path.join(working_dir, os.path.basename(idf_path))
        final_idf_path = os.path.join(working_dir, os.path.basename(idf_path))
        with self.assertRaises(FileAccessException):
            transition.main([final_idf_path])

    def test_command_line(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.join(cur_dir, "..")
        transition_file = os.path.join(cur_dir, "..", "eptransition", "transition.py")
        my_env = os.environ.copy()
        my_env["PYTHONPATH"] = root_dir
        subprocess.check_output(["python", transition_file, "-h"], env=my_env)
