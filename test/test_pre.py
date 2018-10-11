import unittest
import pandas as pd
from src.pre import pre

class TestStringMethods(unittest.TestCase):
  def test_pre(self):
    filepath = './test/data/test_book.xlsx'
    headers = ['Item', 'Default', 'Val*']

    expected_sheet1 = pd.DataFrame({
      'Item': ['AAA', 'BBB', 'CCC', 'DDD', 'EEE'],
      'Default': ['aaa', 'bbb', '', 'ddd', 'eee'],
      'Val1': ['xxx', 'xxx', '', 'ddd', 'eee'],
      'Val2': ['aaa', 'bbb', '', 'ddd', 'eee'],
      'Val3':  ['aaa', 'bbb', '', 'xxx', 'xxx']
    })
    expected_sheet2 = pd.DataFrame({
      'Item': ['FFF', 'GGG', 'HHH'],
      'Default': ['fff', '', 'hhh'],
      'Val1': ['fff', '', 'hhh'],
      'Val2': ['fff', '', 'hhh']
    })

    actual = pre.main(filepath, headers)
    self.assertTrue(actual[0].equals(expected_sheet1))
    self.assertTrue(actual[1].equals(expected_sheet2))

if __name__ == '__main__':
    unittest.main()