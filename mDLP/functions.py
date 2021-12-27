p = 94413310751917369305079812653655619566021075449954923397392050181976939189891


"""
Simply return GCD of two numbers
"""
def gcd(x, y): return x if y == 0 else gcd(y, x % y)


"""
Given a set of coprime numbers and the remainders
Find the number modulo product of those prime numbers
"""
def crt(ps, rs):
    assert len(ps) == len(rs)
    if len(ps) == 1:
        return ps[0], rs[0]
    p1, r1 = crt(ps[:-1], rs[:-1])
    p2, r2 = ps[-1], rs[-1]
    assert gcd(p1, p2) == 1
    p3 = p1 * p2
    r3 = pow(p1, -1, p2) * (r2 - r1) * p1 + r1
    r3 = (r3 % p3 + p3) % p3
    return p3, r3


"""
Assume 10**x mod p == num and factor is a divisor of p-1
Also note that 10 is a primitive root modulo p
Then this function returns x mod factor with O(factor) time complexity
"""
def find_r(num, factor):
    W = pow(10, (p-1)//factor, p)
    A = pow(num, (p-1)//factor, p)
    W = pow(W, -1, p)
    cnt = 0
    while A != 1:
        A = A * W % p
        cnt += 1
    return cnt


"""
Solve a 2-degree equation: ax^2 + bx + c = 0
"""
def d2solve(a, b, c):
    a %= p
    b %= p
    c %= p
    delta = (b**2 - 4 * a * c) % p
    sq = square_root(delta, p)
    if delta != 0: assert sq != 0
    sq1 = +sq
    sq2 = (p-sq) % p
    bot = pow(2 * a, -1, p)
    return ((-b + sq1) * bot) % p, ((-b + sq2) * bot) % p


"""
Find eigenvalues of a matrix m
"""
def eigenvals(m):
    a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]
    A = 1
    B = -(a + d)
    C = a * d - b * c
    return d2solve(A, B, C)


"""
Multiply A and B matrices
"""
def mult(A, B):
    C = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] %= p
    return C


"""
Find inverse of matrix M
"""
def inv(m):
    a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]
    det = (a * d - b * c) % p
    det = pow(det, -1, p)
    return [[d * det % p, -b * det % p], [-c * det % p, a * det % p]]


"""
Receives matrix `A` and its eigenvalues
Diagonalize matrix `A` and return its P such that (P^-1)A(P) == (matrix of eigenvalues)
"""
def Pof(A, ev):
    P = [[1, 1], [0, 0]]
    P[1][0] = -(A[0][0] - ev[0]) * pow(A[0][1], -1, p) % p
    P[1][1] = -(A[0][0] - ev[1]) * pow(A[0][1], -1, p) % p
    return P


"""
Return modular sqrt of a
"""
def square_root(a, p):
    # Tonelli–Shanks algorithm
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


"""
This function is used by square_root function
"""
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls
