import os
from unittest import TestCase, skipIf

from eptransition import settings, driver


class TestDriver(TestCase):
    @skipIf(not settings.run_large_tests, "This is a large test that reads the entire idd")
    def test_driver(self):
        # normal arg mode
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "support", "transition_files", "1ZoneEvapCooler.idf")
        idd_path = os.path.join(cur_dir, "..", "support", "transition_files", "Energy+.idd")
        idd_path_2 = os.path.join(cur_dir, "..", "support", "transition_files", "Energy+2.idd")
        r = driver.drive(['program_name', 'update', idf_path, '/tmp/new_idf', idd_path, idd_path_2], True)
        self.assertEqual(0, r)
        # usage mode
        r = driver.drive(['program_name', 'usage'], True)
        self.assertEqual(0, r)
        # incorrect number of args
        r = driver.drive(['program_name'], True)
        self.assertEqual(1, r)
        r = driver.drive(['program_name', 'usage', 'what'], True)
        self.assertEqual(1, r)
        # bad arg mode
        r = driver.drive(['program_name', 'badarg'], True)
        self.assertEqual(1, r)
