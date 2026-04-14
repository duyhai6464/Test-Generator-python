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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def run():
    n,m,a,b = read(), read(), read(), read()
    if gcd(a, n) == 1 and gcd(b, m) == 1:
        if gcd(n, m) <= 2:
            return "YES"
    return "NO"

t = read()
for _ in range(t):
    out.append(run())
    
sys.stdout.write("\n".join(out))