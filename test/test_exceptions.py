import unittest

from eptransition.exceptions import UnimplementedMethodException, ManagerProcessingException


class TestUnimplementedMethodException(unittest.TestCase):
    def test_type(self):
        e = UnimplementedMethodException()
        self.assertTrue(isinstance(e, Exception))


class TestManagerExceptions(unittest.TestCase):
    def test_a(self):
        e = ManagerProcessingException('mymessage', ['issue1', 'issue2'])
        self.assertTrue(str(e) != '')
