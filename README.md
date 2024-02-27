# CrypS
 CrypS Tool for Cryptography

# BaseEncDec
This is a Base64 ( for the moment module ) for encoding and decoding.
It also comes with some extra features such as a History of the operations (encodings and decodings)

```
base64 = BaseEncDec()
base64.encode("ABC")
QUJD

base64.decode("QUJD")
ABC
```

# DES Algorithm
Implementation for DES.
The Encryption keys for Feistel are generated using a random seed.

