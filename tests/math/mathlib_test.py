# file: mathlib_test.py

import unittest
from ctf_library.math.mathlib import MathLib

class MathLibTest(unittest.TestCase):

    def test_gcd(self):
        test_cases = [
            [ 1, 1, 1 ], [ 5, 7, 1 ], [ 35, 7, 7 ],
            [ -5, 7, 1 ], [ 5, -7, 1 ], [ -5, -7, 1 ],
            [ -1, 1, 1 ], [ 1, -1, 1 ], [ -1, -1, 1 ],
            [ 0, 7, 7 ], [ 7, 0, 7 ], [ 0, 0, 0 ],
            [ 210, 30, 30 ], [ 210, 150, 30 ],
        ]
        for a, b, expected in test_cases:
            self.assertEqual(MathLib.gcd(a, b), expected)
        return
    
    def test_lcm(self):
        test_cases = [
            [ 1, 1, 1 ], [ 5, 7, 35 ], [ 35, 7, 35 ],
            [ -5, 7, 35 ], [ 5, -7, 35 ], [ -5, -7, 35 ],
            [ -1, 1, 1 ], [ 1, -1, 1 ], [ -1, -1, 1 ],
            [ 0, 7, 0 ], [ 7, 0, 0 ], [ 0, 0, 0 ],
            [ 210, 30, 210 ], [ 210, 150, 1050 ],
        ]
        for a, b, expected in test_cases:
            self.assertEqual(MathLib.lcm(a, b), expected)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
