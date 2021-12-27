There are some utilities defined in `functions.py` file.
Each function is described in its docstring.

Then we diagonalize matrix A and find out that its eigenvalues are `10` and `-1`.
`10` is a primitive root modulo `p`. Also `p-1`'s prime factors are all below 1000, so we can multiply `P` and `P^-1` to `A^d` and `A^r` and then solve DLP problem on the resulting matrices using CRT and number theoretic stuff.
After finding `r` and `d`, we calculate `r.d` and then calculate `A**(r.d)**-1`.
It's obvious that by calculating product of this matrix and `C`(ciphertext matrix) we can find `P`(plaintext matrix)

```ipython
In [1]: exec(open('functions.py', 'r').read())

In [2]: A = [[38199337272663519912859864066101528484023656231849338967558894235177040565160 , 39708167173513090810083500967474691943646789486489990958
   ...: 101592717502452906918],
   ...: [ 8216211510625558273096642057121313417997488994504871245106775381995665925783 , 5621397347925384939221994858755409108199741921810558442983315
   ...: 5946799898624740]]

In [3]: ev = eigenvals(A)

In [4]: P = Pof(A, ev)

In [5]: Q = inv(P)

```

Import functions, define matrix A, calculate its eigenvalues, P and Q!

```ipython
In [6]: Ad = [[61709241598677561125021718690991651934557899286972116933820920757636771220273 , 1945367449329759288724720626216309893787847192907494307
   ...: 536759223359193510642] ,
   ...: [37495232301500074672571996664644922614693962264764098174213150757616575323566 , 7348269231944161963123250652171976847627786311806728904368575
   ...: 861561449853500]]

In [7]: Ar = [[47566868540912475779105819546118874217903268597017385039977593878486632022506 , 8607316230195499521991273934401065924872082381455781052
   ...: 8618517154406350653517],
   ...: [23443866424088482893369441934221448179896589659663581973508963775891809430857 , 7456733364017748467813857453439571412885431544007684072842864
   ...: 9074147859070975]]

In [8]: T = mult(Q, mult(Ad, P))

In [9]: T
Out[9]:
[[69057510830621723088144969343163628782185685598778845838189496619198221073772,
  0],
 [0, 1]]

```

Then define `A**d` and `A**r`. `Q.A**d.P` is a diagonal matrix as expected.

```ipython
In [10]: factors = [2, 5, 103, 131, 139, 149, 181, 223, 263, 313, 337, 347, 349, 359, 389, 409, 479, 509, 547, 599, 613, 643, 751, 757, 773, 787, 6352
    ...: 09, 839, 857, 877]

In [16]: T = mult(Q, mult(Ar, P))

In [17]: rems = list(map(lambda x: find_r(T[0][0], x), factors))

In [19]: _, r = crt(factors, rems)

In [20]: T = mult(Q, mult(Ad, P))

In [21]: rems = list(map(lambda x: find_r(T[0][0], x), factors))

In [22]: _, d = crt(factors, rems)

In [23]: pow(10, d, p) == T[0][0]
Out[23]: True

```

Factorize `p-1` and find `r mod factor` for each of those factors. These factors are not necessarily prime, but they're coprime.

After finding these remainders, we use CRT to combine them and find `r` and `d` modulo `p-1`

```ipython
In [24]: dr = d * r % (p - 1)

In [25]: Adr = mult(P, mult([[pow(10, dr, p), 0],[0, pow(-1, dr, p)]], Q))

In [26]: C = [[56937964695156855099385034285428853461603799261684034842341841781057485084327 , 8245932883532288582485442586402380922271740198199318234
    ...: 6342472865578156162544],
    ...: [85092677346274708324092648597361729755305119435989183201786866456596369562681 , 222288617149535853572811827800022715056685869482024160544538
    ...: 61940155538803489]]

In [27]: P = mult(inv(Adr), C)

```

Then calculate inverse of `A**dr` and decrypt `C` to earn `P`

```ipython
In [28]: from Crypto.Util.number import bytes_to_long, long_to_bytes

In [29]: long_to_bytes(P[0][0]) + long_to_bytes(P[0][1]) + long_to_bytes(P[1][0]) + long_to_bytes(P[1][1])
Out[29]: b'ASIS{PuBl1c-K3y_CRyp70sy5tEm_B4S3d_On_Tw0D!m3nSiOn_DLP!}'

```

Use `long_to_bytes` to find the flag at last.
