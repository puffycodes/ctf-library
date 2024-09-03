# file: rsa_demo.py

# Public Key Cryptography
# - Ref: https://en.wikipedia.org/wiki/Public-key_cryptography

# RSA
# - Ref: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
# - Ref: https://www.askpython.com/python/examples/rsa-algorithm-in-python

# Fermat Primes
# - Ref: https://en.wikipedia.org/wiki/Fermat_number

import math

class RSADemo:

    # Note: This is a demonstration of RSA. Not for production use.

    class RSADemoKey:
        pass

    def __init__(self, key):
        self.key = key
        return
    
    def encrypt(self, plain_text):
        return 'not implemented yet'
    
    def decrypt(self, cipher_text):
        return 'not implemented yet'

    class Helper:

        e_minimum_value = 3
        e_common_choices = [ 3, 17, 65537 ] # Fermat Primes

        @staticmethod
        def euler_totient_function(p, q):
            # the computation is valid assuming that p, q are primes
            return (p - 1) * (q - 1)

        @staticmethod
        def carmichael_totient_function(p, q):
            # the computation is valid assuming that p, q are primes
            return math.lcm(p - 1, q - 1)
        
        @staticmethod
        def compute_private_key(p, q, e=-1, phi_function=euler_totient_function):
            # compute n and phi from p and q
            n = p * q
            phi = phi_function(p, q)

            # save original e for reporting later when needed
            e_input = e

            # choose a value of e such that 1 < e < phi and gcd(phi, e) == 1
            if e < RSADemo.Helper.e_minimum_value:
                e = RSADemo.Helper.e_minimum_value
            found_e = False
            while e < phi:
                # get next number if gcd(phi, e) != 1
                if math.gcd(phi, e) != 1:
                    e += 1
                else:
                    found_e = True
                    break

            if not found_e:
                raise ValueError(
                    f'cannot find a suitable value for e between 1 and {phi}. e given is {e_input}.'
                )
            
            # compute d from e and phi
            d = pow(e, -1, phi)

            # returns e, d, and n
            # note that value of e may have changed
            return e, d, n
        
        @staticmethod
        def rsa_encrypt_value(m, e, n):
            return pow(m, e, n)
        
        @staticmethod
        def rsa_decrypt_value(c, d, n):
            return pow(c, d, n)
        
# --- end of file --- #
