import sys
from bisect import bisect_left, bisect_right


INF = 10**30


def debug(*x, **y): print(*x, file=sys.stderr, **y)


def read_ints():
    data = sys.stdin.buffer.read()
    value = 0
    in_number = False
    for byte in data:
        if 48 <= byte <= 57:
            value = value * 10 + byte - 48
            in_number = True
        elif in_number:
            yield value
            value = 0
            in_number = False
    if in_number:
        yield value


def run():
    ints = read_ints()
    n = next(ints)
    p_values = [next(ints) for _ in range(n)]
    points = [(p_values[i], next(ints)) for i in range(n)]
    del p_values

    points.sort()
    # Keep only Pareto-minimal articles.  If another article has both
    # coordinates no larger, it is never worse for any monotone clamp query.
    p_front = []
    c_front = []
    best_c = INF
    for p, c in points:
        if c < best_c:
            p_front.append(p)
            c_front.append(c)
            best_c = c

    def build_sparse_table(values):
        n = len(values)
        logs = [0] * (n + 1)
        for i in range(2, n + 1):
            logs[i] = logs[i >> 1] + 1
        table = [values]
        level = 1
        while (1 << level) <= n:
            half = 1 << (level - 1)
            prev = table[-1]
            length = n - (1 << level) + 1
            table.append([min(prev[i], prev[i + half]) for i in range(length)])
            level += 1
        return logs, table

    k = len(p_front)
    sum_front = [p_front[i] + c_front[i] for i in range(k)]
    logs, sparse = build_sparse_table(sum_front)
    neg_c_front = [-c for c in c_front]

    def min_sum(left, right):
        if left >= right:
            return INF
        level = logs[right - left]
        width = 1 << level
        row = sparse[level]
        return min(row[left], row[right - width])

    def count_c_ge(value):
        # c_front is strictly decreasing, so -c_front is increasing.
        return bisect_right(neg_c_front, -value)

    def has_common(left_a, right_a, left_b, right_b):
        return max(left_a, left_b) < min(right_a, right_b)

    def best_const(left_a, right_a, left_b, right_b, value):
        if has_common(left_a, right_a, left_b, right_b):
            return value
        return INF

    def best_by_p(left_a, right_a, left_b, right_b, extra):
        left = max(left_a, left_b)
        right = min(right_a, right_b)
        if left < right:
            return p_front[left] + extra
        return INF

    def best_by_c(left_a, right_a, left_b, right_b, extra):
        left = max(left_a, left_b)
        right = min(right_a, right_b)
        if left < right:
            return c_front[right - 1] + extra
        return INF

    def best_by_sum(left_a, right_a, left_b, right_b):
        left = max(left_a, left_b)
        right = min(right_a, right_b)
        if left < right:
            return min_sum(left, right)
        return INF

    def solve_user(tp, tc, d):
        # p zones on the frontier:
        #   [0, p_mid)      has political cost 0
        #   [p_mid, p_full) has political cost p
        #   [p_full, k)     has political cost tp + d
        p_mid = bisect_left(p_front, tp)
        p_full = bisect_left(p_front, tp + d)

        # c_front is decreasing, so high culture values are on the left:
        #   [0, c_full)     has cultural cost tc + d
        #   [c_full, c_mid) has cultural cost c
        #   [c_mid, k)      has cultural cost 0
        c_full = count_c_ge(tc + d)
        c_mid = count_c_ge(tc)

        if has_common(0, p_mid, c_mid, k):
            return 0

        return min(
            best_by_p(p_mid, p_full, c_mid, k, 0),
            best_const(p_full, k, c_mid, k, tp + d),
            best_by_c(0, p_mid, c_full, c_mid, 0),
            best_const(0, p_mid, 0, c_full, tc + d),
            best_by_sum(p_mid, p_full, c_full, c_mid),
            best_by_p(p_mid, p_full, 0, c_full, tc + d),
            best_by_c(p_full, k, c_full, c_mid, tp + d),
            best_const(p_full, k, 0, c_full, tp + tc + 2 * d),
        )

    m = next(ints)
    tp_values = [next(ints) for _ in range(m)]
    tc_values = [next(ints) for _ in range(m)]

    out = []
    for i in range(m):
        tp = tp_values[i]
        tc = tc_values[i]
        d = next(ints)
        out.append(str(solve_user(tp, tc, d)))

    return "\n".join(out)


if __name__ == "__main__":
    output = run()
    if output is not None:
        sys.stdout.write(str(output))
