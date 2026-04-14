import sys


def update(tree, lazy, node, start, end, left, right, val):
    if start > right or end < left:
        return
    if left <= start and end <= right:
        tree[node] += (end - start + 1) * val
        lazy[node] += val
        return

    left_node = node << 1
    right_node = left_node | 1
    mid = (start + end) >> 1
    pending = lazy[node]
    if pending:
        tree[left_node] += (mid - start + 1) * pending
        tree[right_node] += (end - mid) * pending
        lazy[left_node] += pending
        lazy[right_node] += pending
        lazy[node] = 0

    update(tree, lazy, left_node, start, mid, left, right, val)
    update(tree, lazy, right_node, mid + 1, end, left, right, val)
    tree[node] = tree[left_node] + tree[right_node]


def query(tree, lazy, node, start, end, left, right):
    if start > right or end < left:
        return 0
    if left <= start and end <= right:
        return tree[node]

    left_node = node << 1
    right_node = left_node | 1
    mid = (start + end) >> 1
    pending = lazy[node]
    if pending:
        tree[left_node] += (mid - start + 1) * pending
        tree[right_node] += (end - mid) * pending
        lazy[left_node] += pending
        lazy[right_node] += pending
        lazy[node] = 0

    return query(tree, lazy, left_node, start, mid, left, right) + query(
        tree, lazy, right_node, mid + 1, end, left, right
    )


data = list(map(int, sys.stdin.buffer.read().split()))
ptr = 0
out = []

n = data[ptr]
q = data[ptr + 1]
ptr += 2

tree = [0] * (4 * n + 5)
lazy = [0] * (4 * n + 5)

for _ in range(q):
    typ = data[ptr]
    ptr += 1
    if typ == 1:
        left = data[ptr] - 1
        right = data[ptr + 1] - 1
        ptr += 2
        out.append(str(query(tree, lazy, 1, 0, n - 1, left, right)))
    else:
        left = data[ptr] - 1
        right = data[ptr + 1] - 1
        val = data[ptr + 2]
        ptr += 3
        update(tree, lazy, 1, 0, n - 1, left, right, val)

sys.stdout.write("\n".join(out))
