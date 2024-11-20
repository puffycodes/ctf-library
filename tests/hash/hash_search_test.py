# file: hash_search_test.py

import unittest
from ctf_library.hash.hash_search import HashSearch

class HashSearchTest(unittest.TestCase):

    def test_01(self):
        test_cases = [
            [ '0dQk5dyK0KuOb9a5', '000000', '' ],
            [ '0dQk5dyK0KuOb9a5', '000001', '' ],
            [ 'AybqFVbeXiMJCxbh', '000000', '' ],
            [ 'QZSsdNefcQysLe77', '000000', '' ],
            [ 'yMniGPbb8EbN4xYJ', '000000', '' ],
        ]
        for prefix, search_target, _ in test_cases:
            result = HashSearch.search_hash_htv(prefix, search_target)
            print(f'{prefix}, {search_target} -> {result}')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
