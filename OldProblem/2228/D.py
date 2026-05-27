import sys
from array import array


data = sys.stdin.buffer.read()
data_len = len(data)
ptr = 0


def read_int():
    global ptr
    while ptr < data_len and data[ptr] <= 32:
        ptr += 1
    value = 0
    while ptr < data_len and data[ptr] > 32:
        value = value * 10 + data[ptr] - 48
        ptr += 1
    return value


def solve_case(n):
    xs = array("I")
    ys = array("I")
    count_x = array("i", [0]) * (n + 2)
    present_y = bytearray(n + 2)

    for _ in range(n):
        x = read_int()
        y = read_int()
        xs.append(x)
        ys.append(y)
        count_x[x] += 1
        present_y[y] = 1

    y_rank = array("i", [0]) * (n + 2)
    y_count = 0
    for y in range(1, n + 1):
        if present_y[y]:
            y_rank[y] = y_count
            y_count += 1

    start = array("i", [0]) * (n + 2)
    pos = 0
    for x in range(1, n + 1):
        start[x] = pos
        pos += count_x[x]
    start[n + 1] = pos

    write_pos = array("i", start)
    by_x_y = array("i", [0]) * n
    rank_freq = array("i", [0]) * y_count

    for i in range(n):
        x = xs[i]
        yr = y_rank[ys[i]]
        p = write_pos[x]
        by_x_y[p] = yr
        write_pos[x] = p + 1
        rank_freq[yr] += 1

    left_min = y_count
    left_max = -1
    right_min = 0
    right_max = y_count - 1
    moved = 0
    answer = 0

    for x in range(1, n + 1):
        begin = start[x]
        end = start[x + 1]
        if begin == end:
            continue

        for p in range(begin, end):
            yr = by_x_y[p]
            if yr < left_min:
                left_min = yr
            if yr > left_max:
                left_max = yr
            rank_freq[yr] -= 1

        moved += end - begin
        while right_min < y_count and rank_freq[right_min] == 0:
            right_min += 1
        while right_max >= 0 and rank_freq[right_max] == 0:
            right_max -= 1

        if moved == n:
            break

        low = left_min if left_min > right_min else right_min
        high = left_max if left_max < right_max else right_max
        if high > low:
            answer += high - low

    return answer


def main():
    if not data:
        return

    t = read_int()
    out = []
    for _ in range(t):
        n = read_int()
        out.append(str(solve_case(n)))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
