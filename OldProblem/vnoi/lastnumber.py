import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])


#1^(x^k) + 2^(x^k) + ... + n^(x^k) MOD 10
def run():
    n, k, x = read(), read(), read()
    ans = 0
    loops = [0, 1, 5, 6]
    for i in range(10):
        count = ((n - i) // 10 + 1) % 10
        if count == 0: continue
        if i in loops:
            ans = (ans + i * count) % 10
            continue
        if i in [2, 8]: # 2 ^ (x ^ k)| 2 ^ 4 = 16(loop) same 8
            u = pow(x, k, 4)
            pp = 6 if pow(x, min(k, 2)) >= 4 else 1
            ans = (ans + count * pow(i, u) * pp) % 10
        if i == 4:# 4 ^ 2 = 16(loop)
            u = x % 2
            pp = 6 if pow(x, min(k, 2)) >= 2 else 1
            ans = (ans + count * pow(i, u) * pp) % 10
        if i in [3, 7]:# 3^4 = 81(loop) same 7
            u = pow(x, k, 4)
            ans = (ans + count * pow(i, u)) % 10
        if i == 9:
            u = x % 2
            ans = (ans + count * pow(i, u)) % 10
    return ans

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))