import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    v = read()
    if v >= MAXN: return 0
    if v not in meme:
        meme[v] = sum(cnt[v::v])
    return meme[v]

MAXN = int(1e6 + 5)
meme: dict[int, int] = {}

n, t = read(), read()
cnt = [0] * MAXN
for _ in range(n): cnt[read()] += 1

for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))