import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = []
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(input().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run1():
    n = read()
    l1, ln = -1, -1
    for i in range(n):
        x = read()
        if x == 1: l1 = i
        elif x == n: ln = i
    print(1 if l1 < ln else 0)

def ask(l, r):
    if l > r: l, r = r, l
    print('?', l, r, flush=True)
    return read()

def run2():
    n, x = read(), read()
    L, R = 1, n
    ans = -1
    if x == 1: # l1 < ln
        while L <= R:
            mid = (L + R) // 2
            if ask(1, mid) == n - 1:
                ans = mid
                R = mid - 1 # Thử tìm cái R nào nhỏ hơn nữa không
            else:
                L = mid + 1
    else:
        # Ta tìm L lớn nhất sao cho [L, n] chứa cả 1 và n
        while L <= R:
            mid = (L + R) // 2
            if ask(mid, n) == n - 1:
                ans = mid
                L = mid + 1 # Thử tìm cái L nào lớn hơn nữa không
            else:
                R = mid - 1
    print('!', ans, flush=True)
        

F = read(str)
t = read()
for _ in range(t):
    run1() if F == "first" else run2()
    