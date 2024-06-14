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
        self.verbose = False
        self.test_matrix_inverse = []
        for m_data, m_inv_data in IntegerMatrixMathTestData.inverse_matrix_mod_26:
            m = np.array(m_data, dtype=np.int64)
            m_inv = np.array(m_inv_data, dtype=np.int64)
            self.test_matrix_inverse.append([m, m_inv])
            if self.verbose:
                print(f'matrix:\n{m}')
                print(f'matrix inverse:\n{m_inv}')
                print(f'-----')
        if self.verbose:
            print(f'=====')
        self.test_matrix_cofactor = []
        for m_data, m_cofactor_data in IntegerMatrixMathTestData.cofactor_matrix:
            m = np.array(m_data, dtype=np.int64)
            m_cofactor = np.array(m_cofactor_data, dtype=np.int64)
            self.test_matrix_cofactor.append([m, m_cofactor])
            if self.verbose:
                print(f'matrix:\n{m}')
                print(f'cofactor:\n{m_cofactor}')
                print(f'------')
        if self.verbose:
            print(f'========')
        return

    def test_matrix_multiplication(self):
        for m, m_inv in self.test_matrix_inverse:
            mul = np.matmul(m, m_inv) % 26
            print(f'mul:\n{mul}')
        print(f'=====')
        return
    
    def test_matrix_minor(self):
        for m, _ in self.test_matrix_inverse:
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
    
    def test_matrix_cofactor(self):
        for m, _ in self.test_matrix_inverse:
            print(f'm:\n{m}')
            cofactor = IntegerMatrixMath.matrix_cofactor(m)
            cofactor_ref = IntegerMatrixMath.matrix_cofactor_ref(m)
            diff = cofactor - cofactor_ref
            print(f'cofactor:\n{cofactor}')
            print(f'cofactor ref:\n{cofactor_ref}')
            print(f'diff:\n{diff}')
        return
    
    def test_matrix_modular_inverse(self):
        for m, m_inv in self.test_matrix_inverse:
            print(f'm:\n{m}')
            m_computed_inv = IntegerMatrixMath.matrix_modular_inverse(m, 26)
            diff = m_computed_inv - m_inv
            print(f'inverse:\n{m_inv}')
            print(f'computed inverse:\n{m_computed_inv}')
            print(f'diff:\n{diff}')
        return
    
    # --- These are some tests to check the numpy behaviour
    
    def test_np_array_elements(self):
        array = np.array(
            IntegerMatrixMathTestData.inverse_matrix_mod_26[0][0], dtype=np.int64
        )
        print(f'array:\n{array}')
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                print(f' array[{i}, {j}] = {array[i][j]}')
        return

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
