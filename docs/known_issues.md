# Known Issues for CTF Library

## Unimplemented Features

1. Book Cipher Encryption (ctf_library.cipher.book_cipher.py) is not implemented.
1. Unit tests for a few cipher are not implemented.

## Known Bugs

1. Hill Cipher Decryption (ctf_library.cipher.hill_cipher.py) is not working correctly.
    - The reason is that the computation of the inverse modulo of the matrix key is wrong.
    - The unit test is not implemented correctly because it compensates for the above error.

***

*Updated on 12 June 2024*