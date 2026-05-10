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

def check(l, r, pre):
    s = l % 2
    if pre[s][r + 1] - pre[s][l] > pre[1 - s][r + 1] - pre[1 - s][l]:
        return 1
    return 0

def run():
    n = read()
    a = [[0] * n, [0] * n]
    pre = [[0] * (n + 1), [0] * (n + 1)]
    for i in range(n):
        a[i % 2][i] = read()
        for j in range(2):
            pre[j][i + 1] = pre[j][i] + a[j][i]
    ans = 0
    for l in range(n):
        ans += 1
        for r in range(l + 2, n, 2):
            ans += check(l, r, pre)
    return ans

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))