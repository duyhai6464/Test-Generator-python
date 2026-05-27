import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def total(end, start, step=1):
    if start > end: return 0
    return (start + end) * ((end - start) // step + 1) // 2

def run():
    n = read()
    a = [read() for _ in range(n)]
    b = [read() for _ in range(n)]
    t = read()
    p = [a[i] + b[i] for i in range(n)]
    p.append(0)
    p.sort(reverse=True)
    res = 0
    m = max(a)
    # debug(a, b)
    # debug(p, m)
    for i in range(n):
        tmp = (p[i] - p[i + 1]) * (i + 1)
        if t >= tmp:
            if p[i + 1] < m:
                res += total(p[i], m + 1) * (i + 1)
                t -= (i + 1) * (p[i] - m)
                # debug('++++', t, i, p[i], p[i + 1], res)
                return res + t * m
            
            res += total(p[i], p[i + 1] + 1) * (i + 1)
            t -= tmp
            # debug('----', i, res, tmp, t)
        else:
            l, r = t // (i + 1), t % (i + 1)
            if p[i] - l < m:
                res += total(p[i], m + 1) * (i + 1)
                t -= (i + 1) * (p[i] - m)
                return res + t * m
                
            res += total(p[i], p[i] - l + 1) * (i + 1)
            res += (p[i] - l) * r
            return res

print(run())