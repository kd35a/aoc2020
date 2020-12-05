#!/usr/bin/env python3

import unittest
from solution import bin_search_row, bin_search_column

class Test5(unittest.TestCase):

    def test_bin_search_row(self):
        self.assertEqual(bin_search_row("BFFFBBF"), 70)
        self.assertEqual(bin_search_row("FFFBBBF"), 14)
        self.assertEqual(bin_search_row("BBFFBBF"), 102)
        self.assertEqual(bin_search_row("BBFFBBB"), 103)

    def test_bin_search_column(self):
        self.assertEqual(bin_search_column("RRR"), 7)
        self.assertEqual(bin_search_column("RLL"), 4)

if __name__ == '__main__':
    unittest.main()
