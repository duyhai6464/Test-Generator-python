import sys
from array import array
from collections import deque


def read_ints():
    data = sys.stdin.buffer.read()
    num = 0
    in_num = False
    for byte in data:
        if 48 <= byte <= 57:
            num = num * 10 + byte - 48
            in_num = True
        elif in_num:
            yield num
            num = 0
            in_num = False
    if in_num:
        yield num


def solve():
    ints = read_ints()
    try:
        q = next(ints)
    except StopIteration:
        return ""

    n_max = q + 1
    max_level = (n_max + 1).bit_length() + 2

    parent = [0] * (n_max + 1)
    children = [[] for _ in range(n_max + 1)]

    to_parent = [0] * (n_max + 1)
    from_parent = [0] * (n_max + 1)

    cnt = [None] + [array("I", [0]) * (n_max + 1) for _ in range(max_level)]
    queue = deque()
    ans = 1

    def get_value(src, dst):
        if parent[src] == dst:
            return to_parent[src]
        return from_parent[dst]

    def set_value(src, dst, value):
        if parent[src] == dst:
            to_parent[src] = value
        else:
            from_parent[dst] = value

    def raise_directed(src, dst, value):
        old = get_value(src, dst)
        if value <= old:
            return
        set_value(src, dst, value)
        for level in range(old + 1, value + 1):
            queue.append((dst, level))

    def process_queue():
        nonlocal ans
        while queue:
            v, level = queue.popleft()
            cnt_level = cnt[level]
            cnt_level[v] += 1
            current = cnt_level[v]

            if current >= 2 and ans < level + 1:
                ans = level + 1

            if level + 1 >= max_level or (current != 2 and current != 3):
                continue

            p = parent[v]
            if p and current - (1 if get_value(p, v) >= level else 0) >= 2:
                raise_directed(v, p, level + 1)

            for child in children[v]:
                if current - (1 if to_parent[child] >= level else 0) >= 2:
                    raise_directed(v, child, level + 1)

    def value_excluding(src, blocked_neighbor):
        blocked_value = get_value(blocked_neighbor, src)
        value = 1
        for level in range(1, max_level - 1):
            if cnt[level][src] - (1 if blocked_value >= level else 0) >= 2:
                value = level + 1
            else:
                break
        return value

    out = []
    for new_node in range(2, q + 2):
        p = next(ints)
        parent[new_node] = p
        children[p].append(new_node)

        raise_directed(new_node, p, 1)
        raise_directed(p, new_node, 1)
        process_queue()

        raise_directed(p, new_node, value_excluding(p, new_node))
        process_queue()

        out.append(str(ans))

    return " ".join(out)


if __name__ == "__main__":
    sys.stdout.write(solve())
