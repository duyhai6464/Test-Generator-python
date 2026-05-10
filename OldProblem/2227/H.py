import sys
from collections import deque

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

def run():
    n = read()
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = read(), read()
        adj[u].append(v)
        adj[v].append(u)
    # Tập S là các đỉnh có bậc <= 1. Với N >= 3, lá là đỉnh có degree == 1
    leaves_list = [i for i in range(1, n + 1) if len(adj[i]) == 1]
    
    # Chọn 1 gốc không phải là lá để dễ tính toán
    root = 1
    for i in range(1, n + 1):
        if len(adj[i]) > 1:
            root = i
            break
            
    # Duyệt BFS/DFS iterative để lấy thứ tự tính toán (topological order)
    parent = [0] * (n + 1)
    order = []
    stack = [root]
    parent[root] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if parent[v] == 0:
                parent[v] = u
                stack.append(v)
    
    # Đếm số lá trong cây con của mỗi nút
    leaf_count = [0] * (n + 1)
    for leaf in leaves_list:
        leaf_count[leaf] = 1
        
    for u in reversed(order):
        if parent[u] != -1:
            leaf_count[parent[u]] += leaf_count[u]
    num_leaves = len(leaves_list)
    # Tính Base Cost (giả định dùng mọi cạnh có leaf_count lẻ)
    base_cost = 0
    for i in range(1, n + 1):
        if i != root:
            if leaf_count[i] % 2 == 1:
                base_cost += 1
    if num_leaves % 2 == 0:
        return base_cost
    # Nếu số lá lẻ, tìm lá x để bỏ lại sao cho cost giảm mạnh nhất
    # f[u] = số cạnh (lẻ) - số cạnh (chẵn) trên đường từ root tới u
    f = [0] * (n + 1)
    max_reduction = -1e18
    
    for u in order:
        if u != root:
            # Nếu cạnh tới cha là lẻ, bỏ lá ở dưới sẽ làm nó thành chẵn (-1 cost)
            # Nếu cạnh tới cha là chẵn, bỏ lá ở dưới sẽ làm nó thành lẻ (+1 cost)
            change = 1 if (leaf_count[u] % 2 == 1) else -1
            f[u] = f[parent[u]] + change
        
        if len(adj[u]) == 1: # Chỉ xét bỏ các đỉnh là lá
            if f[u] > max_reduction:
                max_reduction = f[u]
    
    return base_cost - max_reduction

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))