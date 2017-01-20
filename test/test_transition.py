import os
import shutil
import subprocess
import tempfile
import unittest

from eptransition import settings, transition


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

    def test_command_line(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        transition_file = os.path.join(cur_dir, "..", "eptransition", "transition.py")
        subprocess.check_output(["python", transition_file, "-h"])
