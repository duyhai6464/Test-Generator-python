import sys, bisect

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def fi(x):
    s, p = 0, 0
    while x:
        d = x % 10
        x //= 10
        s += d
        p += d * d
    return s, p
        

def is_doub(x):
    if x <= 0: return False
    s, p = fi(x)
    m = s ** 4 + p ** 2
    return x % m == 0

sys.setrecursionlimit(10**5)
MAXX = int(2e9)
ans = []
def dfs_small(leng: int, s: int, p: int, val: int):
    if leng > 0:
        M = s ** 4 + p ** 2
        if val % M == 0: ans.append(val)
    if leng >= 10: return
    for d in range(10):
        if leng == 0 and d == 0: continue
        new_v = 10 * val + d
        if new_v > MAXX: break
        if s + d < 12: dfs_small(leng + 1, s + d, p + d * d, new_v)


N_str = str(MAXX)
L = len(N_str)

S_MAX = 83  # s từ 0 đến 82
P_MAX = 731 # p từ 0 đến 730
W = P_MAX
SIZE = S_MAX * W

# can[tight][s * W + p]
# Dùng 2 mảng để tiết kiệm bộ nhớ (hiện tại và kế tiếp)
can_tight = [False] * SIZE
can_free = [False] * SIZE

# Trạng thái cơ sở (Base case) tại vị trí cuối cùng (sau 10 chữ số)
# Tương đương can[10][0][0][tight] = True
can_tight[0 * W + 0] = True
can_free[0 * W + 0] = True

next_tight = [False] * SIZE
next_free = [False] * SIZE
for i in range(L - 1, -1, -1):
    for j in range(SIZE):
        next_tight[j] = next_free[j] = False
    up = int(N_str[i])

    for s in range(S_MAX):
        for p in range(P_MAX):
            idx = s * W + p
            # Nếu từ trạng thái này không thể đi tiếp, bỏ qua
            if not (can_tight[idx] or can_free[idx]):
                continue
            
            # Thử các chữ số d từ 0-9 để quay ngược lại trạng thái trước đó
            for d in range(10):
                ns, np = s + d, p + d * d
                if ns < S_MAX and np < P_MAX:
                    n_idx = ns * W + np
                    # Cập nhật trạng thái tự do (free)
                    next_free[n_idx] = next_free[n_idx] or can_free[idx]
                    
                    # Cập nhật trạng thái thắt chặt (tight)
                    if d < up:
                        next_tight[n_idx] = next_tight[n_idx] or can_free[idx]
                    elif d == up:
                        next_tight[n_idx] = next_tight[n_idx] or can_tight[idx]
    
    for i in range(SIZE):
        can_tight[i] = next_tight[i]
        can_free[i] = next_free[i]

# Trích xuất các cặp (s, p) có thể tạo ra số < 2e9
possible_pairs = []
for s in range(12, 68): # Chỉ xét s >= 12 để M đủ lớn
    for p in range(s, P_MAX):
        if can_tight[s * W + p]:
            possible_pairs.append((s, p))


dfs_small(0, 0, 0, 0)
# if s > 12
for s, p in possible_pairs:
    m = s ** 4 + p ** 2
    if m > MAXX: continue
    for x in range(m, MAXX, m):
        if x % 9 != s % 9: continue
        ts, tp = fi(x)
        if ts == s and tp == p:
            ans.append(x)

debug(len(ans))   
ans.sort()
debug(ans[-10:])

def run():
    l, r = read(), read()
    # res = []
    # for i in range(l, r + 1):
    #     if is_doub(i):
    #         res.append(i)
    # print(*res)
    print(bisect.bisect(ans, r) - bisect.bisect(ans, l - 1))

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))