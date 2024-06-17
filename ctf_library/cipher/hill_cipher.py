# file: hill_cipher.py

# Hill Cipher
# Ref: https://en.wikipedia.org/wiki/Hill_cipher

import numpy as np
import string
from ctf_library.math.integer_matrix_math import IntegerMatrixMath

class HillCipher:

    class HillCipherKey:

        # encryption matrix should be an numpy.array of dimension n x n
        def __init__(self, encryption_matrix):
            self.valid = False
            self.encryption_matrix = encryption_matrix
            self.modulo = 26
            row = self.encryption_matrix.shape[0]
            col = self.encryption_matrix.shape[1]
            if row != col:
                raise ValueError(f'Encryption matrix dimensions are not the same: {row} != {col}')
            self.block_length = row
            # The next call may raise ValueError if the inverse does not exist.
            self.decryption_matrix = IntegerMatrixMath.matrix_modular_inverse(
                self.encryption_matrix, self.modulo
            )
            self.valid = True
            return
        
    @staticmethod
    def key(encryption_matrix):
        return HillCipher.HillCipherKey(encryption_matrix)
    
    @staticmethod
    def key_from_string(key_code_str, block_size):
        key_code_len = len(key_code_str)
        required_len = block_size * block_size
        if key_code_len < required_len:
            raise ValueError(
                f'Insufficient length for key code.'
                f' Needs {required_len} but only gets {key_code_len}.'
            )
        key_code_list = []
        for c in key_code_str:
            c_code = HillCipher.key_code(c)
            if c_code != -1:
                key_code_list.append(c_code)
        key_code_list_len = len(key_code_list)
        if key_code_list_len < required_len:
            raise ValueError(
                f'Insufficient length for key code.'
                f' Needs {required_len} but only gets {key_code_list_len}.'
            )
        key_array = np.array([key_code_list[:required_len]], dtype=np.int64).reshape(
            (block_size, block_size)
        )
        key = HillCipher.HillCipherKey(key_array)
        return key
    
    @staticmethod
    def key_code(c):
        result = -1
        if c >= 'A' and c <= 'Z':
            result = ord(c) - ord('A')
        elif c >= 'a' and c <= 'z':
            result = ord(c) - ord('a')
        else:
            pass
        return result
    
    def __init__(self, key, no_match=None, pad_value=0, pad_separator='=-='):
        self.key = key
        self.no_match = no_match
        self.pad_value = pad_value
        self.pad_separator = pad_separator
        return
    
    def encrypt(self, plain_text):
        if not self.key.valid:
            raise ValueError(f'Key is not valid.')
        plain_list = self.string_to_code(plain_text)
        cipher_list = self.process_code_list(self.key.encryption_matrix, plain_list)
        cipher_text = self.code_to_string(cipher_list, plain_text)
        return cipher_text
    
    def decrypt(self, cipher_text):
        if not self.key.valid:
            raise ValueError(f'Key is not valid.')
        cipher_list = self.string_to_code(cipher_text)
        plain_list = self.process_code_list(self.key.decryption_matrix, cipher_list)
        plain_text = self.code_to_string(plain_list, cipher_text)
        return plain_text
    
    def pad_text(self, text):
        count = 0
        for c in text:
            if c in string.ascii_letters:
                count += 1
        pad_count = (self.key.block_length - (count % self.key.block_length))
        if pad_count == self.key.block_length:
            pad_text = ''
        else:
            pad_text = self.pad_separator + ''.join(['a' for i in range(pad_count)])
        return text + pad_text
    
    def unpad_text(self, text):
        parts = text.split(self.pad_separator)
        if len(parts) == 1:
            # original text has no padding
            result = parts[0]
        else:
            result = self.pad_separator.join(parts[:-1])
        return result
    
    def string_to_code(self, text):
        code_list = []
        for c in text:
            cv = ord(c)
            if cv >= ord('A') and cv <= ord('Z'):
                code_list.append(cv - ord('A'))
            elif cv >= ord('a') and cv <= ord('z'):
                code_list.append(cv - ord('a'))
            else:
                pass
        return code_list
    
    def code_to_string(self, code_list, template):
        string = ''
        code_ptr = 0
        for c in template:
            if code_ptr >= len(code_list):
                string += c
            else:
                cv = ord(c)
                if cv >= ord('A') and cv <= ord('Z'):
                    string += chr(ord('A') + code_list[code_ptr])
                    code_ptr += 1
                elif cv >= ord('a') and cv <= ord('z'):
                    string += chr(ord('a') + code_list[code_ptr])
                    code_ptr += 1
                else:
                    if self.no_match == None:
                        string += c
                    else:
                        string += self.no_match
        return string
    
    def process_code_list(self, matrix, code_list):
        result_list = []
        for i in range(0, len(code_list), self.key.block_length):
            current_block = code_list[i:i+self.key.block_length]
            result_block = self.process_block(matrix, current_block)
            result_list.extend(result_block)
        return result_list
    
    def process_block(self, matrix, block):
        temp_block = self.pad_block(block)
        temp_block = (matrix * temp_block).sum(axis=1)
        for i in range(temp_block.shape[0]):
            temp_block[i] = temp_block[i] % self.key.modulo
        return list(temp_block)
    
    def pad_block(self, block):
        temp_block = block.copy()
        if len(temp_block) < self.key.block_length:
            for _ in range(self.key.block_length):
                temp_block.append(self.pad_value)
            temp_block = temp_block[:self.key.block_length]
        return temp_block
        
# --- end of file --- #
