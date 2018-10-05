import unittest
from src.pre import pre

class TestStringMethods(unittest.TestCase):
  def test_pre(self):
    filepath = './data/test_book.xlsx'
    self.assertEqual(pre.main(filepath), filepath)

if __name__ == '__main__':
    unittest.main()