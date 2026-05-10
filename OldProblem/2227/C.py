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

def comp(x, y):
    return True

def run():
    n = read()
    cnt2, cnt3, cnt6, cnt0 = [], [], [], []
    for _ in range(n):
        x = read()
        if x % 6 == 0:cnt6.append(x)
        elif x % 2 == 0:cnt2.append(x)
        elif x % 3 == 0:cnt3.append(x)
        else:cnt0.append(x)
    if len(cnt2) > len(cnt3): cnt2, cnt3 = cnt3, cnt2
    return ' '.join(map(str, cnt6 + cnt2 + cnt0 + cnt3))

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))