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

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def run():
    n = read()
    data = [[read(), i + 1] for i in range(n)]
    steps = []
    while True:
        active = [v for v in data if v[0] > 0]
        active.sort(key=lambda x: x[0])
        if len(active) >= 3:
            # Sử dụng thuật toán 3 bình để triệt tiêu bình nhỏ thứ hai (b)
            a = active[0]  # Bình nhỏ nhất
            b = active[1]  # Bình nhỏ thứ hai
            c = active[-1] # Bình lớn nhất (đóng vai trò bình đệm)
            
            q = b[0] // a[0]
            # Chuyển q sang nhị phân và duyệt từ bit thấp đến cao
            binary_q = bin(q)[2:][::-1]
            
            for bit in binary_q:
                if bit == '1':
                    # Đổ từ b sang a
                    steps.append((b[1], a[1]))
                    b[0] -= a[0]
                    a[0] *= 2
                else:
                    # Đổ từ c sang a
                    steps.append((c[1], a[1]))
                    c[0] -= a[0]
                    a[0] *= 2
        elif len(active) == 2:
            # Trường hợp còn 2 bình, kiểm tra xem có thể đưa về 1 bình không
            a = active[0]
            b = active[1]
            if a[0] > b[0]: a, b = b, a
            
            s_sum = a[0] + b[0]
            g = gcd(a[0], b[0])
            ratio = s_sum // g
            
            # Điều kiện để làm rỗng 1 trong 2 bình là tổng/gcd là lũy thừa của 2
            if ratio > 0 and (ratio & (ratio - 1)) == 0:
                while a[0] > 0:
                    if b[0] < a[0]: a, b = b, a
                    steps.append((b[1], a[1]))
                    b[0] -= a[0]
                    a[0] *= 2
                    if a[0] > b[0]: a, b = b, a
                break
            else:
                break
        else:
            break
    out.append(len(steps))
    return "\n".join(f"{x[0]} {x[1]}" for x in steps)

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))