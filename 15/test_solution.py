#!/usr/bin/env python3

import unittest
from solution import play_game

class Test15(unittest.TestCase):

    def test_play_game(self):
        self.assertEqual(play_game([0,3,6], 10), 0)
        self.assertEqual(play_game([0,3,6], 2020), 436)

if __name__ == '__main__':
    unittest.main()
