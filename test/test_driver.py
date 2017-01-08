import os
import subprocess
import unittest


class TestDriver(unittest.TestCase):
    def test_driver(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        driver_path = os.path.join(dir_path, "..", "driver.py")
        # usage mode
        r = subprocess.call([driver_path, "usage"], stdout=open(os.devnull, 'wb'))
        self.assertEqual(0, r)
        # incorrect number of args
        r = subprocess.call([driver_path], stdout=open(os.devnull, 'wb'))
        self.assertEqual(1, r)
        r = subprocess.call([driver_path, "hi", "what"], stdout=open(os.devnull, 'wb'))
        self.assertEqual(1, r)
        # bad arg mode
        r = subprocess.call([driver_path, "badarg"], stdout=open(os.devnull, 'wb'))
        self.assertEqual(1, r)
