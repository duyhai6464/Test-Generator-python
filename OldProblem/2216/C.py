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
    n, k, p, q = read(), read(), read(), read()
    a = [read() for _ in range(n)]
    a_pq = [x % q % p for x in a]
    a = [x % p for x in a]
    prefix_a = [0] * (n + 1)
    prefix_a_pq = [0] * (n + 1)
    prefix_a_best = [0] * (n + 1)
    for i in range(n):
        prefix_a[i + 1] = prefix_a[i] + a[i]
        prefix_a_pq[i + 1] = prefix_a_pq[i] + a_pq[i]
        prefix_a_best[i + 1] = prefix_a_best[i] + min(a[i], a_pq[i])
    # now find best l, r len = k in [1, n] min sum(a[l:r])
    best = int(1e18)
    for i in range(n - k + 1):
        cur_a = prefix_a[i + k] - prefix_a[i]
        cur_a_pq = prefix_a_pq[i + k] - prefix_a_pq[i]
        cur = min(cur_a, cur_a_pq)
        # need add [1, i] and [i + k, n] to cur
        cur += prefix_a_best[i] + (prefix_a_best[n] - prefix_a_best[i + k])
        best = min(best, cur)
    return best

    


t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))