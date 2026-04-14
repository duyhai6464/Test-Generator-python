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
    n, k = read(), read()# k = 1
    a = [read() for _ in range(n)]# value 0 or 1 only
    p = read() - 1
    value_x = a[p]
    left, right = 0, 0
    isflip = False
    for i in range(p):
        if (a[i] != value_x) != isflip:
            isflip = not isflip
            left += 1
    if isflip: left += 1

    isflip = False
    for i in range(n - 1, p, -1):
        if (a[i] != value_x) != isflip:
            isflip = not isflip
            right += 1
    if isflip: right += 1
    return max(left, right)

t = read()
for _ in range(t):
    out.append(str(run()))

sys.stdout.write("\n".join(out))