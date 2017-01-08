import unittest
import os

import driver


class TestDriver(unittest.TestCase):
    def test_driver(self):
        # normal arg mode
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path = os.path.join(cur_dir, "..", "support", "transition_files", "1ZoneEvapCooler.idf")
        r = driver.drive(['program_name', 'update', idf_path], True)
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
