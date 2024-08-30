# file: mathlib_test.py

import unittest
from ctf_library.math.mathlib import MathLib

class MathLibTest(unittest.TestCase):

    # [ <a>, <b>, <gcd>, <lcm> ]
    test_cases_gcd_lcm = [
        [ 1, 1, 1, 1 ], [ 5, 7, 1, 35 ], [ 35, 7, 7, 35 ],
        [ -5, 7, 1, 35 ], [ 5, -7, -1, 35 ], [ -5, -7, -1, 35 ],
        [ -1, 1, 1, 1 ], [ 1, -1, -1, 1 ], [ -1, -1, -1, 1 ],
        [ 0, 7, 7, 0 ], [ 7, 0, 7, 0 ], [ 0, 0, 0, 0 ],
        [ 210, 30, 30, 210 ], [ 210, 150, 30, 1050 ],
        [ -210, 30, 30, 210], [ 210, -30, -30, 210 ], [ -210, -30, -30, 210 ],
        [ 1000, 50, 50, 1000 ],
    ]

    def test_gcd(self):
        verbose = False
        for a, b, gcd_expected, _ in MathLibTest.test_cases_gcd_lcm:
            g = MathLib.gcd(a, b)
            g_e1 = MathLib.gcd_euclidean(a, b)
            g_e2 = MathLib.gcd_euclidean_recursive(a, b)
            if verbose:
                print(f'gcd({a}, {b}) = {g}')
            self.assertEqual(g, abs(gcd_expected))
            self.assertEqual(g_e1, gcd_expected)
            self.assertEqual(g_e2, gcd_expected)
        return
    
    def test_xgcd(self):
        verbose = False
        for a, b, gcd_expected, _ in MathLibTest.test_cases_gcd_lcm:
            g, x, y = MathLib.xgcd(a, b)
            if verbose:
                print(f'gcd({a}, {b}) = {g} = ({a})*({x}) + ({b})* ({y})')
            self.assertEqual(g, gcd_expected)
            g_computed = a * x + b * y
            self.assertEqual(g_computed, g)
        return
    
    def test_lcm(self):
        verbose = False
        for a, b, _, lcm_expected in MathLibTest.test_cases_gcd_lcm:
            l = MathLib.lcm(a, b)
            if verbose:
                print(f'lcm({a}, {b}) = {l}')
            self.assertEqual(l, lcm_expected)
        return
    
    test_cases_pow_base_list = [ -177, -2, -1, 0, 2, 5, 71, 1999 ]
    test_cases_pow_exponent_list = [ -4, -1, 0, 2, 5, 35, 197, 2001 ]
    
    def test_pow(self):
        verbose = False
        for exponent in MathLibTest.test_cases_pow_exponent_list:
            for base in MathLibTest.test_cases_pow_base_list:
                self.do_check_pow(base, exponent, pow_function=MathLib.pow, verbose=verbose)
                self.do_check_pow(base, exponent,
                                  pow_function=MathLib.pow_exponentiation_by_squaring,
                                  verbose=verbose)
                self.do_check_pow(base, exponent,
                                  pow_function=MathLib.pow_exponentiation_by_squaring_recursive,
                                  verbose=verbose)
        return
    
    def test_pow_comparison(self):
        verbose = True
        for exponent in MathLibTest.test_cases_pow_exponent_list:
            for base in MathLibTest.test_cases_pow_base_list:
                self.do_check_pow_comparison(base, exponent, verbose=verbose)
        return
    
    # --- Internal Functions
    
    def do_check_pow(self, base, exponent, pow_function=MathLib.pow_exponentiation_by_squaring,
                     verbose=False):
        try:
            result = pow_function(base, exponent)
            expected_result = pow(base, exponent)
            if verbose:
                print(f'pow({base}, {exponent}) = {result}')
            self.assertEqual(expected_result, result)
        except ValueError as e:
            if verbose:
                print(f'error: {e}')
        return
    
    def do_check_pow_comparison(self, base, exponent, verbose=False):
        try:
            result_01 = MathLib.pow_exponentiation_by_squaring(base, exponent)
            result_01_error = False
        except ValueError:
            result_01_error = True
        try:
            result_02 = MathLib.pow_exponentiation_by_squaring_recursive(base, exponent)
            result_02_error = False
        except ValueError:
            result_02_error = True
        self.assertEqual(result_01_error, result_02_error)
        if result_01_error == False and result_02_error == False:
            self.assertEqual(result_01, result_02)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
