# file: hill_cipher.py

# Hill Cipher
# Ref: https://en.wikipedia.org/wiki/Hill_cipher

# Matrix Inverse Modulo
# Ref: https://www.andreaminini.net/math/modular-inverse-of-a-matrix
# Ref: https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
# Matrix Inverse and Cofactor
# Ref: https://www.geeksforgeeks.org/compute-the-inverse-of-a-matrix-using-numpy/
# Ref: https://www.geeksforgeeks.org/how-to-find-cofactor-of-a-matrix-using-numpy/
# Adjugate
# Ref: https://stackoverflow.com/questions/51010662/getting-the-adjugate-of-matrix-in-python/75566371#75566371

import numpy as np

class HillCipher:
    
    # Ref: https://www.geeksforgeeks.org/how-to-find-cofactor-of-a-matrix-using-numpy/
    # Ref: https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
    # Ref: https://math.stackexchange.com/questions/2686150/inverse-of-a-modular-matrix
    @staticmethod
    def matrix_modular_inverse(matrix, modulo):
        matrix_cofactor = np.linalg.inv(matrix).transpose() * np.linalg.det(matrix)
        matrix_adjucate = matrix_cofactor.transpose()
        # TODO: There is some rounding issue here?
        matrix_inverse = (matrix_adjucate * pow(int(np.linalg.det(matrix)), -1, modulo)) % modulo
        # TODO: This function needs to return intergers
        return matrix_inverse
    
    # key should be an numpy.array of dimension n x n
    def __init__(self, key, no_match=None):
        if key.shape[0] != key.shape[1]:
            raise ValueError('key dimensions are not the same')
        self.block_length = key.shape[0]
        self.key = key
        self.modulo = 26
        # TODO: This computation of self.key_inv is incorrect
        #self.key_inv = np.linalg.inv(key).astype(np.int64)
        self.key_inv = HillCipher.matrix_modular_inverse(key, self.modulo)
        self.no_match = no_match
        self.pad_value = 0
        return
    
    def encrypt(self, plain_text):
        plain_list = self.string_to_code(plain_text)
        cipher_list = self.process_code_list(self.key, plain_list)
        cipher_text = self.code_to_string(cipher_list, plain_text)
        return cipher_text
    
    def decrypt(self, cipher_text):
        cipher_list = self.string_to_code(cipher_text)
        plain_list = self.process_code_list(self.key_inv, cipher_list)
        plain_text = self.code_to_string(plain_list, cipher_text)
        return plain_text
    
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
                elif cv >= ord('a') and cv < ord('z'):
                    string += chr(ord('a') + code_list[code_ptr])
                    code_ptr += 1
                else:
                    if self.no_match == None:
                        string += c
                    else:
                        string += self.no_match
        return string
    
    def process_code_list(self, key, code_list):
        result_list = []
        for i in range(0, len(code_list), self.block_length):
            current_block = code_list[i:i+self.block_length]
            result_block = self.process_block(key, current_block)
            result_list.extend(result_block)
        return result_list
    
    def process_block(self, key, block):
        temp_block = self.pad_block(block)
        temp_block = (key * temp_block).sum(axis=1)
        for i in range(temp_block.shape[0]):
            temp_block[i] = temp_block[i] % self.modulo
        return list(temp_block)
    
    def pad_block(self, block):
        temp_block = block.copy()
        if len(temp_block) < self.block_length:
            for _ in range(self.block_length):
                temp_block.append(self.pad_value)
            temp_block = temp_block[:self.block_length]
        return temp_block
        
# --- end of file --- #
