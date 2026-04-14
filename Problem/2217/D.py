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
    n, k = read(), read()# k > 1
    a = [read() for _ in range(n)]# value 0 or 1 only
    p = [read() for _ in range(k)]
    value_x = a[p[0] - 1]
    # xor a with value_x to make B, add 0 at start and end
    B = [0] + [x ^ value_x for x in a] + [0]
    P = [0] + p + [n + 1]
    count_list = [0] * (k + 1)
    for i in range(k + 1):
        for j in range(P[i], P[i + 1]):
            count_list[i] += 1 if B[j] != B[j + 1] else 0
    max_range = max(count_list)
    total_range = sum(count_list)
    # print(count_list, max_range, total_range)
    if max_range <= total_range // 2:
        return total_range // 2
    return max_range

t = read()
for _ in range(t):
    out.append(str(run()))

sys.stdout.write("\n".join(out))