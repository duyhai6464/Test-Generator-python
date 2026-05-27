import sys


data = list(map(int, sys.stdin.buffer.read().split()))
if not data:
    raise SystemExit

n, q = data[0], data[1]
a = data[2:2 + n]
ptr = 2 + n

# With n < 2e5 this uses at most 18 bits, and 3 packed slots stay inside 64 bits.
SHIFT = n.bit_length()
MASK = (1 << SHIFT) - 1
SHIFT2 = SHIFT << 1


def merge_min(x, y, ar=a, mask=MASK, sh=SHIFT):
    r1 = r2 = 0
    v1 = v2 = 0

    c = x & mask
    if c:
        r1 = c
        v1 = ar[c - 1]

    c = (x >> sh) & mask
    if c and c != r1:
        vc = ar[c - 1]
        if vc < v1:
            r2, v2 = r1, v1
            r1, v1 = c, vc
        else:
            r2, v2 = c, vc

    c = y & mask
    if c and c != r1 and c != r2:
        vc = ar[c - 1]
        if not r1 or vc < v1:
            r2, v2 = r1, v1
            r1, v1 = c, vc
        elif not r2 or vc < v2:
            r2, v2 = c, vc

    c = (y >> sh) & mask
    if c and c != r1 and c != r2:
        vc = ar[c - 1]
        if not r1 or vc < v1:
            r2, v2 = r1, v1
            r1, v1 = c, vc
        elif not r2 or vc < v2:
            r2, v2 = c, vc

    return r1 | (r2 << sh)


def merge_max(x, y, ar=a, mask=MASK, sh=SHIFT, sh2=SHIFT2):
    r1 = r2 = r3 = 0
    v1 = v2 = v3 = 0

    c = x & mask
    if c:
        r1 = c
        v1 = ar[c - 1]

    c = (x >> sh) & mask
    if c and c != r1:
        vc = ar[c - 1]
        if vc > v1:
            r2, v2 = r1, v1
            r1, v1 = c, vc
        else:
            r2, v2 = c, vc

    c = (x >> sh2) & mask
    if c and c != r1 and c != r2:
        vc = ar[c - 1]
        if vc > v1:
            r3, v3 = r2, v2
            r2, v2 = r1, v1
            r1, v1 = c, vc
        elif not r2 or vc > v2:
            r3, v3 = r2, v2
            r2, v2 = c, vc
        elif not r3 or vc > v3:
            r3, v3 = c, vc

    c = y & mask
    if c and c != r1 and c != r2 and c != r3:
        vc = ar[c - 1]
        if not r1 or vc > v1:
            r3, v3 = r2, v2
            r2, v2 = r1, v1
            r1, v1 = c, vc
        elif not r2 or vc > v2:
            r3, v3 = r2, v2
            r2, v2 = c, vc
        elif not r3 or vc > v3:
            r3, v3 = c, vc

    c = (y >> sh) & mask
    if c and c != r1 and c != r2 and c != r3:
        vc = ar[c - 1]
        if not r1 or vc > v1:
            r3, v3 = r2, v2
            r2, v2 = r1, v1
            r1, v1 = c, vc
        elif not r2 or vc > v2:
            r3, v3 = r2, v2
            r2, v2 = c, vc
        elif not r3 or vc > v3:
            r3, v3 = c, vc

    c = (y >> sh2) & mask
    if c and c != r1 and c != r2 and c != r3:
        vc = ar[c - 1]
        if not r1 or vc > v1:
            r3, v3 = r2, v2
            r2, v2 = r1, v1
            r1, v1 = c, vc
        elif not r2 or vc > v2:
            r3, v3 = r2, v2
            r2, v2 = c, vc
        elif not r3 or vc > v3:
            r3, v3 = c, vc

    return r1 | (r2 << sh) | (r3 << sh2)


levels = n.bit_length()
st_min = [list(range(1, n + 1))]
st_max = [list(range(1, n + 1))]

for k in range(1, levels):
    half = 1 << (k - 1)
    size = n - (1 << k) + 1
    prev_min = st_min[-1]
    prev_max = st_max[-1]
    st_min.append([merge_min(prev_min[i], prev_min[i + half]) for i in range(size)])
    st_max.append([merge_max(prev_max[i], prev_max[i + half]) for i in range(size)])

out = []

for _ in range(q):
    l = data[ptr] - 1
    r = data[ptr + 1] - 1
    ptr += 2

    k = int.bit_length(r - l + 1) - 1
    start = r - (1 << k) + 1
    mi = merge_min(st_min[k][l], st_min[k][start])
    ma = merge_max(st_max[k][l], st_max[k][start])

    c1 = mi & MASK
    c2 = (mi >> SHIFT) & MASK
    c3 = ma & MASK
    c4 = (ma >> SHIFT) & MASK
    c5 = (ma >> SHIFT2) & MASK

    ids = [c1]
    if c2 and c2 != c1:
        ids.append(c2)
    if c3 and c3 != c1 and c3 != c2:
        ids.append(c3)
    if c4 and c4 != c1 and c4 != c2 and c4 != c3:
        ids.append(c4)
    if c5 and c5 != c1 and c5 != c2 and c5 != c3 and c5 != c4:
        ids.append(c5)

    vals = [a[i - 1] for i in ids]
    vals.sort()
    ans = vals[0] * vals[1] * vals[-1]
    other = vals[-1] * vals[-2] * vals[-3]
    if other > ans:
        ans = other
    out.append(str(ans))

sys.stdout.write("\n".join(out))
