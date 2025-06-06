# file: factorization_test.py

import unittest
import random
from ctf_library.math.factorization import Factorization

class FactorizationTest(unittest.TestCase):

    def test_factorization(self):
        verbose = False
        for number in range(2, 5000):
            self.do_check_factorization_and_totient(number, verbose=verbose)
        for number in range(-1, -50, -1):
            self.do_check_factorization_and_totient(number, verbose=verbose)
        for number in [ 65535, 65536, 1234567890 ]:
            self.do_check_factorization_and_totient(number)
        for number in [0, 1]:
            factors = Factorization.prime_factorization(number)
            totient = Factorization.euler_totient_function(number)
            if verbose:
                print(f'{number}: {factors} {totient}')
            self.assertEqual([], factors)
        return
    
    def test_factorization_random(self):
        verbose = False
        self.do_check_factorization_random(rounds=20, verbose=verbose)
        return
    
    def test_all_factors(self):
        verbose = False
        for number in range(-10, 65):
            self.do_check_all_factors(number, verbose=verbose)
        for number in [ 65535, 65536, 1234567890 ]:
            self.do_check_all_factors(number, verbose=verbose)
        return
    
    test_cases_fermat_factorization = [
        # Test cases from small numbers
        [ 59 * 73, 73, 59 ],
        [ 3 * 73, 3, 73 ],
        [ 97 * 499, 499, 97 ],
        [ 11 * 13, 11, 13 ],
        [ 25 * 27, 25, 27 ],
        [ -25 * 27, 25, -27 ],
        # Example from CyberSpace CTF 2024
        [
            18644771606497209714095542646224677588981048892455227811334258151262006531336794833359381822210403450387218291341636672728427659163488688386134401896278003165147721355406911673373424263190196921309228396204979060454870860816745503197616145647490864293442635906688253552867657780735555566444060335096583505652012496707636862307239874297179019995999007369981828074059533709513179171859521707075639202212109180625048226522596633441264313917276824985895380863669296036099693167611788521865367087640318827068580965890143181999375133385843774794990578010917043490614806222432751894223475655601237073207615381387441958773717,
            136545858986998246186017611284664707398999797498692946608523559469499827972094856292942650773093192162138423617662757531574919967461255241533395505995030617210156281091030371701198122810180540132811734185012657022629634425970608413451030604056026161196348671111947083652764868355722990294951453693249819907769,
            136545858986998246186017611284664707398999797498692946608523559469499827972094856292942650773093192162138423617662757531574919967461255241533395505995030621481175031499344949735265383560242346915071826552296754272942746356998125287415246140255211942791159132750757895494949215741681277852308288626896929744893
        ],
        # Example from H7CTF 2024
        [
            19941761574905742888287481436741891092124181365374951557784462831976463640107265018634834348445714890239773671635245721007690323617473110640838905137749040079027523456576873242576882348266023282328418714706775196352487380997352642934338999701240803315143633815388891936049690566875086476878846288179053430346474607507140036260924419560806005408849547824680623840905827643373832321736642361809029363098769822048159935628385558949380403530181068302284344450193809037352292218892697094260257903235373427839438588016417069626966199168116250816624950794879795025563625197229849548571880188149181610538268071041049047969843,
            141215302198117831625062864040488799070519720517200041108428144553545151598056768261249804591039619563427429432774864846431648576756532204385570644513881377399176360191752553530461890049438561464940760188273504330998813264974135649979472954395545506855735753302212710905410503554080274040723801092443415762179,
            141215302198117831625062864040488799070519720517200041108428144553545151598056768261249804591039619563427429432774864846431648576756532204385570644513881377399176360191752553530461890049438561464940760188273504330998813264974135649979472954395545506855735753302212710905410503554080274040723801092443415763217
        ],
        # perfect square of primes
        [ 4, 2, 2], [ 9, 3, 3 ], [ 25, 5, 5 ], [ 49, 7, 7 ],
        [ 11 * 11, 11, 11 ], [ 13 * 13, 13, 13 ], [ 17 * 17, 17, 17 ],
        [ -4, 2, -2], [ -49, 7, -7 ],
        # perfect square of non-primes
        [ 16, 4, 4 ], [ 36, 6, 6 ], [ 64, 8, 8 ], [ 81, 9, 9 ],
        [ 15 * 15, 15, 15 ], [ -15 * 15, 15, -15 ],
        # prime numbers
        [ 97, 1, 97 ], [ -97, 1, -97 ],
        # very small numbers
        [ 0, 0, 0 ], [ 1, 1, 1 ], [ 2, 1, 2 ], [ 3, 1, 3 ],
        [ -1, 1, -1 ], [ -2, 1, -2 ], [ -3, 1, -3 ],
        # small numbers
        [ 4, 2, 2 ], [ 5, 1, 5 ], [ 7, 1, 7 ], [ 8, 2, 4 ],
        [ 11, 1, 11 ], [ 12, 2, 6 ], [ 13, 1, 13 ],
        [ 15, 3, 5 ], 
        # this algorith gives 1 as the result for the following small numbers
        [ 6, 1, 6 ], [ 10, 1, 10 ], [ 14, 1, 14 ], [ 82, 1, 82 ],
    ]

    def test_fermat_factorization_single_value(self):
        verbose = False
        for n, f1, f2 in FactorizationTest.test_cases_fermat_factorization:
            self.do_check_fermat_factorization_single_value(n, f1, f2, verbose=verbose)
        return
    
    def test_fermat_factorization_single_value_termination(self):
        # check that the function terminates for small numbers
        for n in range(1000):
            result = Factorization.fermat_factorization_single_value(n)
            if result != 0:
                self.assertEqual(n % result, 0)
        return
    
    def test_fermat_factorization_factor_list(self):
        verbose = False
        for n in range(-1000, 1000):
            self.do_check_fermat_factorization_factor_list(n, verbose=verbose)
        for n, _, _ in FactorizationTest.test_cases_fermat_factorization:
            self.do_check_fermat_factorization_factor_list(n, verbose=verbose)
        self.do_check_fermat_factorization_random(verbose=verbose)
        self.do_check_fermat_factorization_random(
            rounds=100, first_range=99999999999999999999, diff_range=999999,
            verbose=verbose
        )
        return

    # --- Internal Functions
    
    def do_check_factorization_random(self, rounds=100, start=-99999999, end=99999999, verbose=False):
        for _ in range(rounds):
            number = random.randint(start, end)
            self.do_check_factorization(number, verbose=verbose)
        return
    
    def do_check_factorization_and_totient(self, number, verbose=False):
        factors = Factorization.prime_factorization(number)
        totient = Factorization.euler_totient_function(number)
        product = self.list_multiplication(factors)
        if verbose:
            print(f'{number}: {factors} {totient}')
        self.assertEqual(product, number)
        return
    
    def do_check_factorization(self, number, verbose=False):
        factors = Factorization.prime_factorization(number)
        product = self.list_multiplication(factors)
        if verbose:
            print(f'{number}: {factors}')
        self.assertEqual(product, number)
        return
    
    def do_check_all_factors(self, number, verbose=False):
        all_factors = Factorization.all_factors(number)
        if verbose:
            print(f'{number}: {all_factors}')
        for factor in all_factors:
            self.assertEqual(number % factor, 0)
        return
    
    def do_check_fermat_factorization_random(self, rounds=100,
                                             first_range=99999999,
                                             diff_range=9999,
                                             verbose=False):
        for _ in range(rounds):
            first = random.randint(0, first_range)
            diff = random.randint(0, diff_range)
            second = first + diff
            if first % 2 == 0:
                first += 1
            if second % 2 == 0:
                second += 1
            number = first * second
            self.do_check_fermat_factorization_factor_list(number, verbose=verbose)
        return
    
    def do_check_fermat_factorization_factor_list(self, n, verbose=False):
        result = Factorization.fermat_factorization_factor_list(n)
        product = self.list_multiplication(result)
        if verbose:
            print(f'fermat_factorization_factor_list({n}) = {result}', end='')
            print(f'; product = {product}')
        self.assertEqual(n, product)
        return

    def do_check_fermat_factorization_single_value(self, n, f1, f2, verbose=False):
        result_f1 = Factorization.fermat_factorization_single_value(n)
        if result_f1 != 0:
            result_f2 = n // result_f1
        else:
            result_f2 = 0
        if verbose:
            print(f'fermat_factorization({n}) = {result_f1}', end='')
            print(f'; ({n}) = ({result_f1}) * ({result_f2})')
        # Factorization.fermat_factorization() always returns a positive number
        self.assertEqual(min(abs(f1), abs(f2)), result_f1)
        self.assertEqual(max(abs(f1), abs(f2)), abs(result_f2))
        self.assertEqual(result_f1 * result_f2, n)
        return
    
    def list_multiplication(self, number_list):
        product = 1
        for number in number_list:
            product *= number
        return product
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
