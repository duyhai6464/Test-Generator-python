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

def KMP(s: str):# kmp for s
    N = len(s) + 1
    kmp = [0] * N
    j = 0
    for i in range(2, N):
        while j > 0 and s[i - 1] != s[j]:
            j = kmp[j]
        if s[i - 1] == s[j]:
            j += 1
        kmp[i] = j
    return kmp

MAXN = int(1e6+9)
kmp = [0] * MAXN
b = [0] * MAXN
dp = [0] * MAXN

def run():
    n, q, s = read(), read(), read_t()
    for _ in range(q):
        l, r = read() - 1, read()
        j = 0
        for i in range(2, r - l + 1):
            while j > 0 and s[l + i - 1] != s[l + j]:
                j = kmp[j]
            if s[l + i - 1] == s[l + j]:
                j += 1
            kmp[i] = j
        for i in range(1, r - l + 1):
            if kmp[i] == 0:
                b[i] = 0
            elif kmp[kmp[i]] == 0:
                b[i] = kmp[i]
            else:
                b[i] = b[kmp[i]]
        ans = 0
        for i in range(1, r - l + 1):
            dp[i] = 1 if b[i] == 0 else dp[i - b[i]] + 1
            ans += dp[i]
                    
        # debug(l, r, kmp[:r - l + 1])
        # debug(s[l: r], b[:r - l + 1])
        # debug(dp[:r - l + 1])
        out.append(ans)
    # debug('---------------------')


t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))