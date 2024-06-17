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

    key_code_str_list = [
        ['GYBNQKURP', 3],
        ['GybnQKUrp', 3],
        ['ABCDEFGHI', 3],
        ['ABCDEFGHJ', 3],
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
    
    def test_key_generation_01(self):
        print(f'Key Generation Test 01:')
        test_data = HillCipherTest.valid_matrix_data
        for matrix_data, _ in test_data:
            matrix = np.array(matrix_data)
            print(f'source matrix:\n{matrix}')
            try:
                key = HillCipher.key(matrix)
                print(f'encryption matrix:\n{key.encryption_matrix}')
                print(f'decryption matrix:\n{key.decryption_matrix}')
                self.check_encryption_02(key)
            except ValueError as e:
                print(f'ValueError: {e}')
        return
    
    def test_key_generation_02(self):
        print(f'Key Generation Test 02:')
        for key_string, block_size in HillCipherTest.key_code_str_list:
            print(f'source key string: {key_string}')
            try:
                key = HillCipher.key_from_string(key_string, block_size)
                print(f'encryption matrix:\n{key.encryption_matrix}')
                print(f'decryption matrix:\n{key.decryption_matrix}')
                self.check_encryption_02(key)
            except ValueError as e:
                print(f'ValueError: {e}')
            print('=====^^^===')
        return
    
    def check_encryption_02(self, key):
        plain_text = 'The quick brown fox JUMPS over the laZy dog.'
        cipher = HillCipher(key)
        plain_text = cipher.pad_text(plain_text)
        cipher_text = cipher.encrypt(plain_text)
        deciphered_text = cipher.decrypt(cipher_text)
        print(f'{plain_text} -> {cipher_text} -> {deciphered_text}')
        self.assertEqual(deciphered_text, plain_text)
        return
    
    def test_padding(self):
        matrix_array = np.array(HillCipherTest.matrix_01_data, dtype=np.int64)
        key = HillCipher.HillCipherKey(matrix_array)
        cipher = HillCipher(key)
        for i in range(20):
            text = 'b' * i
            padded_text = cipher.pad_text(text)
            unpadded_text = cipher.unpad_text(padded_text)
            print(f'padding: {text} -> {padded_text} -> {unpadded_text}')
            self.assertEqual(unpadded_text, text)
        text_without_pad_list = [
            'abcde', 'abcde=fghij', 'abcde=-asdff-='
        ]
        for text in text_without_pad_list:
            unpadded_text = cipher.unpad_text(text)
            print(f'unpadding: {text} -> {unpadded_text}')
            self.assertEqual(text, unpadded_text)
        return
    
    def test_key_inverse(self):
        modulo = HillCipherTest.modulo
        test_data = HillCipherTest.valid_matrix_data
        for matrix_data, matrix_inv_data in test_data:
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
