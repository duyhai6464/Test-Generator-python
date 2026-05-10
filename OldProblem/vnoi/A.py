import sys, time

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[int] = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []
def read() -> int:
    global ptr, buffer
    # while ptr >= len(buffer):
    #     buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return buffer[ptr - 1]

def add(bit, idx, val, size):
    while idx <= size:
        bit[idx] += val
        idx += idx & -idx

def prefix(bit, idx):
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s

def run():
    start = time.time()
    n = read()
    a = [read() for _ in range(n)]
    # debug("Input read in", time.time() - start, "seconds")
    vals = sorted(set(a))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    debug("Rank computed in", time.time() - start, "seconds")
    bit = [0] * (n + 1)
    less = [0] * n
    greater = [0] * n
    equal = [0] * n
    for i in range(n):
        less[i] = prefix(bit, rank[a[i]] - 1)
        greater[i] = i - prefix(bit, rank[a[i]])
        equal[i] = i - less[i] - greater[i]
        add(bit, rank[a[i]], 1, n)
    debug("Less/Greater/Equal computed in", time.time() - start, "seconds")
    bit2 = [0] * (n + 1)
    rless = [0] * n
    rgreater = [0] * n
    requal = [0] * n
    for i in range(n - 1, -1, -1):
        rless[i] = prefix(bit2, rank[a[i]] - 1)
        rgreater[i] = (n - 1 - i) - prefix(bit2, rank[a[i]])
        requal[i] = (n - 1 - i) - rless[i] - rgreater[i]
        add(bit2, rank[a[i]], 1, n)
    # debug("Reverse Less/Greater/Equal computed in", time.time() - start, "seconds")
    diff = 0
    for i in range(1, n - 1):
        diff += less[i] * rless[i] + greater[i] * rgreater[i] + equal[i] * requal[i]
        diff += less[i] * requal[i] + equal[i] * rless[i]
        diff += greater[i] * requal[i] + equal[i] * rgreater[i]
    return diff

t = 1
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))