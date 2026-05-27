import sys

def debug(*x, **y): print('---', *x, file=sys.stderr, **y)

arr = [0, 1, 5, 2, 6, 4, 9, 3, 7, 8]
p = [3, 1, 2, 3, 4]
meme: dict[tuple, int] = {}

def ask(i, j):
    if i == j: return 0
    if (i, j) in meme: return meme[(i, j)]
    if (j, i) in meme: return 1 - meme[(j, i)]
    arr[0] += 1
    print('?', i, j, flush=True)
    if sys.stdin.isatty():
        meme[(i, j)] = 1 if arr[i] > arr[j] else 0
    else:
        meme[(i, j)] = int(input())
    return meme[(i, j)]

def answer(x):
    print('!', x, 1, flush=True)

def read():
    if sys.stdin.isatty(): return p.pop()
    return int(input())

class SegmentTree: # by domigo
    def __init__(self, n: int):
        self.n = n # dùng khi cần truy vấn đoạn liên tiếp chính xác 
        self.tree = [-1] * (self.n << 2)

    def _build(self, node, start, end, data, l):
        if l > end or l + len(data) - 1 < start: return
        if start == end: self.tree[node] = data[start-l]; return
        mid = (start + end) >> 1
        ln, rn = node << 1, node << 1 | 1
        self._build(ln, start, mid, data, l)
        self._build(rn, mid + 1, end, data, l)
        self.tree[node] = self.__calc(self.tree[ln], self.tree[rn])

    def build(self, data, l):
        self._build(1, 1, self.n, data, l)
    
    def _delete(self, node, start, end, val):
        if start == end and self.tree[node] == val:
            self.tree[node] = -1
            return
        mid = (start + end) >> 1
        ln, rn = node << 1, node << 1 | 1
        if self.tree[ln] == val:
            self._delete(ln, start, mid, val)
        elif self.tree[rn] == val:
            self._delete(rn, mid + 1, end, val)
        self.tree[node] = self.__calc(self.tree[ln], self.tree[rn])
    
    def delete(self, val: int):
        self._delete(1, 1, self.n, val)


    def __calc(self, left, right):# define logic here
        if left == -1: return right
        if right == -1: return left
        return right if ask(left, right) else left

def solve():
    n = read()
    a = SegmentTree(2048)
    l = 1
    for q in range(n):
        x = read()
        a.build(list(range(l, l + x)), l)
        l += x
        idx = a.tree[1]
        answer(idx)
        # debug(arr[0])
        if q != n - 1: a.delete(idx)
solve()