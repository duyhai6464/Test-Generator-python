import sys

#ONLINE
# sys.stdin = open('PINE.INP', 'r')
# sys.stdout = open('PINE.OUT', 'w')

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = []
ptr, out = 0, []

def read(t: type = int):
    global buffer, ptr
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

from array import array

def make_array(typecode: str, value: int, size: int):
    return array(typecode, [value]) * size

class BIT: # by domigo
    def __init__(self, size: int, typecode: str = 'i'):
        self.size = size
        self.bit = make_array(typecode, 0, size + 1)

    def add(self, idx, val):
        idx += 1
        size, bit = self.size, self.bit
        while idx <= size:
            bit[idx] += val
            idx += idx & -idx

    def prefix(self, idx):
        if idx < 0: return 0
        if idx >= self.size: idx = self.size - 1
        idx += 1
        s, bit = 0, self.bit
        while idx > 0:
            s += bit[idx]
            idx ^= idx & -idx
        return s
    
    def query(self, l, r):
        if l > r: return 0
        return self.prefix(r) - self.prefix(l - 1)

def solve():
    sys.setrecursionlimit(100_000)
    n, q = read(), read()
    a = make_array('i', 0, n + 1)
    for i in range(1, n + 1): a[i] = read()
    edge_count = max(0, 2 * (n - 1))
    graph_head = make_array("i", -1, n + 1)
    to = make_array("i", 0, edge_count)
    nxt = make_array("i", 0, edge_count)
    edge_idx = 0

    def add_edge(u: int, v: int):
        nonlocal edge_idx
        to[edge_idx] = v
        nxt[edge_idx] = graph_head[u]
        graph_head[u] = edge_idx
        edge_idx += 1
        debug('graph_head:\t' ,*graph_head)
        debug('to:', u, v, '\t' ,*to)
        debug('nxt:\t\t' ,*nxt)

    for _ in range(n - 1):
        u, v = read(), read()
        add_edge(u, v)
        add_edge(v, u)

    parent = make_array("i", 0, n + 1)
    depth = make_array("i", 0, n + 1)
    order = array("i")
    stack = [1]
    parent[1] = -1

    while stack:
        u = stack.pop()
        order.append(u)
        e = graph_head[u]
        while e != -1:
            v = to[e]
            if v != parent[u]:
                parent[v] = u
                depth[v] = depth[u] + 1
                stack.append(v)
            e = nxt[e]
    

    size = make_array("i", 1, n + 1)
    heavy = make_array("i", 0, n + 1)

    for u in reversed(order):
        best_size = 0
        e = graph_head[u]
        while e != -1:
            v = to[e]
            if v != parent[u]:
                size[u] += size[v]
                if size[v] > best_size:
                    best_size = size[v]
                    heavy[u] = v
            e = nxt[e]

    top = make_array("i", 0, n + 1)
    pos = make_array("i", 0, n + 1)
    values = make_array("i", 0, n)
    cur = 0
    stack = [(1, 1)]

    while stack:
        u, h = stack.pop()
        while u:
            top[u] = h
            pos[u] = cur
            values[cur] = a[u]
            cur += 1

            hv = heavy[u]
            e = graph_head[u]
            while e != -1:
                v = to[e]
                if v != parent[u] and v != hv:
                    stack.append((v, v))
                e = nxt[e]
            u = hv

    max_value = max(max(a), q, 1)
    del a

    seg = make_array("i", 0, 4 * n + 5)

    def build(idx: int, left: int, right: int):
        if left == right:
            seg[idx] = values[left]
            return
        mid = (left + right) >> 1
        build(idx << 1, left, mid)
        build(idx << 1 | 1, mid + 1, right)
        left_max = seg[idx << 1]
        right_max = seg[idx << 1 | 1]
        seg[idx] = left_max if left_max >= right_max else right_max

    build(1, 0, n - 1)

    bit_count = BIT(max_value + 1, "i")
    bit_sum = BIT(max_value + 1, "q")
    total_sum = 0

    for value in values:
        bit_count.add(value, 1)
        bit_sum.add(value, value)
        total_sum += value

    def change_value(old: int, new: int):
        nonlocal total_sum
        if old == new:
            return
        bit_count.add(old, -1)
        bit_sum.add(old, -old)
        bit_count.add(new, 1)
        bit_sum.add(new, new)
        total_sum += new - old

    def range_mod(idx: int, left: int, right: int, ql: int, qr: int, mod: int):
        if qr < left or right < ql or seg[idx] < mod:
            return
        if left == right:
            old = values[left]
            new = old % mod
            values[left] = new
            seg[idx] = new
            change_value(old, new)
            return

        mid = (left + right) >> 1
        range_mod(idx << 1, left, mid, ql, qr, mod)
        range_mod(idx << 1 | 1, mid + 1, right, ql, qr, mod)
        left_max = seg[idx << 1]
        right_max = seg[idx << 1 | 1]
        seg[idx] = left_max if left_max >= right_max else right_max

    def path_mod(u: int, v: int, mod: int):
        while top[u] != top[v]:
            if depth[top[u]] < depth[top[v]]:
                u, v = v, u
            range_mod(1, 0, n - 1, pos[top[u]], pos[u], mod)
            u = parent[top[u]]
        if depth[u] > depth[v]:
            u, v = v, u
        range_mod(1, 0, n - 1, pos[u], pos[v], mod)

    def beauty(mod: int) -> int:
        if seg[1] < mod:
            return total_sum
        res = 0
        left = 0
        while left <= max_value:
            right = left + mod - 1
            if right > max_value:
                right = max_value
            cnt = bit_count.query(left, right)
            res += bit_sum.query(left, right) - left * cnt
            left += mod
        return res

    for t in range(1, q + 1):
        x, y, w = read(), read(), read()
        path_mod(x, y, w)
        out.append(str(beauty(t)))

solve()    
sys.stdout.write("\n".join(map(str, out)))
