import sys

sys.setrecursionlimit(10**5)

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr = 0
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

MAXN = 10**3 + 5
w = [0] * MAXN
n, s_limit = read(), read()
for i in range(1, n + 1): w[i] = read()
G = {i : [] for i in range(1, n + 1)}
for _ in range(n - 1):
    u, v = read(), read()
    G[u].append(v)
    G[v].append(u)

# debug(f"n = {n}, s = {s_limit}, w = {w[1:n+1]}, G = {G}")
    
# dp[u][state] = {tổng_có_thể: (tổng_con_v, trạng_thái_v)}
# state 0: không chọn u, state 1: chọn u
# Để truy vết, ta cần lưu lại lịch sử thay đổi của dict sau mỗi lần gộp con
dp0 = [{} for _ in range(n + 1)]
dp1 = [{} for _ in range(n + 1)]
history0 = [[] for _ in range(n + 1)] # Lưu (v, dict_trước_khi_gộp)
history1 = [[] for _ in range(n + 1)]

def dfs(u, p):
    # Khởi tạo
    dp0[u][0] = None
    if w[u] <= s_limit:
        dp1[u][w[u]] = None
    
    for v in G[u]:
        if v == p: continue
        dfs(v, u)
        
        # Lưu lại trạng thái trước khi gộp để truy vết
        history0[u].append((v, dp0[u].copy()))
        history1[u].append((v, dp1[u].copy()))
        
        # Gộp cho dp1 (Chọn u -> v bắt buộc không chọn)
        new_dp1 = {}
        for s_u in dp1[u]:
            for s_v in dp0[v]:
                if s_u + s_v <= s_limit:
                    new_dp1[s_u + s_v] = s_v # Lưu lại s_v để traceback
        dp1[u] = new_dp1
        
        # Gộp cho dp0 (Không chọn u -> v có thể chọn hoặc không)
        new_dp0 = {}
        # Các tổng có thể từ v: (giá trị, trạng thái của v)
        v_options = []
        for s_v in dp0[v]: v_options.append((s_v, 0))
        for s_v in dp1[v]: v_options.append((s_v, 1))
        
        for s_u in dp0[u]:
            for s_v, v_st in v_options:
                if s_u + s_v <= s_limit:
                    if (s_u + s_v) not in new_dp0:
                        new_dp0[s_u + s_v] = (s_v, v_st)
        dp0[u] = new_dp0

dfs(1, 0)

# Truy vết tìm tập hợp các đỉnh
res_nodes = []
def backtrack(u, current_sum, state):
    if state == 1:
        res_nodes.append(u)
        rem_sum = current_sum - w[u]
        # Duyệt ngược lịch sử gộp các con của u
        for v, old_dp_state in reversed(history1[u]):
            s_v = dp1[u][current_sum] # Đây là s_v đã đóng góp
            backtrack(v, s_v, 0)
            current_sum -= s_v
            dp1[u] = old_dp_state # Quay lại trạng thái dict trước đó
    else:
        for v, old_dp_state in reversed(history0[u]):
            s_v, v_st = dp0[u][current_sum]
            backtrack(v, s_v, v_st)
            current_sum -= s_v
            dp0[u] = old_dp_state

# Tìm xem tổng S nằm ở dp0 hay dp1 của gốc
if s_limit in dp1[1]:
    backtrack(1, s_limit, 1)
elif s_limit in dp0[1]:
    backtrack(1, s_limit, 0)

# In kết quả
print(len(res_nodes))
print(*res_nodes)
