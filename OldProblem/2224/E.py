import math
import sys

INF = 10**18 + 100_000


def solve_case(next_int) -> str:
    n = next_int()
    q = next_int()

    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    for v in range(2, n + 1):
        p = next_int()
        parent[v] = p
        children[p].append(v)

    dep = [0] * (n + 1)
    for v in range(2, n + 1):
        p = parent[v]
        dep[v] = dep[p] + next_int()

    degree = [0] * (n + 1)
    for u in range(1, n + 1):
        degree[u] = len(children[u])

    lcm_path = [0] * (n + 1)
    fixed = [0] * (n + 1)
    lcm_path[1] = 1

    for u in range(2, n + 1):
        prev = lcm_path[parent[u]]
        deg = degree[u]
        if deg == 0:
            continue
        if prev == INF or prev % deg == 0:
            lcm_path[u] = prev
            fixed[u] = 1
        else:
            g = math.gcd(prev, deg)
            mul = prev // g
            if mul > INF // deg:
                lcm_path[u] = INF
            else:
                lcm_path[u] = mul * deg

    cached_next = [0] * (n + 1)
    out = []
    dep_local = dep
    degree_local = degree
    children_local = children
    fixed_local = fixed
    cached_local = cached_next

    for _ in range(q):
        d = next_int()
        u = 1
        trace = []

        while True:
            deg = degree_local[u]
            if deg == 0:
                ans = u
                break

            cached = cached_local[u]
            if fixed_local[u] and cached:
                u = cached
                continue

            if fixed_local[u]:
                trace.append(u)
            elif trace:
                for node in trace:
                    cached_local[node] = u
                trace.clear()

            u = children_local[u][(d + dep_local[u]) % deg]

        for node in trace:
            cached_local[node] = ans
        out.append(str(ans))

    return " ".join(out)


def main() -> None:
    data = sys.stdin.buffer.read()
    size = len(data)
    ptr = 0

    def next_int() -> int:
        nonlocal ptr
        while ptr < size and data[ptr] <= 32:
            ptr += 1
        num = 0
        while ptr < size and data[ptr] > 32:
            num = num * 10 + data[ptr] - 48
            ptr += 1
        return num

    t = next_int()
    out = []
    for _ in range(t):
        out.append(solve_case(next_int))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
