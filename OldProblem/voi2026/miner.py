import sys, random

def debug(*x, **y): print('---', *x, file=sys.stderr, **y)

def answer(*args): print(*args, flush=True)

def show(grid):
    def line(row, space):
        for i, v in enumerate(row):
            print(f"{str(v)[:2]:>{space[i]}}", file=sys.stderr, end='|' if i + 1 != len(row) else '\n')
    s = [4] * (len(grid[0]) + 1)
    line(['**'] + list(range(1, M + 1)), s)
    for i in range(1, N + 1): line([i] + grid[i][1:-1], s)
    
N, M, K = 5, 5, 6
g = [[0] * (M + 2) for _ in range(N + 2)]
p = [(i, j) for i in range(1, N + 1) for j in range(1, M + 1)]
rng = random.Random(67)
mine = rng.sample(p, K)
for i, j in mine: g[i][j] = 1
quer = [0, 0]

def ask(*args):
    print(*args, flush=True)
    if sys.stdin.isatty():
        x, y = args
        quer[0] += 1
        if g[x][y] == 1:
            quer[1] += 1
            return -1
        cnt = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0: continue
                nx, ny = x + i, y + j
                cnt += g[nx][ny]
        debug(cnt)
        return cnt
    return int(input())

def read():
    if sys.stdin.isatty(): return 1
    return int(input())

def readline():
    if sys.stdin.isatty(): return N, M, K
    return map(int, input().split())

