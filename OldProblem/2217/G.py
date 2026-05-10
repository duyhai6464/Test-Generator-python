import sys

data = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []

def read():
    global ptr
    if ptr >= len(data):
        raise Exception("No more input")
    res = data[ptr]
    ptr += 1
    return res

MOD = int(1e9 + 7)
MAXN = int(2e6 + 3)
fact = [1] * MAXN
inv_fact = [1] * MAXN
cats = [1] * (MAXN // 2)

def modInverse(x):
    return (pow(x, MOD - 2, MOD) + MOD) % MOD

def nCr(n, r):
    if r > n or r < 0:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

def catalan(n):
    return (nCr(2 * n, n) - nCr(2 * n, n - 1) + MOD * 2) % MOD

def precompute():
    fact[0] = 1
    for i in range(1, MAXN):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact[MAXN - 1] = modInverse(fact[MAXN - 1])
    for i in range(MAXN - 2, -1, -1):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD
    for i in range(MAXN // 2):
        cats[i] = catalan(i)
    # print some sample values to check
    # for i in range(10):
    #     print(f"Catalan({i}) = {cats[i]}")
    #     print(f"nCr({2*i}, {i}) = {nCr(2*i, i)}")

def solve_Z(n, k):
    if k < 0: return 0
    if k >= n: k = n
    F = [0] * (n + 1)
    F[0] = 1
    for i in range(1, n):
        F[i] = (2 * F[i - 1] - nCr(i - 1, k) + MOD * 2) % MOD
    res = 0
    for i in range(n):
        res = (res + cats[i] * cats[n - 1 - i] % MOD * F[i] % MOD * F[n - 1 - i] % MOD) % MOD
    return res

def run():
    n, k = read(), read()
    return (solve_Z(n, k) - solve_Z(n, k - 2) + MOD) % MOD
    
precompute()
t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))