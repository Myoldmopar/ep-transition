import unittest

from eptransition.version import START_VERSION, END_VERSION, VersionInformation


class TestVersions(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(isinstance(START_VERSION, VersionInformation))
        self.assertTrue(isinstance(END_VERSION, VersionInformation))
