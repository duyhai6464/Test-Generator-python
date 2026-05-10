import random
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def bfs(start, G, D):
    q = deque()
    q.append(start)
    D[start] = 0
    while len(q) > 0:
        u = q.popleft()
        for v in G.get(u, []):
            if D[v] < 0:
                D[v] = D[u] + 1
                q.append(v)

def generate_test():
    X = []
    with open(ROOT / "start.in", 'r') as f:
        data = list(map(int, f.read().split()))
        ptr = 1
        for _ in range(data[0]):
            n, m = data[ptr: ptr + 2]
            ptr += 2
            E = []
            G = {i: [] for i in range(1, n + 1)}
            for i in range(m):
                u, v = data[ptr: ptr + 2]
                ptr += 2
                E.append((u, v))
                G[u].append(v)
                G[v].append(u)
            D = [-1] * (n + 1)
            bfs(1, G, D)
            X.append({"n": n, "m": m, 'E': E, 'G': G, 'D': D})
        return X


def make_input_phase1(X):
    r = ["first", len(X)]
    for t in X:
        r.append(f"{t['n']} {t['m']}")
        for u, v in t['E']:
            r.append(f"{u} {v}")
    return '\n'.join(map(str, r))


def validate_phase1(X, output: str):
    # kiểm tra format
    lines = output.splitlines()
    if len(lines) != len(X):
        return False, None
    for i, t in enumerate(X):
        if len(lines[i]) != t['n']:
            return False, None
    # processed = dữ liệu truyền qua phase2
    return True, lines


def make_input_phase2(X, encoded_validate):
    r = ["second", len(X)]
    for i, t in enumerate(X):
        q = random.randint(1, t['n'] - 1)
        QUERY = random.sample(range(2, t['n'] + 1), q)
        t['QUERY'] = QUERY
        r.append(len(QUERY))
        for vertex in QUERY:
            a = []
            for v in t['G'].get(vertex, []):
                a.append(encoded_validate[i][v - 1])
            r.append(len(a))
            r.append("".join(a))
        
            
    return '\n'.join(map(str, r))


def validate_phase2(X, output: str):
    try:
        decoded = list(map(int, output.split()))
        ptr = 0
        for t in X:
            D = t['D']
            for vertex in t['QUERY']:
                edges_connected = t['G'].get(vertex, [])
                answer = decoded[ptr]
                ptr += 1
                if answer < 1 or answer > len(edges_connected):
                    return False
                if D[edges_connected[answer - 1]] >= D[vertex]:
                    return False
    except:
        return False
    return True
    