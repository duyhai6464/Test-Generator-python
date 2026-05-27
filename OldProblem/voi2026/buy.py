import sys, random, functools

def debug(*x, **y): print('--', *x, file=sys.stderr, **y)
buf = []
ptr = 0
    
arr = [0, 4, 8, 10, 12, 9, 1, 3, 7, 5, 11]
if sys.stdin.isatty():
    buf.extend([len(arr) - 1, 7])

def ask(*args):
    print('?', *args, flush=True)
    if sys.stdin.isatty():
        return args[0] if arr[args[0]] > arr[args[1]] else args[1]
    return read()

def read():
    global ptr
    if ptr >= len(buf): buf.extend(map(int, input().split()))
    ptr += 1
    return buf[ptr - 1]

class Tournament:
    def __init__(self, N: int, is_min = False):
        self.root = 0
        self.is_min = is_min
        self.lost_to = [[] for _ in range(N + 1)]
        self.root = self.tournament(list(range(1, N + 1)))

    def match(self, i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        big = ask(i, j)
        small = big ^ i ^ j
        if self.is_min:
            self.lost_to[small].append(big)
            return small
        self.lost_to[big].append(small)
        return big
    
    def tournament(self, candidates: list[int]) -> int:
        if not candidates: return 0
        cur = candidates[:]
        while len(cur) > 1:
            random.shuffle(cur)
            nxt = []
            for k in range(0, len(cur) - 1, 2):
                nxt.append(self.match(cur[k], cur[k + 1]))
            if len(cur) & 1:
                nxt.append(cur[-1])
            cur = nxt
        return cur[0]
    
    def pop(self) -> int:
        res = self.root
        candidates = self.lost_to[res]
        self.lost_to[res] = []
        self.root = self.tournament(candidates)
        return res

def choose_pivot(candidates: list[int], k: int) -> int:
    if len(candidates) < 32:
        return random.choice(candidates)

    edge = min(k, len(candidates) - k)
    if edge * 10 < len(candidates):
        sample_size = 17
    elif edge * 3 < len(candidates):
        sample_size = 33
    else:
        sample_size = 65
    sample = random.sample(candidates, min(sample_size, len(candidates)))

    def cmp(i: int, j: int) -> int:
        return -1 if ask(i, j) == i else 1

    sample.sort(key=functools.cmp_to_key(cmp))
    return sample[(k - 1) * len(sample) // len(candidates)]

def top_k_select(candidates: list[int], k: int) -> list[int]:
    res = []
    while 0 < k < len(candidates):
        pivot = choose_pivot(candidates, k)
        bigger = []
        smaller = []
        for x in candidates:
            if x == pivot:
                continue
            if ask(x, pivot) == x:
                bigger.append(x)
            else:
                smaller.append(x)

        if len(bigger) >= k:
            candidates = bigger
        elif len(bigger) + 1 == k:
            return res + bigger + [pivot]
        else:
            res.extend(bigger)
            res.append(pivot)
            k -= len(bigger) + 1
            candidates = smaller

    if k > 0:
        res.extend(candidates)
    return res

N, K = read(), read()
edge = min(K, N - K)
use_tournament = edge * 15 <= N

if K == 0:
    print('!', 1, 1, flush=True)
    print(flush=True)
elif K == N:
    print('!', 1, 1, flush=True)
    print(*range(1, N + 1), flush=True)
elif use_tournament and K <= N // 2:
    t = Tournament(N)
    ans = [t.pop() for _ in range(K)]
    print('!', 1, 1, flush=True)
    print(*ans, flush=True)
elif use_tournament:
    t = Tournament(N, True)
    ans = [1] * N
    for _ in range(N - K):
        ans[t.pop() - 1] = 0
    ans = [i for i, v in enumerate(ans, 1) if v != 0]
    print('!', 1, 1, flush=True)
    print(*ans, flush=True)
else:
    ans = top_k_select(list(range(1, N + 1)), K)
    print('!', 1, 1, flush=True)
    print(*ans, flush=True)
