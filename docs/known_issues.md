# Known Issues in CTF Library

## Unimplemented Features

1. Book Cipher Encryption (ctf_library.cipher.book_cipher.py) is not implemented.
1. Unit tests for a few cipher are not implemented.

## Known Issues

1. Hill Cipher (ctf_library.cipher.hill_cipher.py) is not working correctly when the plain text or
cipher text does not match the block boundary exactly.
    - [Partial Resolution] Added padding and unpadding functions. Those functions are not called by the encrypt() and decrypt() functions automatically.
1. Math Library pow() function (ctf_library.math.mathlib.MathLib.pow(x, n)) does not work properly when x is not integer.
    - The algorithm is originally intended for integer value of x and positive integer n > 0.
    - Interesting to find out why it did not work for non-integer, but not likely to be resolved soon.

## Resolved Issues

1. [Resolved on 14 June 2024] Hill Cipher Decryption (ctf_library.cipher.hill_cipher.py) is not working correctly.
    - The reason is that the computation of the modular inverse of the matrix key is wrong.
    - The unit test is not implemented correctly because it compensates for the above error.

1. [Resolved on 26 Jun 2024] USB Keystroke Decoder (ctf_library.packet.usb_keystroke_decoder.py) does not process up-arrow and down-arrow correctly.
    - Captures with those keystroke will not decode correctly.

***

*Updated on 30 August 2024*
