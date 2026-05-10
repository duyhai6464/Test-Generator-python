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
    n, k = read(), read()
    sumary = 0
    for i in range(n):
        val = read()
        sumary += val
    if sumary % 2 == 1 or n * k % 2 == 0: return "YES"
    return "NO"

t = read()
for _ in range(t):
    out.append(run())

sys.stdout.write("\n".join(out))
    