import sys


def debug(*x, **y):
    print(*x, file=sys.stderr, **y)


buffer: list[str] = sys.stdin.read().split()
ptr, out = 0, []


def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])


def all_same(bits):
    first = bits[0]
    for value in bits[1:]:
        if value != first:
            return False
    return True


def run():
    n, m = read(), read()
    grid = [[0] * m for _ in range(n)]
    row_parity = [0] * n
    col_parity = [0] * m

    for i in range(n):
        parity = 0
        row = grid[i]
        for j in range(m):
            value = read()
            row[j] = value
            parity ^= value
            col_parity[j] ^= value
        row_parity[i] = parity

    total_parity = 0
    for value in row_parity:
        total_parity ^= value

    if m % 2 == 0 and n % 2 == 0:
        row_press = [value ^ total_parity for value in row_parity]
        col_press = [value ^ total_parity for value in col_parity]
    elif m % 2 == 0:
        if not all_same(col_parity):
            return "NO"
        col_sum = total_parity ^ col_parity[0]
        row_press = [value ^ col_sum for value in row_parity]
        col_press = [0] * m
        col_press[0] = col_sum
    elif n % 2 == 0:
        if not all_same(row_parity):
            return "NO"
        row_sum = total_parity ^ row_parity[0]
        row_press = [0] * n
        row_press[0] = row_sum
        col_press = [value ^ row_sum for value in col_parity]
    else:
        if not all_same(row_parity) or not all_same(col_parity):
            return "NO"
        row_press = [0] * n
        col_press = [0] * m
        row_press[0] = total_parity
        col_press[0] = total_parity

    answer = ["YES"]
    for i in range(n):
        ri = row_press[i]
        answer.append(" ".join(
            "1" if grid[i][j] ^ ri ^ col_press[j] else "0"
            for j in range(m)
        ))
    return "\n".join(answer)


_ = read()  # subtask index, not needed for the solution
t = read()
for _ in range(t):
    output = run()
    if output is not None:
        out.append(output)

sys.stdout.write("\n".join(map(str, out)))
