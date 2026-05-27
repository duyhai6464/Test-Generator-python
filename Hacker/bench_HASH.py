import random
import timeit


class PolyHash:
    NMOD = 2
    ACTIVE_MODS = []
    BASE = 0
    PW = []

    @classmethod
    def init_globals(cls, nmod=2):
        cls.NMOD = nmod
        pool = [1000000181, 1000003999, 1000009999, 1000000403, 1000002727, 1000002907, 1000007929]
        cls.ACTIVE_MODS = random.sample(pool, cls.NMOD)
        cls.BASE = random.randint(256, min(cls.ACTIVE_MODS) - 1)
        cls.PW = [[1] for _ in range(cls.NMOD)]

    @classmethod
    def ensure_pw(cls, max_len):
        if not cls.ACTIVE_MODS:
            cls.init_globals()

        curr_len = len(cls.PW[0])
        if curr_len <= max_len:
            target_len = max(curr_len * 2, max_len + 1)
            for i in range(cls.NMOD):
                m = cls.ACTIVE_MODS[i]
                base = cls.BASE
                pw = cls.PW[i]
                last = pw[-1]
                for _ in range(target_len - curr_len):
                    last = (last * base) % m
                    pw.append(last)

    def __init__(self, sequence):
        if not PolyHash.ACTIVE_MODS:
            PolyHash.init_globals()

        if isinstance(sequence, str):
            self.seq = [ord(c) for c in sequence]
        else:
            self.seq = list(sequence)

        self.n = len(self.seq)
        PolyHash.ensure_pw(self.n)

        base = PolyHash.BASE
        if PolyHash.NMOD >= 1:
            m0 = PolyHash.ACTIVE_MODS[0]
            self.pre0 = [0] * (self.n + 1)
            curr = 0
            for i in range(self.n):
                curr = (curr * base + self.seq[i]) % m0
                self.pre0[i + 1] = curr

        if PolyHash.NMOD >= 2:
            m1 = PolyHash.ACTIVE_MODS[1]
            self.pre1 = [0] * (self.n + 1)
            curr = 0
            for i in range(self.n):
                curr = (curr * base + self.seq[i]) % m1
                self.pre1[i + 1] = curr

    def is_equal(self, l1, r1, other: "PolyHash", l2, r2):
        len1 = r1 - l1 + 1
        len2 = r2 - l2 + 1
        if len1 != len2:
            return False

        m0 = PolyHash.ACTIVE_MODS[0]
        h0_self = (self.pre0[r1] - self.pre0[l1 - 1] * PolyHash.PW[0][len1]) % m0
        h0_other = (other.pre0[r2] - other.pre0[l2 - 1] * PolyHash.PW[0][len1]) % m0

        if h0_self != h0_other:
            return False

        if PolyHash.NMOD >= 2:
            m1 = PolyHash.ACTIVE_MODS[1]
            h1_self = (self.pre1[r1] - self.pre1[l1 - 1] * PolyHash.PW[1][len1]) % m1
            h1_other = (other.pre1[r2] - other.pre1[l2 - 1] * PolyHash.PW[1][len1]) % m1
            return h1_self == h1_other

        return True

    def get_hash_int(self, l, r):
        length = r - l + 1
        m0 = PolyHash.ACTIVE_MODS[0]
        h0 = (self.pre0[r] - self.pre0[l - 1] * PolyHash.PW[0][length]) % m0

        if PolyHash.NMOD == 2:
            m1 = PolyHash.ACTIVE_MODS[1]
            h1 = (self.pre1[r] - self.pre1[l - 1] * PolyHash.PW[1][length]) % m1
            return (h0 << 32) | h1

        return h0


HASH_BENCH_SEED = 20260516
NMOD = 2
HASH_BENCH_N = 2048
HASH_BENCH_Q = 20000
HASH_BENCH_REPEAT = 200
MOD_POOL = [1000000181, 1000003999, 1000009999, 1000000403, 1000002727, 1000002907, 1000007929]

rng = random.Random(HASH_BENCH_SEED)
MODD = rng.sample(MOD_POOL, NMOD)
BASE = rng.randint(256, min(MODD) - 1)


def build_pw(max_len, mods=MODD, base=BASE):
    pw = [[1] * (max_len + 1) for _ in range(len(mods))]
    for i, mod in enumerate(mods):
        row = pw[i]
        for j in range(1, max_len + 1):
            row[j] = row[j - 1] * base % mod
    return pw


def build_func_pre(sequence, mods=MODD, base=BASE):
    if isinstance(sequence, str):
        seq = [ord(c) for c in sequence]
    else:
        seq = list(sequence)

    n = len(seq)
    pre = [[0] * (n + 1) for _ in range(len(mods))]
    for i, mod in enumerate(mods):
        row = pre[i]
        curr = 0
        for j, value in enumerate(seq):
            curr = (curr * base + value) % mod
            row[j + 1] = curr
    return pre


