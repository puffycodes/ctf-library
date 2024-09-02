# file: mathlib.py

# A random collection of math functions.

# GCD (or HCF)
# - Ref: https://simple.wikipedia.org/wiki/Greatest_common_divisor

# Extended GCD
# - Ref: http://anh.cs.luc.edu/331/notes/xgcd.pdf

# LCM
# - Ref: https://en.wikipedia.org/wiki/Least_common_multiple
# - Ref: https://www.cuemath.com/numbers/lcm-least-common-multiple/

# Euclidean Algorithms
# - gcd() Ref: https://en.wikipedia.org/wiki/Euclidean_algorithm
# - xgcd() Ref: https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

# Exponentiation
# - Ref: https://simple.wikipedia.org/wiki/Exponentiation_by_squaring

# Integer Square Root
# 1. Using Newton's Method
#    - Ref: https://stackoverflow.com/questions/15390807/integer-square-root-in-python
#    - Ref: http://code.activestate.com/recipes/577821-integer-square-root-function/
#    - Ref: https://en.wikipedia.org/wiki/Newton%27s_method


class MathLib:

    # --- Greatest Common Divisor (GCD) Related
    #     - Can use math.gcd() for Python 3.5 and above.
    #     - The Euclidean Algorithms may return a negative gcd value, which
    #       is different from math.gcd(). The return value is negative when
    #       the second value is negative.
    #     - The function gcd() returns the positive gcd value.

    @staticmethod
    def gcd(a, b):
        return abs(MathLib.gcd_euclidean(a, b))
    
    # --- Euclidean Algorithms for finding GCD
    
    @staticmethod
    def gcd_euclidean(a, b):
        while b != 0:
            r = a % b
            a, b = b, r
        return a
    
    @staticmethod
    def gcd_euclidean_recursive(a, b):
        if b == 0:
            return a
        else:
            return MathLib.gcd_euclidean_recursive(b, a % b)
        
    # --- Extended Euclidean Algorithm (XGCD)
    #     - For two numbers a and b, return g, x and y,
    #       where g = gcd(a, b) and g = ax + by.
    #     - The value g may be negative.

    @staticmethod
    def xgcd(a, b):
        prevx, x = 1, 0
        prevy, y = 0, 1
        while b != 0:
            q = a // b
            x, prevx = prevx - q * x, x
            y, prevy = prevy - q * y, y
            a, b = b, a % b
        return a, prevx, prevy
        
    # --- Least Common Multiple (LCM) Related
    #     - Can use math.lcm() for Python 3.9.0 and above.
    #     - Return value of lcm() is always positive.

    @staticmethod
    def lcm(a, b):
        if a == 0 and b == 0:
            # special case
            return 0
        return abs(a * b) // abs(MathLib.gcd(a, b))

    # --- Exponentiation Related
    #     - Can use Python built-in function pow().

    @staticmethod
    def pow(x, n):
        return MathLib.pow_exponentiation_by_squaring(x, n)
    
    # --- Exponentation by Squaring
    #     - An algorithm that compute x ^ n for a positive integer n where n > 0.
    #     - Two versions, one non-recursive, one recursive.
    #     - Limitation:
    #         - Do not compute modulo of exponentiation.
    #           - Use ModularArithmetic.mod_pow() or Python built-in function pow().
    #         - Do not work for x that is not integer. (TODO: check why)

    @staticmethod
    def pow_exponentiation_by_squaring(x, n):
        result = 1
        if n < 0:
            # special case when n < 0
            raise ValueError('exponent cannot be negative: {n}')
        # the case when n == 0 is taken care of in the loop
        while n > 0:
            if n % 2 == 1:
                result = result * x
            x = x * x
            n = n // 2
        return result
    
    @staticmethod
    def pow_exponentiation_by_squaring_recursive(x, n):
        if n < 0:
            # special case when n < 0
            raise ValueError('exponent cannot be negative: {n}')
        elif n == 0:
            # special case when n = 0
            return 1
        elif n == 1:
            return x
        elif n % 2 == 0:
            # n is even
            return MathLib.pow_exponentiation_by_squaring_recursive(x*x, n//2)
        else:
            # n is odd and n > 2
            return x * MathLib.pow_exponentiation_by_squaring_recursive(x*x, (n-1)//2)
        
    # --- Integer Square Root
    #     - Can use gmpy2.isqrt().
    #     - Can use math.isqrt() for Python 3.8 and above.

    @staticmethod
    def isqrt(n):
        return MathLib.isqrt_newtons_method_faster(n)
    
    # --- Newton's Method
    #     - Returns the largest integer x for which x * x does not exceed n.
    @staticmethod
    def isqrt_newtons_method(n):
        if n >= 0:
            x = n
            y = (x + 1) // 2
            while y < x:
                x = y
                y = (x + n // x) // 2
            return x
        else:
            raise ValueError('square root not defined for negative numbers')
        
    @staticmethod
    def isqrt_newtons_method_faster(n):
        if n > 0:
            x = 1 << (n.bit_length() + 1 >> 1)
            while True:
                y = (x + n // x) >> 1
                if y >= x:
                    return x
                x = y
        elif n == 0:
            return 0
        else:
            raise ValueError('square root not defined for negative numbers')
        
    @staticmethod
    def isqrt_newtons_method_faster_02(x):
        if x < 0:
            raise ValueError('square root not defined for negative numbers')
        n = int(x)
        if n == 0:
            return 0
        a, b = divmod(n.bit_length(), 2)
        x = 2**(a+b)
        while True:
            y = (x + n//x)//2
            if y >= x:
                return x
            x = y
    
# --- end of file --- #
