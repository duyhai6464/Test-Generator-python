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
    p, q = read(), read()
    # 2nm + n + m = 2q + p
    # (2n + 1)(2m + 1) = 2(2q + p) + 1 = T
    T = 2*(2*q + p) + 1
    # print any n m if such n and m exist, otherwise print -1
    for i in range(3, int(T**0.5) + 1, 2):
        if T % i == 0:
            j = T // i
            if (i - 1) % 2 == 0 and (j - 1) % 2 == 0:
                n = (i - 1) // 2
                m = (j - 1) // 2
                if q <= m * (n + 1) and q <= n * (m + 1):
                    return f"{n} {m}"
    return -1

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))