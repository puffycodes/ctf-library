# file: mathlib.py

# A random collection of math functions.

# GCD (or HCF)
# - Ref: https://simple.wikipedia.org/wiki/Greatest_common_divisor

# Extended GCD
# - Ref: http://anh.cs.luc.edu/331/notes/xgcd.pdf

# LCM
# - Ref: https://en.wikipedia.org/wiki/Least_common_multiple
# - Ref: https://www.cuemath.com/numbers/lcm-least-common-multiple/

class MathLib:

    # --- GCD Related
    #     - Can use math.gcd() for Python 3.5 and above.
    #     - The Euclidean Algorithm may return a negative gcd value, which
    #       is different from math.gcd(). The return value is negative when
    #       the second value is negative.

    @staticmethod
    def gcd(a, b):
        return MathLib.gcd_euclidean(a, b)
    
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
        
    # --- LCM Related
    #     - Can use math.lcm() for Python 3.9.0 and above.
    #     - Return value of lcm() is always positive.
    @staticmethod
    def lcm(a, b):
        if a == 0 and b == 0:
            # special case
            return 0
        return abs(a * b) // abs(MathLib.gcd(a, b))

# --- end of file --- #
