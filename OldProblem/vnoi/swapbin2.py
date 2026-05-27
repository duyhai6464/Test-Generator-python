import sys
from collections import defaultdict
from heapq import heappop, heappush

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n, k = read(), read()# k = 2
    s = read(str)
    pre = [0] * (n + 1)
    counts = defaultdict(int)
    counts[0] = 1
    arr = [1 if cc == '1' else -1 for cc in s]
    for i in range(n):
        pre[i + 1] = pre[i] + arr[i]
        counts[pre[i + 1]] += 1
    
    initial_beauty = 0
    for val in counts:
        freq = counts[val]
        initial_beauty += freq * (freq - 1) // 2

    def choose2(x):
        return x * (x - 1) // 2

    def gain_change(old_values, new_values):
        delta = defaultdict(int)
        for x in old_values:
            delta[x] -= 1
        for x in new_values:
            delta[x] += 1

        gain = 0
        for x, d in delta.items():
            if d:
                gain += choose2(counts[x] + d) - choose2(counts[x])
        return gain

    max_gain = 0
    moves = [None] * (n + 1)

    for i in range(n - 1):
        if arr[i] != arr[i+1]:
            pos = i + 1
            old_value = pre[pos]
            new_value = old_value + arr[i + 1] - arr[i]
            current_gain = gain_change([old_value], [new_value])
            moves[pos] = (old_value, new_value, current_gain)

            if current_gain > max_gain:
                max_gain = current_gain

    # Two swaps on adjacent borders: a block 001/011/100/110 can move
    # one bit across the two equal opposite bits. This changes two
    # consecutive prefix sums by the same +/-2.
    for i in range(1, n - 1):
        if arr[i - 1] != arr[i + 1]:
            delta = arr[i + 1] - arr[i - 1]
            current_gain = gain_change(
                [pre[i], pre[i + 1]],
                [pre[i] + delta, pre[i + 1] + delta],
            )
            if current_gain > max_gain:
                max_gain = current_gain

    def interaction(left, right):
        a, b, _ = left
        c, d, _ = right
        return (a == c) - (a == d) - (b == c) + (b == d)

    best_by_type = {}
    heap = []

    def add_move(move):
        old_value, new_value, gain = move
        typ = (old_value, new_value)
        if gain > best_by_type.get(typ, -10**30):
            best_by_type[typ] = gain
            heappush(heap, (-gain, typ))

    def best_independent_gain(current):
        c, d, _ = current
        related = set()
        for x in (c, d):
            related.add((x, x - 2))
            related.add((x, x + 2))
            related.add((x - 2, x))
            related.add((x + 2, x))

        best = -10**30
        for typ in related:
            gain = best_by_type.get(typ)
            if gain is None:
                continue
            old_value, new_value = typ
            best = max(
                best,
                gain + interaction((old_value, new_value, gain), current),
            )

        popped = []
        while heap:
            neg_gain, typ = heappop(heap)
            gain = -neg_gain
            if best_by_type.get(typ) != gain:
                continue
            if typ in related:
                popped.append((neg_gain, typ))
                continue
            best = max(best, gain)
            popped.append((neg_gain, typ))
            break

        for item in popped:
            heappush(heap, item)

        return best

    # Two swaps on non-adjacent borders do not interact in the string.
    # Scan left to right and only keep moves with distance at least 2.
    for pos in range(1, n):
        if pos - 2 >= 1 and moves[pos - 2] is not None:
            add_move(moves[pos - 2])

        if moves[pos] is not None:
            best_previous = best_independent_gain(moves[pos])
            if best_previous > -10**20:
                max_gain = max(max_gain, moves[pos][2] + best_previous)
    
    # debug(pre, initial_beauty)
    # debug(counts)
    return initial_beauty + max_gain
    
t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))
