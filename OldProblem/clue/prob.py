import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []

def read(t: type = int):
    global buffer, ptr
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def calc(sub: list[tuple]):
    best = 0
    for i in range(1, len(sub)):
        if sub[i][1] > sub[best][1]:
            best = i
    base = sub[best][1], sub[best][0] + best * 20 if sub[best][1] > 0 else 0
    max_gain = 100 - sub[best][1], sub[0][0] - base[1]
    m = lambda x: sub[x][1] if x != best else 0
    best2 = 0
    for i in range(1, len(sub)):
        if m(i) > m(best2):
            best2 = i
    base2 = m(best2), sub[best2][0] + best2 * 20 if m(best2) > 0 else 0
    min_gain = base2[0] - base[0], base2[1] - base[1]
    return base, max_gain, min_gain

from bisect import bisect_left
from collections import defaultdict
n, m = read(), read()
d: dict[str, dict[str, list[tuple]]] = defaultdict(lambda: defaultdict(list))
r: list[tuple] = []
b: list[tuple] = []

for _ in range(n):
    name, prob, pen, point = read(str), read(str), read(), read()
    d[name][prob].append((pen, point))

for name, data in d.items():
    bpoint, bpen, maxpoi, maxpen, minpoi, minpen = 0, 0, -1e18, 0, 1e18, 0
    for prob, submit in data.items():
        base, maxg, ming = calc(submit)
        bpoint += base[0]
        bpen += base[1]
        if maxpoi < maxg[0] or (maxpoi == maxg[0] and maxpen > maxg[1]):
            maxpoi, maxpen = maxg
        if minpoi > ming[0] or (minpoi == ming[0] and minpen < ming[1]):
            minpoi, minpen = ming
    base = (bpoint, -bpen)
    maxp = (bpoint + maxpoi, -bpen-maxpen)
    minp = (bpoint + minpoi, -bpen-minpen)
    r.append((base, maxp, minp))
    b.append((base, len(r) - 1))

bkey = lambda x: x[0]
b.sort(key=bkey)
k = min(36, m // 10 + int(m % 10 != 0))
ncontestant = len(b)
res: list[str] = []
# debug(b)
for i, name in enumerate(d.keys()):
    index_max = bisect_left(b, r[i][1], key=bkey)
    # debug(name, i, index_max)
    if ncontestant - index_max < k:
        res.append(name)
        continue
    index_base = bisect_left(b, r[i][0], key=bkey)
    if ncontestant - index_base > k + 1:
        continue
    for j in range(k):
        xj = b[-1-j][1]
        if r[xj][2] < r[i][0]:
            res.append(name)
            break

for name in sorted(set(res)): print(name)