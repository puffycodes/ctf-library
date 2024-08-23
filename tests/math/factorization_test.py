# file: factorization_test.py

import unittest
from ctf_library.math.factorization import Factorization

class FactorizationTest(unittest.TestCase):

    verbose = False

    def test_factorization(self):
        for number in range(2, 50):
            self.do_check_factorization(number)
        for number in range(-1, -50, -1):
            self.do_check_factorization(number)
        for number in [0, 1]:
            factors = Factorization.prime_factorization(number)
            totient = Factorization.totient_function(number)
            if FactorizationTest.verbose:
                print(f'{number}: {factors} {totient}')
            self.assertEqual([], factors)
        return
    
    def do_check_factorization(self, number):
        factors = Factorization.prime_factorization(number)
        totient = Factorization.totient_function(number)
        product = self.list_multiplication(factors)
        if FactorizationTest.verbose:
            print(f'{number}: {factors} {totient}')
        self.assertEqual(product, number)
        return
    
    def list_multiplication(self, number_list):
        product = 1
        for number in number_list:
            product *= number
        return product
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
