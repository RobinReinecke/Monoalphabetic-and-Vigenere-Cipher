# Monoalphabetic-and-Vigenere-Cipher
Encrypt and break monoalphabetic and vigenère cipher using n-gram analysis

## [Monoalphabetic cipher](https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution)

### Usage of encryption and decryption module
```bash
mono.py [-h] (--encrypt KEY | --decrypt KEY) [--out OUT] FILE
```

### Example: Encryption
Encrypt a given plaintext with a chosen key.
```python
$ python3 ./src/mono/mono.py -e ZEBRASCDFGHIJKLMNOPQTUVWXY ./examples/mono.plaintext
```

### Example: Decryption
Decrypt a given cyphertext with the correct key.
```python
$ python3 ./src/mono/mono.py -d ZEBRASCDFGHIJKLMNOPQTUVWXY ./examples/mono.ciphertext
```
