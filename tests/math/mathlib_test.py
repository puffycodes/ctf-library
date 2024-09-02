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
            self.do_check_gcd_all_methods(a, b, gcd_expected, verbose=verbose)
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
    
    # [ <n>, <expected isqrt(n) value> ]
    test_cases_isqrt = [
        [ 0, 0 ], [ 1, 1 ], [ 2, 1 ], [ 3, 1 ], [ 4, 2 ], [ 5, 2 ], [ 6, 2 ],
        [ 9, 3 ], [ 10, 3 ], [ 11, 3 ], [ 24, 4 ], [ 25, 5 ], [ 26, 5 ],
        [ 4294836225, 65535 ], [ 4294836227, 65535 ],
        [ 60493815061729, 7777777 ], [ 60493815061731, 7777777 ],
    ]
    
    def test_isqrt_01(self):
        verbose = False
        for n, expected_value in MathLibTest.test_cases_isqrt:
            self.do_check_isqrt_all_methods(
                n, expected_value=expected_value, verbose=verbose
            )
        return
    
    def test_isqrt_02(self):
        verbose = False
        for n in range(-100, 0):
            with self.assertRaises(ValueError):
                result = MathLib.isqrt_newtons_method(n)
            with self.assertRaises(ValueError):
                result = MathLib.isqrt_newtons_method_faster(n)
            with self.assertRaises(ValueError):
                result = MathLib.isqrt_newtons_method_faster_02(n)
            with self.assertRaises(ValueError):
                result = MathLib.isqrt_hybrid(n)
        return
    
    def test_isqrt_03(self):
        verbose = False
        for n in range(65536):
            self.do_check_isqrt_all_methods(n, verbose=verbose)
        for n in range(0, 1 << 512, 1 << 500):
            self.do_check_isqrt_all_methods(n, verbose=verbose)
        return
    
    # --- Internal Functions
    
    def do_check_gcd_all_methods(self, a, b, expected_value, verbose=False):
        g = MathLib.gcd(a, b)
        g_e1 = MathLib.gcd_euclidean(a, b)
        g_e2 = MathLib.gcd_euclidean_recursive(a, b)
        if verbose:
            print(f'gcd({a}, {b}) = {g}')
        self.assertEqual(g, abs(expected_value))
        self.assertEqual(g_e1, expected_value)
        self.assertEqual(g_e2, expected_value)
        for value in [ g, g_e1, g_e2 ]:
            if value != 0:
                self.assertEqual(a % value, 0)
                self.assertEqual(b % value, 0)
        return
    
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
    
    def do_check_isqrt_all_methods(self, n, expected_value=-1, verbose=False):
        result_01 = MathLib.isqrt_newtons_method(n)
        result_02 = MathLib.isqrt_newtons_method_faster(n)
        result_03 = MathLib.isqrt_newtons_method_faster_02(n)
        result_04 = MathLib.isqrt_hybrid(n)
        if verbose:
            print(f'isqrt({n}) = {result_01}, {result_02}, {result_03}, {result_04}')
        if expected_value >= 0:
            self.assertEqual(expected_value, result_01)
            self.assertEqual(expected_value, result_02)
            self.assertEqual(expected_value, result_03)
            self.assertEqual(expected_value, result_04)
        self.assertEqual(result_01, result_02)
        self.assertEqual(result_01, result_03)
        self.assertEqual(result_01, result_04)
        self.assertEqual(result_02, result_03)
        self.assertEqual(result_02, result_04)
        self.assertEqual(result_03, result_04)
        self.do_check_isqrt_correctness(n, result_01)
        self.do_check_isqrt_correctness(n, result_02)
        self.do_check_isqrt_correctness(n, result_03)
        self.do_check_isqrt_correctness(n, result_04)
        return

    def do_check_isqrt_correctness(self, n, isqrt_n):
        square_1 = isqrt_n * isqrt_n
        square_2 = (isqrt_n + 1) * (isqrt_n + 1)
        self.assertLessEqual(square_1, n)
        self.assertGreater(square_2, n)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
