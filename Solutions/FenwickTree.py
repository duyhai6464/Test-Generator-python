import sys


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


def range_add(bit1, bit2, left, right, val, size):
    add(bit1, left, val, size)
    add(bit1, right + 1, -val, size)
    add(bit2, left, val * (left - 1), size)
    add(bit2, right + 1, -val * right, size)


def range_sum(bit1, bit2, idx):
    return prefix(bit1, idx) * idx - prefix(bit2, idx)

data = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []

n = data[ptr]
q = data[ptr + 1]
ptr += 2

size = n + 1
bit1 = [0] * (size + 1)
bit2 = [0] * (size + 1)

for _ in range(q):
    typ = data[ptr]
    ptr += 1
    if typ == 1:
        l = data[ptr]
        r = data[ptr + 1]
        ptr += 2
        out.append(str(range_sum(bit1, bit2, r) - range_sum(bit1, bit2, l - 1)))
    else:
        l = data[ptr]
        r = data[ptr + 1]
        x = data[ptr + 2]
        ptr += 3
        range_add(bit1, bit2, l, r, x, size)

sys.stdout.write("\n".join(out))
