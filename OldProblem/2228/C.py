import sys
from bisect import bisect_left, bisect_right

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def to_int(digits):
    return int("".join(map(str, digits)))

def smallest_number(length, digits, min_nonzero):
    if length == 1:
        return digits[0]
    if min_nonzero is None:
        return None
    return to_int([min_nonzero] + [digits[0]] * (length - 1))

def largest_number(length, digits):
    return to_int([digits[-1]] * length)

def largest_leq(s, digits, nonzero_digits):
    length = len(s)
    res = []
    for i, ch in enumerate(s):
        target = int(ch)
        allowed = digits if i > 0 or length == 1 else nonzero_digits
        j = bisect_right(allowed, target) - 1
        if j >= 0:
            x = allowed[j]
            res.append(x)
            if x < target:
                return to_int(res + [digits[-1]] * (length - i - 1))
            continue

        for k in range(i - 1, -1, -1):
            prev_allowed = digits if k > 0 or length == 1 else nonzero_digits
            j = bisect_left(prev_allowed, res[k]) - 1
            if j >= 0:
                return to_int(res[:k] + [prev_allowed[j]] + [digits[-1]] * (length - k - 1))
        return None
    return to_int(res)

def smallest_geq(s, digits, nonzero_digits):
    length = len(s)
    res = []
    for i, ch in enumerate(s):
        target = int(ch)
        allowed = digits if i > 0 or length == 1 else nonzero_digits
        j = bisect_left(allowed, target)
        if j < len(allowed):
            x = allowed[j]
            res.append(x)
            if x > target:
                return to_int(res + [digits[0]] * (length - i - 1))
            continue

        for k in range(i - 1, -1, -1):
            prev_allowed = digits if k > 0 or length == 1 else nonzero_digits
            j = bisect_right(prev_allowed, res[k])
            if j < len(prev_allowed):
                return to_int(res[:k] + [prev_allowed[j]] + [digits[0]] * (length - k - 1))
        return None
    return to_int(res)

def run():
    a, n = read(), read()
    d = sorted(set(read() for _ in range(n)))
    nonzero_digits = [x for x in d if x > 0]
    min_nonzero = nonzero_digits[0] if nonzero_digits else None
    a_str = str(a)
    L = len(a_str)
    candidates = []

    if L > 1:
        candidates.append(largest_number(L - 1, d))

    bigger_len = smallest_number(L + 1, d, min_nonzero)
    if bigger_len is not None:
        candidates.append(bigger_len)

    for x in (largest_leq(a_str, d, nonzero_digits), smallest_geq(a_str, d, nonzero_digits)):
        if x is not None:
            candidates.append(x)

    return min(abs(a - c) for c in candidates)
    
    

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))
