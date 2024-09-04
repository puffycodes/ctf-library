# file: factorization.py

import math

class Factorization:

    # ----- Prime Factorization ----- #

    @staticmethod
    def prime_factorization(number):
        factors = []
        
        if number < 0:
            factors.append(-1)
            number *= -1
            
        factor = 2
        while factor <= number:     
            if number % factor == 0:      
                factors.append(factor)
                number //= factor
            else:
                factor += 1
                
        return factors
    
    @staticmethod
    def max_prime_factor(number):
        factors = Factorization.prime_factorization(number)
        factors.sort()
        return factors[-1]
    
    # ----- Get All Factors ----- #
    
    # Ref: https://courses.lumenlearning.com/mathforliberalartscorequisite/chapter/finding-all-the-factors-of-a-number/
    #
    # - return a list [ f0, f1, ..., fn ] where number % fn == 0
    @staticmethod
    def all_factors(number):
        result = []

        # special case for zero
        if number == 0:
            # result.append(0)
            # result.sort()
            return result

        # handle negative numbers
        if number < 0:
            result.append(-1)
            number *= -1

        divisor = 1
        while divisor <= number:
            if number % divisor == 0:
                quotient = number // divisor
                if quotient > divisor:
                    result.append(quotient)
                    result.append(divisor)
                elif quotient == divisor:
                    # a perfect square
                    result.append(divisor)
                    break
                else:
                    # terminates when quotient is less than divisor
                    break
            divisor += 1

        result.sort()

        return result
    
    # ----- Fermat's Factorization -----

    # Fermat's Factorization
    # Ref: https://en.wikipedia.org/wiki/Fermat%27s_factorization_method
    #
    # Input: n should be odd (but we do not check)
    # Return: one of the factors for n, always positive or zero
    #
    # Limitation: The algorithm may return a trivial factor 1 for for smaller numbers.
    #
    @staticmethod
    def fermat_factorization(n):
        if n < 0:
            # do factorization on the positive number
            n *= -1
        if n == 0:
            # special case when n is zero
            return 0
        elif n <= 2:
            # special case when n is 1 or 2
            # result is 1 because this function returns the smaller factor
            return 1
        
        a = math.isqrt(n)
        if a * a == n:
            # special case when n is a perfect square
            return a
        
        a = math.isqrt(n) + 1   # original algorith uses ceil(sqrt(n))
        b2 = a * a - n
        # set a (very loose) upper limit for a so that it will terminate
        # (TODO: Is this limit correct? Please check.)
        while a < n and math.isqrt(b2) * math.isqrt(b2) != b2:
            a += 1
            b2 = a * a - n
        return a - math.isqrt(b2)
    
    # The basic Fermat's Factorization (For reference)
    #
    # Input: n should be odd
    # Return: one of the factors for n
    #
    # Limitation: There is no limit for a so this function may loop forever.
    #
    @staticmethod
    def fermat_factorization_basic(n):
        a = math.isqrt(n) + 1   # original algorith uses ceil(sqrt(n))
        b2 = a * a - n
        # no other termination condition. this loop may not end.
        while math.isqrt(b2) * math.isqrt(b2) != b2:
            a += 1
            b2 = a * a - n
        return a - math.isqrt(b2)

    # ----- Other Factor Related Functions ----- #

    # Euler's totient function
    # Ref: https://en.wikipedia.org/wiki/Euler%27s_totient_function
    @staticmethod
    def totient_function(number):
        factors = Factorization.prime_factorization(number)
        phi_n = 1
        for p in set(factors):
            phi_n *= p ** (factors.count(p) - 1) * (p - 1)
        return phi_n

# --- end of file --- #
