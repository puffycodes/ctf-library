# file: quagmire_cipher_test.py

import unittest
from ctf_library.cipher.quagmire_cipher import QuagmireCipher

class QuagmireCipherTest(unittest.TestCase):

    # Examples from https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/quagmire

    test_plaintext = 'dontletanyonetellyoutheskyisthelimitwhentherearefootprintsonthemoon'.upper()
    test_keyword_1 = 'PAULBRANDT'
    test_keyword_2 = 'BRANDT'
    test_indicator_keyword = 'BRANDT'
    test_indicator_keyword_2 = 'COUNTRY'

    def setUp(self):
        self.verbose = False
        return

    def test_quagmire_one(self):
        verbose = self.verbose
        original_plaintext = QuagmireCipherTest.test_plaintext
        original_ciphertext = 'HIFUFCIRFKUYKYJPFQSSHZMMQONGKFKTNDQAWDJSKFKVJNHCLIRUCXOWHGUYIDJDUKG'
        
        plain_keyword = QuagmireCipherTest.test_keyword_1
        indicator_keyword = QuagmireCipherTest.test_indicator_keyword
        indicator_position = 'A'
        
        key = QuagmireCipher.quagmire_one_key(plain_keyword, indicator_keyword, indicator_position,
                                              verbose=verbose)
        self.verify(key, original_plaintext, original_ciphertext, verbose=verbose)
        
        return
    
    def test_quagmire_two(self):
        verbose=self.verbose
        original_plaintext = QuagmireCipherTest.test_plaintext
        original_ciphertext = 'RMGXKEVLGUQQNWLJKBKXOFCYGADWYHNIDKHZYELMYHNSLBWEDMHXSXEKOWQQVELKQSJ'
        
        plain_keyword = QuagmireCipherTest.test_keyword_1
        indicator_keyword = QuagmireCipherTest.test_indicator_keyword
        indicator_position = 'C'
        
        key = QuagmireCipher.quagmire_two_key(plain_keyword, indicator_keyword, indicator_position,
                                              verbose=verbose)
        self.verify(key, original_plaintext, original_ciphertext, verbose=verbose)

        return
        
    def test_quagmire_three(self):
        verbose = self.verbose
        original_plaintext = QuagmireCipherTest.test_plaintext
        original_ciphertext = 'FXDIEOGNDBZIIHFCENWDCQMUSLJPJVITJXVKPOFGJVIEFDGOJXQIDHOFCPZIGOFXZPE'
        
        plain_keyword = QuagmireCipherTest.test_keyword_1
        indicator_keyword = QuagmireCipherTest.test_indicator_keyword
        indicator_position = 'P'
        
        key = QuagmireCipher.quagmire_three_key(plain_keyword, indicator_keyword, indicator_position,
                                                verbose=verbose)
        self.verify(key, original_plaintext, original_ciphertext, verbose=verbose)

        return
        
    def test_quagmire_four(self):
        verbose = self.verbose
        original_plaintext = QuagmireCipherTest.test_plaintext
        original_ciphertext = 'KFBIFICEWQVIICOSXRXNCSBLSNMQLNDCSQJLJEKIGIOVDDHIGYFANHMDLHJGKLFXFJG'
        
        plain_keyword = QuagmireCipherTest.test_keyword_1
        cipher_keyword = QuagmireCipherTest.test_keyword_2
        indicator_keyword = QuagmireCipherTest.test_indicator_keyword_2
        indicator_position = 'P'
        
        key = QuagmireCipher.quagmire_four_key(plain_keyword, cipher_keyword,
                                               indicator_keyword, indicator_position, verbose=verbose)
        self.verify(key, original_plaintext, original_ciphertext, verbose=verbose)

        return
        
    def verify(self, key, original_plaintext, original_ciphertext, verbose=False):
        if verbose:
            key.dump()
            
        enc = QuagmireCipher(key)
        ciphertext = enc.encrypt(original_plaintext, verbose=verbose)
        if verbose:
            print(ciphertext)
            print(original_ciphertext)
        self.assertEqual(original_ciphertext, ciphertext)
        
        plaintext = enc.decrypt(ciphertext, verbose=verbose)
        if verbose:
            print(plaintext)
            print(original_plaintext)
        self.assertEqual(original_plaintext, plaintext)
        
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
