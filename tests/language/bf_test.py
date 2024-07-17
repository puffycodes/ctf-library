# file: bf_test.py

import unittest
from ctf_library.language.bf import *

class BrainfuckTestCases:

    # Brainfuck test cases in the format:
    #   [ <code>, <input>, <expected output> ]
    test_cases = [
        [ '', '', '' ],
        [ '++++++++++.', '', '\n' ],
        [ '+++++++++++++.---.', '', '\r\n' ],
        [ '++++++++[>++++++++<-]>+.', '', 'A' ],
        [ '+++[>,.<-]', 'abcde', 'abc' ],
        [ '+[>,.<]', 'abcde', 'abcde' ],
        [ '.', '', '\0' ],
        [ '>+++++[-<+++>]<.', '', '\x0f' ],
        [
            '++++++++++[>+++++++>++++++++++>+++<<<-]>++.>+.+++++++'
            ' ..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.',
            '',
            'Hello World!'
        ],
    ]

    # Encoder encodes a string into a Brainfuck program that, when executed, will generate the string.
    # bf(bf(encoder, 'hello,world!')) == 'hello, world!'
    encoder = '+++++++++[<+++++>-],[[-<--.++<+>>]<+.-<[->.<]>>,]'

class BrainfuckTest(unittest.TestCase):

    def test_bf_parse_paren(self):
        assert parse_parens('') == {}
        assert parse_parens('[]') == { 0: 1, 1: 0 }
        assert parse_parens('[.]') == { 0: 2, 2: 0 }
        assert parse_parens('[.[]]') == { 0: 4, 4: 0, 2: 3, 3: 2 }
        return

    def test_bf_test_cases(self):
        for code, in_data, out_data in BrainfuckTestCases.test_cases:
            result = bf(code, in_stream=in_data)
            self.assertEqual(result, out_data)
        return
    
    def test_bf_encoder(self):
        test_strings = [
            'hello, world!',
            'The quick brown fox jumps over the lazy dog',
            'asdfGHJK12345!@#$%[]{}',
            '\xff\xfe',
        ]
        for s in test_strings:
            encoded_string = bf(BrainfuckTestCases.encoder, s)
            decoded_string = bf(encoded_string)
            self.assertEqual(decoded_string, s)
        return
    
    def test_bf_encoder_2(self):
        test_strings = [
            'Hello, world!',
        ]
        for s in test_strings:
            encoded_string = bf(BrainfuckTestCases.encoder, s)
            print(f'input: {s}')
            print(f'encoded: {encoded_string}')
            print()
        return
    
if __name__ == '__main__':
    unittest.main()

# --- end of file --- #
