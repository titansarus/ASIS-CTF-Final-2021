# Stairs


## Description

It's quite similar to public crypto-system, or the fear of climbing stairs, except in its specific focus.

```bash
nc 95.217.210.96 11010
```


After connecting to the server, we get this:

```log
------------------------------------------------------------------------
|          ..:: Try to going down the stairs carefully ::..            |
|           Try to break this cryptosystem and find the flag!          |
------------------------------------------------------------------------
| Options:                                                             |
|       [E]ncryption function                                          |
|       [T]ry encryption!                                              |
|       [P]ublic key                                                   |
|       [Q]uit                                                         |
|----------------------------------------------------------------------|
```

\[E\]ncryption function is:

```python
def encrypt(m, pubkey):
        e, n = 5, pubkey
        M = bytes_to_long(flag)
        m += M
        c = (pow(m, e, n) + m) % n
        return c
```

\[T\]ry encryption!, gets an input and encrpyts it using the encyption function.

\[P\]ublic key, gives the public key which changes everytime a new connection is made.

## Writeup


This problem can be solved easily by some algebraic acts!

The idea is to use terms with different degrees to construct higher and lower degrees. For example, by setting the `m=0`, we have `M^5 + M`. Afterward by setting `m=+/- 1` we have `(M+1)^5 + M + 1` and `(M-1)^5 + M - 1` respectively. By adding/subtracting the two later terms, we can achieve new terms with degrees 3 and 4. Now we can build terms with degree 8 in 2 ways. The first one is squaring the 4th-degree term. The other way is to multiply 3rd-degree and 5th-degree terms. Now we try to eliminate the 8th degree and get new terms. We can finally compute `M` by continuing this procedure, which leads us to the flag.


For more description on details of the computations, see the comments in [the code](./stairs.py).
