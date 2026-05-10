import sys
from typing import Any

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

class Node:
    def __init__(self, val):
        self.val = val
        self.left: Node|None = None
        self.right: Node|None = None

class BalancedBST:
    def __init__(self, sorted_values: list[int] = []):
        self.root = self._build(sorted_values, 0, len(sorted_values)-1)

    def _build(self, arr: list[int], l: int, r: int) -> Node|None:
        if l > r:
            return None
        mid = (l + r) // 2
        node = Node(arr[mid])
        node.left = self._build(arr, l, mid-1)
        node.right = self._build(arr, mid+1, r)
        return node

    def find_max_less_than(self, x):
        cur = self.root
        candidate = None
        while cur:
            if cur.val < x:
                candidate = cur.val
                cur = cur.right
            else:
                cur = cur.left
        return candidate

    def erase(self, val):
        self.root = self._erase(self.root, val)

    def _erase(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._erase(node.left, val)
        elif val > node.val:
            node.right = self._erase(node.right, val)
        else:
            # xóa node
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # có 2 con: lấy successor
            succ = self._min_node(node.right)
            node.val = succ.val
            node.right = self._erase(node.right, succ.val)
        return node

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

def run():
    n = read()
    last = -1
    A = [0] * n
    has = [False] * (n + 1)
    for i in range(n):
        x = read()
        if x == last: A[i] = -1
        else: A[i] = last = x
        has[x] = True
    minA = []
    maxA = []
    min_i = 1
    max_i = n
    missing = [i for i in range(1, n + 1) if not has[i]]
    tree = BalancedBST(missing)
    for i in range(n):
        if A[i] != -1:
            minA.append(A[i])
            maxA.append(A[i])
            max_i = A[i]
        else:
            while has[min_i]: min_i += 1
            minA.append(min_i)
            min_i += 1
            val = tree.find_max_less_than(max_i)
            maxA.append(val)
            tree.erase(val)
            
    out.append(' '.join(map(str, minA)))
    return ' '.join(map(str, maxA))

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))