import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []

def read(t: type = int):
    global buffer, ptr
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run(n, k):
    if n == k: return -1
    if n < k: return n
    LIMIT = 400
    if n <= LIMIT: return max(calc_dp(n, k))
    w = [0, 2, 3, 2, 3, 2, 4, 2, 3][k]
    q = (n - LIMIT) // w
    rem_n = n - w * q
    dp = calc_dp(rem_n, k)
    ans = -1
    SIZE = 1 << (k + 1)
    MASK = SIZE - 1
    for mask in range(SIZE):
        if dp[mask] == -1:
            continue
        m = mask
        steps = min(q, k + 2) 
        for _ in range(steps):
            m = m | ((m << w) & MASK)
            if m & (1 << k):
                break
        else:
            ans = max(ans, dp[mask] + q)
    return ans

def calc_dp(n, k):
    size = 1 << (k + 1)
    MASK = size - 1
    dp = [[-1] * size for _ in range(n + 1)]
    dp[0][1] = 0
    for w in range(n):
        for mask in range(size):
            if dp[w][mask] == -1: continue
            for v in range(1, 2 * k + 2):
                if w + v > n: continue
                nexmask = mask | ((mask << v) & MASK) if v <= k else mask
                if not (nexmask & (1 << k)):
                    if dp[w][mask] + 1 > dp[w + v][nexmask]:
                        dp[w + v][nexmask] = dp[w][mask] + 1
    return dp[n]

# for k in range(1, 3):
#     for n in range(1, 20):
#         debug(f"k:{k} n:{n} f:{run(n, k)}")
#         debug('--------------')

t = read()
for _ in range(t):
    output = run(read(), read())
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))