import unittest
from transition.filetype import TypeEnum


class TestA(unittest.TestCase):
    def setUp(self):
        """
        Does test setup
        """
        self.a = 1
        self.b = 2

    def test_it(self):
        self.assertEqual(3, self.a+self.b)
        self.assertEqual(0, TypeEnum.IDF)

# allow execution directly as python tests/test_main.py
if __name__ == '__main__':
    unittest.main()
