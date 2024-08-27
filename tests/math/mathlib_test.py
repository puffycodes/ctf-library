# file: mathlib_test.py

import unittest
from ctf_library.math.mathlib import MathLib

class MathLibTest(unittest.TestCase):

    # [ <a>, <b>, <gcd>, <lcm> ]
    test_cases = [
        [ 1, 1, 1, 1 ], [ 5, 7, 1, 35 ], [ 35, 7, 7, 35 ],
        [ -5, 7, 1, 35 ], [ 5, -7, -1, 35 ], [ -5, -7, -1, 35 ],
        [ -1, 1, 1, 1 ], [ 1, -1, -1, 1 ], [ -1, -1, -1, 1 ],
        [ 0, 7, 7, 0 ], [ 7, 0, 7, 0 ], [ 0, 0, 0, 0 ],
        [ 210, 30, 30, 210 ], [ 210, 150, 30, 1050 ], [ 1000, 50, 50, 1000 ],
    ]

    def test_gcd(self):
        verbose = False
        for a, b, gcd_expected, _ in MathLibTest.test_cases:
            g = MathLib.gcd(a, b)
            if verbose:
                print(f'gcd({a}, {b}) = {g}')
            self.assertEqual(g, gcd_expected)
        return
    
    def test_xgcd(self):
        verbose = False
        for a, b, gcd_expected, _ in MathLibTest.test_cases:
            g, x, y = MathLib.xgcd(a, b)
            if verbose:
                print(f'gcd({a}, {b}) = {g} = ({a})*({x}) + ({b})* ({y})')
            self.assertEqual(g, gcd_expected)
            g_computed = a * x + b * y
            self.assertEqual(g_computed, g)
        return
    
    def test_lcm(self):
        verbose = False
        for a, b, _, lcd_expected in MathLibTest.test_cases:
            l = MathLib.lcm(a, b)
            if verbose:
                print(f'lcm({a}, {b}) = {l}')
            self.assertEqual(l, lcd_expected)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
