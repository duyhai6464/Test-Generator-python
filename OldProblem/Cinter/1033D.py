import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = []
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

pos: dict[int, int] = {}
a: list[int] = []

for i in range(read()):
    n = read()
    for i in [4, 3, 2]:
        x = int(round(n ** (1.0 / i)))
        if x ** i == n:
            pos[x] = pos.get(x, 0) + i
            break
    else:
        a.append(n)

b = a + list(pos.keys())
pos2 = {}
for v in a:
    for u in b:
        if u == v: continue
        g = gcd(v, u)
        if g != 1:
            for x in [g, v // g]:
                pos[x] = pos.get(x, 0) + 1
            break
    else:
        pos2[v] = pos2.get(v, 0) + 1
            


MOD = 998244353
res = 1
for p in pos.values(): res = res * (p + 1) % MOD
debug(res)
for p in pos2.values(): res = res * (p + 1) % MOD * (p + 1) % MOD
debug(a)
debug(pos, pos2)
print(res)