import sys
from array import array


MOD = 998244353

tokens = list(map(int, sys.stdin.buffer.read().split()))
ptr = 0

fact = array("i", [1])
inv_fact = array("i", [1])
inv_num = array("i", [0, 1])


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


def ensure_inverses(limit):
    current = len(inv_num) - 1
    if limit <= current:
        return

    inv_num.extend([0] * (limit - current))
    for i in range(current + 1, limit + 1):
        inv_num[i] = (MOD - MOD // i) * inv_num[MOD % i] % MOD


def comb(n, k):
    if k < 0 or k > n:
        return 0
    ensure_factorials(n)
    return fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD


class SegTree:
    __slots__ = (
        "n", "base", "length", "fixed", "fixed_mod", "holes",
        "sum_a", "sum_t", "sum_a2", "sum_t2", "sum_at",
    )

    def __init__(self, values):
        self.n = len(values)
        base = 1
        while base < self.n:
            base <<= 1
        self.base = base
        size = base << 1

        self.length = array("i", [0]) * size
        self.fixed = array("q", [0]) * size
        self.fixed_mod = array("q", [0]) * size
        self.holes = array("i", [0]) * size
        self.sum_a = array("q", [0]) * size
        self.sum_t = array("q", [0]) * size
        self.sum_a2 = array("q", [0]) * size
        self.sum_t2 = array("q", [0]) * size
        self.sum_at = array("q", [0]) * size

        for i, value in enumerate(values, base):
            self.length[i] = 1
            self._set_node(i, value)

        for node in range(base - 1, 0, -1):
            self._pull(node)

    def _set_node(self, node, value):
        if value == -1:
            self.fixed[node] = 0
            self.fixed_mod[node] = 0
            self.holes[node] = 1
            self.sum_a[node] = 0
            self.sum_t[node] = 1
            self.sum_a2[node] = 0
            self.sum_t2[node] = 1
            self.sum_at[node] = 0
            return

        value_mod = value % MOD
        self.fixed[node] = value
        self.fixed_mod[node] = value_mod
        self.holes[node] = 0
        self.sum_a[node] = value_mod
        self.sum_t[node] = 0
        self.sum_a2[node] = value_mod * value_mod % MOD
        self.sum_t2[node] = 0
        self.sum_at[node] = 0

    def _pull(self, node):
        left = node << 1
        right = left | 1

        len_l = self.length[left]
        len_r = self.length[right]
        fixed_l = self.fixed[left]
        fixed_mod_l = self.fixed_mod[left]
        holes_l = self.holes[left]

        sum_a_r = self.sum_a[right]
        sum_t_r = self.sum_t[right]

        self.length[node] = len_l + len_r
        self.fixed[node] = fixed_l + self.fixed[right]
        self.fixed_mod[node] = (fixed_mod_l + self.fixed_mod[right]) % MOD
        self.holes[node] = holes_l + self.holes[right]

        self.sum_a[node] = (
            self.sum_a[left] + sum_a_r + len_r * fixed_mod_l
        ) % MOD
        self.sum_t[node] = (
            self.sum_t[left] + sum_t_r + len_r * holes_l
        ) % MOD
        self.sum_a2[node] = (
            self.sum_a2[left] + self.sum_a2[right]
            + 2 * fixed_mod_l * sum_a_r
            + len_r * fixed_mod_l * fixed_mod_l
        ) % MOD
        self.sum_t2[node] = (
            self.sum_t2[left] + self.sum_t2[right]
            + 2 * holes_l * sum_t_r
            + len_r * holes_l * holes_l
        ) % MOD
        self.sum_at[node] = (
            self.sum_at[left] + self.sum_at[right]
            + fixed_mod_l * sum_t_r
            + holes_l * sum_a_r
            + len_r * fixed_mod_l * holes_l
        ) % MOD

    def update(self, pos, value):
        node = self.base + pos - 1
        self._set_node(node, value)
        node >>= 1
        while node:
            self._pull(node)
            node >>= 1

    @staticmethod
    def _merge(left_state, right_state):
        len_l, fixed_l, fixed_mod_l, holes_l, a_l, t_l, a2_l, t2_l, at_l = left_state
        len_r, fixed_r, fixed_mod_r, holes_r, a_r, t_r, a2_r, t2_r, at_r = right_state

        return (
            len_l + len_r,
            fixed_l + fixed_r,
            (fixed_mod_l + fixed_mod_r) % MOD,
            holes_l + holes_r,
            (a_l + a_r + len_r * fixed_mod_l) % MOD,
            (t_l + t_r + len_r * holes_l) % MOD,
            (a2_l + a2_r + 2 * fixed_mod_l * a_r + len_r * fixed_mod_l * fixed_mod_l) % MOD,
            (t2_l + t2_r + 2 * holes_l * t_r + len_r * holes_l * holes_l) % MOD,
            (at_l + at_r + fixed_mod_l * t_r + holes_l * a_r + len_r * fixed_mod_l * holes_l) % MOD,
        )

    def _node_state(self, node):
        return (
            self.length[node],
            self.fixed[node],
            self.fixed_mod[node],
            self.holes[node],
            self.sum_a[node],
            self.sum_t[node],
            self.sum_a2[node],
            self.sum_t2[node],
            self.sum_at[node],
        )

    def query(self, left, right):
        left += self.base - 1
        right += self.base - 1

        left_state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        right_state = (0, 0, 0, 0, 0, 0, 0, 0, 0)

        while left <= right:
            if left & 1:
                left_state = self._merge(left_state, self._node_state(left))
                left += 1
            if not (right & 1):
                right_state = self._merge(self._node_state(right), right_state)
                right -= 1
            left >>= 1
            right >>= 1

        return self._merge(left_state, right_state)


def answer_query(state, total):
    _, fixed_sum, _, holes, _, sum_t, sum_a2, sum_t2, sum_at = state
    remaining = total - fixed_sum
    if remaining < 0:
        return 0

    if holes == 0:
        return sum_a2 if remaining == 0 else 0

    ensure_inverses(holes + 1)
    ways = comb(remaining + holes - 1, holes - 1)

    rem = remaining % MOD
    inv_h = inv_num[holes]
    inv_h2 = inv_h * inv_h % MOD

    term = sum_a2
    term = (term + 2 * rem * inv_h % MOD * sum_at) % MOD
    term = (term + rem * rem % MOD * inv_h2 % MOD * sum_t2) % MOD

    variance_part = (holes * sum_t - sum_t2) % MOD
    coeff = rem * ((remaining + holes) % MOD) % MOD
    coeff = coeff * inv_h2 % MOD * inv_num[holes + 1] % MOD
    term = (term + coeff * variance_part) % MOD

    return ways * term % MOD


def solve_case():
    global ptr

    n = tokens[ptr]
    q = tokens[ptr + 1]
    ptr += 2

    values = tokens[ptr:ptr + n]
    ptr += n

    tree = SegTree(values)
    out = []

    for _ in range(q):
        op = tokens[ptr]
        ptr += 1

        if op == 1:
            pos = tokens[ptr]
            value = tokens[ptr + 1]
            ptr += 2
            tree.update(pos, value)
        else:
            left = tokens[ptr]
            right = tokens[ptr + 1]
            total = tokens[ptr + 2]
            ptr += 3
            out.append(str(answer_query(tree.query(left, right), total)))

    return out


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
