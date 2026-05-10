import sys

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

def add(bit, idx, val, size):
    while idx <= size:
        bit[idx] += val
        idx += idx & -idx


def prefix(bit, idx):
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s

MAXN = int(2e5 + 5)
V = [0] * MAXN
BIT1 = [0] * MAXN
BIT2 = [0] * MAXN

def run():
    n = read()
    a = [read() for _ in range(n)]
    for i in range(1, n + 1):
        V[i] = V[i - 1] + (a[i - 1] if i % 2 else -a[i - 1])
    # Nén tọa độ V(Coordinate Compression)
    C = sorted(list(set(V[:n + 1])))
    rank = {v: i + 1 for i, v in enumerate(C)}
    m = len(C)
    for i in range(m + 1):
        BIT1[i] = BIT2[i] = 0
    ans = 0
    add(BIT1, rank[0], 1, m)
    for j in range(1, n + 1):
        x = rank[V[j]]
        if j % 2:# TH1: l lẻ, r lẻ (l-1 chẵn)
            ans += prefix(BIT1, x - 1) # đếm v[j] > v[l-1]
            add(BIT2, x, 1, m)# thêm v[l-1] với l-1 = 0, 2, 4...
        else:# TH2: l chẵn, r chẵn (l-1 lẻ)
            ans += j // 2 - prefix(BIT2, x) # đếm v[j] < v[l-1]
            add(BIT1, x, 1, m) # thêm v[l-1] với l-1 = 1, 3, 5...
    # debug(n, m)
    # debug(V[:n+1])
    # debug([rank(v) for v in V[:n+1]])
    return ans

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))