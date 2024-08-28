# file: modular_arithmetic.py

from ast import mod
import unittest
import random
from ctf_library.math.modular_arithmetic import ModularArithmetic

class ModularArithmeticTest(unittest.TestCase):

    # --- Test Cases

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
    
    def test_mod_sqrt(self):
        verbose = False
        modulo_list = [ 17, 32, 37, 55, 59, 199, 293, 991, 997 ]
        for modulo in modulo_list:
            for number in range(modulo):
                self.do_check_mod_sqrt_tonelli_shanks(number, modulo, verbose=verbose)
        for modulo in modulo_list:
            for number in range(modulo):
                self.do_check_mod_sqrt_slow(number, modulo, verbose=verbose)
        return
    
    def test_mod_sqrt_compare(self):
        verbose = False
        modulo_list = [ 17, 32, 55, 997 ]
        for modulo in modulo_list:
            for number in range(modulo):
                self.do_compare_mod_sqrt(number, modulo, verbose=verbose)
        return
    
    # --- Internal Functions
    
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
    
    def do_check_mod_sqrt_tonelli_shanks(self, number, modulo, verbose=False):
        self.do_check_mod_sqrt_function(
            number, modulo,
            mod_sqrt_ftn=ModularArithmetic.mod_sqrt_tonelli_shanks,
            verbose=verbose
        )
        return
    
    def do_check_mod_sqrt_slow(self, number, modulo, verbose=False):
        self.do_check_mod_sqrt_function(
            number, modulo,
            mod_sqrt_ftn=ModularArithmetic.mod_sqrt_slow,
            verbose=verbose
        )
        return
    
    def do_check_mod_sqrt_function(self,
                                   number, modulo, 
                                   mod_sqrt_ftn=ModularArithmetic.mod_sqrt_tonelli_shanks,
                                   verbose=False):
        try:
            sqrt_list = mod_sqrt_ftn(number, modulo)
            if verbose:
                print(f'mod_sqrt({number}, {modulo}) = {sqrt_list}')
            for sqrt in sqrt_list:
                result = (sqrt * sqrt) % modulo
                self.assertEqual(number, result)
        except ValueError as e:
            if verbose:
                print(f'no modular square root for {number}, modulo {modulo}')
        return
    
    def do_compare_mod_sqrt(self, number, modulo, verbose=False):
        try:
            sqrt_list_1 = ModularArithmetic.mod_sqrt_tonelli_shanks(number, modulo)
        except ValueError as e:
            sqrt_list_1 = []
            if verbose:
                print(f'no modular square root for {number}, modulo {modulo}')
        sqrt_list_2 = ModularArithmetic.mod_sqrt_slow(number, modulo)
        if verbose or len(sqrt_list_1) != len(sqrt_list_2):
            print(f'mod_sqrt({number}, {modulo}) = {sqrt_list_1}, {sqrt_list_2}')
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
