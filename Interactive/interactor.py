import sys
import random
from collections import deque

# ===== TEST CONFIG =====
sys.setrecursionlimit(200001)
T = 1000
HIDDEN = 0
N = 2

def search_path(start, end, D) -> list[int]:
    path = []
    track = start
    while track > 0:
        path.append(track)
        if track == end: return path
        track = D[track]
    path2 = []
    track = end
    while track > 0:
        path2.append(track)
        track = D[track]
    path2.reverse()
    for i, u in enumerate(path):
        if u in path2:
            j = path2.index(u)
            return path[:i] + path2[j:]
    print('no fucking way', file=sys.stderr)
    return []
        
        

def bfs(start, G: dict[int, list], D):
    q = deque()
    q.append(start)
    D[start] = 0
    while len(q) > 0:
        u = q.popleft()
        for v in G.get(u, []):
            if D[v] < 0:
                D[v] = u
                q.append(v)

def gen_binary_tree(n):
    q = deque()
    q.append(1)
    E = []
    while q:
        u = q.popleft()
        if 2 * u <= n:
            E.append((u, 2 * u))
            q.append(2 * u)
        if 2 * u + 1 <= n:
            E.append((u, 2 * u + 1))
            q.append(2 * u + 1)
    return E
        

def main(_test):
    query_count = 0
    # ===== PUBLIC INPUT =====
    global HIDDEN, N
    HIDDEN += 1 if _test % 10 == 0 else 0
    if HIDDEN > N:
        HIDDEN, N = 1, N + 1
    
    print(N, flush=True)
    MAX_QUERY = ((N + 1) >> 1)
    print(f"MAX QUERY {MAX_QUERY}", file=sys.stderr)

    G: dict[int, list] = {i : [] for i in range(1, N + 1)}
    E = []
    vdindex = list(range(1, N + 1))
    # random.shuffle(vdindex)
    for i in range(1, N):
        # edge vdindex[i] với 1 đỉnh ngẫu nhiên đã có
        # u, v = vdindex[i], random.choice(vdindex[:i])
        u = vdindex[i]
        if i < 3:
            v = vdindex[i - 1]
        else:
            v = 1 if i % 2 == 0 else vdindex[i - 1]
        E.append((u, v))
        G[u].append(v)
        G[v].append(u)
    
    # E = gen_binary_tree(N)
    # for u, v in E:
    #     G[u].append(v)
    #     G[v].append(u)
        
    random.shuffle(E)
    for u, v in E:
        if random.randint(0, 1):
            print(u, v, flush=True)
        else:
            print(v, u, flush=True)
            
    D = [-1] * (N + 1)
    bfs(1, G, D)
    
    # XY = random.choices(vdindex[-2:], k = 2)
    XY = [HIDDEN] * 2
    PATHXY = search_path(*XY, D=D)
        
    print(f"G:{G}\nE:{E}\nD:{D},PathXY: {PATHXY}", file=sys.stderr)
    
    # ===== INTERACTION =====
    while True:
        line = sys.stdin.readline()
        if not line:
            exit(1)

        parts = line.strip().split()

        if parts[0] == "?":
            u, v = map(int, parts[1:])

            query_count += 1
            if query_count > MAX_QUERY:
                print("Too many queries", file=sys.stderr)
                exit(1)

            # ===== CUSTOM LOGIC =====
            path = search_path(u, v, D)
            cross = any(x in PATHXY for x in path)
            print(path, cross, u, v, file=sys.stderr)
            print(1 if cross else 0, flush=True)

        elif parts[0] == "!":
            x = int(parts[1])
            # ===== CHECK ANSWER =====
            if x in PATHXY:
                print(f"AC in {query_count} queries", file=sys.stderr)
                return
            else:
                print(f"WA: expected {PATHXY}, got {x}", file=sys.stderr)
                exit(1)

if __name__ == "__main__":
    print(T, flush=True)
    for test in range(T):
        main(test)