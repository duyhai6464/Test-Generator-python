import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)

def answer(*args): print('answer', *args, flush=True)

arr = [5, 3, 6, 7, 9, 1, 4]

def ask(*args):
    print('?', *args, flush=True)
    if sys.stdin.isatty():
        ans = args[0] if arr[args[0]] > arr[args[1]] else args[1]
        debug(ans)
        return ans
    return int(input())

def read():
    if sys.stdin.isatty():
        return len(arr)
    return int(input())

class CPPMt19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.idx = 624
        self.mt[0] = seed & 0xffffffff
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff

    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) | (self.mt[(i + 1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y & 1:
                self.mt[i] ^= 0x9908b0df
            self.mt[i] &= 0xffffffff
        self.idx = 0

    def __call__(self):
        if self.idx >= 624:
            self.twist()
        y = self.mt[self.idx]
        self.idx += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= y >> 18
        return y & 0xffffffff


def uniform_u32(g, a, b):
    rng = b - a + 1
    while True:
        product = g() * rng
        low = product & 0xffffffff
        if low >= rng:
            return a + (product >> 32)
        threshold = ((-rng) & 0xffffffff) % rng
        if low >= threshold:
            return a + (product >> 32)


def cpp_shuffle(n, seed=12312123):
    p = list(range(n))
    if n <= 1:
        return p

    g = CPPMt19937(seed)
    urngrange = 0xffffffff

    if urngrange // n >= n:
        i = 1
        if n % 2 == 0:
            j = uniform_u32(g, 0, 1)
            p[i], p[j] = p[j], p[i]
            i += 1

        while i != n:
            swap_range = i + 1
            x = uniform_u32(g, 0, swap_range * (swap_range + 1) - 1)
            j1 = x // (swap_range + 1)
            j2 = x % (swap_range + 1)

            p[i], p[j1] = p[j1], p[i]
            i += 1
            p[i], p[j2] = p[j2], p[i]
            i += 1
    else:
        for i in range(1, n):
            j = uniform_u32(g, 0, i)
            p[i], p[j] = p[j], p[i]

    return p

def solve(n: int):
    if n == 2: return ask(0, 1)
    a = cpp_shuffle(n)
    best = ask(a[0], a[1])
    seco = best ^ a[0] ^ a[1]
    for i in range(2, n):
        r = ask(seco, a[i])
        if r == seco: continue
        r = ask(best, a[i])
        seco = best ^ a[i] ^ r
        best = r
    return best

n = read()
answer(solve(n))
