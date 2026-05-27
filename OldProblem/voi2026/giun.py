import heapq
import random
import sys


LOCAL = sys.stdin.isatty()


def debug(*x, **y):
    if LOCAL: print(*x, file=sys.stderr, **y)


def answer(*args):
    print("!", *args, flush=True)


rng = random.Random(6767)
N, M, K, Q = 11, 2, 3, 180
arr = rng.choices(range(1, 99), k=N * M * K)


def ask_raw(*args):
    print("?", *args, flush=True)
    if LOCAL:
        x, y, z = args
        if not (1 <= x <= N and 1 <= y <= M and 1 <= z <= K):
            return 0
        return arr[(x - 1) * M * K + (y - 1) * K + z - 1]
    return int(input())


def read():
    if LOCAL: return N, M, K, Q
    return map(int, input().split())


n, m, k, q = read()


class Query:
    def __init__(self, n, m, k, limit):
        self.n = n
        self.m = m
        self.k = k
        self.limit = limit
        self.used = 0
        self.cache = {}

    def inside(self, x, y, z):
        return 1 <= x <= self.n and 1 <= y <= self.m and 1 <= z <= self.k

    def get(self, x, y, z):
        if not self.inside(x, y, z):
            return 0
        key = (x, y, z)
        if key not in self.cache:
            if self.used >= self.limit:
                return 0
            self.cache[key] = ask_raw(x, y, z)
            self.used += 1
        return self.cache[key]

    def left(self):
        return self.limit - self.used


query = Query(n, m, k, q)


def sub1():
    if n == 1:
        query.get(1, 1, 1)
        return 1, 1, 1

    fib = [1, 1]
    while fib[-1] < n + 1:
        fib.append(fib[-1] + fib[-2])

    t = len(fib) - 1
    l, r = 0, fib[t]
    x = l + fib[t - 2]
    y = l + fib[t - 1]
    ax = query.get(x, 1, 1)
    ay = query.get(y, 1, 1)

    while t > 2 and query.left() > 0:
        # debug("sub1", "left", query.left(), "range", l, r, "probe", x, y)
        if ax < ay:
            l = x
            t -= 1
            x, ax = y, ay
            y = l + fib[t - 1]
            ay = query.get(y, 1, 1)
        else:
            r = y
            t -= 1
            y, ay = x, ax
            x = l + fib[t - 2]
            ax = query.get(x, 1, 1)

    best = None
    best_val = -1
    for i in range(max(1, l + 1), min(n, r - 1) + 1):
        v = query.get(i, 1, 1)
        if v > best_val:
            best = i
            best_val = v

    if best is None:
        best = max(query.cache, key=query.cache.get)[0]
    return best, 1, 1


def neighbours(x, y, z):
    return (
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    )


def random_cell():
    return (
        rng.randint(1, n),
        rng.randint(1, m),
        rng.randint(1, k),
    )


def sample_best(sample_budget, keep=12):
    total_cells = n * m * k
    target_used = min(query.limit, query.used + sample_budget, total_cells)
    first = (1, 1, 1)
    first_val = query.get(*first)
    starts = [(first_val, first)]

    seen = {first}
    tries = 0
    max_tries = max(sample_budget * 10, 100)
    while query.used < target_used and query.left() > 0 and len(seen) < total_cells and tries < max_tries:
        p = random_cell()
        tries += 1
        if p in seen:
            continue
        seen.add(p)
        v = query.get(*p)
        if len(starts) < keep:
            heapq.heappush(starts, (v, p))
        elif v > starts[0][0]:
            heapq.heapreplace(starts, (v, p))

    starts.sort(reverse=True)
    return [(p, v) for v, p in starts]


def climb(start, start_val):
    cur = start
    cur_val = start_val

    while query.left() > 0:
        cand = []
        for p in neighbours(*cur):
            if query.inside(*p):
                cand.append(p)
        best = cur
        best_val = cur_val
        for p in cand:
            if query.left() <= 0:
                break
            v = query.get(*p)
            if v > best_val:
                best, best_val = p, v

        if best == cur:
            return cur, True
        cur, cur_val = best, best_val

    return cur, False


def random_solver(sample_budget):
    sample_budget = max(1, min(sample_budget, query.left()))
    starts = sample_best(sample_budget)
    # debug("sampled", query.used, "best", starts[0], "left", query.left())
    best, best_val = starts[0]

    for start, start_val in starts:
        if query.left() <= 0:
            break
        p, ok = climb(start, start_val)
        v = query.get(*p)
        if v > best_val:
            best, best_val = p, v
        if ok:
            return p
    return best


def sub2():
    x1, x2 = 1, n
    y1, y2 = 1, m
    px, py, pz = 1, 1, 1
    pv = query.get(px, py, pz)

    while query.left() > 0:
        if x1 == x2 and y1 == y2:
            return x1, y1, 1

        h = x2 - x1 + 1
        w = y2 - y1 + 1

        if h >= w:
            mx = (x1 + x2) // 2
            best = (mx, y1, 1)
            best_val = -1

            for y in range(y1, y2 + 1):
                v = query.get(mx, y, 1)
                if v > best_val:
                    best = (mx, y, 1)
                    best_val = v

            if best_val >= pv:
                nb_best = best
                nb_val = best_val
                for nb in neighbours(*best):
                    v = query.get(*nb)
                    if v > nb_val:
                        nb_best = nb
                        nb_val = v

                if nb_best == best:
                    return best

                px, py, pz = nb_best
                pv = nb_val
                if px < mx:
                    x2 = mx - 1
                elif px > mx:
                    x1 = mx + 1
                else:
                    return climb(nb_best, nb_val)[0]
            else:
                if px < mx:
                    x2 = mx - 1
                else:
                    x1 = mx + 1
        else:
            my = (y1 + y2) // 2
            best = (x1, my, 1)
            best_val = -1

            for x in range(x1, x2 + 1):
                v = query.get(x, my, 1)
                if v > best_val:
                    best = (x, my, 1)
                    best_val = v

            if best_val >= pv:
                nb_best = best
                nb_val = best_val
                for nb in neighbours(*best):
                    v = query.get(*nb)
                    if v > nb_val:
                        nb_best = nb
                        nb_val = v

                if nb_best == best:
                    return best

                px, py, pz = nb_best
                pv = nb_val
                if py < my:
                    y2 = my - 1
                elif py > my:
                    y1 = my + 1
                else:
                    return climb(nb_best, nb_val)[0]
            else:
                if py < my:
                    y2 = my - 1
                else:
                    y1 = my + 1

    return px, py, pz


def sub3():
    sample_budget = min(12000, max(6000, q // 15))
    return random_solver(sample_budget)


if m == k == 1:
    ans = sub1()
elif k == 1:
    ans = sub2()
else:
    ans = sub3()

answer(*ans)


if LOCAL:
    x, y, z = ans
    here = query.get(x, y, z)
    around = [query.get(*p) for p in neighbours(x, y, z)]
    debug("used", query.used, "/", q)
    debug("ans", ans, "value", here, "neighbours", around)
    debug("valid", here >= max(around))
