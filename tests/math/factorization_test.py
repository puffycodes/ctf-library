# file: factorization_test.py

import unittest
import random
from ctf_library.math.factorization import Factorization

class FactorizationTest(unittest.TestCase):

    def test_factorization(self):
        verbose = False
        for number in range(2, 5000):
            self.do_check_factorization(number, verbose=verbose)
        for number in range(-1, -50, -1):
            self.do_check_factorization(number, verbose=verbose)
        for number in [ 65535, 65536, 1234567890 ]:
            self.do_check_factorization(number)
        for number in [0, 1]:
            factors = Factorization.prime_factorization(number)
            totient = Factorization.totient_function(number)
            if verbose:
                print(f'{number}: {factors} {totient}')
            self.assertEqual([], factors)
        return
    
    def test_factorization_random(self):
        verbose = False
        self.do_check_factorization_random(rounds=20, verbose=verbose)
        return
    
    def test_all_factors(self):
        verbose = True
        for number in range(-10, 65):
            self.do_check_all_factors(number, verbose=verbose)
        for number in [ 65535, 65536, 1234567890 ]:
            self.do_check_all_factors(number, verbose=verbose)
        return
    
    def do_check_factorization_random(self, rounds=100, start=-99999999, end=99999999, verbose=False):
        for _ in range(rounds):
            number = random.randint(start, end)
            self.do_check_factorization_only(number, verbose=verbose)
            pass
        return
    
    def do_check_factorization(self, number, verbose=False):
        factors = Factorization.prime_factorization(number)
        totient = Factorization.totient_function(number)
        product = self.list_multiplication(factors)
        if verbose:
            print(f'{number}: {factors} {totient}')
        self.assertEqual(product, number)
        return
    
    def do_check_factorization_only(self, number, verbose=False):
        factors = Factorization.prime_factorization(number)
        product = self.list_multiplication(factors)
        if verbose:
            print(f'{number}: {factors}')
        self.assertEqual(product, number)
        return
    
    def do_check_all_factors(self, number, verbose=False):
        all_factors = Factorization.all_factors(number)
        if verbose:
            print(f'{number}: {all_factors}')
        return
    
    def list_multiplication(self, number_list):
        product = 1
        for number in number_list:
            product *= number
        return product
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
