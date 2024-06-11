# file: book_cipher.py

# online decoder: https://www.dcode.fr/book-cipher
    
import string

class BookCipher:
    
    def __init__(self, word_list):
        self.word_list = word_list
        return
    
    def encrypt(self, plain_text, whole_word=False):
        return 'not implemented yet'
    
    def decrypt(self, cipher_text, whole_word=False):
        result = []
        for v in cipher_text.split(' '):
            try:
                vv = int(v)
                if whole_word:
                    result.append(self.word_list[vv-1])
                else:
                    result.append(self.word_list[vv-1][0])
            except ValueError:
                if v != '':
                    result.append(v)
        if whole_word:
            result_str = ' '.join(result)
        else:
            result_str = ''.join(result)
        return result_str
        
    @staticmethod
    def create_word_list(book_text, exclude_char=string.punctuation+string.whitespace):
        temp_text = book_text
        for c in exclude_char:
            temp_text = temp_text.replace(c, ' ')
        word_list = [w for w in temp_text.split(' ') if w != '']
        return word_list
    
    @staticmethod
    def create_word_list_from_file(filename, exclude_char=string.punctuation+string.whitespace):
        with open(filename, 'r') as fd:
            book_text = fd.read()
        return BookCipher.create_word_list(book_text, exclude_char=exclude_char)
    
# --- end of file --- #
