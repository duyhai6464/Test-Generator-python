import sys

MOD = 2718281828
PISANO = 341361636
buffer = sys.stdin.buffer.read().split()
ptr = 0


def read_int():
    global ptr
    ptr += 1
    return int(buffer[ptr - 1])


def fib_pair(n: int):
    a, b = 0, 1
    for i in range(n.bit_length() - 1, -1, -1):
        d = (a * (((b << 1) - a) % MOD)) % MOD
        e = (a * a + b * b) % MOD
        if (n >> i) & 1:
            a, b = e, (d + e) % MOD
        else:
            a, b = d, e
    return a, b


def solve_one():
    n = read_int()
    if n < 2:
        return "1"
    return str(fib_pair((n << 1) % PISANO)[0])


out = []
for _ in range(read_int()):
    out.append(solve_one())

sys.stdout.write("\n".join(out))
