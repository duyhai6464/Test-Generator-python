import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])


def fi(x):
    s, p, d = 0, 1, 0
    while x:
        a = x % 10
        x //= 10
        s += a
        p *= a
        d += 1
    return s, p, d

def vir(x):
    if x <= 0: return False
    s, p, d = fi(x)
    return p % s == 0 and s % d == 0

def run():
    n = read()
    if n <= 0: return 0
    digits = list(map(int, str(n)))
    ans = 0
    for length in range(1, len(digits) + 1):
        limit = digits if length == len(digits) else [9] * length
        for target_sum in range(length, 9 * length + 1, length):
            dp = {(0, 1 % target_sum, 1): 1}
            for pos in range(length):
                ndp = {}
                for (cur_sum, prod_mod, tight), cnt in dp.items():
                    lo = 1 if pos == 0 else 0
                    hi = limit[pos] if tight else 9
                    for dig in range(lo, hi + 1):
                        nxt_sum = cur_sum + dig
                        if nxt_sum > target_sum:
                            continue

                        left = length - pos - 1
                        if nxt_sum + 9 * left < target_sum:
                            continue

                        key = (
                            nxt_sum,
                            (prod_mod * dig) % target_sum,
                            1 if tight and dig == hi else 0,
                        )
                        ndp[key] = ndp.get(key, 0) + cnt

                dp = ndp

            for (cur_sum, prod_mod, _), cnt in dp.items():
                if cur_sum == target_sum and prod_mod == 0:
                    ans += cnt

    return ans

# sample
# res = []
# for i in range(n + 1):
#     if vir(i): res.append(i)
# debug(res)

print(run())
