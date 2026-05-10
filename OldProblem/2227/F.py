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
    n = read()
    a = [read() for _ in range(n)]
    max_a = max(a) + 1
    cnt = [0] * max_a # cnt[x] is count col has height == x
    for x in a: cnt[x] += 1
    c = [0] * (max_a + 1) # c[h] is number col has height >= h
    for h in range(max_a - 1, 0, -1): c[h] = c[h + 1] + cnt[h]
    # debug(cnt, c)
    # 2. Tính tổng khoảng cách ban đầu
    # D = Sum(Final positions) - Sum(Initial positions)
    sum_initial = 0
    for i, val in enumerate(a):
        sum_initial += (i + 1) * val
        
    sum_final = 0
    for h in range(1, max_a + 1):
        num_blocks = c[h]
        # Tổng các số từ n-num_blocks+1 đến n
        # Công thức: (đầu + cuối) * số_lượng / 2
        sum_final += (n + (n - num_blocks + 1)) * num_blocks // 2
        
    base_distance = sum_final - sum_initial
    
    # 3. Tìm lựa chọn xóa 1 khối tối ưu nhất
    max_adjustment = 0
    for i, val in enumerate(a):
        if val > 0:
            # i+1 là vị trí cột (1-indexed)
            # H = val là độ cao của khối trên cùng
            adjustment = (i + 1) - n + c[val] - 1
            if adjustment > max_adjustment:
                max_adjustment = adjustment
    return base_distance + max_adjustment

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))