import unittest

from eptransition.exceptions import UnimplementedMethodException


class TestUnimplementedMethodException(unittest.TestCase):
    def test_type(self):
        e = UnimplementedMethodException()
        self.assertTrue(isinstance(e, Exception))
