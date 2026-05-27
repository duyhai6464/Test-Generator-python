import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)

# SOLVE 1
def solve1(n):
    res = 2 if n > 1 else 1
    for i in range(2, int(n ** 0.5 + 1)):
        if n % i == 0:
            res += 1
            if n // i != i:
                res += 1
    print(res)

# SOLVE 2
def solve2(n):
    ps = [] # a0**p0 * a1**p1 * ... * ax**px
    x = 2
    while x * x <= n > 1:
        p = 0
        while n and n % x == 0:
            n //= x
            p += 1
        if p:
            ps.append(p)
        x += 1
    if n > 1: ps.append(1)
    res = 1
    for p in ps: res *= p + 1
    print(res)

# SOLVE 3
def solve3(n):
    ps = [] # a0**p0 * a1**p1 * ... * ax**px
    x = 2
    while x * x <= n > 1 and x < 1e6:
        p = 0
        while n and n % x == 0:
            n //= x
            p += 1
        if p:
            ps.append(p)
        x += 1
    res = 1
    for p in ps: res *= p + 1
    if n <= 1:
        return print(res)
    x = int(n ** 0.5)
    if x * x == n:
        return print(res * 3)
    # kiểm tra nguyên tố bằng Miller-Rabin
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
    M, s = n - 1, 0
    while M % 2 == 0:
        M >>= 1
        s += 1
    # M = 2^s * d (M = d now)
    def check_composite(n, a, s, d):
        x = pow(a, d, n)
        if x == 1 or x == n - 1: return False
        for _ in range(1, s):
            x = x * x % n
            if x == n - 1: return False
        return True
    
    for a in primes:
        if check_composite(n, a, s, M):
            return print(res * 4)
    print(res * 2)


n = int(input())
# n < 1e18 count number of divisors of N
# solve1(n)
# solve2(n)
solve3(n)

# MAXP = int(1e7)
# primediv = [1] * MAXP
# for i in range(2, int(MAXP ** 0.5 + 1)):
#     if primediv[i] == 1:
#         for j in range(i * i, MAXP, i):
#             primediv[j] = i
# primes = []
# for i in range(2, MAXP):
#     if primediv[i] == 1:
#         primediv[i] = i
#         primes.append(i)