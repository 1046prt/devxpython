import unittest
from src.main import hello

class TestMain(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")

if __name__ == '__main__':
    unittest.main()
