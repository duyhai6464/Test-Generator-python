import sys
import bisect

buffer:list[str] = []
ptr = 0
out = []
def read() -> int:
    global ptr, buffer
    if ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return int(buffer[ptr - 1])

def read_t(t: type = str):
    global ptr, buffer
    if ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    if t != str: return t(buffer[ptr - 1])
    return buffer[ptr - 1]

def run():
    n = read()
    A = []
    for i in range(1, n + 1):
        x = read()
        if x <= i:
            A.append((i - x, x))
    A.sort()
    lis = []
    for _, val in A:
        idx = bisect.bisect_left(lis, val)
        if idx >= len(lis):
            lis.append(val)
        else:
            lis[idx] = val
    print(lis, file=sys.stderr)
    return len(lis)

t = 1
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))