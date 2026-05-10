import sys

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
    n, m = read(), read()
    a = [list() for _ in range(2)]
    for i in range(n):
        a[i % 2].append(read())
    cmp = lambda x: x
    a[0].sort(reverse=True)
    a[1].sort(reverse=True)
    cnt = [0, 0]
    for i in range(m):
        x = read() - 1
        cnt[x % 2] += 1
    s = 0
    for x in range(2):
        if cnt[x] > 0:
            s += a[x][0]
        for i in range(1, min(cnt[x], len(a[x]))):
            if a[x][i] > 0:
                s += a[x][i]
    return sum(a[0]) + sum(a[1]) - s

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))