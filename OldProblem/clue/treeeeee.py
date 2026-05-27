import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n = read()
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = read(), read()
        adj[u].append(v)
        adj[v].append(u)
    order = []
    parent = [-1] * (n + 1)
    stack = [1]
    parent[1] = 0
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if parent[v] < 0:
                parent[v] = u
                stack.append(v)
    dp = [[0, 1] for _ in range(n + 1)]
    for u in reversed(order):
        p = parent[u]
        if p != 0:
            dp[p][0] += max(dp[u])
            dp[p][1] += dp[u][0]
    F0 = [0 for _ in range(n + 1)]
    F1 = [0 for _ in range(n + 1)]
    F0[1] = dp[1][0]
    F1[1] = dp[1][1]
    for u in order:
        for v in adj[u]:
            if v != parent[u]:
                rem_u0 = F0[u] - max(dp[v][0], dp[v][1])
                rem_u1 = F1[u] - dp[v][0]
                
                F0[v] = dp[v][0] + max(rem_u0, rem_u1)
                F1[v] = dp[v][1] + rem_u0
    
    K = 0
    for i in range(1, n + 1):
        if F1[i] > F0[i]:
            K += 1
            
    # debug(dp)
    # debug(F0)
    # debug(F1)

    total_pairs = n * (n - 1) // 2
    invalid_pairs = K * (K - 1) // 2
    return total_pairs - invalid_pairs
    
print(run())