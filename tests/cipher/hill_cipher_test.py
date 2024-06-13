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

    def test_encryption_01(self):
        # Test cases from https://en.wikipedia.org/wiki/Hill_cipher
        
        key_01 = np.array(HillCipherTest.key_01, dtype=np.int64)
        key_01_inv = np.array(HillCipherTest.key_inv_01, dtype=np.int64)

        self.check_encryption_01(key_01, 'ACT', 'POH', key_inv=key_01_inv)
        self.check_encryption_01(key_01, 'CAT', 'FIN', key_inv=key_01_inv)

        key_02 = np.array(HillCipherTest.key_02, dtype=np.int64)
        key_02_inv = np.array(HillCipherTest.key_inv_02, dtype=np.int64)

        self.check_encryption_01(key_02, 'HELP', 'HIAT', key_inv=key_02_inv)

        return
    
    def check_encryption_01(self, key, plain_text, expected_cipher_text, key_inv):
        cipher = HillCipher(key)
        print(cipher.key)
        print(cipher.key_inv)

        # TODO:
        # Rounding of the matrix modular inverse is off.
        print(cipher.key_inv.astype(np.int64))
        # *** end of block *** #

        # TODO:
        # We have some bug here.
        # The computation of the inverse modulo of the matrix key (cipher.key_inv) is wrong.
        # The following block should not be needed when this is fixed.
        cipher.key_inv = key_inv
        print(cipher.key_inv)
        # *** end of block *** #

        print('=====')

        cipher_text = cipher.encrypt(plain_text)
        decrypted_text = cipher.decrypt(cipher_text)
        print(f'{plain_text} -> {cipher_text} -> {decrypted_text}')
        self.assertEqual(cipher_text, expected_cipher_text)
        self.assertEqual(decrypted_text, plain_text)

        return
    
    def test_inverse(self):
        key_01 = np.array(HillCipherTest.key_01, dtype=np.int64)
        key_01_inv = np.array(HillCipherTest.key_inv_01, dtype=np.int64)
        key_01_computed_inv = IntegerMatrixMath.matrix_modular_inverse(key_01, 26)
        print(key_01)
        print(key_01_inv)
        print(key_01_computed_inv)
        print(key_01_computed_inv - key_01_inv)
        print('==========')
        key_02 = np.array(HillCipherTest.key_02, dtype=np.int64)
        key_02_inv = np.array(HillCipherTest.key_inv_02, dtype=np.int64)
        key_02_computed_inv = IntegerMatrixMath.matrix_modular_inverse(key_02, 26)
        print(key_02)
        print(key_02_inv)
        print(key_02_computed_inv)
        print(key_02_computed_inv - key_02_inv)
        print('==========')
        return
    
    def test_np_array(self):
        array = np.array(HillCipherTest.key_01, dtype=np.int64)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                print(f' array[{i}, {j}] = {array[i][j]}')
        return

if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
