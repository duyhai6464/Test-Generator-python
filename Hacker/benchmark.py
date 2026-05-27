import timeit, gc
import random

class LazySegTree:
    def __init__(self, n, initial_data=None):
        self.n = n
        self.tree = [LazySegTree.DEFAULT() for _ in range(self.n << 2)]
        self.lazy = [0] * (self.n << 2)
        if initial_data: self._build(1, 0, self.n - 1, initial_data)

    def _build(self, node, start, end, data):
        if start == end: self.tree[node] = data[start]; return
        mid = (start + end) >> 1
        ln, rn = node << 1, node << 1 | 1
        self._build(ln, start, mid, data)
        self._build(rn, mid + 1, end, data)
        self._pull(node)

    def _pull(self, node, start=None, end=None):
        self.tree[node] = self.__calc(self.tree[node << 1], self.tree[node << 1 | 1])

    def _update_range(self, node, start, end, l, r, val):
        if r < start or end < l: return
        if l <= start and end <= r:
            self.tree[node] += val
            self.lazy[node] += val
            return
        self._push(node, start, end)
        mid = (start + end) >> 1
        self._update_range(node << 1, start, mid, l, r, val)
        self._update_range(node << 1 | 1, mid + 1, end, l, r, val)
        self._pull(node)

    def _query_range(self, node, start, end, l, r):
        if r < start or end < l: return LazySegTree.DEFAULT()
        if l <= start and end <= r: return self.tree[node]
        self._push(node, start, end)
        mid = (start + end) >> 1
        return self.__calc(self._query_range(node << 1, start, mid, l, r),
                           self._query_range(node << 1 | 1, mid + 1, end, l, r))
    
    def update_range(self, l, r, val, index=1):
        self._update_range(1, 0, self.n - 1, l-index, r-index, val)
        
    def query_range(self, l, r, index=1):
        return self._query_range(1, 0, self.n - 1, l-index, r-index)

    def __calc(self, left, right):# define logic here
        return max(left, right)

    @staticmethod# Sum: 0, Min: float('inf'), Max: -float('inf'), GCD: 0, ...
    def DEFAULT():
        return -float('inf')
    
    def _push(self, node, start=None, end=None):
        val = self.lazy[node]
        if val == 0: return
        for child in (node << 1, node << 1 | 1):
            self.tree[child] += val
            self.lazy[child] += val
        self.lazy[node] = 0


LAZYSEG_DEFAULT = lambda: -float("inf")


def lazyseg_calc(left, right):
    return max(left, right)


def lazyseg_create(n, initial_data=None):
    tree = [LAZYSEG_DEFAULT() for _ in range(n << 2)]
    lazy = [0] * (n << 2)
    if initial_data:
        lazyseg_build(tree, 1, 0, n - 1, initial_data)
    return tree, lazy


def lazyseg_build(tree, node, start, end, data):
    if start == end:
        tree[node] = data[start]
        return
    mid = (start + end) >> 1
    lazyseg_build(tree, node << 1, start, mid, data)
    lazyseg_build(tree, node << 1 | 1, mid + 1, end, data)
    lazyseg_pull(tree, node)


def lazyseg_pull(tree, node):
    tree[node] = lazyseg_calc(tree[node << 1], tree[node << 1 | 1])


def lazyseg_push(tree, lazy, node):
    val = lazy[node]
    if val == 0:
        return
    for child in (node << 1, node << 1 | 1):
        tree[child] += val
        lazy[child] += val
    lazy[node] = 0


def lazyseg_update_range(tree, lazy, node, start, end, l, r, val):
    if r < start or end < l:
        return
    if l <= start and end <= r:
        tree[node] += val
        lazy[node] += val
        return
    lazyseg_push(tree, lazy, node)
    mid = (start + end) >> 1
    lazyseg_update_range(tree, lazy, node << 1, start, mid, l, r, val)
    lazyseg_update_range(tree, lazy, node << 1 | 1, mid + 1, end, l, r, val)
    lazyseg_pull(tree, node)


def lazyseg_query_range(tree, lazy, node, start, end, l, r):
    if r < start or end < l:
        return LAZYSEG_DEFAULT()
    if l <= start and end <= r:
        return tree[node]
    lazyseg_push(tree, lazy, node)
    mid = (start + end) >> 1
    return lazyseg_calc(
        lazyseg_query_range(tree, lazy, node << 1, start, mid, l, r),
        lazyseg_query_range(tree, lazy, node << 1 | 1, mid + 1, end, l, r),
    )


def lazyseg_update(tree, lazy, n, l, r, val, index=1):
    lazyseg_update_range(tree, lazy, 1, 0, n - 1, l - index, r - index, val)


def lazyseg_query(tree, lazy, n, l, r, index=1):
    return lazyseg_query_range(tree, lazy, 1, 0, n - 1, l - index, r - index)


SEG_BENCH_SEED = 20260516
SEG_BENCH_N = 1 << 18
SEG_BENCH_Q = 50000
NUMBER_N = 3


def make_lazysegtree_benchmark_case(n=SEG_BENCH_N, q=SEG_BENCH_Q, seed=SEG_BENCH_SEED):
    rng = random.Random(seed)
    data = [rng.randint(-10**6, 10**6) for _ in range(n)]
    updates = []
    queries = []
    mixed_ops = []

    for i in range(q):
        l = rng.randint(1, n)
        r = rng.randint(1, n)
        if l > r:
            l, r = r, l
        update = (l, r, rng.randint(-1000, 1000))
        updates.append(update)

        l = rng.randint(1, n)
        r = rng.randint(1, n)
        if l > r:
            l, r = r, l
        query = (l, r)
        queries.append(query)

        if i & 1:
            mixed_ops.append(("query", query))
        else:
            mixed_ops.append(("update", update))

    return data, updates, queries, mixed_ops


