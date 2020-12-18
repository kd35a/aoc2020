#!/usr/bin/env python3

import unittest
from solution import calculate, calculate_expression, calculate_expression2

class Test18(unittest.TestCase):

    def test_play_game(self):
        self.assertEqual(calculate("1 + 2 * 3 + 4 * 5 + 6", calculate_expression), 71)
        self.assertEqual(calculate("1 + (2 * 3) + (4 * (5 + 6))", calculate_expression), 51)
        self.assertEqual(calculate("1 + 2 * 3 + 4 * 5 + 6", calculate_expression2), 231)

if __name__ == '__main__':
    unittest.main()
