import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n, k, x = read(), read(), read()
    a = [read() for _ in range(n)]
    N_indices = [i for i, v in enumerate(a) if v > x]
    n_F = n - len(N_indices)  # Số lượng phần tử F ban đầu
    if n_F == 0:
        return 0
    if not N_indices:
        total_sum = sum(a)
        if total_sum <= x:
            return k
        B = 0
        curr_sum = 0
        for v in a:
            if curr_sum + v <= x:
                curr_sum += v
            else:
                B += 1
                curr_sum = v
        if curr_sum > 0:
            B += 1
        max_safe_merges = n - B
        k_rem = n - k
        if k_rem <= max_safe_merges:
            return (n - k_rem)
        loss = k_rem + 1
        return max(0, n - loss)
    num_N_blocks = 1
    internal_islands = []
    for i in range(1, len(N_indices)):
        diff = N_indices[i] - N_indices[i - 1]
        if diff > 1:
            num_N_blocks += 1
            internal_islands.append(diff - 1)
    N_comp = n_F + num_N_blocks
    k_rem = N_comp - k  # Số lượng đoạn cần phải giảm thêm để đạt k
    if k_rem <= 0:
        return n_F
    internal_islands.sort()
    fragile_left = n_F
    # debug(f"N_comp: {N_comp}, k_rem: {k_rem}, internal: {internal_islands}")
    for m in internal_islands:
        if k_rem >= m + 1:
            k_rem -= m + 1
            fragile_left -= m
        else:
            fragile_left -= k_rem
            k_rem = 0
            break
    if k_rem > 0:
        fragile_left -= k_rem
    return max(0, fragile_left)

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))