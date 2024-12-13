# file: hash_search.py

from hashlib import sha256
import string
import itertools

class HashSearch:

    '''
    A collection of some of the hash search challenges from various CTF.
    '''

    printable_characters = string.ascii_letters + string.digits + string.punctuation

    # Challenge for Hack The Vote 2024:
    #   Give me input where sha256(0dQk5dyK0KuOb9a5 + input).hexdigest().endswith('0'*6)
    #                              ^^^^^^^^^^^^^^^^                               ^^^^^
    #                              -> <prefix>                                    -> <search_target>
    @staticmethod
    def hash_search_htv_2024(prefix, search_target, search_space='', result_length=4):
        search_length = len(search_target)
        if search_space == '':
            search_space = HashSearch.printable_characters
        for curr_list in itertools.permutations(search_space, result_length):
            curr_postfix = ''.join(curr_list)
            curr_bytes = (prefix + curr_postfix).encode()
            curr_hash = sha256(curr_bytes).hexdigest()[-search_length:]
            if curr_hash == search_target:
                return curr_postfix
        return None

    # Challenge for XMAS CTF 2021:
    #   Provide a hex string X such that sha256(unhexlify(X))[-5:] = e709b
    #                                                                ^^^^^
    #                                                                -> <search_target>
    @staticmethod
    def hash_search_xmas_ctf_2021(search_target, string_length=4):
        search_length = len(search_target)
        for curr_value in range(0, 2**32):
            curr_bytes = (curr_value).to_bytes(string_length, byteorder='big')
            curr_hash = sha256(curr_bytes).hexdigest()[-search_length:]
            if curr_hash == search_target:
                return curr_bytes.hex()
        return None

# --- end of file --- #
