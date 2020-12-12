#!/usr/bin/env python3

import unittest
from solution import rotate

class Test12(unittest.TestCase):

    def test_rotate(self):
        self.assertEqual(rotate([3, 1], 90), [-1, 3])

if __name__ == '__main__':
    unittest.main()
