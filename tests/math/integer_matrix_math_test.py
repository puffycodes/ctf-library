# file: integer_matrix_math_test.py

import unittest
import numpy as np
from ctf_library.math.integer_matrix_math import IntegerMatrixMath

class IntegerMatrixMathTestData:
    
    inverse_matrix_mod_26 = [
        # Test cases from https://en.wikipedia.org/wiki/Hill_cipher
        [ [[6, 24, 1], [13, 16, 10], [20, 17, 15]], [[8, 5, 10], [21, 8, 21], [21, 12, 8]] ],
        [ [[3, 3], [2, 5]], [[15, 17], [20, 9]] ],
    ]

    cofactor_matrix = [
        # Test cases from https://stackoverflow.com/questions/6527641/speed-up-python-code-for-computing-matrix-cofactors
        [ [[1, 2, 0], [0,3, 0], [0, 7, 1]], [[3, 0, 0], [-2, 1, -7], [0, 0, 3]] ]
    ]

class IntegerMatrixMathTest(unittest.TestCase):

    def setUp(self):
        self.test_matrix = []
        for m_data, m_inv_data in IntegerMatrixMathTestData.inverse_matrix_mod_26:
            m = np.array(m_data, dtype=np.int64)
            m_inv = np.array(m_inv_data, dtype=np.int64)
            self.test_matrix.append([m, m_inv])
            print(f'matrix:\n{m}')
            print(f'matrix inverse:\n{m_inv}')
            print(f'-----')
        print(f'=====')
        return

    def test_matrix_multiplication(self):
        for m, m_inv in self.test_matrix:
            mul = np.matmul(m, m_inv) % 26
            print(f'mul:\n{mul}')
        print(f'=====')
        return
    
    def test_matrix_minor(self):
        for m, _ in self.test_matrix:
            print(f'm:\n{m}')
            for i in range(m.shape[0]):
                for j in range(m.shape[1]):
                    m_minor = IntegerMatrixMath.matrix_minor(m, i, j)
                    m_minor_det = np.linalg.det(m_minor)
                    m_minor_det_int = round(m_minor_det)
                    print(f'matrix_minor({i}, {j}):\n{m_minor}')
                    print(f'det(matrix_minor): {m_minor_det} ({m_minor_det_int})')
            print('-----')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
