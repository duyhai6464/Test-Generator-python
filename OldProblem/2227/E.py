import sys, bisect

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr = 0
out = []
def read(base: int = 10) -> int:
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return int(buffer[ptr - 1], base)

def read_t(t: type = str):
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    if t != str: return t(buffer[ptr - 1])
    return buffer[ptr - 1]

def run():
    n = read()
    a = [read() for _ in range(n)]
    a.append(int(1e18))
    d = 0
    m = n
    gain = 0
    for i in range(n - 1, -1, -1):
        if a[i] < a[m]:
            m = i
        d += a[i] - a[m]
        gain = max(gain, m - i)
    debug(d, gain)
    return d + gain

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))