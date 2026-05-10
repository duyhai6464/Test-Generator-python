import sys

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

def find(p, i):
    root = i
    while p[root] != root:
        root = p[root]
    while p[i] != root:
        nxt = p[i]
        p[i] = root
        i = nxt
    return root

def union(p, i, j):
    root_i = find(p, i)
    root_j = find(p, j)
    if root_i != root_j:
        p[root_i] = root_j
        return True
    return False

def run():
    n, m, q = read(), read(), read()
    
    # Khởi tạo các mảng DSU cho 3 điều kiện liên thông
    p0 = list(range(n + 1))  # Đường đi không chứa 0 (cost 0)
    p1 = list(range(n + 1))  # Đường đi không chứa 1 (cost <= 1)
    pa = list(range(n + 1))  # Đường đi bất kỳ (check -1)

    # Xử lý m cạnh ban đầu
    for _ in range(m):
        u, v, w = read(), read(), read()
        union(pa, u, v)
        if w >= 1:
            union(p0, u, v)
        if w != 1:
            union(p1, u, v)
    
    # Đọc q đỉnh trong đồ thị mới
    Q = [read() for _ in range(q)]
    
    if q <= 1:
        return 0
    
    # 1. Kiểm tra tính liên thông toàn cục (nếu không liên thông thì cost = -1)
    root_all = find(pa, Q[0])
    for i in range(1, q):
        if find(pa, Q[i]) != root_all:
            return -1
            
    # 2. k: Số lượng thành phần liên thông 'mex 0' trong Q
    q_p0_roots = set()
    for node in Q:
        q_p0_roots.add(find(p0, node))
    k = len(q_p0_roots)
    
    # 3. L: Số lượng thành phần sau khi nối các đỉnh Q bằng cạnh 'mex 1'
    # Hai thành phần p0 có thể nối với nhau nếu tồn tại các đỉnh trong Q 
    # cùng thuộc một thành phần p1.
    pm = {r0: r0 for r0 in q_p0_roots}
    def find_m(i):
        if pm[i] == i: return i
        pm[i] = find_m(pm[i])
        return pm[i]
    
    def union_m(i, j):
        ri, rj = find_m(i), find_m(j)
        if ri != rj: pm[ri] = rj

    p1_map = {} # r1 -> r0
    for node in Q:
        r0 = find(p0, node)
        r1 = find(p1, node)
        if r1 in p1_map:
            union_m(r0, p1_map[r1])
        else:
            p1_map[r1] = r0
    
    l_val = len(set(find_m(r0) for r0 in q_p0_roots))
    
    # 4. Công thức MST: k + L - 2
    # Giải thích: Cần (k-L) cạnh trọng số 1 và (L-1) cạnh trọng số 2
    return k + l_val - 2

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))