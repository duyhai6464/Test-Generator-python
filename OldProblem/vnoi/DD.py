import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = []
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def query(l: int, r: int) -> int:
    print(f"? {l} {r}", flush=True)
    return read()

def run():
    n = read()
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = query(1, i)
    B = [0] * (n + 2)
    for i in range(1, n + 1):
        B[i] = query(i, n)

    nodes = set()
    for i in range(1, n + 1):
        nodes.add((i, i))
    for r in range(1, n + 1):
        for k in range(r - 1, -1, -1):
            if A[k] == A[r] - 1:
                l = k + 1
                nodes.add((l, r))
                break
                
    for l in range(1, n + 1):
        for k in range(l + 1, n + 2):
            if B[k] == B[l] - 1:
                r = k - 1
                nodes.add((l, r))
                break

    internal_nodes = [res for res in nodes if res[0] < res[1]]
    internal_nodes.sort(key=lambda x: x[1] - x[0])
    
    range_to_id = {}
    for i in range(1, n + 1):
        range_to_id[(i, i)] = i
        
    for idx, segment in enumerate(internal_nodes):
        range_to_id[segment] = n + 1 + idx

    a = {}
    b = {}

    for segment in internal_nodes:
        l, r = segment
        p = range_to_id[segment]
        
        best_m = -1
        for m in range(l, r):
            if (l, m) in range_to_id:
                best_m = max(best_m, m)
        a[p] = range_to_id[(l, best_m)]
        
        best_m_prime = n + 1
        for m_prime in range(l + 1, r + 1):
            if (m_prime, r) in range_to_id:
                best_m_prime = min(best_m_prime, m_prime)
        b[p] = range_to_id[(best_m_prime, r)]

    print('!', end=" ")
    for p in range(n + 1, 2 * n):
        print(f"{a[p]} {b[p]}", end=" ")
    print(flush=True)

t = read()
for _ in range(t):
    run()