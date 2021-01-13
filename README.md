# Monoalphabetic-and-Vigenere-Cipher
Encrypt and break monoalphabetic and vigenère cipher using n-gram analysis

## [Monoalphabetic cipher](https://en.wikipedia.org/wiki/Substitution_cipher#Simple_substitution)

### Usage of encryption and decryption module
```bash
mono.py [-h] (-e/--encrypt KEY | -d/--decrypt KEY) [-o/--out OUT] FILE
```

### Usage of breaking module
```bash
break_mono.py [-h] [-o/--out OUT] FILE
```

### Example: Encryption
Encrypt a given plaintext with a chosen key.
```python
$ python3 ./src/mono/mono.py -e ZEBRASCDFGHIJKLMNOPQTUVWXY ./examples/mono.plaintext -o ./examples/mono.ciphertext2
```

### Example: Decryption
Decrypt a given cyphertext with the correct key.
```python
$ python3 ./src/mono/mono.py -d ZEBRASCDFGHIJKLMNOPQTUVWXY ./examples/mono.ciphertext -o ./examples/mono.plaintext2
```

### Example: Breaking
The breaker uses an evolutionary algorithm to iteratively improve the key. Multithreading is used by default. Amount of threads is adjustable. But depending on the used hardware, the breaking takes a while.
```python
$ python3 ./src/mono/break_mono.py ./examples/mono.ciphertext -o ./examples/mono.key2
```
