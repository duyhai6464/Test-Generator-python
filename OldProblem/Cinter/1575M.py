import sys
from bisect import bisect_left

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

# Hàm tính điểm giao của hai parabol (x-i)^2 + g_i và (x-j)^2 + g_j
def intersect(i, j, col_g):
    return (col_g[j] + j*j - (col_g[i] + i*i)) / (2 * (j - i))

def run():
    n, m = read(), read()
    A = [read_t() for _ in range(n + 1)]
    # print(*A, sep="\n", file=sys.stderr)
    INF = int(1e9)
    d = [[INF] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        last = -INF
        for j in range(m + 1):
            if A[i][j] == '1': last = j
            d[i][j] = (j - last) ** 2
        last = -INF
        for j in range(m, -1, -1):
            if A[i][j] == '1': last = j
            d[i][j] = min(d[i][j], (j - last) ** 2)
        # print(*d[i], file=sys.stderr)
        
    total_sum = 0
    for j in range(m + 1):
        col = [d[i][j] for i in range(n + 1)]
        # q lưu chỉ số các parabol trong bao dưới, s lưu các điểm giao
        q = [0] * (n + 1)
        s = [0.0] * (n + 2)
        h = 0 # đầu hàng đợi
        ## Xây dựng bao dưới
        for i in range(1, n + 1):
            if col[i] >= INF: continue
            while h >= 0:
                idx = q[h]
                if col[idx] >= INF: # Nếu parabol cũ là vô hạn
                    h -= 1
                    continue
                f_inter = intersect(idx, i, col)
                if f_inter <= s[h]:
                    h -= 1
                else:
                    s[h + 1] = f_inter
                    break
            h += 1
            q[h] = i
            s[h + 1] = INF
        if h < 0: continue
        # print(*q, file=sys.stderr)
        # print(*s, file=sys.stderr)
        # tính kq trên cột j
        cp = 0
        for i in range(n + 1):
            while cp + 2 < len(s) and s[cp + 1] < i:
                cp += 1
            best_i = q[cp]
            total_sum += (i - best_i)**2 + col[best_i]
        #     print((i - best_i)**2 + col[best_i], file=sys.stderr, end=' ')
        # print(file=sys.stderr)
    return total_sum

t = 1
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))