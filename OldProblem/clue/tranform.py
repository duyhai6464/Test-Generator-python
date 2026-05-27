import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

import bisect

class BIT:
    def __init__(self, size):
        self.size = size
        self.bit = [0] * (size + 1)

    def add(self, idx, val):
        while idx <= self.size:
            self.bit[idx] += val
            idx += idx & -idx

    def prefix(self, idx):
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx ^= idx & -idx
        return s
    
    def query(self, l, r):
        if l > r: return 0
        return self.prefix(r) - self.prefix(l - 1)

def run():
    n = read()
    a = [read() for i in range(n)]
    if n % 2: return -1
    b = set(a)
    if len(b) != n // 2: return -1
    sb = sorted(b)
    rank = lambda x: bisect.bisect_left(sb, x) + 1
    first_pos = [0] * (n // 2 + 1)
    bit = BIT(n)
    swaps = 0
    for i, v in enumerate(a, start=1):
        r = rank(v)
        if first_pos[r] == 0:
            first_pos[r] = i
            bit.add(i, 1)
        else:
            l = first_pos[r]
            swaps += bit.query(l + 1, i)
            bit.add(l, -1)
    return swaps + n // 2
    

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))