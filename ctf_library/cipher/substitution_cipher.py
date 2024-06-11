# file: substitution_cipher.py

import string

class SubstitutionCipher:
    
    upper_case_only = 1
    lower_case_only = 2
    both_cases = 3
    
    class SubstitutionCipherKey:
        def __init__(self, plain, cipher):
            self.plain = plain
            self.cipher = cipher
            return

    @staticmethod
    def key(plain, cipher):
        return SubstitutionCipher.SubstitutionCipherKey(plain, cipher)
    
    @staticmethod
    def caesar_cipher_key(alphabets, shift):
        cipher = alphabets[shift:] + alphabets[:shift]
        return SubstitutionCipher.SubstitutionCipherKey(alphabets, cipher)
    
    @staticmethod
    def key_from_keyword(keyword, char_set=lower_case_only):
        keyword_tmp = keyword.lower()
        plain = string.ascii_lowercase
        cipher_part_1 = ''
        cipher_part_2 = string.ascii_lowercase
        
        for c in keyword_tmp:
            if c < 'a' or c > 'z':
                continue
            if c not in cipher_part_1:
                cipher_part_1 += c
            cipher_part_2 = cipher_part_2.replace(c, '')
        cipher = cipher_part_1 + cipher_part_2
        
        if char_set == SubstitutionCipher.lower_case_only:
            pass
        elif char_set == SubstitutionCipher.upper_case_only:
            plain = plain.upper()
            cipher = cipher.upper()
        elif char_set == SubstitutionCipher.both_cases:
            plain = plain + plain.upper()
            cipher = cipher + cipher.upper()
        else:
            raise ValueError('invalid char_set value %d' % (char_set))
            
        return SubstitutionCipher.SubstitutionCipherKey(plain, cipher)
    
    def __init__(self, key, no_match=None):
        self.key = key
        self.no_match = no_match
        return
    
    def encrypt(self, plain_text):
        return self.substitute(plain_text, self.key.plain, self.key.cipher, no_match=self.no_match)
    
    def decrypt(self, cipher_text):
        return self.substitute(cipher_text, self.key.cipher, self.key.plain, no_match=self.no_match)
    
    def substitute(self, text, src_key, dest_key, no_match=None):
        result_string = ''
        for c in text:
            if c in src_key:
                c_sub = dest_key[src_key.index(c)]
            else:
                if no_match == None:
                    c_sub = c
                else:
                    c_sub = no_match
            result_string += c_sub
        return result_string

# --- end of file --- #
