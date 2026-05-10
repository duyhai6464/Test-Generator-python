import sys


data = sys.stdin.buffer.read().split()
ptr = 0


def read_int():
    global ptr
    value = int(data[ptr])
    ptr += 1
    return value


n = read_int()
c = read_int()
q = read_int()
s = data[ptr]
ptr += 1
t = data[ptr]
ptr += 1

initial_s = [0] * (n + 1)
diff = [0] * (n + 1)
for i in range(1, n + 1):
    initial_s[i] = s[i - 1] - 97
    diff[i] = (initial_s[i] - (t[i - 1] - 97)) % c

bit = [0] * (n + 2)


def bit_add(index, value):
    while index <= n:
        bit[index] = (bit[index] + value) % c
        index += index & -index


def add_s(left, right, value):
    if value == 0:
        return
    bit_add(left, value)
    if right + 1 <= n:
        bit_add(right + 1, c - value)


def get_s(index):
    total = 0
    original = index
    while index > 0:
        total = (total + bit[index]) % c
        index -= index & -index
    return (initial_s[original] + total) % c


size = 4 * n + 5
tree = [0] * size
lazy = [0] * size
full_mask = (1 << c) - 1


def rotate_mask(mask, shift):
    if shift == 0:
        return mask
    return ((mask << shift) | (mask >> (c - shift))) & full_mask


def apply(node, shift):
    if shift == 0:
        return
    tree[node] = rotate_mask(tree[node], shift)
    lazy[node] = (lazy[node] + shift) % c


def push(node):
    shift = lazy[node]
    if shift == 0:
        return
    apply(node << 1, shift)
    apply(node << 1 | 1, shift)
    lazy[node] = 0


def pull(node):
    tree[node] = tree[node << 1] | tree[node << 1 | 1]


def build(node, left, right):
    if left == right:
        tree[node] = 1 << diff[left]
        return
    mid = (left + right) >> 1
    build(node << 1, left, mid)
    build(node << 1 | 1, mid + 1, right)
    pull(node)


def update(node, start, end, left, right, shift):
    if end < left or right < start:
        return
    if left <= start and end <= right:
        apply(node, shift)
        return
    push(node)
    mid = (start + end) >> 1
    update(node << 1, start, mid, left, right, shift)
    update(node << 1 | 1, mid + 1, end, left, right, shift)
    pull(node)


def first_different(node, start, end, lower_bound):
    if end < lower_bound or tree[node] == 1:
        return -1
    if start == end:
        return start
    push(node)
    mid = (start + end) >> 1
    result = first_different(node << 1, start, mid, lower_bound)
    if result != -1:
        return result
    return first_different(node << 1 | 1, mid + 1, end, lower_bound)


def get_diff(node, start, end, index):
    if start == end:
        return tree[node].bit_length() - 1
    push(node)
    mid = (start + end) >> 1
    if index <= mid:
        return get_diff(node << 1, start, mid, index)
    return get_diff(node << 1 | 1, mid + 1, end, index)


build(1, 1, n)

out = []
for _ in range(q):
    query_type = read_int()

    if query_type == 3:
        left = read_int()
        pos = first_different(1, 1, n, left)
        if pos == -1:
            out.append("=")
            continue

        s_value = get_s(pos)
        t_value = (s_value - get_diff(1, 1, n, pos)) % c
        out.append("<" if s_value < t_value else ">")
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
        update(1, 1, n, left, right, c - shift)

sys.stdout.write("\n".join(out))
