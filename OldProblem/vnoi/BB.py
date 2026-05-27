import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n, k = read(), read()
    a = [read() for _ in range(n)]
    b = [read() for _ in range(n)]
    g_a = [min(x, k - x) for x in a]
    g_b = [min(x, k - x) for x in b]
    if g_a != g_b:
        return "NO"
    i = 0
    while i < n:
        j = i
        while j < n and g_a[j] == g_a[i]:
            j += 1
        sub_a = a[i:j]
        sub_b = b[i:j]
        count_a = {}
        for x in sub_a:
            count_a[x] = count_a.get(x, 0) + 1
        count_b = {}
        for x in sub_b:
            count_b[x] = count_b.get(x, 0) + 1
        if count_a != count_b:
            return "NO"
        i = j
    return "YES"

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))