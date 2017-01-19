import os
import unittest

from eptransition import settings, transition


class TestDriver(unittest.TestCase):
    @unittest.skipIf(not settings.run_large_tests, "This is a large test that reads the entire idd")
    def test_driver(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        idf_path_85 = os.path.join(cur_dir, "..", "eptransition", "versions", "8.5", "PlantLoadProfile.idf")
        idf_path = os.path.join(cur_dir, "..", "eptransition", "versions", "8.6", "1ZoneEvapCooler.idf")
        if os.path.exists('/tmp/new_86_branch.idf'):
            os.remove('/tmp/new_86_branch.idf')  # pragma no cover
        r = transition.main([idf_path_85])
        self.assertEqual(0, r)
        if os.path.exists('/tmp/new_idf.idf'):
            os.remove('/tmp/new_idf.idf')  # pragma no cover
        r = transition.main([idf_path])
        self.assertEqual(0, r)
