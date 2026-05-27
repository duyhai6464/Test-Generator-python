import sys


MOD = 998244353

tokens = list(map(int, sys.stdin.buffer.read().split()))
ptr = 0

fact = [1]
inv_fact = [1]


def ensure_factorials(limit):
    current = len(fact) - 1
    if limit <= current:
        return

    fact.extend([1] * (limit - current))
    for i in range(current + 1, limit + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact.extend([1] * (limit - current))
    inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
    for i in range(limit, current + 1, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD


def comb(n, k):
    if k < 0 or k > n:
        return 0
    ensure_factorials(n)
    return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD


def range_sum(pref, left, right):
    return (pref[right] - pref[left - 1]) % MOD


def query_answer(l, r, total, fixed_pref, hole_pref, sum_p, sum_p2, sum_h, sum_h2, sum_ph):
    fixed_sum = fixed_pref[r] - fixed_pref[l - 1]
    holes = hole_pref[r] - hole_pref[l - 1]
    remaining = total - fixed_sum
    if remaining < 0:
        return 0

    length = r - l + 1
    p0 = fixed_pref[l - 1] % MOD
    h0 = hole_pref[l - 1] % MOD

    sp = range_sum(sum_p, l, r)
    sp2 = range_sum(sum_p2, l, r)
    sh = range_sum(sum_h, l, r)
    sh2 = range_sum(sum_h2, l, r)
    sph = range_sum(sum_ph, l, r)

    sum_a2 = (sp2 - 2 * p0 * sp + length * p0 * p0) % MOD
    if holes == 0:
        return sum_a2 if remaining == 0 else 0

    sum_at = (sph - p0 * sh - h0 * sp + length * p0 * h0) % MOD
    sum_t = (sh - length * h0) % MOD
    sum_t2 = (sh2 - 2 * h0 * sh + length * h0 * h0) % MOD

    rem = remaining % MOD
    h = holes % MOD
    inv_h = pow(h, MOD - 2, MOD)
    inv_h2 = inv_h * inv_h % MOD

    ways = comb(remaining + holes - 1, holes - 1)

    term = sum_a2
    term = (term + 2 * rem * inv_h % MOD * sum_at) % MOD
    term = (term + rem * rem % MOD * inv_h2 % MOD * sum_t2) % MOD

    variance_part = (h * sum_t - sum_t2) % MOD
    coeff = rem * ((remaining + holes) % MOD) % MOD
    coeff = coeff * inv_h2 % MOD * pow(holes + 1, MOD - 2, MOD) % MOD
    term = (term + coeff * variance_part) % MOD

    return ways * term % MOD


def solve_case():
    global ptr

    n = tokens[ptr]
    q = tokens[ptr + 1]
    ptr += 2

    fixed_pref = [0] * (n + 1)
    hole_pref = [0] * (n + 1)
    sum_p = [0] * (n + 1)
    sum_p2 = [0] * (n + 1)
    sum_h = [0] * (n + 1)
    sum_h2 = [0] * (n + 1)
    sum_ph = [0] * (n + 1)

    fixed = 0
    holes = 0
    for i in range(1, n + 1):
        value = tokens[ptr]
        ptr += 1
        if value == -1:
            holes += 1
        else:
            fixed += value

        fixed_pref[i] = fixed
        hole_pref[i] = holes

        p = fixed % MOD
        h = holes % MOD
        sum_p[i] = (sum_p[i - 1] + p) % MOD
        sum_p2[i] = (sum_p2[i - 1] + p * p) % MOD
        sum_h[i] = (sum_h[i - 1] + h) % MOD
        sum_h2[i] = (sum_h2[i - 1] + h * h) % MOD
        sum_ph[i] = (sum_ph[i - 1] + p * h) % MOD

    answers = []
    for _ in range(q):
        op = tokens[ptr]
        ptr += 1
        if op != 2:
            raise ValueError("Easy version only supports query type 2")

        l = tokens[ptr]
        r = tokens[ptr + 1]
        total = tokens[ptr + 2]
        ptr += 3

        answers.append(str(query_answer(
            l, r, total,
            fixed_pref, hole_pref,
            sum_p, sum_p2, sum_h, sum_h2, sum_ph,
        )))

    return answers


def main():
    global ptr
    if not tokens:
        return

    tests = tokens[ptr]
    ptr += 1
    out = []
    for _ in range(tests):
        out.extend(solve_case())

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
