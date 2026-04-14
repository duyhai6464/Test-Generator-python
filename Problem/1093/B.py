import sys

data = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []

def read():
    global ptr
    if ptr >= len(data):
        raise Exception("No more input")
    res = data[ptr]
    ptr += 1
    return res


def run():
    n, m = read(), read()
    a = [read() for _ in range(n)]
    if m > n: return "YES"
    cur, best = 0, 0
    for i in range(n - 1):
        if a[i] == a[i + 1]:
            cur += 1
        else:
            best = max(best, cur)
            cur = 0
    best = max(best, cur)
    if best >= m - 1:
        return "NO"
    return "YES"


t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))