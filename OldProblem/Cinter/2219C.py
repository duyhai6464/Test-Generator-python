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
    n, s = read(), read_t()
    adj = [[] for _ in range(n)]
    degree = [0] * n
    for _ in range(n - 1):
        u, v = read() - 1, read() - 1# Chuyển về 0-indexed
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1
    root = -1
    for i in range(n):
        if s[i] == '1':
            root = i
            break
    order = []
    parent = [-1] * n
    stack = [root]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)
    dp0 = [0.0] * n
    dp1 = [0.0] * n
    INF = 1e18
    # Duyệt từ lá lên gốc
    for u in reversed(order):
        children = [v for v in adj[u] if v != parent[u]]
        if s[u] == '1':
            # Nếu là đỉnh đỏ: Đã xong, chỉ cần cộng chi phí hoàn thành các cây con
            res = 0.0
            for v in children:
                # Vì u đã đỏ, các con v sẽ coi u là cha đã đỏ -> lấy min(dp0, dp1)
                # Với đỉnh đen dp1 < dp0, với đỉnh đỏ dp0 < dp1=inf
                res += dp1[v] if dp1[v] < dp0[v] else dp0[v]
            dp0[u] = res
            dp1[u] = INF # Đỉnh đỏ không cần cha giúp
        else:
            # Đỉnh ĐEN:
            red_children_cost = 0.0
            num_red_children = 0
            black_diffs = []
            base_black_cost = 0.0
            
            # Tách con đỏ và con đen
            for v in children:
                if s[v] == '1' or dp0[v] < INF/2: # v là đỏ hoặc có đường dẫn tới đỏ
                    if dp0[v] < dp1[v]: # v đóng vai trò là nguồn đỏ
                        red_children_cost += dp0[v]
                        num_red_children += 1
                    else:
                        base_black_cost += dp1[v]
                        black_diffs.append(dp0[v] - dp1[v])
                else:
                    base_black_cost += dp1[v]
                    black_diffs.append(dp0[v] - dp1[v])
            
            black_diffs.sort()
            d_u = float(degree[u])

            # Tính dp0: u đỏ trước cha (cần ít nhất 1 nguồn từ con)
            best_dp0 = INF
            curr_sum = red_children_cost + base_black_cost
            # k = số nguồn đỏ từ con
            for m in range(len(black_diffs) + 1):
                k = num_red_children + m
                if k > 0:
                    best_dp0 = min(best_dp0, curr_sum + d_u / k)
                if m < len(black_diffs):
                    curr_sum += black_diffs[m]
            dp0[u] = best_dp0

            # Tính dp1: u đỏ sau cha (cha là 1 nguồn chắc chắn)
            best_dp1 = INF
            curr_sum = red_children_cost + base_black_cost
            for m in range(len(black_diffs) + 1):
                k = num_red_children + m + 1 # +1 từ cha
                best_dp1 = min(best_dp1, curr_sum + d_u / k)
                if m < len(black_diffs):
                    curr_sum += black_diffs[m]
            dp1[u] = best_dp1
    
    # debug(f"root{root}order {order}")
    # debug(f"dp0{dp0}")
    # debug(f"dp1{dp1}")
    
    return f"{dp0[root]:.10f}"

t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))