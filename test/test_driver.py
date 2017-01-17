import os
import unittest

from eptransition import settings, transition


class TestDriver(unittest.TestCase):
    @unittest.skipIf(not settings.run_large_tests, "This is a large test that reads the entire idd")
    def test_driver(self):
        # normal arg mode
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path_85 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.6", "1ZoneEvapCooler.idf")
        idd_path_85 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "V8-5-0-Energy+.idd")
        idd_path_86 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.6", "V8-6-0-Energy+.idd")
        idd_path_87 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.7", "V8-7-0-Energy+.idd")
        if os.path.exists('/tmp/new_86_branch.idf'):
            os.remove('/tmp/new_86_branch.idf')  # pragma no cover
        r = transition.drive(
            ['program_name', 'update', idf_path_85, '/tmp/new_86_branch.idf', idd_path_85, idd_path_86],
            True)
        self.assertEqual(0, r)
        if os.path.exists('/tmp/new_idf.idf'):
            os.remove('/tmp/new_idf.idf')  # pragma no cover
        r = transition.drive(
            ['program_name', 'update', idf_path, '/tmp/new_idf.idf', idd_path_86, idd_path_87], True)
        self.assertEqual(0, r)
        # usage mode
        r = transition.drive(['program_name', 'usage'], True)
        self.assertEqual(0, r)
        # incorrect number of args
        r = transition.drive(['program_name'], True)
        self.assertEqual(1, r)
        r = transition.drive(['program_name', 'usage', 'what'], True)
        self.assertEqual(1, r)
        # bad arg mode
        r = transition.drive(['program_name', 'badarg'], True)
        self.assertEqual(1, r)
