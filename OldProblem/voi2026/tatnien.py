import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
# sys.stdin = open('TET.INP', 'r')
# sys.stdout = open('TET.OUT', 'w')
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []

def read(t: type = int):
    global buffer, ptr
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def getp(u: int):# dsu by dom
    root = u
    while par[root] > 0: root = par[root]
    while u != root:
        parent = par[u]
        par[u] = root
        u = parent
    return root

def union(u: int, v: int):
    global max_div
    freq_local = freq_map
    pair_local = pair_sum
    u, v = getp(u), getp(v)
    if u == v: return
    if u > v: u, v = v, u
    par[u] += par[v]
    par[v] = u
    
    freq_u, freq_v = freq_local[u], freq_local[v]
    if len(freq_u) < len(freq_v):
        dict_src, dict_dest = freq_u, freq_v
    else:
        dict_src, dict_dest = freq_v, freq_u
    p_new = pair_local[u] + pair_local[v]
    for val, c2 in dict_src.items():
        c1 = dict_dest.get(val)
        if c1 is not None:
            p_new += c1 * c2
            dict_dest[val] = c1 + c2
        else:
            dict_dest[val] = c2
    pair_local[u] = p_new
    freq_local[u] = dict_dest
    freq_local[v] = None # type: ignore
    
    L = -par[u]
    div = 1 + L * (L - 1) // 2 - p_new
    if div > max_div:
        max_div = div
    
n, t = read(), read()
a = [read() for _ in range(n)]
q = [read() for _ in range(t)]

# from bisect import bisect_left
# b = sorted(set(a))
# a = [bisect_left(b, v) for v in a]# rời rạc hóa mảng a
freq_map = [{} for _ in range(n + 1)] 
pair_sum = [0] * (n + 1)
par = [0] * (n + 1)
max_div = 1
deleted = [False] * (n + 1)
for i in q: deleted[i] = True
for i in range(1, n + 1):
    if not deleted[i]:
        par[i] = -1
        freq_map[i][a[i - 1]] = 1

for i in range(1, n):
    if par[i] != 0 and par[i + 1] != 0:
        union(i, i + 1)

ans = []
for i in reversed(q):
    ans.append(max_div)
    par[i] = -1
    freq_map[i][a[i - 1]] = 1
    if i > 1 and par[i - 1] != 0:
        union(i - 1, i)
    if i < n and par[i + 1] != 0:
        union(i, i + 1)

print('\n'.join(map(str, reversed(ans))))
