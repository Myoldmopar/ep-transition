import unittest

import driver


class TestDriver(unittest.TestCase):
    def test_driver(self):
        # usage mode
        r = driver.drive(['program_name', 'usage'])
        self.assertEqual(0, r)
        # incorrect number of args
        r = driver.drive(['program_name'])
        self.assertEqual(1, r)
        r = driver.drive(['program_name', 'usage', 'what'])
        self.assertEqual(1, r)
        # bad arg mode
        r = driver.drive(['program_name', 'badarg'])
        self.assertEqual(1, r)
