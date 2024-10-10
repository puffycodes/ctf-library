# file: chinese_remainder_theorem.py

# --- Chinese Remainder Theorem
# Ref: https://en.wikipedia.org/wiki/Chinese_remainder_theorem
# Ref: https://www.math.cmu.edu/~mradclif/teaching/127S19/Notes/ChineseRemainderTheorem.pdf
# Ref: http://homepages.math.uic.edu/~leon/mcs425-s08/handouts/chinese_remainder.pdf
# Ref: https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html

import math
from ctf_library.math.mathlib import MathLib
from ctf_library.math.modular_arithmetic import ModularArithmetic

class ChineseRemainderTheorem:

    # ----- Chinese Remainder Theorem ----- #

    # Solve
    #   x = a1 mod n1
    #   x = a2 mod n2
    #   ...
    #   x = ak mod nk
    #   where the ni are pairwise coprime.
    # as solution
    #   x = a mod n1*n2*...*nk
    
    # Input:
    # - coef_list = [ (a1, n1), (a2, n2), ..., (ak, nk) ]
    # Return:
    # - result = (a, n)
    @staticmethod
    def solve(coef_list, verbose=False):
        coef_len = len(coef_list)
        if coef_len < 1:
            return []
        if coef_len == 1:
            return coef_list[0]
        result = []
        for i in range(0, coef_len, 2):
            if i + 1 < coef_len:
                coef_pair = [coef_list[i], coef_list[i+1]]
                new_coef = ChineseRemainderTheorem.solve_pair(coef_pair, verbose=verbose)
                result.append(new_coef)
            else:
                result.append(coef_list[i])
        return ChineseRemainderTheorem.solve(result, verbose=verbose)
    
    # Input:
    # - coef_pair = [ (a1, n1), (a2, n2) ]
    # Return:
    # - result = (a, n)
    @staticmethod
    def solve_pair(coef_pair, verbose=False):
        (a1, n1), (a2, n2) = coef_pair
        g, m1, m2 = MathLib.xgcd(n1, n2)
        if g != 1:
            raise ValueError('%d and %d are not co-prime' % (n1, n2))
        n = n1 * n2
        a = (a1 * m2 * n2 + a2 * m1 * n1) % n
        if verbose:
            print('[1]:', a1, n1)
            print('[2]:', a2, n2)
            print('xgcd:', g, m1, m2)
            print('result:', a, n)
        return [a, n]
    
    @staticmethod
    def solve_extended(coef_list, verbose=False):
        '''
        Solve the given equations using Chinese Remainder Theorem

        Solve

            m1 * x = a1 mod n1
            m2 * x = a2 mod n2
            ...
            mk * x = ak mod nk

        as solution

            x = a mod n

        :param coef_list: a list of tuple (m, a, n)
        :type coef_list: list of tuple
        :param verbose: when True print some debugging information
        :type verbose: bool, optional

        :return: the tuple (a, n)
        :rtype: tuple
        '''
        reduced_coef_list = [
            ChineseRemainderTheorem.reduce(coef, verbose=verbose) for coef in coef_list
        ]
        result = ChineseRemainderTheorem.solve(reduced_coef_list, verbose=verbose)
        return result
    
    @staticmethod
    def reduce(coef, verbose=False):
        '''
        Reduce m * x = a mod n to x = a_prime mod n_prime

        :param coef: the tuple (m, a, n)
        :type coef: tuple
        :param verbose: when True print some debugging information
        :type verbose: bool, optional

        :return: the tuple a_prime, n_prime
        :rtype: tuple
        '''
        (m, a, n) = coef
        gcd = math.gcd(*coef)
        if verbose:
            print(f'{gcd=}')
        if gcd > 1:
            m, a, n = m // gcd, a // gcd, n // gcd
        if m == 1:
            a_prime = a
            n_prime = n
        else:
            m_inv = ModularArithmetic.mod_inv(m, n)
            if verbose:
                print(f'{m_inv=}')
            a_prime = (a * m_inv) % n
            n_prime = n
        return (a_prime, n_prime)
    
# --- end of file --- #
