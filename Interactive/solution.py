import sys

def trace(u: int, D: list, visited: list):
    while D[u] > 0 and not visited[u]:
        visited[u] = True
        u = D[u]
    visited[u] = True
    return u

def getpath(u: int, D: list, visited: list):
    path = []
    while D[u] > 0 and not visited[u]:
        path.append(u)
        visited[u] = True
        u = D[u]
    if not visited[u]:
        path.append(u)
        visited[u] = True
    return path

def binary_s(path: list):
    l, r = 0, len(path) - 1
    while l < r:
        mid = (l + r) >> 1
        if ask(path[l], path[mid]):
            r = mid
        else:
            l = mid + 1
    return path[l]

def ask(u, v):
    print("?", u, v, flush=True)
    return read()

def answer(k):
    print('!', k, flush=True)

buffer:list[int] = []
ptr = 0
def read() -> int:
    global ptr, buffer
    if ptr >= len(buffer):
        buffer.extend(map(int, input().split()))
    ptr += 1
    return buffer[ptr - 1]

def run():
    n = read()
    G = {i: [] for i in range(1, n + 1)}
    for _ in range(n - 1):
        u, v = read(), read()
        G[u].append(v)
        G[v].append(u)
    for i in range(1, n + 1):
        G[i] = sorted(G[i])
    D = [-1] * (n + 1)
    order = []
    stack = [1]
    D[1] = 0
    V = []
    # duyệt dfs lấy order và D(parent)
    while stack:
        u = stack.pop()
        order.append(u)
        if len(G.get(u, [])) == 1: V.append(u)
        for v in G.get(u, []):
            if D[v] < 0:
                D[v] = u
                stack.append(v)
    # đếm số lượng con là lá gốc v bằng cách duyệt ngược order
    countChild = [0] * (n + 1)
    for v in V: countChild[v] = 1
    for u in reversed(order):
        if D[u] > 0:
            countChild[D[u]] += countChild[u]
    # chọn root là trọng tâm (Centroid) của các nút là(k phải toàn cây)
    root = -1
    for u in order:
        is_centroid = True
        if len(V) - countChild[u] > len(V) // 2:
            continue
        for v in G.get(u, []):
            if v != D[u] and countChild[v] > len(V) // 2:
                is_centroid = False
                break
        if is_centroid:
            root = u
            break
    # dfs lại từ root + lưu các đỉnh lá
    print(f'Centroid {root}', file=sys.stderr)
    V.clear()
    stack = [root]
    D = [-1] * (n + 1)
    D[root] = 0
    while stack:
        u = stack.pop()
        order.append(u)
        if len(G.get(u, [])) == 1: V.append(u)
        for v in G.get(u, []):
            if D[v] < 0:
                D[v] = u
                stack.append(v)
    print(f"dfs order: {order}", file=sys.stderr)
    vis = [False] * (n + 1)
    if len(V) == 2:
        path = getpath(V[0], D, vis)
        path2 = list(reversed(getpath(V[1], D, vis)))
        print(f'only 2 {V} {path} {path2}', file=sys.stderr)
        return binary_s(path + path2)
    k = (len(V) + 1) >> 1
    found = -1
    for i in range(k - 1):
        u, v = V[i], V[i + k]
        if ask(u, v):
            found = i
            break
        trace(u, D, vis)
        trace(v, D, vis)
    if found == -1:
        if len(V) % 2:
            print(f"not found so it's {V[k - 1]}", file=sys.stderr)
            return binary_s(getpath(V[k - 1], D, vis))
        found = k - 1
    path = getpath(V[found], D, vis) 
    path2 = list(reversed(getpath(V[found + k], D, vis)))
    return binary_s(path + path2)


t = int(read())
for _ in range(t):
    answer(run())