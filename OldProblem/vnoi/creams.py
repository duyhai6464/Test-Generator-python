import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

n, t = read(), read()
a = [read() for _ in range(n)]

pre = [0] * (n + 1)
for i in range(n): pre[i + 1] = pre[i] + a[i]

fix = [1e9] * (n + 1)
for i in range(n - t, 0, -1):
    fix[i] = min(pre[i + t] - pre[i], fix[i + 1])

ans = 1e9
for i in range(n - 2 * t):
    ans = min(ans, pre[i + t] - pre[i] + fix[i + t + 1])

print(ans)