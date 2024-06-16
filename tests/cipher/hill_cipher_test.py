# file: hill_cipher_test.py

import unittest
import numpy as np
from ctf_library.cipher.hill_cipher import HillCipher
from ctf_library.math.integer_matrix_math import IntegerMatrixMath

class HillCipherTest(unittest.TestCase):

    key_01 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    key_inv_01 = [[8, 5, 10], [21, 8, 21], [21, 12, 8]]

    key_02 = [[3, 3], [2, 5]]
    key_inv_02 = [[15, 17], [20, 9]]

    key_invalid_11 = [[6, 24, 1], [13, 16, 10]]
    key_invalid_12 = [[1, 1], [1, 1]]

    def test_encryption_01(self):
        # Test cases from https://en.wikipedia.org/wiki/Hill_cipher
        
        key_01 = np.array(HillCipherTest.key_01, dtype=np.int64)
        key_01_inv = np.array(HillCipherTest.key_inv_01, dtype=np.int64)

        self.check_encryption_01(key_01, 'ACT', 'POH', key_inv=key_01_inv)
        self.check_encryption_01(key_01, 'CAT', 'FIN', key_inv=key_01_inv)

        self.check_encryption_01(key_01, 'Cat', 'Fin', key_inv=key_01_inv)
        self.check_encryption_01(key_01, '{CAT}', '{FIN}', key_inv=key_01)

        key_02 = np.array(HillCipherTest.key_02, dtype=np.int64)
        key_02_inv = np.array(HillCipherTest.key_inv_02, dtype=np.int64)

        self.check_encryption_01(key_02, 'HELP', 'HIAT', key_inv=key_02_inv)
        self.check_encryption_01(key_02, 'hElP', 'hIaT', key_inv=key_02_inv)

        key_invalid_11 = np.array(HillCipherTest.key_invalid_11, dtype=np.int64)

        self.check_encryption_01(key_invalid_11, 'ACT', 'POH', key_inv=key_invalid_11)

        key_invalid_12 = np.array(HillCipherTest.key_invalid_12, dtype=np.int64)

        self.check_encryption_01(key_invalid_12, 'ACT', 'POH', key_inv=key_invalid_12)

        return
    
    def check_encryption_01(self, key_data, plain_text, expected_cipher_text, key_inv):
        try:
            key = HillCipher.HillCipherKey(key_data)
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
        modulo = 26
        test_data = [
            [ HillCipherTest.key_01, HillCipherTest.key_inv_01 ],
            [ HillCipherTest.key_02, HillCipherTest.key_inv_02 ],
        ]
        for key_data, key_inv_data in test_data:
            key = np.array(key_data, dtype=np.int64)
            key_inv = np.array(key_inv_data, dtype=np.int64)
            key_computed_inv = IntegerMatrixMath.matrix_modular_inverse(key, modulo)
            diff = key_computed_inv - key_inv
            mul = np.matmul(key, key_computed_inv) % modulo
            print(f'key:\n{key}')
            print(f'key inverse (computed):\n{key_computed_inv}')
            print(f'key inverse (given):\n{key_inv}')
            print(f'diff:\n{diff}')
            print(f'mul:\n{mul}')
            print('=====')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
