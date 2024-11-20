# file: hash_search.py

from hashlib import sha256
import string
import itertools

class HashSearch:

    printable_characters = string.ascii_letters + string.digits + string.punctuation

    # For Hack The Vote 2024
    # Give me input where sha256(0dQk5dyK0KuOb9a5 + input).hexdigest().endswith('0'*6)
    @staticmethod
    def search_hash_htv(prefix, search_target, search_space='', result_length=4):
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

# --- end of file --- #
