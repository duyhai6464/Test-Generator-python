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

def run():
    n, s = read(), list(map(int, read_t()))
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = read() - 1, read() - 1# Chuyển về 0-indexed
        adj[u].append(v)
        adj[v].append(u)
    
    memo = {}

    def get_expected_value(current_state):
        # Trạng thái mục tiêu: tất cả là 1 (đỏ)
        if all(current_state):
            return 0
        
        state_tuple = tuple(current_state)
        if state_tuple in memo:
            return memo[state_tuple]
        
        min_ev = float('inf')
        
        # Thử chọn từng đỉnh 'a' đang là màu đen (0)
        for a in range(n):
            if current_state[a] == 0:
                # Đếm số hàng xóm màu đỏ
                red_neighbors = sum(1 for neighbor in adj[a] if current_state[neighbor] == 1)
                
                # Chỉ có thể đổi màu nếu có ít nhất 1 hàng xóm màu đỏ
                if red_neighbors > 0:
                    degree = len(adj[a])
                    
                    # Chuyển trạng thái: đỉnh a thành đỏ
                    new_state = list(current_state)
                    new_state[a] = 1
                    
                    # Công thức: E(S) = d(a)/r(a) + E(S_mới)
                    ev = (degree / red_neighbors) + get_expected_value(new_state)
                    
                    if ev < min_ev:
                        min_ev = ev
        
        memo[state_tuple] = min_ev
        return min_ev

    result = get_expected_value(s)
    print(f"{result:.10f}")

t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))