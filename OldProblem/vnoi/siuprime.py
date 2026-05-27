import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)


MAXP = int(1e6)
primediv = [1] * MAXP
for i in range(2, int(MAXP ** 0.5 + 1)):
    if primediv[i] == 1:
        for j in range(i * i, MAXP, i):
            primediv[j] = i
primes = []
for i in range(2, MAXP):
    if primediv[i] == 1:
        primediv[i] = i
        primes.append(i)

siuprimes = [[2, 3, 5, 7]]

def is_p(n):
    for p in primes:
        if n % p == 0: return False
        if p * p > n: break
    return True

for i in range(1, 12):
    siu = []
    for v in siuprimes[i - 1]:
        for x in [1, 3, 7, 9]:
            n = 10 * v + x
            if n < MAXP:
                if primediv[n] == n:
                    siu.append(n)
            else:
                if is_p(n):
                    siu.append(n)
    siuprimes.append(siu)

ALL = []
for i in range(1, 12):
    debug(siuprimes[i])
    ALL.extend(siuprimes[i])

from bisect import bisect, bisect_left
a, b = map(int, input().split())

print(bisect(ALL, b) - bisect_left(ALL, a))
