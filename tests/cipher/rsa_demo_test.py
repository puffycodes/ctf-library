# file: rsa_demo_test.py

import unittest
import random
from ctf_library.cipher.rsa_demo import RSADemo

class RSADemoTest(unittest.TestCase):

    # [
    #   <p>, <q>, <e>, <phi_function>, <expected_d>, <expected_n>,
    #   [ [<message>, <encrypted_message>], ... ]
    # ]
    # phi_function: 1 = eular totient function
    #               2 = carmichael's totient function
    test_cases = [
        # Test cases from https://en.wikipedia.org/wiki/RSA_(cryptosystem)
        [ 61, 53, 17, 2753, 3233, 1, [ [ 65, 2790 ] ] ],
        [ 61, 53, 17, 413, 3233, 2, [ [ 65, 2790 ] ] ],
        # Test cases from https://www.askpython.com/python/examples/rsa-algorithm-in-python
        [ 3, 7, 5, 5, 21, 1, [ [ 11, 2 ], [ 2, 11 ], [ 3, 12 ] ] ],
        [ 3, 7, -1, 5, 21, 1, [ [ 11, 2 ], [ 2, 11 ], [ 3, 12 ] ] ], # e will compute to 5
        [ 3, 7, 4, 5, 21, 1, [ [ 11, 2 ], [ 2, 11 ], [ 3, 12 ] ] ], # e will compute to 5
        [ 3, 7, 6, 7, 21, 1, [ [ 11, 11 ], [ 2, 2 ], [ 3, 3 ], [ 20, 20 ] ] ], # e will compute to 7
        [ 3, 11, 7, 3, 33, 1, [ [ 31, 4 ], [ 4, 16 ], [ 5, 14 ] ] ],
        # Other test cases
        [
            247783006742674559981423958215936779423,
            256816475875521019462736001544970355701,
            65537,
            4063528459192105061881707942213314161305684904964858151442922799625528800473,
            63634758573494143235493785760772752733955178124597146277440535472080687540523,
            1,
            []
        ],
    ]

    def test_rsa_helper_01(self):
        verbose = False
        for p, q, e, expected_d, expected_n, totient_choice, message_pairs in RSADemoTest.test_cases:
            phi_function = self.get_totient_function(totient_choice)
            new_e, d, n = self.do_check_compute_private_key(
                p, q, e, expected_d, expected_n, phi_function, verbose=verbose
            )
            for message, encrypted_message in message_pairs:
                self.do_check_encryption_decryption(
                    new_e, d, n, message, encrypted_message, verbose=verbose
                )
        return
    
    def test_rsa_helper_02(self):
        verbose = False
        for p, q, e, _, _, totient_choice, _ in RSADemoTest.test_cases:
            phi_function = self.get_totient_function(totient_choice)

            # provide value for e
            new_e, d, n = RSADemo.Helper.compute_private_key(p, q, e, phi_function=phi_function)
            self.do_check_encryption_decryption_random(new_e, d, n, verbose=verbose)

            # do not provide value for e
            new_e, d, n = RSADemo.Helper.compute_private_key(p, q, phi_function=phi_function)
            self.do_check_encryption_decryption_random(new_e, d, n, verbose=verbose)

            # provide a random value for e
            random_e = random.randint(2, p-1)
            new_e, d, n = RSADemo.Helper.compute_private_key(p, q, random_e, phi_function=phi_function)
            self.do_check_encryption_decryption_random(new_e, d, n, verbose=verbose)
        return
    
    # --- Internal Functions
    
    def do_check_compute_private_key(self, p, q, e, expected_d, expected_n,
                                     phi_function=RSADemo.Helper.euler_totient_function_fast,
                                     verbose=False):
        new_e, d, n = RSADemo.Helper.compute_private_key(p, q, e, phi_function=phi_function)
        if verbose:
            print(f'private_key({p}, {q}, {e}) = ({new_e}, {d}, {n})')
            if e != new_e:
                print(f'  - e has changed: {e} -> {new_e}')
        self.assertEqual(expected_d, d)
        self.assertEqual(expected_n, n)
        return new_e, d, n
    
    def do_check_encryption_decryption(self, e, d, n, message, encrypted_message,
                                       verbose=False):
        computed_c = RSADemo.Helper.rsa_encrypt_value(message, e, n)
        computed_m = RSADemo.Helper.rsa_decrypt_value(encrypted_message, d, n)
        if verbose:
            print(f'encrypt({message}, {e}, {n}) = {computed_c}')
            print(f'decrypt({encrypted_message}, {d}, {n}) = {computed_m}')
        self.assertEqual(encrypted_message, computed_c)
        self.assertEqual(message, computed_m)
        return
    
    def do_check_encryption_decryption_random(self, e, d, n, rounds=100, verbose=False):
        for i in range(rounds):
            message = random.randint(0, n-1)
            encrypted_message = RSADemo.Helper.rsa_encrypt_value(message, e, n)
            decrypted_message = RSADemo.Helper.rsa_decrypt_value(encrypted_message, d, n)
            if verbose or (not verbose and message != decrypted_message):
                print(f'encrypt({message}, {e}, {n}) = {encrypted_message}')
                print(f'decrypt({encrypted_message}, {d}, {n}) = {decrypted_message}')
            self.assertEqual(decrypted_message, message)
        return
    
    def get_totient_function(self, choice):
        if choice == 2:
            return RSADemo.Helper.carmichael_lambda_function_fast
        else:
            # include choice = 1
            return RSADemo.Helper.euler_totient_function_fast
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
