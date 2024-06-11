# file: rot13_cipher.py

class Rot13Cipher:

    def __init__(self):
        return

    def encrypt(self, plain_text: str, shift=13) -> str:
        return self.rot13(plain_text, shift=shift)
    
    def decrypt(self, cipher_text: str, shift=13) -> str:
        return self.rot13(cipher_text, shift=-shift)

    def rot13(self, text: str, shift=13) -> str:
        result = ''
        for c in text:
            if c >= 'A' and c <= 'Z':
                diff = (ord(c) - ord('A') + shift) % 26
                result = result + chr(ord('A') + diff)
            elif c >= 'a' and c <= 'z':
                diff = (ord(c) - ord('a') + shift) % 26
                result = result + chr(ord('a') + diff)
            else:
                result = result + c
        return result

# --- end of file --- #
