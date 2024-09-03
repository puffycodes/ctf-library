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
    # Input: n should be odd
    # Return: one of the factor for n
    def fermat_factorization(n):
        a = math.isqrt(n) + 1
        b2 = a * a - n
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
