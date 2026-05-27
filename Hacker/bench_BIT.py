import random
import timeit, gc


class BIT:
    def __init__(self, size):
        self.size = size
        self.bit = [0] * (size + 1)

    def add(self, idx, val):
        while idx <= self.size:
            self.bit[idx] += val
            idx += idx & -idx

    def prefix(self, idx):
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx ^= idx & -idx
        return s
    
    def query(self, l, r):
        if l > r: return 0
        return self.prefix(r) - self.prefix(l - 1)

def bit_create(size):
    return [0] * (size + 1)


def bit_add(bit, size, idx, val):
    while idx <= size:
        bit[idx] += val
        idx += idx & -idx


def bit_prefix(bit, idx):
    s = 0
    while idx > 0:
        s += bit[idx]
        idx ^= idx & -idx
    return s

def bit_query(bit, l, r):
    return bit_prefix(bit, r) - bit_prefix(bit, l - 1)

BIT_BENCH_SEED = 20260516
BIT_BENCH_N = 1 << 19
BIT_BENCH_Q = 500000
NUMBER_N = 1


def make_bit_benchmark_case(n=BIT_BENCH_N, q=BIT_BENCH_Q, seed=BIT_BENCH_SEED):
    rng = random.Random(seed)
    data = [rng.randint(-1000, 1000) for _ in range(n)]
    updates = []
    queries = []
    range_queries = []
    mixed_ops = []

    for i in range(q):
        update = (rng.randint(1, n), rng.randint(-1000, 1000))
        query = rng.randint(1, n)
        l = rng.randint(1, n)
        r = rng.randint(1, n)
        if l > r:
            l, r = r, l

        updates.append(update)
        queries.append(query)
        range_queries.append((l, r))
        if i & 1:
            mixed_ops.append(("query", query))
        else:
            mixed_ops.append(("update", update))

    return data, updates, queries, range_queries, mixed_ops


bit_data, bit_updates, bit_queries, bit_range_queries, bit_mixed_ops = make_bit_benchmark_case()
bit_n = len(bit_data)


def make_class_bit_state(data=bit_data):
    bit = BIT(len(data))
    for idx, value in enumerate(data, 1):
        bit.add(idx, value)
    return bit


def make_func_bit_state(data=bit_data):
    size = len(data)
    bit = bit_create(size)
    for idx, value in enumerate(data, 1):
        bit_add(bit, size, idx, value)
    return bit, size


def bench_class_update(bit, updates=bit_updates):
    for idx, value in updates:
        bit.add(idx, value)
    return bit.bit[1]


def bench_func_update(state, updates=bit_updates):
    bit, size = state
    for idx, value in updates:
        bit_add(bit, size, idx, value)
    return bit[1]


def bench_class_prefix(bit, queries=bit_queries):
    ans = 0
    for idx in queries:
        ans += bit.prefix(idx)
    return ans


def bench_func_prefix(state, queries=bit_queries):
    bit, _ = state
    ans = 0
    for idx in queries:
        ans += bit_prefix(bit, idx)
    return ans


def bench_class_query(bit, queries=bit_range_queries):
    ans = 0
    for l, r in queries:
        ans += bit.query(l, r)
    return ans


def bench_func_query(state, queries=bit_range_queries):
    bit, _ = state
    ans = 0
    for l, r in queries:
        ans += bit_query(bit, l, r)
    return ans


def bench_class_mixed(bit, mixed_ops=bit_mixed_ops):
    ans = 0
    for op_type, op in mixed_ops:
        if op_type == "update":
            idx, value = op
            bit.add(idx, value)
        else:
            ans += bit.prefix(op)
    return ans + bit.bit[1]


def bench_func_mixed(state, mixed_ops=bit_mixed_ops):
    bit, size = state
    ans = 0
    for op_type, op in mixed_ops:
        if op_type == "update":
            idx, value = op
            bit_add(bit, size, idx, value)
        else:
            ans += bit_prefix(bit, op)
    return ans + bit[1]


