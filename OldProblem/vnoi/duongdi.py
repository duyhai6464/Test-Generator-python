import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

n, m = read(), read()

g = [read(str) for _ in range(n)]

dp = [[0] * m for _ in range(n)]
for i in range(n):
    if g[i][0] != '0':
        break
    dp[i][0] = 1
for i in range(m):
    if g[0][i] != '0':
        break
    dp[0][i] = 1

for i in range(1, n):
    for j in range(1, m):
        if g[i][j] != '1':
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

# for i in range(n):
#     debug(dp[i])
print(dp[n - 1][m - 1])