# file: hill_cipher_test.py

import unittest
import numpy as np
from ctf_library.cipher.hill_cipher import HillCipher
from ctf_library.math.integer_matrix_math import IntegerMatrixMath

class HillCipherTest(unittest.TestCase):

    matrix_01_data = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    matrix_01_inv_data = [[8, 5, 10], [21, 8, 21], [21, 12, 8]]

    matrix_02_data = [[3, 3], [2, 5]]
    matrix_02_inv_data = [[15, 17], [20, 9]]

    matrix_invalid_11 = [[6, 24, 1], [13, 16, 10]]
    matrix_invalid_12 = [[1, 1], [1, 1]]

    modulo = 26
    valid_matrix_data = [
        [ matrix_01_data, matrix_01_inv_data ],
        [ matrix_02_data, matrix_02_inv_data ],
    ]
    
    def test_encryption_01(self):
        # Test cases from https://en.wikipedia.org/wiki/Hill_cipher
        
        key_01_array = np.array(HillCipherTest.matrix_01_data, dtype=np.int64)

        self.check_encryption_01(key_01_array, 'ACT', 'POH')
        self.check_encryption_01(key_01_array, 'CAT', 'FIN')

        self.check_encryption_01(key_01_array, 'Cat', 'Fin')
        self.check_encryption_01(key_01_array, '{CAT}', '{FIN}')
        self.check_encryption_01(
            key_01_array, 'The Quick Brown Fox Jumps.', 'Ajn Mkato Rspye Zjk Tdiel.',
        )

        key_02_array = np.array(HillCipherTest.matrix_02_data, dtype=np.int64)

        self.check_encryption_01(key_02_array, 'HELP', 'HIAT')
        self.check_encryption_01(key_02_array, 'hElP', 'hIaT')

        # Test cases for invalid encryption matrix

        key_invalid_11_array = np.array(HillCipherTest.matrix_invalid_11, dtype=np.int64)

        self.check_encryption_01(key_invalid_11_array, 'ACT', 'POH')

        key_invalid_12_array = np.array(HillCipherTest.matrix_invalid_12, dtype=np.int64)

        self.check_encryption_01(key_invalid_12_array, 'ACT', 'POH')

        return
    
    def check_encryption_01(self, key_array, plain_text, expected_cipher_text):
        try:
            key = HillCipher.HillCipherKey(key_array)
        except ValueError as e:
            print(f'ValueError: {e}')
            print('=====***==')
            return
        
        cipher = HillCipher(key)
        print(f'encryption matrix:\n{cipher.key.encryption_matrix}')
        print(f'decryption matrix:\n{cipher.key.decryption_matrix}')
        print('-----')

        cipher_text = cipher.encrypt(plain_text)
        decrypted_text = cipher.decrypt(cipher_text)
        print(f'Result: {plain_text} -> {cipher_text} -> {decrypted_text}')
        self.assertEqual(cipher_text, expected_cipher_text)
        self.assertEqual(decrypted_text, plain_text)
        print('=====*****')

        return
    
    def test_key_inverse(self):
        modulo = HillCipherTest.modulo
        valid_matrix_data = HillCipherTest.valid_matrix_data
        for matrix_data, matrix_inv_data in valid_matrix_data:
            matrix = np.array(matrix_data, dtype=np.int64)
            matrix_inv = np.array(matrix_inv_data, dtype=np.int64)
            matrix_computed_inv = IntegerMatrixMath.matrix_modular_inverse(matrix, modulo)
            diff = matrix_computed_inv - matrix_inv
            mul = np.matmul(matrix, matrix_computed_inv) % modulo
            print(f'matrix:\n{matrix}')
            print(f'matrix inverse (computed) (should equal to given):\n{matrix_computed_inv}')
            print(f'matrix inverse (given):\n{matrix_inv}')
            print(f'diff (should be zero):\n{diff}')
            print(f'mul (should be identity matrix):\n{mul}')
            print('=====')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
