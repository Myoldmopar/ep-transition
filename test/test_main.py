import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

# from mypyopt.ReturnStateEnum import ReturnStateEnum


class TestA(unittest.TestCase):
    def setUp(self):
        """
        Does test setup
        """
	self.a = 1
	self.b = 2

    def test_it(self):
        self.assertEqual(3, self.a+self.b)

# allow execution directly as python tests/test_main.py
if __name__ == '__main__':
    unittest.main()
