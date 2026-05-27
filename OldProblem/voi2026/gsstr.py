import sys

def debug(*x, **y): print('---', *x, file=sys.stderr, **y)

s = 'aaaabbbbca'
query = [0]

def ask(q: str, t: str):
    query[0] += 1
    print(q, t, flush=True)
    if sys.stdin.isatty():
        l = lcs(t)
        debug(l)
        return l
    return int(input())

def lcs(t):
    x = len(t)
    y = len(s)
    dp = [[0] * (y + 1) for _ in range(x + 1)]
    for i in range(1, x + 1):
        for j in range(1, y + 1):
            if t[i - 1] == s[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # for i in range(1, x + 1): debug(i, dp[i])
    return dp[x][y]

def read():
    if sys.stdin.isatty():
        debug(len(s))
        return len(s)
    return int(input())

def build(cur: list, base: int, cnt: int, b: str):
    pos, cntb = 0, 0
    while cntb < cnt:
        if pos == len(cur):
            cur.extend([b] * (cnt - cntb))
            break
        cur.insert(pos, b)
        ans = ask('?', ''.join(cur))
        if ans == -1: exit(67)
        if ans > base:
            base += 1
            cntb += 1
        else:
            cur.pop(pos)
        pos += 1

def solve():
    n = read()
    a = ask('?', 'a' * n)
    b = ask('?', 'b' * n)
    c = n - a - b
    if a == n: return 'a' * n
    if b == n: return 'b' * n
    if c == n: return 'c' * n
    r = [(a, 'a'), (b, 'b'), (c, 'c')]
    r.sort()
    cur = [r[0][1]] * r[0][0]
    build(cur, r[0][0], r[1][0], r[1][1])
    build(cur, r[0][0] + r[1][0], r[2][0], r[2][1])
    debug(n, query, r)
    return ''.join(cur)

print('!', solve(), flush=True)
