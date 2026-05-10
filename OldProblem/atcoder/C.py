def add(bit, idx, val, size):
    while idx <= size:
        bit[idx] += val
        idx += idx & -idx


def prefix(bit, idx):
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s


n, q = list(map(int, input().split()))
a = list(map(int, input().split()))

bit = [0] * (n + 1)

def update(l, r, x):
    add(bit, l, x, n)
    add(bit, r + 1, -x, n)
    
def query(p):
    return prefix(bit, p)

for i in range(n):
    update(i + 1, i + 1, a[i])
for _ in range(q):
    que = list(map(int, input().split()))
    if que[0] == 1:
        update(que[1], que[2], que[3])
    else:
        print(query(que[1]))
