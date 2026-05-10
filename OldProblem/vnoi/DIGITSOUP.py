import sys


MOD = 10**9 + 7


def digits(x: int) -> int:
    return len(str(x))


def build_group_poly(count: int, weight: int, inv: list[int]) -> list[int]:
    poly = [1] * (count + 1)
    for i in range(1, count + 1):
        poly[i] = poly[i - 1] * (count - i + 1) % MOD
        poly[i] = poly[i] * inv[i] % MOD
        poly[i] = poly[i] * weight % MOD
    return poly


def convolve(a: list[int], b: list[int]) -> list[int]:
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            res[i + j] = (res[i + j] + ai * bj) % MOD
    return res


def solve_case(a: list[int]) -> int:
    n = len(a)
    if n == 0:
        return 0
    if n == 1:
        return a[0] % MOD

    cnt = [0] * 10
    total = [0] * 10
    for value in a:
        d = digits(value)
        cnt[d] += 1
        total[d] = (total[d] + value) % MOD

    inv = [0] * (n + 2)
    inv[1] = 1
    for i in range(2, n + 2):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD

    poly = [1]
    for d in range(1, 10):
        if cnt[d] == 0:
            continue
        weight = (pow(10, d, MOD) - 1) % MOD
        poly = convolve(poly, build_group_poly(cnt[d], weight, inv))

    fact = 1
    for i in range(2, n + 1):
        fact = fact * i % MOD

    ans = 0
    for d in range(1, 10):
        if cnt[d] == 0:
            continue
        weight = (pow(10, d, MOD) - 1) % MOD
        q = [0] * n
        q[0] = 1
        for i in range(1, n):
            q[i] = (poly[i] - weight * q[i - 1]) % MOD

        coef = 0
        for i in range(n):
            coef = (coef + q[i] * inv[i + 1]) % MOD

        ans = (ans + total[d] * fact % MOD * coef) % MOD
    return ans

data = list(map(int, sys.stdin.read().split()))
print(solve_case(data[1:]))
