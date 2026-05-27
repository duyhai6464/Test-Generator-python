import sys


def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def sum_consecutive(left: int, right: int) -> int:
    count = right - left + 1
    return count * (left + right) // 2


MOD = 10**9 + 21
def query_sum(row1: int, col1: int, row2: int, col2: int, cols: int) -> int:
    height = row2 - row1 + 1
    width = col2 - col1 + 1

    row_offsets = sum_consecutive(row1 - 1, row2 - 1) % MOD
    col_values = sum_consecutive(col1, col2) % MOD

    row_part = (width % MOD) * (cols % MOD) % MOD * row_offsets
    col_part = (height % MOD) * col_values
    return (row_part + col_part) % MOD

n, m, t = read(), read(), read()
res = 0

for _ in range(t):
    res ^= query_sum(read(), read(), read(), read(), m)
    
print(res)