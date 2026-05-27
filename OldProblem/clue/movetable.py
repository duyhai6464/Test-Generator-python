import sys


def solve_case(n, m, values):
    max_value = max(values) if values else 0
    if max_value < 1:
        return 0

    groups = {}
    for i in range(n):
        row_base = i * m
        for j in range(m):
            value = values[row_base + j]
            if value >= 1:
                encoded = (j << 3) | i
                current = groups.get(value)
                if current is None:
                    groups[value] = encoded
                elif type(current) is int:
                    groups[value] = [current, encoded]
                else:
                    current.append(encoded)

    sorted_values = sorted(groups)
    if not sorted_values:
        return 0

    pos = [[-1] * n for _ in range(n)]
    bit_count = 0
    for i in range(n):
        for j in range(i, n):
            pos[i][j] = bit_count
            bit_count += 1

    row_code = [[0] * (1 << n) for _ in range(n)]
    for i in range(n):
        for mask in range(1 << n):
            code = 0
            for j in range(i, n):
                if mask & (1 << j):
                    code |= 1 << pos[i][j]
            row_code[i][mask] = code

    code_count = 1 << bit_count
    rows_of = [None] * code_count
    for code in range(code_count):
        rows = [0] * n
        for i in range(n):
            mask = 0
            for j in range(i, n):
                if code & (1 << pos[i][j]):
                    mask |= 1 << j
            rows[i] = mask
        rows_of[code] = rows

    bit_to_row = [0] * (1 << n)
    for i in range(n):
        bit_to_row[1 << i] = i

    identity = 0
    for i in range(n):
        identity |= 1 << pos[i][i]

    compose_cache = [None] * code_count

    def compose(
        left,
        right,
        identity=identity,
        compose_cache=compose_cache,
        rows_of=rows_of,
        row_code=row_code,
        bit_to_row=bit_to_row,
        n=n,
    ):
        if left == 0 or right == 0:
            return 0
        if left == identity:
            return right
        if right == identity:
            return left

        cache_row = compose_cache[left]
        if cache_row is not None:
            cached = cache_row.get(right, -1)
            if cached != -1:
                return cached

        left_rows = rows_of[left]
        right_rows = rows_of[right]
        result = 0
        for i in range(n):
            can_enter = left_rows[i]
            out_mask = 0
            while can_enter:
                bit = can_enter & -can_enter
                out_mask |= right_rows[bit_to_row[bit]]
                can_enter ^= bit
            result |= row_code[i][out_mask]

        if cache_row is None:
            cache_row = {}
            compose_cache[left] = cache_row
        cache_row[right] = result
        return result

    transfer = [0] * (1 << n)
    for mask in range(1 << n):
        code = 0
        for i in range(n):
            out_mask = 0
            for j in range(i, n):
                if not (mask & (1 << j)):
                    break
                out_mask |= 1 << j
            code |= row_code[i][out_mask]
        transfer[mask] = code

    size = 1
    while size < m:
        size <<= 1

    tree = [identity] * (size * 2)
    for col in range(m):
        tree[size + col] = transfer[0]
    for node in range(size - 1, 0, -1):
        tree[node] = compose(tree[node << 1], tree[node << 1 | 1])

    column_masks = [0] * m
    marked = [False] * m

    def rebuild_columns(columns):
        if not columns:
            return

        columns.sort()
        nodes = []
        for col in columns:
            marked[col] = False
            leaf = size + col
            new_value = transfer[column_masks[col]]
            if tree[leaf] != new_value:
                tree[leaf] = new_value
                if leaf > 1:
                    nodes.append(leaf >> 1)

        while nodes:
            next_nodes = []
            previous = -1
            for node in nodes:
                if node == previous:
                    continue
                previous = node

                new_value = compose(tree[node << 1], tree[node << 1 | 1])
                if tree[node] != new_value:
                    tree[node] = new_value
                    if node > 1:
                        next_nodes.append(node >> 1)
            nodes = next_nodes

    def apply_cells(
        cells,
        add,
        column_masks=column_masks,
        tree=tree,
        transfer=transfer,
        compose=compose,
        size=size,
        marked=marked,
        rebuild_columns=rebuild_columns,
    ):
        if type(cells) is int:
            encoded = cells
            col = encoded >> 3
            bit = 1 << (encoded & 7)
            if add:
                column_masks[col] |= bit
            else:
                column_masks[col] &= ~bit

            leaf = size + col
            new_value = transfer[column_masks[col]]
            if tree[leaf] != new_value:
                tree[leaf] = new_value
                node = leaf >> 1
                while node:
                    new_value = compose(tree[node << 1], tree[node << 1 | 1])
                    if tree[node] == new_value:
                        break
                    tree[node] = new_value
                    node >>= 1
            return

        changed_columns = []
        if add:
            for encoded in cells:
                col = encoded >> 3
                bit = 1 << (encoded & 7)
                if not marked[col]:
                    marked[col] = True
                    changed_columns.append(col)
                column_masks[col] |= bit
        else:
            for encoded in cells:
                col = encoded >> 3
                bit = 1 << (encoded & 7)
                if not marked[col]:
                    marked[col] = True
                    changed_columns.append(col)
                column_masks[col] &= ~bit

        rebuild_columns(changed_columns)

    target_bit = 1 << pos[0][n - 1]

    answer = 0
    right = -1
    previous_value = 0

    for left_index, left_value in enumerate(sorted_values):
        if left_index > 0:
            apply_cells(groups[sorted_values[left_index - 1]], False)

        while not (tree[1] & target_bit) and right + 1 < len(sorted_values):
            right += 1
            apply_cells(groups[sorted_values[right]], True)

        if not (tree[1] & target_bit):
            break

        lower_count = left_value - previous_value
        upper_count = max_value - sorted_values[right] + 1
        answer += lower_count * upper_count
        previous_value = left_value

    return answer

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

n, m = read(), read()
print(solve_case(n, m, [read() for _ in range(n * m)]))