def validate_bit(data=bit_data, updates=bit_updates, queries=bit_queries, range_queries=bit_range_queries, mixed_ops=bit_mixed_ops):
    class_bit = make_class_bit_state(data)
    func_state = make_func_bit_state(data)
    func_bit, func_size = func_state

    for i, (idx, value) in enumerate(updates[:1000]):
        class_bit.add(idx, value)
        bit_add(func_bit, func_size, idx, value)

        query_idx = queries[i]
        class_ans = class_bit.prefix(query_idx)
        func_ans = bit_prefix(func_bit, query_idx)
        if class_ans != func_ans:
            raise AssertionError((i, query_idx, class_ans, func_ans))

        query_l, query_r = range_queries[i]
        class_ans = class_bit.query(query_l, query_r)
        func_ans = bit_query(func_bit, query_l, query_r)
        if class_ans != func_ans:
            raise AssertionError((i, query_l, query_r, class_ans, func_ans))

    class_mixed = make_class_bit_state(data)
    func_mixed = make_func_bit_state(data)
    if bench_class_mixed(class_mixed, mixed_ops[:1000]) != bench_func_mixed(func_mixed, mixed_ops[:1000]):
        raise AssertionError("mixed benchmark mismatch")


def timeit_bit_update_only(number=NUMBER_N):
    return timeit_bit_phase(
        make_class_bit_state,
        make_func_bit_state,
        bench_class_update,
        bench_func_update,
        len(bit_updates),
        number,
    )


def timeit_bit_prefix_only(number=NUMBER_N):
    return timeit_bit_phase(
        make_class_bit_state,
        make_func_bit_state,
        bench_class_prefix,
        bench_func_prefix,
        len(bit_queries),
        number,
    )


def timeit_bit_query_only(number=NUMBER_N):
    return timeit_bit_phase(
        make_class_bit_state,
        make_func_bit_state,
        bench_class_query,
        bench_func_query,
        len(bit_range_queries),
        number,
    )


def timeit_bit_mixed(number=NUMBER_N):
    return timeit_bit_phase(
        make_class_bit_state,
        make_func_bit_state,
        bench_class_mixed,
        bench_func_mixed,
        len(bit_mixed_ops),
        number,
    )


def _profile_prepare_and_run(make_state, bench_run, number):
    prepare_time = 0.0
    run_time = 0.0
    last_result = None

    gc_enabled = gc.isenabled()
    try:
        gc.disable()
        for _ in range(number):
            start = timeit.default_timer()
            state = make_state()
            prepare_time += timeit.default_timer() - start

            start = timeit.default_timer()
            last_result = bench_run(state)
            run_time += timeit.default_timer() - start
    finally:
        if gc_enabled:
            gc.enable()

    total_time = prepare_time + run_time
    prepare_ratio = prepare_time / total_time if total_time else 0.0
    return {
        "prepare": prepare_time,
        "run": run_time,
        "total": total_time,
        "prepare_ratio": prepare_ratio,
        "last_result": last_result,
    }


def timeit_bit_phase(make_class_state, make_func_state, bench_class, bench_func, ops, number=NUMBER_N):
    class_result = _profile_prepare_and_run(make_class_state, bench_class, number)
    func_result = _profile_prepare_and_run(make_func_state, bench_func, number)
    return {
        "class": class_result,
        "func": func_result,
        "ops": ops,
        "number": number,
    }


def timeit_bit_all():
    validate_bit()
    return {
        "update_only": timeit_bit_update_only(),
        "prefix_only": timeit_bit_prefix_only(),
        "query_only": timeit_bit_query_only(),
        "mixed": timeit_bit_mixed(),
    }


def print_bit_benchmark():
    results = timeit_bit_all()
    print("BIT benchmark")
    print(f"N: {bit_n}, q: {BIT_BENCH_Q}")
    for name, result in results.items():
        class_result = result["class"]
        func_result = result["func"]
        class_ns = class_result["run"] * 1e9 / (result["ops"] * result["number"])
        func_ns = func_result["run"] * 1e9 / (result["ops"] * result["number"])
        
        prepare_class = f"{class_result['prepare']:.6f}s"
        prepare_func  = f"{func_result['prepare']:.6f}s"

        run_class = f"{class_result['run']:.6f}s ({class_ns:.1f} ns/op)"
        run_func  = f"{func_result['run']:.6f}s ({func_ns:.1f} ns/op)"

        total_class = f"{class_result['total']:.6f}s"
        total_func  = f"{func_result['total']:.6f}s"

        ratio_class = f"{class_result['prepare_ratio']:.2%}"
        ratio_func  = f"{func_result['prepare_ratio']:.2%}"

        print_row(name, 'class', 'func')
        print("-" * 120)
        print_row("prepare", prepare_class, prepare_func)
        print_row("run", run_class, run_func)
        print_row("total", total_class, total_func)
        print_row("prepare ratio", ratio_class, ratio_func)
        print(f"ops: {result['ops']} number: {result['number']}")
        print("-" * 120)

def print_row(title, left, right):
    print(f"{title:<20} | {left:<45} | {right:<45}")

if __name__ == "__main__":
    print_bit_benchmark()
