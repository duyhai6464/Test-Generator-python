import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

sys.setrecursionlimit(int(1e6))

def update(A, l, r, x):
    for i in range(l - 1, r):
        A[i] = (A[i] + x) % c
    debug(l, r, x)
    debug(A)

def run():
    query_t = read()
    if query_t != 3:
        l, r, x = read(), read(), read()
        if query_t == 1:
            return update(S, l, r, x)
        return update(T, l, r, x)
    l = read()
    for i in range(l - 1, n):
        if S[i] != T[i]:
            if S[i] > T[i]: return '>'
            return '<'
    return '='


n, c, q = read(), read(), read()
S, T = [ord(x) - ord('a') for x in read(str)], [ord(x) - ord('a') for x in read(str)]
for _ in range(q):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))