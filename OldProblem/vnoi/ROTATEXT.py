import sys


data = sys.stdin.buffer.read().split()
ptr = 0


def read_int():
    global ptr
    value = int(data[ptr])
    ptr += 1
    return value


def read_str():
    global ptr
    value = data[ptr].decode()
    ptr += 1
    return value


n = read_int()
c = read_int()
q = read_int()
S = read_str()
T = read_str()
BASE = 256
MOD1, MOD2 = (1000000093, 1000000223)

pow1 = [1] * (n + 1)
pow2 = [1] * (n + 1)
same1 = [0] * (n + 1)
same2 = [0] * (n + 1)
for i in range(1, n + 1):
    pow1[i] = pow1[i - 1] * BASE % MOD1
    pow2[i] = pow2[i - 1] * BASE % MOD2
    same1[i] = (same1[i - 1] * BASE + 1) % MOD1
    same2[i] = (same2[i - 1] * BASE + 1) % MOD2

factors = []
value = c
div = 2
while div * div <= value:
    if value % div == 0:
        factors.append(div)
        while value % div == 0:
            value //= div
    div += 1
if value > 1:
    factors.append(value)


def find_root(mod):
    if c == 1:
        return 1
    step = (mod - 1) // c
    cand = 2
    while True:
        root = pow(cand, step, mod)
        if root != 1 and all(pow(root, c // factor, mod) != 1 for factor in factors):
            return root
        cand += 1


root1 = find_root(MOD1)
root2 = find_root(MOD2)
rot1 = [1] * c
rot2 = [1] * c
for i in range(1, c):
    rot1[i] = rot1[i - 1] * root1 % MOD1
    rot2[i] = rot2[i - 1] * root2 % MOD2
decode = {(rot1[i], rot2[i]): i for i in range(c)}

initial_s = [0] * (n + 1)
diff = [0] * (n + 1)
for i in range(1, n + 1):
    s_value = ord(S[i - 1]) - 97
    initial_s[i] = s_value
    diff[i] = (s_value - (ord(T[i - 1]) - 97)) % c

size = (n << 2) + 5
hd1 = [0] * size
hd2 = [0] * size
lazy = [0] * size
bit = [0] * (n + 2)


def bit_add(index, delta):
    while index <= n:
        bit[index] += delta
        index += index & -index


def add_s(left, right, delta):
    bit_add(left, delta)
    bit_add(right + 1, -delta)


def get_s(index):
    orig = index
    total = 0
    while index > 0:
        total += bit[index]
        index -= index & -index
    return (initial_s[orig] + total) % c


def apply(node, shift):
    if shift == 0:
        return
    hd1[node] = hd1[node] * rot1[shift] % MOD1
    hd2[node] = hd2[node] * rot2[shift] % MOD2
    lazy[node] += shift
    if lazy[node] >= c:
        lazy[node] -= c


def push(node):
    shift = lazy[node]
    if shift == 0:
        return
    left = node << 1
    apply(left, shift)
    apply(left | 1, shift)
    lazy[node] = 0


def pull(node, right_len):
    left = node << 1
    right = left | 1
    hd1[node] = (hd1[left] * pow1[right_len] + hd1[right]) % MOD1
    hd2[node] = (hd2[left] * pow2[right_len] + hd2[right]) % MOD2


def build(node, start, end):
    if start == end:
        value = diff[start]
        hd1[node] = rot1[value]
        hd2[node] = rot2[value]
        return

    mid = (start + end) >> 1
    left = node << 1
    build(left, start, mid)
    build(left | 1, mid + 1, end)
    pull(node, end - mid)


def update(node, start, end, left, right, shift):
    if start > right or end < left:
        return
    if left <= start and end <= right:
        apply(node, shift)
        return

    push(node)
    mid = (start + end) >> 1
    left_node = node << 1
    update(left_node, start, mid, left, right, shift)
    update(left_node | 1, mid + 1, end, left, right, shift)
    pull(node, end - mid)


def compare(node, start, end, left_bound):
    if end < left_bound:
        return 0
    seg_len = end - start + 1
    if left_bound <= start and hd1[node] == same1[seg_len] and hd2[node] == same2[seg_len]:
        return 0
    if start == end:
        delta = decode[(hd1[node], hd2[node])]
        s_char = get_s(start)
        t_char = (s_char - delta) % c
        if s_char < t_char:
            return -1
        return 1

    push(node)
    mid = (start + end) >> 1
    res = compare(node << 1, start, mid, left_bound)
    if res:
        return res
    return compare(node << 1 | 1, mid + 1, end, left_bound)


build(1, 1, n)

out = []
for _ in range(q):
    query_type = read_int()
    if query_type == 3:
        left = read_int()
        out.append("=><"[compare(1, 1, n, left)])
        continue

    left = read_int()
    right = read_int()
    shift = read_int() % c
    if shift == 0:
        continue
    if query_type == 1:
        add_s(left, right, shift)
        update(1, 1, n, left, right, shift)
    else:
        update(1, 1, n, left, right, (-shift) % c)

sys.stdout.write("\n".join(out))