def get_hashs(l, r, pre, pw, mods):
    length = r - l + 1
    h0 = (pre[0][r] - pre[0][l - 1] * pw[0][length]) % mods[0]
    if NMOD == 1:
        return h0

    h1 = (pre[1][r] - pre[1][l - 1] * pw[1][length]) % mods[1]
    return (h0 << 32) | h1


def cmp_hash(l1, r1, l2, r2, pre, pw, mods):
    length = r1 - l1 + 1
    if length != r2 - l2 + 1:
        return False

    h0_left = (pre[0][r1] - pre[0][l1 - 1] * pw[0][length]) % mods[0]
    h0_right = (pre[0][r2] - pre[0][l2 - 1] * pw[0][length]) % mods[0]
    if h0_left != h0_right:
        return False

    if NMOD >= 2:
        h1_left = (pre[1][r1] - pre[1][l1 - 1] * pw[1][length]) % mods[1]
        h1_right = (pre[1][r2] - pre[1][l2 - 1] * pw[1][length]) % mods[1]
        return h1_left == h1_right

    return True


def make_range_queries(n, q, rng):
    queries = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(1, n)
        if l > r:
            l, r = r, l
        queries.append((l, r))
    return queries


def make_cmp_queries(n, q, rng):
    queries = []
    for i in range(q):
        l1 = rng.randint(1, n)
        r1 = rng.randint(l1, n)

        if i & 1:
            l2 = rng.randint(1, n)
            r2 = rng.randint(l2, n)
        else:
            length = r1 - l1 + 1
            l2 = rng.randint(1, n - length + 1)
            r2 = l2 + length - 1

        queries.append((l1, r1, l2, r2))
    return queries


s = "".join(chr(rng.randint(ord("a"), ord("z"))) for _ in range(HASH_BENCH_N))
n = len(s)
pw = build_pw(n)
pre = build_func_pre(s)

# Class va function dung chung BASE/MOD/PW, tranh benchmark 2 bai toan khac nhau.
PolyHash.NMOD = NMOD
PolyHash.ACTIVE_MODS = MODD
PolyHash.BASE = BASE
PolyHash.PW = pw
class_hash = PolyHash(s)

get_queries = make_range_queries(n, HASH_BENCH_Q, rng)
cmp_queries = make_cmp_queries(n, HASH_BENCH_Q, rng)


def bench_func_get():
    ans = 0
    get = get_hashs
    local_pre = pre
    local_pw = pw
    mods = MODD
    for l, r in get_queries:
        ans ^= get(l, r, local_pre, local_pw, mods)
    return ans


def bench_class_get():
    ans = 0
    get = class_hash.get_hash_int
    for l, r in get_queries:
        ans ^= get(l, r)
    return ans


def bench_func_cmp():
    ans = 0
    cmp_ = cmp_hash
    local_pre = pre
    local_pw = pw
    mods = MODD
    for l1, r1, l2, r2 in cmp_queries:
        ans += cmp_(l1, r1, l2, r2, local_pre, local_pw, mods)
    return ans


def bench_class_cmp():
    ans = 0
    eq = class_hash.is_equal
    other = class_hash
    for l1, r1, l2, r2 in cmp_queries:
        ans += eq(l1, r1, other, l2, r2)
    return ans


def validate_benchmark():
    for l, r in get_queries[:1000]:
        if get_hashs(l, r, pre, pw, MODD) != class_hash.get_hash_int(l, r):
            raise AssertionError(("get", l, r))

    for l1, r1, l2, r2 in cmp_queries[:1000]:
        func_ans = cmp_hash(l1, r1, l2, r2, pre, pw, MODD)
        class_ans = class_hash.is_equal(l1, r1, class_hash, l2, r2)
        if func_ans != class_ans:
            raise AssertionError(("cmp", l1, r1, l2, r2, func_ans, class_ans))


def run_benchmark(number=HASH_BENCH_REPEAT):
    validate_benchmark()
    results = {
        "func_get": timeit.timeit(bench_func_get, number=number),
        "class_get": timeit.timeit(bench_class_get, number=number),
        "func_cmp": timeit.timeit(bench_func_cmp, number=number),
        "class_cmp": timeit.timeit(bench_class_cmp, number=number),
    }

    print(f"N: {n}, q: {HASH_BENCH_Q}, repeat: {number}")
    print(f"MODD: {MODD}")
    print(f"BASE: {BASE}")
    for name, elapsed in results.items():
        ns_per_op = elapsed * 1e9 / (HASH_BENCH_Q * number)
        print(f"{name}: {elapsed:.6f}s ({ns_per_op:.1f} ns/op)")


if __name__ == "__main__":
    run_benchmark()