seg_data, seg_updates, seg_queries, seg_mixed_ops = make_lazysegtree_benchmark_case()
seg_n = len(seg_data)


def make_class_lazyseg_state(data=seg_data):
    return LazySegTree(len(data), data)


def make_func_lazyseg_state(data=seg_data):
    tree, lazy = lazyseg_create(len(data), data)
    return tree, lazy, len(data)


def bench_class_update(seg, updates=seg_updates):
    for l, r, val in updates:
        seg.update_range(l, r, val)
    return seg.tree[1]


def bench_func_update(state, updates=seg_updates):
    tree, lazy, n = state
    for l, r, val in updates:
        lazyseg_update(tree, lazy, n, l, r, val)
    return tree[1]


def bench_class_query(seg, queries=seg_queries):
    ans = 0
    for l, r in queries:
        ans += seg.query_range(l, r)
    return ans


def bench_func_query(state, queries=seg_queries):
    tree, lazy, n = state
    ans = 0
    for l, r in queries:
        ans += lazyseg_query(tree, lazy, n, l, r)
    return ans


def bench_class_mixed(seg, mixed_ops=seg_mixed_ops):
    ans = 0
    for op_type, op in mixed_ops:
        if op_type == "update":
            l, r, val = op
            seg.update_range(l, r, val)
        else:
            l, r = op
            ans += seg.query_range(l, r)
    return ans + seg.tree[1]


def bench_func_mixed(state, mixed_ops=seg_mixed_ops):
    tree, lazy, n = state
    ans = 0
    for op_type, op in mixed_ops:
        if op_type == "update":
            l, r, val = op
            lazyseg_update(tree, lazy, n, l, r, val)
        else:
            l, r = op
            ans += lazyseg_query(tree, lazy, n, l, r)
    return ans + tree[1]


def validate_lazysegtree(data=seg_data, updates=seg_updates, queries=seg_queries, mixed_ops=seg_mixed_ops):
    seg = LazySegTree(len(data), data)
    tree, lazy = lazyseg_create(len(data), data)
    n = len(data)

    for i, (l, r, val) in enumerate(updates):
        seg.update_range(l, r, val)
        lazyseg_update(tree, lazy, n, l, r, val)

        ql, qr = queries[i]
        class_ans = seg.query_range(ql, qr)
        func_ans = lazyseg_query(tree, lazy, n, ql, qr)
        if class_ans != func_ans:
            raise AssertionError((i, ql, qr, class_ans, func_ans))

    class_mixed = make_class_lazyseg_state(data)
    func_mixed = make_func_lazyseg_state(data)
    if bench_class_mixed(class_mixed, mixed_ops) != bench_func_mixed(func_mixed, mixed_ops):
        raise AssertionError("mixed benchmark mismatch")


def timeit_lazysegtree_update_only(number=1):
    return timeit_lazysegtree_phase(
        make_class_lazyseg_state,
        make_func_lazyseg_state,
        bench_class_update,
        bench_func_update,
        len(seg_updates),
        number,
    )


def timeit_lazysegtree_query_only(number=1):
    return timeit_lazysegtree_phase(
        make_class_lazyseg_state,
        make_func_lazyseg_state,
        bench_class_query,
        bench_func_query,
        len(seg_queries),
        number,
    )


def timeit_lazysegtree_mixed(number=1):
    return timeit_lazysegtree_phase(
        make_class_lazyseg_state,
        make_func_lazyseg_state,
        bench_class_mixed,
        bench_func_mixed,
        len(seg_mixed_ops),
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


def timeit_lazysegtree_phase(make_class_state, make_func_state, bench_class, bench_func, ops, number=1):
    class_result = _profile_prepare_and_run(make_class_state, bench_class, number)
    func_result = _profile_prepare_and_run(make_func_state, bench_func, number)
    return {
        "class": class_result,
        "func": func_result,
        "number": number,
        "ops": ops,
    }


def timeit_lazysegtree_all():
    validate_lazysegtree()
    return {
        "update_only": timeit_lazysegtree_update_only(NUMBER_N),
        "query_only": timeit_lazysegtree_query_only(NUMBER_N),
        "mixed": timeit_lazysegtree_mixed(NUMBER_N),
    }


def print_lazysegtree_benchmark():
    results = timeit_lazysegtree_all()
    print("\nLazySegTree benchmark")
    print(f"N: {seg_n}, q: {SEG_BENCH_Q}")
    for name, result in results.items():
        class_result = result["class"]
        func_result = result["func"]
        prepare_class = f"{class_result['prepare']:.6f}s"
        prepare_func  = f"{func_result['prepare']:.6f}s"

        run_class = f"{class_result['run']:.6f}s"
        run_func  = f"{func_result['run']:.6f}s"

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

        print(f"ops: {result['ops']}")
        print(f"number: {result['number']}")

        print("-" * 120)

def print_row(title, left, right):
    print(f"{title:<20} | {left:<45} | {right:<45}")

if __name__ == "__main__":
    print_lazysegtree_benchmark()
