def read_line() -> list[int]:
    return list(map(int, input().split()))

def run1():
    n, s = read_line()
    # because we only have n-1 bit, 2^(n-1) has n bit
    # can use s -= 1 instead but this is more clear 2^(n-1) now is 0
    if s >= (1 << (n - 1)): s = 0
    bit_s = bin(s)[2:].zfill(n)
    bit_arr = [int(x) for x in bit_s]
    for i in range(n - 1):
        u, v = read_line()
        min_u_v, max_u_v = min(u, v), max(u, v)
        if bit_arr[u - 1] ^ bit_arr[v - 1] == 0:
            print(min_u_v, max_u_v)
        else:
            print(max_u_v, min_u_v)

def unque_id(u, v):
    return min(u, v) + max(u, v) * 1000

def run2():
    n = int(input())
    # rebuild tree
    tree = {i: [] for i in range(1, n + 1)}
    direction = {}
    for i in range(n - 1):
        u, v = read_line()
        tree[u].append(v)
        tree[v].append(u)
        # we need direction of edge later
        direction[unque_id(u, v)] = int(u > v)
    
    bit_arr = [0] * (n + 1)# index from 1 to n and bit1 = 0
    visited = [False] * (n + 1)
    # dfs to restore bit_arr
    def dfs(u):
        visited[u] = True
        for v in tree[u]:
            if not visited[v]:
                bit_arr[v] = bit_arr[u] ^ direction[unque_id(u, v)]
                dfs(v)
    dfs(1)
    ans = int(''.join(map(str, bit_arr)), 2)
    # it must sync with run1, if ans is 0, it means s is 2^(n-1)
    # can use ans += 1 if run1 use s -= 1
    if ans == 0: ans = 1 << (n - 1)
    print(ans)
        

t, q = read_line()
for _ in range(t):
    if q == 1:
        run1()
    else:
        run2()