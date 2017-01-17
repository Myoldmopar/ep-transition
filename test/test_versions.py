import unittest

from eptransition.versions.versions import TypeEnum


class TestTypeEnums(unittest.TestCase):
    def test_they_exist(self):
        types = TypeEnum()
        attributes = dir(types)
        self.assertTrue("IDF" in attributes)
        self.assertTrue("JSON" in attributes)
