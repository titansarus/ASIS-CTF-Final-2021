from Crypto.Util.number import isPrime


N = 56469405750402193641449232753975279624388972985036568323092258873756801156079913882719631252209538683205353844069168609565141017503581101845476197667784484712057287713526027533597905495298848547839093455328128973319016710733533781180094847568951833393705432945294907000234880317134952746221201465210828955449


def getb(a):
    lower = 500 // (a.bit_length())
    for b in range(lower, 1000):
        num = a ** b
        if num.bit_length() == 512:
            return b
        if num.bit_length() > 512:
            return -1


def solve():
    cands = []
    for a in range(2, 513):
        b = getb(a)
        if b not in range(32, 513):
            continue
        cands.append((a, b))

    print(len(cands))
    ans = []
    for a in cands:
        le = a[0] ** a[1]
        le += le % 2
        for b in cands:
            ri = b[0] ** b[1]
            ri += ri % 2

            if le * ri < N and (N - le * ri).bit_length() < 600:
                ans.append((a, b))

    print('Count:', len(ans))
    print('\n'.join(map(str, ans)))


if __name__ == '__main__':
    solve()
