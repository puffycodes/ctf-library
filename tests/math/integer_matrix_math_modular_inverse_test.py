# file: integer_matrix_math_modular_inverse_test.py

import unittest
import numpy as np
from ctf_library.math.integer_matrix_math import IntegerMatrixMath

class IntegerMatrixMathModularInverseTest(unittest.TestCase):

    test_matrix_data = [
        [[1, 2], [3, 4]],
        [[1, 2], [3, 5]],
        [[1, 1], [1, 1]],
        [[1, 1], [1, 2]],
        [[1, 0], [0, 13]],
        [[1, 1], [2, 13]],
        [[1, 1], [5, 4]],
        [[-1, -2], [-3, -4]],
        [[-3, -2], [-3, -4]],
        [[-3, -2], [-3, -3]],
        [[500, 499], [498, 497]],
        [[500, 499], [497, 497]],
        [[500, 1], [3, 499]],
        [[500, 1], [3, 498]],
        [[500, 1], [2, 499]],
        [[500, 1], [1, 499]],
        [[500, 1], [1, -499]],
    ]

    def test_compute_inverse(self):
        modulo = 26
        error_determinants = []
        for m_data in IntegerMatrixMathModularInverseTest.test_matrix_data:
            m = np.array(m_data, dtype=np.int64)
            m_mod = IntegerMatrixMath.matrix_modulo(m, modulo)
            det = IntegerMatrixMath.matrix_det(m)
            print(f'm:\n{m}')
            print(f'm mod:\n{m_mod}')
            print(f'det: {det}')
            try:
                m_inv = IntegerMatrixMath.matrix_modular_inverse(m, modulo)
                print(f'm inverse:\n{m_inv}')
                mul_1 = IntegerMatrixMath.matrix_modulo(np.matmul(m, m_inv), modulo)
                print(f'm * m_inv:\n{mul_1}')
                mul_2 = IntegerMatrixMath.matrix_modulo(np.matmul(m_mod, m_inv), modulo)
                print(f'm_mod * m_inv:\n{mul_2}')
            except ValueError as e:
                error_determinants.append(det)
                print(f'ValueError: {e}')
            print('=====')
        print(f'list of determinants with error: {error_determinants}')
        print(f'     mod {modulo} -> {[e % modulo for e in error_determinants]}')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
