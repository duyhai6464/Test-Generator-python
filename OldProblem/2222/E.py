import sys

buffer:list[str] = []
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

def ask_i(x):
    print(f"I {x}", flush=True)
    return int(sys.stdin.readline().strip())

def ask_q(y):
    print(f"Q {y}", flush=True)
    return int(sys.stdin.readline().strip())

def run():
    n = read()
    print(0, flush=True)
    current_s_size = 1
    res_i0 = ask_i(0)
    if res_i0 == 1:
        # k=1 (AND) vì 0 & c = 0, không tạo thêm phần tử mới
        k = 1
        c = 0
        current_s_size = 1
        # Tìm từng bit của c bằng I (2^i)
        for i in range(n - 1, -1, -1):
            val = 1 << i
            new_size = ask_i(val)
            if new_size > current_s_size:
                # Nếu size tăng, nghĩa là val & c = val -> bit i của c là 1
                c |= val
                current_s_size = new_size
        
        print(f"A {k} {c}", flush=True)
    else:
        # k là 2 (OR) hoặc 3 (XOR) vì 0 | c = c hoặc 0 ^ c = c (tạo ra phần tử mới)
        # Hiện tại S = {0, c}, size = 2
        c = 0
        # Bước 2: Tìm giá trị c bằng Q (vì hiện tại S chỉ có 0 và c)
        for i in range(n - 1, -1, -1):
            target = c | (1 << i)
            if ask_q(target) == 1:
                # Nếu có phần tử >= target, đó chính là c
                c |= (1 << i)
        
        # Bước 3: Phân biệt OR (2) và XOR (3)
        # Dùng tối đa 2 truy vấn còn lại
        if c < (1 << n) - 1:
            # Nếu c chưa phải là số toàn bit 1, thử I với số toàn bit 1 (mask)
            mask = (1 << n) - 1
            ask_i(mask) # Thêm f(mask) vào S
            # f(mask) = mask | c (nếu OR) -> vẫn là mask
            # f(mask) = mask ^ c (nếu XOR) -> NOT c (nhỏ hơn mask)
            if ask_q(mask) == 1:
                k = 2 # Là OR
            else:
                k = 3 # Là XOR
        else:
            # Nếu c = 111...1, dùng I 1
            # f(1) = 1 | c = c (nếu OR) -> không tăng size
            # f(1) = 1 ^ c = c - 1 (nếu XOR) -> tăng size lên 3
            new_size = ask_i(1)
            if new_size > 2:
                k = 3
            else:
                k = 2
        print(f"A {k} {c}", flush=True)

t = read()
for _ in range(t):
    out.append(str(run()))
    
# sys.stdout.write("\n".join(map(str, out)))