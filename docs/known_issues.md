# Known Issues in CTF Library

## Unimplemented Features

1. Book Cipher Encryption (ctf_library.cipher.book_cipher.py) is not implemented.
1. Unit tests for a few cipher are not implemented.

## Known Bugs

1. Hill Cipher (ctf_library.cipher.hill_cipher.py) is not working correctly when the plain text or
cipher text does not match the block boundary exactly.

## Resolved Bugs

1. [Resolved on 14 June 2024] Hill Cipher Decryption (ctf_library.cipher.hill_cipher.py) is not working correctly.
    - The reason is that the computation of the modular inverse of the matrix key is wrong.
    - The unit test is not implemented correctly because it compensates for the above error.

***

*Updated on 16 June 2024*
