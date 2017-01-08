import unittest

import driver


class TestDriver(unittest.TestCase):
    def test_driver(self):
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
