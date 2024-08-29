# file: modular_arithmetic.py

# Modular Arithmetic
# - Ref: https://en.wikipedia.org/wiki/Modular_arithmetic
#
# Modular Multiplicative Inverse
# - Ref: https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
# - Ref: https://cp-algorithms.com/algebra/module-inverse.html
# - Ref: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
# - Ref: https://docs.python.org/3/library/functions.html#pow
#
# Modular Exponentiation
# - Ref: https://simple.wikipedia.org/wiki/Exponentiation_by_squaring
#
# Modular Square Root
# - Tonelli–Shanks algorithm
#   Ref: https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm

from ctf_library.math.mathlib import MathLib

class ModularArithmetic:

    @staticmethod
    def mod_inv(number, modulo):
        return ModularArithmetic.multiplicative_inverse(number, modulo)
    
    @staticmethod
    def mod_pow(base, exponent, modulo):
        return ModularArithmetic.mod_pow_exponentiation_by_squaring(
            base, exponent, modulo
        )

    @staticmethod
    def mod_sqrt(number, modulo):
        return ModularArithmetic.mod_sqrt_tonelli_shanks(number, modulo)
    
    # ----- Modulo Inverse related ----- #

    # Modular Multiplicative Inverse
    # - Can use pow(number, -1, modulo) for Python 3.8 and above.
    # - Returns inverse where (number * inverse) = 1 mod modulo.
    # - The return value is made positive because MathLib.xgcs() may return
    #   a negative x.
    @staticmethod
    def multiplicative_inverse(number, modulo):
        g, x, _ = MathLib.xgcd(number, modulo)
        if g != 1:
            raise ValueError('modular multiplicative inverse does not exist.')
        else:
            return (x % modulo + modulo) % modulo
        
    # ----- Modular Exponentation related ----- #

    # Modular Exponentiation
    # - Can use pow(base, exponent, modulo) for Python 3.8(?) and above.
    @staticmethod
    def mod_pow_exponentiation_by_squaring(base, exponent, modulo):
        result = 1
        if exponent < 0:
            # if exponent is negative, compute mod_pow(inv_base, -exponent, modulo).
            # may raise error if multiplicative inverse does not exist.
            base = ModularArithmetic.multiplicative_inverse(base, modulo)
            exponent = - exponent
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulo
            base = (base * base) % modulo
            exponent = exponent // 2
        return result

    # ----- Modulo Square Root related ----- #
    
    @staticmethod
    def mod_sqrt_slow(v, p):
        result = []
        for i in range(p):
            if pow(i, 2, p) == v:
                result.append(i)
        return result    
    
    @staticmethod
    def legendres_symbol(v, p):
        if p % 2 == 0:
            raise ValueError('p is even')
        s = pow(v, (p-1)//2, p)
        if s == p - 1:
            s = -1
        return s
    
    # Tonelli–Shanks Algorithm
    #
    # input:
    #  p: a prime
    #  n: r exists such that r ^ 2 mod p = n
    # output:
    #  r: where r ^ 2 mod p = n
    # limitation:
    #  p must be a prime
    #
    @staticmethod
    def mod_sqrt_tonelli_shanks(n, p, verbose=False):
        result = []
        
        if ModularArithmetic.legendres_symbol(n, p) == -1:
            return result
        
        # find q and s such that p - 1 = q * 2 ^ s
        q, s = p - 1, 0
        while q % 2 == 0:
            q = q // 2
            s += 1
        if verbose:
            print('q:', q)
            print('s:', s)
        
        # find z such that z is a quadratic non-residues
        found = False
        for i in range(2, p):
            if ModularArithmetic.legendres_symbol(i, p) == -1:
                z, found = i, True
                break
        if not found:
            return result
        if verbose:
            print('z:', z)
        
        # compute
        m = s
        c = pow(z, q, p)
        t = pow(n, q, p)
        r = pow(n, ((q+1)//2), p)
        
        while True:
            if t == 0:
                result.append(0)
                return result
            if t == 1:
                result.append(r)
                # add -r mod p
                result.append(-r % p)
                return result
            found = False
            for i in range(1, m):
                if pow(t, 2**i, p) == 1:
                    found = True
                    break
            if not found:
                return result
            if verbose:
                print('i:', i)
            
            b = pow(c, 2**(m-i-1), p)
            m = i
            c = pow(b, 2, p)
            t = (t * c) % p
            r = (r * b) % p
        
        return result
    
# --- end of file --- #
