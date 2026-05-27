import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])


K_LIMIT = 12
def build(tree: list[list[int]], node, start, end, arr):
    if start > end: return
    if start == end:
        tree[node].append(arr[start - 1])
        return

    left_node = node << 1
    right_node = left_node | 1
    mid = (start + end) >> 1

    build(tree, left_node, start, mid, arr)
    build(tree, right_node, mid + 1, end, arr)
    merge(tree[node], tree[left_node], tree[right_node])
    

def merge(arr: list[int], left_half: list[int], right_half: list[int]):
    i, j = 0, 0
    arr.clear()
    while i < len(left_half) and j < len(right_half):
        if left_half[i] > right_half[j]:
            arr.append(left_half[i])
            i += 1
        else:
            arr.append(right_half[j])
            j += 1
        if len(arr) >= K_LIMIT: return

    while i < len(left_half):
        arr.append(left_half[i])
        i += 1
        if len(arr) >= K_LIMIT: return

    while j < len(right_half):
        arr.append(right_half[j])
        j += 1
        if len(arr) >= K_LIMIT: return

def query(tree: list[list[int]], node, start, end, left, right):
    if start > right or end < left:
        return []
    if left <= start and end <= right:
        return tree[node]

    left_node = node << 1
    right_node = left_node | 1
    mid = (start + end) >> 1
    L = query(tree, left_node, start, mid, left, right)
    R = query(tree, right_node, mid + 1, end, left, right)
    res = []
    merge(res, L, R)
    return res


n, t = read(), read()
a = [read() for _ in range(n)]
pref = [0] * (n + 1)
for i in range(n): pref[i+1] = pref[i] + a[i]

size = 1 << (n - 1).bit_length()
tree = [[] for _ in range(2 * size)]

for i in range(n):
    tree[size + i] = [a[i]]
for i in range(size - 1, 0, -1):
    merge(tree[i], tree[i << 1], tree[i << 1 | 1])
    
p10 = [10**i for i in range(K_LIMIT + 1)]
# TREE = [[] for _ in range(n << 2)]
# build(TREE, 1, 1, n, a)

# debug(a)
# debug(TREE)
# debug(tree)

def run():
    l, r = read() - 1, read() - 1
    total = pref[r + 1] - pref[l]
    # best = query(TREE, 1, 1, n, l, r)
    ans = total
    top_vals = []
    ql, qr = l + size, r + size
    
    while ql <= qr:
        if ql % 2 == 1:
            tmp = []
            merge(tmp, top_vals, tree[ql])
            top_vals = tmp
            ql += 1
        if qr % 2 == 0:
            tmp = []
            merge(tmp, top_vals, tree[qr])
            top_vals = tmp
            qr -= 1
        ql //= 2
        qr //= 2
    # debug(l, r, total)
    # debug(top_vals)
    for i, b in enumerate(top_vals):
        total -= b
        ans = min(ans, total + p10[i + 1])
    return ans

for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))