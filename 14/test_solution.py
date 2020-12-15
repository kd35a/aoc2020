#!/usr/bin/env python3

import unittest
from solution import apply_mask, apply_mask2

class Test14(unittest.TestCase):

    def test_apply_mask(self):
        self.assertEqual(apply_mask(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"), 73)
        self.assertEqual(apply_mask(101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"), 101)
        self.assertEqual(apply_mask(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"), 64)

    def test_apply_mask2(self):
        self.assertEqual(apply_mask2(42, "000000000000000000000000000000X1001X"), [26, 27, 58, 59])

if __name__ == '__main__':
    unittest.main()
