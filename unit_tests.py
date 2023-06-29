import unittest


class MyTestCase(unittest.TestCase):
    def test_test_framework(self):
        test_var = True
        self.assertEqual(True, test_var)  # add assertion here


if __name__ == '__main__':
    unittest.main()
