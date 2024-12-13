# file: modular_linear_equation_test.py

import unittest
import numpy as np
from ctf_library.math.modular_arithmetic import ModularArithmetic

class ModularLinearEquationTest(unittest.TestCase):

    def test_mod_solve_linear_equation(self):
        verbose = True
        debug = False
        test_cases = [
            [ [[3, 2]], 5 ],
            [ [[3, 5, 2], [1, 2, 3]], 5 ],
            [ [[2, 7, 2], [5, 3, 6]], 11 ],
            [ [[3, 1, 2], [6, 3, 4]], 17 ],
            [ [[3, 3, 5, 2], [3, 5, 2, 1], [4, 5, 3, 6]], 17 ],
            [ [[3, 3, 5, 2], [3, 5, 2, 1], [4, 5, 3, 6]], 23 ],
            [ [[3, 1, 3, 2], [6, 3, 2, 4], [6, 3, 6, 5]], 17 ],
            [ [[3, 1, 3, 0], [6, 3, 2, 0], [6, 3, 6, 0]], 17 ],
            [ [[3, 1, 3, 1], [6, 3, 2, 1], [6, 3, 6, 1]], 17 ],
            [ [[3, 12, 5, 7, 2], [3, 5, 2, 16, 1], [4, 5, 3, 5, 6], [15, 21, 3, 15, 16]], 23 ],
            [ [[3, 12, 5, 7, 2], [3, 5, 2, 16, 1], [4, 5, 3, 5, 6], [15, 21, 3, 15, 16]], 71 ],
            # Value out of range but have solutions
            [ [[3, 8]], 5 ],
            [ [[3, 10, 2], [1, 2, 13]], 5 ],
            # Error / No solution
            [ [[3, 1, 2], [6, 2, 4]], 17 ],
            [ [[3, 1, 3, 2], [6, 3, 2, 4], [6, 2, 6, 5]], 17 ],
            [ [[3, 1, 3, 2], [6, 3, 2, 4], [6, 2, 6, 5]], 29 ],
        ]
        for m, modulo in test_cases:
            m_np = np.array(m)
            if verbose:
                print(f'input: {m = }; {modulo = }')
                print(f'm (np array) =\n{m_np}')
            try:
                result = ModularArithmetic.mod_solve_linear_equation(m_np, modulo, verbose=debug)
                if verbose:
                    print(f'result =\n{result}')
                self.do_check_result(m_np, result, modulo, verbose=verbose)
            except ValueError as e:
                if verbose:
                    print(f'error: {e}')
            if verbose:
                print()
        return

    def do_check_result(self, m, result, modulo, verbose=False):
        n_row, n_col = m.shape
        if verbose:
            print(f'matrix shape = {n_row}, {n_col}')
        for row in range(n_row):
            sum = 0
            for col in range(n_col-1):
                sum += m[row][col] * result[col][n_col-1]
            sum = int(sum % modulo)
            expected_sum = m[row][n_col-1] % modulo
            if verbose:
                print(f' row {row}: {sum=}; expected={expected_sum}')
            # check result
            for col in range(n_col-1):
                self.assertLess(result[col][n_col-1], modulo)
            self.assertEqual(expected_sum, sum)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
