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

def run():
    n = read()
    v = [0] * (n + 1)
    for i in range(1, n + 1):
        v[i] = v[i - 1] + read()
    # 2. Lấy danh sách các chỉ số (0 đến n-1)
    # Sắp xếp chỉ số theo giá trị V tăng dần
    # V càng nhỏ thì vị trí đó sẽ được gán giá trị hoán vị p càng lớn
    indices = sorted(range(n), key=lambda i: v[i])
    # 3. Gán giá trị từ n xuống 1 vào các vị trí đã sắp xếp
    p = [0] * n
    current_p_val = n
    for idx in indices:
        p[idx] = current_p_val
        current_p_val -= 1
    return " ".join(map(str, p))

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))