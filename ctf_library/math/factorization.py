# file: factorization.py

class Factorization:

    # ----- Factorisation ----- #
    @staticmethod
    def prime_factors(number):
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
        factors = Factorization.prime_factors(number)
        factors.sort()
        return factors[-1]

    # Ref: https://en.wikipedia.org/wiki/Euler%27s_totient_function
    @staticmethod
    def totient_function(number):
        factors = Factorization.prime_factors(number)
        phi_n = 1
        for p in set(factors):
            phi_n *= p ** (factors.count(p) - 1) * (p - 1)
        return phi_n

# --- end of file --- #
