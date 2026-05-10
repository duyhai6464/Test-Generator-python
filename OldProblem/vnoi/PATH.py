import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

sys.setrecursionlimit(int(1e6))

def run():
    n = read()
    E = []
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = read(), read()
        E.append((u, v))
        adj[u].append(v)
        adj[v].append(u)
    
    order = []
    par = [-1] * (n + 1)
    stack = [1]
    par[1] = 0
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if par[v] < 0:
                par[v] = u
                stack.append(v)
    
    ccount = [1] * (n + 1)
    for u in reversed(order):
        if par[u] > 0:
            ccount[par[u]] += ccount[u]
    
    # debug(par, ccount)
    for u, v in E:
        if par[v] != u: u, v = v, u
        # now par[v] == u
        # debug(u, v, ccount[v])
        out.append((n - ccount[v]) * ccount[v] % 67)
                

t = 1
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))