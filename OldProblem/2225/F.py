import sys
import random

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr = 0
out = []
def read(base: int = 10) -> int:
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return int(buffer[ptr - 1], base)

def read_t(t: type = str):
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    if t != str: return t(buffer[ptr - 1])
    return buffer[ptr - 1]

NMOD = 1
MODD = list(map(int, [1e9+17107, 1e9+3999, 1e9+9999, 1e9+403, 1e9+2727, 1e9+2907, 1e9+7929]))
MODD = random.sample(MODD, NMOD)
BASE = random.randint(256, MODD[0] - 1)
MAXN = int(1e6+5)
pw = [[0] * (MAXN) for i in range(NMOD)]
for i in range(NMOD):
    pw[i][0] = 1
    for j in range(1, MAXN):
        pw[i][j] = pw[i][j - 1] * BASE % MODD[i]
# n, s = 6, "string"
# pre = [[0] * (n + 1) for i in range(NMOD)]
# for i in range(NMOD):
#     for j in range(1, n + 1):
#         pre[i][j] = (pre[i][j - 1] + ord(s[j - 1]) * pw[i][j - 1]) % MODD[i]

def get_hash(l, r, pre, pw, mod):
    return (pre[r] - pre[l - 1] + mod) % mod * pw[MAXN - l] % mod

def cmp_hash(l1, r1, l2, r2, pre):
    for i in range(NMOD):
        if get_hash(l1, r1, pre[i], pw[i], MODD[i]) != get_hash(l2, r2, pre[i], pw[i], MODD[i]):
            return False
    return True

def LCP(l1, r1, l2, r2, pre):
    rx = min(r1 - l1, r2 - l2)
    lx = 0
    while lx < rx:
        mid = (lx + rx) >> 1
        if cmp_hash(l1, l1 + mid, l2, l2 + mid, pre):
            lx = mid + 1
        else:
            rx = mid
    # print(l1, l2, lx, file=sys.stderr)
    # print(get_hash(l1 + lx, l1 + lx, pre), get_hash(l2 + lx, l2 + lx, pre), file=sys.stderr)
    return lx

def run():
    n, l, k, s = read(), read(), read(), read_t()
    if n < l * k: return "NO"
    out.append("YES")
    # print(n, l, k , s, file=sys.stderr)
    if k == 1:
        return s
    pre = [[0] * (n + 1) for i in range(NMOD)]
    for i in range(NMOD):
        for j in range(1, n + 1):
            pre[i][j] = (pre[i][j - 1] + ord(s[j - 1]) * pw[i][j - 1]) % MODD[i]
    # find max r in l=left with s[1:n] split in k part
    find_max_r = lambda left: n - (k - 1 - min((left - 1) // l, k - 1)) * l
    res_l = 1
    res_r = find_max_r(res_l)
    # print(res_l, res_r, file=sys.stderr)
    for x in range(2, n + 1):
        if x - 1 > 0 and x - 1 < l: continue
        max_r = find_max_r(x)
        if max_r - x + 1 < l: continue
        ind = LCP(res_l, res_r, x, max_r, pre)
        # print(x, max_r, ind, file=sys.stderr)
        if s[res_l - 1 + ind] != s[x - 1 + ind]:
            if s[res_l - 1 + ind] < s[x - 1 + ind]:
                res_l, res_r = x, max_r
        else:
            if max_r - x > res_r - res_l:
                res_l, res_r = x, max_r
    # print(res_l, res_r, file=sys.stderr)
    # print(file=sys.stderr)
    return s[res_l - 1: res_r]

debug(BASE, MODD)
t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))