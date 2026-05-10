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
    n, a, b = read(), read_t(), read_t()
    bal_A = 0
    bal_B = 0
    possible = True
    
    for i in range(n):
        if a[i] == b[i]:
            if a[i] == '(':
                bal_A += 1
                bal_B += 1
            else:
                bal_A -= 1
                bal_B -= 1
        else:
            if bal_A <= bal_B:
                bal_A += 1
                bal_B -= 1
            else:
                bal_A -= 1
                bal_B += 1
        
        # Nếu tại bất kỳ thời điểm nào balance bị âm, ta không thể tạo RBS
        if bal_A < 0 or bal_B < 0:
            possible = False
            break
    
    # Kết thúc chuỗi, balance của cả 2 phải bằng 0
    if possible and bal_A == 0 and bal_B == 0:
        return "YES"
    return "NO"

t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))