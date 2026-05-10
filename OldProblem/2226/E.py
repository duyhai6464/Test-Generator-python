import sys

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr = 0
out = []
def read(base: int = 10) -> int:
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return int(buffer[ptr - 1], base)

def read_t(t: type = str):
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    if t != str: return t(buffer[ptr - 1])
    return buffer[ptr - 1]

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, delta: int) -> None:
        idx += 1
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def sum_prefix(self, idx: int) -> int:
        if idx < 0:
            return 0
        idx += 1
        result = 0
        while idx > 0:
            result += self.bit[idx]
            idx -= idx & -idx
        return result

    def sum_suffix(self, idx: int) -> int:
        if idx <= 0:
            return self.sum_prefix(self.n - 1)
        if idx >= self.n:
            return 0
        return self.sum_prefix(self.n - 1) - self.sum_prefix(idx - 1)

class SegmentTree:
    def __init__(self, n: int):
        self.n = n
        self.minv = [0] * (4 * n)
        self.lazy = [0] * (4 * n)

    def _push(self, node: int) -> None:
        delta = self.lazy[node]
        if delta == 0:
            return
        left = node * 2
        right = left + 1
        self.minv[left] += delta
        self.minv[right] += delta
        self.lazy[left] += delta
        self.lazy[right] += delta
        self.lazy[node] = 0

    def _add(self, node: int, left: int, right: int, ql: int, qr: int, delta: int) -> None:
        if ql <= left and right <= qr:
            self.minv[node] += delta
            self.lazy[node] += delta
            return
        self._push(node)
        mid = (left + right) // 2
        if ql <= mid:
            self._add(node * 2, left, mid, ql, qr, delta)
        if mid < qr:
            self._add(node * 2 + 1, mid + 1, right, ql, qr, delta)
        self.minv[node] = min(self.minv[node * 2], self.minv[node * 2 + 1])

    def add(self, ql: int, qr: int, delta: int) -> None:
        if ql > qr:
            return
        self._add(1, 0, self.n - 1, ql, qr, delta)

    def _query_min(self, node: int, left: int, right: int, ql: int, qr: int) -> int:
        if ql <= left and right <= qr:
            return self.minv[node]
        self._push(node)
        mid = (left + right) // 2
        result = 10 ** 18
        if ql <= mid:
            result = self._query_min(node * 2, left, mid, ql, qr)
        if mid < qr:
            result = min(result, self._query_min(node * 2 + 1, mid + 1, right, ql, qr))
        return result

    def query_min(self, ql: int, qr: int) -> int:
        return self._query_min(1, 0, self.n - 1, ql, qr)

    def _set_point(self, node: int, left: int, right: int, idx: int, value: int) -> None:
        if left == right:
            self.minv[node] = value
            self.lazy[node] = 0
            return
        self._push(node)
        mid = (left + right) // 2
        if idx <= mid:
            self._set_point(node * 2, left, mid, idx, value)
        else:
            self._set_point(node * 2 + 1, mid + 1, right, idx, value)
        self.minv[node] = min(self.minv[node * 2], self.minv[node * 2 + 1])

    def set_point(self, idx: int, value: int) -> None:
        self._set_point(1, 0, self.n - 1, idx, value)

def run():
    n = read()
    a = [read() for _ in range(n)]
    max_a = max(a, default=0)
    count = [0] * (max(max_a, n) + 2)
    bit = Fenwick(max_a + 1)
    seg = SegmentTree(n + 1)

    mex = 0
    answer = []

    for value in a:
        first = count[value] == 0
        count[value] += 1
        bit.add(value, 1)

        if first and value < mex:
            seg.add(0, value, 1)
        else:
            limit = (value - 1) // 2
            if limit >= 0 and mex > 0:
                seg.add(0, min(limit, mex - 1), 1)

        while mex <= n:
            rollback_right = -1
            if count[mex] == 0:
                rollback_right = mex - 1
                if rollback_right >= 0:
                    seg.add(0, rollback_right, -1)
                point_value = bit.sum_suffix(2 * mex + 1) - 1
            else:
                rollback_right = min((mex - 1) // 2, mex - 1)
                if rollback_right >= 0:
                    seg.add(0, rollback_right, -1)
                point_value = bit.sum_suffix(2 * mex + 1)

            ok = point_value >= 0
            if ok and mex > 0:
                ok = seg.query_min(0, mex - 1) >= 0

            if not ok:
                if rollback_right >= 0:
                    seg.add(0, rollback_right, 1)
                break

            seg.set_point(mex, point_value)
            mex += 1

        answer.append(str(mex))

    return " ".join(answer)

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))