def solve(params):
    n, m, k = params
    total = n * m

    def idx(x, y):
        return (x - 1) * m + y - 1

    def pos(v):
        return v // m + 1, v % m + 1

    xs = [v // m + 1 for v in range(total)]
    ys = [v % m + 1 for v in range(total)]
    neighbors = [[] for _ in range(total)]
    for x in range(1, n + 1):
        for y in range(1, m + 1):
            v = idx(x, y)
            for dx in (1, -1, 0):
                for dy in (0, 1, -1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 1 <= nx <= n and 1 <= ny <= m:
                        neighbors[v].append(idx(nx, ny))

    bom = bytearray(total)
    vis = bytearray(total)
    cbom = [0] * total
    fbom = [0] * total
    cvis = bytearray(total)
    known_bom = bytearray(total)
    mvis = bytearray(len(nei) for nei in neighbors)
    mines = []
    mine_set = set()
    frontier = []
    in_frontier = bytearray(total)
    dirty = []
    in_dirty = bytearray(total)
    dirty_clues = []
    in_dirty_clue = bytearray(total)
    fallback_order = list(range(total))
    fallback_order.sort(key=lambda v: (mvis[v], rng.randrange(total)))

    def add_frontier(v):
        if not vis[v] and cvis[v] and not in_frontier[v]:
            in_frontier[v] = 1
            frontier.append(v)

    def add_dirty(v):
        if not vis[v] and not in_dirty[v]:
            in_dirty[v] = 1
            dirty.append(v)

    def add_dirty_clue(v):
        if vis[v] and not bom[v] and not in_dirty_clue[v]:
            in_dirty_clue[v] = 1
            dirty_clues.append(v)

    def refresh(v):
        for c in neighbors[v]:
            fbom[c] = cbom[c] - known_bom[c]
            add_frontier(c)
            add_dirty_clue(c)
            add_dirty(c)
            for u in neighbors[c]:
                add_dirty(u)
                add_dirty_clue(u)
        fbom[v] = cbom[v] - known_bom[v]
        add_frontier(v)
        add_dirty_clue(v)
        add_dirty(v)
        for u in neighbors[v]:
            add_dirty(u)
            add_dirty_clue(u)

    def visit(v, is_mine):
        if not vis[v]:
            vis[v] = 1
            for c in neighbors[v]:
                cvis[c] += 1
        if is_mine and not bom[v]:
            bom[v] = 1
            mines.append(v)
            mine_set.add(v)
            for c in neighbors[v]:
                known_bom[c] += 1
        refresh(v)

    def mark_mine(v):
        visit(v, True)

    def get(v, res):
        if res == -1:
            visit(v, True)
        else:
            cbom[v] = res
            visit(v, False)

    def check(v, as_mine):
        for c in neighbors[v]:
            if not vis[c] or bom[c]:
                continue
            cur = known_bom[c] + (1 if as_mine else 0)
            if cur > cbom[c] or cur + mvis[c] - cvis[c] - 1 < cbom[c]:
                return False
        return True

    def choose_fallback():
        dense = k * 4 >= total
        best_score = 10.0
        best_peak = 10.0
        best_avg = 10.0
        best_cnt = -1
        best_deg = -1
        candidates = []
        eps = 0.012
        for v in frontier:
            if vis[v]:
                continue
            risk_sum = 0.0
            risk_peak = 0.0
            cnt = 0
            for c in neighbors[v]:
                if vis[c] and not bom[c] and cvis[c] < mvis[c]:
                    p = fbom[c] / (mvis[c] - cvis[c])
                    cnt += 1
                    risk_sum += p
                    if p > risk_peak:
                        risk_peak = p
            if cnt:
                risk_avg = risk_sum / cnt
                risk = risk_avg if dense else risk_peak * 0.70 + risk_avg * 0.30
                deg = mvis[v]
                if dense:
                    better = risk < best_score - eps or (
                        risk <= best_score + eps and (
                            cnt > best_cnt or (cnt == best_cnt and deg > best_deg)
                        )
                    )
                    near = risk <= best_score + eps and cnt == best_cnt and deg == best_deg
                else:
                    better = risk < best_score - eps or (
                        risk <= best_score + eps and (
                            risk_peak < best_peak - eps or (
                                risk_peak <= best_peak + eps and (
                                    risk_avg < best_avg - eps or (
                                        risk_avg <= best_avg + eps and (
                                            cnt > best_cnt or (cnt == best_cnt and deg > best_deg)
                                        )
                                    )
                                )
                            )
                        )
                    )
                    near = risk <= best_score + eps and risk_peak <= best_peak + eps and risk_avg <= best_avg + eps

                if better:
                    best_score = risk
                    best_peak = risk_peak
                    best_avg = risk_avg
                    best_cnt = cnt
                    best_deg = deg
                    candidates = [v]
                elif near:
                    if len(candidates) < 32:
                        candidates.append(v)
                    elif rng.randrange(32) == 0:
                        candidates[rng.randrange(32)] = v
        if candidates:
            return candidates[rng.randrange(len(candidates))]

        while fallback_order:
            v = fallback_order.pop()
            if not vis[v]:
                return v
        return -2

    def helper():
        # Single-cell feasibility. If a frontier cell can only be safe, query it;
        # if it can only be a mine, mark it without spending a query.
        while dirty:
            v = dirty.pop()
            in_dirty[v] = 0
            if vis[v] or cvis[v] == 0:
                continue
            can_mine = check(v, True)
            can_safe = check(v, False)
            if can_safe and not can_mine:
                return v
            if can_mine and not can_safe:
                mark_mine(v)
                return -1

        # Local subset rule, equivalent to the second block
        while dirty_clues:
            c = dirty_clues.pop()
            in_dirty_clue[c] = 0
            if fbom[c] < 1 or cvis[c] >= mvis[c]:
                continue
            cx, cy = xs[c], ys[c]
            for nx in range(max(1, cx - 1), min(n, cx + 1) + 1):
                base = (nx - 1) * m
                for ny in range(max(1, cy - 1), min(m, cy + 1) + 1):
                    d = base + ny - 1
                    if not vis[d] or bom[d] or fbom[d] < 1 or fbom[d] > fbom[c]:
                        continue

                    rest_unknown = mvis[c] - cvis[c]
                    ok_subset = True
                    for u in neighbors[d]:
                        if vis[u]:
                            continue
                        ux, uy = xs[u], ys[u]
                        if not (cx - 1 <= ux <= cx + 1 and cy - 1 <= uy <= cy + 1):
                            ok_subset = False
                            break
                        rest_unknown -= 1
                    if not ok_subset:
                        continue

                    diff_need = fbom[c] - fbom[d]
                    if diff_need == 0:
                        for u in neighbors[c]:
                            if vis[u]:
                                continue
                            ux, uy = xs[u], ys[u]
                            if not (nx - 1 <= ux <= nx + 1 and ny - 1 <= uy <= ny + 1):
                                return u
                    elif diff_need == rest_unknown:
                        for u in neighbors[c]:
                            if vis[u]:
                                continue
                            ux, uy = xs[u], ys[u]
                            if not (nx - 1 <= ux <= nx + 1 and ny - 1 <= uy <= ny + 1):
                                mark_mine(u)
                                return -1

        return choose_fallback()

    # chọn điểm bắt đầu cố thử cho đến khi AC( ~_~ )
    sx, sy = n // 2 + 1, m // 2 - 2
    if sy < 1: sx, sy = 2, 1
    if total > 0 and len(mines) < k:
        start = idx(sx, sy)
        get(start, ask(sx, sy))

    while len(mines) < k:
        v = helper()
        if v == -1:
            continue
        if v == -2:
            break
        x, y = pos(v)
        get(v, ask(x, y))

    final_mines = sorted(mines)
    if len(final_mines) < k:
        for v in range(total):
            if v not in mine_set:
                final_mines.append(v)
                if len(final_mines) == k:
                    break
    answer(0, 0)
    for v in final_mines[:k]:
        answer(*pos(v))
    # show(g)
    # debug(mine)
    # for x, y in map(pos, mines):
    #     if g[x][y] != 1:
    #         debug('wa')
    # else:
    #     debug('AC', quer)

t = read()
for _ in range(t):
    solve(readline())