import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []

def read(t: type = int):
    global buffer, ptr
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    s = read(str)
    n = len(s)
    cnt = [0] * 5
    ar = [0] * n
    for i, c in enumerate(s):
        ar[i] = ord(c) - ord('0')
        cnt[ar[i]] += 1
    l13 = cnt[1] + cnt[3]
    max_l = l13
    l2 = 0
    
    for c in ar:
        if c == 2:
            l2 += 1
        elif c % 2:
            l13 -= 1
        max_l = max(max_l, l2 + l13)
    return n - max_l
        
t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))