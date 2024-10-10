# file: chinese_remainder_theorem.py

import unittest
from ctf_library.math.chinese_remainder_theorem import ChineseRemainderTheorem

class ChineseRemainderTheoremTest(unittest.TestCase):

    error_result_marker = [ -1, -1 ]

    # [ coef_list, expected_result ]
    test_cases = [
        # Test cases from https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        [ [ (2, 3), (3, 5), (2, 7) ], [ 23, 105 ] ],
        [ [ (0, 3), (3, 4), (4, 5) ], [ 39, 60 ] ],
        # Test cases from https://www.math.cmu.edu/~mradclif/teaching/127S19/Notes/ChineseRemainderTheorem.pdf
        [ [ (2, 5), (3, 7), (10, 11) ], [ 87, 385 ] ],
        [ [ (3, 4), (0, 6) ], error_result_marker ],
        [ [ (3, 7), (3, 5), (4, 12) ], [ 388, 420 ] ],
        [ [ (6, 7), (4, 8) ], [ 20, 56 ] ],
        # Test cases from https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
        [ [ (2, 5), (3, 7) ], [ 17, 35] ],
        # Boundary test cases
        [ [], [] ],
        # Error test cases
        [ [ (2, 4), (2, 2) ], error_result_marker ],
    ]

    # not implemented yet (TODO)
    test_cases_extended = [
        # Test cases from https://www.math.cmu.edu/~mradclif/teaching/127S19/Notes/ChineseRemainderTheorem.pdf
        [ [ (2, 5, 7), (3, 4, 8) ], [ (6, 7), (4, 8) ], [ 20, 56 ] ],
        [
            [ (2, 6, 14), (3, 9, 15), (5, 20, 60) ],
            [ (3, 7), (3, 5), (4, 12) ],
            [ 388, 420 ]
        ],
    ]

    def test_solve(self):
        verbose = False
        for coef_list, expected_result in ChineseRemainderTheoremTest.test_cases:
            try:
                result = ChineseRemainderTheorem.solve(coef_list)
                if verbose:
                    print(f'coef_list: {coef_list}')
                    print(f'result: {result}')
                    print(f'expected result: {expected_result}')
                self.assertEqual(expected_result, result)
            except ValueError as e:
                if verbose:
                    print(f'coef_list: {coef_list}')
                    print(f'error: {e}')
                # verified that this is an error test case
                self.assertEqual(expected_result, ChineseRemainderTheoremTest.error_result_marker)
        return
    
    def test_solve_extended(self):
        verbose = False
        for coef_list, _, expected_result in ChineseRemainderTheoremTest.test_cases_extended:
            try:
                result = ChineseRemainderTheorem.solve_extended(coef_list)
                if verbose:
                    print(f'coef_list: {coef_list}')
                    print(f'result: {result}')
                    print(f'expected result: {expected_result}')
                self.assertEqual(expected_result, result)
            except ValueError as e:
                if verbose:
                    print(f'coef_list: {coef_list}')
                    print(f'error: {e}')
                # verified that this is an error test case
                self.assertEqual(expected_result, ChineseRemainderTheoremTest.error_result_marker)
        return
    
    def test_reduce(self):
        verbose = False
        for coef_list, coef_list_2, _ in ChineseRemainderTheoremTest.test_cases_extended:
            for coef, coef_2 in zip(coef_list, coef_list_2):
                m, a, n = coef
                a_prime_exp, n_prime_exp = coef_2
                a_prime, n_prime = ChineseRemainderTheorem.reduce(coef, verbose=verbose)
                if verbose:
                    print(f'({m}, {a}, {n}) -> ({a_prime}, {n_prime}) expect ({a_prime_exp}, {n_prime_exp})')
                self.assertEqual((a_prime, n_prime), coef_2)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
