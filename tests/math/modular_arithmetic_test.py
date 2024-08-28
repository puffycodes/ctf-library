# file: modular_arithmetic.py

import unittest
import random
from ctf_library.math.modular_arithmetic import ModularArithmetic

class ModularArithmeticTest(unittest.TestCase):

    def test_multiplicative_inverse(self):
        verbose = False
        for modulo in range(2, 100):
            if verbose:
                print(f'modulo = {modulo}:')
            for number in range(modulo):
                self.do_check_multiplicative_inverse(number, modulo, verbose=verbose)
                self.do_check_multiplicative_inverse(-number, modulo, verbose=verbose)
                self.do_check_multiplicative_inverse(number, -modulo, verbose=verbose)
                self.do_check_multiplicative_inverse(-number, -modulo, verbose=verbose)
        return
    
    def test_multiplicative_inverse_random(self):
        verbose = False
        self.do_check_multiplicative_inverse_random(verbose=verbose)
        self.do_check_multiplicative_inverse_random(end_m=999, verbose=verbose)
        return
    
    def do_check_multiplicative_inverse_random(self, rounds=100,
                                               start_n=2, end_n=9999999999,
                                               start_m=2, end_m=999999,
                                               verbose=False):
        for _ in range(rounds):
            number = random.randint(start_n, end_n)
            modulo = random.randint(start_m, end_m)
            self.do_check_multiplicative_inverse(number, modulo, verbose=verbose)
        return
    
    def do_check_multiplicative_inverse(self, number, modulo, verbose=False):
        try:
            inverse = ModularArithmetic.multiplicative_inverse(number, modulo)
            if verbose:
                print(f'mod_inv({number}, {modulo}) = {inverse}')
            result = (number * inverse) % modulo
            self.assertEqual(1, result)
        except ValueError as e:
            if verbose:
                print(f'mod_inv({number}, {modulo}) does not exist.')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
