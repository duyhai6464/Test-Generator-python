import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

n, q = read(), read()

D:list[set[int]] = [set() for _ in range(30)]
C:list[set[int]] = [set() for _ in range(n)]
 
for i in range(n):
    for c in set(read(str)):
        x = ord(c) - ord('a')
        D[x].add(i)
        C[i].add(x)

for _ in range(q):
    x = ord(read(str)) - ord('a')
    if len(D[x]) <= 0:
        print(n)
        continue
    n -= len(D[x])
    print(n)
    # update all D[u] have x
    for val in D[x]:
        for cx in C[val]:
            if cx == x: continue
            D[cx].remove(val)
    D[x].clear()