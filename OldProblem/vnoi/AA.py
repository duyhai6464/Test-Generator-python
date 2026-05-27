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
    n, m, r, c = read(), read(), read(), read()
    if r == 1 or r == n:
        t_rows = n - 1
    else:
        t_rows = 2 * n - r - 1

    if c == 1 or c == m:
        t_cols = m - 1
    else:
        t_cols = 2 * m - c - 1

    return min(t_rows, t_cols)

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))