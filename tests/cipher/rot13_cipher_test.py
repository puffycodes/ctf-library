# file: rot13_cipher_test.py

import unittest
from ctf_library.cipher.rot13_cipher import Rot13Cipher

class Rot13Test(unittest.TestCase):

    def setUp(self) -> None:
        self.cipher = Rot13Cipher()
        self.plain_text = 'abcdeFGHIJ12345!@#$%'
        super().setUp()
        return

    def test_rot13(self):
        for i in range(26):
            self.check_encrypt_decrpyt(self.plain_text, shift=i)
        return
    
    def test_rot13_02(self):
        for i in range(0, -13, -1):
            self.check_encrypt_decrpyt(self.plain_text, shift=i)
        return
    
    def check_encrypt_decrpyt(self, plain_text, shift):
        enc = self.cipher.encrypt(plain_text, shift=shift)
        dec = self.cipher.decrypt(enc, shift=shift)
        print(f' {shift}: {plain_text} -> {enc} -> {dec}')
        self.assertEqual(dec, plain_text)
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
