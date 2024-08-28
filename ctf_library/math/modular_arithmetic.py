# file: modular_arithmetic.py

# Modular Arithmetic
# - Ref: https://en.wikipedia.org/wiki/Modular_arithmetic
#
# Modular Multiplicative Inverse
# - Ref: https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
# - Ref: https://cp-algorithms.com/algebra/module-inverse.html
# - Ref: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
# - Ref: https://docs.python.org/3/library/functions.html#pow

from ctf_library.math.mathlib import MathLib

class ModularArithmetic:

    @staticmethod
    def mod_inv(number, modulo):
        return ModularArithmetic.multiplicative_inverse(number, modulo)

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

# --- end of file --- #
