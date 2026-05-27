import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)

# MAXP = int(1e6)
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

def phong(x):
    cnt = 1
    for p in range(2, round(x ** 0.5) + 1):
        if p * p > x: break
        if x % p: continue
        cnt += p
        if p != x // p:
            cnt += x // p
        if cnt > x:
            return True
    return False


n = int(input())

for x in range(n, n + 10 ** 7):
    if phong(x):
        print(x)
        break
