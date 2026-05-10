import sys


OFF = (0, 0, 1, 3, 7, 15)
NEG_INF = -(10**30)


def solve_case(n: int, a: list[int]) -> int:
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i]

    future: dict[int, tuple[list[int], list[int]]] = {}

    def block_value(fr: int, bk: int, mask: int) -> int:
        # gap >= 6 and the front token moves now:
        # front side takes everything after fr, back side takes all free cells in (bk, fr).
        res = pref[n] - pref[fr]
        bit = 0
        for pos in range(bk + 1, fr):
            if ((mask >> bit) & 1) == 0:
                res -= a[pos]
            bit += 1
        return res

    def get_future(dir_: int, fr: int, bk: int, mask: int) -> int:
        arr0, arr1 = future[fr]
        idx = OFF[fr - bk] + mask
        return arr0[idx] if dir_ == 0 else arr1[idx]

    def large_back_turn(fr: int, bk: int, mask: int) -> int:
        # Only called for dir = 1 and fr - bk >= 6.
        best = None
        hi = min(n, bk + 4)
        for nxt in range(bk + 1, hi + 1):
            if nxt == fr:
                continue
            bit = nxt - bk - 1
            if (mask >> bit) & 1:
                continue
            if nxt < fr:
                next_mask = mask >> (nxt - bk)
                gap = fr - nxt
                if gap >= 6:
                    val = a[nxt] - block_value(fr, nxt, next_mask)
                else:
                    val = a[nxt] - get_future(0, fr, nxt, next_mask)
            else:
                val = a[nxt] - get_future(1, nxt, fr, 0)
            if best is None or val > best:
                best = val
        if best is None:
            return -block_value(fr, bk, mask)
        return best

    for fr in range(n, 0, -1):
        cur0 = [0] * 31
        cur1 = [0] * 31
        max_gap = min(5, fr - 1)

        if fr < n:
            hi_front = min(n, fr + 4)
            for gap in range(1, max_gap + 1):
                bk = fr - gap
                cnt = 1 << (gap - 1)
                off = OFF[gap]
                add_bit = 1 << (gap - 1)
                for mask in range(cnt):
                    best = NEG_INF
                    next_mask = mask | add_bit
                    for nxt in range(fr + 1, hi_front + 1):
                        new_gap = nxt - bk
                        if new_gap <= 5:
                            val = a[nxt] - get_future(1, nxt, bk, next_mask)
                        else:
                            val = a[nxt] - large_back_turn(nxt, bk, next_mask)
                        if val > best:
                            best = val
                    cur0[off + mask] = best

        for gap in range(1, max_gap + 1):
            bk = fr - gap
            cnt = 1 << (gap - 1)
            off = OFF[gap]
            hi_back = min(n, bk + 4)
            for mask in range(cnt):
                best = None
                for nxt in range(bk + 1, hi_back + 1):
                    if nxt == fr:
                        continue
                    bit = nxt - bk - 1
                    if (mask >> bit) & 1:
                        continue
                    if nxt < fr:
                        idx = OFF[fr - nxt] + (mask >> (nxt - bk))
                        next_val = cur0[idx] if fr < n else -cur1[idx]
                    else:
                        next_val = get_future(1, nxt, fr, 0)
                    val = a[nxt] - next_val
                    if best is None or val > best:
                        best = val
                if best is None:
                    best = -cur0[off + mask] if fr < n else 0
                cur1[off + mask] = best

        if fr == n:
            for gap in range(1, max_gap + 1):
                cnt = 1 << (gap - 1)
                off = OFF[gap]
                for mask in range(cnt):
                    cur0[off + mask] = -cur1[off + mask]

        future[fr] = (cur0, cur1)
        old = fr + 5
        if old in future:
            del future[old]

    return future[2][1][0]


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    ptr = 1
    out = []
    for _ in range(t):
        n = data[ptr]
        ptr += 1
        a = [0] * (n + 1)
        for i in range(3, n + 1):
            a[i] = data[ptr]
            ptr += 1
        out.append(str(solve_case(n, a)))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
