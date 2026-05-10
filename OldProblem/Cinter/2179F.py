import sys
from collections import deque


def run1():
    n, m = map(int, input().split())
    G = {i: [] for i in range(1, n+1)}
    for _ in range(m):
        u, v = map(int, input().split())
        G[u].append(v)
        G[v].append(u)
    val = [-1] * (n + 1)# -1: none 0: red 1: blue 2: green
    q = deque()
    q.append(1)
    val[1] = 0
    while len(q) > 0:
        u = q.popleft()
        for v in G.get(u, []):
            if val[v] == -1:
                val[v] = (val[u] + 1) % 3
                q.append(v)
    color_map = 'rbg'
    ans = ''.join(color_map[x] for x in val[1:])
    return ans.strip()

def run2():
    q, = map(int, input().split())
    ans = []
    for _ in range(q):
        d, = map(int, input().split())
        s = input()
        color_map = {"r": 0, "b": 1, "g": 2}
        has = [0] * 3
        for i in range(d):
            has[color_map[s[i]]] = 1
            if sum(has) >= 2:
                break
        if sum(has) == 1:# all index same in this case
            ans.append(1)
            continue
        idonthave = has.index(0)# has 2 color neighbor
        best_move = (idonthave + 2) % 3# idonthave - 1
        for i in range(d):
            if color_map[s[i]] == best_move:
                ans.append(i + 1)
                break
    return '\n'.join(map(str, ans)).strip()

first = input()
t, = map(int, input().split())
for _ in range(t):
    if first == "first":
        print(str(run1()))
    else:
        print(str(run2()))
