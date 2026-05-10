import sys


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)
        self.mask = 1
        while (self.mask << 1) <= n:
            self.mask <<= 1

    def add(self, idx: int, delta: int) -> None:
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def sum(self, idx: int) -> int:
        total = 0
        while idx:
            total += self.bit[idx]
            idx -= idx & -idx
        return total

    def kth(self, k: int) -> int:
        idx = 0
        step = self.mask
        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            step >>= 1
        return idx + 1


class ActiveSet:
    """Store active DFS positions by 64-position blocks."""

    def __init__(self, n: int):
        self.n = n
        self.blocks = (n + 63) >> 6
        self.bits = [0] * self.blocks
        self.non_empty = 0
        self.fw = Fenwick(self.blocks)

    @staticmethod
    def first_bit(mask: int) -> int:
        return (mask & -mask).bit_length() - 1

    def add(self, pos: int) -> None:
        idx = pos - 1
        block = idx >> 6
        bit = 1 << (idx & 63)

        if self.bits[block] == 0:
            self.fw.add(block + 1, 1)
            self.non_empty += 1
        self.bits[block] |= bit

    def remove(self, pos: int) -> None:
        idx = pos - 1
        block = idx >> 6
        bit = 1 << (idx & 63)

        self.bits[block] &= ~bit
        if self.bits[block] == 0:
            self.fw.add(block + 1, -1)
            self.non_empty -= 1

    def first_pos(self) -> int:
        block = self.fw.kth(1) - 1
        return (block << 6) + self.first_bit(self.bits[block]) + 1

    def last_pos(self) -> int:
        block = self.fw.kth(self.non_empty) - 1
        return (block << 6) + self.bits[block].bit_length()

    def next_pos(self, pos: int) -> int:
        # Strictly after pos.
        idx = pos
        block = idx >> 6
        offset = idx & 63
        if block >= self.blocks:
            return 0

        cur = self.bits[block] & (-1 << offset)
        if cur:
            return (block << 6) + self.first_bit(cur) + 1

        before = self.fw.sum(block + 1)
        if before == self.non_empty:
            return 0

        block = self.fw.kth(before + 1) - 1
        return (block << 6) + self.first_bit(self.bits[block]) + 1

    def prev_pos(self, pos: int) -> int:
        # Strictly before pos.
        idx = pos - 2
        if idx < 0:
            return 0

        block = idx >> 6
        offset = idx & 63
        cur = self.bits[block] & ((1 << (offset + 1)) - 1)
        if cur:
            return (block << 6) + cur.bit_length()

        before = self.fw.sum(block)
        if before == 0:
            return 0

        block = self.fw.kth(before) - 1
        return (block << 6) + self.bits[block].bit_length()


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    ptr = 0
    n = data[ptr]
    q = data[ptr + 1]
    ptr += 2

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = data[ptr]
        v = data[ptr + 1]
        ptr += 2
        adj[u].append(v)
        adj[v].append(u)

    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = [0] * (n + 1)

    stack = [1]
    timer = 0
    while stack:
        u = stack.pop()
        timer += 1
        tin[u] = tout[u] = timer
        order[timer] = u

        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)

    for idx in range(n, 1, -1):
        u = order[idx]
        p = parent[u]
        if tout[u] > tout[p]:
            tout[p] = tout[u]

    log = n.bit_length()
    up = [parent[:]]
    for level in range(1, log):
        prev = up[level - 1]
        cur = [0] * (n + 1)
        for u in range(1, n + 1):
            cur[u] = prev[prev[u]]
        up.append(cur)

    def ancestor(u: int, v: int) -> bool:
        return tin[u] <= tin[v] <= tout[u]

    def child_below(u: int, x: int) -> int:
        # x is inside u subtree; return the direct child of u that contains x.
        diff = depth[x] - depth[u] - 1
        bit = 0
        while diff:
            if diff & 1:
                x = up[bit][x]
            diff >>= 1
            bit += 1
        return x

    active_pos = ActiveSet(n)
    active = bytearray(n + 1)
    leaf = bytearray(n + 1)
    active_count = 0
    leaf_count = 0

    def prev_node(pos: int) -> int:
        prev_pos = active_pos.prev_pos(pos)
        return order[prev_pos if prev_pos else active_pos.last_pos()]

    def next_node(pos: int) -> int:
        nxt_pos = active_pos.next_pos(pos)
        return order[nxt_pos if nxt_pos else active_pos.first_pos()]

    def check_leaf(u: int, pre: int, nxt: int) -> bool:
        if active_count <= 2:
            return True

        in_pre = ancestor(u, pre)
        in_next = ancestor(u, nxt)
        if not in_pre and not in_next:
            return True
        if in_pre != in_next:
            return False
        return child_below(u, pre) == child_below(u, nxt)

    def set_leaf(u: int, now: bool) -> None:
        nonlocal leaf_count
        if now != bool(leaf[u]):
            leaf_count += 1 if now else -1
            leaf[u] = 1 if now else 0

    out = []
    for _ in range(q):
        u = data[ptr]
        ptr += 1
        pos = tin[u]

        if active[u]:
            total = active_count
            pre = nxt = pre2 = nxt2 = 0

            if total > 1:
                pre = prev_node(pos)
                nxt = next_node(pos)
                if total > 3:
                    pre2 = prev_node(tin[pre])
                    nxt2 = next_node(tin[nxt])

            leaf_count -= leaf[u]
            leaf[u] = 0
            active[u] = 0
            active_count -= 1
            active_pos.remove(pos)

            if active_count == 1:
                set_leaf(pre, True)
            elif active_count == 2:
                set_leaf(pre, True)
                set_leaf(nxt, True)
            elif active_count > 2:
                set_leaf(pre, check_leaf(pre, pre2, nxt))
                set_leaf(nxt, check_leaf(nxt, pre, nxt2))
        else:
            active[u] = 1
            active_count += 1
            active_pos.add(pos)

            if active_count == 1:
                set_leaf(u, True)
            elif active_count == 2:
                other = prev_node(pos)
                set_leaf(u, True)
                set_leaf(other, True)
            else:
                pre = prev_node(pos)
                nxt = next_node(pos)
                pre2 = prev_node(tin[pre])
                nxt2 = next_node(tin[nxt])

                set_leaf(u, check_leaf(u, pre, nxt))
                set_leaf(pre, check_leaf(pre, pre2, u))
                set_leaf(nxt, check_leaf(nxt, u, nxt2))

        # A tree with L leaves can be covered by ceil(L / 2) paths.
        out.append(str((leaf_count + 1) >> 1))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
