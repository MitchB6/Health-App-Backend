import unittest

def add_numbers(a, b):
    return a + b

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add_numbers(3, 5)
        self.assertEqual(result, 8, "Adding 3 and 5 should be 8")

    def test_add_negative_numbers(self):
        result = add_numbers(-2, -7)
        self.assertEqual(result, -9, "Adding -2 and -7 should be -9")

    def test_add_mixed_numbers(self):
        result = add_numbers(10, -3)
        self.assertEqual(result, 7, "Adding 10 and -3 should be 7")

if __name__ == '__main__':
    unittest.main()