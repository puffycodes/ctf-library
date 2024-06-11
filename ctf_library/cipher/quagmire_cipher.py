# file: quagmire_cipher.py

# Ref: https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/quagmire

import string

class QuagmireCipher:

    upper_case = string.ascii_uppercase
    
    class QuagmireCipherKey:
        def __init__(self, plain, cipher, indicator_keyword, indicator_position, verbose=False):
            self.plain = plain
            self.cipher = cipher
            self.indicator_keyword = indicator_keyword
            self.indicator_position = indicator_position
            self.init_keys(verbose=verbose)
            return
        
        def init_keys(self, verbose=False):
            self.cipher_strings = []
            offset = self.plain.index(self.indicator_position[0])
            if verbose:
                print('offset: %2d %s' % (offset, self.plain))
            for c in self.indicator_keyword:
                curr_index = self.cipher.index(c)
                curr_cipher = self.cipher[curr_index:] + self.cipher[:curr_index]
                curr_cipher_2 = curr_cipher[-offset:] + curr_cipher[:-offset]
                self.cipher_strings.append(curr_cipher_2)
                if verbose:
                    print('index:  %2d %s' % (curr_index, curr_cipher_2))
            self.count = len(self.cipher_strings)
            return
        
        def dump(self):
            print('I:', self.indicator_keyword, self.indicator_position, self.count)
            print('P:', self.plain)
            for s in self.cipher_strings:
                print('C:', s)
            return
        
    # Key generation helper functions
    
    @staticmethod
    def keyed_alphabet(key):
        key = key.upper()
        keyed_string = ''
        for c in key:
            if c not in keyed_string:
                keyed_string += c
        for c in QuagmireCipher.upper_case:
            if c not in keyed_string:
                keyed_string += c
        return keyed_string
    
    # Key generation functions for Quagmire 1 to 4
    
    @staticmethod
    def quagmire_one_key(key, indicator_keyword, indicator_position, verbose=False):
        keyed_plain = QuagmireCipher.keyed_alphabet(key)
        key = QuagmireCipher.QuagmireCipherKey(keyed_plain, string.ascii_uppercase,
                                               indicator_keyword, indicator_position, verbose=verbose)
        return key
    
    @staticmethod
    def quagmire_two_key(key, indicator_keyword, indicator_position, verbose=False):
        keyed_cipher = QuagmireCipher.keyed_alphabet(key)
        key = QuagmireCipher.QuagmireCipherKey(string.ascii_uppercase, keyed_cipher,
                                               indicator_keyword, indicator_position, verbose=verbose)
        return key
    
    @staticmethod
    def quagmire_three_key(key, indicator_keyword, indicator_position, verbose=False):
        keyed_plain = QuagmireCipher.keyed_alphabet(key)
        keyed_cipher = QuagmireCipher.keyed_alphabet(key)
        key = QuagmireCipher.QuagmireCipherKey(keyed_plain, keyed_cipher,
                                               indicator_keyword, indicator_position, verbose=verbose)
        return key
    
    @staticmethod
    def quagmire_four_key(key1, key2, indicator_keyword, indicator_position, verbose=False):
        keyed_plain = QuagmireCipher.keyed_alphabet(key1)
        keyed_cipher = QuagmireCipher.keyed_alphabet(key2)
        key = QuagmireCipher.QuagmireCipherKey(keyed_plain, keyed_cipher,
                                               indicator_keyword, indicator_position, verbose=verbose)
        return key
    
    # Quagmire encryption and decryption
    
    def __init__(self, key):
        self.key = key
        return

    def encrypt(self, plaintext, verbose=False):
        ciphertext = ''
        for i in range(len(plaintext)):
            ci = i % self.key.count
            pc = plaintext[i]
            pi = self.key.plain.index(pc)
            cc = self.key.cipher_strings[ci][pi]
            ciphertext += cc
            if verbose:
                print(ci, pc, pi, cc)
        return ciphertext
    
    def decrypt(self, ciphertext, verbose=False):
        plaintext = ''
        for i in range(len(ciphertext)):
            ci = i % self.key.count
            cc = ciphertext[i]
            pi = self.key.cipher_strings[ci].index(cc)
            pc = self.key.plain[pi]
            plaintext += pc
            if verbose:
                print(ci, cc, pi, pc)
        return plaintext
        
# --- end of file --- #