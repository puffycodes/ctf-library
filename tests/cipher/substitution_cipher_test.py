# file: substitution_cipher_test.py

import unittest
import string
from ctf_library.cipher.substitution_cipher import SubstitutionCipher

class SubstitutionCipherTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.key_text_list = [
            'Hello World',
            'Hello World!@#$',
            'hello world',
            'Caesar The Great',
            'The quick brown fox jumps over the lazy dog.',
        ]
        self.plain_text_list = [
            'The quick brown fox jumps over the lazy dog.',
            'Too many symbols !@#$%^&** and numbers 1234567890 is not good.',
            string.printable,
        ]
        super().setUp()
        return

    def test_substitution(self):
        cipher_list = [self.create_cipher_from_key(key) for key in self.key_text_list]
        for cipher in cipher_list:
            for plain_text in self.plain_text_list:
                self.check_encrypt_decrypt(cipher, plain_text)
        return
    
    def test_substitution_upper_case(self):
        cipher_list = [
            self.create_cipher_from_key(key, char_set=SubstitutionCipher.upper_case_only) \
                for key in self.key_text_list
        ]
        for cipher in cipher_list:
            for plain_text in self.plain_text_list:
                self.check_encrypt_decrypt(cipher, plain_text.upper())
        return
    
    def test_substitution_lower_case(self):
        cipher_list = [
            self.create_cipher_from_key(key, char_set=SubstitutionCipher.lower_case_only) \
                for key in self.key_text_list
        ]
        for cipher in cipher_list:
            for plain_text in self.plain_text_list:
                self.check_encrypt_decrypt(cipher, plain_text.lower())
        return
    
    def create_cipher_from_key(self, key_text, char_set=SubstitutionCipher.both_cases):
        key = SubstitutionCipher.key_from_keyword(key_text, char_set=char_set)
        cipher = SubstitutionCipher(key)
        return cipher
    
    def check_encrypt_decrypt(self, cipher, plain_text):
        enc = cipher.encrypt(plain_text)
        dec = cipher.decrypt(enc)
        print(f' {plain_text} -> {enc} -> {dec}')
        self.assertEqual(dec, plain_text)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
