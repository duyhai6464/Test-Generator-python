import sys

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
    E: list[list[int]] = [[] for _ in range(n)]
    a: list[int] = []
    for i in range(n * 2):
        x = read()
        E[x].append(i)
        a.append(x)
    for i in range((E[0][1] - E[0][0]) // 2):
        if a[E[0][0] + 1 + i] != a[E[0][1] - 1 - i]:
            break
    else:
        l, r = E[0]
        while l >= 0 and r < n * 2 and a[l] == a[r]:
            l -= 1
            r += 1
        cnt = [False] * n
        for i in range(l + 1, (E[0][1] + E[0][0]) // 2 + 1):
            cnt[a[i]] = True
        for i in range(n):
            if not cnt[i]:
                return i
        return n
    ans = 1
    for idx in E[0]:
        l = 0
        while idx - l >= 0 and idx + l < n * 2 and a[idx - l] == a[idx + l]:
            l += 1
        cnt = [False] * n
        for i in range(idx, idx + l):
            cnt[a[i]] = True
        debug(idx, l, cnt)          
        for i in range(n):
            if not cnt[i]:
                ans = max(ans, i)
                break
        else:
            return n
    return ans

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))