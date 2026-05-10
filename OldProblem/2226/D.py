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
    min_value = [n + 1, n + 1]
    max_value = [0, 0]
    for value in a:
        parity = value & 1
        if value < min_value[parity]:
            min_value[parity] = value
        if value > max_value[parity]:
            max_value[parity] = value

    if max_value[0] == 0 or max_value[1] == 0:
        for i in range(n - 1):
            if a[i] > a[i + 1]:
                return "NO"
        return "YES"

    def check(parity: int) -> bool:
        low_limit = min_value[parity ^ 1]
        high_limit = max_value[parity ^ 1]
        seen_high = False
        for value in a:
            if (value & 1) != parity:
                continue
            if seen_high and value <= low_limit:
                return False
            if value >= high_limit:
                seen_high = True
        return True

    return "YES" if check(0) and check(1) else "NO"

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))
