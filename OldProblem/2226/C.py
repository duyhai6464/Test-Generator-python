import sys
from collections import Counter, defaultdict

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
    count = Counter(a)
    activate_at = defaultdict(list)
    for value in count:
        limit = (value - 1) // 2
        if limit >= 0:
            activate_at[limit].append(value)

    def can_make(target_mex: int) -> bool:
        if target_mex == 0:
            return True

        pool = 0
        threshold = 2 * target_mex - 1
        for value, freq in count.items():
            if value >= threshold:
                pool += freq

        for need in range(target_mex - 1, -1, -1):
            if need < target_mex - 1:
                for value in activate_at.get(need, []):
                    remaining = count[value]
                    if value < target_mex and remaining > 0:
                        remaining -= 1
                    pool += remaining

            if count.get(need, 0) > 0:
                continue
            if pool == 0:
                return False
            pool -= 1

        return True

    left, right = 0, n
    while left < right:
        mid = (left + right + 1) // 2
        if can_make(mid):
            left = mid
        else:
            right = mid - 1

    return left

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))
