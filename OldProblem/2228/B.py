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
    n, x1, x2, k = read(), read(), read(), read()
    if n <= 3: return 1
    diff = abs(x1 - x2)
    d = min(diff, n - diff)
    return k + d

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))